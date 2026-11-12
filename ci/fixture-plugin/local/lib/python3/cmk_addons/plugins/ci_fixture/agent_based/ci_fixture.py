"""A minimal check plugin that touches the agent_based API the skill documents."""

from cmk.agent_based.v2 import (
    AgentSection,
    CheckPlugin,
    CheckResult,
    DiscoveryResult,
    Service,
    StringTable,
    check_levels,
)


def parse_ci_fixture(string_table: StringTable) -> dict[str, int]:
    return {line[0]: int(line[1]) for line in string_table}


def discover_ci_fixture(section: dict[str, int]) -> DiscoveryResult:
    for item in section:
        yield Service(item=item)


def check_ci_fixture(item: str, params: dict, section: dict[str, int]) -> CheckResult:
    if item in section:
        yield from check_levels(
            section[item],
            levels_upper=params["levels"],
            metric_name="ci_fixture_value",
            label="Value",
        )


agent_section_ci_fixture = AgentSection(name="ci_fixture", parse_function=parse_ci_fixture)

check_plugin_ci_fixture = CheckPlugin(
    name="ci_fixture",
    service_name="CI fixture %s",
    discovery_function=discover_ci_fixture,
    check_function=check_ci_fixture,
    check_default_parameters={"levels": ("fixed", (10, 20))},
    check_ruleset_name="ci_fixture",
)
