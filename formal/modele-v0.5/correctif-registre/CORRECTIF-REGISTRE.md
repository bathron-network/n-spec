# Correctif de garantie — registre d’époque de N

30 septembre 2026. Exécution de `MANDAT-CORRECTIF.md`. Références locales : `N-SPEC-v0.5.md`, `RAPPORT-TLA-N.md`, `NModel.tla`. Proposition v0.6 dans `NModel_v06.tla` ; originaux conservés.

**Décision : corriger la propriété 6, pas réintroduire une finalité locale du registre.** La v0.5 autorise explicitement le changement de registre lors d’une réorganisation admissible (§5.7.3). L’immutabilité absolue du mandat initial contredit ce choix. Le contre-exemple est réel, mais ce n’est pas une violation des règles de la SPEC. Il expose une obligation de sûreté encore non démontrée : le préfixe commun temporel des supports. La recommandation ci-dessous clarifie cette limite et interdit de qualifier N sur la seule base du lemme conditionnel. **Elle ne rend pas impossibles les changements de registre observés.**

## 1. Qualification et propriété exacte

| Question | Réponse |
|---|---|
| Erreur du modèle ? | Non pour le phénomène identifié : les anciennes opérations peuvent appartenir au suffixe encore réorganisable. Le modèle reste une abstraction finie. |
| Bug d’implémentation par rapport à v0.5 ? | Non : §5.7.3 exige le remplacement atomique des états du suffixe adopté et refuse le registre mémorisé comme seconde ancre. |
| Défaut réel si l’exigence produit est « jamais deux registres par époque » ? | Oui : cette exigence n’est pas satisfaite. Il faut changer le protocole et accepter un coût d’arrêt/finalité, ou renoncer à cette exigence absolue. |
| Défaut des unités ? | Aucune conversion déterministe ne relie âge en créneaux et profondeur en blocs après des créneaux vides. `K_reg > maxreorg`, comparant ces deux nombres sans unités, ne résout rien. |
| Le contre-exemple réfute-t-il un théorème probabiliste de N ? | Aucun théorème avec domaine et probabilité n’est fourni. Il réfute l’invariant universel. On ne peut ni lui attribuer une probabilité, ni déclarer le domaine opérationnel sûr. |
| Suffit-il de dire « partition » ? | Non : la partition du replay se termine ; la deuxième adoption arrive après réunion. Une hypothèse de réseau doit couvrir l’histoire pertinente, pas uniquement l’instant final. |

Le replay `MC_replay_spec_adopt` (avec `MaxReorg=1`, contrairement à la sonde générale à 4) comporte 13 états : production sur deux branches depuis genesis, traversée de créneaux vides, retour du nœud 2, première adoption en époque 2, réunion, puis seconde adoption en époque 2. Le retrait est permis par les protections en blocs. Les supports et registres diffèrent ; origine et faits Bitcoin restent fixes. Le nœud 2 passe de `(2,1,1)` sur le bloc du créneau 4 à `(3,1,1)` sur la branche des créneaux 0 et 3 ; le second registre courant est installé même si cette branche n’a pas encore de bloc d’époque 2. H1 et les deux mutations sont désactivés. Le replay court `MC_replay_spec` couvre aussi l’engagement par signature.

### Formulation à retenir

Fixer un contexte externe `X = (rules_id, origine de confiance, faits Bitcoin consommés pertinents)`. **Ne pas inclure le registre ou la graine complète dans X** : la graine engage déjà le registre. RECOVERY explicitement accepté ouvre un nouveau contexte ; BOOTSTRAP ne le fait pas.

Soit `P_j(C)` le préfixe complet de C jusqu’à `A_j(C)`, genesis inclus, et `D_e(C) = (P_0(C), …, P_e(C))`. La comparaison couvre les contenus de contrôle et l’ordre, pas seulement un nombre de blocs ou les poids. Dans le modèle, `Supports(C,e)` contient directement ces préfixes ; l’identité d’un support réel n’est suffisante qu’avec engagement cryptographique de son ascendance.

