# Rapport TLA+ — N-SPEC v0.6

30 septembre 2026. Exécution de `MANDAT-TLA-v0.6.md`, §8 prioritaire. Sources normatives et modèles v0.5 conservés ; aucune commande Git.

## Résultat et décision de qualification

Le miroir élargi final est **NON QUALIFIÉ : voir statuts par vecteur** avec A activée. A désactivée : **le FAIL historique est retrouvé sur les quatre vecteurs**. Les premières explorations interrompues restent INCOMPLET ; elles ne sont pas converties en PASS.

A activée, les quatre vecteurs finaux donnent **3 PASS, 1 INCOMPLET, 0 FAIL**. L’interruption d’un seul vecteur suffit à empêcher un PASS composé.

Les 9 scénarios d’ordre H1 corrigés donnent 9 PASS bornés. Sensibilité : **13/13 mutations** réfutées par un moniteur attendu, avec code TLC 12. Voie lente : PASS ; témoin de sortie après libération de quota : TÉMOIN.

**Gel bloqué.** CP_reg et A4 ne sont pas qualifiés sous un domaine H_N propre à N. Des contre-exemples bornés sont publiés. Les familles de modèles ne sont pas composées en un modèle global ; plusieurs obligations restent NT, en particulier le contrôle complet, la vivacité générale et l’application monétaire complète. La livraison n’est donc pas une qualification intégrale du mandat.

## 1. Miroir de la règle A — §8.1

Même générateur élargi que v0.5 : deux honnêtes, un adversaire, poids `(2,1,1)`, deux branches, trois époques, deux slots par époque, slots 0–5, KReg=1, maxreorg=registry_min_blocks=4, divergence autorisée dès 0. Seul `RuleA` diffère dans chaque paire finale. La nouvelle maturité est réduite au début de l’époque : cette restriction est explicitement compensée par les sondes de fenêtre et de fermeture, sans prétendre composer leurs résultats.

| Bitcoin | A désactivée : fort | A activée : fort + C6 | Distincts A on | File publiée |
|---|---|---|---:|---:|
| (0,0,0) | [MC_fast_off_00](logs/MC_fast_off_00.log) : FAIL | [MC_fast_on_00](logs/MC_fast_on_00.log) : PASS | 280913 | 0 |
| (0,0,1) | [MC_fast_off_01](logs/MC_fast_off_01.log) : FAIL | [MC_fast_on_01](logs/MC_fast_on_01.log) : PASS | 141242 | 0 |
| (0,1,0) | [MC_fast_off_10](logs/MC_fast_off_10.log) : FAIL | [MC_fast_on_10](logs/MC_fast_on_10.log) : INCOMPLET | 549892 | 72479 |
| (0,1,1) | [MC_fast_off_11](logs/MC_fast_off_11.log) : FAIL | [MC_fast_on_11](logs/MC_fast_on_11.log) : PASS | 278093 | 0 |

La composition est exhaustive uniquement si les quatre lignes A on terminent avec file vide : Init impose bitcoin[0]=0, les deux autres composantes valent 0 ou 1, et Next ne modifie jamais Bitcoin dans cette famille. Les quatre états d’entrée sont disjoints et leur union est exactement Init. Pour un INCOMPLET, les compteurs du tableau sont ceux du dernier point publié, pas une file finale épuisée. Aucun filtrage de densité, contrainte d’état, symétrie ou limite de profondeur ne retire une histoire.

| Replay historique | A désactivée | A activée |
|---|---|---|
| spec | [MC_v6_replay_spec_off](logs/MC_v6_replay_spec_off.log) : FAIL ; 9 distincts ; 0.58 s | [MC_v6_replay_spec_on](logs/MC_v6_replay_spec_on.log) : PASS ; 9 distincts ; 0.57 s |
| spec_adopt | [MC_v6_replay_spec_adopt_off](logs/MC_v6_replay_spec_adopt_off.log) : FAIL ; 13 distincts ; 0.65 s | [MC_v6_replay_spec_adopt_on](logs/MC_v6_replay_spec_adopt_on.log) : PASS ; 13 distincts ; 0.64 s |

