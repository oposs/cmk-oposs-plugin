# MKP Builder Reference

## Overview

The `oposs/mkp-builder` GitHub Action builds Checkmk MKP packages from a standard local directory structure. It is a community tool, not officially affiliated with Checkmk GmbH.

## Configuration File

Create `.mkp-builder.ini` in your repository root:

```ini
[package]
name = my_plugin
title = My Awesome Plugin
author = John Doe <john@example.com>
description = A plugin that does amazing things.
    This description can span multiple lines
    and provides better formatting options.

# Checkmk Compatibility
version.min_required = 2.3.0p1
version.packaged = 2.3.0p34
version.usable_until = 3.0.0

# Optional
download_url = https://github.com/user/repo
validate_python = true
```

## Required Directory Structure

```
repository/
+-- local/
|   +-- lib/python3/
|   |   +-- cmk_addons/plugins/
|   |   |   \-- your_plugin/
|   |   |       +-- agent_based/
|   |   |       +-- checkman/
|   |   |       +-- graphing/
|   |   |       +-- rulesets/
|   |   |       +-- server_side_calls/
|   |   |       \-- libexec/
|   |   \-- cmk/base/cee/plugins/bakery/
|   |       \-- your_plugin.py
|   \-- share/check_mk/
|       +-- agents/plugins/
|       |   \-- your_plugin
|       \-- notifications/
|           \-- your_notification.py
+-- .mkp-builder.ini
\-- .github/workflows/release.yml
```

## GitHub Action Usage

### Basic
```yaml
- name: Build MKP
  uses: oposs/mkp-builder@v2
  with:
    version: '1.2.3'
```

### Full Options
```yaml
- name: Build MKP
  id: build-mkp
  uses: oposs/mkp-builder@v2
  with:
    version: ${{ steps.version.outputs.version }}
    package-name: 'my_plugin'
    title: 'My Plugin'
    author: 'Name <email>'
    description: 'What it does'
    version-min-required: '2.3.0p1'
    version-packaged: '2.3.0p34'
    version-usable-until: '3.0.0'
    validate-python: 'true'
    verbose: 'true'
    output-dir: '.'
```

### Inputs

| Input | Required | Default | Description |
|-------|----------|---------|-------------|
| `version` | Yes | - | Package version (semver, e.g., 1.2.3) |
| `package-name` | No | Auto-detected | Package name |
| `title` | No | From config | Package title |
| `author` | No | From config | Author name and email |
| `description` | No | From config | Package description |
| `version-min-required` | No | From config | Minimum Checkmk version |
| `version-packaged` | No | From config | Checkmk packaging version |
| `version-usable-until` | No | From config | Max compatible Checkmk version |
| `download-url` | No | From config | Download URL |
| `output-dir` | No | `.` | Output directory |
| `validate-python` | No | `true` | Validate Python syntax |
| `verbose` | No | `false` | Verbose logging |

### Outputs

| Output | Description |
|--------|-------------|
| `package-file` | Path to the created .mkp file |
| `package-name` | Name of the built package |
| `package-size` | Size of the package |

## Release workflows

Not here. Release and validation workflows are installed by
[`oposs/repo-infra`](https://github.com/oposs/repo-infra), which owns one standard release
flow across every repository rather than a per-ecosystem copy. Run `/repo-infra:check` in
the plugin repo to see what it would install.

What repo-infra installs calls this action; the two halves meet at
`uses: oposs/mkp-builder@v2`. Its inputs and outputs are documented above.

## MKP package format

Not here. What an `.mkp` actually is — the tar-of-tars layout, the `info` and `info.json`
metadata, and how files under `local/` map into each component archive — is documented by
the action that produces it:
[`cmk-mkp-format.md`](https://github.com/oposs/mkp-builder/blob/main/cmk-mkp-format.md).

You do not need it to build a plugin. Put the files in the layout described under
[Required Directory Structure](#required-directory-structure) above and the action does the
packing. Read it when you are debugging a package that installs but behaves oddly, or
adding a component type this skill does not cover.

## Troubleshooting

| Error | Fix |
|-------|-----|
| "No MKP file found" | Check `local/` directory structure, validate `.mkp-builder.ini` syntax |
| "Package name could not be determined" | Set `name` in `.mkp-builder.ini` or pass `package-name` input |
| "Python syntax error" | Fix Python errors or set `validate-python: 'false'` |

## Local Testing

The build script can also be run locally (it's a standalone Python 3 script using only stdlib):

```bash
python3 mkp-builder.py --version 1.0.0 --verbose
```

## Version Pinning

```yaml
# Exact version (production)
- uses: oposs/mkp-builder@v2.0.3

# Major version (gets fixes)
- uses: oposs/mkp-builder@v2

# Latest (development only)
- uses: oposs/mkp-builder@main
```