Soit `u` un engagement honnête (adoption d’un bloc utilisant e, ou signature en e), et `v` un autre engagement ou une installation du registre courant par adoption, éventuellement chez un autre nœud :

```text
C6 — Stabilité conditionnelle :
  epoch(u) = epoch(v) = e ∧ X(u) = X(v) ∧ D_e(C_u) = D_e(C_v)
  ⇒ R(u) = R(v) ∧ Control(u) = Control(v) ∧ Calendar(u) = Calendar(v).
```

La conclusion sur le calendrier suppose les mêmes entrées Bitcoin, et non l’égalité supposée de la graine finale. C6 est un lemme de dérivation déterministe, **pas une preuve de consensus**. Pour obtenir l’ancienne propriété avec une borne de risque, il faut séparément :

```text
CP_reg(e, X) : tous les engagements honnêtes et installations de registre
              par adoption pertinents de (e,X) ont le même D_e.
H_N ⇒ Pr[∃ e,X dans l’horizon qualifié : ¬CP_reg(e,X)] ≤ ε_CP.
C6 ∧ CP_reg ⇒ immutabilité et accord des registres concernés.
```

`H_N` doit fixer le réseau et ses délais sur les fenêtres pertinentes, les horloges et leur désynchronisation admissible, la disponibilité honnête, les poids adverses dynamiques, les corruptions, la source/garde Bitcoin, les possibilités de rétention et de grinding, ainsi que l’horizon. `ε_CP` doit porter sur l’événement global annoncé, ou être composé explicitement depuis les bornes par époque. Aucune valeur numérique n’est établie ici. Un préfixe commun à un instant ne garantit pas sa conservation aux engagements ultérieurs.

La justification de C6 est une induction sur les transitions d’époque : bootstrap identique ; mêmes préfixes autorisés, donc mêmes opérations nouvellement consommées dans le même ordre ; même état de contrôle précédent, donc même état suivant et même registre ; enfin même époque et mêmes faits Bitcoin, donc même graine et calendrier. Elle dépend du déterminisme complet de la machine de contrôle, pas seulement de la somme des poids. Ce raisonnement ne prouve pas que deux histoires réelles possèdent ces mêmes préfixes.

Inclure maintenant `D_e` dans **la prémisse de C6**, clairement renommée, est légitime. Le faire silencieusement dans « même contexte » de l’ancienne propriété 6 pour annoncer sa réussite serait trompeur. L’ancien moniteur `RegistryImmutable` est donc conservé et ses contre-exemples sont rejoués.

## 2. Comparaison aux protocoles publiés

Les références ci-dessous sont des sources primaires ; leurs hypothèses et paramètres ne sont pas transférés à N.

