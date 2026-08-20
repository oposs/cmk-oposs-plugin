# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
except that the first subsection is called `New` rather than `Added`.

This project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Changed

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
