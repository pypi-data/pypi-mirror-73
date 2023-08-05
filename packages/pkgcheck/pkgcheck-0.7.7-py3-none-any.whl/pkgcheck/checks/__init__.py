"""Core check classes."""

from collections import defaultdict

from snakeoil import klass
from snakeoil.cli.exceptions import UserException

from .. import addons, base, feeds, sources
from ..results import FilteredVersionResult, MetadataError
from ..caches import CachedAddon
from ..log import logger


class Check(feeds.Feed):
    """Base template for a check.

    :cvar scope: scope relative to the package repository the check runs under
    :cvar source: source of feed items
    :cvar known_results: result keywords the check can possibly yield
    """

    # check priority that affects runtime ordering
    _priority = 0
    # flag to allow package feed filtering
    _filtering = True
    known_results = frozenset()

    @klass.jit_attr
    def priority(self):
        # raise priority for checks that scan for metadata errors
        if self._priority == 0 and self.known_results & MetadataError.results:
            return -1
        return self._priority

    @property
    def source(self):
        # replace versioned pkg feeds with filtered ones as required
        if self._filtering and self.options.verbosity < 1 and self.scope is base.version_scope:
            filtered_results = [
                x for x in self.known_results if issubclass(x, FilteredVersionResult)]
            if filtered_results:
                partial_filtered = len(filtered_results) != len(self.known_results)
                return (
                    sources.FilteredRepoSource,
                    (sources.LatestPkgsFilter, partial_filtered),
                    (('source', self._source),)
                )
        return self._source

    @classmethod
    def skip(cls, namespace, skip=False):
        """Conditionally skip check when running all enabled checks."""
        if skip and namespace.forced_checks:
            return cls.__name__ not in namespace.forced_checks
        return skip

    def start(self):
        """Do startup here."""

    def finish(self):
        """Do cleanup and yield final results here."""
        yield from ()

    def __lt__(self, other):
        if self.priority == other.priority:
            return self.__class__.__name__ < other.__class__.__name__
        return self.priority < other.priority


class GentooRepoCheck(Check):
    """Check that is only run against the gentoo repo."""

    @classmethod
    def skip(cls, namespace, skip=False):
        if not skip:
            skip = not namespace.gentoo_repo
            if skip:
                logger.info(f'skipping {cls.__name__}, not running against gentoo repo')
        return super().skip(namespace, skip=skip)


class OverlayRepoCheck(Check):
    """Check that is only run against overlay repos."""

    @classmethod
    def skip(cls, namespace, skip=False):
        if not skip:
            skip = not namespace.target_repo.masters
            if skip:
                logger.info(f'skipping {cls.__name__}, not running against overlay repo')
        return super().skip(namespace, skip=skip)


class ExplicitlyEnabledCheck(Check):
    """Check that is only run when explicitly enabled."""

    @classmethod
    def skip(cls, namespace, skip=False):
        if not skip:
            if namespace.selected_checks is not None:
                disabled, enabled = namespace.selected_checks
            else:
                disabled, enabled = [], []

            # enable checks for selected keywords
            keywords = namespace.filtered_keywords
            if keywords is not None:
                keywords = keywords.intersection(cls.known_results)

            skip = cls.__name__ not in enabled and not keywords
            if skip:
                logger.info(f'skipping {cls.__name__}, not explicitly enabled')
        return super().skip(namespace, skip=skip)


class GitCheck(ExplicitlyEnabledCheck):
    """Check that is only run when explicitly enabled via the --commits git option."""

    @classmethod
    def skip(cls, namespace, skip=False):
        if not skip:
            skip = namespace.commits is None
            if skip:
                logger.info(f'skipping {cls.__name__}, not explicitly enabled')
        return super().skip(namespace, skip=skip)


class AsyncCheck(Check):
    """Check that schedules tasks to be run asynchronously."""


class NetworkCheck(AsyncCheck):
    """Check that is only run when network support is enabled."""

    required_addons = (addons.NetAddon,)

    def __init__(self, *args, net_addon):
        super().__init__(*args)
        self.timeout = self.options.timeout
        self.session = net_addon.session

    @classmethod
    def skip(cls, namespace, skip=False):
        if not skip:
            skip = not namespace.net
            if skip:
                logger.info(f'skipping {cls.__name__}, network checks not enabled')
        return super().skip(namespace, skip=skip)


class SkipOptionalCheck(UserException):
    """Check failed to initialize due to missing dependencies or other situation.

    Checks not explicitly selected will be skipped if they raise this during
    initialization.
    """

    def __init__(self, check, msg):
        check_name = check.__class__.__name__
        super().__init__(f'{check_name}: {msg}')


def init_checks(enabled_addons, options):
    """Initialize selected checks."""
    enabled = defaultdict(lambda: defaultdict(list))
    addons_map = {}
    source_map = {}
    caches = []

    if options.selected_checks is not None:
        _disabled, selected_checks = options.selected_checks
    else:
        _disabled, selected_checks = [], []

    for cls in enabled_addons:
        try:
            addon = addons.init_addon(cls, options, addons_map)
        except SkipOptionalCheck:
            if cls.__name__ in selected_checks:
                raise
            continue
        if isinstance(addon, Check):
            source = source_map.get(addon.source)
            if source is None:
                source = sources.init_source(addon.source, options, addons_map)
                source_map[addon.source] = source
            exec_type = 'async' if isinstance(addon, AsyncCheck) else 'sync'
            enabled[addon.scope][(source, exec_type)].append(addon)
        if isinstance(addon, CachedAddon):
            caches.append(addon)
    return enabled, caches
