# Première divergence du registre — Codex

30 septembre 2026. Exécution du [mandat](../MANDAT-LEMME-PREMIERE-DIVERGENCE.md), sous l’autorité de DIRECTION.md. Sources : [N-SPEC v0.6](../N-SPEC-v0.6.md), analyses [Codex](CP-REG-codex.md) et [Opus](CP-REG-opus.md), modèles livrés. Aucune modification normative, aucune opération git.

## 1. Verdict

**L1 est démontrable, avec un argument de fermeture absent de sa justification proposée. L2 est vrai pour les fonctions de tirage communes, conditionnellement à un même contexte Bitcoin. P ne constitue pas une réduction probabiliste démontrée.** Sa disjonction structurelle est correcte ; l’identification de sa voie (i) avec une violation de préfixe commun à calendrier fixé ne l’est pas automatiquement.

Une branche privée valide peut être moins longue que la branche honnête lorsqu’elle acquiert un registre distinct. Sa conservation n’est pas une violation de CP entre engagements honnêtes. Ses productions ultérieures utilisent déjà un autre calendrier. Il faut démontrer que cette branche ne pourra jamais obtenir un engagement honnête sans un événement rare **antérieur** couvert par le théorème invoqué. L1 et L2 ne démontrent pas cette propriété.

Les recherches ci-dessous n’établissent aucun contre-exemple à la disjonction brute « préfixe ancien différent ou pivot ». Elles établissent des désaccords par signatures et isolent la lacune de la réduction. **ε_CP de N reste UNKNOWN ; le gel n’est pas débloqué.** Ce verdict ne signifie pas que le risque réel vaut 1, ni qu’aucune réduction plus forte n’existe.

## 2. Contexte et preuve de L1

Fixons le même contexte X : règles, origine, Bitcoin vérifié et faits de graine communs. Sans cela, deux registres identiques peuvent donner des graines différentes (§5.4) ; un énoncé inconditionnel sur toutes les histoires valides serait faux. Les réservations honnêtes et la validité historique sont celles des §§7–9. On ne suppose aucun accord futur des supports.

Soit P le plus long préfixe commun de deux chaînes non comparables par inclusion. Leurs premiers successeurs différents ne portent pas nécessairement le même créneau. Notons s le plus petit de ces deux créneaux, j son époque. « Sur les deux branches au créneau s » signifie alors **le registre de validation d’une candidate à s sur P** ; s’il n’existe aucun bloc sur l’autre branche à s, il ne faut pas en inventer un.

Le support brut de j précède `snapshot_cut(j)<start(j)≤s` (§5.2). Il appartient donc à P. Mais cela ne suffit pas : le support effectif dépend aussi de la fermeture A. Pour chaque époque k≤j, procédons par induction :

* Si son premier porteur de maturité est dans P, la fermeture et le compte sont déjà identiques. Toute extension les conserve.
* Sinon, une candidate valide de l’époque j doit engager sa propre maturité et les maturités antérieures pertinentes. Elle ferme les fenêtres encore ouvertes. Le compte est celui des blocs de P dans la fenêtre, augmenté d’un bloc lorsque la candidate appartient à cette fenêtre. Il ne dépend ni de sa signature ni de son corps. Les deux candidates sur P donnent le même compte et le même support brut.
* Le seuil atteint sélectionne ce support brut ; le seuil manqué sélectionne le support précédent, identique par induction.

Le §5.2 prescrit précisément cet ordre : parent, créneau, repère, compte, registre, puis loterie et signature. Aucun bloc de j ne peut précéder son propre porteur de maturité. Cette règle exclut l’objection selon laquelle le premier bloc divergent pourrait ajouter une opération à son propre registre.

Les transitions de contrôle rejouées depuis les supports sont déterministes (§§5.7, 5.9, 6, 23.5). On obtient le même registre et le même contrôle pour la candidate à s. À faits Bitcoin communs, §5.4 donne la même graine ; §7.1 donne le même producteur. Deux premiers blocs divergents **dans la même époque**, éventuellement à des créneaux différents, utilisent aussi le même registre : chacun est le premier successeur de P, donc ajoute le même nombre de blocs aux fenêtres encore ouvertes.

Si les deux premiers successeurs appartiennent à des époques différentes, on ne prétend pas que leurs registres d’époques différentes sont égaux. L1 doit conserver son interprétation au même créneau. Sa justification « D dépend seulement du préfixe avant la coupure » est donc **fausse littéralement**, même si le résultat local est sauvable par l’argument précédent.

## 3. L2 et cas limites

