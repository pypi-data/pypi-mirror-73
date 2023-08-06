import re

import pytest
from _pytest import fixtures

from pytest_alembic.plugin.error import AlembicReprError, AlembicTestFailure


def collect_all_tests():
    from pytest_alembic import tests

    all_tests = {}
    for name in dir(tests):
        if name.startswith("test_"):
            all_tests[name[5:]] = getattr(tests, name)

    return all_tests


def parse_raw_test_names(raw_test_names):
    test_names = re.split(r"[,\n]", raw_test_names)

    result = []
    for test_name in test_names:
        test_name = test_name.strip()
        if not test_name:
            continue
        result.append(test_name)
    return result


def enabled_test_names(all_test_names, raw_included_tests="", raw_excluded_tests=""):
    if raw_included_tests:
        included_tests = set(parse_raw_test_names(raw_included_tests))
        invalid_tests = included_tests - all_test_names
        if invalid_tests:
            invalid_str = ", ".join(sorted(invalid_tests))
            raise ValueError(f"The following tests were unrecognized: {invalid_str}")

        return included_tests

    excluded_tests = set(parse_raw_test_names(raw_excluded_tests))
    invalid_tests = excluded_tests - all_test_names
    if invalid_tests:
        invalid_str = ", ".join(sorted(invalid_tests))
        raise ValueError(f"The following tests were unrecognized: {invalid_str}")

    return all_test_names - excluded_tests


def collect_tests(session, config):
    cli_enabled = config.option.pytest_alembic_enabled
    if not cli_enabled:
        return []

    option = config.option
    raw_included_tests = config.getini("pytest_alembic_include")
    raw_excluded_tests = option.pytest_alembic_exclude or config.getini("pytest_alembic_exclude")

    all_tests = collect_all_tests()
    test_names = enabled_test_names(set(all_tests), raw_included_tests, raw_excluded_tests)

    tests_folder = config.getini("pytest_alembic_tests_folder")

    result = []
    for test_name in sorted(test_names):
        test = all_tests[test_name]

        result.append(
            PytestAlembicItem.from_parent(
                session, name=f"{tests_folder}::pytest_alembic::{test.__name__}", test_fn=test
            )
        )

    return result


class PytestAlembicItem(pytest.Item):
    obj = None

    @classmethod
    def from_parent(cls, parent, *, name, test_fn):
        kwargs = dict(name=name, parent=parent, nodeid=name)
        if hasattr(super(), "from_parent"):
            self = super().from_parent(**kwargs)
        else:
            self = cls(**kwargs)

        self.test_fn = test_fn
        self.funcargs = {}
        self.add_marker("alembic")
        return self

    def runtest(self):
        fm = self.session._fixturemanager
        self._fixtureinfo = fm.getfixtureinfo(node=self, func=self.test_fn, cls=None)

        fixture_request = fixtures.FixtureRequest(self)
        fixture_request._fillfixtures()

        params = {arg: self.funcargs[arg] for arg in self._fixtureinfo.argnames}

        self.test_fn(**params)

    def reportinfo(self):
        return (self.fspath, 0, f"[pytest-alembic] {self.name}")

    def repr_failure(self, excinfo):
        if isinstance(excinfo.value, AlembicTestFailure):
            return AlembicReprError(excinfo, self)
        return super().repr_failure(excinfo)
