"""Git specific support and addon."""

import argparse
import os
import pickle
import shlex
import subprocess
import sys
from collections import UserDict
from contextlib import AbstractContextManager
from functools import partial

from pathspec import PathSpec
from pkgcore.ebuild import cpv
from pkgcore.ebuild.atom import MalformedAtom
from pkgcore.ebuild.atom import atom as atom_cls
from pkgcore.repository import multiplex
from pkgcore.repository.util import SimpleTree
from pkgcore.restrictions import packages, values
from snakeoil.cli.exceptions import UserException
from snakeoil.demandload import demand_compile_regexp
from snakeoil.iterables import partition
from snakeoil.klass import jit_attr
from snakeoil.osutils import pjoin
from snakeoil.process import CommandNotFound, find_binary
from snakeoil.process.spawn import spawn_get_output
from snakeoil.strings import pluralism

from . import base, caches, objects
from .checks import GitCheck
from .log import logger

# hacky path regexes for git log parsing, proper validation is handled later
_ebuild_path_regex_raw = '([^/]+)/([^/]+)/([^/]+)\\.ebuild'
_ebuild_path_regex = '(?P<category>[^/]+)/(?P<PN>[^/]+)/(?P<P>[^/]+)\\.ebuild'
demand_compile_regexp('ebuild_ADM_regex', fr'^(?P<status>[ADM])\t{_ebuild_path_regex}$')
demand_compile_regexp('ebuild_R_regex', fr'^(?P<status>R)\d+\t{_ebuild_path_regex}\t{_ebuild_path_regex_raw}$')
demand_compile_regexp('eclass_regex', r'^eclass/(?P<eclass>\S+)\.eclass$')


class GitCommit:
    """Git commit objects."""

    def __init__(self, hash, commit_date, author, committer, message):
        self.hash = hash
        self.commit_date = commit_date
        self.author = author
        self.committer = committer
        self.message = message

    def __str__(self):
        return self.hash

    def __eq__(self, other):
        return self.hash == other.hash


class GitPkgChange:
    """Git package change objects."""

    def __init__(self, atom, status, commit):
        self.atom = atom
        self.status = status
        self.commit = commit


