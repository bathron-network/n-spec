# Profil de livraison H_N : seuil de densité et non-interférence (Q3)

1er octobre 2026. Ce document applique la décision Q3 du propriétaire (`DIRECTION.md`, « Gel v0.7 — Q1/Q3 (01/10) »). Il s'appuie sur `CRITERES-GEL-v0.7.md` (critère 9) et sur `COHERENCE-v0.7.md`, Q3. Il n'ajoute aucune mécanique et ne modifie ni le frein, ni la fork-choice, ni la règle A, ni STOP.

## Verdict

- **Seuil proposé.** Un seul seuil, `rho_deliv = 43/100`, appliqué aux trois fenêtres du §14.2. Le format de profil v6 ne porte qu'un `rho_min` ; des seuils distincts par fenêtre demanderaient un nouveau format.
- **Coût du seuil.** La valeur candidate de 0,45 suspend trop souvent la fenêtre de 1 000 créneaux au coin du domaine. Le seuil de 0,43 coûte en revanche une protection plus faible contre la fausse livraison sur une vue éclipsée, tant que la profondeur reste 77.
- **Dépendances.** La densité de livraison n'est lue que par le §14.2, les statuts du §14.5 et l'API (§16.2). Elle n'entre dans aucune fonction de consensus.
- **`rho_min` partagé.** Le paramètre est partagé textuellement avec la condition de dimensionnement du §14.3, mais pas avec le frein : le 7/10 du §6.6 est une constante de consensus écrite en dur. La séparation demandée tient donc en deux renommages, détaillés plus bas.
- **Non-interférence (TLA+).** Deux copies d'un même nœud reçoivent la même suite d'événements, mais chacune avec son propre seuil de livraison. Résultat : traces de consensus identiques pour les 13 classes de seuils, statut **PASS borné**. Cinq pièges de non-vacuité donnent TÉMOIN. Trois mutations, où le seuil fuit vers la sélection, le frein ou STOP, donnent FAIL.

## 1. Où la densité et `rho_min` sont-ils utilisés ?

Relevé exhaustif de `N-SPEC-v0.7.md`, obtenu en cherchant `rho`, `densit`, `7/10`, `0,70`, `livraison` et `§14`.

| Lieu | Usage | Nature | Lit `rho_min` ? |
|---|---|---|---|
| §3.3, IDs 4–7 | Fenêtres 100 et 1 000, `rho_min = 7/10` | Profil client (`policy_id`) | Définition |
| §14.1 | Définition de la densité | Mesure | Non |
| §14.2 | `10 × filled ≥ 7 × window_length` sur les fenêtres 100, 1 000 et depuis l'inclusion | Livraison applicative | **Oui** |
| §14.3 | `1 − alpha − beta > rho_min` ; « retour à 7/10 » | Condition de dimensionnement (vivacité de la livraison) | **Oui** |
| §14.4 | `P[Bin(100;0,75) < 70]` | Exemple de laboratoire | Valeur 0,70 |
| §14.5, §16.2 | `SUSPENDU`, `STABLE_SELON_POLITIQUE` ; « fenêtres exactes de densité » | Statuts et API | Indirect, en sortie |
| §6.6 | `health_ok : 10×filled_eligible ≥ 7×eligible_slots` ; « Le ratio n'est ni la densité de livraison du §14 » | **Consensus** (frein et voie lente) | **Non** : constante écrite en dur |
| §5.9, invariant 28 | La production n'exige ni densité ni profondeur | Production | Non |
| §9.5 | `Select(…, politique, …)` ; `BaseNDecision` ne lit que `maxreorg` | Fork-choice, STOP | Non |
| §9.6 | `Nbound` (`maxreorg`), `Bbound` (`D_btc`) | Ancre | Non |
| §5.2–5.3 | Règle A : compte de `maxreorg` blocs | Registre | Non |
| §12 | Prédicats H1 : profondeurs, `G_anchor` | Veto | Non |
| §12.14, étape 8 | « revalider les conditions de production et de livraison » | Sortie de RECOVERY | Lecture seule |
| §13.5 | « Ne pas payer avant … politique client » | Discipline du payeur (hors N) | Indirect, comportement externe |
| §17.3, §17.6 | La table K(ε) n'est pas une borne de livraison sans §14 et §15.8 ; « suspension de livraison par densité (§14.2) » | Domaine | Non |
| §20.3–20.4 | Vecteurs « santé sous 0,7 », « densité < 0,2 » | Frein et production | Non |
| §23.2–23.7 | Livraison au sens réseau (messages) ; densités < 0,2 obligatoires | Modèles | Non |