Le replay signature conserve maxreorg=4 et EndSlot=5 ; celui d’adoption conserve maxreorg=1 et EndSlot=4. Les parcours attendus sont respectivement 9 et 13 états. Un PASS de replay ne prouve que ce parcours. Le témoin [MC_witness_mirror_advance](logs/MC_witness_mirror_advance.log) donne TÉMOIN : A avance réellement le support. [MC_witness_mirror_empty](logs/MC_witness_mirror_empty.log) donne TÉMOIN après deux époques entièrement vides.

`RegistryModelV6` implémente la fermeture sur l’en-tête candidat, l’héritage, le compte inclusif et le maintien du registre déjà installé tant que la fenêtre est ouverte. `RegistryModelFast2` calcule la même fonction plus directement dans la projection ADD. Les sondes d’équivalence 1/2/4, la justification algébrique et les versions intermédiaires sont décrites dans [PORTEE-ET-MAPPING.md](PORTEE-ET-MAPPING.md). L’ancien invariant fort demeure inchangé ; C6 ne le remplace pas.

### C6 sur la sonde générale — moniteur local séparé du fort

Les recherches regroupées à seuil 1 et 2 ont été interrompues au plafond : elles restent INCOMPLET. Les partitions suivantes gardent le même Init/Next et fixent seulement les deux composantes Bitcoin invariantes. Leur union couvre exactement les quatre entrées initiales. Aucune prémisse CP_reg ne filtre les histoires.

| Seuil | (0,0,0) | (0,0,1) | (0,1,0) | (0,1,1) | Composition |
|---|---|---|---|---|---|
| 1 | [MC_c6_k1_00](logs/MC_c6_k1_00.log) : PASS | [MC_c6_k1_01](logs/MC_c6_k1_01.log) : PASS | [MC_c6_k1_10](logs/MC_c6_k1_10.log) : PASS | [MC_c6_k1_11](logs/MC_c6_k1_11.log) : PASS | PASS borné C6 — 792500 états |
| 2 | [MC_c6_k2_00](logs/MC_c6_k2_00.log) : PASS | [MC_c6_k2_01](logs/MC_c6_k2_01.log) : PASS | [MC_c6_k2_10](logs/MC_c6_k2_10.log) : PASS | [MC_c6_k2_11](logs/MC_c6_k2_11.log) : PASS | PASS borné C6 — 630030 états |

Dans le miroir et ces partitions, `RegistryStableOnCommonPrefix` compare directement les registres des engagements locaux successifs à supports égaux ; il ne conserve pas toutes les anciennes époques. Les sondes `RegistryCommitmentsChecked` et le journal persistant `RegistryAudit` comparent en plus la projection ADD du contrôle et le calendrier dérivé, entre nœuds et engagements conservés, sans modifier les actions de production/adoption. Le contrôle complet de la SPEC reste NT.

## 2. H1 — §8.2

`H1OrdersChecked` explore toutes les permutations unitaires des six événements C/W/L/BTC/F/A par nœud, leurs entrelacements et les livraisons groupées simultanées. Les états peuvent être fusionnés par TLC quand toutes les données et l’état d’adoption pertinent coïncident : aucun ordre n’est exclu. C est supérieure, W inférieure, et L fournit une troisième branche.

| Scénario | Résultat |
|---|---|
| [MC_h1_forward_checked](logs/MC_h1_forward_checked.log) | PASS ; 30276 distincts ; 2.44 s |
| [MC_h1_forward_k2_checked](logs/MC_h1_forward_k2_checked.log) | PASS ; 27556 distincts ; 2.36 s |
| [MC_h1_inverse_checked](logs/MC_h1_inverse_checked.log) | PASS ; 26896 distincts ; 2.54 s |
| [MC_h1_mutual_checked](logs/MC_h1_mutual_checked.log) | PASS ; 50176 distincts ; 3.24 s |
| [MC_h1_foreign_checked](logs/MC_h1_foreign_checked.log) | PASS ; 26896 distincts ; 2.56 s |
| [MC_h1_false_checked](logs/MC_h1_false_checked.log) | PASS ; 26896 distincts ; 2.59 s |
| [MC_h1_losers_checked](logs/MC_h1_losers_checked.log) | PASS ; 28224 distincts ; 2.58 s |
| [MC_h1_shallow_checked](logs/MC_h1_shallow_checked.log) | PASS ; 16384 distincts ; 2.05 s |
| [MC_h1_stale_checked](logs/MC_h1_stale_checked.log) | PASS ; 30276 distincts ; 2.49 s |

