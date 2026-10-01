# Pivot profond : qualification TLA+

1er octobre 2026. Objet : confirmer ou réfuter en TLA+ le « pivot profond » de [LEMME-L1-opus.md](LEMME-L1-opus.md) §4.4, dans la machine N-SPEC v0.6 telle qu'elle est ([CONFRONTATION-LEMME-L1.md](CONFRONTATION-LEMME-L1.md) §3 point 3). Aucune règle N n'est proposée, aucun profil n'est adopté, aucune opération git n'a été faite. Artefacts : [pivot-profond/](../tla/modele-v0.6/pivot-profond/).

## 1. Verdict

**Le pivot profond est CONFIRMÉ comme exécution atteignable** du miroir réduit : fermeture précoce privée sous le seuil, héritage, puis prise d'avantage. Nous en avons trois témoins stricts : deux replays dirigés et une exploration semi-dirigée. Un quatrième vient d'une exploration à adversaire restreint. **Dans chacun d'eux, maxreorg ne transforme pas l'événement en STOP** : le nœud honnête synchronisé adopte la branche gagnante après 2 ou 3 déconnexions, sous le seuil, et CP_reg(e) est violée. Le contraste montre qu'un STOP n'apparaît que lorsque la chaîne honnête compte plus de maxreorg blocs après la fourche.

Transposée aux paramètres réels (arithmétique, hors TLA+), cette frontière dépend de h et de l'instant de l'engagement. Le détail est au §5.

## 2. Pourquoi un nouveau miroir

`RegistryModelFast2` réduit la maturité au début d'époque : `Carrier(c,e)` est le premier bloc de créneau ≥ start(e). Toute fenêtre y ferme donc au même point, et la fermeture précoce qui définit le pivot profond y est **structurellement impossible**. Les PASS Fast2 et L1 ne disent rien de ce cas. `RegistryModel_PivotDeep.tla` reprend de Fast2 le codage des blocs, la formule de loterie jouet, le rang (longueur, puis séquence de `tie`), le test `Len(tip)−LCA > MaxReorg` et l'ancre. Il ne change qu'une chose : la maturité m_E est un fait **par bloc**, avec les contraintes suivantes.

