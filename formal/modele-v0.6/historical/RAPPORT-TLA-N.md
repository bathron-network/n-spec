# Rapport TLA+ — N-SPEC v0.5

Date : 30 septembre 2026. Sources : `N-SPEC-v0.5.md` et `MANDAT-TLA-N.md` du présent dossier. Modèle : `NModel.tla`. Ce rapport concerne une abstraction finie des interactions de consensus ; il ne qualifie pas N pour un déploiement.

## Lecture des résultats

**Un PASS borné n'est pas une preuve de préfixe commun de N.** `MC_safe` part d'un bloc commun au créneau 0 et laisse diverger les suffixes à partir du créneau 1. Dans ses trois époques, le dernier cliché admissible reste ce bloc commun. `MC_spec_registryreorg` supprime cette restriction de scénario : les fourches peuvent commencer au créneau 0, sans activer aucune mutation du protocole.

L'invariant d'immutabilité utilise comme contexte l'origine locale et les faits Bitcoin, à époque identique. **Il n'inclut pas le support N dans sa prémisse** : cela rendrait invisible précisément le risque recherché. Une signature honnête engage aussi le registre. Une acceptation explicite de RECOVERY ouvre un nouveau contexte. La graine complète du §5.4 contient la racine du registre : exiger l'égalité de cette graine tout en recherchant deux racines différentes serait une propriété différente, en grande partie tautologique avec des hashes injectifs.

## Exécution reproductible

```sh
./run.sh MC_safe
TLC_WORKERS=1 ./run.sh MC_broken_tipsnapshot
TLC_WORKERS=1 ./run.sh MC_broken_h1promote
TLC_WORKERS=1 ./run.sh MC_spec_registryreorg
./run.sh MC_live
./run.sh MC_witness_empty
./run.sh MC_witness_equivocation
./run.sh MC_witness_twoempty
./run.sh MC_live_recovery
```

`run.sh` compile le petit lanceur Java puis invoque le TLC fourni, en recherche exhaustive BFS, quatre workers, paramètre `-seed 1`, tas de 3 Gio. Les trois recherches de défauts sont aussi exécutées avec `TLC_WORKERS=1` pour obtenir des traces BFS minimales sans entrelacement de workers. La compilation et les extractions de modules standard disposent chacune d’un répertoire temporaire propre au run. Le code de sortie de TLC est conservé : 0 signifie succès, 12 violation d'invariant. Les traces complètes sont dans `logs/NOM.log` ; `logs/RESULTATS.json` contient les compteurs et les SHA-256 des sources, configurations, lanceur et JAR. Les modules de campagne étendent `NModel` ; les modules `MC_replay_*` ajoutent un compteur de pas pour rejouer un seul contre-exemple.

Le TLC 2.19 fourni exporte son stockage local de fingerprints par RMI, même en mode non distribué. Le premier essai a échoué avec `Listen failed ... Operation not permitted`. `tools/LocalTLC.java` fournit un endpoint RMI **sans bind, sans connexion, sans communication réseau** ; son `accept()` attend simplement la fermeture. Il appelle ensuite `tlc2.TLC.main`. Le JAR, l'algorithme d'exploration, l'évaluation des invariants et les fingerprints ne sont pas modifiés. Ce lanceur est réservé au TLC local.

Aucun `CONSTRAINT`, `ACTION_CONSTRAINT`, quotient de symétrie, simulation aléatoire ni coupe de profondeur BFS n'est utilisé. Les limites sont des paramètres et des restrictions explicites du générateur d'histoires. Le dernier créneau autorise encore production, livraison et récupération ; `Tick` seul y est désactivé. `CHECK_DEADLOCK FALSE` évite de confondre un horizon fini avec une panne du protocole ; ce réglage ne prouve aucune vivacité. BOOTSTRAP et la spécification autorisent par ailleurs le stuttering.

## Bornes et abstractions

