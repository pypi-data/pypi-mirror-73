from snakeoil.cli import arghparse

from pkgcheck import objects
from pkgcheck.checks import init_checks


def test_checks():
    """Scan through all public checks and verify various aspects."""
    for name, cls in objects.CHECKS.items():
        assert cls.known_results, f"check class {name!r} doesn't define known results"


def test_check_scope(tool):
    """Verify check scopes match their source scopes."""
    namespace = arghparse.Namespace()
    # forcibly enable all checks so none are skipped
    namespace.forced_checks = [name for name, _cls in objects.CHECKS.items()]
    options, _func = tool.parse_args(['scan'], namespace)
    enabled_checks, _ = init_checks(options.addons, options)
    for scope, d in enabled_checks.items():
        for (source, is_async), runners in d.items():
            for check in runners:
                assert check.scope == source.feed_type, \
                    f"check scope doesn't match source scope: {check}"


def test_keywords():
    """Scan through all public result keywords and verify various aspects."""
    for name, cls in objects.KEYWORDS.items():
        assert cls.level is not None, f"result class {name!r} missing level"
