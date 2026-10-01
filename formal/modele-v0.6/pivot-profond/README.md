# Pivot profond : campagne TLA+

Rapport : [PIVOT-PROFOND-TLA.md](../../../cp-reg/PIVOT-PROFOND-TLA.md).

Les modules sources résident au niveau parent (`*_PivotDeep.tla` / `.cfg`), parce que le lanceur livré (`run.sh`/`run.py`, non modifié) ne lit que ce répertoire. `modules/` en contient des copies. Aucun fichier livré n'a été modifié.

- `RegistryModel_PivotDeep.tla` : miroir focalisé, dérivé de `RegistryModelFast2`, avec une maturité de graine explicite par bloc (§5.2, §8.4) au lieu de la réduction « porteur = premier bloc ≥ start(e) ». Cette réduction exclut par construction la fermeture précoce.
- `Replay_PivotDeep.tla` : pilote de replay. `PathNotStuck` échoue en FAIL si un pas du chemin n'est pas activable.
- `logs/`, `traces/` : copies des sorties du lanceur, label `pivot_profond_final`.
- `RESULTATS.json` : statuts, compteurs, configurations et empreintes des modules.
- `preliminaire/`, `incomplets/` : runs obtenus avec des versions antérieures du modèle (erreur de configuration, deux bogues de moniteur corrigés, prédicat faible). Ils sont archivés et ne servent pas de résultats.

Reproduction, depuis ce répertoire parent :

```sh
TLC_RUN_LABEL=<nouveau_label> ./run.sh MC_replay_sync_PivotDeep MC_replay_aftersig_PivotDeep \
  MC_replay_stop_PivotDeep MC_replay_shallow_PivotDeep MC_explore_mixed_PivotDeep \
  MC_explore_sync_restricted_PivotDeep MC_explore_suffix_PivotDeep MC_explore_sync_PivotDeep
```

Statuts : un TÉMOIN signifie qu'un piège `NoWitness…` a été violé, donc que l'exécution est atteinte ; ce n'est jamais un PASS. INCOMPLET signifie que le run a été interrompu à 569 s. Un replay ne parcourt qu'un seul chemin.