Les invariants comparent le résultat H1 quand les données reçues sont identiques et exigent `AdoptedWithH1 ⊆ AdoptableByBaseN`. Les témoins CommonVeto, Maintain et Unknown sont séparés des PASS. Les mutations vérifient notamment la prise en compte d’une perdante jamais adoptée, MAINTAIN et l’indépendance de Deep vis-à-vis de l’ancre. Les motifs d’ancre/BTC de la base N sont testés séparément ; leur composition avec H1 reste NT et aucune sûreté sous éclipse n’en est déduite.

`H1Scan` distingue références étrangères, dossiers pertinents manquants, fenêtres mûres, étapes strictes de progrès et scan complet. `H1Reevaluation` conserve le motif de base pendant un veto, réévalue sur rang et Bitcoin et conserve l’archive lors d’une éviction. Le contre-exemple de cadence avec anciennes références est publié ci-dessous.

## 3. Frein mécanique — §8.3

Calendrier réduit L=5, vingt époques, cinq producteurs, W=1000. L’identité 1 est présente à 2/3, les autres sont silencieuses ; l’identité 5 a un auto-ommer au slot 44, sans crédit d’activité mais bloquant son éligibilité lente. Activité, suspicion, file et récupérations sont rejouées avant santé ; le masque Q est fixe. Les quotas 2 %/époque, 5 %/sept époques et 1 % lent/sept époques sont entiers et prospectifs.

| Époque | W_f | Budget lent | Exclusion | Rotation |
|---:|---:|---:|---|---|
| 10 | 1000 | 10 | IID 4, poids 5 | exécutée sous frein |
| 11–16 | 995 | 4 | aucun lot supplémentaire admissible | sans condition de santé |
| 17 | 995 | 9 | IID 5, poids 5 | déjà effectuée |

Ce tableau est le calcul de référence de [tools/brake_reference.py](tools/brake_reference.py), à confronter aux témoins TLC : [MC_witness_brake_Slow_checked](logs/MC_witness_brake_Slow_checked.log) = TÉMOIN, [MC_witness_brake_Release_checked](logs/MC_witness_brake_Release_checked.log) = TÉMOIN. La propriété temporelle sous WF(Advance) donne INCOMPLET en formulation directe, et PASS avec la formulation équivalente par avancement d’époque. Elle ne démontre pas une reprise productive infinie.

Aucune appréciation locale n’intervient une fois calendrier, support et observations fixés. La SPEC impose cette mécanique. Les arrondis W<100, les identités indivisibles trop lourdes et l’absence persistante d’avancement de support restent des blocages intentionnels. La sonde pondérée 0,68 est distincte du calendrier cyclique : 680 présents, 120 honnêtes disparus, 200 adverses abstinents ; le masque QUEUED retire ces derniers de la mesure de santé sans confondre santé et livraison.

## 4. Contre-exemples et séparation des garanties

| Recherche | Résultat final | Interprétation |
|---|---|---|
| [MC_general_a_k1_strong](logs/MC_general_a_k1_strong.log) | FAIL | Contre-exemple avec productions de la loterie abstraite, A active, maxreorg=1. |
| [MC_general_a_k2_strong](logs/MC_general_a_k2_strong.log) | FAIL | Même défaut à maxreorg=2, sans déconnexion excessive. |
| [MC_audit_cp_k1](logs/MC_audit_cp_k1.log) | FAIL | Journal persistant des engagements honnêtes : CP_reg séparé. |
| [MC_audit_cp_k2](logs/MC_audit_cp_k2.log) | FAIL | Journal persistant, seuil 2. |
| [MC_replay_audit_c6](logs/MC_replay_audit_c6.log) | PASS | C6 sur le même parcours qui viole le fort et CP_reg. |
| [MC_registry_commits_CPreg_checked](logs/MC_registry_commits_CPreg_checked.log) | FAIL | D_e diffère malgré même contexte ; obligation A3 non acquise. |
| [MC_registry_commits_RegistryImmutable_checked](logs/MC_registry_commits_RegistryImmutable_checked.log) | FAIL | La règle A n’assure pas une immutabilité globale inconditionnelle. |
| [MC_registry_commits_C6_checked](logs/MC_registry_commits_C6_checked.log) | PASS | Lemme conditionnel séparé ; aucun filtre CP_reg. |
| [MC_anchor_agreement_checked](logs/MC_anchor_agreement_checked.log) | FAIL | Ancres incompatibles après livraisons séparées, sans domaine réseau qualifié. |
| [MC_tie_reservations](logs/MC_tie_reservations.log) | FAIL | Convergence des données n’efface pas des réservations antérieures différentes. |
| [MC_scan_stale_counterexample](logs/MC_scan_stale_counterexample.log) | FAIL | La fréquence des empreintes seule ne borne pas la fraîcheur du progrès. |