Soit e la première époque dont les supports complets D diffèrent, une fois leurs fenêtres déterminées sur les histoires examinées. Pour k<e, D_k est identique par définition. C6, sous le même X, donne contrôle, registre, graine et fonction de tirage identiques (§5.7.1, §23.4). Cela prouve l’égalité des fonctions de tirage sur les créneaux de `[s,start(e))`. La réciproque est fausse : des D différents peuvent produire le même registre, voire le même contrôle (§5.3). La première divergence de D ne signifie donc pas nécessairement première divergence effective du calendrier.

Cette égalité ne dit pas que tous les créneaux sont effectivement attribués : §5.5 distingue un tirage calculable d’une attribution attestée par la maturité dans la branche. Un créneau vide avant le premier porteur n’est pas attribué rétroactivement. Le miroir Fast2 réduit la maturité au début d’époque et ne prouve pas cette distinction complète.

**Époques vides consécutives.** Le §5.2 impose de traiter les époques sautées ; le bloc de reprise peut fermer plusieurs fenêtres. Si A_k=A_(k−1), le §5.9 s’applique. L’induction porte sur les supports et les transitions prescrites, pas sur la présence d’un bloc à chaque frontière. Une époque sans engagement honnête n’offre aucune confirmation supplémentaire.

**Porteur tardif.** La fermeture est propre à la branche, non à l’heure mondiale de connaissance du Bitcoin. Le §8.4 contraint le repère honnête, et §5.2 compte le premier porteur une seule fois. Un porteur tardif peut allonger la fenêtre ; il n’autorise pas à la remplacer par une durée moyenne Bitcoin. Inversement, une fermeture pour e peut avoir eu lieu avant `start(e)` dans un bloc d’une époque précédente : la garde et la maturité ne s’ajoutent donc pas mécaniquement à `start(e)−snapshot_cut(e)`.

**Absence et retour.** Le §8.6 exige reconstruction puis sélection. Il ne rend pas commun le passé vu pendant l’absence. §§5.7.3 et 9 imposent rang, ancre et veto, sans verrou de registre. L1/L2 restent des propriétés de dérivation ; ils ne donnent aucune convergence préalable au revenant.

**Signatures.** Un engagement est déjà créé par une signature, sans adoption ultérieure (§§5.7.2, 23.2). Deux nœuds peuvent signer dans la même époque sous deux registres distincts sans qu’aucun ne réorganise alors sa propre chaîne. La réservation `(IID,slot)` n’empêche pas deux IID différents de signer.

**Branche privée multi-époques.** L’adversaire peut retarder la première divergence effective de D : absence d’opération déterminante, héritages successifs, fenêtres trop peu remplies. On prend e réellement atteint, jamais la première époque où une divergence était seulement possible. Cela prolonge l’intervalle commun de cette paire, mais ne prouve pas sa compétitivité. Une autre paire de l’arbre adverse peut avoir divergé auparavant ; un raisonnement global doit couvrir tout cet arbre.

## 4. P : ce qui se prouve et ce qui manque

À la première époque e de désaccord, les supports antérieurs sont égaux. Si les préfixes bruts diffèrent, on est dans la voie structurelle (i). Sinon, deux décisions identiques du seuil donneraient soit le même brut, soit le même support hérité. Le désaccord exige donc des côtés différents du seuil : voie (ii). Cette preuve est déterministe et exhaustive, à fenêtres définies.

Mais « il existe encore une branche valide avec un autre ancien préfixe » n’est pas « deux branches sont viables pour le théorème de CP ». Un adversaire peut conserver indéfiniment une branche perdante. La chaîne honnête peut croître, sans retrait ni insertion d’ancien bloc dans aucun engagement honnête. Au passage à e, la branche privée change son registre, puis son calendrier. La continuation n’est plus une exécution du modèle à calendrier commun.

La première divergence de registre **parmi toutes les branches valides** peut ainsi précéder le premier désaccord honnête. S’arrêter au premier désaccord honnête ne garantit pas un calendrier commun jusque-là ; s’arrêter au premier désaccord privé ne garantit pas un échec de CP jusque-là. C’est le passage manquant dans P.

Le score puis le départage public (§§9.3–9.4) comparent les candidates disponibles au nœud. Ils ne détruisent aucune histoire valide cachée, et ne constituent pas une preuve probabiliste d’impossibilité de retour. Un STOP après révélation ne retire pas une signature déjà exportée.