- Un bloc ne peut porter m_E que si son créneau est ≥ `MatMin`. C'est la borne MTP du §8.4, soit freeze + 6 000 créneaux = cut + 13 200 dans les paramètres réels.
- m_E n'existe qu'à partir de l'instant `BtcMat`. Les honnêtes l'incluent dès cet instant (discipline d_ref).
- L'adversaire peut signer **après BtcMat** un bloc d'un créneau passé ≥ MatMin qui porte m_E (antidatage). La validation historique ne l'interdit pas.
- Le repère s'étend du parent à l'enfant, et tout bloc de l'époque E porte m_E.
- La règle A est celle du §5.2 (compte inclusif jusqu'au porteur ; héritage de A_1 = genesis si le compte est inférieur à `registry_min_blocks`). Ce paramètre vaut maxreorg (profil §3.3).
- Une installation de R_E a lieu à l'adoption d'une chaîne dont la fenêtre est fermée. Signatures, adoptions et installations sont journalisées, comme dans CP_reg (§5.7.2).

Constantes des replays : L = 8, K_reg = 4 (cut = 4, freeze = 8, start = 16), MatMin = 12, BtcMat = 14, b = maxreorg = 4. Les proportions respectent le réel : K_reg = L/2 ; MatMin = freeze + ⌈0,42 L⌉ ; BtcMat ≈ freeze + 0,75 L. Explorations : L = 4, K_reg = 2, MatMin = 6, BtcMat = 7, b = 2, horizon de 12 créneaux.

## 3. Propriété observable

Soit x le côté qui passe le seuil (X) et y le côté gagnant sous le seuil (Y). `DeepShapeChains(x,y)` exige :

1. les deux fenêtres fermées, **le même préfixe brut** et `Pass(x) ∧ ¬Pass(y)` : on est dans la classe `ii_pivot` ;
2. **une fermeture précoce** : `slot(porteur y) < slot(porteur x)` et `slot(porteur y) < BtcMat`, donc un créneau qu'aucun porteur honnête ne peut occuper, atteint seulement par antidatage ;
3. tous les blocs de y postérieurs à la fourche sont byzantins (branche privée) ;
4. **un passage robuste de x** : les seuls blocs honnêtes de la fenêtre de x atteignent le seuil (`HonestCount(x) ≥ b`).

Deux variantes d'engagement :

- `DeepSync` : un honnête, dont la pointe précédente portait le D_E de x, installe y avec une déconnexion > 0 ;
- `DeepAfterSig` : un honnête installe y après qu'un autre honnête a signé un bloc de E sur x.

**Distinction avec le pivot peu profond** (`MC_replay_closure_checked_fixed_L1`, 2 déconnexions). Dans celui-ci, les deux histoires ferment au même créneau et le compte bascule par un bloc adverse dans la fenêtre (zone de compte). Les clauses 2 et 4 l'excluent. Le contrôle `MC_replay_shallow_PivotDeep` le vérifie dans le même miroir : il atteint `ii_pivot` avec deux porteurs honnêtes (créneaux 14 et 17), et `DeepAbsent` tient sur tout le chemin. Sans la clause 4, l'exploration trouve d'abord une forme **mixte** : X passe grâce à un bloc byzantin public au créneau 6, équivoque avec le porteur privé du même créneau. Elle est rapportée à part.

## 4. Runs

Lanceur livré non modifié, label `pivot_profond_final`, 4 workers, 3 Gio, plafond de 569 s.

| Run | Nature | Statut | États distincts | Profondeur | Durée (s) |
|---|---|---|---:|---:|---:|
| `MC_replay_sync_PivotDeep` | replay, SYNC avant start(E) | TÉMOIN `NoWitnessDeepSyncBeforeStart` | 32 | 32 | 1,45 |
| `MC_replay_aftersig_PivotDeep` | replay, AFTER_SIG après start(E) | TÉMOIN `NoWitnessDeepAfterSig` | 42 | 42 | 3,73 |
| `MC_replay_stop_PivotDeep` | replay de contraste | TÉMOIN `NoWitnessDeepStop` (`DeepAbsent` tenu) | 44 | 44 | 1,04 |
| `MC_replay_shallow_PivotDeep` | replay de contrôle, zone de compte | TÉMOIN `NoWitnessPivot` (`DeepAbsent` tenu) | 33 | 33 | 0,88 |
| `MC_explore_mixed_PivotDeep` | BFS, `Next` complet, forme mixte | TÉMOIN `NoWitnessMixedSync` | 523 997 | 16 | 41,39 |
| `MC_explore_sync_PivotDeep` | BFS, `Next` complet, forme stricte | **INCOMPLET** (interrompu, 3 056 203 en file) | 5 211 850 | ≥ 19 | 569,19 |
| `MC_explore_sync_restricted_PivotDeep` | BFS, adversaire limité à sa voie privée | TÉMOIN `NoWitnessDeepSync` | 1 082 953 | 19 | 109,37 |
| `MC_explore_suffix_PivotDeep` | BFS exhaustive après un préfixe fixé | TÉMOIN `NoWitnessDeepSync` | 159 906 | 23 | 25,31 |

Chaque run vérifie aussi `TypeOK`, `MaturityLegal` (maturité ≥ MatMin, porteurs monotones, blocs de E mûrs), `AdoptWithinMaxreorg` et `NoOtherStructural`. **Aucun n'a été violé.** En particulier, aucun « autre » structurel n'apparaît : c'est cohérent avec la dichotomie d'Opus §4.1. Il n'y a **aucun PASS exhaustif** : l'exploration complète de la forme stricte est INCOMPLET, ce qui ne vaut pas PASS. Les témoins restreint et semi-dirigé sont des comportements de `Spec`, car chacun de leurs pas est un pas de `Next`. Quatre runs antérieurs sont archivés sans être retenus : une erreur de configuration, deux bogues de moniteur (entrée de journal lue avant l'ajout du porteur, puis comparaison de chaîne de caractères avec un entier) et le prédicat faible.

**Lecture des témoins.** Dans les replays, les blocs honnêtes 1, 2, 4 et 5 sont communs (c = 2 dans la fenêtre), puis la voie privée s'enracine après le créneau 5.
- *SYNC.* Les honnêtes produisent 13 puis 14 ; 14 porte m_E et X ferme avec un compte honnête de 4 ≥ 4. Les deux nœuds installent le brut. Au créneau 14, l'adversaire antidate 12 avec m_E : Y ferme avec 3 < 4 et hérite. Il signe ensuite 15. Au créneau 15, le nœud 1 voit Y, à égalité de longueur, départagé par le tie jouet (12 < 13). Il **adopte Y avec 2 déconnexions** et installe D_E = genesis alors qu'il avait installé le brut.
- *AFTER_SIG*, sans recours au tie. Le nœud 1 signe 17 sur X, sous le calendrier de R_brut. Y croît à 18 et 21 sous son propre calendrier hérité. Le nœud 2, synchronisé sur X jusqu'à 17, adopte Y (4 blocs contre 3 après la fourche) avec **3 déconnexions ≤ 4**.
- *Exploration restreinte.* Le nœud 2 signe le bloc 11 de E sur X (compte honnête {5, 11} = 2), puis adopte Y = {6 antidaté, 9, 12} avec 2 déconnexions. **Le même nœud signe D_brut puis adopte D_genesis**, ce qui est aussi une violation au sens du §5.7.2 (« y compris chez le même nœud »).
- *Semi-dirigé.* X = {1, 4, 7 porteur}, Y = {6 antidaté, 9, 12}. Le nœud 1 installe X à 7 et adopte Y à 12, avec 2 déconnexions.
- *Contraste STOP.* Même forme, sans bloc commun dans la fenêtre. X compte 5 blocs honnêtes après la fourche, et Y est plus longue. La déconnexion vaudrait 5 > 4 et l'ancre serait retirée : le résultat est `STOP_DEEP`, sans adoption.

## 5. Question clé : violation ou STOP ?

**Dans le miroir : violation, pas STOP.** L'arithmétique des témoins le montre. Si Y passe sous le seuil, alors c + a₁ < b, où a₁ ≥ 1 compte le porteur privé. Si X passe honnêtement, alors hon(f, porteur X] ≥ b − c. Pour que Y gagne, il faut adv(f,t] ≥ hon(f,t]. La déconnexion d'un synchronisé vaut hon(f,t]. Son minimum, b − c (plus 1 si le nœud a vu une signature de E), est ≤ b dès que c ≥ 1 : **aucun garde-fou ne l'empêche d'être inférieure à maxreorg**. maxreorg n'arrête que les configurations où l'honnête a produit plus de b blocs depuis la fourche, ce que montre le run de contraste.

**Transposition aux paramètres réels** (espérances, hors TLA+, hypothèses d'Opus : f − cut ≲ b/h, b = 2 880). La déconnexion minimale d'un synchronisé vaut ≈ h·(t − cut) − 2 880. Le STOP est garanti si et seulement si elle dépasse 2 880, soit h > 5 760/(t − cut).

| h (β ; d) | installation à cut + 13 200 (plancher MTP) | porteur honnête réaliste, ≈ cut + 18 000 | signature de E, ≥ cut + 21 600 |
|---|---:|---:|---:|
| 0,30 (0,25 ; 0,4) | 1 080 : **adoption** | 2 520 : **adoption** | 3 600 : STOP |
| 0,32 (0,20 ; 0,4) | 1 344 : **adoption** | 2 880 : **adoption (limite)** | 4 032 : STOP |
| 0,49 (0,30 ; 0,7) | 3 588 : STOP | 5 940 : STOP | 7 704 : STOP |
| 0,56 (0,20 ; 0,7) | 4 512 : STOP | 7 200 : STOP | 9 216 : STOP |

On en tire trois conclusions.

1. **Engagements d'époque e** (signatures ou adoptions de blocs de e, donc t ≥ start(e)). Pour un nœud synchronisé, maxreorg transforme le pivot profond en STOP dès que h > 0,267. C'est le cas de tous les profils candidats (d ≥ 0,4). Les témoins AFTER_SIG et restreint, qui aboutissent à une adoption, exigent un h plus faible que 0,267, ce que la réduction permet.
2. **Installations** (D3 = oui, lecture littérale du §5.7.2). Entre cut + 13 200 et start(e), le pivot profond peut aboutir à **une adoption sans STOP** si h < 0,436, donc à (0,20 ; 0,4) ou (0,25 ; 0,4). C'est une violation de CP_reg que maxreorg ne capte pas. Sa probabilité reste celle de la course privée à calendrier fixe sur au moins K_piv créneaux : ε_fix(K_piv), de l'ordre de 2·10⁻¹⁸ à (0,20 ; 0,4) selon Opus. Ce chiffre n'est pas vérifié ici. Opérationnellement, il s'agit d'un remplacement de R_e avant start(e), que le §5.2 autorise (« une adoption autorisée peut remplacer support et registre de la même époque »). Il ne devient une divergence d'engagements de e que si d'autres honnêtes ne reçoivent pas Y avant start(e), ce qui est une question de Δ.
3. **À (≤ 0,30 ; ≥ 0,7)**, le pivot profond se réduit à un STOP pour tout nœud synchronisé. Il reste pour les nœuds non protégés (nouveaux ou de retour), c'est-à-dire la classe D1, déjà hors du champ de cette qualification.

## 6. Ce que le miroir ne capture pas

- **Aucune probabilité.** La loterie jouet est périodique (β = 1/3 avant l'ajout) et la disponibilité honnête est arbitraire : les honnêtes peuvent sauter leurs créneaux, ce que le modèle ne force jamais. Les témoins établissent une **atteignabilité**, pas une fréquence. La prise d'avantage de Y est l'événement rare mesuré par ε_fix(K_piv).
- **Pas de Δ.** La livraison est sélective et arbitraire (`Reveal` par nœud). La convergence des autres synchronisés vers Y, décisive pour la conclusion 2 du §5, n'est pas modélisée.
- **Tie jouet** ordonné par (époque, racine, créneau, producteur) au lieu d'un hachage. Seul le replay SYNC en dépend. Au §9.3, l'adversaire peut de toute façon choisir les égalités qu'il exploite.
- **Autres simplifications** : une seule époque cible et une seule opération ADD ; pas de H1, de preuves d'équivoque ou de frein de densité ; ancre en Nbound seul. Bbound ne pourrait qu'abaisser l'ancre, donc ce choix est conservateur pour la protection. Les constantes sont réduites, et b est petit relativement aux fenêtres.
- **Le §5 est arithmétique**, en espérance, sans queue de fluctuation. Ce n'est pas un résultat du model checker.

## 7. Questions séparées (aucune règle proposée)

1. D3 : les installations comptent-elles dans CP_reg ? Si oui, le pivot profond sans STOP existe, en théorie, dans les profils d = 0,4. Si non, maxreorg le ferme pour les synchronisés dans tout le domaine d ≥ 0,4.
2. Faut-il une hypothèse Δ dans H_N pour affirmer qu'un remplacement de R_e antérieur à start(e) converge avant le premier engagement de e ?
3. La fenêtre [MatMin, BtcMat), ouverte par la marge MTP de 7 200 s, est ce qui permet à la branche privée de fermer avant tout porteur honnête. Son rôle dans K_piv mérite une question explicite au propriétaire. Ce n'est pas une proposition de règle.
