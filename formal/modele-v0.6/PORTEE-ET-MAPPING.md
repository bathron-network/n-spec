# Portée, hypothèses et correspondance — campagne v0.6

Cette livraison est une **famille de modèles finis**, et non un modèle intégré de tous les §§4–23. Les interactions entre familles non composées restent NT. Les PASS ne se composent pas automatiquement en une preuve de N. Le modèle historique et le correctif D ont été lus ; `historical/` conserve une copie des sources/configurations v0.5, sans modifier leurs originaux. `RegistryModel` part du correctif D et ajoute réellement A.

## Modèle miroir (§8.1 prioritaire)

`RegistryModel` conserve le générateur v0.5 : deux honnêtes, un adversaire, poids `(2,1,1)`, deux branches, partition puis réunion possibles, absence puis retour possibles, trois époques de deux créneaux, créneaux 0–5, `KReg=1`, `MaxReorg=4`. Les quatre valeurs du vecteur Bitcoin `(0,b1,b2)` sont les seules partitions de la sonde historique. Bitcoin est immuable dans cette famille. `RuleA=FALSE/TRUE` est l'unique différence entre les configurations jumelles.

Évolution sémantique nécessaire : chaque époque e a ici sa maturité publique réduite au début `e*SlotsPerEpoch`. Le premier bloc de la branche dont le slot atteint cette borne est son porteur. Cette restriction est **plus étroite que la SPEC**, qui permet des repères mûrs plus précoces, tardifs ou retenus. `RegistryWindow` explore séparément une fermeture dès le slot 3, tardive et retenue, mais cette sonde ne compose pas une preuve générale avec le miroir.

- `RawSupport`, `Carrier`, `WindowCount`, `Support` : §5.2. Compte inclusif, support strictement avant la coupure, héritage récursif, aucun événement consommé deux fois dans `ReplayOps`.
- `Candidate`, `ProductionRegistry`, `Owner`, `ComputedTie` : dérivation sur l'en-tête candidat, avant signature. Ses opérations ne sont pas dans le cliché autorisé. A désactivée restitue la dérivation historique.
- `RegistryImmutable` : **ancien moniteur local**, inchangé. Il compare l'engagement local mémorisé et l'installation/adoption/signature suivante de la même époque. Il oublie l'ancienne époque et ne compare pas tous les nœuds. Un PASS n'est donc pas celui du moniteur global CP_reg.
- `RegistryStableOnCommonPrefix` : C6 sur cette instrumentation ; l'état de contrôle est limité aux ADD. Aucun filtrage des exécutions où le fort échoue.
- `RegistryCommitments` : instrumentation complémentaire persistante, deux engagements maximum par nœud, même époque, contextes X explicites sans registre/graine finale, préfixes D complets, signature/adoption/installation et comparaisons croisées. Aucun garde conforme ne lit son journal.
- H1, ancre et RECOVERY du miroir restent les abstractions **v0.5** : les résultats du miroir ne qualifient pas ces sous-machines v0.6.

Les deux replays historiques gardent leurs constantes propres, notamment `MaxReorg=1`, `EndSlot=4` pour l'adoption, contre 4 et 5 pour la signature. Un replay est un parcours imposé, jamais une exploration exhaustive de la SPEC. Le nombre d'états atteint doit confirmer l'absence de blocage anticipé.

## Autres familles

