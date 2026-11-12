# Imports a name the Checkmk API does not have. The harness must fail on it.
from cmk.agent_based.v2 import NoSuchName  # noqa: F401