Contre-exemples issus du générateur de production, sans mutation : [MC_replay_general_k1](logs/MC_replay_general_k1.log) et [MC_replay_general_k2](logs/MC_replay_general_k2.log). Un bloc B_0 porte un ADD pour le producteur 2. Au slot 4, le nœud 1 signe C_4 avec `(2,1,1)` ; le nœud 2 signe B_4 avec `(2,2,1)` après fermeture de la fenêtre. Le nœud 1 reçoit ensuite cette branche supérieure et installe le second registre, dans la même époque et le même contexte. Au seuil 2, B_3 fournit le bloc comptable supplémentaire. La pointe adoptée antérieure du nœud 1 est genesis : **zéro déconnexion**, donc aucun STOP profond attendu. Même la branche du seul bloc C_4 signé ne représenterait qu’une déconnexion. La règle A est respectée sur chaque branche ; la propriété forte demeure trop forte sans CP_reg.

Le journal global trouve CP_reg en 11 états au seuil 1 et 12 au seuil 2, sur leurs vecteurs Bitcoin fixes. Au seuil 1, la partition reste active : deux signatures honnêtes de l’époque 2 portent des D_e différents, et des registres `(2,1,1)` / `(2,2,1)`. Le moniteur local fort est encore vrai à ce point ; aucune déconnexion ni réunion n’est requise pour ce FAIL global. Le replay court [MC_replay_audit_min_k1](logs/MC_replay_audit_min_k1.log) donne FAIL. Le domaine réseau non borné est annoncé avant la recherche ; aucune hypothèse corrective n’est introduite après coup.

Recherche BFS à un worker : [MC_min_general_k1](logs/MC_min_general_k1.log) = FAIL (profondeur 13), [MC_min_general_k2](logs/MC_min_general_k2.log) = FAIL (profondeur 14). Les replays imposés des premières traces contiennent respectivement 13 et 14 états ; la minimalité BFS porte uniquement sur ces bornes et ce générateur, sous la réserve habituelle des fingerprints TLC.


Le replay de fermeture [MC_replay_closure_checked_fixed](logs/MC_replay_closure_checked_fixed.log) compare `⟨0,11,13⟩` à `⟨0,23⟩`. Le bloc 0 est commun et seul antérieur à la coupure 1 ; les comptes jusqu’au porteur au slot 3 sont 2 et 1. Au seuil 2, le registre passe de `(3,1,1)` à `(2,1,1)`. Le LCA a hauteur 1 : **deux déconnexions, égales à maxreorg=2**, donc ce n’est pas un cas exigeant >maxreorg. L’ancre éventuelle au bloc commun n’empêche pas ce changement de compte. Les fixtures sont déclarées validées, mais cette sonde ne vérifie ni la loterie ni Rank : son passage de longueur 3 à longueur 2 ne démontre donc pas une adoption conforme à BaseNDecision. Il illustre le changement de fermeture et sa distance. Les contre-exemples issus des productions ci-dessus, indépendants de cette fixture, interdisent de généraliser le PASS du miroir.

Le replay [MC_replay_anchor_split_checked_fixed](logs/MC_replay_anchor_split_checked_fixed.log) adopte A chez le nœud 1 et B chez le nœud 2, chacune de hauteur 3. Les bornes N/BTC autorisent une ancre de hauteur 2 de chaque côté. Elles sont incompatibles. La première hypothèse manquante est une borne réseau sur l’histoire de construction et de livraison, pas seulement après réunion. La SPEC n’est ni modifiée ni complétée par un verrou pour cacher ce résultat.