| Élément | Représentation et portée |
|---|---|
| Honnêtes | Deux nœuds/producteurs, identifiants 1 et 2 |
| Producteur adverse | Identifiant 3, capable de produire les deux variantes de son créneau |
| Tickets | Poids initiaux `(2,1,1)`, donc quatre tickets ; ADD préparés aux créneaux 0 et `ForkSlot`, au plus deux tickets supplémentaires |
| Histoires N | Deux suites de blocs, préfixe commun initial éventuel ; parents implicites dans les suites, score = longueur |
| Époques | Trois époques de deux créneaux, horizon sûr tronqué au premier créneau de la troisième ; deux pour le contrôle temporel complémentaire |
| Cliché | `cut(e)=(e-1)*2-1` ; sélection strictement `slot < cut`, genesis si la borne est non positive |
| `maxreorg` | Un bloc dans le scénario sûr ; quatre dans la sonde de cliché ancien |
| Bitcoin | Fait initial fixé par genesis ; deux valeurs possibles par époque suivante, toutes les combinaisons explorées ; disponibilité/maturité séparée |
| Réseau | Partition initiale, puis réunion irréversible ; le nœud 2 est initialement absent, puis revient ; ces événements peuvent survenir à tous les créneaux |
| Données | Préfixes connus indépendants par nœud et branche ; `Fetch` livre les préfixes accessibles et effectue leur rejeu atomique |
| H1 | Résultat abstrait validé `NONE`, `UNKNOWN`, `LAG` ; pertinence des paires calculée depuis maxima, chaîne adoptée, LCA, ancre et profondeur |
| BOOTSTRAP | Réception possible dans tout état avec origine locale, y compris absence et STOP ; aucun effet sur l'état de sûreté |
| RECOVERY | Acte externe `ExplicitAccept(n,b)` pour le dossier exact calculé depuis l'état courant, à usage unique par nœud ; autorisé à l'horizon, après STOP profond |

`MC_safe` fixe `EndSlot=4` : cinq créneaux 0–4, dont le créneau 0 initialisé, avec deux époques complètes et le premier créneau de la troisième. Les campagnes de défauts vont jusqu’à 5. La tentative générale à six créneaux a été interrompue avant dix minutes, sans violation observée mais sans exploration achevée : elle n’est pas un PASS. Le coût du classement a été réduit en stockant son composant immuable `blockTie` lors de la création de chaque bloc ; `BlockMetadataCorrect` compare ce cache au calcul historique indépendant pour chaque bloc. Les essais de développement interrompus ne comptent pas comme des succès.

Les quatre vecteurs Bitcoin possibles du scénario à trois époques sont des entrées exhaustives, pas quatre simulations. Le calendrier est une loterie déterministe simplifiée sur les **tickets individuels**, indexée par époque, fait Bitcoin, racine du registre et créneau. La graine engage bien la racine du registre. `Reveal` abstrait la disponibilité du service de graines ; seules celles de l’époque courante sont consommables par la production. Les délais MTP, garde et confirmations ne sont pas des sous-machines de ce modèle. Le model-checker connaît les valeurs nondéterministes futures : aucune preuve d’imprévisibilité ou d’anti-grinding n’est revendiquée. Cette fonction arithmétique n'est ni SHAKE256 ni une hypothèse de pseudo-aléa uniforme. Le départage conserve score puis séquence de valeurs dérivées de `(graine, créneau, producteur)`, sans hash de bloc, contenu ou ordre de réception supplémentaire. Deux variantes d'une même réservation peuvent donc rester exactement ex æquo.

Les ADD représentent des opérations déjà préparées et historiquement valides. Leur effet n'entre dans le registre qu'une fois couvert par un support autorisé. `ReplayOps` rejoue les époques et déduplique les opérations ; `ReferenceRegistry` calcule indépendamment le résultat directement depuis le support. Un support inchangé ne consomme aucune opération supplémentaire et ne retire aucun poids. Les exclusions, rotations, REACT et bans ne sont pas développés dans cette abstraction de contrôle. L'équivoque est produite, mais son ban ultérieur n'est pas simulé.

Les réservations honnêtes interdisent deux signatures au même créneau. Les réservations et le moniteur d'engagement devenus inutiles sont oubliés après avancement irréversible du créneau/de l'époque : aucun retour de l'horloge ni restauration de sauvegarde n'est disponible. Cet oubli est une réduction d'état pour ce modèle, **pas une règle de persistance proposée pour N**.

## Correspondance avec la SPEC

