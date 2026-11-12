# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
except that the first subsection is called `New` rather than `Added`.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### New

- `04-check-plugins.md` documents one check plugin consuming several sections: the
  `section_<name>` argument convention and its ordering, that Checkmk validates the
  signature at load time, that any section may arrive as `None`, and that annotating the
  parameters on a multi-section plugin requires `| None`. None of this was covered, and
  the argument naming is not guessable - it is enforced in
  `cmk/base/api/agent_based/register/utils.py`.
- `02-snmp-plugins.md` documents splitting a section to control fetch cost: a section is
  the unit of both fetching and caching, `snmp_check_interval` can only slow a section
  down, so bundling a cheap fast-moving tree with an expensive slow-moving one makes a
  short check interval unaffordable. Includes measured per-row costs from a Nokia ISAM
  (5.8 ms/row versus 23 ms/row, because the second table reads SFP hardware on demand)
  and how to read `cmk_time_snmp` off the `Check_MK` service to find where time goes.

### Changed

- The test harness now tests against the Checkmk tag `v2.3.0p52`. `CMK_VERSION = "2.3.0"`
  named the 2.3.0 maintenance branch, not a release, so a cached `.cmk-api/` and a fresh
  CI clone could test against different code.
- The harness `pytest.ini` writes pytest's temporary files to `.pytest-tmp/` in the
  project instead of the system temp dir, and the setup steps add `.pytest-tmp/` to
  `.gitignore` next to `.cmk-api/`.
- `08-testing-debugging.md` shows how to test against Checkmk 2.4: a `v2.4.0p…` tag and
  the `cmk-ccc` package in `API_PACKAGES`, which became separate in 2.4.
- `08-testing-debugging.md` and the harness `conftest.py` tell plugin authors to set
  `CMK_VERSION` to the tag matching `version.packaged` in `.mkp-builder.ini`, and say why a
  branch is wrong: it changes the test results without a commit in the plugin.
  The `version.packaged` examples in `SKILL.md` and `mkp-builder.md` now show
  `2.3.0p52` instead of `2.3.0p34`, so they match the pinned tag.

- The skill now lives in its own repository. It was part of `oposs/mkp-builder`, so a
  skill change cut a release of the packaging action and an action change told skill users
  their skill had updated; neither was true. The action stays at `oposs/mkp-builder` and
  this skill documents it.
- Release and validation workflows are no longer shipped with the skill. They belong to
  `oposs/repo-infra`, which installs one standard release flow across every repository.
  The `assets/release.yml` and `assets/validate.yml` artifacts are gone.

## 2.3.0 - 2026-08-20

Released as part of `oposs/mkp-builder`; see that repository for history up to this point.

### New

- A test harness the skill installs into a plugin repo, running pytest against the real
  Checkmk API pulled from Checkmk and pinned to the targeted version.