## 5. Mutations négatives

| Mutation | Moniteur attendu | Résultat observé |
|---|---|---|
| Cliché sur pointe | ARule | [MC_mut_registry_tip_checked](logs/MC_mut_registry_tip_checked.log) : FAIL — ARule |
| Suppression du seuil A | ARule | [MC_mut_registry_no_threshold_checked](logs/MC_mut_registry_no_threshold_checked.log) : FAIL — ARule |
| Registre engagé utilisé comme veto | NoJournalVeto | [MC_mut_registry_lock_checked](logs/MC_mut_registry_lock_checked.log) : FAIL — NoJournalVeto |
| H1 promoteur | H1Subset | [MC_mut_h1_promote_checked](logs/MC_mut_h1_promote_checked.log) : FAIL — H1Subset |
| H1 limité à l’adoptée | H1Order, H1NonVacuity, NoContinuation | [MC_mut_h1_adopted_only_checked](logs/MC_mut_h1_adopted_only_checked.log) : FAIL — H1NonVacuity |
| MAINTAIN saute H1 | H1Order, H1NonVacuity, NoContinuation | [MC_mut_h1_maintain_checked](logs/MC_mut_h1_maintain_checked.log) : FAIL — NoContinuation |
| Deep dépend d’une ancre locale | H1Order, H1Orientation | [MC_mut_h1_anchor_deep_checked](logs/MC_mut_h1_anchor_deep_checked.log) : FAIL — H1Orientation |
| Frein annule tous les budgets | Mechanical | [MC_mut_brake_checked](logs/MC_mut_brake_checked.log) : FAIL — Mechanical |
| ADD efface le passif | AddNoReset | [MC_mut_add_checked](logs/MC_mut_add_checked.log) : FAIL — AddNoReset |
| Ancre libre à la pointe | AnchorExact | [MC_mut_free_anchor_checked](logs/MC_mut_free_anchor_checked.log) : FAIL — AnchorExact |
| Scellement oublié | G0 | [MC_mut_forget_seal_checked](logs/MC_mut_forget_seal_checked.log) : FAIL — G0 |
| Réservation par génération | S1 | [MC_mut_generation_checked](logs/MC_mut_generation_checked.log) : FAIL — S1 |
| Import non idempotent | MON1, MON2, MON3, MON4 | [MC_mut_import_checked](logs/MC_mut_import_checked.log) : FAIL — MON1 |

Aucune mutation n’est active dans les configurations conformes. Un PASS de mutation serait une absence de sensibilité, jamais un succès. Les premiers essais dont l’audit devenait une garde sont conservés, marqués développement, et ne sont pas comptés dans les 13 contrôles.

## 6. Outils, exécution et limites

Java fourni : OpenJDK Homebrew 21.0.12.1 ; TLC 2.19 du 8 août 2024, révision 5a47802. JAR copié depuis `modele-v0.5/tla2tools.jar`, lanceur `LocalTLC.java` local sans réseau conservé. Aucun besoin du JAR absent de `etudes/sequenceur/tla/`, ni de téléchargement.

Un verrou de fichier sérialise les explorations. Maximum quatre workers, `-Xmx3g`, BFS, seed 1, répertoire d’états temporaire propre. Le lanceur initial envoyait SIGTERM au plafond de 570 s ; les durées globales peuvent inclure quelques dixièmes de seconde de nettoyage après ce signal. Le lanceur final prend une marge à 569 s et arrête aussi les erreurs fatales de modèle au lieu d’attendre le plafond. Tous les runs interrompus restent INCOMPLET. Les compteurs d’un timeout sont parfois le **dernier point publié**, la file exacte à l’arrêt n’étant pas fournie par TLC.