| Variables/opérateurs | Champs ou règles normatifs |
|---|---|
| `slot`, `Epoch` | Créneau et époque mécaniques, §5.1 |
| `chains`, `Block`, `Slot`, `Lane`, `blockTie` | Arbre N réduit à deux branches, ascendance, contenu ADD abstrait, score et départage, §§8–9 |
| `bitcoin`, `ready`, `Seed`, `Owner` | Faits de graine, disponibilité et attribution pondérée, §§5.4–5.5 et 7.1 |
| `Support`, `ReplayOps`, `Registry` | `registry_support_by_epoch`, registre et consommation idempotente, §§5.2–5.9 |
| `local[n].seen`, `partition`, `absent` | Préfixes connus, files de messages abstraites, séparation et rattrapage, §9.7 |
| `local[n].tip/anchor/origin` | Chaîne adoptée, ancre persistante, origine de confiance, §§9.5–9.6 et 12.14 |
| `local[n].registry/epoch/signed` | Registre courant et réservation de signature, §§5 et 7.4 |
| `evidence`, `local[n].mode` | Décision H1 et motifs d’attente/arrêt, §§12.6–12.7 |
| `recoveryUsed`, `ExplicitAccept` | Consommation de l’acceptation explicite du dossier courant, §12.14 |
| `audit`, `local[n].history` | Instrumentation de vérification uniquement ; ne bloque jamais une adoption et n’est pas un verrou de protocole |

Les identifiants de tickets et les clés sont fixes ou reconstructibles à partir des opérations représentées : dans ces bornes, deux ensembles d’ADD distincts donnent des vecteurs de poids distincts. Il n’y a pas de test de rotation de clé à poids constant.

## Propriétés vérifiées

| Obligation | Opérateur | Sens exact |
|---|---|---|
| 1. Accord | `Agreement` | Même époque, mêmes supports nécessaires et mêmes faits Bitcoin globaux impliquent même registre local ; lemme conditionnel A1 |
| 2. Déterminisme | `Determinism` | Rejeu incrémental = calcul direct ; registre adopté correct ; supports identiques donnent mêmes graines et producteurs |
| 3. Recovery | `Recovery` | Après réunion, retour, maturité, fin de l'alerte H1 et traitement complet des mêmes données, deux histoires distinctes ne sont pas toutes deux considérées continuables |
| 4. Pas d'arrêt accidentel | `NoAccidentalHalt` | Dans un créneau honnête, avec données, protections et H1 compatibles, une vraie transition `Produce` est activable ; aucune exigence de nouveaux blocs ou de densité |
| 5. H1 détecteur | `H1Detector` | Chaque adoption réelle appartient à `BaseAdoptable` calculé sur **le même état antérieur et les mêmes candidats**, avant H1 |
| 6. Immutabilité | `RegistryImmutable` | Moniteur des engagements par adoption ou signature : aucun deuxième registre dans la même époque/contexte ; le moniteur ne filtre jamais `Next` |
| BOOTSTRAP | `BootstrapNoEffect` | Comparaison avant/après de l'état local complet, des candidats et de leurs maxima |
| Complément | `AnchorProtected` | Chaque adoption automatique conserve l'ancre antérieure ; RECOVERY est séparé |
| Complément | `RecoveryExplicit` | Acceptations non rejouées ; l'origine ne change que par l'action externe explicite |
| Typage | `TypeOK` | Domaines finis et cohérence des tailles de préfixes connus |

`STOP_TIE` signifie arrêt de la canonicité et des nouvelles stabilités, **pas interdiction de produire**. La production sur une pointe maximale reste possible (§7.3). Ni l'écoulement du temps ni BOOTSTRAP ne départagent l'égalité. Un STOP profond est réévalué par `Fetch` ; ce n'est pas un verrou permanent. L'ancre avance après validation/adoption, jamais pour justifier cette même adoption.

`NoAccidentalHalt` est une obligation locale d'activabilité, pas une preuve que l'environnement produira. Deux propriétés temporelles complètent cette distinction dans `MC_live` :

- `RecoveryProgress` : finalement, durablement, mêmes pointes ou au moins un arrêt explicite de canonicité.
- `ResumptionProgress` : après stabilisation finale des données et du réseau, les attentes de graine/H1 disparaissent ; restent RUN, égalité productive ou conflit profond explicite.

