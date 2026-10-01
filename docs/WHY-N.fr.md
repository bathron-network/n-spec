# Pourquoi N

**Architecture frozen candidate. Not mainnet-qualified. Not production-ready.**
(Candidat d'architecture gelé. Non qualifié pour le mainnet. Pas prêt pour la production.)

Pourquoi le moteur de base de BATHRON est N (sans vote, un producteur par créneau), ce qu'il garantit et sous quelles conditions. Texte normatif : **N-SPEC v0.7**. Contre-exemples : **ATTACKS.fr.md**. Version anglaise : `WHY-N.md`.

Statut au 1er octobre 2026 : N v0.7 est gelé **au niveau architectural**. Toute modification de l'architecture exige l'un de ces quatre déclencheurs : un contre-exemple, une violation d'invariant, une impossibilité d'implémentation, ou une mesure réelle incompatible avec H_N. La recherche d'une architecture « plus élégante » n'en fait pas partie. Une valeur de paramètre mal choisie se corrige dans H_N ou dans un profil client.

---

## 1. Ce qui a été abandonné, et pourquoi

Chaque candidat ci-dessous a subi des kill-tests menés par au moins deux analyses indépendantes, et plusieurs ont en plus fait l'objet de relectures aveugles.

### C : séquenceur et quorum de détenteurs de tickets (famille Tendermint)

C associait un séquenceur unique à un quorum de détenteurs de tickets qui finalisait les lots (`q > (N+f)/2`, verrou par hauteur, certificats chaînés, ban sur équivoque prouvée). Son modèle TLA+ borné, adapté d'un modèle Tendermint publié, n'a trouvé **aucune violation de sûreté**, et toutes les variantes volontairement cassées ont été détectées. C n'a pas été abandonné pour un défaut de sûreté. Trois éléments ont pesé contre lui :

- **β n'est pas garantissable.** Le kill-test sur β a montré que l'affirmation « le burn garantit β » est fausse. Un burn a un coût, mais il ne borne ni la concentration, ni la location de clés, ni la corruption, ni la coercition, ni l'attrition. Au lancement, avec quelques opérateurs gérés par le projet, aucun β < 1 n'est défendable.
- **Le coût.** Les votes post-quantiques de milliers d'opérateurs coûtent cher. Une analyse estime les signatures de production de N à ≈ 35 Mo/jour (créneaux de 6 s), contre ≈ 49 Go/jour pour deux phases C complètes toutes les 60 s à 7 000 identités, soit un facteur ≈ 1 400.
- **L'économie des témoins.** Une relecture aveugle de l'économie n'a trouvé aucune rémunération des témoins.

C est **archivé** comme finality gadget possible d'une évolution future. Au genesis, rien ne défère à C. Un C privé ajouté au-dessus de N fournirait une attestation ou une assurance, jamais une « finalité de N ».

### La finalité sans quorum : D, D2, D3, barrière Bitcoin

- **D** (finalité par convergence) : tué. Un propriétaire qui équivoque, combiné à une partition, produit deux « finalités » incompatibles, et le silence ne prouve rien.
- **D2** (finalité mécanique) : sans vote, l'unicité exige un journal commun qui n'équivoque pas, c'est-à-dire Bitcoin. Le prix est une transaction Bitcoin par transfert ou par lot. Non adopté.
- **D3** (lignée unique, Bitcoin en lecture seule) : tué pour les paiements libres. Pour toute règle locale, P[double lignée] ≥ 2·(vivacité d'un paiement honnête) − 1. Lire Bitcoin prouve « après H », jamais « avant H ». Ce qui survit : les automates d'horloge et l'**objet de swap à un saut**.
- **Barrière Bitcoin** (BFT synchrone cadencé par les blocs Bitcoin) : la sûreté repose sur Δ. Deux tickets et une partition plus longue que 2Δ suffisent à produire deux FINAL silencieux.

### Certificats échantillonnés et hybrides : E, E2, deux étages, NC

- **E/F** : l'échantillonnage ne donne pas de petits comités (≈ 200 membres à β = 0,1, 1 300 à 2 600 à β = 0,2, impossible à β = 0,3), et E dépend encore de C. Reporté.
- **E2** (SBRB/DPRB fidèles aux papiers) : **fermé**. Il demande de 27 à 252 Mbit/s par nœud à 32 tx/s (contre ≈ 5 pour C). Sa sûreté n'est que probabiliste, sous un adversaire statique, et il ne fournit aucune preuve exportable.
- **Deux étages** (chaîne et checkpoints C) et **NC** (finalité C par objet) : aucun gain sur β. Dans NC, la finalité ne reste pas locale : elle se propage en profondeur, en amont et vers les nœuds neufs.

Fil commun : la finalité ferme exige un quorum à intersection, des écritures dans Bitcoin, ou une synchronie qui porte la sûreté. Le 30 septembre, le propriétaire a choisi de renoncer à la finalité ferme.

## 2. Pourquoi N existe

N répond à un choix explicite du propriétaire du projet, le 30 septembre : **N pur au genesis**.

- Un producteur par créneau, tiré mécaniquement à partir de Bitcoin et du registre des tickets.
- Une fork-choice mécanique, sans vote, quorum, QC, verrou, round ni certificat.
- Les tickets servent de loterie de production ; ils ne donnent pas de poids de vote. Un burn de `P0 = 1 000 000 sats` donne une unité de poids. Le burn rend les Sybils coûteux ; il ne garantit pas l'indépendance des tickets.
- Aucune récompense de bloc : les frais sont transférés, jamais créés.

N renonce à la finalité ferme, à la preuve de finalité exportable et à la règle « pause plutôt que recul ». Le vocabulaire client est **inclusion → profondeur → stabilité selon une politique**, et il n'existe aucun statut natif `FINAL`. L'atomicité est garantie **sur chaque branche** : un règlement livraison contre paiement X/M1 est tout ou rien. Pour BTC/M1, la jambe Bitcoin est irréversible. Le risque résiduel ε(k) est donc porté et tarifé par le prestataire de règlement ou de liquidité (SP/LP), au moyen de la profondeur qu'il choisit.

En échange, N offre une chaîne qui continue de produire, mécanique « comme Bitcoin », avec une bande passante de signatures inférieure de deux à trois ordres de grandeur à celle d'un moteur à votes.

## 3. Répartition des propriétés

> Bitcoin crée les racines. Les objets transportent et conservent les droits. N choisit l'histoire canonique lorsque des évolutions deviennent incompatibles.

| Propriété | Portée par | Sens |
|---|---|---|
| **Provenance** | Bitcoin | Toute ressource monétaire a une origine Bitcoin typée. L'offre est égale à la somme des burns. TICKET et REACT créent zéro M0 et zéro M1. |
| **Conservation** | Objets / Core | Les transitions sont valides dans chaque histoire. Une transition native et son undo sont atomiques. C'est une obligation d'interface (G1–G10), vérifiée conjointement avec la spécification applicative : N seul ne démontre pas la conservation monétaire. |
| **Canonicité** | N | Sélection d'une histoire parmi des histoires incompatibles. C'est la seule chose que N décide. |
| **Antériorité** | Bitcoin | Engagement d'un préfixe dans une transaction Bitcoin admissible (burns M0, tickets NEW/ADD, REACT). Il n'existe aucune transaction `ANCHOR` dédiée. |
| **Origine** (nœuds nouveaux ou de retour) | A′ / RELEASE | Dossier `BOOTSTRAP` distribué avec les releases, authentifié par 4 clés avec un seuil de 3 sur 4. La récupération exceptionnelle passe par un dossier `RECOVERY` accepté explicitement. |

Sous N, une attaque longue portée est donc un conflit de **registre**, jamais de monnaie. La conservation monétaire (aucune création de M0 ou de M1) ne vaut **que sous les obligations applicatives G1–G10 (spec §21), pas encore qualifiées**.

## 4. Subjectivité faible

N est faiblement subjectif, par décision explicite du propriétaire (D1, 1er octobre).

- Un nœud **synchronisé**, c'est-à-dire qui satisfait lui-même les hypothèses réseau de H_N, est protégé par `maxreorg`. Une branche privée qui change de calendrier après le début d'une époque exigerait une réorganisation plus profonde que `maxreorg`. Le nœud passe alors en `HALTED_DEEP_REORG` au lieu de l'adopter. Cette protection est probabiliste et non déterministe : la probabilité d'échec est bornée par le terme `T_CG` de la composition.
- Un nœud **nouveau ou de retour** (sans origine locale, ou dont la réception est sortie du régime D = 0) est **hors du domaine CP_reg**. Il peut adopter une branche privée sans aucune déconnexion interdite. Ce risque n'est pas borné : c'est la longue portée, qui réapparaît par le registre.
- Il ne revient dans le domaine qu'après une initialisation depuis une **origine authentifiée récente**, c'est-à-dire postérieure d'au moins `maxreorg + 1 = 1 631` blocs à toute fourche pertinente. Un nœud neuf passe par un `BOOTSTRAP`. Un nœud de retour qui conserve son origine passe par la `RECOVERY` explicite, qui conserve ses réservations de signature et sa mémoire anti-double-signature.
- Une origine n'a **aucun pouvoir sur la fork-choice** d'un nœud synchronisé. Un `BOOTSTRAP` reçu par un nœud qui a déjà une origine locale est ignoré (`BOOTSTRAP_IGNORED_LOCAL_ORIGIN`). Le fonctionnement ordinaire (redémarrage, absence, rattrapage, fork-choice) n'exige aucun checkpoint. Un bootstrap n'expire pas du seul fait de son âge, et aucun temps écoulé ne vaut approbation d'une nouvelle origine.

## 5. Le rôle de Bitcoin

Pour N, Bitcoin est en lecture seule : N ne modifie jamais les règles de Bitcoin et n'ajoute aucune transaction d'ancrage. Bitcoin fournit quatre choses :

1. **Les racines.** Les burns créent le M0 et les tickets. Une REACT est authentifiée par la signature Bitcoin elle-même.
2. **Les faits.** Chaque nœud vérifie lui-même les en-têtes, les confirmations et les paiements. Le swap BTC/M1 à un saut est résolu par l'inclusion de la jambe Bitcoin.
3. **Le temps.** Il comprend la MTP (median time past), une garde de graine de 12 h (43 200 s), une marge MTP de 7 200 s, et des durées comptées en hauteurs Bitcoin (`G_anchor = 26 280`, cadence 13 140, grâce REACT 4 032).
4. **L'aléa.** La graine d'époque hache le premier bloc Bitcoin dont la MTP atteint l'heure de graine, enfoui à `k_seed = 30` confirmations, ainsi que la racine du registre. Aucun parent N, état, signature ni nonce de producteur n'entre dans la graine.

**Les empreintes peuvent déclencher un STOP, mais ne promeuvent jamais une branche.** L'invariant du propriétaire, tel qu'il figure dans N-SPEC :

> une preuve d'antériorité Bitcoin peut réduire l'ensemble des histoires qu'un nœud considère sûres ou déclencher un arrêt ; elle ne peut jamais, à elle seule, rendre canonique une histoire que la fork-choice N n'aurait pas choisie.

H1, le contrôle longue portée, est un **veto séparé** : la décision de base de N reste identique, ou devient une attente ou un arrêt. H1 ne modifie jamais le score, le départage, le registre, l'ancre ni l'origine. Il suppose au moins une empreinte valide environ tous les 13 140 blocs Bitcoin (≈ 3 mois), avec une fenêtre `G_anchor` d'environ 6 mois. Au bootstrap, un véritable ADD de 0,01 BTC par trimestre est prévu si l'activité naturelle ne suffit pas. H1 n'offre pas de protection longue portée complète et ne protège pas un nœud neuf sous éclipse.

## 6. Le domaine H_N

H_N **fait partie du protocole**. Les garanties quantitatives de N (préfixe commun, CP_reg, profondeurs de sûreté) ne valent que dans ce domaine. Un seul profil est publié (profil B), pour garder une frontière simple et vérifiable.

| # | Hypothèse | Valeur | Statut |
|---|---|---|---|
| H_N-1 | Durée de créneau | τ = 10 s | Décision, sur banc |
| H_N-2 | Poids adverse, sur le poids **total**, à tout instant de l'horizon | β ≤ 0,30 | Décision |
| H_N-3 | Disponibilité honnête effective (DoS ciblé compris) | d ≥ 0,70, donc h = (1−β)d ≥ 0,49 | Décision |
| H_N-4 | Blocs honnêtes en retard, sur toute fenêtre de 1 913 créneaux | p_late ≤ 10⁻² | Hypothèse conservatrice, **non certifiée** |
| H_N-5 | Retards indépendants, non choisis par l'adversaire | — | Hypothèse non vérifiée |
| H_N-6 | Réseau de classe W1 | aller-retour ≲ 170 ms, perte ≲ 0,5 % | Décision ; émulation |
| H_N-7 | Sauts de relais du producteur vers tout honnête | ≤ 2 | Décision ; extrapolation |
| H_N-8 | Écart d'horloge | ≤ 100 ms | Décision ; mesure |
| H_N-9 | Validation par saut | Δ_val = 100 ms | Micro-banc cryptographique ; accès à l'état non testé |
| H_N-10 | Condition d'existence | (1−β)·d·(1−2p_late) > β ; au coin, 0,4802 > 0,30 | Analytique, nécessaire |
| H_N-11 | Condition renforcée | d ≥ d_min(β, ε) ; 0,70 contre 0,524 requis (≈ 0,53 à p_late = 10⁻²) | Analytique + interpolation |
| H_N-12 | Cible de sûreté | ε_H = 10⁻⁹ sur 10 ans (2 192 époques de 40 h) | Décision |
| H_N-13 | Graines Bitcoin sélectionnables par époque | Q_B = 1 (256 non qualifié) | Décision |
| H_N-14 | Origine commune | nœud synchronisé au sens du §4 | Décision D1 |
| H_N-15 | Adversaire couvert | calendrier public, choix du moment, rétention, révélation optimale, équivoque (une unité de progrès par branche), abstention, départage défavorable | Analytique (DP) |

Paramètres dérivés (borne DP, composée par époque, arrondie vers le haut) : **K_reg = 2 750 créneaux** (7 h 38 min) et **registry_min_blocks = maxreorg = 1 630 blocs**. Le risque composé sur l'horizon vaut ε_H ≈ 4,6·10⁻¹⁰ ≤ 10⁻⁹. Ce sont des dérivations conditionnelles, pas des garanties acquises : la courbe DP est extrapolée sous 10⁻¹⁴, et la composition des deux termes de pivot reste une esquisse.

**Hors domaine :** les réseaux W2 ou pires ; plus de 2 sauts ; des horloges au-delà de 100 ms ; β > 0,30 ou d < 0,70 à un instant quelconque ; des retards corrélés ou ciblés ; les nœuds nouveaux ou de retour avant réinitialisation ; Q_B > 1 ; un horizon au-delà de 10 ans. Hors H_N, N ne fait **aucune prétention quantitative**. Seuls les arrêts et récupérations existants s'appliquent. **Rien ne garantit qu'un STOP se déclenche hors domaine.**

## 7. Pourquoi les SP et les LP choisissent leur profondeur

N n'a pas de finalité ; il publie une table. K(ε) est la profondeur au-delà de laquelle une violation du préfixe commun a une probabilité d'au plus ε **par coupure**, au coin le plus défavorable du domaine (β = 0,30, d = 0,70, p_late = 10⁻²) :

| ε par coupure | K créneaux | K blocs | Durée à τ = 10 s | [meilleure attaque privée exacte, créneaux] |
|---|---:|---:|---:|---:|
| 10⁻⁶ | 937 | 739 | 2 h 36 min | [584] |
| 10⁻⁹ | 1 425 | 1 123 | 3 h 58 min | [903] |
| 10⁻¹² | 1 913 | 1 508 | 5 h 19 min | [1 224] |

« K blocs » compte les créneaux non vides, équivoques comprises. Ne compter que les blocs honnêtes visibles ne serait pas sûr. La profondeur par défaut du profil de livraison H_N est **K(10⁻⁶) = 739 blocs**. Core expose la table complète, et chaque SP ou LP peut exiger une profondeur plus grande pour un ε plus petit. Le risque appartient à celui qui livre une valeur extérieure : c'est donc lui qui choisit la profondeur, avec un plafond d'exposition. Le seuil de densité de livraison (`rho_deliv = 43/100`) ne joue que sur la vivacité. Une vérification TLA+ bornée de non-interférence (13 classes de seuils, sur un modèle au frein simplifié) n'a trouvé aucun chemin de ce seuil vers la fork-choice, l'ancre, STOP, la règle de registre, le frein ou la production. La vérification avec le frein fidèle, puis sur l'implémentation, reste ouverte (QR-5).

## 8. Ce que N garantit sous H_N, et ce qu'il ne garantit pas

**Sous H_N, N revendique :**
- un préfixe commun à la profondeur K(ε) par coupure, selon la table publiée (borne DP analytique) ;
- l'accord sur le registre (CP_reg) entre nœuds synchronisés, comme dérivation conditionnelle (pas un théorème clos), avec ε_H ≈ 4,6·10⁻¹⁰ ≤ 10⁻⁹ sur 10 ans ;
- pour un nœud synchronisé, un arrêt profond (`HALTED_DEEP_REORG`) plutôt que l'adoption d'une branche privée qui change de calendrier après le début d'une époque, sauf avec une probabilité d'au plus `T_CG` (les pivots sous `maxreorg` sont comptés à part, dans `T_court` et `T_profond`, à l'intérieur de ε_H) ;
- le déterminisme : une même chaîne candidate, une même époque et un même contexte Bitcoin donnent le même registre et la même graine, quelles que soient les observations antérieures du nœud ;
- l'atomicité des transitions natives sur chaque branche ;
- aucune création monétaire par N, et aucun pouvoir sur la fork-choice pour une origine ou pour H1.

**N ne garantit pas :** une finalité native ; la convergence entre origines incompatibles ; une synchronisation sûre sous éclipse ; un calendrier imprévisible ; un aléa Bitcoin non biaisé ; une protection longue portée complète ; un coût d'attaque universel ; l'absence de censure ou de DoS ; l'atomicité BTC/M1 après disparition du verrou ; la conservation monétaire sans qualification applicative. Les arrêts profonds persistent tant que le conflit demeure.

## 9. Réserves de qualification (QR-1 … QR-10)

Chaque réserve ouverte a une phase et un critère d'acceptation. L'ordre prévu est : implémentation → simulation → fuzzing → banc étendu → audit externe → testnet. Un testnet public suppose QR-1 à QR-9 acceptées.

| ID | Exigence | Statut (1er oct.) |
|---|---|---|
| QR-1 | Mesurer Δ, l'écart d'horloge et p_late avec un client N réel, sur au moins 3 continents, avec au moins 2 sauts réels et des blocs maximaux | Mesure européenne seulement, plus émulation |
| QR-2 | Estimer la corrélation des retards et la borne par fenêtre, y compris sous coupures et DoS ciblé | Supposée |
| QR-3 | Expliquer le facteur 1,3 à 1,8 entre la borne DP et le Monte-Carlo sur K | Ouvert (DP publiée, conservatrice) |
| QR-4 | Terminer l'exploration TLA+ stricte du pivot profond, ou en prouver une abstraction | INCOMPLET (5,2 M états) |
| QR-5 | Refaire la non-interférence de la livraison avec le frein fidèle, puis sur l'implémentation | PASS borné sur un modèle simplifié |
| QR-6 | Rédiger la preuve de composition (ε_fix + pivots + T_CG) et la faire relire indépendamment | Esquisse sous hypothèses |
| QR-7 | Qualifier le grinding de la graine Bitcoin (MTP, rétention, horodatages), puis décider de Q_B | Q_B = 1 supposé |
| QR-8 | Spécifier et tester la procédure de RECOVERY par nœud | Non spécifiée |
| QR-9 | Requalifier A4 (compatibilité des ancres) aux paramètres v0.7 | Ouvert |
| QR-10 | Aligner les profils clients (`alpha_budget`, `Delta_nom_ms`, β) sur H_N | Ouvert (documentation) |

N v0.7 est un candidat dont les faiblesses sont nommées et dont les paramètres sont dérivés. Ce n'est pas un système qualifié.