| Source normative | Module / opérateurs | Bornes et limites |
|---|---|---|
| §5.2, 23.3 | `RegistryWindow`: `Prepare`, `Validate`, `Carrier`, `Count`, `ARule` | Une branche, slots 0–5, seuil 1/2/4, fermeture possible dès 3, validité finale booléenne. Le bloc invalide ne s'installe pas. Fenêtre ouverte et héritage ; pas de cryptographie/loterie dans cette sonde. |
| §23.4 A3/A5 | `RegistryCommitments`: `Entry`, `Commit`, `CPreg`, `C6` | Cinq histoires préconstruites déclarées historiquement valides ; slots 0–4 ; seuil et maxreorg 2. Validation des signatures/loteries et sélection par Rank de ces fixtures NT : Allowed ne vérifie que le nombre de déconnexions. Les traces sont des contre-exemples de l'abstraction sous ces entrées, pas des attaques cryptographiques démontrées. |
| §§9.5, 12.6–12.7, 23.8 | `H1Orders`: `V`, `M`, `Pairs`, `H1`, `Evaluate`, `Permit` | Deux nœuds, trois branches, six événements indépendants C/W/L/BTC/F/A. F=empreintes, A=authentification et couverture. Chaque sous-ensemble non vide restant peut arriver en une transition : tous ordres unitaires et toutes livraisons groupées. Distances 3/2, LCA abstrait commun, maxreorg=1 ; scénario peu profond à égalité 1. |
| §§12.3–12.5 | `H1Scan`: `Relevant`, `Progress`, `Steps`, `RawLag` | G=2, profondeur BTC=1, hauteurs 1–5, tables exhaustives blocs/dossiers. Objets pertinents manquants ⇒ UNKNOWN ; étrangers ⇒ IRRELEVANT. Recul/avance BTC, cache et rang comme actions. Pas de validation d'octets Bitcoin. |
| §§6.1–6.6, 6.9 | `Brake`: `Observe`, `Replay`, `Health`, `Eligible`, `Select`, `Advance` | Cinq producteurs, L=5, horizon 20 époques, poids total 10/100/1000. Calendrier d'attributions cyclique explicite, **pas une loterie pondérée qualifiée**. Sept époques et caps 2/5/1 % exacts. Le petit calendrier n'atteint ni 144 ni 30 attributions dans les fenêtres : seules les voies temporelles sont exercées. |
| §6.6, scénario 0,68 | `BrakeArithmetic`: `Eligible`, `Filled`, `Health` | Poids 680/120/190/5/5, 680 présences sur 1000, honnêtes disparus 120, adversaires silencieux 200. Tous masques Q ; calcul arithmétique séparé du calendrier cyclique de `Brake`. Ne pas appeler la densité de ce dernier « 0,68 ». |
| §§4.6–4.7 | `Admissions`: `Add`, `ReactExam`, `Rollback` | Tous états, ban/exclusion avant ADD, F_x à 59/60/61 ; x est un identifiant de dossier, pas un bloc. Prix au moment d'inclusion booléen, réservation/consommation. Rollback efface l'examen ; le complément final réexamine avec un prix ultérieur distinct. |
| §§9.5–9.6, 11 | `AnchorBTC`: `M`, `Deep`, `Bbound`, `Exact`, `Select`, `Reorg` | Deux histoires N de hauteur 3, arbre BTC à deux bras de quatre blocs (travail unitaire), vues singleton ou égalité. maxreorg 1/2, D_btc=3. Livraisons séparées avant réunion, ancres persistantes. Pas de conversion 3↔100 ni 3↔2880. |
| §§7.4, 7.6, 10 | `Persistence`: `Prepare`, `Reserve`, `Export`, `Commit`, `CrashRestore`, `S1`, `S2` | Deux clones, un IID/slot/chain_id fixe, deux digests, deux générations, deux crashes par clone, témoin externe durable partagé. Disponibilité/intégrité de ce témoin supposées ; protocole distribué du témoin NT. S2 est une sonde algébrique d'effectivité des générations, pas une vérification cryptographique. |
| §§12.11–12.14, 23.6 | `Authorities`: `Bootstrap`, `Prepare`, `ExplicitApprove`, `Recover` | 0/1/2 canaux, dossiers concordants ou contradictoires, fait BTC valide/invalide, deux demandes fraîches. Aucun fair scheduling de RECOVERY. Canaux abstraits ; indépendance réelle et signatures RELEASE NT. |
| §§7.3, 9.4 | `TieDelivery`: `Parent`, `Reserve`, `Deliver` | Deux variantes de même Rank. Ordre A<B utilisé seulement pour choisir le parent, pas pour départager Rank. Le test de convergence des réservations est volontairement plus fort que la SPEC. |
| §23.9 MON1–MON5 | `Money`: `Import`, `Transfer`, `Commit`, `Crash`, `Withdraw`, `Undo` | Une source BTC de valeur 10, trois pointes, un transfert avec frais, import/notification répété, ressource consommée une fois, crash aux quatre phases. Sources ticket/REACT et conversions complexes absentes : absence d'émission par ces actions non qualifiée. G1–G10 applicatifs, covenants, swaps et conversions NT. |

## Cadence et voie lente

`Brake` rejoue chaque créneau avant la mesure de santé. Les attributions historiques restent dans `calendar`, même après exclusion ; le masque Q de la transition est fixé avant le parcours de file. Les époques héritées inscrivent W_f et zéro exclusion. Les quotas sont prospectifs et utilisent les sept époques calendaires. L'ordre est `(queue_slot,IID)` ; on passe après les poids trop lourds, aucun retrait partiel ou du dernier poids. Une rotation préparée devient effective à l'époque 10 sans lire la santé. L'auto-ommer de l'identité 5 ne crédite pas sa présence mais interdit son éligibilité lente pendant la fenêtre.