Le seul canal par lequel la politique client atteint la fork-choice est `maxreorg`. Le §3.3 l'impose égal à `registry_min_blocks` : le profil H_N le garde à 1 630, et seul son `policy_id` change. Le §13.5 crée un effet indirect : un payeur qui suit un seuil plus bas paie plus tôt. Ce paiement Bitcoin devient une **entrée** ordinaire de N, que les fonctions de consensus traitent de façon déterministe (invariant 20). Ce n'est pas une interférence du paramètre sur la règle.

**Séparation (renommages, aucune mécanique).**

1. Le 7/10 du §6.6 est nommé `health_min`. C'est une constante de consensus, inchangée.
2. Au §14.3, `rho_min` désigne le seuil du profil actif : `rho_deliv = 43/100` pour le profil H_N, 7/10 pour le laboratoire. La condition au coin devient `0,49 > 0,43`.

Ces deux lectures figurent dans le texte inséré au §14.2. Le §6.6 et le §14.3 ne sont pas réécrits.

## 2. Dérivation du seuil

Au coin du profil B, avec `p_late = 10⁻²` : `h' = 0,4851` pour la chaîne publique quand l'adversaire s'abstient, et `a = β + h·p_late = 0,3049`. Cette valeur borne la densité d'une branche purement adverse : une branche porte au plus un bloc par créneau, l'adversaire n'a que ses propres attributions, et les retards sont comptés comme adverses par convention conservatrice. Tous les calculs sont binomiaux exacts : sommes de termes en log-gamma, et programmation dynamique exacte pour la fenêtre depuis l'inclusion. Ils sont reproductibles avec `cp-reg/livraison-hn/seuils.py` ; les valeurs sont dans `seuils.json`.

- **Fausse suspension (FS)** : `P[Bin(W, h') < ρW]`, par instant d'évaluation. Les fenêtres glissantes sont corrélées (§14.4).
- **Fausse livraison (FL)** : `P[Bin(W, a) ≥ ρW]`.

| ρ | W = 100 : FS | W = 100 : FL | W = 1 000 : FS | W = 1 000 : FL |
|---:|---:|---:|---:|---:|
| 0,38 | 1,3 × 10⁻² | 6,6 × 10⁻² | 9,1 × 10⁻¹² | 2,5 × 10⁻⁷ |
| 0,40 | 3,5 × 10⁻² | 2,7 × 10⁻² | 2,7 × 10⁻⁸ | 1,1 × 10⁻¹⁰ |
| 0,42 | 8,0 × 10⁻² | 9,7 × 10⁻³ | 1,6 × 10⁻⁵ | 9,7 × 10⁻¹⁵ |
| **0,43** | **0,114** | **5,5 × 10⁻³** | **2,1 × 10⁻⁴** | **4,9 × 10⁻¹⁷** |
| 0,45 | 0,211 | 1,6 × 10⁻³ | 1,2 × 10⁻² | 3,9 × 10⁻²² |
| 0,70 | 1 | 5,1 × 10⁻¹⁶ | 1 | 2,2 × 10⁻¹⁴⁵ |