Dans le suffixe temporel vérifié, l'équité faible porte sur le retour du nœud, la réunion, la disponibilité des graines, la fin de l'alerte et le traitement par chaque honnête. Le créneau est déjà final ; `FairSpec`, qui ajoute l'équité d'avancement au générateur complet, reste disponible mais sa campagne complète n'a pas été terminée. L’équité ne porte **jamais sur l’acceptation de RECOVERY**. Il n'y a pas d'équité de production ni de garantie de croissance infinie au-delà de l'horizon. Le témoin `MC_witness_empty` exige séparément une production honnête effective en époque 2 après une époque 1 sans aucun bloc sur aucune branche. `MC_witness_twoempty` part de genesis, saute les deux premières époques sans aucun bloc et produit honnêtement en époque 2.

`MC_live` (également disponible sous le nom `MC_live_recovery`) est un contrôle temporel complémentaire sur 48 états initiaux de reconnexion : histoires déjà construites aux créneaux 0, 1, 2, 3, avec ou sans équivoque au créneau 3, ancres ordinaires, données et alertes variables. Il explore uniquement le suffixe de réunion/rejeu, sans production nouvelle. Ces états couvrent à la fois une réorganisation permise et un conflit entre ancres ; ils ne sont pas présentés comme les états initiaux de `MC_safe`.

## Limites de généralisation

1. Le scénario sûr ne démontre ni A3 (préfixe commun probabiliste), ni A4 (compatibilité universelle des ancres). Sa divergence tardive est une restriction explicite des histoires explorées. Le test élargi est indispensable pour ne pas prendre ce lemme conditionnel pour un résultat général.
2. `KReg=1` et `maxreorg=1/4` sont des échelles abstraites. Rien ici ne justifie `K_reg=7200`, `maxreorg=2880`, un délai d'absence sûr ou une probabilité d'échec. Le poids adverse initial vaut 1/4, pas la valeur de travail 1/5 ; aucune revendication probabiliste n'en est tirée.
3. Les deux branches ne représentent ni un arbre sans borne ni des forks imbriqués. Une seule partition et une seule absence sont explorées, sans délai réseau quantifié pendant la partition.
4. Bitcoin est une source de faits finis avec maturité abstraite. Arbre Bitcoin, chainwork, MTP, réorganisations de graines consommées et STOP_BTC ne sont pas implémentés ; la réorg BTC est optionnelle dans le mandat et reste hors campagne.
5. H1 abstrait les résultats de preuves recevables ; formats de transactions, scans Bitcoin, fenêtres exactes RawLag et disponibilité détaillée restent à vérifier séparément.
6. Le rejeu est atomique. Crash entre préparation/témoin/commit, journal anti-rollback, restauration, clonage, compromission/rotation des clés et LOST_CONTEXT ne sont pas vérifiés. La fraîcheur de RECOVERY est abstraite comme un acte externe unique atomique, pas prouvée pour un protocole d'interface utilisateur.
7. Pas de modèle monétaire G1–G10, d'import Bitcoin, de token applicatif, de quotas d'exclusion ni d'undo applicatif. Les autres invariants du §23.9 ne sont pas annoncés comme couverts.
8. Le contrôle temporel porte sur les suffixes de reconnexion de deux époques, à partir de 48 états initiaux explicites ; l'horizon fini ne prouve pas une reprise productive universelle après une absence de durée arbitraire. Les témoins de couverture sont des existences, pas des garanties pour toute exécution.
9. L'exploration TLC utilise des fingerprints, avec la probabilité résiduelle de collision estimée dans le log. Les mutations valident la capacité des moniteurs à détecter ces défauts précis ; elles ne prouvent pas que toute implémentation incorrecte sera détectée.

## Résultats définitifs et contre-exemples

