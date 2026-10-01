from pathlib import Path
P=Path(__file__).resolve().parent

def cfg(name,module,constants,invs,spec='Spec',props=''):
 (P/(name+'.tla')).write_text(f'---- MODULE {name} ----\nEXTENDS {module}\n====\n')
 (P/(name+'.cfg')).write_text(f'SPECIFICATION {spec}\nCONSTANTS\n'+''.join(f' {k} = {v}\n' for k,v in constants.items())+'INVARIANTS '+invs+'\n'+('PROPERTIES '+props+'\n' if props else '')+'CHECK_DEADLOCK FALSE\n')
for scenario in ['forward','inverse','mutual','foreign','false','losers','shallow','stale']:
 cfg('MC_h1_'+scenario,'H1Orders',dict(Scenario=f'"{scenario}"',Mutation='"none"',MaxReorg=1),'H1Order H1Subset H1NonVacuity H1Orientation NoContinuation')
for mutation in ['promote','adopted_only','maintain','anchor_deep']:
 cfg('MC_mut_h1_'+mutation,'H1Orders',dict(Scenario='"shallow"' if mutation=='anchor_deep' else '"forward"',Mutation=f'"{mutation}"',MaxReorg=1), 'H1Subset' if mutation=='promote' else 'H1Order H1NonVacuity H1Orientation NoContinuation')
for witness in ['CommonVeto','Maintain','Unknown']:
 cfg('MC_witness_h1_'+witness,'H1Orders',dict(Scenario='"forward"',Mutation='"none"',MaxReorg=1),'NoWitness'+witness)
for scenario,w in [('slow',1000),('068',1000),('rounding',10),('heavy',100),('inherited',1000)]:
 cfg('MC_brake_'+scenario,'Brake',dict(W=w,Scenario=f'"{scenario}"',Mutation='"none"',Horizon=20),'Mechanical RotationUnderBrake IntentionalRounding SlowProgress')
cfg('MC_mut_brake','Brake',dict(W=1000,Scenario='"slow"',Mutation='"zero_brake"',Horizon=20),'Mechanical')
for wit,sc in [('Slow','slow'),('Release','slow'),('068','068')]:
 cfg('MC_witness_brake_'+wit,'Brake',dict(W=1000,Scenario=f'"{sc}"',Mutation='"none"',Horizon=20),'NoWitness'+wit)
cfg('MC_brake_live','Brake',dict(W=1000,Scenario='"slow"',Mutation='"none"',Horizon=20),'Mechanical',spec='FairSpec',props='EventuallySlow')
for k in [1,2,4]:
 cfg(f'MC_registry_window_{k}','RegistryWindow',dict(Threshold=k,Mutation='"none"'),'ARule NoCircularity')
for mut in ['tip','no_threshold']:
 cfg('MC_mut_registry_'+mut,'RegistryWindow',dict(Threshold=2,Mutation=f'"{mut}"'),'ARule')
for wit in ['Threshold','Below','Above','Empty','Reject']:
 cfg('MC_witness_registry_'+wit,'RegistryWindow',dict(Threshold=2,Mutation='"none"'),'NoWitness'+wit)
for inv in ['C6','CPreg','RegistryImmutable']:
 cfg('MC_registry_commits_'+inv,'RegistryCommitments',dict(MaxReorg=2,Mutation='"none"'),inv)
cfg('MC_mut_registry_lock','RegistryCommitments',dict(MaxReorg=2,Mutation='"journal_veto"'),'NoJournalVeto')
for name,mut,invs in [('MC_persistence','none','S1 S2'),('MC_mut_generation','generation','S1'),('MC_witness_persistence','none','NoWitnessCrash')]:
 cfg(name,'Persistence',dict(Mutation=f'"{mut}"'),invs)
for name,mut,invs in [('MC_money','none','MON1 MON2 MON3 MON4 MON5'),('MC_mut_import','duplicate','MON1 MON2 MON3 MON4'),('MC_witness_money','none','NoWitnessMoney')]:
 cfg(name,'Money',dict(Mutation=f'"{mut}"'),invs)
for k in [1,2]:
 cfg(f'MC_anchor_{k}','AnchorBTC',dict(Mutation='"none"',MaxReorg=k,Dbtc=3),'AnchorExact G0 SafeBTC')
for mut,inv in [('free_anchor','AnchorExact'),('forget_seal','G0')]:
 cfg('MC_mut_'+mut,'AnchorBTC',dict(Mutation=f'"{mut}"',MaxReorg=1,Dbtc=3),inv)
cfg('MC_witness_btc','AnchorBTC',dict(Mutation='"none"',MaxReorg=1,Dbtc=3),'NoWitnessBTCStop')
for name,mut,inv in [('MC_admissions','none','AddNoReset ReactReference'),('MC_mut_add','add_reset','AddNoReset'),('MC_witness_react','none','NoWitnessReact')]:
 cfg(name,'Admissions',dict(Mutation=f'"{mut}"'),inv)

cfg("MC_anchor_agreement","AnchorBTC",dict(Mutation='"none"',MaxReorg=1,Dbtc=3),"A4")
for sc in ['foreign','matching','stale']:
 cfg('MC_scan_'+sc,'H1Scan',dict(Scenario=f'"{sc}"'),'TrueComplete ForeignIrrelevant ResolvedDecidable')
cfg('MC_scan_stale_counterexample','H1Scan',dict(Scenario='"stale"'),'NoStaleVeto')
for wit in ['Unknown','Decidable']:
 cfg('MC_witness_scan_'+wit,'H1Scan',dict(Scenario='"matching"'),'NoWitness'+wit)
cfg('MC_authorities','Authorities',{},'AuthoritiesSafe')
cfg('MC_witness_recovery','Authorities',{},'NoWitnessRecovery')
cfg('MC_tie_parent','TieDelivery',{},'ParentDeterministic')
cfg('MC_tie_reservations','TieDelivery',{},'ReservationsConverge')
cfg('MC_brake_068_arithmetic','BrakeArithmetic',{},'Density068 MaskFixed DenominatorZero')
cfg('MC_witness_068_arithmetic','BrakeArithmetic',{},'NoWitnessHealth')
for tag,op in [('advance','~(\\E b\\in Branches,e\\in Es: Support(chains[b],e)#<<>>)'),('empty','NoTwoEmptyEpochsWitness')]:
 name='MC_witness_mirror_'+tag
 cfg(name,'RegistryModel',dict(Epochs=3,SlotsPerEpoch=2,EndSlot=4,KReg=1,MaxReorg=4 if tag=='advance' else 1,ForkSlot=0,BrokenTipSnapshot='FALSE',BrokenH1Promote='FALSE',RuleA='TRUE'),'NoWitnessMirror')
 (P/(name+'.tla')).write_text(f'---- MODULE {name} ----\nEXTENDS RegistryModel\nNoWitnessMirror == {op}\n====\n')
