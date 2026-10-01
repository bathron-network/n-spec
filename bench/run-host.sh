#!/bin/bash
# Lance les trois phases du banc sur un hôte (v2).
# Usage : run-host.sh NAME T0 "PEERS" LISTEN CUT_PEER_IP|- NETEM(0/1) RUNID
# Phases : P0 natif 14400 s ; P1 netem +75ms±15 perte 0,5 % 5400 s ; P2 +150ms±40 perte 2 % 5400 s ; 60 s entre phases.
# netem n'agit qu'en SORTIE de cet hôte, sur le seul port du banc (sport ou dport) ; autres flux : fq_codel dans les bandes prio.
# Coupures (si CUT_PEER_IP) : chaîne iptables dédiée NBCUT, alternant lien seul (depuis CUT_PEER_IP) et isolement (tout le port).
set -u
NAME=$1 T0=$2 PEERS=$3 LISTEN=$4 CUTIP=$5 NETEM=$6 RUNID=$7
D=$(cd "$(dirname "$0")" && pwd); cd "$D"
PORT=29171; NODES=vps1,vps2,mac; OUT=out/$RUNID; mkdir -p $OUT/P0 $OUT/P1 $OUT/P2
LOG=$OUT/phases-$NAME.log
IF=$(ip route get 1.1.1.1 2>/dev/null | awk '{for(i=1;i<=NF;i++) if($i=="dev") print $(i+1)}')
log() { echo "$(date +%s%N) $*" >> $LOG; }
netem_off() { [ "$NETEM" = 1 ] && sudo -n tc qdisc del dev "$IF" root 2>/dev/null; true; }
netem_on() {
  [ "$NETEM" = 1 ] || return 0
  netem_off
  if sudo -n tc qdisc add dev "$IF" root handle 1: prio bands 4 priomap 1 2 2 2 1 2 0 0 1 1 1 1 1 1 1 1 &&
     for b in 1 2 3; do sudo -n tc qdisc add dev "$IF" parent 1:$b fq_codel || exit 1; done &&
     sudo -n tc qdisc add dev "$IF" parent 1:4 handle 40: netem $1 &&
     sudo -n tc filter add dev "$IF" parent 1: protocol ip prio 1 u32 match ip dport $PORT 0xffff flowid 1:4 &&
     sudo -n tc filter add dev "$IF" parent 1: protocol ip prio 1 u32 match ip sport $PORT 0xffff flowid 1:4; then
    log "netem_ok $IF $1"
  else
    log "netem_FAILED $1"; netem_off
  fi
}
netem_stats() { [ "$NETEM" = 1 ] && { echo "== $(date +%s)"; tc -s qdisc show dev "$IF"; } >> $OUT/tc-$NAME.txt; true; }
cut_setup() { sudo -n iptables -N NBCUT 2>/dev/null; sudo -n iptables -C INPUT -j NBCUT 2>/dev/null || sudo -n iptables -I INPUT 1 -j NBCUT; sudo -n iptables -F NBCUT; }
cut_clean() { sudo -n iptables -F NBCUT 2>/dev/null; sudo -n iptables -D INPUT -j NBCUT 2>/dev/null; sudo -n iptables -X NBCUT 2>/dev/null; true; }
cut_loop() {  # $1 = fin (epoch s)
  [ "$CUTIP" != - ] || return 0
  local k=0 plan=(link:10 iso:30 link:60 iso:10 link:30 iso:60)
  while :; do
    sleep 1200; [ "$(date +%s)" -lt $(( $1 - 180 )) ] || return 0
    local m=${plan[$((k % 6))]}; k=$((k+1)); local mode=${m%%:*} d=${m##*:}
    if [ $mode = link ]; then
      sudo -n iptables -A NBCUT -p tcp -s $CUTIP --dport $PORT -j DROP; sudo -n iptables -A NBCUT -p tcp -s $CUTIP --sport $PORT -j DROP
    else
      sudo -n iptables -A NBCUT -p tcp --dport $PORT -j DROP; sudo -n iptables -A NBCUT -p tcp --sport $PORT -j DROP
    fi
    log "cut_start $mode $d"; sleep "$d"; sudo -n iptables -F NBCUT; log "cut_end $mode $d"
  done
}
cleanup() { netem_off; cut_clean; log "cleanup"; }
trap 'cleanup; trap - TERM EXIT; kill 0' EXIT
trap 'exit 1' INT TERM
[ "$CUTIP" != - ] && cut_setup
phase() {  # nom t0 durée netem
  local P=$1 PT0=$2 DUR=$3 NE=$4
  local w=$(( PT0 - 30 - $(date +%s) )); [ $w -gt 0 ] && sleep $w
  if [ -n "$NE" ]; then netem_on "$NE"; else netem_off; log "native"; fi
  netem_stats
  ( while [ "$(date +%s)" -lt $((PT0+DUR)) ]; do echo "== $(date +%s)"; timedatectl timesync-status 2>/dev/null | grep -E 'Offset|Jitter|Delay|Server|Frequency'; sleep 300; done > $OUT/$P/timesync-$NAME.txt ) &
  local TP=$!
  cut_loop $((PT0+DUR)) & local CP=$!
  log "phase_start $P"
  python3 nbench.py --name $NAME --nodes $NODES ${LISTEN:+--listen $LISTEN} --peers "$PEERS" --t0 $PT0 --duration $DUR --out $OUT/$P
  log "phase_end $P"
  kill $CP $TP 2>/dev/null; sudo -n iptables -F NBCUT 2>/dev/null; netem_stats
}
phase P0 $T0 14400 ""
phase P1 $((T0+14460)) 5400 "delay 75ms 15ms distribution normal loss 0.5% limit 20000"
phase P2 $((T0+19920)) 5400 "delay 150ms 40ms distribution normal loss 2% limit 20000"
log "done"