La borne ε_CP-fixe(K) doit donc porter sur un événement précisément défini : préfixes engagés ou fourches viables, unités temporelles, avance privée et horizon. On ne peut lui substituer la simple persistance d’une histoire adverse. De même, choisir arbitrairement `K≥start(e)−cut(e)` ne renforce pas la protection : une borne décroissante exige **au moins K créneaux effectivement couverts avant l’événement pertinent**. Le début nominal de e, sa première fermeture et son premier engagement honnête sont trois instants distincts.

### Recherche de contre-exemple

Les replays existants `MC_replay_audit_cp_L1` et `MC_replay_audit_min_k1_L1` atteignent deux signatures honnêtes avec D différent. `MC_replay_closure_checked_fixed_L1` atteint le pivot sur un même brut. Ils ne réfutent pas la disjonction structurelle ; ils réfutent toute tentative de remplacer les engagements par les seules réorganisations adoptées.

Le replay supplémentaire [MC_private_return_L1](../tla/modele-v0.6/MC_private_return_L1.tla) atteint `NoWitnessMissingBridge` après 15 états distincts (0,71 s). Il expose explicitement la lacune : à créneau 0, l’adversaire produit deux variantes ; l’honnête 1 prolonge seulement A aux créneaux 1 et 2 ; B reste privée à un bloc. Au début de l’époque 2, A a trois blocs, B un. Les deux bruts avant `cut(2)=1` diffèrent. Le seuil réduit b=1 est atteint des deux côtés : aucun pivot. Après retour et livraison sélective à l’honnête 2, les deux producteurs signent au créneau 4 sous leurs registres respectifs.

La trace finale donne `R_A=⟨3,1,1⟩`, `R_B=⟨2,2,1⟩` et des comptes A respectifs de 3 et 1. Les producteurs du créneau 4 sont respectivement 1 et 2. Tous les engagements antérieurs à cette époque restent sur A. B n’avait pas rejoint son score à la frontière ; ses tirages à partir du créneau 4 sont déjà différents. Ce témoin vise l’implication « désaccord futur ⇒ violation de CP déjà observée sous calendrier commun ». Il reste dans la voie **(i) au sens faible de branche conservée** ; le présenter comme un « autre » de la disjonction brute serait trompeur. Il n’est pas une attaque probabilistiquement qualifiée sous un domaine synchrone imposé après retour : les livraisons sélectives et l’absence doivent être confrontées à ce domaine.

## 5. Vérification TLA+ et limites

Les nouveaux modules [RegistryModelFast2_L1](../tla/modele-v0.6/RegistryModelFast2_L1.tla), [RegistryAudit_L1](../tla/modele-v0.6/RegistryAudit_L1.tla) et [RegistryCommitmentsChecked_L1](../tla/modele-v0.6/RegistryCommitmentsChecked_L1.tla) étendent les modèles livrés sans modifier leurs transitions. Les wrappers portent le suffixe `_L1`. Le journal d’audit ajouté conserve les chaînes et les engagements par signature, adoption ou installation.

`FirstBlockCommon` compare les registres de candidates au premier créneau divergent ; `CommonInterval` compare les fonctions avant e ; `Class` distingue `i_raw`, `ii_pivot`, `other`. **`i_raw` n’est pas un certificat de violation de CP-fixe. Les configurations ciblent les nouveaux invariants et ne reconduisent pas l’ancien `RegistryImmutable` : un PASS avec A désactivée ne réhabilite donc pas cette variante.** `NoOtherStructural` teste seulement la partition déterministe. Dans CommitmentsChecked, les histoires sont préconstruites : aucune preuve de leur production n’est ajoutée. Fast2 utilise une loterie jouet, une fermeture simplifiée et des livraisons sans borne Δ ; il ne qualifie ni Bitcoin ni un risque numérique.

Les fichiers détaillés et les traces sont dans [lemme-L1](../tla/modele-v0.6/lemme-L1/). Le lanceur livré `run.sh`/`run.py` est utilisé sans modification : un TLC, quatre workers, 3 Gio, interruption à environ 569 secondes. Le premier log partiel de `MC_fast_off_00_L1`, interrompu avec la session, est archivé séparément **INCOMPLET**. Un replay terminé vérifie son chemin ; il n’explore pas toutes les exécutions du protocole. Un piège `NoWitness…` violé est un témoin attendu, jamais un PASS. La première tentative du replay supplémentaire a échoué à l’analyse sémantique (portée d’une variable du moniteur) ; elle est archivée INCOMPLET, puis corrigée et relancée.