| Configuration | Résultat | Générés | Distincts | File restante | Profondeur | Durée |
|---|---|---:|---:|---:|---:|---|
| `MC_broken_h1promote` | FAIL | 236 955 | 47 687 | 20 524 | 11 | 02min 28s |
| `MC_broken_tipsnapshot` | FAIL | 11 774 | 2 880 | 1 581 | 7 | 05s |
| `MC_live` | PASS | 1 296 | 386 | 0 | 7 | 08s |
| `MC_live_recovery` | PASS | 1 296 | 386 | 0 | 7 | 14s |
| `MC_replay_h1` | FAIL | 13 | 11 | 0 | 11 | 01s |
| `MC_replay_spec` | FAIL | 9 | 9 | 0 | 9 | 01s |
| `MC_replay_spec_adopt` | FAIL | 13 | 13 | 0 | 13 | 00s |
| `MC_replay_tip` | FAIL | 7 | 7 | 0 | 7 | 01s |
| `MC_safe` | PASS | 639 168 | 93 112 | 0 | 21 | 02min 57s |
| `MC_spec_registryreorg` | FAIL sans mutation | 71 382 | 16 048 | 8 054 | 9 | 19s |
| `MC_witness_empty` | TÉMOIN ATTEINT (FAIL attendu) | 40 953 | 9 133 | 4 565 | 9 | 06s |
| `MC_witness_equivocation` | TÉMOIN ATTEINT (FAIL attendu) | 6 060 | 1 523 | 852 | 6 | 03s |
| `MC_witness_twoempty` | TÉMOIN ATTEINT (FAIL attendu) | 64 400 | 14 533 | 7 216 | 9 | 05s |

Les PASS ci-dessus terminent avec une file vide et le code 0. Chaque FAIL termine avec le code 12 et une violation d’invariant explicite, jamais une erreur de parsing ou une exception. Les FAIL de sondes de couverture signifient que leur anti-propriété a été réfutée : la situation recherchée est atteignable. Un FAIL général s’arrête à la première violation ; ses autres invariants ne sont donc pas réputés vérifiés exhaustivement.

| Invariant du mandat | `MC_safe` | `MC_broken_tipsnapshot` | `MC_broken_h1promote` | `MC_spec_registryreorg` |
|---|---|---|---|---|
| Accord | PASS | NT | NT | NT |
| Déterminisme | PASS | NT | NT | NT |
| Recovery | PASS | NT | NT | NT |
| Pas d’arrêt accidentel | PASS | NT | NT | NT |
| H1 détecteur | PASS | NT | FAIL | NT |
| Immutabilité | PASS | FAIL | NT | FAIL |
| BOOTSTRAP sans effet | PASS | NT | NT | NT |

`NT` : non testé par cette configuration, et non « PASS ». Les quatre contrôles auxiliaires de `MC_safe` (`TypeOK`, `BlockMetadataCorrect`, `AnchorProtected`, `RecoveryExplicit`) passent également. Les deux propriétés temporelles de `MC_live` et `MC_live_recovery` passent sur leurs 386 états.

Le PASS principal couvre **93 112 états distincts**, 639 168 générations et une profondeur BFS de 21, en **2 min 57 s**. Tous les runs terminés durent moins de dix minutes. L’estimation TLC de collision de fingerprints pour ce run est 2,8×10⁻⁹ (calcul optimiste), 1,3×10⁻⁹ selon les fingerprints observés. Les résultats sont ceux de TLC avec cette limite habituelle, pas une preuve déductive non bornée.


## Contre-exemples et diagnostic de SPEC

Notation : `G` est genesis ; `P0` le bloc commun du créneau 0 quand `ForkSlot=1` ; `A_s`/`B_s` les blocs des deux branches au créneau `s`. Un registre est donné par ses poids `(p1,p2,p3)`. Les vrais identifiants numériques de blocs et tous les états locaux figurent dans les logs.

### Mutation : cliché pris sur la pointe

Défaut unique : pour `e>0`, `Registry` utilise `Ops(c)` à la place des seules opérations couvertes par les supports anciens. Le contexte Bitcoin vaut `(0,0,0)`.

Trace minimale : **7 états, 6 transitions**.

1. Depuis `P0`, le producteur 1 crée `B_1`, qui porte l’ADD du producteur 2.
2. Passage au créneau 2, retour du producteur 2, disponibilité des graines.
3. Le producteur 2 signe `A_2` sur `P0`, avec le registre fautif `(3,1,1)`.
4. Il reçoit `P0 → B_1`, mieux classé dans ce tirage de départage, et l’adopte.
5. Toujours en époque 1, il dérive `(3,2,1)` : **`RegistryImmutable` devient FALSE**.

Les supports normatifs de l’époque 1 sont pourtant genesis sur les deux branches. Le poids de l’ADD récent n’aurait dû apparaître dans aucun des deux registres. Reproduction rapide : `./run.sh MC_replay_tip`.

### Mutation : H1 promoteur

Défaut unique : une alerte pertinente `LAG` fait retourner une adoption positive de la branche B avant de respecter le résultat de base N. Le rang lui-même n’est pas modifié.

