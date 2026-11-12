#!/bin/sh
# Install the skill's test harness into a scratch plugin the way
# references/08-testing-debugging.md tells plugin authors to, then check that
# it fetches the pinned Checkmk API, passes a working plugin and fails a
# broken one.
#
# usage: ci/test-harness.sh <empty-work-dir>
# PYTHON selects the interpreter (default: python3); it needs requirements-dev.txt.
set -eu

REPO=$(cd "$(dirname "$0")/.." && pwd)
ASSETS=$REPO/skills/checkmk-plugin/assets
PYTHON=${PYTHON:-python3}
WORK=${1:?usage: $0 <empty-work-dir>}

fail() { echo "FAIL: $*" >&2; exit 1; }

# The docs quote the pinned tag; they must name the one the template uses.
pin=$(sed -n 's/^CMK_VERSION = "\(.*\)"$/\1/p' "$ASSETS/tests/conftest.py")
[ -n "$pin" ] || fail "no CMK_VERSION in assets/tests/conftest.py"
grep -q "CMK_VERSION = \"$pin\"" "$REPO/skills/checkmk-plugin/references/08-testing-debugging.md" \
    || fail "08-testing-debugging.md does not quote CMK_VERSION = \"$pin\""
grep -q "(\`$pin\`)" "$REPO/skills/checkmk-plugin/SKILL.md" \
    || fail "SKILL.md does not name $pin"

mkdir -p "$WORK"
[ -z "$(ls -A "$WORK")" ] || fail "$WORK is not empty"
cp -r "$REPO/ci/fixture-plugin/." "$WORK/"
cd "$WORK"

# The install steps from 08-testing-debugging.md
mkdir -p tests
cp -r "$ASSETS/tests/."              tests/
cp    "$ASSETS/pytest.ini"           pytest.ini
cp    "$ASSETS/requirements-dev.txt" requirements-dev.txt
printf '.cmk-api/\n.pytest-tmp/\n' >> .gitignore

echo "== working plugin, fresh fetch of the Checkmk $pin API"
"$PYTHON" -m pytest -q -p no:cacheprovider
[ -d ".cmk-api/$pin/packages/cmk-agent-based" ] || fail "the Checkmk API was not fetched"

echo "== broken plugin module must fail"
cp "$REPO/ci/broken-module/broken.py" local/lib/python3/cmk_addons/plugins/ci_fixture/agent_based/
if "$PYTHON" -m pytest -q -p no:cacheprovider > broken.log 2>&1; then
    cat broken.log
    fail "the harness passed a module that imports a name Checkmk does not have"
fi
grep -q NoSuchName broken.log || { cat broken.log; fail "the failure does not name the missing import"; }
echo "OK: the broken module failed as expected"
