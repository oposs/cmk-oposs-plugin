# Releasing

This repo ships one thing: the **`cmk-oposs-plugin` Claude Code skill**. Users install it
from [`oposs/claude-plugins`](https://github.com/oposs/claude-plugins).

`.claude-plugin/plugin.json` is the single source of truth for the version. Claude Code
resolves `plugin.json → marketplace entry → commit SHA`, and `plugin.json` wins — which is
why the marketplace entry carries **no** `version` field for this plugin. A stale duplicate
there silently masks the real one.

## Why the version bump matters

Claude caches a plugin under its resolved version and reads the skill from
`~/.claude/plugins/cache/<marketplace>/<plugin>/<version>/`.

**Merging a skill fix without moving the version ships nothing.** Every Claude keeps
reading the old cached copy, with no error and no signal that anything is stale. While this
was a manual step it was missed often enough that an installed copy was found ten commits
and three merged skill fixes behind `main`.

So: a skill change is not released until `plugin.json` moves.

## Cutting a release

1. Make the change under `skills/`, add a `CHANGES.md` entry under `## [Unreleased]`, and
   merge to `main`.
2. Bump `version` in `.claude-plugin/plugin.json` and roll the `[Unreleased]` section into
   a dated one.
3. Tag it.

Users then run `/plugin marketplace update` followed by `/plugin update cmk-oposs-plugin`.

## The marketplace moves on its own

Claude only re-resolves plugin versions when it re-fetches the marketplace, so
`oposs/claude-plugins` has to move as well. That is handled from the other side: it runs an
hourly **Track plugin versions** workflow that reads this repository's `plugin.json` and
commits when the version changes.

That direction was chosen deliberately. A push from here would need a credential for
another repository (the org restricts fine-grained PATs, leaving a deploy key or a GitHub
App). Polling from the marketplace needs no credential at all, covers every plugin instead
of only those wired up to push, and still catches a version bumped outside a release.

## Adopting repo-infra

Steps 2 and 3 above are hand work, and they are exactly what
[`oposs/repo-infra`](https://github.com/oposs/repo-infra) automates: a two-step release
where merging a release PR rolls `CHANGES.md`, bumps every declared version file, tags, and
publishes. Run `/repo-infra:check` here to see what it would install.
