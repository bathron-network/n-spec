#!/bin/bash
# Run r2 : WAN émulé à charge réaliste. Blocs tous à taille maximale (2 820 + 262 144 o), espacés de τ candidat, tx de fond 4/s par nœud.
# Sous-phases de 45 min : W1-6 (P1, τ=6) W1-10 (P1, τ=10) W2-6 (P2, τ=6) W2-10 (P2, τ=10), 60 s entre elles. Pas de coupures. VPS seulement.
# Usage : run-wan.sh NAME T0 "PEERS" LISTEN RUNID
set -u
NAME=$1 T0=$2 PEERS=$3 LISTEN=$4 RUNID=$5
D=$(cd "$(dirname "$0")" && pwd); cd "$D"
PORT=29171; NODES=vps1,vps2; OUT=out/$RUNID; LOG=$OUT/phases-$NAME.log; mkdir -p $OUT
IF=$(ip route get 1.1.1.1 | awk '{for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}')
log() { echo "$(date +%s%N) $*" >> $LOG; }
netem_off() { sudo -n tc qdisc del dev "$IF" root 2>/dev/null; true; }
netem_on() {
  netem_off
  if sudo -n tc qdisc add dev "$IF" root handle 1: prio bands 4 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1 &&
     for b in 1 2 3; do sudo -n tc qdisc add dev "$IF" parent 1:$b fq_codel || exit 1; done &&
     sudo -n tc qdisc add dev "$IF" parent 1:4 handle 40: netem $1 &&
     sudo -n tc filter add dev "$IF" parent 1: protocol ip prio 1 u32 match ip dport $PORT 0xffff flowid 1:4 &&
     sudo -n tc filter add dev "$IF" parent 1: protocol ip prio 1 u32 match ip sport $PORT 0xffff flowid 1:4
  then log "netem_ok $1"; else log "netem_FAILED $1"; netem_off; fi
}
trap 'netem_off; log cleanup; trap - TERM EXIT; kill 0' EXIT
trap 'exit 1' INT TERM
DUR=2700; i=0
for spec in "W1-6|6|delay 75ms 15ms distribution normal loss 0.5% limit 20000" "W1-10|10|delay 75ms 15ms distribution normal loss 0.5% limit 20000" \
            "W2-6|6|delay 150ms 40ms distribution normal loss 2% limit 20000" "W2-10|10|delay 150ms 40ms distribution normal loss 2% limit 20000"; do
  IFS='|' read P TAU NE <<< "$spec"; PT0=$((T0 + i * (DUR + 60))); i=$((i+1))
  w=$(( PT0 - 30 - $(date +%s) )); [ $w -gt 0 ] && sleep $w
  netem_on "$NE"; { echo "== $P"; tc -s qdisc show dev "$IF"; } >> $OUT/tc-$NAME.txt
  mkdir -p $OUT/$P; log "phase_start $P tau=$TAU"
  python3 nbench.py --name $NAME --nodes $NODES ${LISTEN:+--listen $LISTEN} --peers "$PEERS" --t0 $PT0 --duration $DUR \
     --cadence $TAU --tx-rate 4 --max-blocks --out $OUT/$P
  { echo "== fin $P"; tc -s qdisc show dev "$IF"; } >> $OUT/tc-$NAME.txt; log "phase_end $P"
done
log done
