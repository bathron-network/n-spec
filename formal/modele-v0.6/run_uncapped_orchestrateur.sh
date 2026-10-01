#!/bin/zsh
# Complément orchestrateur : relance d'un seul vecteur sans plafond de temps, 8 workers, 6 Go.
# Usage : ./run_uncapped_orchestrateur.sh MC_fast_on_10   (log : logs/orchestrateur/NAME.log)
set -eu; cd "$(dirname "$0")"; NAME=$1
JAVA=/opt/homebrew/opt/openjdk@21/bin/java; OUT=logs/orchestrateur; CL=$OUT/classes-$NAME; ST=$OUT/states-$NAME
rm -rf "$CL" "$ST"; mkdir -p "$CL" "$ST"
"${JAVA%/java}/javac" -cp tla2tools.jar -d "$CL" tools/LocalTLC.java
{ echo "orchestrateur: $(date '+%F %T') workers=8 heap=6g no-cap seed=1 fp=0";
  "$JAVA" -XX:+UseParallelGC -Xmx6g -Djava.io.tmpdir="$ST" -cp "$CL:tla2tools.jar" LocalTLC -workers 8 -seed 1 -fp 0 -metadir "$ST" -config $NAME.cfg $NAME.tla; echo "exit=$?"; } > $OUT/$NAME.log 2>&1 || true
rm -rf "$CL" "$ST"; grep -h "completed\|violated\|states generated\|depth\|Finished in\|exit=" $OUT/$NAME.log | tail -5
