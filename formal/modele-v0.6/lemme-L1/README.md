# Campagne première divergence

Rapport : [LEMME-L1-codex.md](../../../cp-reg/LEMME-L1-codex.md).

Les modules et configurations ajoutés résident au niveau parent, suffixe `_L1`, afin d'utiliser le lanceur livré sans modification. `campaign.json` énumère les sondes choisies : représentants des trois familles demandées et replays. Ce n'est pas une reprise exhaustive de toutes les combinaisons Bitcoin existantes.

Depuis la racine du dépôt :

```sh
python3 etudes/n-spec/tla/modele-v0.6/lemme-L1/run-campaign.py
python3 etudes/n-spec/tla/modele-v0.6/lemme-L1/finalize.py
```

Le script ignore les résultats JSON déjà existants ; le lanceur refuse d'écraser un log. Pour une nouvelle reproduction indépendante, appeler `run.sh MODULE_L1` avec un nouveau `TLC_RUN_LABEL`. Un log orphelin sans JSON n'est pas un PASS. La première tentative interrompue est archivée sous `MC_fast_off_00_L1.interrupted.*`.

Le lanceur existant conserve lui-même logs, configurations, compteurs, empreintes et traces. Des copies sont réunies ici. Chaque run est limité par ce lanceur à environ 569 secondes ; aucune durée de campagne ne modifie cette borne par run.

`FirstBlockCommon` : dérivation de deux candidates au premier créneau divergent. `CommonInterval` : fonctions de tirage avant la première époque de supports différents, fenêtres fermées. `NoOtherStructural` : classification brute `i_raw`/`ii_pivot`/`other`, **sans prétendre que i_raw est une violation de CP-fixe**. Le journal supplémentaire conserve tous les engagements observés, y compris les signatures. `NoWitnessMissingBridge` cherche deux signatures divergentes après une frontière où la branche privée était plus courte, avec tous les engagements antérieurs sur l'autre branche.

Les témoins attendus violent un invariant `NoWitness…`. Un résultat TÉMOIN est une atteignabilité, pas un PASS. Les modèles ne comportent ni loi probabiliste de tirage réelle, ni borne de livraison Δ, ni calcul Bitcoin complet ; la fermeture Fast2 est simplifiée au début d'époque. Le rapport expose ces limites.
