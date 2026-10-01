# CP_reg — simulateurs et calculs de l'auteur 1

Lire d'abord [CP-REG-codex.md](../CP-REG-codex.md). **Les résultats chiffrés ne qualifient pas le registre variable de N.** Aucune source de l'auteur 2 n'est lue ou importée.

## Reproduction

Python 3.9 ou ultérieur, NumPy (campagne : 2.0.2). Pillow est nécessaire seulement pour les images PNG. Aucun téléchargement, réseau, accès git ou paquet non livré n'est effectué par les scripts.

Depuis la racine du dépôt :

```sh
python3 etudes/n-spec/cp-reg/sim/check.py
python3 etudes/n-spec/cp-reg/sim/run.py --out <TMPDIR>
python3 etudes/n-spec/cp-reg/sim/closure_calibration.py --out <TMPDIR>
```

`run.py` refuse d'écraser une campagne terminée. Les graines et résultats numériques sont indépendants de l'ordre d'exécution des workers. Les temps et empreintes des sources reflètent naturellement l'environnement. `render.py` lit les résultats livrés sous `sim/results/` ; il régénère les SVG, PNG et deux tables Markdown.

Commande de la campagne finale livrée :

```sh
python3 etudes/n-spec/cp-reg/sim/run.py --out etudes/n-spec/cp-reg/sim/results --prior-cpu-reservation 600
```

La réserve de 600 s couvre la campagne exploratoire antérieure et les pilotes. Elle n'est pas du temps artificiellement ajouté aux temps mesurés. Une reproduction isolée n'a pas besoin de cette option. Le budget de réservation maximal, les consommations parent/enfants et les commandes sont dans les JSON de campagne.

## Fichiers

| Fichier | Objet |
|---|---|
| `model.py` | PGF analytique, queues binomiales de Chernoff, point fixe d'horizon, calcul des barrières, oracle de course, supports et trace de seuil A. |
| `run.py` | Grille 4×4×4, 4 096 essais par case, multiprocessing spawn, huit workers, un processus neuf par case, plafonds CPU. |
| `closure_calibration.py` | Un million d'essais par (β,u), abstention calibrée causalement après publication du calendrier de e−1 ; deux variantes et révélation stratégique ; géométrie temporelle de N conservée. |
| `check.py` | Oracle indépendant explicite sur petits arbres ; score et séquence de tie ; limites du compte inclusif ; comparaison aux probabilités binomiales exactes ; contrôle du risque recomposé. |
| `render.py` | Figures statiques SVG/PNG et tables complètes à partir des CSV. |
| `compare_existing.py` | Contrôle a posteriori du couple 7 200/2 880, après la dérivation ; refait la croissance avec b imposé et publie 192 comparaisons conditionnelles. |
| `results/derivation.csv` | 384 lignes : 64 triplets × trois risques × deux Q ; statut de N toujours UNKNOWN. |
| `results/mc-curves.csv` | Probabilités, nombres d'événements et IC, pour âge de divergence, enveloppe et blocs déconnectés. |
| `results/d-curves.csv` | **Moniteur de supports à géométrie d'époque réduite**, b=32/2 880 ; ne pas lire ses K comme les K_reg du manifeste. |
| `results/closure-calibration.csv` | Mesure conditionnelle de D_e divergent avec les vraies distances coupure/freeze/start de N ; b=2 880. |
| `results/*.npz` | Échantillons bruts : âge/profondeur maximaux, barrière, croissance et départs favorables. Aucun « zéro événement » n'efface les essais. |
| `results/closure-witness*.json` | Trace projetée du seuil A, score/tie vérifiés ; ni octets de blocs natifs signés ni campagne exhaustive de validateur. |
| `results/campaign.json`, `results/closure-campaign.json` | Métadonnées et temps CPU réellement consommés. |
| `validation.json` | Résultat de l'oracle et des contrôles numériques. |
| `development/`, `pilot/`, `pilot-worst/` | Provenance des calculs exploratoires, conservée pour le budget CPU ; pas des résultats de qualification. |

## Trois objets différents