| Sonde | Statut | États distincts | Durée (s) |
|---|---|---:|---:|
| `MC_replay_general_k1_L1` | PASS | 13 | 0.75 |
| `MC_replay_general_k2_L1` | PASS | 14 | 0.65 |
| `MC_replay_ruleA_advance_L1` | PASS | 18 | 0.65 |
| `MC_replay_audit_cp_L1` | TÉMOIN | 12 | 0.64 |
| `MC_replay_audit_min_k1_L1` | TÉMOIN | 11 | 0.62 |
| `MC_replay_closure_checked_fixed_L1` | TÉMOIN | 3 | 0.56 |
| `MC_registry_commits_C6_checked_L1` | PASS | 43264 | 1.18 |
| `MC_fast_off_00_L1` | PASS | 402099 | 358.18 |
| `MC_fast_on_00_L1` | PASS | 280913 | 348.32 |
| `MC_c6_k1_00_L1` | PASS | 134506 | 131.59 |
| `MC_general_a_k1_c6_L1` | INCOMPLET | 693034 | 569.23 |
| `MC_private_return_L1` | TÉMOIN | 15 | 0.71 |

Les PASS des replays sont limités au chemin fixé. Les explorations interrompues restent INCOMPLET, indépendamment des invariants non violés jusque-là. Pour INCOMPLET, les compteurs proviennent du dernier relevé TLC disponible. La première tentative interrompue est conservée en plus de ce tableau.

## 6. Domaine H_N et composition admissible

La composition souhaitée serait valide si l’on démontrait, dans un domaine H fixé,

`Bad_reg ⊆ Bad_CP_fixe ∪ Bad_pivot`.

Alors, sans indépendance : `Pr_H[Bad_reg] ≤ min(1, ε_CP_fixe + ε_pivot)`. Pour un horizon comportant plusieurs cibles, sommer des bornes couvrant les époques, départs et choix de graines pertinents, ou employer directement une borne globale. Les hypothèses Bitcoin, réseau, horloge, origine et clés doivent être conditionnées explicitement ou ajouter leurs risques de défaillance.

Ici l’inclusion probabiliste manque. Une écriture honnête conserve un événement résiduel U : désaccord obtenu après divergence privée de calendrier sans témoin déjà couvert par les deux termes. On a seulement

`Pr_H[Bad_reg] ≤ min(1, ε_CP_fixe + ε_pivot + ε_U)`.

**ε_U est UNKNOWN.** Il ne s’agit pas d’ajouter une mécanique : cette notation rend visible l’obligation restante. Le grinding post-divergence privée peut contribuer à U avant le premier désaccord honnête. L’exclure au motif qu’il est « post-divergence » confond deux événements différents. Même avant cette divergence, un registre commun évolutif impose une loi conditionnelle des calendriers successifs ; l’égalité entre branches ne prouve pas cette loi.

Pour la densité, notons d la disponibilité du poids honnête, h=(1−β)d et g le taux de croissance garanti dans le modèle retenu. La zone moyenne `gW<b≤(g+β)W` ne définit pas une exclusion certaine dans un modèle aléatoire. Pour W=14 400 et b=2 880, b/W=0,20. À délai nul et β=0,20 : d=0,20 donne h=0,16, donc la zone pilotable ; d=0,40 donne h=0,32 ; d=0,70 donne h=0,56. Les deux derniers profils sont au-dessus de la zone **en moyenne**, avec une marge à convertir en borne de queue et à composer sur l’horizon.

Ces calculs ne garantissent pas hW blocs sur toute branche privée : une croissance honnête publique n’impose pas leur inclusion dans une histoire cachée. La robustesse de toutes les fermetures pertinentes exige encore un argument de préfixe/barrière ou de compétitivité. Délai, DoS ciblé, β dynamique, maturité et fenêtre effective changent également la condition.

Enfin, **aucun d_min=0,40 ou 0,70 n’est adopté par N-SPEC §17 ou §23.4**. Opus §6 propose H_N-4 et une condition supplémentaire H_N-5 ; ce sont des candidats, et les couples numériques sont soumis au propriétaire. On ne peut donc déclarer la zone dangereuse « déjà hors domaine par construction ». Même adopter d_min ne suffirait pas à transformer une marge moyenne en impossibilité déterministe du pivot.

## 7. Questions au propriétaire, sans changement de règles

1. Quel domaine quantitatif publier : β maximal dynamique, disponibilité minimale sous attaque, délai et horloges, horizon, Bitcoin et conditions de retour ? Aucun de ces choix n’est implicitement adopté ici.
2. Faut-il poursuivre la preuve manquante pour les branches privées non compétitives qui changent de calendrier avant tout engagement honnête ? C’est une obligation d’analyse de la machine existante, pas une proposition de verrou, vote ou finalité locale.

L1/L2 clarifient la première divergence ; ils ne ferment pas à eux seuls l’objection sur le registre variable.
