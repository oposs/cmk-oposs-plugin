"""Exercises the bakery stub the harness ships in tests/cmk_stubs/."""

from cmk.base.plugins.bakery.bakery_api.v1 import OS, Plugin, register


def get_ci_fixture_files(conf):
    yield Plugin(base_os=OS.LINUX, source="ci_fixture")


register.bakery_plugin(name="ci_fixture", files_function=get_ci_fixture_files)