| Protocole | Distribution retardée, préfixe et temps | Conséquence pour N |
|---|---|---|
| Ouroboros Praos | La distribution de l’époque j est tirée d’un état ancien de la chaîne candidate (figure 6 : borne `(j−2)R`). Le préfixe commun retire k **blocs** ; croissance et qualité de chaîne font l’objet de résultats distincts sur des intervalles de créneaux. Les garanties sont probabilistes, sous contraintes de poids honnête, délai et fréquence de production. | Le retard du cliché ne constitue pas sa finalité. Les créneaux vides sont pris en compte par l’analyse, pas par une conversion « un créneau = un bloc ». N doit analyser son propre calendrier public et sa source Bitcoin. [Praos, §§2.3, 4.4, 5 et figure 6](https://iacr.org/archive/eurocrypt2018/10822378/10822378.pdf). |
| Ouroboros Genesis | Conserve une organisation par époques et poids historiques, mais modifie la sélection de chaîne pour permettre une synchronisation depuis genesis sous hypothèses de disponibilité. Pour des divergences anciennes, la comparaison porte sur le nombre de blocs dans une portion temporelle définie après divergence ; ce n’est pas seulement « la plus longue chaîne reçue ». | La densité intervient dans une règle précise avec preuve, pas comme certificat local de sûreté. Copier cette règle changerait la fork-choice de N et demanderait une nouvelle analyse. [Genesis, règle `maxvalid-bg`](https://www.pure.ed.ac.uk/ws/files/76645278/Ouroboros_Genesis.pdf). |
| Sleepy | Le modèle distingue joueurs éveillés et endormis ; la sûreté et la vivacité reposent notamment sur une majorité honnête parmi les participants en ligne, une infrastructure de clés, des horloges et délais bornés. La cohérence retire un suffixe de T blocs et couvre aussi le futur du même nœud ; la croissance relie séparément blocs et pas de temps (§3.2). Ce n’est pas à lui seul un mécanisme de distribution de stake évolutive retardée. | Tolérer des absences ne signifie pas garantir la sûreté sous toute partition et toute disponibilité. Le temps écoulé sans production n’est pas une preuve de consolidation. [Pass–Shi, modèle et théorèmes 1–2](https://eprint.iacr.org/2016/918.pdf). |
| Snow White | Dans la version consultée, comité et nonce ont des reculs temporels distincts `2ω` et `ω`. La sécurité articule croissance, cohérence, restriction de réécriture en blocs et hypothèses de sommeil/corruption. La contrainte `ω ≥ 2κ/γ + Δ̃` relie explicitement recul temporel, croissance et sommeil léger. | Le chaînon manquant ne se remplace pas par un compteur local. La reprise après absence et la stabilité du comité se prouvent ensemble sous les hypothèses publiées. [Bentov–Pass–Shi, §§2.2 et 5, version ePrint consultée](https://iacr.steepath.eu/2016/919-SnowWhiteProvablySecureProofsofStake.pdf). |

**Déduction pour N :** un CP en blocs joint à une croissance suffisamment forte peut couvrir une borne temporelle ancienne. Sans hypothèse de croissance applicable sur l’intervalle, l’implication n’existe pas. Une densité élevée observée sur une branche ne prouve ni l’absence d’une autre branche, ni l’accord des supports. Les seuils client de §14 et le frein d’exclusion de §6.6 ne constituent pas une telle preuve.

## 3. Options normatives

Les trois changements de protocole ci-dessous sont comparés à l’option de clarification recommandée. Aucun n’est déclaré sûr sur la seule intuition.

| Option et règle envisagée | Accord / immutabilité | Époques vides, absence et vivacité | Grinding | Complexité et cohérence normative |
|---|---|---|---|---|
| **A — Double recul fixe, en blocs et créneaux.** Définir `B_e(C)=C restreinte aux slots < freeze_slot(e)`. Choisir le dernier bloc de slot `< cut(e)` ayant au moins k descendants dans `B_e(C)` ; à défaut hériter `A_(e−1)(C)`. | Dérivation reproductible ; réduit l’exposition d’un support peu profond. Ne garantit pas seule l’immutabilité : `B_e` peut être réorganisée, ou des blocs anciens livrés tardivement. Vérifier k descendants sur la pointe courante ferait aussi avancer le cliché dans la même époque par simple extension : à proscrire. | Produire reste possible avec registre hérité ; admissions/rotations/exclusions différées lorsque les blocs manquent. Rattrapage depuis la candidate complète, sans cliché local mémorisé. Ne pas imposer k nouveaux blocs avant de produire. | Réduit certaines variantes récentes, sans prouver `Q_reg=1`. L’adversaire peut retenir des descendants et influencer le franchissement du seuil. | Modifier §§5.2, 5.9, 6 et vecteurs. Compatible avec dérivation sans verrou (§5.7), mais ne relie pas automatiquement le support à l’ancre réellement persistée (§9.6). Aucun pouvoir nouveau pour H1 (§12). |
| **B — Héritage sous faible densité.** Pour une fenêtre historique fixe `W_e=[freeze_slot(e)−W,freeze_slot(e))`, calculer sur C la fraction de créneaux occupés ; sous un seuil d, poser `A_e=A_(e−1)` et reporter les opérations nouvelles. | Deux candidates peuvent être de part et d’autre du seuil : accord toujours conditionnel au préfixe. Le seuil n’est pas un mécanisme de finalité. | Époques entièrement vides : registre hérité, production ordinaire permise. Après absence, recalcul depuis la candidate. Risque de gel prolongé des admissions, même si la production continue. | Manipulation du seuil par publication/rétention ; peut conserver un ancien poids adverse ou offrir deux registres possibles. Aucune borne automatique. | Nouvelles constantes W,d et règles de bord ; §§5.2/5.9/6 modifiés. §5.7 compatible si calcul purement historique ; §9.6 inchangé ; densité de §12 ne devient pas vote ni sélection. Ne pas confondre cette règle avec le frein d’exclusion existant. |
| **C — STOP avant changement d’un registre engagé.** Comparer au journal des engagements d’époque avant adoption **et signature** ; si différence, STOP, réévaluation ou RECOVERY explicite. | Empêche localement le deuxième engagement, mais peut arrêter deux nœuds sur deux premiers registres différents. Ne prouve ni A3 ni A4. Un contrôle de la seule adoption manque le cas signature. | Époques vides sans conflit : reprise possible. Après partition/absence : désaccords superficiels deviennent des arrêts ; aucun retour garanti sans contexte historique fiable ou acceptation explicite. | Peut rendre un premier choix adverse persistant et faciliter le DoS. N’élimine pas le choix initial entre préfixes. | **Rejetée sous les contraintes du mandat.** La dérivation peut rester pure et la candidate historiquement valide, mais une racine mémorisée devient une contrainte d’adoption : c’est un verrou fonctionnel. Contredit §5.7.3 ; il faudrait modifier §§7,9,12 et la persistance. Nommer le mécanisme STOP ne change pas sa nature. |
| **D — Clarifier C6 et séparer la qualification CP (recommandée).** Garder les règles v0.5, préciser l’absence de finalité du registre et rendre A3/A4 et leur domaine explicitement bloquants pour une revendication de sûreté. | C6 exacte, testable ; immutabilité forte toujours fausse sans CP. Aucun gain de sûreté du protocole revendiqué. | Aucun nouveau blocage : héritage, rejeu et production après vide inchangés ; conflit profond toujours STOP et RECOVERY explicite si nécessaire. | Surface existante conservée et explicitement comptée ; `Q_reg=1` seulement sous préfixe fixé. | Modification de garanties et de tests, pas de fork-choice. Cohérente avec §§5.7,9.6,12 ; pas de verrou, pas de vote, N pur, A′ sans effet sur un synchronisé. |

Une variante de C qui relève une ancre au support au premier engagement ne fait pas disparaître le problème : elle ajoute une finalité locale anticipée, peut créer des ancres incompatibles et doit aussi traiter l’insertion de blocs anciens après un support genesis. Protéger le seul bloc support ne prouve pas que la partie temporelle située avant la coupure restera identique. Cette variante demande une spécification autonome ; elle n’est pas présentée comme un correctif déjà acquis.

**Choix : D.** A et B restent des pistes de réduction d’exposition, pas des solutions démontrées à l’invariant fort. C enfreint la contrainte sans verrou. Si l’immutabilité absolue reste un impératif produit, cette recommandation ne le satisfait pas : il faudra rouvrir explicitement les compromis de finalité et vivacité. Le présent mandat permet précisément de conclure que la propriété initiale est trop forte.

## 4. Patch normatif précis à intégrer

Ces textes constituent le patch proposé ; `N-SPEC-v0.5.md` n’est pas modifié. Les formules existantes de §5.2, la fork-choice et le format réseau restent inchangés. « v0.6 » désigne ici la proposition de clarification, pas une version publiée.

### §5.2 — Ajouter après « Chaque opération est consommée au plus une fois sur une branche »

> L’ancienneté en créneaux de `A_e(C)` ne lui confère aucune finalité locale. Une époque engagée par adoption ou signature ne fige ni son support ni son registre contre toute réorganisation admissible. En l’absence de préfixe commun, deux candidates historiquement valides peuvent déterminer des registres différents pour la même époque, et une adoption autorisée peut remplacer le registre courant. La limite de réorganisation en blocs du §9.6 ne DOIT PAS être interprétée comme une borne équivalente en créneaux.

### §5.7.2 — Ajouter après le paragraphe sur la probabilité d’échec

> La propriété de préfixe commun doit couvrir tous les événements d’engagement honnête concernés, y compris les signatures et toute installation de registre par les adoptions successives d’une même époque, et les préfixes nécessaires aux états de contrôle antérieurs. Son domaine qualifié DOIT préciser réseau, horloges, disponibilité, adversaire, évolution des poids, faits Bitcoin, horizon et borne d’échec. Une garantie déterministe de dérivation à préfixe fixé ne constitue pas une preuve de cette propriété. Tant que cette qualification n’est pas établie, N NE DOIT PAS être présenté comme assurant l’immutabilité globale des registres d’époque.

### §5.7.3 — Ajouter après « Un registre mémorisé ne devient jamais une seconde ancre »

> Un engagement de registre passé n’est ni une condition supplémentaire de validité historique, ni un veto supplémentaire d’adoption ou de signature. Les réservations anti-double-signature du §7.4 restent obligatoires. Un changement de registre issu d’une adoption autorisée NE DOIT PAS être dissimulé dans les diagnostics ; son époque et les identifiants des anciens et nouveaux supports doivent être exposés. Ces diagnostics ne participent pas à la sélection.

### §5.8 — Ajouter après la définition conditionnelle de `Q_reg=1`

> Cette égalité ne borne pas le nombre de préfixes que l’adversaire peut rendre adoptables. Toute analyse d’exposition DOIT traiter cette possibilité séparément ; elle NE DOIT PAS substituer une probabilité de course à registre fixe à une borne de préfixe commun pour un registre variable.

### §5.9 — Ajouter à la fin

> La possibilité de produire après des époques vides est une propriété de vivacité locale. Elle n’implique pas que le support hérité ou devenu ancien soit commun aux autres histoires honnêtes. Le passage du temps sans bloc NE DOIT PAS être compté comme des confirmations en blocs.

### §9.6 — Ajouter à la fin

> La protection de l’ancre ne garantit l’identité d’un préfixe temporel de registre que lorsque cette identité découle effectivement du préfixe protégé et des règles de validation. L’âge en créneaux du dernier bloc du support, à lui seul, ne permet pas cette déduction. Aucun avancement d’ancre ni nouvel arrêt ne résulte de la seule mémorisation d’une racine de registre d’époque.

### §12.1 — Ajouter à la fin

> Une preuve H1 NE DOIT PAS certifier un registre d’époque, rendre commun son support, ni départager positivement deux registres. Les décisions restent celles du §9, sous les seuls vetos définis ici. BOOTSTRAP conserve son pouvoir nul sur un nœud ayant une origine locale ; RECOVERY demeure une acceptation explicite d’un nouveau contexte, sans automatisme dû au changement de registre.

### §23.4 — Ajouter A5 après A4

> **A5 — Stabilité conditionnelle du registre d’époque.** Pour un engagement honnête et un engagement ou une installation ultérieure de registre par adoption, de même époque, mêmes règles, même origine de confiance et mêmes faits Bitcoin pertinents, l’identité des préfixes complets nécessaires à tous les supports de contrôle implique l’identité du registre, de l’état de contrôle et du calendrier. Cette propriété est distincte d’A3. Une campagne conforme DOIT tester A5 sans filtrer les exécutions qui violent A3, conserver une sonde de l’immutabilité inconditionnelle et publier ses contre-exemples. Un PASS d’A5 NE DOIT PAS être rapporté comme un PASS d’A3 ou d’A4.

### §19.4 et §23.10 — Ajouter la même condition de qualification

> La qualification d’une garantie d’immutabilité du registre requiert une analyse du préfixe commun temporel propre à N et de la compatibilité des ancres, avec hypothèses, unités, horizon et probabilité explicites. Un résultat conditionnel de dérivation et des explorations finies ne suffisent pas. Un scénario interrompu ou limité à un replay NE DOIT PAS être déclaré exploration exhaustive du protocole.

Pour le mandat de vérification ultérieur, remplacer son obligation 6 par C6 ci-dessus **et conserver CP_reg comme obligation de sûreté séparée**. Ne pas renommer l’ancien invariant en prétendant en préserver le sens.

## 5. Implémentation et portée des vérifications

`NModel_v06.tla` est une copie de `NModel.tla`. Seuls le nom du module, les commentaires et l’instrumentation d’audit changent. Les opérateurs de support, registre, classement, adoption admissible, H1, ancre, production et RECOVERY conservent leurs règles. `history.supports` mémorise les entrées historiques du dernier engagement de l’époque, à seule fin de comparaison ; aucun garde de protocole ne le lit. `audit.conditional` accumule les violations de `RegistryStableOnCommonPrefix`. `audit.immutable` et `RegistryImmutable` restent présents.

Le moniteur compare le dernier engagement à l’adoption suivante (même si celle-ci n’engage pas encore un bloc de l’époque), et à toute nouvelle signature honnête. Il est donc conservateur sur les adoptions. Comme le moniteur original, il oublie l’époque passée lorsque l’horloge avance, et réinitialise l’historique lors de RECOVERY. Il vérifie des comparaisons successives dans l’époque courante ; la formulation générale C6 pour des paires arbitraires découle du déterminisme des entrées, et n’est pas revendiquée comme un journal exhaustif de toutes les paires passées. Les faits Bitcoin restent fixes dans une exécution. Rotation, exclusion et état de contrôle complet restent abstraits par des ADD et vecteurs de poids.

Le modèle vérifie la partie dérivation/engagement de la recommandation. Les obligations éditoriales de qualification et l’exposition des diagnostics dans une API réelle ne sont pas une implémentation client fournie ici. Aucune hypothèse CP, `CONSTRAINT`, limitation de profondeur BFS ou filtre de traces n’est ajouté pour faire passer le moniteur. La suppression des champs d’audit supplémentaires retrouve les règles v0.5 ; ce n’est pas une réparation cachée de la sélection.

Chaque module de campagne porte le suffixe `_v06` et étend la copie. Les `.cfg` reprennent les constantes originales ; seul `RegistryImmutable` est remplacé par `RegistryStableOnCommonPrefix` dans les campagnes conditionnelles. Les variantes `_strong_v06` gardent exactement l’ancienne obligation. Les fichiers originaux et anciens logs sont conservés.

`MC_safe_v06` contrôle également typage, métadonnées, H1, accord conditionnel, déterminisme, recovery, activabilité de production, BOOTSTRAP, ancre et acceptation explicite. `MC_spec_registryreorg_v06` ne contrôle que le typage et C6, comme la portée ciblée de son original. `MC_live_v06` contrôle les deux propriétés temporelles originales sur le suffixe de reconnexion, sans production et sans équité de RECOVERY. Les deux témoins vides sont des recherches d’existence de production honnête ; ils ne prouvent pas la vivacité universelle.

Les bornes restent celles des campagnes originales : deux honnêtes, un producteur adverse, deux branches, deux créneaux par époque et `KReg=1`. Les lots de graines ne sont pas interprétés comme une distribution probabiliste.

| Campagne | Époques | Dernier créneau inclus | `ForkSlot` | `MaxReorg` |
|---|---:|---:|---:|---:|
| `MC_safe` | 3 | 4 | 1 | 1 |
| `MC_spec_registryreorg`, ses quatre partitions et sa sonde forte | 3 | 5 | 0 | 4 |
| `MC_replay_spec_adopt`, conditionnel et fort | 3 | 4 | 0 | 1 |
| `MC_replay_spec`, fort | 3 | 5 | 0 | 4 |
| Deux mutations | 3 | 5 | 1 | 1 |
| Témoin d’une époque vide | 3 | 5 | 1 | 1 |
| Témoin de deux époques vides | 3 | 4 | 0 | 1 |
| `MC_live` | 2 | 3 | 1 | 1 |

## 6. Résultats exécutés

| Campagne | Résultat | Générés | Distincts | File | Profondeur | Secondes / code |
|---|---|---:|---:|---:|---:|---|
| `MC_replay_spec_adopt_v06` | PASS borné | 13 | 13 | 0 | 13 | 0.78 / 0 |
| `MC_replay_spec_adopt_strong_v06` | FAIL attendu : `RegistryImmutable` | 13 | 13 | 0 | 13 | 0.79 / 12 |
| `MC_replay_spec_strong_v06` | FAIL attendu : `RegistryImmutable` | 9 | 9 | 0 | 9 | 0.74 / 12 |
| `MC_broken_tipsnapshot_v06` | FAIL attendu : `RegistryStableOnCommonPrefix` | 19116 | 4588 | 2485 | 7 | 1.5 / 12 |
| `MC_broken_h1promote_v06` | FAIL attendu : `H1Detector` | 224060 | 46122 | 20537 | 11 | 19.98 / 12 |
| `MC_witness_empty_v06` | TÉMOIN ATTEINT : `NoEmptyEpochWitness` | 56559 | 12359 | 6031 | 9 | 3.91 / 12 |
| `MC_witness_twoempty_v06` | TÉMOIN ATTEINT : `NoTwoEmptyEpochsWitness` | 86289 | 19306 | 9440 | 9 | 3.99 / 12 |
| `MC_live_v06` | PASS borné | 1296 | 386 | 0 | 7 | 6.8 / 0 |
| `MC_safe_v06` | PASS borné | 639168 | 93112 | 0 | 21 | 159.2 / 0 |
| `MC_spec_registryreorg_strong_v06` | FAIL attendu : `RegistryImmutable` | 69227 | 15659 | 7908 | 9 | 1.97 / 12 |
| `MC_spec_registryreorg_v06` | INCOMPLET — plafond (dernier relevé) | 7044269 | 1190110 | 307635 | 17 | 570.0 / -15 |
| `MC_spec_registryreorg_b00_v06` | PASS borné | 2925161 | 402099 | 0 | 26 | 339.59 / 0 |
| `MC_spec_registryreorg_b01_v06` | PASS borné | 2479295 | 339829 | 0 | 26 | 281.76 / 0 |
| `MC_spec_registryreorg_b10_v06` | INCOMPLET — plafond (dernier relevé) | 4978003 | 700997 | 18220 | 22 | 570.01 / -15 |
| `MC_spec_registryreorg_b11_v06` | INCOMPLET — plafond (dernier relevé) | 3880612 | 552409 | 18557 | 22 | 570.01 / -15 |
| `MC_spec_registryreorg_b10_w8_v06` | PASS borné | 5179260 | 718718 | 0 | 29 | 404.68 / 0 |
| `MC_spec_registryreorg_b11_w8_v06` | PASS borné | 4097562 | 572125 | 0 | 31 | 247.7 / 0 |

**Sonde élargie, réunion exhaustive des quatre entrées : PASS conditionnel borné**, 14,681,278 états générés, 2,032,771 états distincts, file totale 0. Les ensembles sont disjoints puisque chaque état conserve son vecteur Bitcoin. Ce résultat composé ne requalifie pas le lancement global interrompu en PASS.

Les codes 12 correspondent tous à des violations d’invariant explicites, pas à une exception ou à une erreur de syntaxe. Pour les mutations, ils démontrent la détection du défaut injecté ; pour les témoins vides, ils réfutent l’anti-propriété et établissent la couverture. Pour les sondes fortes, ils conservent le constat d’impossibilité de la garantie absolue sous les règles actuelles. Les autres invariants d’une campagne arrêtée sur violation ne sont pas réputés vérifiés exhaustivement.

Le replay conditionnel termine avec **13 états et profondeur 13**, soit les 12 transitions prévues : son PASS ne vient pas d’une action devenue inactivable. Le même replay sous l’invariant fort termine avec `RegistryImmutable = FALSE`, alors que `conditional`, `h1`, `anchor`, `bootstrap` et `recovery` restent vrais.

Les PASS TLC restent des résultats finis avec risque résiduel de collision de fingerprints, estimé dans chaque log. Ni probabilité de préfixe commun de N, ni reprise productive universelle ne sont obtenues.

## 7. Reproduction, intégrité et travail restant

```sh
python3 run_v06.py
# Compléter la sonde élargie par les quatre entrées Bitcoin disjointes :
python3 run_v06_shards.py
# Relances exhaustives de b10 et b11 à huit workers, mêmes bornes :
python3 run_v06_retry.py
python3 run_v06_retry_b11.py
# Ou un cas individuel, avec le lanceur original :
TLC_WORKERS=4 ./run.sh MC_replay_spec_adopt_v06
TLC_WORKERS=4 ./run.sh MC_replay_spec_adopt_strong_v06
```

Le runner principal et celui des partitions utilisent le `run.sh` original, quatre workers et sa graine TLC 1. Les partitions `(0,1,0)` et `(0,1,1)` ont aussi atteint le plafond à quatre workers. Leurs relances distinctes `run_v06_retry.py` et `run_v06_retry_b11.py` utilisent huit workers sur la même machine (14 processeurs logiques), sans changer une règle ni une borne. La première relance a été lancée pendant la dernière partition à quatre workers ; la seconde a tourné seule. Aucun nom de module, log ou répertoire TLC n’est partagé entre les processus simultanés. Chaque runner impose un plafond de 570 secondes par cas, termine le groupe de processus en cas de dépassement et inscrit explicitement `NOT A PASS`. Le lancement global de la sonde élargie a effectivement atteint ce plafond : il est INCOMPLET, jamais PASS. `run_v06_shards.py` reprend alors la même sonde avec chacun des quatre vecteurs Bitcoin initiaux `(0,b1,b2)`, sans autre restriction. Comme `bitcoin` ne change dans aucune transition, ces quatre ensembles d’états initiaux sont disjoints et leur union égale exactement `Init`. Un PASS achevé pour chacun des quatre vecteurs (en retenant les relances pour les deux vecteurs commençant par `(0,1,…)`) suffit donc au PASS de la sonde bornée par composition ; ce n’est ni un échantillonnage, ni une réduction d’horizon. Les durées du tableau incluent compilation et démarrage ; les logs fournissent aussi la durée TLC. Les compteurs des recherches arrêtées sur violation peuvent varier avec l’entrelacement des workers. Les replays donnent les traces déterministes pertinentes ; les traces BFS à quatre workers ne sont pas annoncées comme minimisées au-delà de la profondeur observée.

Les résultats structurés sont dans `logs/RESULTATS_v06.json`, `logs/RESULTATS_shards_v06.json`, `logs/RESULTATS_retry_v06.json` et `logs/RESULTATS_retry_b11_v06.json`, les empreintes de la campagne dans `logs/SHA256_v06.json`, les empreintes des fichiers préexistants dans `logs/v06_original_hashes.json` et la vérification dans `logs/INTEGRITE_v06.json`. Seule la transcription externe de la session (`logs/codex-correctif.out`) évolue parmi ces fichiers ; elle n’a pas été éditée par ce travail. Aucun appel Git, commit, modification d’index ou de configuration de dépôt n’est nécessaire ni effectué. La SPEC et le modèle original ne sont pas écrasés.

Restent ouverts : démontrer ou réfuter A3/A4 pour le calendrier de N, définir le domaine réseau/disponibilité, analyser le poids adverse variable et le grinding, couvrir les réorganisations Bitcoin et la persistance après crash. **Les PASS conditionnels ci-dessus ne ferment aucune de ces obligations.** La recommandation règle la contradiction de garantie entre mandat et SPEC ; elle conserve volontairement et visiblement le risque illustré par les contre-exemples.