**Depuis l'inclusion.** Le créneau d'inclusion est rempli. La FL vaut `P[∃n : S_n ≥ N et S_n ≥ ρn]` pour une marche de Bernoulli(a). C'est une borne supérieure, puisque les fenêtres de 100 et 1 000 créneaux ne sont pas imposées dans ce calcul. La convergence a été vérifiée en doublant l'horizon. La FS est évaluée à l'instant où la profondeur N est atteinte. Elle est **transitoire** : comme `h' > ρ`, la densité remonte ensuite.

| ρ | N = 77 : FS | N = 77 : FL | N = 739 (K(10⁻⁶)) : FS | N = 739 : FL | N = 1 123 (K(10⁻⁹)) : FL |
|---:|---:|---:|---:|---:|---:|
| 0,40 | 6,3 × 10⁻³ | 6,5 × 10⁻³ | 7,4 × 10⁻¹⁴ | 5,7 × 10⁻¹⁸ | 1,6 × 10⁻²⁶ |
| 0,42 | 2,9 × 10⁻² | 1,3 × 10⁻³ | 1,7 × 10⁻⁸ | 2,7 × 10⁻²⁴ | 4,2 × 10⁻³⁶ |
| **0,43** | **5,2 × 10⁻²** | **5,6 × 10⁻⁴** | **1,9 × 10⁻⁶** | **1,1 × 10⁻²⁷** | **3,0 × 10⁻⁴¹** |
| 0,45 | 0,143 | 9,4 × 10⁻⁵ | 1,9 × 10⁻³ | 7,1 × 10⁻³⁵ | 3,7 × 10⁻⁵² |
| 0,70 | 1 | 4,4 × 10⁻¹⁷ | 1 | 4,4 × 10⁻¹⁵³ | 1,1 × 10⁻²³¹ |

Pour ρ = 0,43, la probabilité d'être encore suspendu après n créneaux depuis l'inclusion vaut 7,3 % à n = 159 (le temps moyen pour atteindre 77 blocs), 2,1 % à n = 300 et 1,9 × 10⁻⁴ à n = 1 000.

**Choix.**

- **1 000 créneaux.** C'est la fenêtre qui exprime la marge sur `h_min`. À 0,45, la FS vaut 1,2 % par instant : un nœud honnête au coin serait suspendu environ 1 % du temps sans attaque. À 0,43, elle vaut 2,1 × 10⁻⁴ (marge de 3,5 σ sous h'), et la FL reste négligeable.
- **100 créneaux.** Cette fenêtre détecte un arrêt récent ; elle ne protège pas contre la fausse livraison. À 0,43, la FS vaut 11,4 %, du même ordre que les 10,4 % du profil de laboratoire à son point nominal (§14.4). Un seuil de 0,40 (FS 3,5 %) serait préférable, mais il demande un format de profil à deux seuils.
- **Depuis l'inclusion.** C'est la vraie défense contre une branche adverse montrée à un nœud éclipsé. En effet, si la fourche est récente, la fenêtre de 1 000 créneaux contient des blocs honnêtes antérieurs : à la profondeur 77, sa densité attendue est d'environ 0,75 × 0,485 + 0,25 × 0,305 ≈ 0,44, et elle peut donc passer le seuil. Avec la profondeur 77, la FL passe de 4,4 × 10⁻¹⁷ (seuil 0,70) à **5,6 × 10⁻⁴ au plus** (seuil 0,43). Cette dégradation est réelle. Elle porte sur un nœud hors domaine (§12.15), et la densité n'a jamais constitué un ε (§15.7).

**Proposition.** `rho_deliv = 43/100` sur les trois fenêtres. Variante si le format évolue : (0,40 ; 0,43 ; 0,43).

## 3. Profondeur N

La livraison exige aussi une profondeur d'au moins `k_default = 77`. C'est une valeur de laboratoire, explicitement **sans borne de risque N** (§3.3). La table K(ε) du §17.3 donne 739, 1 123 et 1 508 blocs au coin pour ε = 10⁻⁶, 10⁻⁹ et 10⁻¹². Un profil H_N qui revendiquerait un ε devrait utiliser K(ε), et cette valeur rendrait aussi la FL par densité négligeable (ligne N = 739 ci-dessus). **Rien n'est changé sans décision.** Le texte inséré laisse 77 et renvoie au §17.3 ; c'est la question séparée Q3-bis.

## 4. Vérification formelle

Aucun modèle de `tla/modele-v0.6/` ne contient de seuil de densité de livraison. `RegistryModelV6` affirme seulement que la densité ne crée pas de garde de production. J'ai donc écrit un modèle dédié, `NonInterference_Deliv.tla` (nouveau ; aucun fichier livré modifié), avec ses configurations `MC_deliv_*` générées par `build_deliv.py`.

**Construction : auto-composition.** Deux copies `c1` et `c2` du même nœud observateur avancent pas à pas, pilotées par **un seul** environnement :

- production honnête ou abstention ;
- adversaire sur n'importe quel parent, avec équivoque à deux étiquettes ;
- éclipse (branche privée montrée au seul observateur) ;
- production propre de l'observateur ;
- horloge et fins d'époque.

Chaque copie reçoit la politique complète `[maxreorg, rho]`, si bien qu'une dépendance au seuil reste exprimable. La copie 1 utilise 7/10. La copie 2 utilise un seuil représentant chacune des **13 classes** de seuils distinguables sur des fenêtres de longueur au plus 6 : toutes les valeurs k/w, 0 et une valeur supérieure à 1. 43/100 représente la classe ]2/5 ; 1/2]. Comme chaque pas du produit est un pas des deux copies, l'invariant d'état `ConsEqual` équivaut à l'égalité des traces de consensus. Le modèle couvre :

- la pointe et les adoptions (`BaseNDecision`) ;
- l'ancre (`Nbound`, maximum avec l'ancienne) ;
- les modes `HALTED_DEEP_REORG` et `EQUIVOCATION_TIE`, recalculés sans bit irréversible ;
- la santé à 7/10 sur les identités hors QUEUED ;
- les exclusions ordinaires et lentes, avec quota lent et sans retrait du dernier poids ;
- les décisions de production.

Par transitivité, l'égalité avec 7/10 vaut pour tout couple de seuils.

Autres invariants : `AdoptSafe` (la pointe étend l'ancre et aucune adoption ne déconnecte plus que `maxreorg`) et `StopRespected` (une copie arrêtée ne livre rien, ce qui découle de la définition).

Bornes : 6 créneaux, 2 époques de 3 créneaux, `maxreorg = 1`, fenêtres de 2 et 4 créneaux (pour 100 et 1 000), profondeur 2 (pour 77), calendrier H, A, H, O, A, A. Lanceur `run.sh` livré, plafond de 569 s, label `deliv_hn_ni`.

| Run | Statut | Détail |
|---|---|---|
| `MC_deliv_ni_{00,16,20,25,33,40,43,60,67,80,83,100,117}` | 13 × PASS borné (7 564 308 états distincts chacun, file vide, profondeur 22, ≈ 146 s) | `ConsEqual`, `AdoptSafe`, `StopRespected`, `TypeOK` |
| Témoins `DeliveryDiffers`, `DeliveredLowDensity`, `Halted`, `SlowLane`, `ReorgAdoption` | 5 × TÉMOIN | Les livraisons diffèrent réellement ; STOP, voie lente et réorganisation sont atteints |
| Mutation `SELECT_GATED` (la sélection filtre selon la livraison) | FAIL `ConsEqual` | Le moniteur détecte une fuite vers la fork-choice |
| Mutation `BRAKE_SHARED` (le frein utilise `rho`) | FAIL `ConsEqual` | Fuite vers le frein et la voie lente |
| Mutation `STOP_BYPASS` (un objet livré lève STOP) | FAIL `ConsEqual` | Contournement de STOP détecté |

**Portée.** Le résultat est un PASS **borné** et **structurel** : le modèle encode les dépendances telles que la spécification les écrit, et vérifie qu'aucun chemin du seuil vers le consensus n'existe dans cet encodage. Plusieurs éléments restent hors du modèle :

- H1 et Bitcoin ;
- la règle A (le registre y est réduit à l'ensemble des exclusions sur un calendrier fixe) ;
- les paiements du §13.5 ;
- la publication adverse vers les honnêtes.

Ce n'est pas une qualification de N. Les probabilités viennent du §2, pas de TLC.

## 5. Modifications textuelles

1. `N-SPEC-v0.7.md` §14.2 : nouvelle sous-section « Profil de livraison H_N ». Elle contient le seuil 43/100 ; β = 3/10 dans les IDs 17–20 du profil, par cohérence avec l'exigence d'une « hypothèse de poids adverse publiée » ; la table des risques ; la profondeur ; la non-interférence ; la séparation `health_min`/`rho_deliv` ; la lecture du §14.3 ; la bande hors domaine [0,43 ; 0,49[.
2. `N-SPEC-v0.7.md` §12.15 : décision Q1. La `RECOVERY` explicite du §12.14 est le chemin de réintégration (KNOWN_CONTEXT ou LOST_CONTEXT, réservations de signature conservées selon le §7.6) ; la réinstallation reste possible ; l'option (ii) n'est pas retenue.
3. `CHANGELOG-v0.7.md` : entrées 43 et 44, total porté à 44.

## 6. Questions séparées (aucune n'est tranchée ici)

- **Q3-bis.** Faut-il aligner la profondeur du profil H_N sur K(ε) (§17.3) ? Cela supprimerait la dégradation de FL à la profondeur 77.
- **Q3-ter.** Faut-il un format de profil à seuils par fenêtre (0,40 sur 100 créneaux) ? Ce serait un changement de format.
- **Q1-bis.** En KNOWN_CONTEXT, un dossier RECOVERY engage le contexte exact du nœud (`previous_anchor_id`, `previous_safety_state_root`). Il faut donc un dossier signé 3/4 par nœud, ou un LOST_CONTEXT. La procédure opérationnelle n'est pas spécifiée.
- **β et α du profil.** β = 3/10 est inscrit dans le profil H_N et doit être confirmé. `alpha_budget` (1/20) reste inchangé, alors que le coin implique α ≈ 0,21. C'est de la documentation, à rapprocher de Q4.

## Reproduction

Résultats et empreintes : `cp-reg/livraison-hn/RESULTATS.json`. Logs : `tla/modele-v0.6/logs/reproductions/deliv_hn_ni/` et `deliv_hn_w/`. Copies des modules : `cp-reg/livraison-hn/modules/`. Un run de mise au point, PASS avant le passage à 13 shards, est archivé dans `preliminaire/` ; ce n'est pas un résultat.

```sh
cd etudes/n-spec/cp-reg/livraison-hn && python3 seuils.py seuils.json
cd ../../tla/modele-v0.6 && python3 build_deliv.py
TLC_RUN_LABEL=<nouveau> ./run.sh MC_deliv_ni_43 MC_deliv_witness_Halted MC_deliv_mut_select_gated
```

## Corrections après revue Codex T2 (01/10)

Revue : `orchestration/reviews/q3-livraison-codex.md`.

Corrigé dans N-SPEC v0.7 :
- Une densité observée entre 0,43 et 0,49 **n'est pas** une sortie du domaine. `h_min` borne la disponibilité, pas chaque réalisation.
- Au coin, `1 − alpha − beta = 0,4851` (et non 0,49), ce qui reste supérieur à 0,43.
- Q1 : `LOST_CONTEXT` seulement dans les conditions du §12.14, sans repli automatique.

Réserves maintenues :
- Les probabilités valent pour une fenêtre et un départ fixés, pas contre une attaque qui choisit sa fenêtre.
- Le modèle de non-interférence simplifie le frein (une époque, quota lent réduit) : il établit une non-interférence **structurelle**, pas la fidélité complète au §6.6.
- `alpha_budget = 1/20` n'est pas aligné sur le coin H_N (documentation).
