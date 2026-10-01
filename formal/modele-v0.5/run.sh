#!/bin/zsh
# ./run.sh MC_NAME [extra TLC args]; preserve TLC's exit status.
set -u
cd "$(dirname "$0")" || exit 1
if (( $# < 1 )); then echo "usage: ./run.sh MC_NAME [TLC args]" >&2; exit 2; fi
NAME=$1
shift
if [[ ! "$NAME" =~ ^[A-Za-z][A-Za-z0-9_]*$ ]]; then exit 2; fi
mkdir -p logs
JAVA=${TLC_JAVA:-/opt/homebrew/opt/openjdk@21/bin/java}
RUN_DIR=$(mktemp -d "${TMPDIR:-/tmp}/n-tlc-${NAME}.XXXXXX") || exit 1
trap 'rm -rf -- "$RUN_DIR"' EXIT
"${JAVA%/java}/javac" -cp tla2tools.jar -d "$RUN_DIR" tools/LocalTLC.java || exit $?
"$JAVA" -XX:+UseParallelGC -Xmx3g -Djava.io.tmpdir="$RUN_DIR" -cp "${RUN_DIR}:tla2tools.jar" LocalTLC \
  -workers "${TLC_WORKERS:-4}" -seed 1 -metadir "logs/states_$NAME" \
  -config "$NAME.cfg" "$NAME.tla" "$@" > "logs/$NAME.log" 2>&1
rc=$?
echo "exit=$rc" >> "logs/$NAME.log"
exit "$rc"
