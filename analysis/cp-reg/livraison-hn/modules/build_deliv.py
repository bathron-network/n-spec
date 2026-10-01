#!/usr/bin/env python3
"""Generates the MC_deliv_* shards for NonInterference_Deliv (Q3, 01/10). New file."""
from pathlib import Path
OWNER = '<<"H", "A", "H", "O", "A", "A">>'
CLASSES = {  # representative of each threshold class distinguishable on windows of length <= 6
 '00': (0,1), '16': (1,6), '20': (1,5), '25': (1,4), '33': (1,3), '40': (2,5),
 '43': (43,100), '60': (3,5), '67': (2,3), '80': (4,5), '83': (5,6), '100': (1,1), '117': (7,6)}
def write(name, rhos, mutation='NONE', invariants='TypeOK ConsEqual AdoptSafe StopRespected'):
    rs = ', '.join(f'<<{a},{b}>>' for a, b in rhos)
    Path(f'{name}.tla').write_text(f'''---- MODULE {name} ----
EXTENDS NonInterference_Deliv
MCRhoRef == <<7, 10>>
MCOwner == {OWNER}
MCRhos == {{{rs}}}
====
''')
    Path(f'{name}.cfg').write_text(f'''SPECIFICATION Spec
CONSTANTS
  MaxSlot = 6
  MaxReorg = 1
  EpochLen = 3
  Owner <- MCOwner
  Ids = {{"A", "H", "O"}}
  WShort = 2
  WLong = 4
  KDepth = 2
  ObjSlot = 1
  RhoRef <- MCRhoRef
  Rhos <- MCRhos
  HealthNum = 7
  HealthDen = 10
  Mutation = "{mutation}"
INVARIANTS {invariants}
CHECK_DEADLOCK FALSE
''')
for k, r in CLASSES.items():
    write(f'MC_deliv_ni_{k}', [r])
for w in ('NoWitnessDeliveryDiffers', 'NoWitnessDeliveredLowDensity', 'NoWitnessHalted',
          'NoWitnessSlowLane', 'NoWitnessReorgAdoption'):
    write(f'MC_deliv_witness_{w[9:]}', [(43,100)], invariants=w)
for m in ('SELECT_GATED', 'BRAKE_SHARED', 'STOP_BYPASS'):
    write(f'MC_deliv_mut_{m.lower()}', [(43,100)], mutation=m, invariants='ConsEqual')
