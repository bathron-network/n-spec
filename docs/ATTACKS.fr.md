# Attaques et contre-exemples : l'histoire de falsification de N

**Architecture frozen candidate. Not mainnet-qualified. Not production-ready.**
(Candidat d'architecture gelé. Non qualifié pour le mainnet. Pas prêt pour la production.)

Ce document recense les attaques, les contre-exemples et les affirmations réfutées qui ont façonné N, depuis les candidats moteurs antérieurs jusqu'à N-SPEC v0.7. Chaque ligne provient d'une étude datée, d'une campagne de model checking, d'une dérivation numérique, d'un banc réseau ou d'une relecture aveugle. Pour les raisons d'ensemble, voir **WHY-N.fr.md**. Version anglaise : `ATTACKS.md`.

## Légende

**Méthode**
- **TLA+** : model checking borné avec TLC. Tout résultat est borné ; ce n'est pas une preuve déductive.
- **Monte-Carlo** : simulation stratégique.
- **Analyse** : argument analytique ou programmation dynamique exacte (DP), le plus souvent produits par deux analyses indépendantes puis confrontés.
- **Banc** : mesure réseau sur des liens réels, ou émulation (netem) sur des liens réels.
- **Relecture aveugle** : relecteurs disposant du seul texte de la spécification, sans contexte du projet.

**Statut**
- **FAIL réel** : contre-exemple atteignable avec les règles telles qu'écrites, sans mutation. La mention « (analytique) » indique qu'il a été établi par un argument plutôt que par le model checker.
- **FAIL de mutation** : une variante volontairement cassée est détectée par le moniteur. C'est le résultat attendu ; il prouve la sensibilité du contrôle.
- **TÉMOIN** : une situation ciblée est atteignable.
- **PASS borné** : aucune violation dans les bornes annoncées.
- **INCOMPLET** : exploration interrompue. Un INCOMPLET ne compte jamais comme un PASS.

Les lignes à partir de N v0.5 se vérifient dans ce dépôt (`spec/`, `formal/`, `analysis/`, `bench/`, `qualification/`). Les lignes sur les candidats moteurs antérieurs (§1) et les premières versions de N résument des études et des relectures aveugles qui ne sont pas publiées ici.

---

## 1. Candidats moteurs antérieurs à N

| Candidat | Attaque / contre-exemple | Méthode | Statut | Correction ou décision | Test de non-régression |
|---|---|---|---|---|---|
| C (séquenceur + quorum de tickets) | Sûreté face à l'équivoque, à la rétention, à des seuils ou verrous cassés | TLA+ (adapté d'un modèle Tendermint publié) : N=4/F=1/q=3 exhaustif, 28,7 M états ; N=7 et N=6 partiels | PASS borné en sûreté ; toutes les variantes cassées détectées. Vivacité : latence quand q = N−F−U exactement | C n'est pas écarté pour une raison de sûreté | Variantes cassées : seuil trop bas, sans verrou, verrous effacés |
| C | « Le burn garantit β » | Analyse (deux kill-tests indépendants) | FAIL réel (analytique) : le burn ne borne ni la concentration, ni la location de clés, ni la corruption, ni la coercition, ni l'attrition ; deux départs honnêtes suffisent à franchir le seuil de forge si F suit N | β devient une hypothèse publiée, jamais une promesse. Ensuite : C archivé, N pur choisi | — |
| Finalité sans quorum (producteur + Core déterministe + arrêt sur ambiguïté) | Le silence n'est pas une ambiguïté détectable ; Bitcoin ne contient pas les racines | Analyse (deux kill-tests) | FAIL réel (analytique) | La finalité ferme exige un quorum, une écriture dans Bitcoin ou une synchronie | — |
| D (finalité par convergence) | Un propriétaire qui équivoque plus une partition donnent deux « finalités » incompatibles | Analyse (deux kill-tests) | FAIL réel (analytique) : « D sans quorum tué » | D abandonné. Retenu sans coût : typage des transactions possédées / partagées | — |
| D3 (lignée unique, Bitcoin en lecture seule) | Pour toute règle locale, P[double lignée] ≥ 2·(vivacité d'un paiement honnête) − 1 | Analyse | FAIL réel (analytique) pour les paiements libres | Seuls survivent l'objet de swap à un saut et les automates d'horloge | — |
| E / F (certificats échantillonnés) | Tailles de comité : ≈ 200 à β = 0,1 ; 1 300 à 2 600 à β = 0,2 ; impossible à β = 0,3 ; un comité public tombe sur ≈ 50 corruptions ciblées | Analyse | FAIL réel (analytique) pour F ; E reporté | Reporté | — |
| E2 (SBRB/DPRB fidèles) | 27 à 252 Mbit/s par nœud à 32 tx/s contre ≈ 5 pour C ; sûreté probabiliste sous adversaire statique ; aucune preuve exportable | Analyse des papiers primaires (deux analyses) | FAIL réel (analytique) au regard de la règle du propriétaire (« si E2 reste plus cher ou moins sûr, on ferme E ») | **E fermé.** Récupéré : exécution parallèle par compte, validité par (source, seq), gel de l'équivoqueur | — |
| Barrière Bitcoin (BFT synchrone cadencé par Bitcoin) | Deux tickets et une partition plus longue que 2Δ donnent deux FINAL silencieux, quel que soit N (borne DLS 1988) | Analyse | FAIL réel (analytique) | Tuée comme moteur de finalité | — |
| Deux étages (chaîne mécanique + checkpoints C) | Aucun gain sur β ; le calendrier public permet des réorgs à la demande ; une réorg Bitcoin au-delà de k_seed arrête aussi | Analyse | Reporté | Non adopté | — |
| NC (finalité C par objet) | La finalité par objet se propage en profondeur, en amont (cône causal) et vers les nœuds neufs | Analyse | FAIL réel (analytique) | N pur au genesis | — |
| N lui-même (premier candidat) | Tentatives de réorg gratuites, répétables et non fautives ; réorgs ciblées grâce au calendrier public (β = 0,2, τ = 6 s : profondeur 6 environ tous les 5,4 jours) ; côté minoritaire effacé en partition ; aucune preuve exportable | Analyse | Réel (analytique), accepté comme limite déclarée | Le propriétaire renonce à la finalité ferme. Vocabulaire : inclusion → profondeur → stabilité. Politique de profondeur et plafonds d'exposition chez les SP/LP | Table K(ε) (§17.3) |

## 2. Longue portée et H1

| Version | Attaque / contre-exemple | Méthode | Statut | Correction ou décision | Test de non-régression |
|---|---|---|---|---|---|
| Étude longue portée (époque v0.1) | Le graphe d'objets seul prouve la provenance, pas la date ; avec des clés volées, une fausse chaîne atteint 100 % de densité | Analyse | FAIL réel (analytique) | Écarté comme défense longue portée | — |
| Idem | « Premier ancré gagne » : un attaquant vivant ancre plus vite qu'un réseau passif et sépare les nœuds neufs du réseau pour 0,01 BTC | Analyse | FAIL réel (analytique) | Écarté | — |
| Idem | La « densité après la divergence » élit le jumeau ou l'attaquant | Analyse | FAIL réel (analytique) | Écartée. Remplacée par la disqualification par progrès prouvé (preuve temporelle négative, jamais fork-choice) | — |
| v0.2.1 | Filtre temporel retourné contre un nœud neuf : une branche adverse empreintée à bas coût est adoptée pendant une sécheresse honnête | Relecture aveugle | FAIL réel (analytique) | v0.3 : le témoin doit aussi mener au score ; jamais d'adoption par le seul filtre | — |
| v0.4 | Un filtre qui exige un meilleur score ne peut éliminer qu'une branche déjà battue : c'est un détecteur, pas une règle de sélection | Relecture aveugle (deux relecteurs sur trois) | Constat | Décision du propriétaire : **H1 = détecteur**. Une preuve d'antériorité Bitcoin peut réduire l'ensemble sûr ou déclencher un STOP, jamais promouvoir | Moniteurs `H1Detector`, `H1Subset` |
| v0.5 | Veto H1 quasi inerte pour un nœud neuf, avec une issue qui dépend de l'**ordre d'arrivée** (C d'abord ⇒ adoptée sans H1 ; W d'abord ⇒ arrêt profond) | Relecture aveugle | FAIL réel (analytique) | v0.6 : paires de veto orientées (C ∈ maxima, W ∈ branches validées profondes) avec témoin complet, réévaluées même après adoption | TLA+ `H1OrdersChecked` : toutes les permutations de six événements, **9/9 PASS borné** |
| v0.5 | Mutation « H1 promoteur » : une alerte réadopte la branche perdante | TLA+ | FAIL de mutation (11 états) | — | `MC_replay_h1` ; mutations v0.6 « H1 promoteur », « H1 limité à l'adoptée », « MAINTAIN saute H1 », « Deep dépend de l'ancre locale » : toutes détectées |
| v0.6 | La fréquence des empreintes ne borne pas, à elle seule, la fraîcheur du progrès prouvé (références anciennes) | TLA+ | FAIL réel (contre-exemple borné) | Publié. N-SPEC §18 : H1 n'est pas une protection longue portée complète | `MC_scan_stale_counterexample` |

## 3. Registre et préfixe commun

| Version | Attaque / contre-exemple | Méthode | Statut | Correction ou décision | Test de non-régression |
|---|---|---|---|---|---|
| v0.3 | **Verrous locaux du registre** (persistés à la coupure, jamais remplacés) : deux honnêtes verrouillent des registres différents après une divergence d'un bloc près de la coupure (exploitable par un producteur adverse) ; une absence qui traverse une coupure ⇒ HALTED ; un BOOTSTRAP de plus d'environ une époque devient inutilisable ; blocage définitif après une époque de faible densité | Relecture aveugle de la v0.4 (trois relecteurs, cause racine commune) | FAIL réel (analytique) | v0.5 : verrous supprimés ; le registre est une fonction déterministe d'un cliché ancien de la chaîne candidate (préfixe stable, façon Ouroboros) | Mutation v0.6 « registre engagé utilisé comme veto » détectée (`NoJournalVeto`) |
| v0.5 | **Réorganisation du registre** : le cliché est daté en créneaux, la protection contre les réorgs en blocs. Un bloc A₀ retenu avec un ADD, des créneaux vides, puis une adoption ⇒ deux registres dans la même époque et le même contexte, sans mutation | TLA+ (`MC_spec_registryreorg`, trace de 9 états) ; confirmé par trois relecteurs aveugles qui ignoraient le modèle | **FAIL réel** (sans mutation) ; le PASS borné `MC_safe` (93 112 états) ne couvrait pas ce cas | Décision du propriétaire **D + A** : stabilité conditionnelle C6 énoncée exactement ; CP_reg comme obligation séparée ; règle A : `A_e` n'avance que si la branche contient au moins maxreorg blocs dans la fenêtre du cliché, sinon il est hérité. Aucun verrou | `MC_v6_replay_spec_{off,on}`, `..._adopt_{off,on}` (9 et 13 états) |
| v0.6 | **A off ⇒ RegistryImmutable FAIL** | TLA+, quatre vecteurs Bitcoin | A off : **FAIL 4/4** + 2 replays. A on : **PASS borné 4/4** (exhaustif dans les bornes du modèle, constantes abstraites), 1 331 054 états distincts (un vecteur terminé lors d'une relance sans plafond) | Règle A retenue | `MC_fast_off_*` / `MC_fast_on_*` ; C6 8/8 PASS borné ; 13/13 mutations détectées |
| v0.5 | Mutation « cliché pris sur la pointe » | TLA+ | FAIL de mutation (7 états) | — | `MC_replay_tip` ; mutations v0.6 « cliché sur pointe » et « suppression du seuil A » détectées |
| v0.6, A on | **B₀ retenu** : B₀ porte un ADD et il est retenu ; au créneau 4, deux honnêtes signent sous (2,1,1) et (2,2,1). Deux registres dans la même époque et le même contexte avec **zéro déconnexion**, donc aucun arrêt profond attendu | TLA+ (`MC_replay_general_k1/k2`, journal d'audit `MC_audit_cp_k1/k2` en 11 et 12 états) | **FAIL réel** de l'immutabilité forte et de CP_reg sans domaine réseau ; C6 PASS sur la même trace | CP_reg devient une obligation séparée, à analyser sous un domaine publié (aucune mécanique nouvelle) | Mêmes replays ; `MC_replay_audit_c6` PASS |
| v0.6 | Ancres incompatibles après des livraisons séparées (A4) | TLA+ (`MC_anchor_agreement_checked`) | FAIL réel (borné, sans domaine réseau) | Ouvert : l'hypothèse manquante est une borne réseau sur la construction et la livraison | **QR-9** |
| v0.6 | La convergence des données n'efface pas des réservations de signature antérieures différentes | TLA+ (`MC_tie_reservations`) | FAIL réel (borné) | Publié ; aucune mécanique modifiée | Même configuration |
| v0.6 | La règle A est pilotable vers d ≈ 0,2 (g·W < b ≤ (g+β)·W) | Analyse (DP) + trace exécutable (2 déconnexions) + Monte-Carlo (0,32 % à β = 0,20, d = 0,20, K = 512 ; 16 M répétitions) | FAIL réel dans cette zone | Zone exclue par le domaine publié (d ≥ 0,70) | Table K(ε), table `d-min` |
| v0.6 | L'ancienne profondeur k = 77 du §15 (modèle sans avance) sous-estime le risque de 8 à 10 ordres de grandeur avec calendrier public, rétention et équivoque | Analyse (deux méthodes indépendantes) + relecture aveugle de la v0.5 | FAIL réel (analytique) de l'ancienne affirmation | k = 77 conservé comme valeur de laboratoire, sans borne de risque ; table DP K(ε) publiée ; équivoque comptée comme une unité de progrès par branche | Règle d'équivoque vérifiée dans trois codes |
| v0.6 | **CP_reg et le calendrier variable** (lemme de première divergence L1). L1 et L2 tiennent, mais « toute la course se joue sous calendrier commun » est faux : une branche privée bifurque avant la coupure, est en retard au début de l'époque, change ensuite de registre et de calendrier, puis rattrape | Analyse E1 (contenu pré-cliché composé après avoir vu la graine, rotation des clés ⇒ nombreux calendriers sélectionnables) + témoin TLA+ `MC_private_return_L1` (15 états ; deux signatures au créneau 4 sous des registres différents) | TÉMOIN / FAIL réel (analytique) de la borne ; ε_U INCONNU | Nœuds synchronisés couverts par maxreorg (arrêt). Nœuds nouveaux ou de retour déclarés **hors domaine CP_reg** (D1, subjectivité faible, retour par une origine A′/RELEASE récente) | `MC_private_return_L1` ; 12 sondes TLA+, `NoOtherStructural` jamais violé |
| v0.6 → v0.7 | **Pivot profond** : une branche privée ferme tôt sa fenêtre sous le seuil en **antidatant un porteur de maturité dans la marge MTP** [MatMin, BtcMat), hérite du registre, puis prend l'avantage. Un nœud synchronisé l'adopte après 2 ou 3 déconnexions, sous maxreorg | TLA+ (miroir dédié) : 2 replays dirigés, 1 exploration semi-dirigée, 1 exploration restreinte ; le run de contraste donne STOP | **TÉMOIN ×4** ; exploration stricte complète **INCOMPLET** (5,2 M états) | Aucune mécanique nouvelle. Couvert en probabilité par le terme `T_profond` quand (K_reg, b) sont dérivés ensemble. Une estimation antérieure trop optimiste de la profondeur du pivot a été corrigée (queue de fluctuation, avance, union sur les positions de fourche) | `MC_replay_{sync,aftersig,stop,shallow}_PivotDeep` ; **QR-4** |
| v0.7 | Bande résiduelle d'environ 370 créneaux (≈ 1 h) au plancher MTP, où l'arithmétique ne force pas le STOP pour une *installation* antidatée | Analyse (contrôle de cohérence) | Expliqué ; borné en probabilité par `T_profond` ≈ 1,95·10⁻¹³ par époque | Couverture probabiliste acceptée comme dimensionnement dérivé | **QR-6** (preuve de composition) |

## 4. Vivacité, réseau et paramètres

| Version | Attaque / contre-exemple | Méthode | Statut | Correction ou décision | Test de non-régression |
|---|---|---|---|---|---|
| v0 | Un repère Bitcoin pris sur la pointe fait réorganiser N à chaque orphelin Bitcoin (≈ 100 blocs N perdus) et scinde N pendant les courses Bitcoin | Relecture aveugle | FAIL réel (analytique) | v0.1 : repère Bitcoin enfoui à `d_ref` = 6, progression bornée | — |
| v0 | Le départage sur l'identifiant de bloc est grindable ⇒ l'adversaire gagne toutes les égalités ⇒ exclusion ciblée d'une identité via le calendrier public | Relecture aveugle | FAIL réel (analytique) | v0.1 : départage indépendant du contenu des blocs ; ommers signés crédités pour l'activité | — |
| v0.2.1 | Égalité par équivoque : deux variantes au même départage bloquent les honnêtes sur le préfixe (≈ 5 h pour 1 M sats, répétable) | Relecture aveugle (trois relecteurs) | FAIL réel (analytique) | v0.3 §7.3 : un producteur peut prolonger n'importe quelle pointe à égalité, et toute extension gagne strictement | État explicite `EQUIVOCATION_TIE_STALLED` (N-SPEC §9.4) |
| v0.5 | Le frein de densité à 7/10 est un interrupteur de vivacité que l'adversaire maintient gratuitement par abstention calibrée ou rétention | Relecture aveugle | FAIL réel (analytique) | v0.6 : santé mesurée hors identités QUEUED, plus une voie lente d'exclusion (1 % sur 7 époques) | Témoins TLA+ de la voie lente ; mutation « le frein annule tous les budgets » détectée |
| v0.7 | **Livraison à 0,70 bloquée par l'abstention adverse** : au coin du domaine (β = 0,30 qui s'abstient, d = 0,70), la densité attendue vaut ≈ 0,49, sous le seuil de laboratoire 7/10 ; la livraison est suspendue | Analyse (contrôle de cohérence) | Réel (vivacité seulement ; la sûreté ne demande que ≈ 0,17) | Décision Q3 du propriétaire : profil de livraison H_N `rho_deliv = 43/100` ; constante de frein du consensus inchangée à 7/10 ; profondeur par défaut K(10⁻⁶) = 739 blocs | Non-interférence TLA+ : **13 PASS bornés**, 5 TÉMOINS, 3 FAIL de mutation (fuite du seuil vers la sélection, le frein, STOP) ; **QR-5** |
| v0.6 → v0.7 | **6 s contre la propagation de blocs de 256 Ko** : en W1 (≈ 170 ms d'aller-retour, 0,5 % de perte), des blocs complets de 256 Ko atteignent un pire cas de 4,7 s par saut pour un budget de 5 s ; à 2 sauts, 10 % des blocs honnêtes sont en retard. Une connexion TCP unique avec pertes écoule ≈ 150 Ko/s | Banc (mesure européenne + émulation sur liens réels) | FAIL réel de τ = 6 s au-delà d'un saut | Décision du propriétaire : **τ = 10 s** (W1 à 2 sauts ≈ 10⁻⁵, extrapolé) ; W2 hors domaine. Aucune optimisation de propagation supposée | **QR-1, QR-2** |
| v0.5 / v0.6 | **Le couple 7 200 / 2 880 n'a jamais été dérivé** : en profil A, il n'est certifié qu'à τ = 6 s, p_late = 0 et ε_H = 10⁻⁶ ; il échoue dès τ ≥ 8 s ou Q_B = 256 (b > b_max) | Analyse (DP exacte + composition) | FAIL réel (analytique) du choix de paramètres | Couple abandonné. Dérivé sous H_N : **K_reg = 2 750, registry_min_blocks = maxreorg = 1 630**, ε_H ≈ 4,6·10⁻¹⁰. Le couple arrondi naïvement (2 740 ; 1 630) est aussi rejeté, car b_max(2 740) = 1 629 | Script de dérivation reproductible et table `composition` |
| v0.7 | Écart de 1,3 à 1,8 entre DP et Monte-Carlo sur K | Analyse + Monte-Carlo (aucun run MC ne dépasse la DP : MC/DP ≤ 0,61 ; aucun dépassement significatif de l'attaque privée exacte à départage défavorable, z max = +1,6) | Non expliqué | DP (conservatrice) publiée | **QR-3** |

---

## 5. Ce qui reste ouvert

Le gel de l'architecture laisse dix exigences traçables. Un testnet public suppose QR-1 à QR-9 acceptées.

| ID | Point ouvert | En cas d'échec |
|---|---|---|
| QR-1 | Mesurer Δ, l'écart d'horloge et p_late avec un client N réel, sur au moins 3 continents, avec au moins 2 sauts réels et des blocs maximaux | Réviser τ ou le domaine, ou optimiser la propagation |
| QR-2 | Corrélation des retards et borne par fenêtre, coupures et DoS ciblé compris | Intégrer la corrélation dans la dérivation de K ; les retards ciblés comptent dans β |
| QR-3 | Expliquer l'écart DP/MC sur K | Une stratégie qui dépasse la DP est un contre-exemple et rouvre K_reg |
| QR-4 | Terminer l'exploration stricte du pivot profond, ou en prouver une abstraction | Violation d'invariant : réouverture architecturale |
| QR-5 | Non-interférence de la livraison avec le frein fidèle, puis sur l'implémentation | Fuite vers le consensus : correction dans l'implémentation |
| QR-6 | Preuve de composition rédigée et relue indépendamment | Borne révisée ; K_reg et b re-dérivés |
| QR-7 | Grinding de la graine Bitcoin qualifié ; décision sur Q_B | Paramètre re-dérivé, aucune mécanique |
| QR-8 | Procédure de RECOVERY par nœud spécifiée et testée | Réouverture limitée à la section de récupération |
| QR-9 | A4 (compatibilité des ancres) requalifiée aux paramètres v0.7 | Violation d'invariant : réouverture |
| QR-10 | Profils clients alignés sur H_N | Documentation |

Également ouverts ou non couverts : rien ne garantit qu'un STOP se déclenche hors H_N (en particulier en W2) ; des horloges macOS ont été mesurées entre 85 et 120 ms, à la limite de H_N-8 ; Δ_val n'inclut pas l'accès à l'état ; les modèles TLA+ utilisent des constantes abstraites et ne sont pas composés en un modèle global.