La cadence de support, les observations, l'attribution et la rotation préparée sont des entrées publiques déterministes de la sonde, pas des décisions locales. La SPEC ne laisse pas de choix local dans le lot une fois ces entrées établies. La disponibilité des données et ressources peut retarder l'exécution ; l'implémentation doit annoncer cette limite, sans changer le registre. Le domaine utile de progression reste conditionnel à l'avancement de support, au poids indivisible et aux budgets.

## Hypothèses H_N et équité

Aucune hypothèse de CP_reg, compatibilité d'ancres ou densité minimale ne filtre Init/Next. Le miroir a une origine commune, horloge logique parfaite, adversaire de poids initial 1/4, réseau partitionnable et un absent, source BTC à quatre vecteurs fixes, rétention illimitée, horizon fini. Il n'impose aucun Δ sur toute l'histoire, aucune borne de corruption adaptative ni de grinding. Ce domaine **n'est pas H_N qualifié** ; aucune epsilon n'est déduite des états TLC.

Les familles ciblées annoncent leurs fixtures/entrées ci-dessus. Elles ne prouvent pas la faisabilité de toutes ces entrées par la loterie réelle. Le calendrier public, le ciblage, les corruptions anciennes, les ressources et le grinding ne sont pas probabilistiquement analysés.

`MC_brake_live` impose uniquement WF(Advance), sur un calendrier fini déterministe avec supports récurrents et données fournies : atteindre un lot lent dans ce scénario. Ce n'est ni L2 universelle ni une croissance infinie. Les témoins d'existence et les propriétés temporelles restent séparés. Aucun modèle ne rend l'acceptation administrative équitable. La vivacité générale sous livraison/production équitables, les cycles entre sous-machines et la restauration intégrale de tout contrôle restent NT.

## Restrictions et outillage

Toutes les campagnes sont BFS, sans symétrie, CONSTRAINT ou ACTION_CONSTRAINT. Les restrictions portent explicitement sur Init, Next et les constantes. `CHECK_DEADLOCK FALSE` traite la fin d'horizon comme terminale autorisée, sans démontrer l'absence de deadlocks en production. Aucun succès ne découle d'un timeout. Les mutations sont des configurations séparées, jamais activées dans un run conforme. Le risque résiduel de collision de fingerprints est celui indiqué par TLC dans chaque log ; les explorations ne constituent pas des preuves déductives illimitées.

## Versions finales et compléments de campagne

Les opérateurs de la table ci-dessus sont conservés dans les modules finaux `H1OrdersChecked`, `BrakeChecked`, `RegistryWindowChecked`, `RegistryCommitmentsChecked`, `AnchorBTCChecked`, `AdmissionsChecked`, `PersistenceChecked`, `MoneyChecked`, `AuthoritiesChecked`. Les modules sans ce suffixe sont conservés comme premiers essais ; des parenthèses manquantes autour d'affectations booléennes pouvaient transformer un moniteur en garde ou produire un successeur incomplet. Les configurations `_checked` sont celles à retenir, avec les sondes complémentaires qui les étendent. Les erreurs d'outil des premières versions ne sont pas des violations normatives.

Pour le registre, `RegistryModel` est le premier essai ; `RegistryModelV6` corrige l'installation en fenêtre ouverte : l'adoption peut changer la pointe, mais ne remplace pas le registre courant sans porteur. `RegistryModelFast` et `RegistryModelFast2` conservent cet état de transition. Ils simplifient le calcul, sans nouvelle restriction d'histoire :

1. Cut(e)≤0 ⇒ tous supports précédents et courant sont genesis.
2. Len(C)<seuil ⇒ le compte ne peut atteindre le seuil ⇒ héritage.
3. Dans cette projection **ADD uniquement**, les supports monotones rendent l'union des opérations autorisées égale aux opérations du dernier support. Le registre de support vide est le vecteur initial.

`ReferenceSupport` et le `ReplayOps` récursif restent disponibles. Les campagnes `MC_support_equivalence_*` et `MC_registry_equivalence_*` comparent les formes sur toutes les sous-suites ordonnées des slots 0–5 des deux branches (127 histoires distinctes), aux seuils 1, 2 et 4. L'argument d'équivalence est aussi structurel : compte≤longueur, coupures croissantes, supports monotones et opérations ADD idempotentes. **Cette simplification ne se généralise pas à la machine complète de contrôle avec opérations non commutatives.** Aucune VIEW, symétrie ou contrainte d'états n'est ajoutée.

Compléments :

