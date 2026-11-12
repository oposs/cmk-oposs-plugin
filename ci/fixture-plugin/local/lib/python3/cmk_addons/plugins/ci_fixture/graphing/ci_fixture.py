from cmk.graphing.v1 import Title, metrics, perfometers

metric_ci_fixture_value = metrics.Metric(
    name="ci_fixture_value",
    title=Title("Value"),
    unit=metrics.Unit(metrics.DecimalNotation("")),
    color=metrics.Color.BLUE,
)

perfometer_ci_fixture_value = perfometers.Perfometer(
    name="ci_fixture_value",
    focus_range=perfometers.FocusRange(perfometers.Closed(0), perfometers.Open(100)),
    segments=["ci_fixture_value"],
)
