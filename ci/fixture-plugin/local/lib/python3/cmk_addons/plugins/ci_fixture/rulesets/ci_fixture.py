from cmk.rulesets.v1 import Title
from cmk.rulesets.v1.form_specs import (
    DefaultValue,
    DictElement,
    Dictionary,
    Integer,
    LevelDirection,
    SimpleLevels,
)
from cmk.rulesets.v1.rule_specs import CheckParameters, HostAndItemCondition, Topic


def _form() -> Dictionary:
    return Dictionary(
        elements={
            "levels": DictElement(
                parameter_form=SimpleLevels(
                    title=Title("Upper levels"),
                    level_direction=LevelDirection.UPPER,
                    form_spec_template=Integer(),
                    prefill_fixed_levels=DefaultValue((10, 20)),
                ),
                required=True,
            ),
        },
    )


rule_spec_ci_fixture = CheckParameters(
    name="ci_fixture",
    title=Title("CI fixture"),
    topic=Topic.GENERAL,
    parameter_form=_form,
    condition=HostAndItemCondition(item_title=Title("Item")),
)