class ParsedGitRepo(UserDict, caches.Cache):
    """Parse repository git logs."""

    # git command to run on the targeted repo
    _git_cmd = 'git log --name-status --date=short --diff-filter=ARMD'

    def __init__(self, repo, commit=None, **kwargs):
        super().__init__()
        self.location = repo.location
        self._cache = GitAddon.cache

        if commit is None:
            self.commit = 'origin/HEAD..master'
            self._pkg_changes(commit=self.commit, **kwargs)
        else:
            self.commit = commit
            self._pkg_changes(**kwargs)

    def update(self, commit, **kwargs):
        """Update an existing repo starting at a given commit hash."""
        self._pkg_changes(commit=self.commit, **kwargs)
        self.commit = commit

    @staticmethod
    def _parse_file_line(line):
        """Pull atoms and status from file change lines."""
        # match initially added ebuilds
        match = ebuild_ADM_regex.match(line)
        if match:
            status = match.group('status')
            category = match.group('category')
            pkg = match.group('P')
            try:
                return atom_cls(f'={category}/{pkg}'), status
            except MalformedAtom:
                return None

        # match renamed ebuilds
        match = ebuild_R_regex.match(line)
        if match:
            status = match.group('status')
            category = match.group('category')
            pkg = match.group('P')
            try:
                return atom_cls(f'={category}/{pkg}'), status
            except MalformedAtom:
                return None

    @classmethod
    def parse_git_log(cls, repo_path, git_cmd=None, commit=None,
                      pkgs=False, debug=False):
        """Parse git log output."""
        if git_cmd is None:
            git_cmd = cls._git_cmd
        cmd = shlex.split(git_cmd) if isinstance(git_cmd, str) else git_cmd
        # custom git log format, see the "PRETTY FORMATS" section of the git
        # log man page for details
        format_lines = [
            '# BEGIN COMMIT',
            '%h', # abbreviated commit hash
            '%cd', # commit date
            '%an <%ae>', # Author Name <author@email.com>
            '%cn <%ce>', # Committer Name <committer@email.com>
            '%B', # commit message
            '# END MESSAGE BODY',
        ]
        format_str = '%n'.join(format_lines)
        cmd.append(f'--pretty=tformat:{format_str}')

        if commit:
            if '..' in commit:
                cmd.append(commit)
            else:
                cmd.append(f'{commit}..origin/HEAD')
        else:
            cmd.append('origin/HEAD')

        git_log = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=repo_path)
        line = git_log.stdout.readline().decode().strip()
        if git_log.poll():
            error = git_log.stderr.read().decode().strip()
            logger.warning('skipping git checks: %s', error)
            return {}

        count = 1
        with base.ProgressManager(debug=debug) as progress:
            while line:
                hash = git_log.stdout.readline().decode().strip()
                commit_date = git_log.stdout.readline().decode().strip()
                author = git_log.stdout.readline().decode('utf-8', 'replace').strip()
                committer = git_log.stdout.readline().decode('utf-8', 'replace').strip()

                message = []
                while True:
                    line = git_log.stdout.readline().decode('utf-8', 'replace').strip('\n')
                    if line == '# END MESSAGE BODY':
                        # drop trailing newline if it exists
                        if not message[-1]:
                            message.pop()
                        break
                    message.append(line)

                # update progress output
                progress(f'{hash} commit #{count}, {commit_date}')
                count += 1

                commit = GitCommit(hash, commit_date, author, committer, message)
                if not pkgs:
                    yield commit

                # file changes
                while True:
                    line = git_log.stdout.readline().decode()
                    if line == '# BEGIN COMMIT\n' or not line:
                        break
                    if pkgs:
                        parsed = cls._parse_file_line(line.strip())
                        if parsed is not None:
                            atom, status = parsed
                            yield GitPkgChange(atom, status, commit)

    def _pkg_changes(self, local=False, **kwargs):
        """Parse package changes from git log output."""
        cmd = shlex.split(self._git_cmd)

        seen = set()
        for pkg in self.parse_git_log(self.location, cmd, pkgs=True, **kwargs):
            atom = pkg.atom
            key = (atom, pkg.status)
            if key not in seen:
                seen.add(key)
                self.data.setdefault(atom.category, {}).setdefault(
                    atom.package, {})[(atom.fullver, pkg.status)] = {
                        'date': pkg.commit.commit_date,
                        'status': pkg.status,
                        'commit': pkg.commit.hash if not local else pkg.commit,
                    }


class _GitCommitPkg(cpv.VersionedCPV):
    """Fake packages encapsulating commits parsed from git log."""

    def __init__(self, *args, date, status, commit):
        super().__init__(*args)

        # add additional attrs
        sf = object.__setattr__
        sf(self, 'date', date)
        sf(self, 'status', status)
        sf(self, 'commit', commit)


class _HistoricalRepo(SimpleTree):
    """Repository encapsulating historical git data."""

    # selected pkg status filter
    _status_filter = None

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('pkg_klass', _GitCommitPkg)
        super().__init__(*args, **kwargs)

    def _get_versions(self, cp_key):
        versions = []
        for (version, status), data in self.cpv_dict[cp_key[0]][cp_key[1]].items():
            if self._status_filter is None or status in self._status_filter:
                versions.append((version, data))
        return tuple(versions)

    def _internal_gen_candidates(self, candidates, sorter, raw_pkg_cls, **kwargs):
        for cp in sorter(candidates):
            yield from sorter(
                raw_pkg_cls(cp[0], cp[1], ver, **data)
                for ver, data in self.versions.get(cp, ()))


class GitChangedRepo(_HistoricalRepo):
    """Historical git repo consisting of the latest changed packages."""


