# Campagne TLA+ N v0.6

Commencer par [RAPPORT-TLA-N-v0.6.md](RAPPORT-TLA-N-v0.6.md), puis [RESULTATS-DETAILLES.md](RESULTATS-DETAILLES.md). Le rapport fait autorité pour la portée des résultats ; un fichier de modèle isolé n'est pas une qualification du protocole.

- `RegistryModelFast2.tla` : modèle final du miroir, dérivé du générateur historique ; `RegistryAudit.tla` : journal persistant séparé.
- `*Checked.tla` : sous-machines finales corrigées ; les premiers modules sans suffixe restent des artefacts de développement.
- `MC_*.tla` et `.cfg` : bornes, restrictions et moniteurs de chaque campagne.
- `logs/`, `traces/`, `RESULTATS.json` : preuves et résultats ; les interruptions restent INCOMPLET.
- `PORTEE-ET-MAPPING.md`, `COUVERTURE-SONDES.md` : hypothèses, réductions, mapping normatif et inventaire NT.
- `historical/` : copies v0.5 et correctif D ; ne pas confondre le suffixe historique `_v06` avec cette campagne.
- `SHA256.json`, `INTEGRITE-ORIGINAUX.json` : empreintes de livraison et comparaison des copies avec leurs originaux.

## Reproduire

Depuis ce dossier, avec Python 3 et Java 21 au chemin indiqué par le mandat :

```sh
TLC_RUN_LABEL=reproduction ./run.sh MC_fast_off_00 MC_fast_on_00
TLC_RUN_LABEL=h1 ./run.sh MC_h1_forward_checked
TLC_RUN_LABEL=frein ./run.sh MC_brake_slow_checked MC_witness_brake_Release_checked
TLC_WORKERS=1 TLC_RUN_LABEL=trace ./run.sh MC_replay_general_k1 MC_replay_general_k2
```

Le JAR et `tools/LocalTLC.java` proviennent de v0.5. Le lanceur compile l'adaptateur local dans un répertoire temporaire, limite le tas à 3 Go, les workers à 4, fixe `-fp 0` et la durée à 569 secondes avec marge sous le plafond 570. Un verrou exclusif commun sérialise les explorations, même si plusieurs commandes sont soumises. Les logs existants ne sont jamais remplacés : choisir un nouveau label. Les traces de reproduction vont aussi dans un sous-dossier séparé.

Les scripts `build_fast*.py` sont des outils de préparation historiques, pas une étape de reproduction des sources finales livrées. Pour reconstruire les tableaux après de nouveaux runs sans label, utiliser `python3 tools/report_results.py`, puis `python3 tools/compose_report.py`. `tools/finalize_manifest.py` ne doit être exécuté qu'une fois les processus terminés.

Aucune continuation par checkpoint n’est utilisée pour prolonger les explorations interrompues. Les résultats INCOMPLET restent tels quels.