1. **Attaque constructive.** Un calendrier entier est généré puis l'adversaire choisit son début et sa révélation. La stratégie retient tous ses blocs, prolonge une branche privée et la révèle une fois. Les débuts/fins possibles sont toutes les frontières des groupes de délai. L'oracle optimise exactement dans cette famille, pas sur tous les arbres et stratégies de N. Des producteurs honnêtes répétés peuvent prolonger leur propre bloc sans attendre sa diffusion.
2. **Enveloppe.** Les honest slots insuffisamment espacés sont transformés en adversaires ; les barrières communes sont calculées sur cette chaîne caractéristique. Cela couvre plus de fourches et de pouvoir de départage. Une absence de barrière n'est pas un succès d'attaque. Le calendrier et le registre y sont globaux et fixes.
3. **Fermeture calibrée.** L'histoire commune et une maturité Bitcoin tardive sont des conditions, pas des variables dont la probabilité serait connue. Le calibrage utilise seulement des créneaux adverses du calendrier déjà public. Une fois la graine de e connue, le suffixe A-H-A et les tie déterminent si les deux variantes permettent l'adoption du support différent.

Le moniteur réduit `d_events` de la campagne principale fixe une maturité à T/2 et une coupure m−K. Il vérifie la fonction support/héritage, mais n'impose pas l'écart de 14 400 créneaux entre freeze et début d'époque. C'est donc une sonde de la dépendance de D_e aux branches, **pas** un modèle complet du calendrier des graines. La mesure au calendrier N est celle de `closure_calibration.py` et de sa trace explicite.

## Paramètres et interprétation

- u est la disponibilité conditionnelle du poids honnête ; h=(1−β)u. β est rapporté à tout le poids éligible, inactifs inclus.
- Les quatre délais partagent les mêmes calendriers (common random numbers). Les 4 096 réplications sont indépendantes **dans chaque case**. Les courbes K, les délais et les deux K témoins ne sont pas des essais indépendants supplémentaires.
- Δ/τ=0 et 0,5 ont le même d=0 avec des phases fixes. Recalculer le chevauchement si la fenêtre de signature ou l'horloge change.
- Les IC Wilson sont ponctuels à 95 %. Pour zéro événement, une borne binomiale exacte unilatérale à 95 % est également publiée. Aucun IC Monte-Carlo n'est une borne sur le pire adversaire hors modèle.
- Un âge maximal atteignant l'horizon est censuré à droite : il peut continuer à augmenter au-delà. Le maximum observé n'est pas une limite de profondeur du protocole.
- Le Q=256 analytique représente au plus 256 calendriers complets candidats à registre fixé. Il n'est ni une borne démontrée sur le minage Bitcoin ni une réduction des registres concurrents.
- Les lignes sans certificat gardent leurs cellules numériques vides. `NO_HONEST_DRIFT` et `DELAY_REDUCTION_LOOSE` n'ont pas la même signification.
- Une K_reg=1 conditionnelle ne signifie pas une confirmation instantanée : elle utilise 6 000 créneaux de marge historique en plus du recul avant freeze. La colonne G=0 publie toute la fenêtre nécessaire.

## Budget et provenance

Le CPU total se mesure en somme des temps utilisateur+système du parent et de tous ses enfants, pas en temps mural multiplié approximativement par le nombre de workers. Les plafonds RLIMIT_CPU sont globaux à chaque processus neuf. Un timeout ou un signal CPU interrompt la campagne ; il ne compte jamais comme un essai sans attaque. La réserve totale admissible est contrôlée avant lancement.

Les premiers résultats `development/distinct-identities` supposaient des honnêtes différents dans chaque groupe. La campagne finale les remplace par 64 identités avec auto-prolongation. Les témoins de fermeture de développement et les anciennes tables ne font pas autorité ; utiliser uniquement les fichiers sous `results/`. La première sonde de fermeture, dont les métadonnées CPU seules sont conservées, a ensuite été remplacée par le calibrage causal au calendrier déjà publié.

Les empreintes de la campagne principale décrivent les fichiers présents lors de cette exécution. Les fichiers auxiliaires ajoutés ou documentés ensuite figurent dans le manifeste final de livraison. Les graines, les données brutes et les CSV de la campagne ne sont pas retouchés pour améliorer un résultat.