- `H1Reevaluation` vérifie explicitement changement de rang, changement de vue Bitcoin, MAINTAIN et éviction avec archive conservée. La priorité temporelle conserve le motif de base ; une preuve peut devenir objectivement hors périmètre quand le maximum change.
- `MC_live_reconnection` est un suffixe avec branches déjà construites, partition puis réunion, absent puis retour. WF porte sur Heal, Return et Receive de toutes les données restantes de chaque nœud. Les protections sont supposées compatibles dans la base abstraite ; aucune équité RECOVERY. Le résultat est une reprise d'autorisation après convergence des données, pas une production infinie.
- `QuotaHistory` conserve les plafonds au moment de chaque décision et applique ensuite un ban : une exclusion passée de 10, admissible sous W=1000, demeure admissible lorsque le poids courant tombe à 90 ; le budget suivant devient zéro. Les bans et toute l'activité ne sont pas intégrés dans cette famille.
- `BrakeChecked` ajoute un scénario d'héritage aux époques 11–13, après une exclusion déjà exécutée. Cela recherche explicitement le rejeu erroné d'une exclusion.
- `AdmissionsChecked` conserve les tickets dormants et leur état d'activité, applique l'exclusion avant ADD, compare le prix d'inclusion 10 à un prix ultérieur 20 et permet rollback/réexamen. L'opérateur REACT teste la **classification du premier examen**, avec réservation/consommation antérieures en entrée ; il ne prétend pas implémenter toute l'activation REACT.
- `AnchorBTCChecked` calcule `BestWork` sur les pointes BTC disponibles (travail unitaire), avec égalités et vues de travaux différents. `SlowBTC=TRUE` place tous les repères N au même bloc BTC récent ; le témoin conserve une ancre genesis malgré trois liens N. D_btc=2 et 3 testent la borne inclusive. Genesis conserve séparément S0 et repère g, scellement a1 ; le témoin seal_only ne consomme pas de graine.

### Réduction qui masque un phénomène : seuil 4 dans le miroir historique

Pour e=2, Cut=1 et la maturité réduite est au slot 4. Il n'existe que quatre slots comptables 1–4 si ce premier porteur est au slot 4. Le seuil historique 4 est donc très exigeant dans cette fenêtre ; ce n'est pas le ratio des paramètres nominaux. Le témoin d'avancement interdit de traiter le miroir comme purement vide, mais son PASS éventuel ne se transfère pas à 2880/7200. Les campagnes générales à seuil 1 puis 2 compensent cette réduction : elles retrouvent une violation de l'ancien fort avec A active, sans dépasser la déconnexion permise.

`RegistryAudit` complète ces recherches avec un ensemble persistant des engagements distincts, incluant nœud, slot, type signature/adoption/installation, époque, X, D_e, registre, projection de contrôle et calendrier. Il n'oublie aucune ancienne époque dans l'horizon et aucun garde de Next ne lit ce journal. Les répétitions strictement identiques sont coalescées ; cela ne change pas les comparaisons par paires. `MC_audit_cp_k1` fixe Bitcoin à (0,0,1), `MC_audit_cp_k2` à (0,1,1), pour rechercher un contre-exemple (pas pour revendiquer un PASS sur les quatre vecteurs). Les replays audit_cp/audit_c6 comparent les deux obligations sur la même histoire issue de productions effectives du modèle.

Dans `BrakeChecked`, les bornes consolidées c et l'avancement du support sont des **entrées de la sous-machine de contrôle**. Le calendrier de cette sonde n'est pas construit conjointement par la règle A et la loterie de `RegistryModelFast2`. Sa réalisation jointe, le retard nominal du cliché et les ressources de validation restent dans l'inventaire NT. Ce choix suffit à vérifier la mécanique du lot conditionnel aux entrées, pas à prouver que ces entrées se produisent avec telle probabilité ou à toute époque réelle.

`MC_brake_live_mechanical` reformule WF(Advance) par WF_epoch(epoch<Horizon /\ epoch'=epoch+1). Sur Spec, Advance est la seule action non bégayante et est totale dès epoch<Horizon ; elle incrémente toujours epoch. Les deux actions ont donc la même activation et la même vérité sur toute transition du modèle. Cette reformulation évite à TLC de recalculer le contrôle complet pour ENABLED ; elle n’ajoute aucune occasion ni donnée. Le run direct reste conservé séparément.

Le replay de fermeture entre fixtures ne valide pas BaseNDecision : son passage d’une histoire de longueur 3 à une histoire de longueur 2 ne serait pas une adoption du maximum si les deux étaient disponibles. Il illustre la fermeture et la distance, pas une attaque exécutable de sélection. Les contre-exemples `MC_general_a_k{1,2}_strong` et leurs replays proviennent, eux, du générateur qui vérifie la production et BaseAdoptable ; leur analyse de déconnexion est indépendante de cette fixture.