class GitModifiedRepo(_HistoricalRepo):
    """Historical git repo consisting of the latest modified packages."""

    _status_filter = frozenset(['A', 'R', 'M'])


class GitAddedRepo(_HistoricalRepo):
    """Historical git repo consisting of added packages."""

    _status_filter = frozenset(['A', 'R'])


class GitRemovedRepo(_HistoricalRepo):
    """Historical git repo consisting of removed packages."""

    _status_filter = frozenset(['D'])


class _ScanCommits(argparse.Action):
    """Argparse action that enables git commit checks."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __call__(self, parser, namespace, value, option_string=None):
        namespace.forced_checks.extend(
            name for name, cls in objects.CHECKS.items() if issubclass(cls, GitCheck))
        setattr(namespace, self.dest, value)


class GitStash(AbstractContextManager):
    """Context manager for stashing untracked or modified/uncommitted files.

    This assumes that no git actions are performed on the repo while a scan is
    underway otherwise `git stash` usage may cause issues.
    """

    def __init__(self, parser, repo):
        self.parser = parser
        self.repo = repo
        self._stashed = False

    def __enter__(self):
        # check for untracked or modified/uncommitted files
        p = subprocess.run(
            ['git', 'ls-files', '-mo', '--exclude-standard'],
            stdout=subprocess.PIPE, stderr=subprocess.DEVNULL,
            cwd=self.repo.location, encoding='utf8')
        if p.returncode != 0 or not p.stdout:
            return

        # stash all existing untracked or modified/uncommitted files
        p = subprocess.run(
            ['git', 'stash', 'push', '-u', '-m', 'pkgcheck scan --commits'],
            stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
            cwd=self.repo.location, encoding='utf8')
        if p.returncode != 0:
            error = p.stderr.splitlines()[0]
            self.parser.error(f'git failed stashing files: {error}')
        self._stashed = True

    def __exit__(self, _exc_type, _exc_value, _traceback):
        if self._stashed:
            # apply previously stashed files back to the working tree
            p = subprocess.run(
                ['git', 'stash', 'pop'],
                stdout=subprocess.DEVNULL, stderr=subprocess.PIPE,
                cwd=self.repo.location, encoding='utf8')
            if p.returncode != 0:
                error = p.stderr.splitlines()[0]
                self.parser.error(f'git failed applying stash: {error}')


class GitAddon(base.Addon, caches.CachedAddon):
    """Git repo support for various checks.

    Pkgcheck can create virtual package repos from a given git repo's history
    in order to provide more info for checks relating to stable requests,
    outdated blockers, or local commits. These virtual repos are cached and
    updated every run if new commits are detected.

    Git repos must have a supported config in order to work properly.
    Specifically, pkgcheck assumes that both origin and master branches exist
    and relate to the upstream and local development states, respectively.

    Additionally, the origin/HEAD ref must exist. If it doesn't, running ``git
    fetch origin`` should create it. Otherwise, using ``git remote set-head
    origin master`` or similar will also create the reference.
    """

    # cache registry
    cache = caches.CacheData(type='git', file='git.pickle', version=3)

    @classmethod
    def mangle_argparser(cls, parser):
        group = parser.add_argument_group('git', docs=cls.__doc__)
        group.add_argument(
            '--commits', action=_ScanCommits, nargs='?',
            metavar='COMMIT', const='origin', default=None,
            help="determine scan targets from local git repo commits",
            docs="""
                For a local git repo, pkgcheck will determine targets to scan
                from the committed changes compared to a given reference that
                defaults to the repo's origin.

                For example, to scan all the packages that have been changed in
                the current branch compared to the branch named 'old' use
                ``pkgcheck scan --commits old``. For two separate branches
                named 'old' and 'new' use ``pkgcheck scan --commits old..new``.

                Note that will also enable eclass-specific checks if it
                determines any commits have been made to eclasses.
            """)

    @staticmethod
    def _committed_eclass(committed, eclass):
        """Stub method for matching eclasses against commits."""
        return eclass in committed

    @staticmethod
    def _pkg_atoms(paths):
        """Filter package atoms from commit paths."""
        for x in paths:
            try:
                yield atom_cls(os.sep.join(x.split(os.sep, 2)[:2]))
            except MalformedAtom:
                continue

    @classmethod
    def check_args(cls, parser, namespace):
        if namespace.commits:
            if namespace.targets:
                targets = ' '.join(namespace.targets)
                s = pluralism(namespace.targets)
                parser.error(f'--commits is mutually exclusive with target{s}: {targets}')

            ref = namespace.commits
            repo = namespace.target_repo
            targets = list(repo.category_dirs)
            if os.path.isdir(pjoin(repo.location, 'eclass')):
                targets.append('eclass')
            try:
                p = subprocess.run(
                    ['git', 'diff', '--cached', ref, '--name-only'] + targets,
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                    cwd=repo.location, encoding='utf8')
            except FileNotFoundError:
                parser.error('git not available to determine targets for --commits')

            if p.returncode != 0:
                error = p.stderr.splitlines()[0]
                parser.error(f'failed running git: {error}')
            elif not p.stdout:
                # no changes exist, exit early
                parser.exit()

            pkgs, eclasses = partition(
                p.stdout.splitlines(), predicate=lambda x: x.startswith('eclass/'))
            pkgs = sorted(cls._pkg_atoms(pkgs))
            eclasses = filter(None, (eclass_regex.match(x) for x in eclasses))
            eclasses = sorted(x.group('eclass') for x in eclasses)

            restrictions = []
            if pkgs:
                restrict = packages.OrRestriction(*pkgs)
                restrictions.append((base.package_scope, restrict))
            if eclasses:
                func = partial(cls._committed_eclass, frozenset(eclasses))
                restrict = values.AnyMatch(values.FunctionRestriction(func))
                restrictions.append((base.eclass_scope, restrict))

            # no pkgs or eclasses to check, exit early
            if not restrictions:
                parser.exit()

            namespace.contexts.append(GitStash(parser, repo))
            namespace.restrictions = restrictions

    def __init__(self, *args):
        super().__init__(*args)
        # disable git support if git isn't installed
        if self.options.cache['git']:
            try:
                find_binary('git')
            except CommandNotFound:
                self.options.cache['git'] = False

        # mapping of repo locations to their corresponding git repo caches
        self._cached_repos = {}

    @jit_attr
    def gitignore(self):
        """Load a repo's .gitignore and .git/info/exclude files for path matching."""
        patterns = []
        for path in ('.gitignore', '.git/info/exclude'):
            try:
                with open(pjoin(self.options.target_repo.location, path)) as f:
                    patterns.extend(f)
            except FileNotFoundError:
                pass
            except IOError as e:
                logger.warning(f'failed reading {path!r}: {e}')
        return PathSpec.from_lines('gitwildmatch', patterns)

    def gitignored(self, path):
        """Determine if a given path in a repository is matched by .gitignore settings."""
        if path.startswith(self.options.target_repo.location):
            repo_prefix_len = len(self.options.target_repo.location) + 1
            path = path[repo_prefix_len:]
        return self.gitignore.match_file(path)

    @staticmethod
    def get_commit_hash(repo_location, commit='origin/HEAD'):
        """Retrieve a git repo's commit hash for a specific commit object."""
        if not os.path.exists(pjoin(repo_location, '.git')):
            raise ValueError
        ret, out = spawn_get_output(
            ['git', 'rev-parse', commit], cwd=repo_location)
        if ret != 0:
            raise ValueError(
                f'failed retrieving {commit} commit hash '
                f'for git repo: {repo_location}')
        return out[0].strip()

    def update_cache(self, output_lock, force=False):
        """Update related cache and push updates to disk."""
        try:
            # running from scan subcommand
            repos = self.options.target_repo.trees
        except AttributeError:
            # running from cache subcommand
            repos = self.options.domain.ebuild_repos

        if self.options.cache['git']:
            for repo in repos:
                try:
                    commit = self.get_commit_hash(repo.location)
                except ValueError as e:
                    continue

                # initialize cache file location
                cache_file = self.cache_file(repo)

                git_repo = None
                cache_repo = True
                if not force:
                    # try loading cached, historical repo data
                    try:
                        with open(cache_file, 'rb') as f:
                            git_repo = pickle.load(f)
                        if git_repo.version != self.cache.version:
                            logger.debug('forcing git repo cache regen due to outdated version')
                            os.remove(cache_file)
                            git_repo = None
                    except FileNotFoundError as e:
                        pass
                    except (AttributeError, EOFError, ImportError, IndexError) as e:
                        logger.debug('forcing git repo cache regen: %s', e)
                        os.remove(cache_file)
                        git_repo = None

                if (git_repo is not None and
                        repo.location == getattr(git_repo, 'location', None)):
                    if commit != git_repo.commit:
                        with output_lock:
                            old, new = git_repo.commit[:13], commit[:13]
                            print(
                                f'updating {repo} git repo cache: {old} -> {new}',
                                file=sys.stderr,
                            )
                        git_repo.update(commit, debug=self.options.debug)
                    else:
                        cache_repo = False
                else:
                    with output_lock:
                        print(
                            f'creating {repo} git repo cache: {commit[:13]}',
                            file=sys.stderr,
                        )
                    git_repo = ParsedGitRepo(repo, commit, debug=self.options.debug)

                if git_repo:
                    self._cached_repos[repo.location] = git_repo
                    # push repo to disk if it was created or updated
                    if cache_repo:
                        try:
                            os.makedirs(os.path.dirname(cache_file), exist_ok=True)
                            with open(cache_file, 'wb+') as f:
                                pickle.dump(git_repo, f)
                        except IOError as e:
                            msg = f'failed dumping git pkg repo: {cache_file!r}: {e.strerror}'
                            raise UserException(msg)

    def cached_repo(self, repo_cls, target_repo=None):
        cached_repo = None
        if target_repo is None:
            target_repo = self.options.target_repo

        if self.options.cache['git']:
            git_repos = []
            for repo in target_repo.trees:
                git_repo = self._cached_repos.get(repo.location, None)
                # only enable repo queries if history was found, e.g. a
                # shallow clone with a depth of 1 won't have any history
                if git_repo:
                    git_repos.append(repo_cls(git_repo, repo_id=f'{repo.repo_id}-history'))
                else:
                    logger.warning('skipping git checks for %s repo', repo)
                    break
            else:
                if len(git_repos) > 1:
                    cached_repo = multiplex.tree(*git_repos)
                elif len(git_repos) == 1:
                    cached_repo = git_repos[0]

        return cached_repo

    def commits_repo(self, repo_cls, target_repo=None, options=None):
        options = options if options is not None else self.options
        if target_repo is None:
            target_repo = options.target_repo

        git_repo = {}
        repo_id = f'{target_repo.repo_id}-commits'

        if options.cache['git']:
            try:
                origin = self.get_commit_hash(target_repo.location)
                master = self.get_commit_hash(target_repo.location, commit='master')
                if origin != master:
                    git_repo = ParsedGitRepo(target_repo, local=True)
            except ValueError as e:
                if str(e):
                    logger.warning('skipping git commit checks: %s', e)

        return repo_cls(git_repo, repo_id=repo_id)

    def commits(self, repo=None):
        path = repo.location if repo is not None else self.options.target_repo.location
        commits = iter(())

        if self.options.cache['git']:
            try:
                origin = self.get_commit_hash(path)
                master = self.get_commit_hash(path, commit='master')
            except ValueError as e:
                if str(e):
                    logger.warning('skipping git commit checks: %s', e)
                return commits

            if origin != master:
                commits = ParsedGitRepo.parse_git_log(path, commit='origin/HEAD..master')

        return commits
