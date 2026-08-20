# cmk-oposs-plugin

A Claude Code skill for building, upgrading and packaging **Checkmk 2.3.x** monitoring
plugins: agent-based and SNMP checks, special agents, metrics and graphing, rulesets, the
agent bakery, notifications, and MKP packaging.

## Install

```
/plugin marketplace add oposs/claude-plugins
/plugin install cmk-oposs-plugin
```

The skill then triggers on its own whenever you work on a Checkmk plugin — a repo with
`.mkp-builder.ini`, files under `local/lib/python3/`, or anything importing `cmk.*`.

## What is here

```
skills/checkmk-plugin/
  SKILL.md          the task router and the conventions that cause silent failures
  references/       fourteen deep references, read on demand
  assets/           the test harness a plugin repo installs, and a CHANGES.md template
  evals/            triggering and behaviour evals for the skill
```

## What is deliberately not here

**The MKP builder action.** `oposs/mkp-builder` is a GitHub Action that packages a plugin
into an `.mkp`. This skill documents how to use it; it does not contain it. The two were one
repository until they were split, which meant every skill change cut a new release of the
action and every action change told skill users their skill had updated.

**Release and CI workflows.** Those belong to
[`oposs/repo-infra`](https://github.com/oposs/repo-infra), which installs one standard
release flow, changelog handling, branch protection and a `ci.yml` across every repository
rather than a per-ecosystem copy. In a plugin repo, run `/repo-infra:check`.

The seam between the three is a single line in the CI workflow repo-infra generates:
`uses: oposs/mkp-builder@v2`.

## Test harness

A Checkmk plugin imports `cmk.agent_based`, `cmk.graphing`, `cmk.rulesets` and
`cmk.server_side_calls`, none of which exist outside a Checkmk installation — which is why
so many plugin repos have no tests at all. `assets/tests/` fixes that: `conftest.py` fetches
the API from Checkmk itself, pinned to the version the plugin targets, so the suite runs
against the real thing rather than against stubs. Raising that pin is how you find out what
a Checkmk upgrade breaks.

See `skills/checkmk-plugin/references/08-testing-debugging.md`.

## License

See [LICENSE](LICENSE).