Trace minimale : **11 états, 10 transitions**. Le nœud 1 adopte d’abord `P0 → B_1`. Une alerte est présente, puis une autre histoire `P0 → A_2 → A_3` est produite. Les scores valent respectivement 2 et 3. La réorganisation déconnecterait un bloc, ce qui est permis avec `maxreorg=1`, et préserverait l’ancre `P0`. La paire est pertinente pour H1 car le suffixe de A dépasse un bloc.

La base N permet uniquement A. La version conforme peut adopter A ou s’arrêter sous H1. La mutation **réadopte B en RUN**, donc rend continuable la branche perdante : `{B}` n’est pas inclus dans `{A}`. **`H1Detector` devient FALSE**. Il ne s’agit pas de reprocher à un STOP de conserver sa pointe locale : la violation est bien le résultat positif RUN/adoption. Reproduction : `./run.sh MC_replay_h1`.

### Modèle conforme : cliché ancien remplacé dans la même époque

`MC_spec_registryreorg` conserve **les deux drapeaux de mutation à FALSE**. Il autorise une divergence dès le créneau 0 et `maxreorg=4`. Le registre utilise toujours exactement la borne temporelle de la SPEC.

Trace minimale : **9 états, 8 transitions**, Bitcoin `(0,0,1)`.

1. Le producteur byzantin produit `A_0`, contenant un ADD pour le producteur 1, puis le retient vis-à-vis du nœud 1.
2. Les créneaux 1, 2 et 3 restent vides ; l’horloge atteint 4, en époque 2.
3. Le nœud 1 signe `B_4` sur genesis avec `(2,1,1)`. L’époque 2 est engagée.
4. Il découvre `A_0`. Les deux candidates ont un bloc ; le départage de ce tirage préfère A.
5. Le nœud adopte A. Pour l’époque 2, `cut(2)=1`, donc `A_0` appartient au support et le nouveau registre est `(3,1,1)`.

Origine, époque et fait Bitcoin sont inchangés ; aucune RECOVERY n’est acceptée ; H1 est absent ; l’ancre est genesis. Le changement de registre est **autorisé par les actions conformes**, mais viole l’immutabilité inconditionnelle du mandat. Reproduction minimale : `./run.sh MC_replay_spec`.

Un second replay utilise même `maxreorg=1` et `EndSlot=4`, comme la campagne sûre, et élimine deux ambiguïtés possibles : `./run.sh MC_replay_spec_adopt`, **13 états**. Avec Bitcoin `(0,1,1)`, le byzantin construit `A_0 → A_3` ; le nœud 1 produit `B_4`. Le nœud 2 revient pendant la partition et **adopte B**, engageant `(2,1,1)`. Après réunion, il découvre A, de score **2 contre 1**, donc strictement supérieure sans dépendre du départage. Il déconnecte un seul bloc, préserve genesis, adopte A et passe à `(3,1,1)` dans la même époque. Il s’agit cette fois d’une véritable réorganisation d’une pointe déjà adoptée.

**Interprétation normative.** Le §5.2 mesure l’ancienneté du cliché en créneaux ; le §9.6 protège selon une distance en blocs et une ancre persistante. Une longue période creuse ne transforme pas une petite profondeur en blocs en préfixe irréversible. Le §5.7.3 autorise explicitement une candidate à avoir un autre registre du fait d’un autre préfixe, et interdit de faire d’un registre mémorisé une seconde ancre. Le §5.7.2 demande une qualification de préfixe commun qui n’est pas démontrée ici.

Ce résultat n’établit donc pas une contradiction interne de la SPEC : il montre que **la propriété 6 du mandat, comprise sans hypothèse de préfixe commun, ne découle pas des règles v0.5**. La trace est hors de l’hypothèse de préfixe commun ; la partition peut néanmoins être temporaire et entièrement résolue, comme dans le replay avec adoption. Le PASS de `MC_safe` ne doit pas masquer ce FAIL du modèle conforme élargi. Une garantie globale exigerait une hypothèse qualifiée supplémentaire ou une modification normative ; aucun verrou de registre n’a été ajouté au modèle pour obtenir artificiellement cette garantie.

Les replays sont des tests de régression de traces, pas des explorations générales supplémentaires. Les variantes générales conservent leur propre exploration BFS exhaustive jusqu’à la première violation.