Le lanceur final fixe aussi le polynôme de fingerprint à `-fp 0` pour les reproductions ; les premiers runs utilisaient l’index choisi par TLC, publié dans leur en-tête. Certains processus Python avaient été mis en attente avant les dernières corrections du lanceur de reproduction : leurs empreintes `run.py` décrivent le fichier sur disque au début du run, pas nécessairement le code Python déjà chargé. La commande Java réellement exécutée, inscrite dans chaque log, fait autorité ; les modèles/configurations et le JAR sont ceux lus pour ce run. Les fingerprints TLC ont un risque résiduel de collision : les estimations publiées par TLC pour chaque PASS restent dans les logs et RESULTATS.json. Elles ne sont pas une epsilon_CP de N. Les runs avec quatre workers ne garantissent pas une trace minimale unique ; les replays explicites donnent des parcours courts reproductibles. Les erreurs syntaxiques, de quantification et d’affectation rencontrées pendant le développement restent des erreurs de modèle/outillage, jamais des FAIL normatifs.

## 7. Reproduction et dossier de preuve

```sh
cd etudes/n-spec/tla/modele-v0.6
TLC_RUN_LABEL=verification ./run.sh MC_fast_off_00 MC_fast_on_00
TLC_RUN_LABEL=h1 ./run.sh MC_h1_forward_checked
TLC_RUN_LABEL=frein ./run.sh MC_brake_slow_checked MC_witness_brake_Release_checked
```

Le contrôle de reproduction `reproduction_check` a retrouvé le FAIL RegistryImmutable attendu en 13 états, avec les logs et la trace d’origine inchangés ; sa validation est dans `logs/reproductions/reproduction_check/VALIDATION.json`. Le label écrit dans un dossier distinct et préserve les logs livrés. Sans label, un run existant est refusé. [RESULTATS-DETAILLES.md](RESULTATS-DETAILLES.md) donne chaque statut, code, compteurs, profondeur, file et durée ; [RESULTATS.json](RESULTATS.json) conserve les configurations exactes et les motifs. Les `.cfg` sont les restrictions exécutables, les logs et [traces/](traces/) les preuves brutes. [PORTEE-ET-MAPPING.md](PORTEE-ET-MAPPING.md) expose les abstractions et H_N ; [COUVERTURE-SONDES.md](COUVERTURE-SONDES.md) inventorie les sondes et NT ; [OBLIGATIONS.md](OBLIGATIONS.md) distingue les moniteurs des obligations complètes, et [TRACES-LECTURE.md](TRACES-LECTURE.md) indexe les contre-exemples. `SHA256.json` et `INTEGRITE-ORIGINAUX.json` identifient les fichiers et contrôlent les copies antérieures.


## 8. Complément orchestrateur — vecteur (0,1,0) du miroir, A activée, sans plafond

Exécuté après la clôture de la campagne Codex, hors de son lanceur (plafond de 570 s levé, 8 workers, tas 6 Go, `-seed 1 -fp 0`,
mêmes `MC_fast_on_10.tla/.cfg` et `RegistryModelFast2.tla` — SHA-256 : `7b636571…f59f29c`, `8803b221…1a1de1f`, `5b8ddcfa…341b9efec`).
Log : [logs/orchestrateur/MC_fast_on_10.log](logs/orchestrateur/MC_fast_on_10.log). Script : `run_uncapped_orchestrateur.sh`.

| Vecteur | Résultat | Générés | Distincts | File finale | Profondeur | Durée | Collision (optimiste) |
|---|---|---:|---:|---:|---:|---|---|
| (0,1,0), A on, fort + C6 | **PASS** | 4 509 097 | 630 806 | 0 | 27 | 6 min 52 s | 1,3 × 10⁻⁷ |

Avec ce résultat, les quatre vecteurs Bitcoin de la sonde élargie donnent, A activée, **PASS avec file vide** (280 913 + 141 242 + 630 806 + 278 093
= 1 331 054 états distincts) ; leur union est exactement `Init` et `Next` ne modifie jamais Bitcoin (§1). On peut donc écrire :
**A ON : PASS exhaustif 4/4 sur l'union des quatre vecteurs modélisés ; A OFF : FAIL `RegistryImmutable` 4/4.**
Le statut « 3 PASS + 1 INCOMPLET » du §1 reste celui de la campagne Codex sous son plafond ; il n'est pas réécrit. Ce PASS ne change rien aux
conclusions des §4 et §7 : CP_reg et A4 restent non qualifiés, le gel reste bloqué.
