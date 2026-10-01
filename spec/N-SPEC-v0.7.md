# N-SPEC v0.7 — Consensus mécanique sans vote

**Date : 1er octobre 2026**  
**Statut : spécification normative candidate ; non qualifiée mainnet.**  
**Remplace : N-SPEC v0.6.**

**v0.7 = v0.6 + paramètres dérivés + domaine H_N publié. Aucune mécanique n'est modifiée.** Cette version applique `DIRECTION.md`, lignes « Mandat orchestrateur — dernier chantier avant gel (01/10) », « Lemme L1 / CP_reg — décisions (01/10) » et « Domaine H_N — décisions (01/10) ». La valeur `tau_ms` = 10 000 est une **décision du propriétaire** fondée sur le banc réseau, utilisée comme entrée de la dérivation ; les valeurs `K_reg`, `registry_min_blocks` et `maxreorg` client sont **dérivées** de `etudes/n-spec/cp-reg/derivation/results/composition.csv` sous le domaine H_N du §17, puis arrondies vers le haut ; les textes dépendant de τ ou de K_reg sont recalculés. Le détail figure dans `CHANGELOG-v0.7.md` et le contrôle de cohérence dans `cp-reg/COHERENCE-v0.7.md`. Les règles ci-dessous sont, pour le reste, celles de la v0.6, qui appliquait la ligne « N v0.6 — décisions (30/09) », le mandat v0.6, les trois avis aveugles v0.5 et le correctif de garantie du registre.

Le registre suit **D + A** : stabilité conditionnelle C6/A5, obligation séparée de préfixe commun `CP_reg`, et héritage du support tant que la fenêtre de branche ne contient pas `maxreorg` blocs. Aucun verrou local ni seuil minimal de production n'est ajouté. `CP_reg` est désormais **analysée sous H_N** (§5.7.2, §17) : la garantie obtenue est conditionnelle et dérivée, pas un théorème clos.

H1 examine les paires orientées de toute candidate maximale avec toute branche validée profonde. Il est réévalué après chaque changement des données, même après adoption de la candidate. Le frein mesure la santé hors QUEUED et conserve une voie lente d'exclusions ainsi que les rotations.

La garde de graine de douze heures, le fonctionnement ordinaire sans checkpoint administratif et la séparation entre `BOOTSTRAP` et `RECOVERY` sont conservés.

Elle applique textuellement l’invariant propriétaire :

> **une preuve d’antériorité Bitcoin peut réduire l’ensemble des histoires qu’un nœud considère sûres ou déclencher un arrêt ; elle ne peut jamais, à elle seule, rendre canonique une histoire que la fork-choice N n’aurait pas choisie.**

Les paramètres de dimensionnement introduits par la v0.6 restent des **valeurs de travail**, à qualifier avant gel. Les trois paramètres dérivés de la v0.7 (`tau_ms`, `K_reg`, `registry_min_blocks` = `maxreorg`) découlent des décisions du propriétaire sur τ et sur le domaine H_N ; ils ne valent que dans ce domaine et ne sont pas des constantes mainnet qualifiées.

---

## Préambule

> Bitcoin crée les racines. Les objets transportent et conservent les droits. N choisit l’histoire canonique lorsque des évolutions deviennent incompatibles.

| Propriété | Objet |
|---|---|
| Provenance | Origine Bitcoin des ressources |
| Conservation | Validité des transitions dans chaque histoire |
| Canonicité | Sélection d’une histoire par N |
| Antériorité | Engagement d’un préfixe dans une transaction Bitcoin admissible |

N n’émet aucune monnaie par récompense de bloc. Les frais, droits actifs, calendriers et états applicatifs dépendent de l’histoire retenue.

Les contraintes propriétaires applicables sont :

1. N pur, sans vote de consensus.
2. Un producteur unique par créneau, désigné mécaniquement à partir de Bitcoin et du registre.
3. Bitcoin fournit des faits vérifiés ; N ne modifie pas les règles Bitcoin.
4. Les empreintes utilisent exclusivement les burns M0, NEW/ADD et REACT existants.
5. Aucun type ni transaction dédiée `ANCHOR`.
6. `G_anchor = 26 280` blocs Bitcoin et `anchor_cadence = 13 140` blocs Bitcoin.
7. Au bootstrap opérationnel, un véritable ADD de 1 000 000 sats à cette cadence reste prévu si l’activité naturelle ne fournit pas le progrès nécessaire.
8. H1 est un détecteur, jamais une autorité positive de sélection.
9. Le registre est dérivé d’un préfixe stable commun ; aucun verrou local de registre.
10. Les releases distribuent des `BOOTSTRAP` authentifiés par quatre clés, seuil 3/4.
11. Leur dépendance administrative commune au lancement est publiée.
12. Un `BOOTSTRAP` n’expire pas du seul fait de son âge.
13. Aucun checkpoint n’est requis par la seule durée d’une absence, d’un arrêt ou d’un rattrapage.
14. Un `BOOTSTRAP` ne change jamais chaîne, ancre, registre ou rang d’un nœud ayant une origine locale.
15. Une récupération exceptionnelle exige une acceptation explicite du dossier exact.
16. Le modèle formel et les vérifications du §23 précèdent tout gel.

Les paiements BTC/M1 restent des faits applicatifs. Ils ne deviennent pas des transactions supplémentaires d’ancrage ou de consensus.

---

## 1. Portée et invariants

### 1.1 Catégories normatives

**DOIT**, **NE DOIT PAS**, **DEVRAIT** et **PEUT** expriment respectivement une obligation, une interdiction, une recommandation et une possibilité.

| Catégorie | Dépendances |
|---|---|
| Validité historique | Octets, ascendance, contexte de branche, faits Bitcoin |
| Adoption locale | Rang, origine, ancre persistante, état durable, détecteur H1 |
| Discipline de production | Créneau courant, horloge, données, clé, réservation |
| Politique client | Profondeur, densité, exposition, risques et disponibilité |

Une interdiction locale d’adoption ne rend pas une branche historiquement invalide.

Une observation d’horloge locale n’est pas une preuve publique de la date réelle d’une signature.

Le champ historique `checkpoint_id` de certains objets désigne un bloc N ; il n’implique pas une intervention administrative.

### 1.2 Périmètre

N spécifie :

- identités, tickets, rotations, exclusions, REACT et bans ;
- registres, graines, créneaux et production ;
- encodages natifs ;
- validation, classement, réorganisations et arrêts ;
- traitement des faits Bitcoin ;
- origines de confiance et synchronisation ;
- interface du graphe monétaire ;
- règlement BTC/M1 ;
- politiques de risque et qualification.

Les ressources M0/M1, conversions, autorisations et covenants sont définis par la spécification engagée par `application_spec_id`.

**G1–G10 sont des obligations d’interface à vérifier conjointement avec cette spécification. Leur énoncé ne démontre pas la conservation monétaire.**

### 1.3 Changements de version

Le manifeste, le descripteur pré-genesis, le profil client et le dossier de checkpoint restent en version **6** (formats inchangés depuis la v0.6). Les formats KEYREG, ROTATE et bloc restent en version **3** ; la preuve d'équivoque reste une paire d'en-têtes. Le réseau et les documents engagés identifient les règles v0.7, qui ne diffèrent de la v0.6 que par des valeurs de paramètres et le domaine H_N publié.

Les paramètres de support, voie lente et profondeur Bitcoin de l'ancre sont explicités au §3. Les choix de dimensionnement ajoutés par la rédaction sont des valeurs candidates à qualifier, pas des garanties mainnet.

Les anciens verrous locaux, l'ancrage implicite d'un registre engagé, les SCC temporelles et le filtrage H1 suivi d'un nouveau classement restent interdits. Aucun arrêt autonome pour changement de registre n'est réintroduit.

Aucune migration implicite depuis un réseau antérieur n'est fournie : une activation sur un réseau vivant exigerait une spécification distincte. Cette rédaction conserve tous les formats et règles non modifiés dans un document autonome.

### 1.4 Invariants

1. TICKET et REACT créent zéro M0 et zéro M1.
2. Toute ressource monétaire possède une provenance Bitcoin typée.
3. Un ticket reste acquis jusqu’au ban ; l’exclusion suspend son droit actif.
4. Aucun remboursement ni transfert de ticket n’est prévu.
5. Le poids actif est le nombre de tickets actifs.
6. Une branche contient au plus un bloc par créneau.
7. Chaque bloc de production valide ajoute exactement une unité de score.
8. Clés et poids sont fixes pendant une époque.
9. Un ban ne retire aucun score passé.
10. Un ommer ajoute zéro score et zéro récompense.
11. Toute transition native et son undo sont atomiques.
12. Les frais transfèrent une ressource existante ; la récompense de bloc vaut zéro.
13. Aucun certificat applicatif ne modifie N.
14. Une empreinte Bitcoin n’ajoute ni score, ni priorité, ni finalité.
15. H1 peut suspendre une décision ; il ne choisit jamais un remplacement.
16. Une transaction réincluse avec les mêmes octets autorisés conserve son identité.
17. N sélectionne une chaîne ; il ne fusionne pas les blocs.
18. Aucun statut natif `FINAL` n’existe.
19. La référence optionnelle d’un burn M0 n’affecte jamais sa création monétaire.
20. À chaîne candidate, époque et contexte Bitcoin identiques, le registre et la graine sont identiques, indépendamment des observations locales antérieures.
21. Un checkpoint ne dispense pas de valider les règles historiques.
22. L’ancre persistante ne recule pas par une succession de rollbacks automatiques.
23. `UNKNOWN` n’est ni une absence, ni une invalidité, ni un risque nul.
24. Un `BOOTSTRAP` ne change jamais chaîne, ancre, registre ou rang d’un nœud ayant une origine locale.
25. Installer une release ne change pas cette propriété.
26. Une récupération exceptionnelle exige l’acceptation explicite de l’identifiant exact de sa nouvelle origine.
27. Aucun temps écoulé ne vaut approbation d’une nouvelle origine.
28. Une faible densité ne crée pas, à elle seule, une interdiction permanente de produire.
29. Une rotation ne soustrait pas une génération antérieure à une preuve d’équivoque encore recevable.
30. Une restauration non vérifiée ne réarme pas la signature.

---

## 2. Encodages et cryptographie

### 2.1 Entiers et listes

```text
U8(x)     : entier non signé, 1 octet
U16(x)    : entier non signé big-endian, 2 octets
U32(x)    : entier non signé big-endian, 4 octets
U64(x)    : entier non signé big-endian, 8 octets
U32LE(x)  : entier non signé little-endian, 4 octets
B32       : exactement 32 octets
V(x)      : U32(len(x)) || x
```

Liste d’éléments fixes :

```text
U32(nombre) || élément_0 || ... || élément_n−1
```

Liste d’éléments variables :

```text
U32(nombre) || V(élément_0) || ... || V(élément_n−1)
```

Les limites sont vérifiées avant allocation. Padding, débordements, champs terminaux inconnus et encodages alternatifs sont interdits.

Les calculs de montants, hauteurs et temps ne sont pas effectués modulo la taille de l’entier sérialisé.

Le tri lexicographique compare les octets non signés.

### 2.2 Domaines

```text
D(d, x) = U16(len(ASCII(d))) || ASCII(d) || x
H(d, x) = SHA256(D(d, x))
```

Aucun terminateur nul.

Les hashes Bitcoin sont les octets bruts du condensat ; leur affichage RPC inversé n’est pas leur représentation binaire dans N.

### 2.3 Engagement des listes

```text
ListRoot(d, []):
    return H(d + "/EMPTY", b"")

ListRoot(d, xs):
    leaves[i] = H(d + "/LEAF", U32(i) || V(xs[i]))
    return H(d + "/ROOT", U32(len(xs)) || Tree(d, leaves))

Tree(d, [x]):
    return x

Tree(d, xs), len(xs) > 1:
    p = plus grande puissance de deux strictement inférieure à len(xs)
    return H(d + "/NODE",
             Tree(d, xs[:p]) || Tree(d, xs[p:]))
```

Aucun dernier élément n’est dupliqué.

Pour `N/OBJECTS`, chaque élément vaut exactement :

```text
U16(type) || V(payload)
```

L’enveloppe extérieure du corps n’est pas engagée une seconde fois.

### 2.4 Suite active

Suite `1` :

- SHA-256 ;
- SHAKE256 pour la loterie ;
- secp256k1/ECDSA pour le contrôle ;
- ML-DSA-44 pur pour la production et les checkpoints.

```text
production_pk  = 1312 octets
production_sig = 2420 octets
```

Contexte ML-DSA exact, de onze octets :

```text
BATHRON/N/0
```

Le message signé est `D(d,payload)`, sans préhash applicatif supplémentaire.

ECDSA natif :

```text
r32 || s32
1 ≤ r < n
1 ≤ s ≤ n/2
```

Une clé secp256k1 comprimée DOIT encoder un point valide. Une suite inconnue est rejetée.

ML-DSA ordinaire ne protège pas les périodes passées après compromission d’une ancienne clé.

### 2.5 Profondeurs et temps

```text
depth_N(B,T) = T.height − B.height + 1
links_N(B,T) = T.height − B.height
```

Les confirmations incluent le bloc considéré.

```text
maxreorg = 1630 blocs déconnectés
links_N(B,T) ≥ 1630 ⇔ depth_N(B,T) ≥ 1631
```

Les liens restent utilisés pour `maxreorg`, la maturité des frais et certaines maturités d’objets. `maxreorg` est dérivé sous H_N (§3.3, §17) ; la maturité des frais et la protection des références restent à 2 880 liens, valeur supérieure ou égale à `maxreorg`.

**Le recul du cliché est exprimé en créneaux ; la règle A ajoute un compte de blocs dans une fenêtre fermée de la branche (§5.2).** Ces conditions sont distinctes. Un créneau vide ne vaut jamais une confirmation en blocs.

---

## 3. Manifeste et paramètres

### 3.1 Manifeste v6

```text
version:u16 = 6
chain_id:32
bitcoin_genesis:32
bitcoin_rules_id:32
application_spec_id:32
crypto_profile_id:32
T0_ms:u64
consensus_parameters: liste fixe de (id:u16, value:u64)
bootstrap_descriptor: V(bytes)
bootstrap_seal: V(bytes)
initial_application_state: V(bytes)
default_client_profile: V(bytes)
checkpoint_trust_policy: V(bytes)
conformance_bundle_id:32
```

```text
genesis_id = H("N/GENESIS", manifeste)
```

Les paramètres sont triés par identifiant, sans doublon. Tous les identifiants requis sont présents. Un identifiant inconnu exige une autre version.

Les documents engagés sont disponibles en octets canoniques.

`conformance_bundle_id` engage le paquet de conformité indépendant du genesis défini au §20.7. Il n’engage pas un paquet contenant récursivement ce manifeste final.

Un identifiant nul est interdit dans un manifeste activable.

### 3.2 Paramètres réseau

| ID | Paramètre | Valeur v0.7 |
|---:|---|---:|
| 1 | `P0`, sats par ticket | 1 000 000 |
| 2 | `k_ticket` | 30 |
| 3 | `k_seed` | 30 |
| 4 | `tau_ms` | **10 000** (décision, §17) |
| 5 | `L_epoch` | 14 400 |
| 6 | `seed_guard_seconds` | 43 200 |
| 7 | Ancien `k_reg` | Retiré, réservé |
| 8 | `k_ban` | 60 |
| 9 | `A_activity` | 144 |
| 10 | `F_activity` | 72 |
| 11 | `A_contest` | 30 |
| 12 | `F_contest` | 15 |
| 13 | `grace_react`, hauteurs BTC | 4 032 |
| 14 | `react_discount`, sats par droit suspendu | 250 000 |
| 15 | `react_full`, sats par droit suspendu | 1 000 000 |
| 16 | `prepare_admission` | 32 |
| 17 | `prepare_react` | 32 |
| 18 | `max_body`, octets | 262 144 |
| 19 | `max_objects` | 2 048 |
| 20 | `max_keyreg` | 16 |
| 21 | `max_rotations` | 8 |
| 22 | `max_ommers` | 16 |
| 23 | `max_evidence` | 8 |
| 24 | `ommer_horizon`, créneaux | 1 440 |
| 25 | `keyreg_fee`, unités atomiques M0 | 1 000 |
| 26 | `rotation_fee`, unités atomiques M0 | 1 000 |
| 27 | `swap_btc_depth` | 6 |
| 28 | `swap_max_span`, hauteurs BTC | 144 |
| 29 | `max_open_swaps` | 4 096 |
| 30 | `d_ref` | 6 |
| 31 | `btc_scan_chunk`, blocs BTC par lot | 144 |
| 32 | `k_admission_ref` | 60 |
| 33 | `activity_time_epochs` | 7 |
| 34 | `activity_min_samples` | 4 |
| 35 | `contest_time_epochs` | 2 |
| 36 | `contest_min_samples` | 2 |
| 37 | `k_boot_commit` | 30 |
| 38 | `bootstrap_start_delay`, secondes | 3 600 |
| 39 | `max_bootstrap_keyregs` | 7 000 |
| 40 | `fee_maturity_links` | 2 880 |
| 41 | `G_anchor`, hauteurs BTC | **26 280** |
| 42 | `anchor_cadence`, hauteurs BTC | **13 140** |
| 43 | `evidence_horizon`, créneaux | 14 400 |
| 44 | `exclusion_epoch_percent` | 2 |
| 45 | Ancien taux dégradé | Retiré, réservé |
| 46 | `exclusion_health_epochs` | 3 |
| 47 | `canonical_activity_numerator` | 1 |
| 48 | `canonical_activity_denominator` | 3 |
| 49 | `registry_stability_slots`, noté `K_reg` | **2 750** (dérivé, §17) |
| 50 | `exclusion_window_epochs` | **7** |
| 51 | `exclusion_window_percent` | **5** |
| 52 | `temporal_reference_depth_N` | **30** |
| 53 | `btc_slot_mtp_margin_seconds` | **7 200** |
| 54 | `registry_min_blocks`, noté `maxreorg` pour la règle A | **1 630** (dérivé, §17) |
| 55 | `slow_exclusion_window_percent` | **1** |
| 56 | `slow_silence_epochs` | **7** |

Les valeurs en gras hors H1 et hors IDs 4, 49 et 54 sont des choix de travail introduits par la v0.6, inchangés. Les IDs 4, 49 et 54 sont fixés par la v0.7 : `tau_ms` par décision du propriétaire, `K_reg` et `registry_min_blocks` par dérivation sous H_N (§17.4), avec arrondi vers le haut. Ils ne valent que dans ce domaine.

```text
anchor_depth = k_ticket = 30
temporal_minimum = 250000 sats
reward_per_block = 0

0 < anchor_cadence ≤ floor(G_anchor/2)
```

L’ID 31 borne un lot de calcul, jamais l’avance Bitcoin historique d’un bloc N.

Les IDs retirés ne figurent pas dans l’encodage v6.

### 3.3 Profil client v6

| ID | Paramètre | Valeur |
|---:|---|---:|
| 1 | `delta_clock_ms` | 500 |
| 2 | `Delta_nom_ms` | 1 000 |
| 3 | `future_tolerance_ms` | 1 000 |
| 4 | Première fenêtre de densité | 100 |
| 5 | Seconde fenêtre de densité | 1 000 |
| 6–7 | `rho_min` | 7/10 |
| 8 | Retard N maximal, créneaux achevés | 3 |
| 9 | Retard BTC maximal face à la cible profonde | 2 |
| 10 | Alerte sans nouveau bloc BTC, secondes | 7 200 |
| 11 | Marge avant échéance BTC | 12 |
| 12 | Première alerte REACT après `H_x` | 3 500 |
| 13 | Marge REACT urgente | 144 |
| 14 | Marge REACT critique | 32 |
| 15 | Monitoring REACT maximal, secondes | 86 400 |
| 16 | `k_default` | **77** |
| 17–18 | `beta_default` | 1/5 |
| 19–20 | `beta_delivery_max` | 1/5 |
| 21–22 | `alpha_budget` | 1/20 |
| 23 | `maxreorg` | **1 630** (dérivé, §17) |
| 24–26 | Anciens seuils d’âge et d’absence | Retirés, réservés |
| 27 | Exposition extérieure réelle au bootstrap, sats | **0** |
| 28 | Protection des références, liens N | 2 880 |
| 29 | Marge temporelle de travail pour l’analyse Bitcoin, secondes | 7 200 |
| 30 | Ancien délai de matérialisation des verrous | Retiré, réservé |
| 31 | Ouverture de signature, ms | 1 000 |
| 32 | Fermeture de signature, ms | 2 000 |
| 33 | Alerte d’égalité persistante, créneaux | 100 |
| 34 | Marge de production du repère BTC | 1 |
| 35 | `Q_B_work` | **256** |
| 36 | `M_work` | **14 400** |
| 37 | `D_btc`, confirmations du repère avant avancement d'ancre | **100** |
| 38 | Nombre minimal de canaux RELEASE initiaux distincts | **2** |

```text
bootstrap_admissibility_max_age = UNBOUNDED
bootstrap_useful_max_age_qualified = UNESTABLISHED
checkpoint_required_by_absence_duration = FALSE

policy_id = H("N/CLIENT/POLICY", encodage_du_profil)
```

Contraintes :

```text
future_tolerance_ms ≥ 2 × delta_clock_ms

(signature_close_ms − signature_open_ms)
    + Delta_nom_ms + 2 × delta_clock_ms < tau_ms

client.maxreorg = consensus.registry_min_blocks = 1630
reference_protection_links ≥ maxreorg      # 2880 ≥ 1630
fee_maturity_links ≥ maxreorg              # 2880 ≥ 1630
```

À `tau_ms = 10 000`, la deuxième contrainte vaut `1 000 + 1 000 + 2 × 500 = 3 000 < 10 000`. `Delta_nom_ms` est une valeur nominale de profil, pas la borne de délai de H_N : celle-ci est exprimée par la condition D = 0 et `p_late` (§17.2).

`k_default=77` est un seuil de laboratoire conservé pour comparaison, **sans borne de risque N associée**. Le dimensionnement antérieur sans avance privée est retiré. `Q_B_work=256` reste une borne de campagne, pas une propriété démontrée de Bitcoin (§15). Tout profil revendiquant une borne doit justifier l'avance, les choix de calendrier et le domaine de risque ; sinon `epsilon=UNKNOWN` et exposition extérieure nulle.

`registry_min_blocks` est un paramètre de consensus : une préférence locale de `maxreorg` NE DOIT PAS changer le registre. Le profil conforme ci-dessus impose leur égalité ; un profil divergent ne revendique pas les mêmes propriétés d'adoption.

### 3.4 Discriminant réseau

```text
network_tag = SHA256(chain_id)[0:4]
```

Deux réseaux utilisant le même genesis Bitcoin NE DOIVENT PAS partager ce discriminant dans le profil de déploiement.

M0 v3 et TICKET utilisent le même registre publié de discriminants. Quatre octets ne constituent pas une preuve universelle d’absence de collision.

---

## 4. Identités, tickets et burns

### 4.1 Identité

```text
IID = H(
    "N/ID",
    chain_id ||
    U16(1) ||
    control_pk33 ||
    initial_production_pk1312 ||
    nonce32
)
```

La clé de contrôle est immuable. Une rotation de production ne modifie pas IID.

Chaque identité conserve KEYREG, générations de production, tickets, droits, opérations préparées, activité, exclusions et preuves de ban.

Perdre la clé de contrôle empêche les opérations l’exigeant. Perdre la clé de production empêche aussi la rotation ordinaire, qui exige l’ancienne signature.

**REACT ne récupère aucune clé perdue.**

### 4.2 KEYREG

| Offset | Taille | Champ |
|---:|---:|---|
| 0 | 2 | version `3` |
| 2 | 2 | suite `1` |
| 4 | 32 | chain_id |
| 36 | 33 | control_pk |
| 69 | 1 312 | initial_production_pk |
| 1 381 | 32 | nonce |
| 1 413 | 32 | fee_receipt_id |
| 1 445 | 64 | control_pop |
| 1 509 | 2 420 | production_pop |
| **Total** | **3 929** | |

Avec `K = objet[0:1445]` :

```text
control_pop    = ECDSA(H("N/KEYREG/CONTROL", K || IID))
production_pop = MLDSA(D("N/KEYREG/PRODUCTION", K || IID))
```

Le reçu engage réseau, IID, opération et montant. Il est consommé une fois et préexiste, ou résulte d’un objet applicatif antérieur du même bloc.

Une clé de production attribuée à un IID ne peut jamais servir à un autre IID.

Seuls les KEYREG du descripteur initial sont exemptés des frais de bootstrap.

### 4.3 TicketID

```text
TicketID = chain_id32 || txid_raw32 || U32LE(vout)
```

Taille : **68 octets**.

Un outpoint ne crée qu’un ticket, même si son montant dépasse `P0`.

### 4.4 Sortie TICKET

```text
ASCII "BTK0"     4 octets
kind            1 octet
network_tag     4 octets
IID            32 octets
reference      32 octets
```

```text
01 = NEW
02 = ADD
03 = REACT
```

Script exact :

```text
6a 49 <73 octets>
```

Taille : **75 octets**.

`04` n’est pas reconnu. Aucun `ANCHOR` n’existe.

Une transaction comportant au moins deux sorties dont le premier push décodable commence par `BTK0` n’accorde aucun droit ni empreinte TICKET. Cette reconnaissance précède les contrôles de longueur, réseau, minimalité et financement.

Une coinbase n’accorde aucun droit.

### 4.5 Authentification Bitcoin

L’entrée zéro :

1. dépense un P2WPKH natif correspondant à `HASH160(control_pk)` ;
2. présente la clé comprimée attendue ;
3. porte une signature Bitcoin valide avec `SIGHASH_ALL = 01`, sans `ANYONECANPAY`.

Prevout, montant, script et témoin sont vérifiés.

D’autres entrées peuvent financer les frais. La clé de contrôle peut rester hors ligne.

### 4.6 NEW et ADD

NEW et ADD achètent chacun un ticket pour au moins `P0`. Leur distinction exprime une intention, pas des droits différents.

La référence désigne un bloc dont le préfixe contient KEYREG, ou `bootstrap_ref` dans les cas strictement définis au §5.6.

Pour `bootstrap_ref`, seuls sont admissibles :

- l’unique NEW de préengagement retenu par la règle du §5.6 ;
- les NEW/ADD inclus dans `[h_start,h_end]`.

Toute autre utilisation de `bootstrap_ref`, notamment après `h_end`, donne `REJECTED_REFERENCE`. L’exception du préengagement ne s’étend à aucun autre burn hors fenêtre.

Dans le préfixe référencé, KEYREG existe et IID n’est pas banni.

| État à l’activation | Effet |
|---|---|
| Admissible, non exclue | Ticket actif |
| Exclue | Ticket dormant |
| Bannie | Aucun droit utilisable |

ADD ne réactive pas une identité exclue. L'activité sanctionne **l'identité entière**, sans cohortes de tickets. NEW/ADD vers une identité déjà active, SUSPECT ou QUEUED conserve exactement activation, reset, fenêtres, suspicion et position de file. Aucun achat n'efface le passif. Si l'identité est encore QUEUED après le lot d'exclusions, les nouveaux tickets deviennent actifs avec ce passif et seront suspendus avec les autres lors d'une exclusion ultérieure. Si elle vient d'être exclue dans cette transition, ils deviennent dormants, hors `k_x`. Cette règle vaut aussi pour NEW visant une identité existante.

### 4.7 Premier examen

Une inclusion Bitcoin à hauteur `b` devient mûre lorsque le repère atteint :

```text
b + k_ticket − 1
```

Le premier examen intervient dans le premier bloc qui scanne l'événement mûr (§4.8), contre l'état et l'ascendance complète du **parent**, sans utiliser les objets de ce bloc pour rendre sa propre référence recevable.

| Type | Prédicat historique de référence |
|---|---|
| NEW/ADD ordinaire | `reference` est un bloc de l'ascendance du parent, à au moins `k_admission_ref=60` confirmations inclusives ; son préfixe contient le KEYREG et un IID non banni |
| NEW/ADD pré-genesis | Exception exhaustive du §5.6, sans profondeur N fictive |
| REACT | `reference=x` identifie le dossier exact reconstruit dans l'histoire du parent ; même IID, dossier courant non consommé, identité EXCLUDED non bannie ; son premier bloc matérialisant `F_x` est dans l'ascendance du parent à au moins 60 confirmations |

Pour REACT, vérifier aussi le hash `x`, tous les champs du dossier, le prix à la hauteur Bitcoin d'inclusion et l'absence de réservation par une REACT antérieure admissible. Le repère de `A_e` détermine le prix ; **`x` n'est pas un bloc et sa profondeur n'est jamais calculée**. Une identité déjà réservée n'accepte pas une seconde REACT ; prix insuffisant ou référence rejetée ne réserve rien.

Données nécessaires indisponibles : `MISSING_DATA`, sans classification terminale. Données complètes mais prédicat faux : `REJECTED_REFERENCE` (ou rejet de montant pour prix insuffisant). Les rejets et réservations sont rejoués après rollback. G7 est une discipline de portefeuille distincte, jamais une lecture de l'ancre locale dans la validité historique.

Le rejet est terminal dans cette histoire. Un rollback du premier examen permet son recalcul.

Un ticket brûlé vers une branche abandonnée peut être perdu sans remboursement. L’API et le portefeuille DOIVENT le signaler.

### 4.8 Scan et préparation

Ordre Bitcoin :

```text
(hauteur, index_transaction, vout)
```

Traitement idempotent par outpoint. Les rejets ne consomment pas les quotas de préparation.

Deux FIFO distinctes :

- NEW/ADD ;
- REACT.

Chaque bloc prépare le maximum disponible, jusqu’à 32 tickets et 32 droits REACT. Une REACT peut être préparée sur plusieurs blocs ; son activation reste indivisible.

Curseurs, classifications, réservations et files sont réorganisables.

Le scan alimente séparément registre, importation monétaire, index temporel et paiements applicatifs.

Un rejet d’admission ne supprime pas nécessairement une empreinte temporelle admissible.

### 4.9 Burn M0 v3

M0 v3 autorise une référence optionnelle de 32 octets à un `block_id`.

Selon la forme monétaire, un payload de 29 ou 30 octets devient **61 ou 62 octets**. La spécification applicative définit les formes exactes.

1. La création M0 dépend uniquement de l’admissibilité monétaire.
2. Une référence absente, inconnue ou perdante ne bloque pas cette création.
3. L’usage temporel exige au moins 250 000 sats.
4. La référence résout vers un bloc vérifiable de la branche examinée.
5. Les profondeurs temporelles du §12.2 s’appliquent.
6. Aucun ticket, score ou droit de canonicité n’en découle.

Le plancher est un filtre d’indexation, pas une borne générale de coût net d’attaque : le burn monétaire ouvre un droit M0.

### 4.10 Gel conjoint

Le corpus fournit les octets exacts, discriminants, règles de sorties multiples, conversions, identités uniques d’importation et autorisations.

Les prédicats sont séparés :

```text
MonetaryBurnValid
TemporalReferenceValid
```

Pour un même burn monétairement admissible, référence absente, inconnue, sur A ou sur B produit le même droit monétaire.

Un mauvais réseau produit zéro droit et zéro empreinte sur le réseau examiné.

Toute divergence entre parseurs sur le réseau, l’importation ou les sorties multiples interdit le gel.

---

## 5. Époques, registre et graines

### 5.1 Créneaux

```text
start_ms(s) = T0_ms + s × tau_ms
epoch(s) = s // L_epoch
```

L’époque `e` contient :

```text
[e × L_epoch, (e+1) × L_epoch − 1]
```

Un bloc n’est pas obligatoire à une frontière.

Les époques sont des intervalles mécaniques de registre et de calendrier. Aucun vote ne décide de leur transition.

Conséquence de `tau_ms = 10 000`, sans changement de `L_epoch` : une époque de 14 400 créneaux dure **40 heures** (144 000 s), contre 24 heures à 6 s. Toutes les fenêtres exprimées en créneaux ou en époques (activité et contestation, voie lente, plafonds d'exclusion, `ommer_horizon`, `evidence_horizon`, fenêtres de densité) conservent leur valeur et voient leur durée multipliée par 10/6. L'horizon de 10 ans de H_N compte `E = ⌈10 ans / 40 h⌉ = 2 192` époques.

### 5.2 Cliché ancien et règle A par branche

Pour `e ≥ 1` :

```text
freeze_slot(e) = (e−1) × L_epoch       # repère du calendrier de graine
snapshot_cut(e) = freeze_slot(e) − K_reg
K_reg = 2750 créneaux
raw_support(C,e) = dernier bloc de C avec slot < snapshot_cut(e),
                   ou genesis si aucun ; genesis si snapshot_cut(e) ≤ 0
A_0(C) = genesis
```

« Coupure de cliché » désigne uniquement `snapshot_cut`. Le repère `freeze_slot` n'est pas un verrou. Le cliché brut précède nominalement le début de l'époque de `(K_reg + L_epoch) × τ = 17 150 × 10 s = 171 500 s`, soit **47 h 38 min** au moins.

La fermeture de la fenêtre DOIT être objective. Soit `m_e=height(S_e)+k_seed−1` dans la branche Bitcoin vérifiée. `B_m(C,e)` est le **premier bloc de C dont le repère contient cette maturité**, genesis compris. On définit :

```text
seed_maturity(e,C) = slot(B_m(C,e))
window_blocks(C,e) = nombre de blocs de production de C tels que
    snapshot_cut(e) ≤ slot ≤ seed_maturity(e,C)

A_e(C) = raw_support(C,e), si window_blocks(C,e) ≥ registry_min_blocks
         A_(e−1)(C),       sinon
```

Dans l'intervalle `[snapshot_cut(e), seed_maturity(e)]` du mandat, la borne finale est ainsi une **maturité engagée sur la branche**, pas une heure locale de réception Bitcoin, ni une preuve du premier instant mondial de révélation. Les deux bornes sont inclusives pour le compte ; le support brut reste strictement avant la borne gauche. Genesis ne compte jamais comme bloc de production. Le bloc fermant la fenêtre compte une fois. Les blocs ultérieurs n'en changent jamais le compte sur une extension ; une autre branche recalcule sa propre fenêtre. La rétention de repères avant fermeture fait partie du grinding à analyser, pas d'une hypothèse de sûreté cachée.

Pour valider le premier bloc engageant `m_e`, établir d'abord son parent, son créneau et son repère, puis compter les blocs jusqu'à cet en-tête, dériver le registre, et enfin vérifier loterie, racine, signature et corps. Le compte n'utilise ni sa signature ni ses opérations ; celles-ci sont postérieures au cliché. Aucune auto-justification par une opération du bloc n'est possible. Un en-tête échouant ensuite est entièrement rejeté, compte compris.

Sans bloc engageant encore `m_e`, la fenêtre est ouverte : aucune nouvelle valeur définitive de `R_e` n'est installée. La production prépare un en-tête au créneau courant avec le repère prescrit au §8.4, ferme la fenêtre dans cette candidate et dérive `R_e` avant de signer. **Un compte insuffisant impose l'héritage ; il n'interdit jamais la production.** Le même calcul s'applique aux époques sautées : leur premier porteur de maturité peut être le bloc de reprise. Aucun bloc d'une époque `e` ne peut précéder son propre porteur de maturité, puisque sa validation exige déjà cette maturité.

Le support est monotone sur une branche : la coupure brute avance et un échec du seuil conserve le précédent support. `R_0` vient du bootstrap. Pour `e ≥ 1`, rejouer les transitions autorisées par `A_1…A_e` ; chaque opération est consommée au plus une fois. Si le support ne change pas, appliquer §5.9.

L'ancienneté en créneaux et la règle A ne confèrent aucune finalité locale. Une adoption autorisée peut remplacer support et registre de la même époque. Aucun registre engagé n'est une seconde ancre. La protection en blocs du §9.6 n'est pas une protection équivalente en temps. D + A vise à réduire l'exposition ; l'accord exige encore `CP_reg` (§5.7.2, §23.4).

### 5.3 Registre actif

Entrées triées par IID :

```text
IID:32
control_pk:33
key_seq:u64
production_pk:1312
weight:u64
tickets: weight × TicketID68, triés
```

```text
registry_root =
    H("N/REGISTRY", U32(nombre_identités) || entrées)
```

`weight > 0` et égale le nombre de tickets. Un ticket ne figure qu’une fois.

Les droits dormants et suspendus, fenêtres d’activité, files et dossiers appartiennent à l’état de contrôle complet.

Deux supports différents peuvent produire le même registre. Une égalité de racine de registre ne prouve pas une égalité des états de contrôle.

### 5.4 Graine

```text
MTP(B) = médiane Bitcoin des timestamps de B et de ses dix prédécesseurs
```

Aux premières hauteurs, la convention Bitcoin de médiane supérieure s’applique.

Pour `e ≥ 1` :

```text
freeze_time(e) = start_ms(freeze_slot(e)) // 1000
seed_time(e) = freeze_time(e) + seed_guard_seconds
```

`S_e` est le premier bloc, depuis le point Bitcoin initial engagé, satisfaisant :

```text
MTP(S_e) ≥ seed_time(e)
```

Le repère N contient `S_e` à au moins `k_seed` confirmations.

```text
seed_e = H(
    "N/SEED",
    chain_id ||
    U16(1) ||
    U64(e) ||
    U32(height(S_e)) ||
    hash_raw(S_e) ||
    registry_root(R_e)
)
```

La même formule s’applique à `e=0` avec `S_0` et `R_0` définis par le bootstrap.

Aucun parent N, état applicatif, objet, signature ou nonce de producteur n’entre directement dans la graine.

### 5.5 Disponibilité et attributions

Aucune graine de remplacement.

Un créneau vide est attribué seulement si un bloc antérieur de la branche, ou genesis, engage déjà la maturité de `S_e`.

Un créneau rempli par un bloc valide est attribué à son producteur, même si ce bloc engage le premier cette maturité.

Aucune attribution rétroactive des créneaux antérieurs.

Un manque local de données produit `UNKNOWN` ; il ne modifie pas les attributions d’une branche complète.

### 5.6 Bootstrap du réseau

Descripteur pré-genesis :

```text
version:u16 = 6
chain_id:32
bitcoin_genesis:32
bitcoin_rules_id:32
application_spec_id:32
crypto_profile_id:32
consensus_parameters
default_client_profile:V(bytes)
checkpoint_trust_policy:V(bytes)
initial_btc_height:u32
initial_btc_hash:32
h_start:u32
h_end:u32
initial_application_state_hash:32
initial_keyregs: liste fixe de KEYREG3929, triés par IID
```

```text
bootstrap_ref = H("N/PREGENESIS", descripteur)
```

Le descripteur est publié et authentifié avant préengagement.

Le préengagement est un NEW ordinaire au prix `P0`, visant un KEYREG initial et `bootstrap_ref`.

Le premier NEW admissible dans l'ordre Bitcoin depuis le point initial est retenu s'il satisfait la condition ci-dessous. Sinon le descripteur échoue : aucun NEW suivant n'est essayé comme remplacement ; les suivants sont nécessairement au moins aussi tardifs.

```text
commit_height + k_boot_commit − 1 < h_start
```

Le registre initial comprend exactement :

1. ce ticket de préengagement ;
2. tous les NEW/ADD admissibles de `[h_start,h_end]` visant les KEYREG initiaux et `bootstrap_ref`.

Le préengagement compte une fois. REACT est interdit au bootstrap.

Aucun sous-ensemble de burns n’est choisi après révélation de la graine.

```text
h_mature = h_end + k_ticket − 1
t_end = MTP(BTC[h_mature])
```

`S_0` est le premier bloc satisfaisant :

```text
height(S_0) > h_mature
MTP(S_0) ≥ t_end + seed_guard_seconds
```

```text
g_ref_height = height(S_0) + k_seed − 1
seal_height = g_ref_height + d_ref

T0_ms =
    ceil_to_multiple(
        1000 × (MTP(BTC[seal_height]) + bootstrap_start_delay),
        tau_ms
    )
```

Scellement de **184 octets** :

```text
commit_txid:32
commit_vout:u32
commit_height:u32
h_mature:u32
seed0_height:u32
seed0_hash:32
genesis_btc_ref_height:u32
genesis_btc_ref_hash:32
seal_height:u32
seal_hash:32
```

**Le manifeste final n’est instancié, signé et distribué qu’après calcul complet de ce scellement et de `T0_ms`.** Le descripteur pré-genesis n’est pas le manifeste final.

L’état applicatif initial doit être constructible sans dépendre circulairement du futur `genesis_id`. Tout solde positif satisfait G1–G3.

La publication de lancement indique :

- le poids initial obtenu ;
- sa concentration ;
- le poids initial minimal visé ;
- les dépendances administratives ;
- les hypothèses de poids adverse.

Aucun seuil de poids initial ne prouve à lui seul l’honnêteté du registre. L’exposition extérieure reste nulle tant que la qualification ne permet pas de la relever.

Le préengagement n’interdit pas de préengager plusieurs projets puis d’en abandonner certains. Cette possibilité est publiée.

### 5.7 Préfixe commun et suppression des verrous

#### 5.7.1 Règle de dérivation

```text
DeriveRegistry(C, e):
    require complete historical inputs needed for A_e(C)
    establish the maturity closure and count as specified in 5.2
    # current header is validated after derivation, before installation
    replay epoch transitions in increasing order
    use only branch facts authorized by each snapshot
    return R_e(C), control_state_e(C), support_id=A_e(C).id
```

Le cache est indexé au minimum par :

```text
rules_id
epoch
support_id
previous_control_state_commitment
window_closure_context_and_count
```

Un cache n’est pas une contrainte d’adoption. Il peut être supprimé puis reconstruit.

Un nœud hors ligne dérive les registres des époques manquées depuis la candidate reçue, exactement comme un nœud ayant conservé tous les blocs.

Il NE DOIT PAS les dériver de sa pointe ancienne en prétendant que celle-ci représentait les coupures manquées.

#### 5.7.2 Hypothèse de préfixe commun

Fixer `X=(rules_id, origine de confiance, faits Bitcoin pertinents)`. X NE DOIT PAS inclure le registre ni la graine finale qui l'engage. RECOVERY accepté ouvre un nouveau contexte ; recevoir BOOTSTRAP sur une origine locale ne le change pas.

`P_j(C)` est le préfixe complet, genesis inclus, jusqu'à `A_j(C)`. `D_e(C)=(P_0,…,P_e)` comprend contenus de contrôle et ordre, pas seulement poids ou hauteurs.

```text
C6 — Stabilité conditionnelle :
  epoch(u)=epoch(v)=e ∧ X(u)=X(v) ∧ D_e(C_u)=D_e(C_v)
  ⇒ R(u)=R(v) ∧ Control(u)=Control(v) ∧ Calendar(u)=Calendar(v)
```

`u` est un engagement honnête (signature ou adoption d'un bloc utilisant e) ; `v` est un autre engagement ou une installation de registre par adoption, y compris chez le même nœud. Les métadonnées d'audit de fermeture de fenêtre peuvent différer : `Control` désigne l'état opérationnel qui gouverne les transitions, non ces diagnostics.

C6 est un lemme de déterminisme par induction sur les transitions, **pas un théorème de consensus**. L'obligation séparée est :

```text
CP_reg(e,X) : tous les engagements et installations honnêtes pertinents
              de (e,X) partagent le même D_e
H_N ⇒ Pr[∃ e,X dans l'horizon qualifié : ¬CP_reg(e,X)] ≤ epsilon_CP
C6 ∧ CP_reg ⇒ accord et immutabilité des registres concernés
```

`H_N` DOIT fixer délais sur toutes les fenêtres pertinentes, horloges, disponibilité, poids adverses dynamiques, corruptions, Bitcoin, rétention, grinding et horizon. La borne couvre l'événement global ou compose explicitement ses bornes par époque. Un préfixe commun à un instant ne garantit pas sa conservation future. Le compte de la règle A et une densité observée ne prouvent pas CP_reg.

**État de l'analyse en v0.7.** Le domaine H_N est publié au §17. L'analyse propre à N existe **sous H_N** et compose explicitement ses bornes par époque (`etudes/n-spec/cp-reg/derivation/DERIVATION-K.md` §5) :

```text
ε_ep ≤ T_fix + T_court + T_profond + T_CG              # par époque
K_inst = K_reg + G(τ),  G(τ) = ⌈(seed_guard − marge MTP)/τ⌉ = 3 600 créneaux
epsilon_CP(10 ans) = E × Q_B × ε_ep,  E = 2 192,  Q_B = 1
avec K_reg = 2 750 et registry_min_blocks = 1 630 :
    epsilon_CP ≈ 4,6 × 10⁻¹⁰ ≤ ε_H = 10⁻⁹               # dérivation conditionnelle
```

| Terme | Événement couvert | Statut |
|---|---|---|
| `T_fix` | Voie (i) : violation de préfixe commun à la coupure fixe `snapshot_cut`, sur `K_inst` créneaux | DP analytique exacte (Opus), réduction `p_late` analytique sous H_late ; au-delà de 10⁻¹⁴ **extrapolée** |
| `T_profond`, `T_court` | Voie (ii) : pivot unifié, profond et peu profond (robustesse du compte de règle A) | Union analytique **esquissée sous hypothèses**, à relire ; pivot profond confirmé comme exécution atteignable en TLA+ (témoins), sans PASS exhaustif |
| `T_CG` | Nœuds synchronisés : une réorganisation profonde est convertie en `HALTED_DEEP_REORG` par `maxreorg` | Analytique (binomiale + avance stationnaire) |
| ε_U, ε_post | Nœud nouveau ou de retour capté par une branche privée changeant de calendrier | **Hors domaine** par décision (D1, §12.15) ; non borné |

Cette garantie est **conditionnelle et dérivée, pas un théorème clos**. Elle ne vaut que si toutes les hypothèses du §17 tiennent sur tout l'horizon. Restent ouverts, sans être levés par cette version :

1. l'écart DP / Monte-Carlo d'un facteur 1,3 à 1,8 sur K, structurel et non expliqué ; la DP, conservatrice, est publiée ;
2. `Q_B = 256` (grinding de graine Bitcoin) n'est pas qualifié ; avec les valeurs ci-dessus, la composition donne ≈ 1,5 × 10⁻⁷ sur 10 ans à `Q_B = 256`, hors de la cible ;
3. l'exploration TLA+ stricte du pivot profond (`MC_explore_sync_PivotDeep`) est **INCOMPLET** ; seuls des témoins (replays, exploration restreinte ou semi-dirigée) existent ;
4. `p_late ≤ 10⁻²` par fenêtre de K créneaux et l'hypothèse H_late ne sont **pas certifiés par le banc** : le banc mesure des livraisons reçues, pas la réception par tous les honnêtes ni une borne par fenêtre ;
5. la compatibilité des ancres A4 n'est pas requalifiée par cette version ; `registry_min_blocks = 1 630 ≥ K_blocs(10⁻¹²) = 1 508` borne seulement la divergence en blocs à la profondeur de `Nbound`, pas les cas de partition ou de réorganisation Bitcoin.

Hors de H_N, ou pour ces points ouverts, N NE DOIT PAS être présenté comme garantissant l'immutabilité des registres. Aucun théorème d'un autre calendrier de consensus n'est importé.

#### 5.7.3 Revalidation et adoption

Une candidate peut avoir un registre différent parce qu’elle possède un autre préfixe.

Cette différence :

- n’est pas une invalidité historique si la dérivation de la candidate est correcte ;
- n’est pas un motif autonome d’arrêt local ;
- n’autorise pas à contourner l’ancre, le rang ou les restrictions Bitcoin.

Si la candidate est adoptable, ses états de contrôle remplacent atomiquement ceux du suffixe retiré.

Un registre mémorisé ne devient jamais une seconde ancre.

Un engagement passé n'est ni condition supplémentaire de validité historique, ni veto d'adoption ou de signature. Les réservations du §7.4 restent obligatoires. Chaque changement par adoption expose époque, anciens et nouveaux supports et registres ; ces diagnostics ne participent pas à la sélection.

#### 5.7.4 Ordre empêchant une justification circulaire

Pour examiner une candidate :

1. lire l’origine, l’ancre et la mémoire Bitcoin **avant** l’examen ;
2. valider l’ascendance et les faits Bitcoin ;
3. dériver ses supports et registres sans mutation de l’état adopté ;
4. exécuter la sélection du §9 ;
5. contrôler la candidate contre les protections lues à l’étape 1 ;
6. persister l’adoption complète, si elle est autorisée ;
7. avancer ensuite l’ancre selon le §9.6.

Une ancre avancée à l’étape 7 ne peut pas servir à autoriser rétroactivement l’étape 5.

La profondeur temporelle du cliché reste une règle historique de dérivation ; elle n’est pas une assertion administrative de finalité.

### 5.8 Anti-grinding

L’analyse distingue quatre choix possibles :

1. choix du préfixe N déterminant le registre ;
2. choix du bloc Bitcoin servant de graine ;
3. choix du moment et de l’avance d’une attaque ;
4. choix administratif d’une origine initiale.

Pour un préfixe commun fixé et une époque donnée :

```text
R_e est unique
Q_reg = 1 conditionnellement à ce préfixe
```

`Q_reg=1` est strictement conditionnel : il ne borne pas les préfixes que l'adversaire peut rendre adoptables. L'analyse DOIT traiter ce nombre séparément ; une course à registre fixe ne remplace pas CP_reg à registre variable. La règle A ne démontre pas `Q_reg=1` mondial.

Si l’adversaire peut faire accepter plusieurs préfixes de cliché, cette condition échoue. Le nombre de registres ou de chemins accessibles doit alors être inclus dans l’analyse adversariale ; il ne peut être ignoré.

La séparation temporelle nominale entre borne du cliché et seuil de graine est :

```text
K_reg × tau_ms/1000 + seed_guard_seconds
= 2750 × 10 + 43200
= 27500 + 43200
= 70700 secondes
```

Avec la marge temporelle de travail et l’incertitude d’horloge :

```text
70700 − 7200 − 1 = 63499 secondes
```

En v0.6 (τ = 6 s, K_reg = 7 200), ces valeurs étaient 86 400 s et 79 199 s. La baisse vient de la dérivation de `K_reg` ; la garde de graine, exprimée en secondes, est inchangée.

Cette marge n’est pas une preuve d’imprévisibilité du hash Bitcoin. MTP, rétention, minage privé et manipulation des timestamps restent dans le modèle de biais.

La garde de douze heures est conservée intégralement. Elle ne dépend pas du remplissage de l’époque.

Le hash de `A_e` n’est pas ajouté à la graine : des variantes de contenu sans changement du registre ne doivent pas offrir un nonce supplémentaire.

Les variantes modifiant admissions, clés, activité ou exclusions avant le cliché restent une surface de grinding si la propriété de préfixe commun échoue.

### 5.9 Faible densité et reprise

La règle A peut reporter l'avancement du support pendant plusieurs époques consécutives ; elle ne conditionne pas l'autorisation de produire au succès de son seuil. La production NE DOIT PAS exiger :

```text
links_N(A_e, tip) ≥ maxreorg
```

Elle NE DOIT PAS exiger que l’époque précédente contienne un nombre minimal de blocs.

Pour une chaîne donnée :

```text
si A_e = A_(e−1) :
    conserver le registre et l’état de contrôle opérationnel ;
    ne pas rejouer les observations déjà traitées ;
    ne pas consommer une seconde fois les opérations ;
    ne pas exécuter une nouvelle vague d’exclusions ;
    dériver néanmoins la graine propre à e lorsqu'elle est mûre ;
    inscrire W_f(e)=poids hérité et excluded(e)=0 dans le journal de quotas.
```

L’époque et les métadonnées de dérivation avancent. Le poids ne décroît pas par le seul passage du temps.

Si `A_e` avance, seules les nouvelles informations autorisées sont traitées, une fois ; §6.6 fixe les deux voies d'exclusion. Les époques calendaires sans avancement comptent dans les fenêtres de quotas, sans vague d'exclusion. Genesis initialise poids et contrôle sans observations ni exclusions. Lors d'un grand saut, chaque époque est rejouée dans l'ordre ; plusieurs époques vides ne créent ni confirmations fictives ni dette d'exclusions à exécuter d'un coup.

Après une époque de densité inférieure à 0,2, voire sans bloc, un producteur encore actif peut produire dans un créneau courant dès que :

- une candidate compatible est entièrement validée ;
- la graine de l’époque est mûre ;
- Bitcoin est réconcilié ;
- l’horloge et la réservation sont admissibles.

Le premier bloc peut apporter lui-même le repère Bitcoin contenant la maturité de cette graine.

Il n’est pas nécessaire de fabriquer des blocs intermédiaires ou d’attendre que des blocs impossibles à produire approfondissent le support.

La reprise de production est une vivacité locale, pas une preuve que le support hérité est commun. Le temps sans bloc NE DOIT PAS compter comme confirmations. Cette règle supprime le blocage circulaire de production. Elle ne garantit pas la reprise si tous les droits ont été bannis, toutes les clés perdues, les données détruites ou un conflit profond réel demeure.

---

## 6. Machine de contrôle

### 6.1 Transition d’époque

Lorsque le support avance :

1. reprendre l’état de contrôle précédent ;
2. identifier les opérations nouvellement admissibles dans le support ;
3. appliquer les bans ;
4. rejouer les nouvelles observations d’activité ;
5. fermer ou ouvrir suspicions et contestations ;
6. traiter les récupérations d’activité ;
7. calculer les quotas et appliquer les exclusions autorisées ;
8. appliquer les rotations ;
9. activer les NEW/ADD préparés ;
10. activer les REACT entièrement préparées.

L’ordre Bitcoin du §4.8 est conservé.

Une identité bannie ne participe plus à l’activité ni à la réactivation.

La première activation d'une identité et une REACT réinitialisent l'activité au début de l'époque d'activation, sans absence antérieure. NEW/ADD d'une identité déjà active ne réinitialise rien (§4.6) : son passif est celui de l'identité, applicable aussi au poids ajouté. Exclusions avant admissions : `k_x` n'inclut pas les tickets activés ou rendus dormants ensuite.

### 6.2 Observations consolidées

```text
activity_cutoff(e) = slot(A_e) − ommer_horizon
```

Pour genesis, aucune observation n’est disponible.

Le curseur est monotone sur une branche. Seuls les créneaux strictement postérieurs au curseur précédent et au plus égaux à la nouvelle borne sont rejoués.

Chaque attribution fournit :

```text
assigned ∈ {0,1}
canonical ∈ {0,1}
external_ommer ∈ {0,1}
activity = max(canonical, external_ommer)
```

Un ommer externe exige un porteur d’IID distinct.

Crédit plafonné à un par attribution. Les auto-ommers sont transportables mais sans crédit.

La consolidation laisse passer tout l’horizon d’inclusion des ommers avant de figer l’observation.

### 6.3 Présence

```text
Present(m,a,c) =
    (2 × a ≥ m)
    and
    (3 × c ≥ m)
```

Pour 144 attributions :

```text
a ≥ 72
c ≥ 48
```

Pour 30 attributions :

```text
a ≥ 15
c ≥ 10
```

L’absence d’activité dans une branche ne prouve ni une panne mondiale ni l’absence de censure.

### 6.4 Fenêtre normale exacte

État minimal par identité :

```text
state ∈ ACTIVE, SUSPECT, QUEUED, EXCLUDED, BANNED
activation_slot
reset_slot
activity_cursor
suspicion_slot
queue_slot
attribution_history
canonical_history
ommer_history
```

L’ancien nom `finalized_cursor` est abandonné au profit de `activity_cursor`.

À chaque créneau consolidé `s`, pour une identité ACTIVE :

1. ajouter l’observation éventuelle ;
2. si au moins 144 attributions sont strictement postérieures à `reset_slot`, prendre **les 144 dernières** de ces attributions ;
3. tester `Present` sur cette fenêtre glissante ;
4. sinon, examiner la fenêtre temporelle si elle est admissible.

La fenêtre temporelle est exactement :

```text
[s − 7×L_epoch + 1, s]
```

Elle doit être entièrement postérieure à l’activation et au dernier reset.

Elle ne s’applique que si :

```text
4 ≤ m < 144
```

Sous quatre attributions : `INSUFFICIENT_ASSIGNMENTS`.

La voie normale a priorité sur la voie temporelle.

Un succès en état ACTIVE **ne provoque pas de reset** : la fenêtre continue de glisser. À la 145e attribution, la première sort et la 145e entre.

Un échec ouvre une suspicion au créneau `s`.

### 6.5 Contestation et récupération en file

#### Contestation

Le créneau ouvrant la suspicion est exclu de la contestation.

Soient les trente premières attributions strictement postérieures à `suspicion_slot`.

- Dès que les observations accumulées atteignent 15 activités et 10 canoniques, la suspicion est annulée.
- À la trentième attribution, si ces seuils ne sont pas atteints, passage à `QUEUED`.
- Avant trente attributions, dès que deux époques de créneaux sont écoulées depuis la suspicion, examiner l’intervalle depuis la suspicion.
- Avec `2 ≤ m < 30`, `Present` annule la suspicion ; sinon mise en file.
- Sous deux attributions, continuer la contestation.

Après l’échéance temporelle, le test est répété à chaque nouvelle attribution tant que le minimum de deux n’a pas été atteint.

La clôture normale à trente attributions a priorité sur la clôture temporelle.

#### File

En état QUEUED, seules les observations strictement postérieures à `queue_slot` comptent.

La récupération utilise :

- les **trente dernières attributions** postérieures à `queue_slot`, dès qu’il y en a au moins trente ;
- sinon une fenêtre glissante de deux époques :

```text
[s − 2×L_epoch + 1, s]
```

entièrement postérieure à `queue_slot`, avec au moins deux attributions.

La voie de trente attributions a priorité.

Une récupération exige `Present`. Elle remet l’identité ACTIVE, fixe `reset_slot=s`, ferme suspicion et file, et réinitialise les fenêtres pertinentes.

Aucune nouvelle suspicion n’est ouverte au même créneau.

#### Ordre de frontière

Pour chaque créneau :

1. ajouter l’observation ;
2. traiter une contestation ou une file déjà ouverte ;
3. traiter les échéances temporelles ;
4. si l’identité était ACTIVE sans clôture au même créneau, tester la suspicion ;
5. avancer le curseur.

Toutes les récupérations révélées par le support sont traitées **avant** le lot d’exclusions de l’époque.

### 6.6 Exclusions : frein de densité et plafonds

Le frein limite l'attrition sous indisponibilité ; il NE DOIT PAS mettre à zéro tout progrès de contrôle au seul motif que la santé est sous 7/10.

#### Condition de santé

Après rejeu des observations et récupérations, avant exclusions, fixer `Q_e`, l'ensemble des identités encore QUEUED. Soit `c=activity_cutoff(e)` ; une époque historique j est entièrement couverte si `j≥0` et `(j+1)L_epoch−1 ≤ c`. Prendre les trois dernières telles époques, sans les remplacer par des périodes plus anciennes plus favorables.

Pour chacune, compter uniquement les créneaux attribuables selon §5.5 à une identité hors `Q_e`. Le numérateur compte les blocs canoniques de ces mêmes créneaux. Les ommers ne comptent pas. Les créneaux non attribuables sont exclus des deux comptes et publiés séparément.

```text
health_ok(e) = trois époques couvertes existent et, pour chacune,
               eligible_slots > 0 et 10×filled_eligible ≥ 7×eligible_slots
```

Le masque `Q_e` est fixe pour toute cette mesure ; aucune recomposition après chaque exclusion. Dénominateur nul ou moins de trois époques : frein actif. Le ratio n'est ni la densité de livraison du §14, ni une estimation du poids adverse. Un QUEUED reste dans la loterie tant qu'il n'est pas exclu, mais son abstention ne dégrade plus cette mesure.

Sous frein, les suspicions, récupérations, bans prouvés, admissions, rotations et REACT continuent. La **voie lente** ci-dessous DOIT être exécutée à chaque avancement de support. Aucun critère local de ciblage ne modifie le registre.

#### Voie lente

Une identité est éligible à cette voie si elle est QUEUED, possède au moins `activity_min_samples=4` attributions dans la fenêtre consolidée inclusive `[c−7L_epoch+1,c]`, entièrement postérieure à son activation/reset, et n'y possède **aucun en-tête signé admissible inclus dans la branche**, canonique ou ommer (y compris auto-ommer). Le test porte sur la branche complète, pas le gossip local. Un en-tête connu hors chaîne ne prouve pas sa disponibilité mondiale.

La voie lente partage les plafonds ordinaires et reçoit en plus un plafond de **1 % sur sept époques**, valeur de travail normative. Si `slow_used(e)` somme les poids exclus par cette voie aux époques `max(0,e−6)…e−1` :

```text
B_slow(e) = min(B(e), max(0, floor(W_base(e)/100) − slow_used(e)))
budget(e) = B(e) si health_ok(e), sinon B_slow(e)
```

Sous frein, parcourir seulement les QUEUED éligibles à la voie lente. En bonne santé, parcourir tous les QUEUED avec les plafonds ordinaires ; aucun second lot lent ne s'ajoute. Chaque exclusion lente compte aussi dans `used` et dans le plafond global de 5 %.

Ainsi une abstention maintenant la mesure sous 0,7 ralentit les exclusions sans les interdire lorsque support, silence, poids et quotas permettent un lot. Les rotations admissibles ne sont jamais conditionnées à `health_ok`. Cette garantie ne supprime ni le report de contrôle par la règle A, ni les arrondis nuls des petits registres, ni l'impossibilité d'exclure une identité indivisible trop lourde. Ces limites doivent rester visibles ; aucune purge universelle n'est promise.

La mesure porte sur des observations retardées : avec les valeurs nominales, l'effet peut attendre environ quatre à cinq époques, et davantage si la règle A reporte le support. Le délai exact vient de la borne c et des trois fins d'époque, jamais d'une horloge locale.

#### Plafonds

`W_f(e)` est le poids après bans, avant exclusions, admissions et REACT. Si le support est inchangé, inscrire le poids hérité et zéro exclusion (ordinaire et lente). Genesis a `W_f(0)=W_0`, zéro exclusion. La fenêtre compte les **époques calendaires**, y compris vides, et non les seules transitions avec nouveau support.

```text
B_epoch(e) = floor(2 × W_f(e) / 100)
```

Sur les sept époques de transition `e−6…e`, avec les époques négatives omises :

```text
W_base(e) = min W_f(j) sur cette fenêtre

used(e) =
    somme des poids effectivement exclus pour inactivité
    aux époques max(0,e−6)…e−1

B_window(e) =
    max(0, floor(5 × W_base(e) / 100) − used(e))
```

```text
B(e) = min(B_epoch(e), B_window(e))
```

Les plafonds sont prospectifs : tester le lot avant de l'exécuter. Un ban ultérieur diminuant W_base n'annule pas rétroactivement un lot antérieur valide ; il peut réduire le prochain budget à zéro. Les plafonds sont calculés avant admissions et REACT de l’époque. Les crédits ne sont pas accumulés au-delà de la fenêtre.

Aucun `max(1,…)` et aucune exception pour identité lourde ne permettent de dépasser ces bornes.

#### Parcours de file

Ordre :

```text
(queue_slot, IID)
```

```text
remaining = budget(e)

for i in queue_order:
    if i no longer QUEUED:
        continue

    if not health_ok(e) and not slow_eligible(i):
        continue

    if weight(i) > remaining:
        continue

    if excluding i would remove all remaining active weight:
        continue

    exclude i
    remaining -= weight(i)
```

Le parcours continue après une identité trop lourde.

Il n’y a pas d’exclusion partielle d’une identité.

Une identité trop lourde peut rester en file indéfiniment. Avec un petit registre, les arrondis peuvent interdire toute exclusion. C’est une limite explicite de cette politique prudente, pas une raison d’introduire une exception cachée.

Une faible densité peut ainsi se prolonger jusqu’au retour de producteurs ou à l’admission de nouveaux droits. Elle ne bloque pas la production ordinaire.

#### Limite de la protection

Les plafonds bornent la vitesse d’attrition ; ils ne prouvent pas que les identités exclues sont malhonnêtes.

Avec poids adverse inchangé et retrait d’une fraction `x` du poids initial exclusivement honnête :

```text
beta_after = beta_before / (1−x)
```

Pour `beta_before=0,20` et `x=0,05` :

```text
beta_after ≈ 0,210526
```

Des fenêtres successives peuvent cumuler l’attrition. L’analyse de risque DOIT intégrer `beta(t)` et les REACT/admissions ; elle ne peut réutiliser indéfiniment un β initial fixe.

### 6.7 Exclusion et REACT

Avant chaque exclusion :

```text
exclusion_serial += 1
```

```text
x = H(
    "N/EXCLUSION",
    chain_id ||
    U64(e) ||
    block_id(A_e) ||
    IID ||
    U64(exclusion_serial)
)
```

Dossier de **124 octets** :

```text
chain_id:32
epoch:u64
checkpoint_id:32
IID:32
exclusion_serial:u64
k_x:u64
H_x:u32
```

```text
H_x = A_e.btc_ref_height
```

`k_x` compte les droits actifs suspendus. Les tickets dormants acquis ensuite ne l’augmentent pas.

Le journal identifie `F_x`, premier bloc de la branche matérialisant l'exclusion. Pour une époque sans bloc, la matérialisation intervient au premier bloc suivant dont le rejeu incorpore cette transition ; le dossier reste calculé avec son époque et son support d'origine. Sa présence dans le parent et sa profondeur servent au premier examen REACT (§4.7).

Pour une REACT incluse à hauteur Bitcoin `b` :

```text
b ≤ H_x + 4032 : minimum = k_x × 250000
sinon          : minimum = k_x × 1000000
```

La référence TICKET REACT vaut `x`.

La première REACT admissible réserve le dossier. Une tentative insuffisante ne réserve rien.

Après préparation complète et activation :

- les droits suspendus sont restaurés ;
- les tickets dormants sont activés ;
- l’activité est réinitialisée ;
- le dossier est consommé.

Un ban est définitif. Une réorganisation Bitcoin peut faire perdre le tarif réduit ; aucun remboursement n’est prévu.

### 6.8 Monitoring REACT

Vérification au moins quotidienne, indépendante de la production.

Publication de :

- suspicion, file, exclusion, `x`, `k_x`, `H_x` ;
- tarif courant et échéance ;
- protection G7 ;
- alerte à `H_x+3500` ;
- alertes à 144 puis 32 blocs de la borne ;
- perte de monitoring et réorganisation.

Sous 32 blocs de marge, le portefeuille propose le tarif plein par défaut.

`grace_react` est mesurée depuis le repère ancien de A_e, **pas depuis la notification**. Après interruption, elle peut être déjà expirée à la matérialisation ; l'API affiche immédiatement le tarif plein, sans promettre 4 032 hauteurs de délai effectif. G7 peut encore retarder l'envoi. Une réorganisation du support peut changer x et perdre une REACT déjà brûlée ; aucune racine de registre ne remplace son engagement d'histoire.

### 6.9 ROTATE

| Offset | Taille | Champ |
|---:|---:|---|
| 0 | 2 | version `3` |
| 2 | 2 | suite `1` |
| 4 | 32 | chain_id |
| 36 | 32 | IID |
| 68 | 8 | old_key_seq |
| 76 | 8 | new_key_seq |
| 84 | 32 | previous_rotation_id |
| 116 | 32 | checkpoint_id |
| 148 | 1 312 | new_production_pk |
| 1 460 | 32 | fee_receipt_id |
| 1 492 | 64 | control_signature |
| 1 556 | 2 420 | old_production_signature |
| 3 976 | 2 420 | new_production_pop |
| **Total** | **6 396** | |

Avec `ROT=objet[0:1492]` :

```text
contrôle : H("N/ROTATE/CONTROL", ROT)
ancienne : D("N/ROTATE/OLD", ROT)
nouvelle : D("N/ROTATE/NEW", ROT)

new_key_seq = old_key_seq + 1
rotation_id = H("N/ROTATE/ID", objet_complet)
```

Génération initiale zéro. Nouvelle clé inutilisée. Le bloc référencé contient la génération concernée.

La première succession admissible réserve cette génération.

La rotation prend effet dans un registre ultérieur. Elle ne réactive pas une identité exclue et n’annule pas les preuves concernant une génération antérieure.

### 6.10 Registre vide

Si `W_e=0` :

```text
HALTED_EMPTY_REGISTRY
```

Aucun producteur de secours, vote ou promotion d’observateur.

Lecture, validation et calcul des transitions futures déjà déterminées continuent. Si ces transitions restaurent `W>0`, la reprise est mécanique.

Un nœud ne peut pas inclure de nouveaux KEYREG ou REACT sans bloc.

Les exclusions ordinaires ne doivent pas vider le registre. Les bans, pertes de clés ou défauts de disponibilité peuvent néanmoins supprimer toute capacité effective de production.

Si aucune transition déterminable ne rétablit un producteur, un dossier `RECOVERY` ne crée pas de droit nouveau. Une continuation exigeant de nouvelles règles nécessite un nouveau manifeste, un `chain_id` distinct, une acceptation explicite et une migration monétaire qualifiée.

Aucun ticket banni n’est ressuscité par signature administrative.

---

## 7. Loterie, production et persistance

### 7.1 Tirage

Tickets actifs triés globalement par TicketID :

```text
stream = SHAKE256(D("N/LOTTERY", seed_e || U64(slot)))
limit = floor(2^256/W) × W

repeat:
    x = entier big-endian des 32 prochains octets
until x < limit

j = x mod W
producer = owner(tickets[j])
```

Les octets rejetés sont consommés. Aucun remplacement du producteur absent.

Sous flux uniforme, la probabilité de l’identité `i` vaut `w_i/W`.

### 7.2 Phases

Pour un créneau commençant à `t` :

| Intervalle local | Action |
|---|---|
| Avant `t+1000 ms` | Synchronisation, validation, préparation |
| À partir de `t+1000 ms` | Choix du parent et réservation définitive |
| Avant ou à `t+2000 ms` | Signature, persistance, diffusion |
| Après `t+2000 ms` | Abandon si aucun en-tête signé |

Le calcul de signature et la persistance appartiennent à cette fenêtre.

Ces bornes sont exprimées en millisecondes absolues et ne dépendent pas de τ. À `tau_ms = 10 000`, un en-tête signé au plus tard à `t+2000 ms` dispose de `τ − 1 s = 9 s` pour être reçu et validé par tous les honnêtes avant la réservation du créneau suivant (`start(s+1)+1000 ms`) : c'est la condition D = 0 dont H_N borne les violations par `p_late` (§17.2).

Le parent est entièrement validé. Le registre est celui dérivé de sa continuation candidate selon le §5.

Un producteur ayant raté la fenêtre ne signe pas rétroactivement.

### 7.3 Égalité

Aucune adoption par premier vu. En cas de rang maximal égal, la production reste possible uniquement si la décision finale du §9 autorise la production et si au moins une pointe maximale est compatible avec les protections locales.

À l'instant de réservation, prendre parmi ces pointes celle de **plus petit `block_id` en ordre lexicographique**. C'est une règle déterministe de choix de parent à ensemble connu fixé, jamais un départage de canonicité : elle ne modifie ni Rank ni M, et ne permet aucune nouvelle stabilité avant résolution par N. Les hashes de contenu ne deviennent pas un score. L'adversaire peut influencer cet ordre de parent et l'ensemble livré ; ce coût figure dans l'analyse de vivacité.

L'ancêtre commun n'est pas imposé comme seul parent. Une extension de score h atteint h+1 ; la convergence exige des livraisons et créneaux honnêtes récurrents. Une réception après réservation ne permet pas de signer un second parent pour le même créneau.

### 7.4 Réservation anti-double-signature

Réservation principale :

```text
(chain_id, epoch, registry_root, seed, slot, IID, key_seq)
    -> header_digest
```

Elle ne contient pas `parent_id`.

Le producteur maintient aussi un garde-fou local :

```text
(chain_id, IID, slot)
    -> au plus un header_digest signé
```

Ce garde-fou couvre toutes les générations, tous les registres et toutes les graines. Un changement de génération ou de contexte ne réarme jamais la signature du même créneau. Ajouter `parent_id` à cette clé pour autoriser une seconde signature est interdit.

Avant toute exportation de signature :

1. réserver les deux clés ;
2. persister le digest exact ;
3. engager la réservation dans le dispositif anti-rollback du §7.6 ;
4. seulement ensuite signer et diffuser.

Après réservation, seuls les mêmes octets peuvent être signés ou rediffusés. Un doute impose l’abandon du créneau.

Les réservations survivent aux rollbacks de chaîne et aux changements d’origine.

### 7.5 Horloge

```text
start_ms(slot) > local_time_ms + future_tolerance_ms
    -> FUTURE
```

`FUTURE` est temporaire. Une réception tardive ne rend pas un bloc historiquement invalide.

Une incertitude excessive suspend production et nouvelles déclarations de stabilité.

### 7.6 Stockage anti-rollback et restauration

Un journal chaîné par hashes ne détecte pas, à lui seul, la restauration d’une ancienne sauvegarde cohérente.

Un nœud qualifié conserve un témoin monotone **extérieur au domaine de restauration de cette sauvegarde**, engageant au minimum :

```text
installation_id
monotonic_sequence
safety_state_digest
signing_reservations_digest
origin_id
```

Le mécanisme peut utiliser un stockage monotone matériel ou un service de journalisation distinct authentifié. Son modèle de panne, ses garanties d’exclusivité et sa procédure de récupération doivent être publiés.

Un simple fichier supplémentaire sauvegardé avec les autres ne satisfait pas cette exigence.

Le protocole de commit est :

1. écrire et synchroniser l’enregistrement préparé ;
2. avancer atomiquement le témoin externe par comparaison de séquence ;
3. marquer le commit local ;
4. exposer l’adoption ou exporter la signature.

Un crash après l’étape 2 mais avant l’étape 3 exige la récupération de l’enregistrement correspondant ; il n’autorise pas le recul du témoin.

Au redémarrage :

- égalité entre journal et témoin : poursuite ;
- journal ancien, divergent ou témoin inaccessible : `RESTORE_UNVERIFIED` ;
- données récentes récupérables et vérifiées contre le témoin : réparation mécanique ;
- continuité impossible à prouver : production interdite et aucune stabilité reposant sur les protections perdues.

Un nœud sans mécanisme anti-rollback qualifié peut fonctionner en observation ; il ne revendique pas la sûreté de restauration d’un producteur.

La copie de clés vers une seconde machine exige une procédure d’exclusivité. Deux témoins indépendants sur deux clones ne préviennent pas la double signature.

Si la mémoire de signature est définitivement perdue, une `RECOVERY` ne suffit pas à réarmer la même génération. La reprise de signature exige une procédure qualifiée éliminant tout risque de réutilisation, notamment exclusivité et changement de génération lorsque celui-ci est encore réalisable.

---

## 8. Blocs et rattrapage Bitcoin

### 8.1 En-tête

| Offset | Taille | Champ |
|---:|---:|---|
| 0 | 4 | ASCII `NBL0` |
| 4 | 2 | version `3` |
| 6 | 2 | suite `1` |
| 8 | 32 | chain_id |
| 40 | 32 | genesis_id |
| 72 | 8 | height |
| 80 | 8 | slot |
| 88 | 8 | epoch |
| 96 | 32 | parent_id |
| 128 | 32 | registry_root |
| 160 | 32 | seed |
| 192 | 4 | btc_ref_height |
| 196 | 32 | btc_ref_hash_raw |
| 228 | 32 | state_root |
| 260 | 32 | objects_root |
| 292 | 32 | ommers_root |
| 324 | 32 | evidence_root |
| 356 | 4 | body_length |
| 360 | 32 | producer_IID |
| 392 | 8 | key_seq |
| **Total** | **400** | |

```text
signature = MLDSA(D("N/BLOCK/SIGN", header400))
block_id = H("N/BLOCK/ID", header400)
```

En-tête signé : **2 820 octets**.

Deux signatures du même en-tête représentent un seul bloc.

### 8.2 Corps

```text
liste_variable(objects)
liste_fixe(ommers_signed_headers2820)
liste_fixe(evidence_pairs5640)
```

Objet :

```text
type:u16 || V(payload)
```

| Type | Contenu |
|---:|---|
| `0001` | Transaction applicative typée |
| `0002` | KEYREG |
| `0003` | ROTATE |
| `0004` | Création BTC/M1 |

Pour `0001` :

```text
version:u16 = 1
access_mode:u8
application_transaction:V(bytes)

00 = POSSEDE
01 = PARTAGE
```

Le mode est vérifié et signé par l’application.

Objets dans l’ordre du corps ; ommers triés par `block_id` ; preuves triées par `evidence_id`.

Domaines : `N/OBJECTS`, `N/OMMERS`, `N/EVIDENCE`.

### 8.3 Genesis et engagements

```text
genesis.height = 0
genesis.block_id = genesis_id
genesis.slot = −1  # convention logique non sérialisée
genesis.kernel_commit = H("N/KERNEL/GENESIS", genesis_id)
```

Premier bloc : hauteur 1, créneau au moins zéro.

```text
kernel_commit = H(
    "N/KERNEL",
    parent_kernel_commit ||
    U64(slot) ||
    U64(epoch) ||
    registry_root ||
    seed ||
    U32(btc_ref_height) ||
    btc_ref_hash_raw ||
    objects_root ||
    ommers_root ||
    evidence_root
)

state_root = H(
    "N/STATE",
    kernel_commit || application_state_root
)
```

Les sorties système utilisent un contexte calculable avant `application_state_root`, sans circularité avec `block_id`.

### 8.4 Repère Bitcoin

Validité historique :

```text
B.ref extends parent.ref
B.ref.height ≥ parent.ref.height

MTP(B.ref) ≤ start_ms(B.slot)//1000
             + btc_slot_mtp_margin_seconds
```

La dernière règle limite l’usage de faits Bitcoin trop tardifs dans un ancien créneau. Elle ne prouve pas la date réelle de signature.

La marge est exprimée en secondes. À `tau_ms = 10 000`, elle vaut 720 créneaux, et la garde nette de graine `G(τ) = ⌈(seed_guard_seconds − btc_slot_mtp_margin_seconds)/τ⌉ = ⌈36 000/10⌉ = 3 600` créneaux. Le premier porteur légal d'une maturité de graine ne peut donc précéder `freeze_slot(e) + 3 600`, soit `snapshot_cut(e) + K_inst` avec `K_inst = K_reg + G(τ) = 6 350` créneaux (§17.4).

Aucune limite historique de 144 hauteurs par bloc N.

Discipline de production :

```text
target = local_validated_btc_tip.height − d_ref

if target < parent.ref.height:
    reconcile Bitcoin
    do not sign

if BTC[target] does not extend parent.ref:
    reconcile Bitcoin
    do not sign

chosen_ref = BTC[target]
```

Le producteur vérifie aussi la borne MTP. Si elle échoue, il attend ; il ne choisit pas discrétionnairement un ancien repère pour améliorer son contexte.

Avec `d_ref=6`, le producteur vise sept confirmations inclusives ; l’adoption exige au moins six confirmations dans la vue du récepteur.

### 8.5 Scan reprenable

Lots d’au plus 144 blocs Bitcoin.

```text
parent_context
target_reference
scan_cursor
validated_Bitcoin_view
event_classifications
working_state
```

Un lot n’est pas un bloc N et n’ajoute aucun score.

Les résultats partiels ne sont ni adoptés, ni monétairement visibles, ni publiés comme registre actif.

Une réorganisation Bitcoin annule ou recontextualise le travail.

L’adoption du bloc est atomique après scan et exécution complets.

`RESOURCE_LIMIT` signifie travail différé, jamais invalidité.

### 8.6 Reprise après interruption

Une reprise mécanique exige :

1. origine, ancre, mémoire Bitcoin et état durable intègres ou réparés vérifiablement ;
2. continuité anti-rollback établie ;
3. récupération des données nécessaires ;
4. dérivation des époques manquées depuis chaque candidate ;
5. validation et scan Bitcoin complets ;
6. sélection selon le §9 ;
7. absence de contradiction bloquante.

Aucun journal d’observation des coupures n’est demandé.

Pour produire s’ajoutent :

- identité active et clé courante ;
- graine mûre ;
- horloge admissible ;
- créneau courant et fenêtre de signature ouverte ;
- réservation durable ;
- absence de veto pertinent.

La durée de l’interruption n’ajoute aucune condition de checkpoint.

Une interruption collective peut reprendre par un bloc ordinaire au créneau courant avec grand saut du repère Bitcoin. Aucun ancien créneau n’est signé et aucun dossier administratif ne simule des blocs manquants.

### 8.7 Fraîcheur opérationnelle

```text
ref_lag =
    max(0, local_btc_tip.height − d_ref + 1 − N_tip.ref.height)
```

Le choix normal du producteur a un retard de 1 selon cette métrique.

Une maturité de `k` dans le repère exige :

- au minimum `k+d_ref−1` confirmations dans la vue d’adoption ;
- normalement `k+d_ref` avec la marge du producteur.

Ticket et graine : minimum 35, cible 36.  
Paiement de swap : minimum 11, cible 12.

Ces valeurs ne limitent pas l’âge d’un `BOOTSTRAP`.

### 8.8 Application

```text
Apply(parent_state, objects, bitcoin_context, system_effects)
    -> new_state, application_state_root
```

Fonction déterministe et atomique, indépendante du mempool, des pairs et de l’horloge locale.

Un objet applicatif invalide invalide le bloc.

Les frais sont transférés au producteur en sorties immatures.

---

## 9. Validation, sélection et réorganisation

### 9.1 Résultats

```text
VALID
INVALID
MISSING_DATA
FUTURE
BTC_IMMATURE
BTC_ORPHANED
BTC_TIE_PENDING
RESOURCE_LIMIT
EQUIVOCATION_TIE
EQUIVOCATION_TIE_STALLED
TEMPORAL_ALERT
TEMPORAL_COMPARISON_UNKNOWN
HALTED_TEMPORAL_CONFLICT
HALTED_DEEP_REORG
HALTED_BTC
HALTED_EMPTY_REGISTRY
RESTORE_UNVERIFIED
BOOTSTRAP_REQUIRED
BOOTSTRAP_IGNORED_LOCAL_ORIGIN
CHECKPOINT_CONFLICT
RECOVERY_AVAILABLE
RECOVERY_ACTIVATION_REQUIRED
UNPROVEN_HISTORY
LOCAL_FAILURE
```

`TEMPORALLY_DISQUALIFIED` est retiré : la v0.6 ne retire pas des candidats pour recalculer un gagnant.

Les états locaux peuvent coexister avec `VALID`.

### 9.2 Validation historique

```text
ValidateHeader(B):
    check exact encoding, version, suite, network, limits
    require parent and complete historical contexts
    require B.height == parent.height + 1
    require parent is genesis or B.slot > parent.slot
    require B.epoch == B.slot // L_epoch

    establish Bitcoin reference and ancestry
    require B.ref extends parent.ref
    require historical MTP bound

    derive skipped epoch transitions from candidate ancestry
    derive R_e and S_e
    require k_seed confirmations within B.ref
    require matching registry_root and seed
    require matching lottery producer and key_seq
    require valid signature

    return HEADER_VALID
```

```text
ValidateBody(B):
    require HEADER_VALID
    check body length, quotas and roots
    validate ommers and evidence
    clone parent state

    scan Bitcoin in resumable chunks
    classify newly mature events against parent ancestry
    prepare FIFO admissions and REACT
    resolve due swaps by swap_id
    execute objects in encoded order
    examine newly created swaps
    enforce provenance, conservation and fee maturity
    credit transferred fees
    compute commitments
    require matching state_root

    persist full validation result
    return VALID
```

La validation historique ne lit aucun ancien verrou local de registre.

### 9.3 Score et rang

```text
score(C) = nombre de blocs de production valides depuis genesis

tie(B) = H(
    "N/TIE",
    B.seed || U64(B.slot) || B.producer_IID
)
```

À score égal, comparer lexicographiquement les séquences de `tie` depuis le premier bloc après l’ancêtre commun. La plus petite gagne.

```text
Rank = (score décroissant, tie_sequence croissante)
```

Aucun contenu, parent, hash de bloc, signature, checkpoint ou ordre de réception n’ajoute un départage.

Le départage est public une fois le calendrier connu. L’adversaire peut choisir les égalités qu’il tente d’exploiter.

### 9.4 Égalité persistante

Des branches distinctes de même score et même séquence restent ex æquo.

Le nœud :

- conserve l’ensemble maximal ;
- suspend les nouvelles stabilités dépendant du suffixe divergent ;
- autorise la production selon le §7.3 ;
- ne remplace pas arbitrairement sa chaîne par une variante.

Après 100 créneaux achevés :

```text
EQUIVOCATION_TIE_STALLED
```

Aucun timeout ne crée de canonicité.

Une branche de même score mais de meilleur départage est une candidate supérieure. Si elle exige une réorganisation interdite, elle peut provoquer un arrêt profond.

### 9.5 Sélection avec veto séparé

Entrées :

```text
candidats validés et opérationnellement examinables
chaîne adoptée
vue Bitcoin
horizon local
politique
origine locale
ancre persistante antérieure
mémoire des graines
données du détecteur H1
```

L’ensemble examinable exclut les blocs historiquement invalides, futurs ou dépendant d’un Bitcoin actuellement non réconcilié. Il n’exclut pas une candidate parce qu’elle contredit l’ancre.

```text
Select(state, candidates):
    S0 = snapshot of durable safety state

    V = completely validated, operationally examinable candidates
    include adopted chain when still examinable

    M = maximal_rank_set(V)          # aucun effet H1 ici

    base = BaseNDecision(S0, M)      # ancre, maxreorg, égalités, BTC
    temporal = H1Decision(S0, V, M) # aucun retrait de V ou de M

    if temporal is TRUE_WITH_COMPLETE_WITNESS:
        return HALTED_TEMPORAL_CONFLICT, plus any base HALT as secondary reason

    if base is HALT:
        return base, plus any temporal UNKNOWN as secondary reason

    if temporal is RELEVANT_UNKNOWN:
        return TEMPORAL_COMPARISON_UNKNOWN   # attente, aucune adoption positive

    if base is UNIQUE_ADOPTION:
        atomically adopt that exact candidate
        advance anchor after adoption
        return ADOPTED

    return base                     # maintien ou égalité
```

H1 ne déclenche jamais un second calcul de rang sur des « survivants ».

Une candidate inférieure ne provoque pas un arrêt profond par sa seule profondeur.

Une candidate maximale incompatible avec l’ancre n’est pas supprimée pour faire gagner la chaîne locale.

Un `BOOTSTRAP` reçu sur une origine existante ne participe à aucune entrée de cette fonction.

La décision de base est la fonction suivante, sans lecture de H1 :

```text
BaseNDecision(S0,M):
    if durable state is unverified: return RESTORE_UNVERIFIED
    if a genesis dependency or consumed seed is orphaned: return HALTED_BTC
    if relevant Bitcoin work tie is unresolved: return BTC_TIE_PENDING
    if M is empty: return WAIT_FOR_VALIDATED_DATA
    if any C in M does not extend S0.anchor
       or disconnects more than maxreorg blocks from S0.adopted_tip:
        return HALTED_DEEP_REORG
    if len(M) > 1: return EQUIVOCATION_TIE  # aucune adoption nouvelle
    let C be the unique member of M
    if C == S0.adopted_chain: return MAINTAIN
    return UNIQUE_ADOPTION(C)
```

La distance de déconnexion est `links_N(LCA(S0.adopted_tip,C),S0.adopted_tip)`. Si M comprend à la fois un maximum compatible et un incompatible, le résultat est STOP, pas le choix du compatible. En égalité sans veto ni arrêt, §7.3 autorise la production sur le parent déterminé. `MAINTAIN` est aussi soumis à H1 : une alerte contre la chaîne déjà adoptée suspend production et nouvelles stabilités. Aucun chemin de maintien ne court-circuite ce contrôle.

Les motifs d'arrêt/attente sont recalculés ; la priorité d'affichage ci-dessus ne supprime aucune protection. Des entrées incomplètes ne deviennent pas une autorisation implicite.

### 9.6 Ancre persistante : fonction exacte

Après adoption complète de T, à vue Bitcoin réconciliée B fixée, calculer :

```text
Nbound(T) = ancestor(T,maxreorg liens), ou genesis si T.height < maxreorg
Bbound(T,B) = plus haut bloc de T dont le repère a au moins D_btc=100
              confirmations inclusives dans B, ou genesis si aucun
eligible(T,B) = le moins haut de Nbound(T) et Bbound(T,B)
anchor_next = le plus haut de anchor_old et eligible(T,B)
```

Les blocs comparés sont sur l'ascendance adoptée ; le contrôle préalable interdit d'adopter une chaîne retirant `anchor_old`. L'ancre initiale est celle de l'origine explicitement installée, non une pointe choisie par préférence locale. Les préconditions Bitcoin de cette origine restent obligatoires (§11.4, §12.12).

**L'égalité ci-dessus est exacte.** Aucune protection automatique plus haute, aucun avancement au support d'un registre engagé, aucune latitude pour ancrer immédiatement la pointe. Une amélioration de profondeur Bitcoin seule peut provoquer une réévaluation avec la même T, par la même fonction et le même commit durable ; elle ne change pas la chaîne. Un recul de B ne fait pas reculer l'ancre.

L'ancre est persistée atomiquement avec l'adoption et avant toute déclaration client dépendante. La borne en confirmations Bitcoin réduit l'exposition des nouveaux avancements aux réorganisations courtes, sans garantir la récupération : les graines consommées, genesis et `maxreorg` restent des protections distinctes. Une RECOVERY n'invalide jamais les faits Bitcoin actuels.

Une candidate maximale retirant l'ancre ou exigeant plus de `maxreorg` = 1 630 déconnexions entraîne `HALTED_DEEP_REORG`. Signature et nouvelles stabilités sont suspendues ; lecture, validation et récupération continuent. L'arrêt est réévalué quand les données changent, sans bit irréversible ; résolution mécanique si possible, sinon récupération explicite.

La protection d'un bloc support ne garantit un préfixe temporel de registre que si cette identité découle effectivement du préfixe protégé et des règles de validation. L'âge du dernier bloc ne suffit pas. Aucun nouvel arrêt ne résulte de la seule mémorisation d'une racine de registre.

### 9.7 Reconnexion

```text
vérifier journal et témoin anti-rollback
récupérer les données
réconcilier Bitcoin
valider chaque candidate
rejouer les époques manquées sur chaque candidate
calculer rang et décisions
contrôler l’ancre antérieure
adopter, attendre ou arrêter
réinclure les transitions admissibles
```

Aucun contrôle administratif lié à deux heures, quatre heures, une journée ou une durée quelconque.

Une restauration ayant perdu des métadonnées de sûreté n’est pas une simple absence.

---

## 10. Équivoques, ommers et ressources

### 10.1 Preuve d’équivoque

Deux en-têtes constituent une preuve publique de faute si :

- leurs digests d'en-tête (`block_id`) diffèrent ;
- ils portent le même `(chain_id, IID, slot)` ;
- chaque signature vérifie sous une génération de cet IID effective à ce créneau dans son **propre contexte historique vérifié**.

Ni `registry_root`, ni graine, ni époque encodée, ni `key_seq` identiques ne sont exigés entre les deux en-têtes. Deux générations différentes effectives dans deux histoires vérifiées sont couvertes ; une clé jamais effective au créneau prouvé ne suffit pas. L'attribution de loterie n'est pas nécessaire à la faute : signer hors attribution est déjà une déviation. Les contextes établissent les clés et leur effectivité sans exiger la validité de production des deux en-têtes fautifs.

Les contextes de branche, KEYREG et rotations nécessaires DOIVENT être disponibles et vérifiés ; sinon `MISSING_DATA`, pas acquittement ni ban. Ils sont des données de validation récupérables par les identifiants d'en-tête ; les deux en-têtes seuls ne dispensent pas de cette vérification.

Les corps n’ont pas à être exécutables.

```text
evidence = signed_header_A2820 || signed_header_B2820
evidence_id = H("N/EQUIVOCATION", evidence)
```

Ordre par `block_id`. Taille : **5 640 octets**.

### 10.2 Admissibilité après rotation

Dans un porteur `B` :

```text
0 < B.slot − proved_slot ≤ evidence_horizon
```

Chaque génération prouvée doit avoir été effective **au créneau prouvé**, dans le contexte historique vérifié de son en-tête, y compris si ce contexte diffère de la branche porteuse.

Elle n’a pas à être encore effective dans le parent du porteur.

Une rotation préparée, activée ou ultérieure ne supprime pas la recevabilité d’une preuve encore dans l’horizon.

Les historiques de clés nécessaires sont conservés ou récupérables.

Une preuve incluse dans l’horizon conserve son effet pendant sa maturation, même si cette maturation intervient après l’horizon.

Une preuve présentée pour la première fois au-delà de l’horizon reste un élément d’audit sans effet de ban.

### 10.3 Ban

Le porteur de preuve doit appartenir au support `A_e` et y posséder au moins `k_ban` confirmations.

Cette maturité d’objet ne constitue pas une condition de production des blocs ni de stabilité du registre.

Le ban détruit les droits, neutralise admissions et REACT, conserve l’historique, et ne modifie ni score passé ni registre de l’époque déjà en cours.

Une preuve de gossip ne déclenche aucun ban instantané.

### 10.4 Déduplication

La clé de faute est `(chain_id, IID, slot)`, toutes générations et tous registres confondus. Deux preuves de cette même clé, ou une clé déjà prouvée dans l'ascendance, rendent le bloc invalide. Le ban vise IID une seule fois ; une autre variante n'ajoute pas un second ban.

Déduplication des ommers par `block_id` : un ommer répété ou déjà inclus rend le bloc invalide.

### 10.5 Ommers

Un ommer :

- est absent de l’ascendance du porteur ;
- a un créneau strictement antérieur ;
- satisfait un écart maximal de 1 440 créneaux ;
- possède signature et attribution valides ;
- utilise le registre et la graine dérivés par la branche porteuse pour son créneau ;
- n’a pas déjà été inclus.

Son corps n’est pas exécuté pour créditer l’activité. Sa signature ne prouve pas la disponibilité du corps.

Pas d’auto-crédit. Le minimum canonique reste exigé.

Plusieurs IID peuvent colluder pour se créditer mutuellement. Cette possibilité figure au banc.

### 10.6 Variantes et DoS

Ordre normal :

1. taille, réseau, version ;
2. contexte ;
3. signature et attribution ;
4. équivoque ;
5. corps.

Au plus deux variantes authentifiées par réservation sont exécutées sur le chemin spéculatif.

Une troisième peut être vérifiée sur un chemin borné si elle appartient à une branche susceptible d’améliorer le rang.

Priorités de travail candidates :

```text
branche adoptée : contrôle urgent : candidats : archives
8 : 4 : 2 : 1
```

Les budgets sont publiés. Leur épuisement donne `RESOURCE_LIMIT`, jamais une preuve de défaite.

---

## 11. Réorganisations Bitcoin

### 11.1 Vue Bitcoin

Le moteur vérifie règles, travail cumulé, transactions et faits nécessaires. Un RPC n’est pas une autorité.

À travail cumulé maximal égal entre branches Bitcoin divergentes :

```text
BTC_TIE_PENDING
```

Le nœud conserve son état adopté comme état local, sans déclarer arbitrairement l’autre branche Bitcoin invalide.

Il suspend adoption, production et nouvelles stabilités lorsqu’elles dépendent des faits divergents.

Les faits du préfixe commun peuvent continuer à être vérifiés.

Une branche de travail strictement supérieur permet la réconciliation. Aucun choix local à travail égal n’est injecté dans la validité historique de N.

### 11.2 Repère retiré

Le nœud :

1. recalcule la vue ;
2. invalide les caches dépendants ;
3. identifie les repères retirés ;
4. classe leurs descendants `BTC_ORPHANED` ;
5. calcule le rollback ;
6. vérifie ancre, graines et `maxreorg` ;
7. applique atomiquement ou s’arrête ;
8. rejoue événements, swaps et index temporel.

Aucun rollback automatique ne retire l’ancre.

La disparition d’une référence N d’un burn M0 n’annule pas l’importation. La disparition du burn Bitcoin lui-même relève des règles monétaires.

### 11.3 Graine consommée retirée

Mémoire durable des graines consommées par une adoption ou une signature :

```text
(epoch, seed_height, seed_hash)
```

Le retrait d’une telle graine entraîne :

```text
HALTED_BTC
```

Aucun recalcul silencieux des producteurs passés.

Une vue Bitcoin rétablissant les graines permet une revalidation mécanique.

Une `RECOVERY` explicitement acceptée reste soumise à la validité Bitcoin actuelle. Une signature administrative ne rend jamais vrai un fait Bitcoin faux.

### 11.4 Dépendances Bitcoin du genesis

Chaque vérificateur, nouveau ou déjà initialisé, DOIT valider le même inventaire :

| Dépendance | Engagement à vérifier dans la vue Bitcoin |
|---|---|
| Point initial | Hauteur/hash et règles Bitcoin du descripteur |
| Préengagement | Outpoint, inclusion, authentification, ordre du premier NEW, profondeur avant h_start |
| Admissions initiales | Scan exhaustif de [h_start,h_end], transactions, prevouts, KEYREG, maturité à h_mature |
| Graine initiale | Sélection exacte de S_0, hauteur/hash, garde MTP et maturité |
| Repère genesis | Hauteur/hash à g_ref_height et ascendance |
| Scellement | Hauteur/hash à seal_height=g_ref_height+d_ref, calcul de T0_ms |

Les préfixes Bitcoin engagés authentifient les inclusions ; des données manquantes imposent attente, pas invalidité par défaut. Le scellement est une dépendance, même si aucun bloc N produit ne référence encore sa hauteur.

Retrait d'une de ces dépendances dans la vue de travail supérieur : genesis et tous ses descendants deviennent `BTC_ORPHANED` dans cette vue ; le nœud initialisé passe `HALTED_BTC` et le nouveau vérificateur refuse l'installation avec ce même motif. Une égalité de travail pertinente impose `BTC_TIE_PENDING`. Aucun nœud ne garde un scellement orphelin comme exception historique implicite.

Si la vue valide rétablit les dépendances, revalidation et reprise mécanique sont possibles. Sinon ni BOOTSTRAP ni RECOVERY ne réparent ce genesis sous le même engagement. Un relancement requiert un nouveau manifeste, un chain_id distinct, une acceptation explicite et une migration monétaire qualifiée ; aucun retraitement silencieux de T0 ou de R_0.

La publication initiale DOIT attendre au moins D_btc confirmations du bloc de scellement. Cette attente retarde éventuellement le premier créneau produit après T0 ; elle ne recalcule pas T0 et n'autorise pas la signature rétroactive. Elle réduit le risque sans remplacer la règle de retrait.

### 11.5 Cadence et risque d'arrêt

À cadence N pleine et `tau_ms = 10 000`, `maxreorg` = 1 630 liens représentent 16 300 s, soit environ 4,5 h (environ 9,3 h à la seule production honnête du coin de domaine, h' ≈ 0,485) ; le repère d'une ancre fondée uniquement sur ces liens aurait environ `d_ref+1+4,5h/intervalle_BTC` confirmations. À 20–30 minutes par bloc Bitcoin, cela ne justifie pas 100 confirmations. Le §9.6 attend donc la seconde borne explicitement, sans conversion consensus entre temps et blocs.

Même une réorganisation Bitcoin ne retirant aucune graine peut exiger plus de maxreorg déconnexions N et provoquer STOP. Une réorganisation retirant des graines consommées ou genesis relève des arrêts obligatoires, quelle que soit D_btc. Le domaine A4 publie séparément profondeur Bitcoin, cadence, avance des repères et probabilité/durée d'arrêt ; aucune absence universelle de RECOVERY n'est déduite de D_btc=100. Des frais déjà protégés dont l'origine devient orpheline ne sont pas silencieusement undo au travers de l'ancre.

---

## 12. H1, longue portée et origines de confiance

### 12.1 Nature de H1

Invariant propriétaire :

> **une preuve d’antériorité Bitcoin peut réduire l’ensemble des histoires qu’un nœud considère sûres ou déclencher un arrêt ; elle ne peut jamais, à elle seule, rendre canonique une histoire que la fork-choice N n’aurait pas choisie.**

La v0.6 réalise cette propriété par un **veto séparé** :

```text
décision de base N
    -> décision identique
    ou attente
    ou arrêt
```

H1 ne modifie ni score, ni départage, ni registre, ni ancre, ni origine. Une preuve H1 NE DOIT PAS certifier un registre, rendre commun son support ni départager positivement deux registres. BOOTSTRAP reste sans effet sur une origine locale ; RECOVERY reste un acte explicite, jamais déclenché automatiquement par un changement de registre.

Il ne prouve pas nécessairement une fabrication tardive. Une branche honnête peu empreintée peut présenter un retard de progrès prouvé.

Il ne protège pas universellement un nœud neuf sous éclipse ni contre une reconstruction supérieure non accompagnée de preuves contradictoires visibles.

### 12.2 Empreintes admissibles

NEW/ADD/REACT :

- sortie unique reconnue ;
- type et réseau exacts ;
- authentification Bitcoin ;
- valeur d’au moins 250 000 sats ;
- inclusion dans la vue Bitcoin examinée ;
- au moins 30 confirmations Bitcoin ;
- identité et preuves de possession vérifiables.

L’admission du ticket sur la branche n’est pas nécessaire à l’usage temporel.

M0 v3 :

- burn monétairement reconnaissable sur le réseau ;
- référence présente ;
- montant d’au moins 250 000 sats ;
- inclusion dans la vue Bitcoin examinée ;
- au moins 30 confirmations Bitcoin ;
- référence résolue vers un bloc vérifiable.

Pour toutes ces sources, le bloc N référencé doit avoir au moins :

```text
temporal_reference_depth_N = 30
```

confirmations dans la branche examinée au moment de l’évaluation.

La profondeur 30 vise la recevabilité d'un détecteur qui ne peut que retirer une autorisation ; les 60 confirmations de §4.7 protègent l'admission de droits et, pour REACT, le bloc matérialisant le dossier. Les deux prédicats sont volontairement distincts : une empreinte recevable ne vaut ni admission ni stabilité. Leur écart reste à qualifier contre le déni de service par veto.

Cette profondeur est une condition de traitement du détecteur. Elle ne prouve pas que trente confirmations N existaient déjà lors de l’inclusion Bitcoin.

| Source | Engagement |
|---|---|
| NEW/ADD | Bloc désigné |
| REACT | `A_e` de la préimage vérifiée du dossier |
| M0 v3 | Bloc désigné |

Une REACT ne prouve pas les blocs postérieurs à son `A_e`.

Genesis, l’ancêtre commun et `bootstrap_ref` ne prouvent pas de progrès post-divergence.

### 12.3 Complétude

L’index conserve :

```text
source_kind
reference_kind
reference32
supporting_outpoint
inclusion_height
Bitcoin_view
authentication_status
resolution_status
resolved_block_id
N_depth_at_evaluation
```

Une preuve d’absence exige :

1. scan Bitcoin complet de l’intervalle ;
2. transactions et prevouts nécessaires ;
3. KEYREG et preuves de possession pertinentes ;
4. préimages REACT pertinentes ;
5. résolution vers les branches examinées ;
6. validation des préfixes N utilisés.

La pertinence est décidée par un algorithme fini pour chaque paire (C,W) complète :

1. Énumérer les block_id des deux histoires et reconstruire leurs dossiers d'exclusion, y compris les transitions d'époques sautées. Former les tables `Blocks` et `Exclusions[x]` avec leurs préimages exactes, ainsi que les KEYREG et générations référencés.
2. Scanner exhaustivement l'intervalle Bitcoin requis par RawLag, avec transactions et prevouts nécessaires. Les limites de lots n'en changent pas la couverture.
3. Pour une référence BLOCK (M0, NEW/ADD), si son identifiant est absent de Blocks, elle est `IRRELEVANT` pour cette paire, sans téléchargement d'une branche arbitraire. Pour REACT, comparer x à Exclusions : absent de la table exhaustive implique `IRRELEVANT`, même sans préimage fournie par l'émetteur.
4. Pour un identifiant correspondant, utiliser la préimage reconstruite, contrôler champs, engagement, source, authentification et règles §12.2. Un KEYREG pour NEW/ADD doit appartenir au préfixe référencé ; pour REACT, au contexte vérifié du dossier. S'il est absent d'un tel préfixe **complet**, l'empreinte est inadmissible ; s'il manque des données de ce préfixe, la résolution reste `UNKNOWN`.
5. Si un dossier ou son KEYREG pertinent ne peut être reconstruit, la paire n'est pas complète : réclamer les objets manquants nommément. Une référence opaque étrangère ne suffit jamais à maintenir une comparaison en attente.

`UNKNOWN` est réservé à une lacune identifiée (scan Bitcoin, prevout/authentification, préfixe nécessaire, pièce correspondante non disponible), jamais à la possibilité abstraite qu'un autre dossier existe ailleurs. Une contradiction de hash est un échec de validation, pas une nouvelle inconnue. Une implémentation peut borner le travail et annoncer `RESOURCE_LIMIT` ; elle ne transforme ni une couverture partielle en absence, ni une annonce non validée en veto.

Un nœud Bitcoin élagué isolé DOIT récupérer vérifiablement les données nécessaires. Les caches de pertinence sont indexés par paire d'histoires, règles et vue Bitcoin ; toute réorganisation les invalide ou les recontextualise.

### 12.4 Progrès prouvé

Pour `D=LCA(C,W)` :

```text
proven_slot(C,D,b)
```

est le plus grand créneau d’un bloc de `C` strictement postérieur à `D`, couvert par une empreinte admissible incluse au plus à hauteur Bitcoin `b`.

Sans progrès : `−∞`.

Un descendant engagé couvre ses ancêtres.

Les étapes sont exactement les hauteurs Bitcoin où le maximum augmente strictement. Les empreintes d’une même hauteur sont agrégées avant création d’une étape. Un maximum ou une absence ne sont définitifs que si la couverture pertinente jusqu'à cette hauteur est complète ; un simple enregistrement partiel d'index ne certifie pas une étape stricte.

### 12.5 Retard temporel

```text
RawLag(C, W, btc_view):
    D = LCA(C,W)
    last_mature_step = btc_view.height − G_anchor − anchor_depth
    if last_mature_step < initial_Bitcoin_scan_height:
        return FALSE  # aucune fenêtre encore évaluable

    for b in increasing proven strict step heights of W up to last_mature_step:
        if witness coverage for W through b and C through b+G_anchor is complete:
            if proven_slot(W,D,b) > proven_slot(C,D,b+G_anchor):
                return TRUE with that complete witness

    if any relevant matured coverage/resolution remains incomplete:
        return UNKNOWN with exact missing intervals/objects
    return FALSE
```

Condition entière conservée :

```text
b + 26280 + 30 ≤ H_BTC
```

Une égalité de progrès ne suffit pas.

`TRUE` signifie retard de progrès prouvé selon cette règle. Il ne signifie pas « branche historiquement invalide ».

### 12.6 Périmètre exact du veto

`V` est l'ensemble validé et examinable du §9.5, avant H1 ; `M=maximal_rank_set(V)`. Les pointes et témoins déjà validés restent indexés comme candidats, même s'ils n'ont jamais été adoptés. Aucune préférence de cache pour l'histoire locale ne peut les exclure du détecteur.

```text
Deep(C,W) = C et W distinctes, aucune préfixe de l'autre, et
            max(links_N(LCA(C,W),tip(C)),
                links_N(LCA(C,W),tip(W))) > maxreorg
Pairs(V,M) = {(C,W) : C ∈ M, W ∈ V, Deep(C,W)}
H1Veto(V,M,B) = ∃ (C,W) ∈ Pairs : RawLag(C,W,B)=TRUE
                                      avec témoin complet
```

La profondeur de H1 est une propriété des deux branches, **indépendante de l'ancre locale et de l'historique d'adoption**. La protection d'ancre demeure dans BaseNDecision, y compris pour un conflit moins profond selon ce prédicat. W peut être de score inférieur et n'avoir jamais été adoptée.

Une paire est orientée : seule la preuve de retard de C, la candidate maximale, permet ce veto. Si W est aussi maximale, les deux directions appartiennent à Pairs ; deux TRUE donnent `MUTUAL_LAG`. Un retard de W inférieure envers C ne justifie pas de stopper C. Les comparaisons entre deux perdants restent diagnostiques.

Tout TRUE avec témoin complet entraîne `HALTED_TEMPORAL_CONFLICT`, **y compris si C est déjà la chaîne adoptée et si BaseNDecision retourne MAINTAIN**. La chaîne locale est conservée pour inspection mais aucune continuation productive ni nouvelle stabilité n'est autorisée sous ce veto. W n'est jamais adoptée par H1. M n'est ni filtré ni recalculé.

À V, rangs, couverture et vue Bitcoin identiques, le résultat H1 est identique pour toutes les permutations d'arrivée. Dans le scénario C supérieure reconstruite / W empreintée, C puis W, W puis C et réception simultanée conduisent au même veto une fois les deux validées. Avant réception de W, aucune promesse de détection n'est possible : une adoption passée de C ne peut être annulée rétroactivement par une information absente. L'indépendance annoncée porte sur la décision réévaluée à données communes, non sur l'identité des états durables déjà acquis.

### 12.7 Inconnues et réévaluation

Une annonce non validée ne déclenche pas STOP. Une inconnue ne suspend que si elle affecte une paire de Pairs et une fenêtre évaluable :

- une étape de progrès admissible de W à hauteur b est déjà prouvée et `b+G_anchor+anchor_depth ≤ H_BTC`, mais le scan nécessaire de C est incomplet ; ou
- la couverture Bitcoin est incomplète dans l'intervalle pouvant contenir une telle étape mûre de W, compte tenu des références résolubles du §12.3.

Les lacunes sont décrites par intervalles et objets exacts. Une couverture et des tables complètes prouvent la non-pertinence des références étrangères. Une fenêtre non encore mûre et une inconnue entre seuls perdants restent diagnostiques.

Une inconnue pertinente suspend adoption, nouvelles stabilités et production engageant la candidate concernée, même si celle-ci est déjà adoptée. Le résultat est `TEMPORAL_COMPARISON_UNKNOWN`. Un témoin TRUE complet suffit au veto sans attendre de résoudre d'autres paires ; aucune donnée manquante ne supprime un témoin déjà vérifié dans la même vue.

Toute modification des candidats, rangs, vue Bitcoin ou données provoque une réévaluation, y compris sur chaîne inchangée. Les preuves et candidats nécessaires sont conservés ou récupérables ; une éviction de cache ne transforme pas un veto connu en FALSE. Les motifs devenus objectivement hors périmètre cessent d'agir. Il n'existe ni graphe de SCC ni journal d'anciennes adoptions participant au prédicat H1.

### 12.8 Limites longue portée

Une reconstruction supérieure peut :

- être bloquée par l’ancre d’un nœud ancien ;
- déclencher H1 si une comparaison pertinente apporte les faits nécessaires ;
- rester non détectée par H1, notamment sous éclipse.

Une preuve temporelle ne permet jamais de choisir à sa place une chaîne de rang inférieur.

Le nœud s’arrête lorsqu’un conflit pertinent ne peut être résolu sous ses protections. Une récupération explicite peut ensuite changer son origine.

### 12.9 Cadence H1

```text
G_anchor = 26280
anchor_cadence = 13140
```

Un progrès doit couvrir un bloc plus récent que le précédent progrès prouvé. Répéter une référence ne satisfait pas H1.

Le suivi utilise la hauteur d’inclusion, même si la reconnaissance attend la maturité.

```text
âge ≥ 6570  : avertissement
âge ≥ 9855  : alerte rouge
âge > 13140 : H1 manquée
```

Le plan d’astreinte publié précise responsables, domaines de panne, escalade, clés, capacité financière, surveillance d’inclusion et réorganisations.

Une dépendance administrative unique est affichée :

```text
SINGLE_ADMIN_CADENCE
```

Une cadence manquée produit `UNPROVEN_HISTORY`, sans invalidation de chaîne, changement de rang, obligation de checkpoint ni arrêt automatique de production.

Pour une divergence `D` :

```text
délai d’évaluation =
    délai jusqu’à une empreinte couvrant un progrès post-D
    + 26310 blocs BTC
```

H1 seule ne borne pas le retard du bloc référencé par rapport à la pointe.

Avec l’hypothèse supplémentaire d’une empreinte post-divergence dans la cadence suivante :

```text
13140 + 26280 + 30 = 39450 blocs BTC
```

Ce nombre est un délai conditionnel d’évaluation, **pas** un âge maximal utile du `BOOTSTRAP`, ni une garantie de détection.

Quatre ADD de secours annuels représentent 0,04 BTC hors frais dans le scénario sans activité naturelle suffisante.

### 12.10 Dossier de checkpoint v6

```text
kind 0 = BOOTSTRAP
kind 1 = RECOVERY

authentication_mode 1 = RELEASE
```

Les modes 2 et 3 ne sont pas acceptés au lancement.

Noyau de **588 octets** :

| Champ | Taille |
|---|---:|
| version=`6` | 2 |
| authentication_mode | 1 |
| kind | 1 |
| chain_id | 32 |
| genesis_id | 32 |
| application_spec_id | 32 |
| crypto_profile_id | 32 |
| policy_id | 32 |
| trust_policy_id | 32 |
| serial | 8 |
| previous_checkpoint_id | 32 |
| previous_origin_id | 32 |
| previous_anchor_id | 32 |
| previous_safety_state_root | 32 |
| block_id | 32 |
| height | 8 |
| slot | 8 |
| state_root | 32 |
| registry_root | 32 |
| btc_ref_height | 4 |
| btc_ref_hash | 32 |
| observed_btc_height | 4 |
| observed_btc_hash | 32 |
| issued_at_seconds | 8 |
| bundle_root | 32 |
| reason_hash | 32 |
| **Total** | **588** |

`previous_safety_state_root` remplace sémantiquement l’ancien champ de racine des verrous. La version 6 interdit de les confondre.

```text
checkpoint_id = H("N/CHECKPOINT/ID", core588)
```

Pour `BOOTSTRAP`, les champs `previous_origin_id`, `previous_anchor_id` et `previous_safety_state_root` valent zéro.

Le bundle comprend les données nécessaires à :

- l’histoire et aux corps ;
- l’état applicatif et à la comptabilité ;
- l’état de contrôle et aux historiques de clés ;
- la dérivation des registres ;
- la mémoire des graines ;
- Bitcoin et à la couverture du scan ;
- la politique de signatures ;
- l’origine et à l’ancre proposées ;
- au motif ;
- pour `RECOVERY`, au contexte antérieur et aux conséquences.

Aucun composant de verrou local de registre n’existe.

Les composants sont typés, ordonnés et encodés selon le schéma engagé par le corpus :

```text
component = type:u16 || V(payload)
bundle_root = ListRoot("N/CHECKPOINT/BUNDLE", composants)
```

Les types requis, leur unicité et leurs schémas doivent être gelés conjointement avant activation. Une racine de snapshot ne remplace pas le rejeu.

Signatures :

```text
key_id = H("N/CHECKPOINT/KEY", public_key1312)
signature = MLDSA(D("N/CHECKPOINT/SIGN", core588))
```

Entrée : `key_id32 || signature2420`, soit **2 452 octets**.

Enveloppe :

```text
core588 || liste_fixe(release_signatures2452)
```

| Signatures | Taille |
|---:|---:|
| 3 | 7 948 octets |
| 4 | 10 400 octets |

Liste triée par `key_id`. Doublons, clés inconnues et plus de quatre entrées rejetés.

### 12.11 Politique RELEASE

```text
4 clés de release
seuil 3/4
administration commune publiée au lancement
```

Chaque clé dispose d’une fiche : identifiant, clé publique, responsable, domaine administratif, rôle, garde, sauvegardes, succession et canaux de publication.

La séparation opérationnelle ne prouve pas l’indépendance administrative.

Trois clés compromises permettent une authentification complète. Deux clés indisponibles empêchent une nouvelle publication, sans arrêter les nœuds déjà initialisés.

Les `BOOTSTRAP` ordinaires successifs suivent un même préfixe. Un serial supérieur n’autorise pas une rupture.

Un nœud sans origine locale **DOIT**, avant installation, comparer les réponses authentifiées d'au moins deux canaux de distribution distincts configurés dans la politique RELEASE, et vérifier la continuité des dossiers successifs disponibles. Deux URLs du même canal ne comptent pas deux fois. La politique publie les canaux, leurs domaines de panne et leur dépendance administrative ; leur pluralité ne prouve pas l'indépendance.

La collecte initiale doit être terminée pour ces canaux et tous les dossiers authentifiés reçus avant le commit sont comparés. Canal indisponible : attente de bootstrap, aucun timeout ni mode mono-canal implicite. Deux dossiers incompatibles (ni ancêtres ni descendants prouvés) donnent `CHECKPOINT_CONFLICT`, sans sélection par serial ou heure d'arrivée. Un unique dossier identique distribué sur deux canaux satisfait la comparaison, **pas une preuve d'absence de collusion de trois clés ou d'éclipse de tous les canaux**.

Deux dossiers authentifiés contradictoires interdisent leur sélection automatique comme nouvelle origine.

Sur un nœud existant, ce conflit de distribution est diagnostiqué sans modifier ni arrêter à lui seul la fork-choice locale.

La rotation de politique exige l’authentification de l’ancienne politique et les preuves de possession des nouvelles clés. Aucun timeout ne réduit les seuils.

### 12.12 Initialisation et pouvoir nul du BOOTSTRAP

Un `BOOTSTRAP` est recevable si réseau, versions, authentification, données, histoire et faits Bitcoin sont vérifiés.

Son âge seul ne le rend jamais irrecevable.

Un nœud réellement dépourvu d’origine :

1. authentifie manifeste et politique ;
2. achève la comparaison multi-canaux du §12.11 et vérifie le dossier ;
3. réconcilie Bitcoin, toutes les dépendances genesis du §11.4 et la profondeur D_btc du repère de l’origine proposée ;
4. rejoue l’histoire et contrôle les engagements ;
5. installe atomiquement origine, chaîne, ancre et mémoire des graines ;
6. initialise le journal et le témoin anti-rollback ;
7. traite ensuite les suffixes par les règles ordinaires.

Aucune activation de règle de verrou implicite n’existe.

```text
ApplyBootstrap(state, package):
    if LocalOriginPresent(state):
        return state unchanged for:
            adopted_chain
            trust_origin
            persistent_anchor
            active_registry
            control_state
            consumed_seeds
            candidate_ranks
            fork_choice_state
```

Résultat :

```text
BOOTSTRAP_IGNORED_LOCAL_ORIGIN
```

Un nœud absent, arrêté ou suspendu possède toujours son origine.

Une erreur de lecture donne `LOCAL_FAILURE` ou `RESTORE_UNVERIFIED`, jamais une permission de se déclarer neuf.

Une release ne réinitialise pas l’origine. Les blocs qu’elle transporte peuvent être soumis séparément comme données ordinaires, sans avantage administratif.

### 12.13 Âge recevable et âge maximal utile

Trois notions sont distinctes.

| Notion | Valeur ou condition |
|---|---|
| Âge maximal de recevabilité | `UNBOUNDED` |
| Âge maximal garantissant universellement la synchronisation sûre | Aucun âge démontré, même très court |
| Âge maximal utile qualifié pour un profil de déploiement | `UNESTABLISHED` en v0.6 |

Un `BOOTSTRAP` ancien reste mécaniquement exploitable si son suffixe est disponible, valide, résoluble par N et compatible avec les protections applicables. Les époques non observées ne constituent plus un obstacle artificiel.

Son utilité en sécurité dépend notamment :

- de la compromission des anciennes clés ;
- de l’évolution du poids ;
- de la disponibilité des archives ;
- de l’accès à des pairs honnêtes ;
- des branches adverses disponibles ;
- de la validité du modèle de préfixe commun ;
- de l’honnêteté de l’origine authentifiée.

H1 détecteur ne fournit pas une borne de faiblesse subjective transformable en nombre de jours.

Un profil futur pourra publier un `T_useful` conditionnel à un modèle explicite de compromission, de poids et de synchronisation. Sans ce modèle qualifié, l’API DOIT afficher `UNKNOWN` ou `UNESTABLISHED`, jamais « sûr pendant six mois » par assimilation à `G_anchor`.

Une publication au moins annuelle reste une recommandation de maintenance. Un bootstrap d’un an et davantage est un cas obligatoire du banc. Ni cette recommandation ni ce test ne constituent une expiration.

### 12.14 Récupération exceptionnelle

Une `RECOVERY` n’appartient pas au chemin de synchronisation ordinaire.

Elle engage :

- réseau, genesis, versions et politique ;
- contexte antérieur ;
- ancienne origine et ancre connues ;
- état de sûreté et graines concernés ;
- branches contradictoires ;
- préfixe retenu ;
- preuves Bitcoin ;
- état applicatif ;
- conséquences ;
- bundle complet.

Activation :

```text
--recover-checkpoint=<fichier>
--accept-new-trust-origin=<checkpoint_id>
```

Les deux paramètres sont requis. Ils ne suffisent pas à constituer une autorisation persistante.

L’acceptation :

- vise l’identifiant exact ;
- est liée à une demande locale fraîche et à usage unique ;
- ne peut être stockée comme politique générale de démarrage ;
- ne peut être rejouée automatiquement depuis une configuration, un script de redémarrage ou une ancienne sauvegarde ;
- est consommée durablement dans le journal anti-rollback.

La procédure produit d’abord le relevé des conséquences, puis exige l’acte explicite correspondant au dossier et à la demande fraîche.

#### Contexte antérieur perdu

Deux modes sont distingués dans le bundle :

```text
KNOWN_CONTEXT
LOST_CONTEXT
```

En `KNOWN_CONTEXT`, les engagements antérieurs doivent correspondre exactement à l’état local.

En `LOST_CONTEXT`, le dossier engage un **rapport de perte exact** : installation, éléments survivants, témoin externe disponible, champs inconnus, raisons de l’impossibilité de reconstruction et conséquences non quantifiables.

`previous_safety_state_root` engage ce rapport. Un champ nul ne vaut jamais joker d’acceptation.

Le mode `LOST_CONTEXT` demande une acceptation explicite de la perte de continuité ; il ne prétend pas avoir vérifié un ancien état disparu.

Avant mutation :

1. vérifier signatures, bundle, contexte et règles historiques ;
2. comparer le contexte exact ou le rapport de perte ;
3. produire les conséquences ;
4. recueillir l’acceptation ponctuelle ;
5. conserver les éléments antérieurs disponibles ;
6. journaliser durablement la rupture ;
7. installer atomiquement la nouvelle origine ;
8. revalider les conditions de production et de livraison.

La mémoire anti-double-signature disponible est conservée. Son absence ne devient pas une preuve d’absence de signature.

Aucun droit producteur n’est créé par le dossier.

### 12.15 Nœuds nouveaux ou de retour : subjectivité faible

Décision du propriétaire (D1, `DIRECTION.md` 01/10). Cette section n'ajoute aucune règle : elle délimite le domaine de la revendication CP_reg.

- **Synchronisé.** Un nœud est synchronisé tant qu'il satisfait lui-même les hypothèses réseau de H_N (§17.2) : il reçoit et valide les blocs honnêtes dans le régime D = 0, avec au plus `p_late_max` retards par fenêtre de K créneaux. Pour lui, une branche privée qui change de calendrier après `start(e)` exige, **sauf événement de probabilité au plus `T_CG`** (croissance honnête insuffisante, §5.7.2), une réorganisation au-delà de `maxreorg`, donc `HALTED_DEEP_REORG` plutôt qu'une adoption. Ce n'est pas une implication déterministe : l'espérance de blocs honnêtes ne garantit pas le nombre effectivement produit.
- **Nouveau ou de retour.** Un nœud sans origine locale, ou dont la réception est sortie de ce régime (arrêt, coupure, éclipse, retard au-delà de `p_late_max` sur une fenêtre de K créneaux), est hors domaine CP_reg. Sa pointe ou son ancre peut être antérieure à une fourche privée de plus de `maxreorg` blocs : il peut alors adopter cette branche sans déconnexion interdite. Ce risque (ε_U, ε_post) n'est pas borné ; c'est la longue portée, réapparue par le registre.
- **Retour dans le domaine.** Il ne revendique CP_reg qu'après une initialisation depuis une origine récente authentifiée (`BOOTSTRAP` A′/RELEASE, §12.10–12.12). Récente signifie postérieure d'au moins `maxreorg + 1 = 1 631` blocs à toute fourche pertinente. Ensuite, N seul gouverne : l'origine n'a **aucun pouvoir de fork-choice** sur un nœud synchronisé (§12.12, invariant 24), et aucun checkpoint n'est requis au fonctionnement ordinaire.
- Les chemins existants sont seulement l'installation sur un nœud sans origine locale (§12.12) et la `RECOVERY` explicite (§12.14). Un `BOOTSTRAP` reçu par un nœud qui a déjà une origine locale reste `BOOTSTRAP_IGNORED_LOCAL_ORIGIN` (§12.12, invariant 24).
- **Réintégration d'un nœud de retour qui conserve son origine** (décision Q1 du propriétaire, `DIRECTION.md`, « Gel v0.7 — Q1/Q3 (01/10) »). Le seul chemin est la **`RECOVERY` explicite du §12.14** :
  - un dossier `kind = RECOVERY` authentifié RELEASE (§12.10–12.11) installe une origine récente au sens ci-dessus ;
  - l'acceptation est ponctuelle et vise l'identifiant exact, avec `--recover-checkpoint` et `--accept-new-trust-origin` ;
  - le mode est `KNOWN_CONTEXT` si les engagements antérieurs du dossier correspondent exactement à l'état local ; `LOST_CONTEXT` ne s'applique que dans les conditions du §12.14 (contexte réellement perdu, rapport de perte exact). Une discordance entre contextes connus n'est pas une perte de contexte et ne déclenche aucun repli automatique ;
  - l'étape 8 du §12.14 revalide ensuite les conditions de production et de livraison.

  Les **réservations de signature et la mémoire anti-double-signature disponibles sont conservées** (§7.6, §12.14). La `RECOVERY` ne réarme aucune génération dont la mémoire est perdue et ne crée aucun droit producteur. Une fois l'acceptation consommée, le nœud revendique CP_reg aux conditions du point précédent. Jusque-là, il applique les règles ordinaires de N, hors domaine CP_reg.
- L'autre chemin existant reste la réinstallation sur un nœud sans origine locale (§12.12) : en observateur, ou en producteur avec rotation (§6.9, §7.6). Aucune règle nouvelle n'est ajoutée. La revendication CP_reg diagnostique fondée sur la compatibilité avec un `BOOTSTRAP` récent (option ii de Q1) n'est pas retenue.
- La `RECOVERY` reste exceptionnelle et ne fait pas partie de la synchronisation ordinaire (§12.14). Aucune équité de `RECOVERY` ne sert à établir une vivacité (§23.7). La procédure opérationnelle de production d'un dossier `RECOVERY` propre au contexte d'un nœud relève de la politique RELEASE (§12.11) ; la v0.7 ne la fixe pas.
- Un nœud hors domaine ne revendique aucune profondeur de sûreté chiffrée au titre de CP_reg. Un diagnostic d'API signalant cet état est une **proposition non activée** (§17.6), pas une exigence v0.7.

---

## 13. Règlement BTC/M1 à un saut

### 13.1 Contrat

Le verrou réserve les M1 au bénéficiaire si un paiement Bitcoin admissible est constaté, sinon à la destination de remboursement.

La résolution ne nécessite pas de transaction native supplémentaire du bénéficiaire. Elle reste réorganisable.

### 13.2 Création

```text
version:u16 = 0
chain_id:32
funding_ref:32
owner:32
beneficiary:32
refund_destination:32
m1_amount:u64
btc_amount_sats:u64
h0:u32
H:u32
btc_depth:u32
btc_script:V(bytes)
nonce:32
```

Taille fixe hors script, longueur comprise : **226 octets**.

```text
swap_id = H("N/SWAP", payload)
```

Conditions :

```text
m1_amount > 0
btc_amount_sats > 0
len(btc_script) ≤ 80
btc_depth = 6

h0 ≤ parent.ref.height + 1
H ≥ h0 + 12
H − h0 + 1 ≤ 144
B.ref.height ≤ H
```

Le financement autorise tous les champs et n’est consommé qu’une fois.

Toute modification du payload change l’identité et exige les autorisations correspondantes.

### 13.3 Paiement

```text
6a 28 <ASCII "NSW0" || network_tag4 || swap_id32>
```

Données : 40 octets ; script : **42 octets**.

Le marqueur n’accorde ni score ni empreinte temporelle de consensus.

Plusieurs premiers pushes reconnus `NSW0` rendent la transaction inadmissible pour tous les verrous.

Le paiement n’est pas coinbase, possède le marqueur, une sortie au script exact, un montant suffisant et une inclusion `h0 ≤ b ≤ H`.

Retenir le premier paiement dans l’ordre Bitcoin, puis la première sortie admissible par `vout`.

Un paiement ne résout pas plusieurs verrous.

### 13.4 Résolution

```text
if first admissible payment exists
   and its depth in B.ref ≥ btc_depth:
    transfer reserved M1 to beneficiary
    state = PAID

else if B.ref.height ≥ H + btc_depth − 1:
    require complete scan of [h0,H]
    require no admissible payment
    transfer reserved M1 to refund_destination
    state = REFUNDED
```

Résolutions exigibles avant les objets facultatifs, par `swap_id`.

Un verrou nouveau est examiné immédiatement.

Des données manquantes donnent `MISSING_DATA`, jamais un remboursement par défaut.

### 13.5 Discipline du payeur

Ne pas payer avant inclusion et satisfaction de la politique client.

Ne pas commencer si :

```text
best_validated_BTC.height > H − 12
```

Revérifier après attente de stabilité.

RBF n’est pas une annulation garantie. Un paiement après `H` peut transférer les BTC sans droit aux M1.

### 13.6 Rollback

Une résolution retirée est rejouée.

Un verrou retiré peut être réinclus avec les mêmes octets jusqu’à `H`, sous validité du financement et du contexte.

Un paiement Bitcoin ne recrée pas un verrou disparu. Aucune atomicité interchaînes générale n’est promise après cette disparition.

---

## 14. Densité, livraison et vivacité

### 14.1 Densité

Pour une fenêtre inclusive `[a,b]` :

```text
rho = nombre de créneaux remplis dans [a,b] / (b−a+1)
```

Les créneaux vides ou sans graine restent au dénominateur. Les ommers ne sont pas au numérateur.

Fenêtre incomplète : `UNKNOWN`, sans raccourcissement.

Pour les fenêtres courantes, la borne droite est le dernier créneau achevé selon l’horloge locale admissible. L’API expose cette borne et son incertitude.

### 14.2 Livraison

Le profil de laboratoire exige (sans risque N chiffré tant que §15/§19 ne sont pas qualifiés) :

- profondeur N au moins 77 ;
- hypothèse de poids adverse publiée ;
- densité `7/10` sur les 100 et 1 000 derniers créneaux achevés ;
- densité `7/10` de l’inclusion au dernier créneau achevé ;
- fenêtres complètes ;
- retard N au plus trois créneaux ;
- retard BTC au plus deux blocs ;
- horloge admissible ;
- aucune égalité, inconnue critique, contradiction ou arrêt pertinent ;
- origine et protections intègres ;
- exigences propres à l’objet ;
- plafond d’exposition respecté.

```text
10 × filled ≥ 7 × window_length
```

Aucune fraîcheur de checkpoint ni présence d’un ancien verrou n’est exigée.

Une reprise de production peut précéder de plusieurs fenêtres la reprise de livraison.

Le plafond d’exposition extérieure réelle au bootstrap reste **zéro**.

#### Profil de livraison H_N

Décision du propriétaire (Q3, `DIRECTION.md`, « Gel v0.7 — Q1/Q3 (01/10) »). Dérivation et vérification : `cp-reg/LIVRAISON-HN.md`. Ce profil n'ajoute aucune mécanique. C'est une instance du profil client v6 (§3.3, format inchangé) qui ne diffère du profil de laboratoire que par les valeurs ci-dessous. Son `policy_id` est donc distinct, et ses paramètres de consensus restent identiques, notamment `maxreorg = registry_min_blocks = 1 630`.

| ID §3.3 | Paramètre | Laboratoire | Profil H_N |
|---:|---|---:|---:|
| 6–7 | `rho_min`, noté `rho_deliv` dans ce profil | 7/10 | **43/100** |
| 17–18 | `beta_default` (hypothèse de poids adverse publiée) | 1/5 | 3/10 (H_N-2) |
| 19–20 | `beta_delivery_max` | 1/5 | 3/10 (H_N-2) |

Le seuil s'applique aux trois fenêtres de la liste ci-dessus : 100 et 1 000 derniers créneaux achevés, et de l'inclusion au dernier créneau achevé. Il s'écrit :

```text
100 × filled ≥ 43 × window_length
```

Toutes les autres exigences de la liste restent inchangées : fenêtres complètes, retards N et BTC, horloge, absence d'égalité, d'inconnue critique, de contradiction et d'arrêt pertinent, intégrité, exigences propres à l'objet et plafond d'exposition.

- **Un seul seuil.** Le format v6 ne porte qu'un `rho_min`. Des seuils distincts par fenêtre, par exemple 40/100 sur 100 créneaux, exigeraient un nouveau format de profil, non activé.
- **Profondeur (décision du propriétaire Q3-bis, 01/10).** La profondeur du profil de livraison H_N est **alignée sur la table K(ε) du §17.3**. Par défaut, elle vaut K(10⁻⁶) = **739 blocs** (937 créneaux ≈ 2 h 36 à τ = 10 s). Core expose la table K(ε) complète, et chaque SP/LP peut exiger une profondeur plus grande pour un ε plus petit (10⁻⁹ : 1 123 blocs ; 10⁻¹² : 1 508 blocs). À 739 blocs, la fausse livraison d'une vue éclipsée tombe à environ 1,1·10⁻²⁷ et la fausse suspension à environ 1,9·10⁻⁶ (`cp-reg/LIVRAISON-HN.md`). `k_default = 77` reste la valeur du **profil de laboratoire** seulement, sans borne de risque N (§3.3). Paramètre de profil, aucune mécanique.
Risques au coin du domaine, par calcul binomial exact avec `h' = 0,4851` et `a = 0,3049` :

| Fenêtre | Fausse suspension (chaîne honnête publique) | Fausse livraison (branche purement adverse, fenêtre seule) |
|---|---:|---:|
| 100 créneaux | 0,114 par instant | 5,5 × 10⁻³ |
| 1 000 créneaux | 2,1 × 10⁻⁴ par instant | 4,9 × 10⁻¹⁷ |
| Depuis l'inclusion, profondeur 77 | 0,052 à l'instant où la profondeur est atteinte (attente transitoire) | ≤ 5,6 × 10⁻⁴ |

Ces probabilités ne sont pas des ε de sûreté (§15.7). La fausse livraison concerne une vue éclipsée, qui est hors domaine (§12.15).

- **Paramètre de vivacité seulement.** `rho_deliv` n'est lu que par la livraison (§14.2), les statuts applicatifs (§14.5) et l'API (§16.2). Il n'entre ni dans `Select`/`BaseNDecision` (§9.5, où la politique n'intervient que par `maxreorg`), ni dans l'ancre (§9.6), ni dans les arrêts `HALTED_*`, ni dans la règle A et la dérivation du registre (§5.2–5.3), ni dans la santé, la voie lente et les exclusions (§6.6), ni dans H1 (§12), ni dans la production (§5.9, §7). Vérification bornée : `tla/modele-v0.6/NonInterference_Deliv.tla`.
- **Séparation des seuils.** Le `7/10` du §6.6 est une constante de consensus du frein, appelée ici `health_min` pour la distinguer. Elle reste 7/10, n'est pas un paramètre de profil et n'est pas modifiée. Au §14.3, `rho_min` désigne le seuil de livraison du profil actif. Pour le profil H_N, la condition `1 − alpha − beta > rho_deliv` vaut `0,4851 > 0,43` au coin (alpha inclut propagation et validation : h' = 0,49 × (1 − 10⁻²)). Le « retour à 7/10 » du §14.3 se lit « retour à `rho_deliv` ».
- **Densité observée et domaine.** `h_min` borne un paramètre de disponibilité, pas chaque réalisation du remplissage : dans le domaine, la densité observée fluctue (loi binomiale) et peut passer sous 0,49 sans que l'on soit sorti de H_N. Le seuil 0,43 est placé sous ces fluctuations avec les risques chiffrés ci-dessus, pour une fenêtre et un départ fixés ; ces chiffres ne bornent pas une attaque qui choisit sa fenêtre après lecture du calendrier public. Inversement, une densité haute ne prouve pas l'appartenance au domaine (§17.6), et la livraison ne revendique aucun ε au-delà de la profondeur exigée.

### 14.3 Vivacité conditionnelle

```text
beta  = fraction adverse des attributions
alpha = fraction de tous les créneaux perdue du côté honnête
gamma = fraction des créneaux adverses alimentant la chaîne publique

rho ≈ 1 − alpha − beta×(1−gamma)
```

`alpha` inclut pannes, propagation, validation, persistance, réservations perdues, forks, rétention, départage public et DoS ciblé.

Conditions de dimensionnement :

```text
1 − alpha − beta > rho_min
2×beta + alpha < 1
```

Pour `alpha=0,05`, `beta=0,20` :

```text
0,75 > 0,70
```

Ces inégalités ne démontrent pas la sûreté complète de N.

Sous frein, la voie lente et les rotations progressent si le support avance et si leurs conditions sont réunies ; elles ne garantissent pas à elles seules le retour à 7/10. La santé hors QUEUED du §6.6 n'est jamais substituée à la densité réelle de livraison. La règle A peut différer tout contrôle ; elle ne doit pas empêcher les producteurs restants de continuer la chaîne.

### 14.4 Suspensions sans attaque

Dans le modèle indépendant de remplissage 0,75 :

```text
P[Binomial(100,0.75) < 70] ≈ 0,103787
```

Environ 10,4 % des fenêtres courtes échouent au seul test court.

Les fenêtres glissantes sont corrélées. Ce nombre n’est ni un taux d’incidents indépendants ni une durée de suspension.

Le banc mesure durée, fréquence et regroupement des suspensions. Aucun résultat favorable n’est présumé.

### 14.5 Statuts applicatifs

```text
INCLUS
PROFONDEUR(k)
STABLE_SELON_POLITIQUE
REORGANISE
REINCLUSION_EN_ATTENTE
REINCLUS
CONFLIT
ORPHELIN_DE_CONE
EXPIRE
SYSTEME
ATTENTE_DONNEES
SUSPENDU
```

Après réinclusion, profondeur et stabilité repartent de la nouvelle inclusion.

---

## 15. Risque, grinding et exposition

### 15.1 Hypothèses

`beta` n’est pas mesuré par le nombre d’IID, la densité ou la concentration visible.

Toute évaluation indique :

- registre et période concernés ;
- poids adverse supposé et évolution `beta(t)` ;
- pertes honnêtes ;
- biais Bitcoin ;
- diversité possible des registres ;
- opportunités de départ ;
- avance privée ;
- équivoques ;
- origine de confiance ;
- hypothèses de disponibilité et de préfixe commun.

### 15.2 Course idéale et calendrier public

Le calendrier complet et ses départages sont publics dès connaissance de R_e et S_e. L'adversaire peut choisir départ, segments favorables, rétention et ciblage avant les créneaux. Connaître le calendrier ne constitue pas en soi des blocs d'avance, mais interdit de supposer sans analyse un départ indépendant de ces informations ou une avance privée nulle.

Le modèle de référence, **non une borne de N**, fixe à l'avance un départ, un registre, des tirages indépendants non biaisés, un poids adverse `0≤beta<1/2`, aucune perte honnête et égalité favorable à l'adversaire. Pour une avance privée entière a déjà présente au départ et k nouveaux blocs honnêtes attendus :

```text
p = 1−beta ; q=beta ; r=q/p
f_k(j) = binom(k+j−1,j) × p^k × q^j
P_a(k,beta) = 1                                 si a ≥ k
P_a(k,beta) = 1 − somme pour j=0…k−a−1 de
                    f_k(j) × (1−r^(k−a−j))     sinon
```

Pour beta≥1/2, borne 1 ; pour beta=0, résultat 0 si a<k, 1 sinon. La formule vient du nombre de blocs privés avant le k-ième honnête puis de la probabilité de rattrapage du déficit restant. Elle suppose que le futur n'est pas déjà conditionné par un choix adaptatif de calendrier ; ce point est une obligation distincte.

### 15.3 Cas sans avance et facteur deux

Pour a=0 seulement :

\[
P_0(k,\beta)=2\sum_{j=k}^{2k-1}{2k-1\choose j}\beta^j(1-\beta)^{2k-1-j}.
\]

Le facteur deux couvre l'égalité favorable dans cette course, pas le calendrier public, la latence du ban ni les pertes honnêtes. Il ne justifie pas d'omettre a.

### 15.4 Reprise du dimensionnement

Comparaison arithmétique à `beta=0,20`, `k=77`, `Q_B_work=256`, `M_work=14400` :

| Avance a | P_a | min(1, 256×14400×P_a) |
|---:|---:|---:|
| 0 | 1,2599810568×10⁻¹⁶ | 4,6447941679×10⁻¹⁰ |
| 10 | 8,8619217689×10⁻¹³ | 3,2668588409×10⁻⁶ |
| 30 | 3,5520583593×10⁻⁶ | 1 |
| 77 | 1 | 1 |

Ces nombres sont des résultats du modèle idéal ci-dessus. L'ancienne justification de `k=77` comme dimensionnement de N est **retirée**. Le profil conserve 77 uniquement comme seuil de comparaison de laboratoire ; aucun nouveau k sûr n'est inventé. Le risque affiché reste UNKNOWN, exposition extérieure réelle nulle.

Pour transformer un calcul en borne, qualifier a_max et sa probabilité de dépassement `epsilon_lead`, puis couvrir exhaustivement les choix adverses admissibles sur un horizon fixé. Si une borne de course s'applique à chaque choix et si leurs nombres sont réellement bornés :

```text
epsilon ≤ min(1, epsilon_lead + Q_paths × M_starts × R_paths
                    × P_a_max(k,beta) + epsilon_model)
```

`Q_paths` borne les chemins Bitcoin, `R_paths` les histoires de registre, `M_starts` les départs et choix de segments pertinents ; `epsilon_model` couvre les autres échecs explicitement bornés. Une union n'exige pas l'indépendance entre essais, mais exige une borne marginale valable pour chaque essai et une couverture complète des choix. On ne multiplie pas une probabilité non conditionnée par 14 400 en prétendant couvrir automatiquement tout arrêt adaptatif ou plusieurs époques.

Sans qualification de ces facteurs, de l'avance, de CP_reg, des pertes et de l'horizon, cette expression **n'est pas une borne applicable à N**. L'adversaire qui sait déjà le calendrier ne peut être traité comme découvrant des tirages indépendants au fil de la course.

### 15.5 Sens de Q_B et travail restant

`Q_B_work=256` est une limite de campagne (huit bits de choix dans l'abstraction), déduite ni de la garde 12 h ni de 30 confirmations. Le domaine publié H_N (§17) suppose `Q_B = 1` ; `Q_B = 256` n'y est pas qualifié. Le banc doit distinguer essais de minage et graines sélectionnables, inclure MTP, timestamps, rétention, corrélations, chemins multi-époques et dépassement de 256.

L'analyse DOIT suivre l'avance privée maximale, les segments choisis après publication du calendrier, les équivoques, l'avantage sélectif du départage et la latence réelle des bans sous la règle A. Aucune suspension anticipée d'identité hors de la machine de contrôle n'est ajoutée. Le coût de ces pertes entre dans alpha et dans les résultats de croissance/qualité de chaîne, pas dans un facteur deux supposé universel.

Une élection cachée ou VRF modifierait l'architecture ; elle n'est pas activée par cette version. Le calendrier public reste normatif et sa qualification est bloquante.

### 15.6 Registre variable et DoS ciblé

Une borne calculée pour β=0,20 n’est plus applicable si les exclusions ou admissions font dépasser cette valeur.

Le modèle dynamique suit au minimum :

```text
W_adversarial(t)
W_honest_available(t)
W_honest_unavailable(t)
excluded_honest(t)
excluded_adversarial(t)
admissions(t)
reactivations(t)
```

Les plafonds du §6.6 bornent certains changements par fenêtre, sans fournir une borne éternelle sur β.

Le modèle de course idéale ne s’étend pas automatiquement aux pertes honnêtes `alpha>0`. Toute substitution par un « β effectif » doit être justifiée dans le modèle concerné.

### 15.7 Densité et Bitcoin

L’inférence suivante est interdite :

```text
blocs privés = créneaux observés − blocs publics
```

L’adversaire peut produire public et privé sous les mêmes attributions.

La densité seule ne produit aucun `epsilon` de sûreté.

Pour Bitcoin, profondeur, part de hash adverse supposée et fréquence empirique restent distinctes.

| Part adverse BTC | Course idéale, 6 confirmations | Course idéale, 35 confirmations |
|---:|---:|---:|
| 0,10 | `5,9141216×10⁻⁴` | `3,4834×10⁻¹⁷` |
| 0,20 | `2,330841088×10⁻²` | `2,5459×10⁻⁸` |
| 0,30 | `1,5644958192×10⁻¹` | `4,9907×10⁻⁴` |

Sans modèle applicable : `UNKNOWN`.

### 15.8 Exposition

Les livraisons effaçables par une même réorganisation sont agrégées.

\[
E_w \le \min(L_{\max}, B_w/\varepsilon_w)
\]

n’a de portée que si `epsilon_w` est une borne applicable publiée.

Le coût historique des tickets n’est pas le coût marginal garanti d’une attaque.

Origine, registre, cône de dépendances ou jambe Bitcoin communs interdisent de présumer l’indépendance.

---

## 16. API

### 16.1 Catégories

- **O** : fonction objective de données explicites ;
- **L** : observation locale ;
- **M** : résultat de modèle.

Contexte obligatoire :

```text
chain_id
genesis_id
rules_version
application_spec_id
policy_id
trust_policy_id
local_origin_id
origin_kind
tip_id
tip_height
tip_slot
btc_ref
validated_BTC_view
registry_epoch
registry_root
registry_support_id
window_closure_and_block_count
registry_inherited
snapshot_cut
arguments
availability_status
```

### 16.2 Métriques

L’API expose :

- inclusion, profondeur et fenêtres exactes de densité ;
- activité, ommers, resets, suspicions et files ;
- santé hors QUEUED et dénominateurs ; budgets ordinaire/lent, fenêtres, exclusions comptées et raison d’un budget nul ;
- tickets actifs, dormants, suspendus et bannis ;
- REACT, tarifs, échéances et protection ;
- supports de registre et état de dérivation ;
- graines et mémoire de consommation ;
- preuves d’équivoque, génération au créneau prouvé et horizon ;
- provenance, comptabilité et rejets de référence ;
- couverture du scan Bitcoin ;
- rang N, ensemble maximal et décision avant H1 ;
- comparaisons H1 pertinentes et diagnostics hors périmètre ;
- décision après veto, sans « nouveau rang après filtrage » ;
- ancienne ancre, Nbound, Bbound, ancre calculée exacte et état anti-rollback ;
- état de cadence H1 ;
- âge du `BOOTSTRAP`, recevabilité et utilité qualifiée distinctes ;
- dossiers ignorés, récupération proposée et activation ;
- conséquences d’un changement d’origine.

Aucune métrique de verrou local ni de cycle temporel n’est requise.

### 16.3 Graphe

```text
provenance(object_id, branch_context)
divergence(C,Cprime,context)
reinclusion_status(transition_id,context)
supply(bitcoin_prefix,application_rules)
accounting(branch_tip)
```

Causes :

```text
CONFLIT(resource, retained_transition)
ORPHELIN_DE_CONE(ancestor)
EXPIRE(predicate, bound, context)
SYSTEME(reason)
ATTENTE_DONNEES(missing)
```

Plusieurs causes peuvent coexister.

### 16.4 Attestations et flux

Une attestation applicative utilise une clé distincte. Une observation locale n’est pas présentée comme un fait mondial signé par la clé de production.

Flux reprenable :

```text
old_tip
new_tip
common_ancestor
removed_blocks
added_blocks
affected_inclusions
reinclusion_candidates
causes
new_statuses
registry_derivation_changes
temporal_changes
origin_changes
halt_reason
```

La réception d’un `BOOTSTRAP` sur une origine existante n’émet aucun changement de chaîne, de registre ou d’origine.

---

## 17. Hypothèses publiées

### 17.1 Domaine H_N : principe

H_N fait partie du protocole. Les garanties quantitatives de N (préfixe commun, `CP_reg`, profondeurs de sûreté) ne valent que dans ce domaine. Un seul profil est publié (profil B), pour garder une frontière simple et vérifiable. Sources : `DIRECTION.md` (« Domaine H_N — décisions (01/10) »), `etudes/n-spec/SYNTHESE-BANC-TAU.md` (réserves comprises), `etudes/n-spec/cp-reg/derivation/DERIVATION-K.md`, `results/K-table.csv` et `results/composition.csv`, `cp-reg/CONFRONTATION-LEMME-L1.md` et `cp-reg/PIVOT-PROFOND-TLA.md`.

Statuts employés : **mesure** (banc, liens réels), **émulation** (netem sur liens réels), **extrapolation** (sommation multi-sauts, prolongement de courbe DP), **DP analytique** (borne exacte du modèle), **composition esquissée** (union analytique sous hypothèses, à relire), **décision** (choix du propriétaire), **hypothèse** (non vérifiée).

### 17.2 Hypothèses du domaine

| # | Hypothèse | Valeur | Statut et source |
|---|---|---|---|
| H_N-1 | Durée de créneau | `τ = 10 s` | Décision, sur banc r1/r2 |
| H_N-2 | Poids adverse, sur le **poids total** et à tout instant de l'horizon, attrition par exclusions comprise (§6.6 : `beta_after = beta_before/(1−x)`) | `β(t) ≤ β_max = 0,30` | Décision (profil B) |
| H_N-3 | Disponibilité honnête effective, DoS ciblé compris | `d(t) ≥ d_min = 0,70`, donc `h = (1−β)·d ≥ h_min = 0,49` | Décision (profil B) |
| H_N-4 | Retards honnêtes : fraction des blocs honnêtes non reçus **et** validés par **tous** les honnêtes avant `start(s+1) + 1 000 ms` | `p_late ≤ p_late_max = 10⁻²` sur **toute fenêtre de K créneaux, avec K = K(10⁻¹²) = 1 913 créneaux** (la plus longue fenêtre publiée au §17.3 ; borne, pas moyenne) | Hypothèse conservatrice ; banc : ≈ 10⁻⁵ à deux sauts W1 (extrapolation, 2 excès sur 200 000 tirages, sans borne de confiance multi-sauts) ; **non certifiée** |
| H_N-5 | H_late : retards indépendants entre créneaux, **non choisis par l'adversaire** ; un retard ciblé est une attaque, compté dans β ou hors domaine | — | Hypothèse ; non vérifiée par le banc |
| H_N-6 | Réseau de classe **W1** entre honnêtes | aller-retour ≲ 170 ms, perte ≲ 0,5 % | Décision ; émulation (r2 W1, 1 saut : p50 1,3–1,7 s, p99 3,5 s, max 4,7 s sur 721 livraisons de blocs de 256 Ko) |
| H_N-7 | Relais | au plus **2 sauts** producteur → tout honnête | Décision ; 2 sauts = extrapolation par sommation indépendante |
| H_N-8 | Horloges | écart ≤ 100 ms | Décision ; mesure : VPS ≤ 5,5 ms natif, ≤ 30 ms W1 ; nœuds macOS 85–120 ms, **à la limite** |
| H_N-9 | Validation Core par saut | `Δ_val = 100 ms` (sensibilité 250 ms) | Micro-banc cryptographique : bloc maximal ≈ 34 ms ; accès à l'état **NT** |
| H_N-10 | Condition d'existence | `(1−β)·d·(1−2·p_late) > β` : au coin, `0,49 × 0,98 = 0,4802 > 0,30`, marge `h' − a = 0,1802`, `θ = a/h' = 0,6285` | DP analytique ; condition nécessaire, non suffisante |
| H_N-11 | Condition renforcée (K raisonnable) | `d ≥ d_min(β, ε)` : à β = 0,30 et ε = 10⁻¹², `d_min = 0,524` (+≈ 0,01 à `p_late = 10⁻²`) ; marge `d_min = 0,70` contre 0,53 | Analytique + interpolation (≤ 2 %) |
| H_N-12 | Cible de sûreté | `ε_H = 10⁻⁹` sur **10 ans** (`E = 2 192` époques de 40 h) | Décision |
| H_N-13 | Graines Bitcoin sélectionnables par époque | `Q_B = 1` | Décision ; `Q_B = 256` **non qualifié** |
| H_N-14 | Origine commune | tout nœud revendiquant CP_reg est synchronisé au sens du §12.15 | Décision D1 |
| H_N-15 | Adversaire couvert | calendrier public, choix du moment, rétention, révélation optimale, équivoque (un créneau équivoqué = une unité de progrès **par branche**), abstention, départage défavorable aux honnêtes | DP analytique (règle d'équivoque vérifiée dans les trois codes) |

Réduction utilisée : un créneau honnête en retard compte comme adverse, `(a, h') = (β + h·p_late, h·(1 − p_late))` ; au coin, `a = 0,3049`, `h' = 0,4851`. K en créneaux ne dépend pas de τ (régime D = 0) ; seule `p_late(τ)` en dépend.

### 17.3 Table K(ε) du domaine

Coin le plus défavorable du profil (β = 0,30 ; d = 0,70), `p_late = 10⁻²`, borne DP publiée. K en blocs compte des créneaux non vides (équivoques comprises). Entre crochets : attaque privée exacte à dépassement strict (borne inférieure réalisable, en créneaux). Source : `K-table.csv`.

| ε par coupure | K créneaux | K blocs | Durée à τ = 10 s | [attaque privée] |
|---|---:|---:|---:|---:|
| 10⁻⁶ | 937 | 739 | 2 h 36 min | [584] |
| 10⁻⁹ | 1 425 | 1 123 | 3 h 58 min | [903] |
| 10⁻¹² | 1 913 | 1 508 | 5 h 19 min | [1 224] |

À `p_late = 10⁻³` : 844 / 1 284 / 1 724 créneaux. Un client peut confronter `k_slots` **ou** `k_blocks` à cette table ; compter les seuls blocs honnêtes visibles ne serait pas sûr. Cette table vaut **par coupure**, dans le domaine ; elle ne constitue pas une borne de livraison applicable sans la politique du §14 et du §15.8.

### 17.4 Dérivation de K_reg et registry_min_blocks

Ligne lue dans `composition.csv` : β = 0,3 ; d = 0,7 ; p = 0,01 ; τ = 10 ; ε_H = 10⁻⁹ ; Q_B = 1 ; mode `b=b_min`. Elle donne `E = 2 192`, `G = 3 600`, `ε_ep = 4,56 × 10⁻¹³`, `b = b_min = 1 629`, `K_fix = 2 066`, `K_inst requis = 6 339`, **`K_reg_min = 2 739`** (7,61 h), `b_max(K_reg) = 1 629`, `ε_H composé = 5,11 × 10⁻¹⁰`, `extrapolated = True`.

Arrondi vers le haut, documenté :

- `b` est arrondi à **1 630**. Ce choix est de vivacité : `b ≥ b_min` garde la probabilité d'un HALT forcé par l'adversaire sous ε_ep/4.
- Augmenter `b` exige d'augmenter `K_reg` d'environ `1/h' ≈ 2` créneaux par bloc : à `K_reg = 2 740`, `b_max = 1 629 < 1 630`, et le couple (2 740 ; 1 630) dépasserait le budget du pivot. `K_reg` est donc arrondi à **2 750**, première dizaine qui respecte `b ≤ b_max(K_reg)` : `b_max(2 750) = 1 634`.
- Recalcul par la même fonction (`derive_k.compose`, courbes DP publiées, sans nouvelle simulation) pour (2 750 ; 1 630) : `T_fix ≈ 5 × 10⁻⁴⁰`, `T_court ≈ 7,6 × 10⁻¹⁵`, `T_profond ≈ 1,95 × 10⁻¹³`, `T_CG ≈ 7,6 × 10⁻¹⁵`, chacun sous son budget ; `ε_ep ≈ 2,10 × 10⁻¹³`, **`ε_H ≈ 4,6 × 10⁻¹⁰ ≤ 10⁻⁹`**. À `p_late = 10⁻³`, ≈ 5,3 × 10⁻¹¹.
- `registry_min_blocks = maxreorg = 1 630` (égalité imposée par le §3.3). `fee_maturity_links = reference_protection_links = 2 880 ≥ 1 630`.
- Durées : `K_reg` = 27 500 s = 7 h 38 min ; `K_inst = K_reg + G(τ) = 6 350` créneaux ; `maxreorg` = 4,5 h à cadence pleine.

Ces valeurs sont des **dérivations conditionnelles**, pas des garanties acquises : la courbe DP (2 238 créneaux calculés) est prolongée log-linéairement au-delà de 10⁻¹⁴, et la composition des deux pivots reste une esquisse. Le couple v0.6 (7 200 / 2 880) n'était pas une dérivation ; il est abandonné.

### 17.5 Exclusions de domaine

Sont **hors domaine** : réseau W2 ou pire (≈ 340 ms, 2 % de perte : à deux sauts, la condition d'existence est violée) ; plus de deux sauts de relais ; horloges au-delà de 100 ms ; `β > 0,30` ou `d < 0,70` à un instant quelconque de l'horizon ; `p_late` au-delà de 10⁻² sur une fenêtre de K créneaux, ou retards corrélés ou ciblés ; nœuds nouveaux ou de retour avant réinitialisation (§12.15 ; ε_U et ε_post non bornés) ; `Q_B > 1` ; horizon au-delà de 10 ans. L'exclusion de W2 est un **choix de domaine**, pas un défaut démontré de N : c'est le couple (`max_body`, transport naïf) qui la fixe.

### 17.6 Comportement hors domaine

Hors H_N, N ne fait **aucune prétention quantitative** : ni ε, ni profondeur de sûreté chiffrée, ni immutabilité du registre. Les LP et services ajustent leur politique.

- **Proposition non activée (non normative en v0.7, décision du propriétaire requise)** : Core pourrait exposer, via les catégories existantes du §16.1, les paramètres du domaine (O), `p_late` observé et l'incertitude d'horloge (L), ainsi qu'un état de domaine IN, DOUTE ou OUT (L/O). Ces diagnostics ne participent à aucune décision de consensus. Le test serait unilatéral : une densité haute ne prouve pas l'appartenance au domaine.
- Les arrêts et récupérations sont ceux des règles existantes, sans ajout : `HALTED_DEEP_REORG` au-delà de `maxreorg` ou de l'ancre (§9.5–9.6) ; `HALTED_TEMPORAL_CONFLICT` et `TEMPORAL_COMPARISON_UNKNOWN` (§12) ; `HALTED_BTC` et `BTC_TIE_PENDING` (§11) ; `EQUIVOCATION_TIE_STALLED` (§9.4) ; suspension de production et de stabilité sous incertitude d'horloge (§7.5) ; suspension de livraison par densité (§14.2) ; `RECOVERY` explicite seulement (§12.14).
- **Rien ne garantit que STOP se déclenche hors domaine.** Le banc ne démontre pas qu'une sortie de domaine (W2 notamment) produit un STOP plutôt qu'une divergence silencieuse.

### 17.7 Autres hypothèses publiées

| Domaine | Hypothèse à publier |
|---|---|
| Cryptographie | Profils, implémentations et compromission des clés |
| Bitcoin | Validation, disponibilité, réorganisations, MTP et biais |
| Préfixe commun | Domaine de validité, paramètre en créneaux, probabilité d’échec |
| Registre | Poids adverse, admissions, exclusions et évolution |
| Persistance | Témoin externe, exclusivité, crash et restauration |
| Réseau | Délais, pertes, éclipse et ciblage |
| Horloge | Incertitude et comportement en cas de défaut |
| Calendrier | Public et exploitable |
| Activité | Censure, collusion et fausses exclusions |
| H1 | Complétude, cadence, retard des références et capacité de détection |
| Releases | Quatre clés, seuil 3/4, administration commune |
| Application | Bilans, consommation unique, conversions et undo |
| Livraison | Modèle, profondeur, β applicable et plafond |
| Ressources | Archives, scans et budgets |
| Récupération | Acte explicite, contexte connu ou perdu, conséquences |

Une latence p99 n’est pas une borne absolue. Plusieurs responsables déclarés ne prouvent pas leur indépendance.

---

## 18. Limites

N ne garantit pas :

- une finalité native mondiale ;
- la convergence automatique entre origines incompatibles ;
- la synchronisation sûre depuis une unique histoire sous éclipse ;
- un calendrier imprévisible ;
- un aléa Bitcoin non biaisé ;
- une protection longue portée complète par H1 ;
- un âge de bootstrap suffisant à lui seul pour garantir la sécurité ;
- un coût universel d’attaque ;
- la reprise après disparition de toutes les clés ou de tous les droits ;
- des archives perpétuellement disponibles ;
- l’absence de censure ou de DoS ;
- une purge rapide des identités inactives ;
- la réinclusion d’objets expirés ou incompatibles ;
- l’atomicité BTC/M1 après disparition du verrou ;
- l’annulation d’une livraison extérieure ;
- la conservation monétaire sans qualification applicative ;
- l’honnêteté d’une origine déduite de ses seules signatures.

Le retrait des verrous locaux corrige un obstacle artificiel à l’accord et au rattrapage. Il ne constitue pas une preuve générale de consensus pour le nouveau mécanisme.

Les arrêts profonds peuvent persister tant que le conflit demeure. La propriété de non-arrêt accidentel permanent du §23 ne prétend pas supprimer ces arrêts intentionnels.

---

## 19. Ressources et qualification

### 19.1 Conservation

Le nœud conserve ou récupère vérifiablement :

- blocs, corps et undo ;
- contrôle, historiques de clés, exclusions et preuves ;
- supports et états nécessaires à la dérivation ;
- graines consommées ;
- ancre et origine ;
- journal des adoptions ;
- réservations anti-double-signature ;
- témoin externe et procédure de rapprochement ;
- transcript Bitcoin ;
- snapshots vérifiables ;
- graphe monétaire et index temporel ;
- dossiers de bootstrap et récupération ;
- journal des changements explicites d’origine ;
- transitions candidates à réinclusion.

Les caches de registre sont jetables. Les métadonnées de sûreté ne le sont pas.

### 19.2 Budget

À dix secondes et plein remplissage :

```text
8640 blocs/jour
20908800 octets/jour de signatures principales
24364800 octets/jour d’en-têtes signés
2264924160 octets/jour de corps au maximum
```

Bitcoin et index sont exclus.

20 Go ne constituent pas une archive permanente.

Les lots bornent le travail simultané, pas le temps total de rattrapage. Les longues suites d’époques vides peuvent être accélérées uniquement par une optimisation démontrée équivalente au rejeu séquentiel.

### 19.3 Banc obligatoire

Le banc couvre :

- 12, 1 000 et 7 000 identités ;
- poids unitaires, concentration et identités lourdes ;
- un bloc livré à une moitié du réseau avant une coupure ;
- branches convergeant après une courte partition ;
- absence traversant zéro, une ou plusieurs coupures ;
- bootstrap d’un an ou davantage avec continuation unique disponible ;
- densités 0,7, 0,2, inférieures à 0,2 et nulles ;
- interruption collective prolongée puis retour de producteurs ;
- support répété sans exclusion répétée ;
- reprise sans `maxreorg` = 1 630 nouveaux blocs ;
- grand saut Bitcoin, scans interrompus et reprise ;
- β dynamique sous DoS ciblé et réactivations ;
- fenêtres dépassant 144 et 30 attributions ;
- files avec identités trop lourdes ;
- équivoque immédiatement avant rotation ;
- ommers collusifs et auto-ommers ;
- égalités longues et départage public ;
- reconstruction tardive supérieure ;
- comparaisons H1 entre perdants ;
- inconnues pertinentes et non pertinentes ;
- éclipse et H1 progressant dans un vieux préfixe ;
- réorganisation Bitcoin, travail égal et retrait de graine ;
- petits rollbacks successifs ;
- sauvegarde ancienne cohérente ;
- crash à chaque étape de commit ;
- clones et bascule de producteur ;
- récupération exacte, mauvaise, rejouée ou persistante ;
- perte partielle ou totale du contexte antérieur ;
- conservation applicative et frontières des swaps ;
- biais de graine au-delà de `Q_B_work`.

### 19.4 Conditions de gel

Restent exigés :

1. publication des quatre clés et de leur dépendance administrative ;
2. manifeste complètement instancié ;
3. gel conjoint des formats applicatifs, Bitcoin, M0 et cryptographiques ;
4. schémas complets des bundles, journaux et rapports de perte ;
5. corpus acyclique exécuté par des implémentations indépendantes ;
6. modèle formel et résultats du §23 ;
7. **CP_reg / A3 et A4 bloquantes**, analyse du préfixe commun temporel propre à N et compatibilité des ancres — état v0.7 : CP_reg analysée sous H_N avec une garantie conditionnelle et dérivée, points ouverts listés au §5.7.2 ; A4 non requalifiée ;
8. qualification du cliché en créneaux et de la garde de graine — état v0.7 : `K_reg` dérivé sous H_N (§17.4), extrapolation et composition esquissée non relues ;
9. qualification de la fenêtre de production — état v0.7 : τ = 10 s décidé sur banc, `p_late` par fenêtre non certifié (§17.2) ;
10. analyse du biais Bitcoin, du calendrier public et du DoS ciblé ;
11. qualification de la restauration et de l’exclusivité de signature ;
12. tests de conservation, rollback et récupération ;
13. résultats de disponibilité, suspensions et rattrapage ;
14. politique d’exposition approuvée.

La qualification d'une immutabilité du registre requiert hypothèses, unités, horizon et probabilité explicites pour CP_reg et A4. Un PASS C6/A5, une exploration finie ou un replay ne suffisent pas. Un scénario interrompu NE DOIT PAS être déclaré exploration exhaustive. La règle A, le veto élargi et la voie lente exigent de nouvelles campagnes ; les résultats v0.5 et du correctif D ne leur sont pas transférés.

La présente rédaction ne déclare aucun de ces résultats acquis.

---

## 20. Vecteurs et conformité

### 20.1 Primitives et tailles

```text
U16(1)   = 0001
U32(30)  = 0000001e
U64(60)  = 000000000000003c
U32LE(1) = 01000000

D("N/EMPTY", vide)
= 00074e2f454d505459

H("N/EMPTY", vide)
= 3279516fc8b867440ffdb901d8caa266dc86e6256a34e89dfa9eab12c06d8127

H("N/TEST", 00 01 … 1f)
= a6fb4a3c202bb994341409a1141160c87a3703aad545459399b68f0ba9d0c067
```

```text
KEYREG                         3929
ROTATE                         6396
TicketID                         68
TICKET script                    75
header                          400
signed header                  2820
evidence                       5640
exclusion dossier               124
bootstrap seal                  184
checkpoint core v6              588
checkpoint signature           2452
checkpoint envelope 3 sigs      7948
checkpoint envelope 4 sigs     10400
swap fixed payload              226
NSW0 script                      42
```

### 20.2 Noyau de calcul de référence

```python
from hashlib import sha256
from math import comb
from decimal import Decimal, localcontext

def u(n, size):
    return n.to_bytes(size, "big")

def D(domain, payload):
    d = domain.encode("ascii")
    return u(len(d), 2) + d + payload

def H(domain, payload):
    return sha256(D(domain, payload)).digest()

def private_race(k, beta):
    assert k >= 1 and 0 <= beta <= 1
    if beta >= 0.5:
        return 1.0
    return 2 * sum(
        comb(2*k-1, j) * beta**j * (1-beta)**(2*k-1-j)
        for j in range(k, 2*k)
    )

def private_race_advance(k, beta, advance):
    assert k >= 1 and advance >= 0
    with localcontext() as ctx:
        ctx.prec = 90
        q = Decimal(str(beta))
        assert 0 <= q <= 1
        if q >= Decimal("0.5") or advance >= k:
            return Decimal(1)
        if q == 0:
            return Decimal(0)
        p = 1-q
        return 1-sum(Decimal(comb(k+j-1,j))*p**k*q**j *
                     (1-(q/p)**(k-advance-j))
                     for j in range(k-advance))

def present(m, activity, canonical):
    return 2*activity >= m and 3*canonical >= m

def exclusion_batch(entries, budget, active_weight, slow=False):
    # entries : (queue_slot, IID, weight, state, slow_eligible)
    selected = []
    remaining, live = budget, active_weight
    for queue_slot, iid, weight, state, eligible in sorted(entries, key=lambda x: (x[0], x[1])):
        if state != "QUEUED" or (slow and not eligible):
            continue
        if weight > remaining or weight >= live:
            continue
        selected.append(iid)
        remaining -= weight
        live -= weight
    return selected

def snapshot_cut(epoch, length=14400, stability=2750):
    assert epoch >= 1
    return (epoch - 1) * length - stability

assert u(1,2).hex() == "0001"
assert u(30,4).hex() == "0000001e"
assert D("N/EMPTY",b"").hex() == "00074e2f454d505459"
assert H("N/EMPTY",b"").hex() == "3279516fc8b867440ffdb901d8caa266dc86e6256a34e89dfa9eab12c06d8127"
assert H("N/TEST",bytes(range(32))).hex() == "a6fb4a3c202bb994341409a1141160c87a3703aad545459399b68f0ba9d0c067"

assert present(144, 72, 48)
assert not present(144, 72, 47)
assert not present(144, 144, 0)
assert present(30, 15, 10)

rows = [(3, "c", 1, "QUEUED", True),
        (1, "a", 60, "QUEUED", True),
        (2, "b", 1, "QUEUED", True),
        (0, "z", 1, "ACTIVE", True)]
assert exclusion_batch(rows, 50, 1000) == ["b", "c"]
assert exclusion_batch(list(reversed(rows)), 50, 1000) == ["b", "c"]
assert exclusion_batch([(0,"a",10,"QUEUED",True)],10,10) == []
assert exclusion_batch([(0,"a",1,"QUEUED",False),
                        (1,"b",1,"QUEUED",True)],1,100,slow=True) == ["b"]

assert snapshot_cut(1) == -2750
assert snapshot_cut(2) == 11650

assert 256 * 14400 * private_race(65, 0.2) > 1e-9
assert 256 * 14400 * private_race(76, 0.2) < 1e-9
assert 256 * 14400 * private_race(77, 0.2) < 1e-9

# Comparaisons idéales, aucune qualification du calendrier de N.
assert abs(private_race_advance(77,"0.2",0) - Decimal(str(private_race(77,0.2)))) < Decimal("1e-28")
assert Decimal("3.26e-6") < 256*14400*private_race_advance(77,"0.2",10) < Decimal("3.27e-6")
assert 256*14400*private_race_advance(77,"0.2",30) > 1
assert private_race_advance(77,"0.2",77) == 1
assert private_race_advance(77,"0",0) == 0

assert 13140 + 26280 + 30 == 39450
assert 588 + 4 + 3*2452 == 7948
assert 588 + 4 + 4*2452 == 10400
```

Ce noyau ne remplace pas les vecteurs cryptographiques, Bitcoin, applicatifs, de persistance et de modèle formel.

### 20.3 Activité et exclusions

| Trace | Résultat requis |
|---|---|
| 144 attributions, 71 activités dont 48 canoniques | Suspicion |
| 144 attributions satisfaisantes, puis pertes successives | Fenêtre glissante ; anciennes réussites sortent |
| 145e attribution | Suppression de la première observation de la fenêtre normale |
| Succès ACTIVE | Aucun reset |
| 15 activités et 10 canoniques avant la 30e attribution de contestation | Annulation et reset |
| 30e attribution et échéance temporelle simultanées | Voie normale prioritaire |
| File dépassant trente attributions | Trente dernières, pas trente premières |
| Récupération et exclusion dans une transition | Récupération prioritaire |
| 144 ommers externes, zéro canonique | Présence insuffisante |
| 144 auto-ommers | Zéro crédit d’ommer |
| Après sept époques, `m=3` | Attributions insuffisantes |
| Santé hors QUEUED sous 0,7 | Voie lente ; quota global et quota lent tous deux respectés |
| Identité trop lourde en tête | Parcours poursuivi |
| Budget cumulé épuisé | Aucune nouvelle exclusion |
| Support inchangé pendant plusieurs époques | Aucune vague répétée |
| Rejeu incrémental ou par grand saut | Même état de contrôle |

Cas supplémentaires obligatoires v0.6 :

| Cas | Résultat |
|---|---|
| ADD sur ACTIVE/SUSPECT/QUEUED | Aucun reset ; historique et file conservés |
| Exclusion puis ADD dans la même transition | ADD dormant, hors k_x |
| Sous frein, W_base=1000, used=0, slow_used=0 | Budget lent min(20,50,10)=10 |
| Même cas, slow_used=10 | Budget lent 0, rotations admissibles continuent |
| W_base=99, sous frein | Arrondi lent 0 explicite, pas de max(1,…) |
| QUEUED 100 créneaux vides, autres 100 créneaux dont 80 remplis | Santé 80/100 ; densité brute 80/200 distincte |
| Aucun créneau hors QUEUED | Frein actif, pas de division par zéro |
| Sept époques sans support nouveau | Zéro exclusion ; W_f hérité à chaque époque |
| REACT référence x complète, F_x à 59/60 confirmations | Rejet terminal / examen poursuivi si autres prédicats vrais |
| Reprise avec b=H_x+4033 dès première REACT possible | Tarif plein, pas de grâce depuis notification |

### 20.4 Sélection et reprise

| Cas | Résultat |
|---|---|
| Pointes égales | Plus petit block_id des maxima productibles ; aucun nouveau départage de rang |
| Extension de score `h` | Score `h+1` |
| Deux signatures du même en-tête | Un bloc |
| Égalité pendant 100 créneaux | Alerte, pas de timeout canonique |
| Avance BTC supérieure à 144 | Aucun rejet pour ce seul motif |
| Cible BTC sous le parent | Réconciliation |
| Coupures manquées | Dérivation depuis la candidate |
| Registre reçu différent du cache | Recalcul ; pas de verrou local |
| Courte partition, même préfixe de cliché | Même registre |
| Densité inférieure à 0,2 puis retour | Production possible sans approfondissement en liens |
| Arrêt collectif prolongé, support identique | Registre conservé, nouvelles graines ordinaires |
| Candidate tentant de justifier son adoption par une ancre postérieure | Refus |
| Preuve reçue après rotation, dans l’horizon | Ban recevable |
| Preuve reçue après l’horizon | Audit seulement |
| Tous droits bannis | `HALTED_EMPTY_REGISTRY` |

Cas de frontière v0.6 :

| Cas | Résultat |
|---|---|
| Fenêtre A de maxreorg−1 / maxreorg / maxreorg+1 blocs | Héritage / support brut / support brut |
| Bloc exactement à snapshot_cut | Compté, jamais choisi comme support brut |
| Premier porteur de maturité | Compté une fois ; bloc rejeté ⇒ aucun effet installé |
| Blocs ajoutés après fermeture | Aucun nouveau compte pour cette fenêtre |
| Genesis puis plusieurs époques vides | Support genesis hérité ; premier bloc courant possible |
| Deux branches aux deux côtés du seuil | Supports différents possibles ; aucun veto de registre local |
| Ancre (maxreorg=1630) : T.height=3750, Nbound=2120, Bbound=2000, ancienne=1900 | Nouvelle=2000 |
| Même cas, Bbound=2300 | Nouvelle=2120, jamais T |
| Ancienne=2200, eligible=2120 sur même chaîne | Conserver 2200 |
| Maxima compatibles et incompatibles avec ancre | HALTED_DEEP_REORG, aucun filtrage |
| Double signature même IID/slot, registres ou générations différents | Preuve recevable si chaque clé était effective |
| Clé jamais effective à ce slot | Pas de preuve de faute recevable par cette clé |
| Retrait du scellement seul | HALTED_BTC ancien et refus d'installation neuf |
| Bitcoin lent, graine tardive | Pas d'attribution fictive, production possible dès maturité |

### 20.5 H1

| Cas | Résultat |
|---|---|
| Référence sur ancêtre commun | Aucun progrès post-divergence |
| H1 satisfaite sur une branche inférieure | Aucun gain de rang |
| Candidate maximale alertée | Veto ou arrêt, jamais promotion d’un perdant |
| H1 ajouté à un même ensemble de candidats | Adoption identique ou retirée |
| Cycle de comparaisons entre branches inférieures | Diagnostic seulement |
| Deux maxima profonds avec retard réciproque | `HALTED_TEMPORAL_CONFLICT` |
| Inconnue hors périmètre | Aucun arrêt |
| Inconnue pertinente dans fenêtre mûre | Attente des données |
| Référence REACT absente de la table exhaustive | IRRELEVANT, aucune attente de préimage étrangère |
| Donnée requise pour un dossier correspondant manquante | `UNKNOWN`, objet nommé |
| Plusieurs empreintes à même hauteur | Une étape agrégée |
| ADD utile à âge 13 141 | H1 manquée d’un bloc |
| Références progressant dans un vieux préfixe | Aucune borne post-divergence inventée |
| M0 avec référence inconnue | Importation monétaire indépendante |
| M0 avec référence N de profondeur 29 | Pas encore d’empreinte admissible |
| Même référence à profondeur 30 | Condition de profondeur satisfaite |

Cas supplémentaires v0.6 :

| Cas | Résultat |
|---|---|
| C maximale, W inférieure jamais adoptée, paire profonde, RawLag(C,W)=TRUE | HALTED_TEMPORAL_CONFLICT ; W jamais promue |
| C déjà adoptée puis W validée | Même veto, MAINTAIN ne contourne pas H1 |
| C→W / W→C / ensemble simultané | Même résultat H1 à données communes |
| Seulement RawLag(W,C)=TRUE, W inférieure | Aucun veto contre C |
| Référence x étrangère, tables complètes | IRRELEVANT sans préimage distante |
| Couverture scan mûr pertinente incomplète | TEMPORAL_COMPARISON_UNKNOWN, lacune identifiée |
| Ancien témoin toujours pertinent évincé du cache | Aucune levée silencieuse du veto |

### 20.6 Origines, restauration et récupération

Maturité des frais :

```text
origine F, parent à 2879 liens -> invalide
origine F, parent à 2880 liens -> maturité satisfaite
```

G7 exige aussi une ancre durable protégeant `F`.

La réception d’un `BOOTSTRAP` sur une origine existante laisse inchangés chaîne, ancre, registre et rangs, qu’il soit :

- ancien ou récent ;
- descendant ou contradictoire ;
- signé par trois ou quatre clés ;
- de serial supérieur ;
- transporté par une release ;
- reçu pendant rattrapage, STOP ou registre vide.

| Cas | Résultat |
|---|---|
| Sauvegarde ancienne cohérente, témoin plus récent | `RESTORE_UNVERIFIED` |
| Journal chaîné valide sans témoin de continuité | Aucune preuve suffisante de non-rollback |
| Enregistrement manquant retrouvé et conforme au témoin | Réparation mécanique |
| RECOVERY seule présente | Aucune activation |
| Un seul paramètre d’activation | Refus |
| Identifiant accepté différent | Refus |
| Acceptation persistante en configuration | Refus |
| Ancienne autorisation rejouée | Refus |
| Contexte connu différent | Refus |
| Contexte perdu sans rapport engagé | Refus |
| Rapport de perte exact et acceptation ponctuelle | Changement d’origine possible, signature encore conditionnelle |
| Fait Bitcoin invalide | Refus |
| Release contenant RECOVERY | Aucune activation implicite |
| Nœud neuf, un seul canal disponible | Attente, aucune installation mono-canal |
| Deux canaux, dossiers incompatibles authentifiés | CHECKPOINT_CONFLICT |
| Même contradiction reçue sur origine existante | Diagnostic de distribution, aucun pouvoir sur la fork-choice |

### 20.7 Engagement acyclique du corpus

Le corpus est séparé en deux couches.

#### Couche A — paquet de conformité engagé

Contient :

- schémas canoniques ;
- règles et profils de test ;
- fixtures indépendantes ;
- clés de test ;
- générateurs déterministes ;
- résultats attendus des tests indépendants ;
- programmes de génération et de vérification des tests dépendant du réseau.

Il ne contient ni le manifeste final de ce réseau, ni son `genesis_id`, ni un hash d’un résultat qui en dépend.

```text
conformance_bundle_id =
    H("N/CONFORMANCE/SPEC", canonical_layer_A)
```

Les fixtures peuvent utiliser des identifiants synthétiques constants, explicitement distincts du réseau à instancier.

#### Couche B — résultats instanciés

Après finalisation du manifeste :

1. calculer `genesis_id` ;
2. générer les vecteurs dépendants ;
3. produire blocs, signatures, registres, checkpoints, états et undo ;
4. exécuter les implémentations ;
5. publier un rapport engageant manifeste, couche A, résultats et versions d’outils.

Le hash de ce rapport est distribué avec la release, **sans être réinjecté dans le manifeste**.

Ordre des dépendances :

```text
spécifications et couche A
    -> descripteur pré-genesis
    -> faits Bitcoin et scellement
    -> manifeste final
    -> genesis_id
    -> vecteurs instanciés et résultats
    -> rapport de qualification et release
```

Aucun point fixe de hash n’est requis.

Les tests instanciés couvrent Bitcoin complet, prevouts, témoins, M0, contrôle, graines, blocs, application, checkpoints, crash, restauration et récupération.

Le corpus exécuté n’est pas réputé exister du seul fait de cette spécification.

---

## 21. Graphe et garanties G1–G10

### 21.1 G1 — Provenance

Toute ressource et unité de poids possède un chemin fini vers des sources Bitcoin typées.

Burn monétaire, ticket, REACT et paiement ne sont pas interchangeables.

Une importation consomme un droit logique unique, sans dépenser à nouveau la sortie détruite.

KEYREG seul ne crée pas de poids.

### 21.2 G2 — Conservation

Pour un transfert sans conversion :

```text
valeur(inputs) = valeur(outputs utilisateur) + frais transférés
```

L’application définit conversions, engagements et extinctions.

M0 support et M1 dérivé ne sont pas additionnés comme ressources indépendantes.

Une transition multi-entrées est indivisible, y compris en rejet et rollback.

### 21.3 G3 — Reconstruction

\[
S_{\mathrm{source}}(B)=\sum q(b)
\]

sur les sources monétaires admissibles et mûres, une fois chacune.

\[
S_{\mathrm{matérialisée}}(C)
\le
S_{\mathrm{source}}(\operatorname{btc\_ref}(C)).
\]

Les sources en attente sont publiées séparément.

Tickets, REACT et paiements de swaps sont exclus de l’offre monétaire.

Le registre exige Bitcoin et l’histoire N ; Bitcoin seul ne le reconstruit pas.

### 21.4 G4 — Identité

```text
txid = H(
    "N/TX/ID",
    chain_id || application_spec_id || typed_application_payload
)

object_id = H(
    "N/OBJECT/ID",
    chain_id || txid || U32(output_index)
)
```

Aucun bloc, producteur ou repère courant n’est ajouté implicitement.

Les sorties système peuvent dépendre d’un contexte non circulaire et ne sont pas transplantables.

Une preuve réincluse conserve ses octets, mais doit encore satisfaire l’horizon et le contexte historique de génération au créneau prouvé.

### 21.5 G5 — Divergence

Chaque transition expose versions consommées, lectures, ressources exclusives, autorisations, sorties et prédicats.

Un conflit direct consomme une même version. Un conflit contextuel peut concerner noms, quotas, registre ou lectures.

Des entrées monétaires disjointes ne prouvent pas l’indépendance.

L’API distingue `Div_objects` et `Div_context`.

Le graphe ne date pas les signatures et ne choisit pas le registre canonique.

### 21.6 G6 — Réinclusion

Les transitions retirées sont revalidées en ordre topologique.

Une transaction possédée est réincluable telle quelle si entrées, lectures, ressources exclusives, autorisations, frais, prédicats et dépendances système restent valides.

Les limites de capacité maintiennent les candidates en attente.

Aucune fusion de blocs ni inclusion garantie contre censure.

### 21.7 G7 — Maturité et persistance

Frais issus de `F`, dépensés dans `B` :

```text
links_N(F,parent(B)) ≥ 2880
```

Toutes les voies indirectes respectent cette règle.

Avant dépense locale ou revendication de G7, l’ancre doit durablement protéger `F`.

Avant NEW/ADD :

```text
links_N(reference,adopted_tip) ≥ 2880
reference appartient au préfixe protégé
```

Avant REACT, protéger `A_e`, le premier bloc matérialisant le dossier et le dossier courant non consommé.

Pour une empreinte M0, une référence protégée est recommandée sans conditionner la création monétaire.

Ces protections de portefeuille ne deviennent pas une condition de production liée au support du registre.

G7 porte sur les rollbacks automatiques. Une récupération explicitement acceptée peut modifier cette protection et doit l’annoncer.

### 21.8 G8 — Possédé et partagé

Une transaction partagée expose les versions mutables lues ou consommées.

De nouveaux effets ou versions peuvent exiger de nouvelles signatures.

Aucune réécriture automatique pour adapter une transaction à une autre histoire.

Une livraison d’objets partagés publie des exigences renforcées.

### 21.9 G9 — Verrou réincluable

```text
h0 ≤ parent.ref.height + 1
H ≥ h0+12
H−h0+1 ≤ 144
B.ref.height ≤ H
```

Le financement doit rester disponible.

Un paiement Bitcoin ne rétablit pas seul un verrou disparu.

### 21.10 G10 — Activité réintégrable

```text
1440 créneaux = 4 heures   # à tau_ms = 10 000 (2,4 h en v0.6)
```

Conditions : registre et graine compatibles, en-têtes disponibles, inclusion dans l’horizon, porteur distinct pour crédit et seuil canonique satisfait.

Une partition inférieure à 4 heures ne garantit pas l’absence de perte.

Les plafonds d’exclusion restent applicables ; les bans sont hors quota.

### 21.11 Dépendances globales

| Élément | Dépendance |
|---|---|
| Sélection | Score, départage et protections locales |
| Registre | Préfixe de cliché, admissions, activité, bans, REACT |
| Accord des registres | Propriété de préfixe commun et déterminisme |
| Calendrier | Ciblage et choix du moment d’attaque |
| Graine Bitcoin | Biais, profondeur et mémoire |
| Frais | Bloc d’origine et ancre |
| Objets partagés | Versions et ordre global |
| Empreintes | Disponibilité et résolution des faits |
| Initialisation | RELEASE 3/4 et honnêteté de l’origine |
| Fonctionnement normal | Règles mécaniques, aucune autorité de checkpoint |
| Récupération | Acceptation ponctuelle d’une nouvelle origine |
| Jambe extérieure | Bitcoin et livraison hors rollback N |

---

## 22. Signatures évolutives post-quantiques

Les signatures évolutives restent une option future non activée.

Un profil futur doit démontrer que la compromission de l’état courant ne permet pas de signer les périodes effacées, sous hypothèse d’effacement réel.

Il traite :

- périodes liées aux créneaux ;
- avancement sans production ;
- interdiction de certification rétroactive ;
- sauvegardes, clones et restauration ;
- persistance avant export ;
- exclusivité des machines ;
- épuisement et renouvellement ;
- ommers et preuves ;
- formats et budgets.

Une rotation ML-DSA ordinaire ne fournit pas cette propriété.

Une signature évolutive qualifiée ne supprime pas automatiquement les origines de confiance, ancres, mémoire Bitcoin ou conflits contemporains.

---

## 23. Propriétés à model-checker

### 23.1 Objet, portée et obligations bloquantes

La qualification est organisée autour de **A3/CP_reg (préfixes), A4 (ancres) et A5/C6 (dérivation conditionnelle)**. A5 ne remplace ni A3 ni A4. A1 ci-dessous est seulement un lemme de déterminisme. Le modèle NE DOIT PAS imposer l'accord des préfixes ou des ancres comme garde d'exécution pour annoncer ensuite leur sûreté.

Séparer invariants déterministes, sûreté sous hypothèses réseau/adversaire, progression sous équité, et arrêts intentionnels. L'exploration TLC finie recherche des contre-exemples structurels ; elle ne calcule pas à elle seule une probabilité pour les paramètres de production. Un replay ne couvre que sa trace.

Les PASS v0.5 et du correctif D n'exécutent ni la règle A, ni le veto élargi, ni la voie lente v0.6. Ils constituent des régressions historiques, jamais une qualification de cette version. **CP_reg et compatibilité des ancres restent bloquantes avant gel.** En v0.7, CP_reg dispose d'une analyse sous H_N (§5.7.2, §17) : garantie conditionnelle et dérivée, avec points ouverts ; elle n'est pas un théorème clos et ne lève pas A4. Les constantes des modèles TLA+ v0.6 sont abstraites (`KReg`, `MaxReorg` de 1 à 4) ; leurs résultats structurels ne dépendent pas des valeurs v0.7.

### 23.2 État minimal

| Sous-machine | Variables minimales |
|---|---|
| Histoires N | Arbre de blocs, créneaux, parents, producteurs, corps de contrôle, score, départages, validations |
| Temps et réseau | Créneau courant, horloges bornées, messages retenus/livrés, partitions, absences et retours |
| Bitcoin | Arbre, chainwork, MTP, inclusions et prevouts, maturités, données disponibles, dépendances genesis |
| Adversaire | Poids, clés connues par période/génération, calendrier public, branches privées, avance et choix de graine |
| Registre par branche | Supports bruts/effectifs, fermeture de maturité et compte, poids, tickets actifs/dormants/suspendus/bannis, générations |
| Contrôle | FIFO, opérations consommées, activité et resets, QUEUED, dossiers et F_x, réservations REACT, W_f et exclusions normales/lentes par époque |
| Nœud | Candidats validés V, M, pointe adoptée, origine, ancre antérieure, mémoire des graines, motifs d'attente/arrêt |
| H1 | Couverture de scan, tables Blocks/Exclusions/KEYREG, pertinence, étapes de progrès, témoins TRUE/FALSE/UNKNOWN |
| Persistance | Journal, témoin monotone externe, commit préparé, réservations (IID,slot), signatures exportées, sauvegardes/clones |
| Autorités | Canaux RELEASE, dossiers contradictoires, demande RECOVERY fraîche, autorisations consommées |
| Monnaie | Sources Bitcoin typées, imports et consommations, ressources exclusives, frais immatures, offre matérialisée, undo et état visible |

Les hashes peuvent être injectifs dans l'abstraction fonctionnelle ; les collisions restent hors modèle. Un jeton exclusif et un import suffisent au premier noyau de contrôle, pas à qualifier toutes les conversions et covenants. Les abstractions omises sont étiquetées NT, jamais PASS.

Un journal d'audit conserve les engagements par signature, adoption et installation de registre courant, avec X, e et D_e ; aucun garde du protocole ne lit ce journal pour bloquer un changement de registre. Les comparaisons couvrent plusieurs nœuds et le futur d'un même nœud. Toute réduction d'historique doit justifier les paires qu'elle conserve.

### 23.3 Actions

Le modèle permet production/omission/équivoque, révélation anticipée du calendrier, livraison/rétention, partition/réunion, absence/retour, saut d'époque, classification/préparation/activation d'opérations, observations et exclusions, rotations, adoption/réorganisation, avancement exact d'ancre, réévaluation H1 sans adoption, réorganisation Bitcoin (y compris scellement et graines), scan interrompu/repris, réception BOOTSTRAP sur nœud neuf ou existant, RECOVERY explicite, crash entre étapes de commit, restauration, clonage et compromission de clés.

L'action qui ferme une fenêtre de règle A doit distinguer parent déjà validé et en-tête en cours de validation. L'échec final d'un bloc ne laisse aucun compte, registre ou effet monétaire installé. Une action ne peut ajouter simultanément des données et faire disparaître le veto qu'elles produisent par un chemin MAINTAIN non contrôlé.

### 23.4 Agreement : A3, A4 et A5

**A1 — Lemme de dérivation.** À entrées historiques identiques, mêmes sorties de machine ; renvoi au §23.5 et à l'avertissement §23.1. Ce n'est pas une preuve d'accord distribué.

**A2 — Absence de divergence locale artificielle.** À données complètes stabilisées, même contexte externe et protections identiques, même décision. Avec protections seulement compatibles, rechercher la convergence ou les STOP explicitement motivés, sans journal de coupure ni registre mémorisé utilisé comme verrou. Pour H1, l'égalité du prédicat à V/M/Bitcoin identiques vaut même si les adoptions antérieures diffèrent (§23.8).

**A3 — Préfixe commun temporel et CP_reg.** Fixer un horizon H, un domaine H_N et un contexte X. Pour des engagements honnêtes u≤v concernant l'époque e, noter `Old_e(C)` le préfixe de C strictement antérieur à snapshot_cut(e). La propriété temporelle à analyser est la conservation de ce préfixe ancien aux engagements ultérieurs, avec absence d'insertion d'un ancien bloc concurrent avant la coupure. En particulier les engagements pertinents de (e,X) doivent avoir des préfixes anciens identiques ; la simple relation « genesis est un préfixe de tout » n'est pas suffisante pour exclure une insertion tardive.

Le moniteur registre indispensable est séparé :

```text
CP_reg(e,X) ≜ ∀ u,v honnêtes pertinents de (e,X) : D_e(C_u)=D_e(C_v)
H_N ⇒ Pr[∃ e,X dans H : ¬CP_reg(e,X)] ≤ epsilon_CP(H)
```

La dérivation de CP_reg depuis une propriété temporelle doit aussi couvrir la **fermeture et le compte de règle A** : deux branches de part et d'autre du seuil peuvent choisir des supports différents malgré un même cliché brut. Ni le recul temporel ni `maxreorg` blocs d'une seule branche ne prouvent cette implication. Le modèle conserve des témoins de désaccord de compte et de supports.

H_N précise : origine commune ; Δ sur toutes les fenêtres de l'histoire concernée, pas seulement après réunion ; erreur d'horloge ; poids adverse dynamique et corruptions anciennes ; disponibilité et récurrence honnêtes ; source, garde, biais et réorganisations Bitcoin ; rétention, ciblage et calendrier public ; horizon et composition de probabilité. Les valeurs de laboratoire beta=1/5, alpha=1/20, Δ=1 s et erreur d'horloge=0,5 s sont des points d'étude, pas un domaine prouvé. Le domaine publié est celui du §17 (profil B, W1, τ = 10 s) ; un modèle qui le cite doit en reprendre toutes les hypothèses.

Explorer séparément les traces sous hypothèses candidates et sans ces hypothèses. Densités <0,2 et époques vides sont obligatoires : aucun filtre densité≥0,4 ne doit cacher leur comportement. Si une trace sort du domaine revendiqué, identifier la première hypothèse violée et publier la trace, sans l'effacer. Si aucun domaine utile n'est démontré, qualification refusée.

**A4 — Compatibilité des ancres.** Pour deux nœuds honnêtes dans le même contexte qualifié :

```text
Compatible(anchor_i(t1),anchor_j(t2))
≜ l'une est ancêtre de l'autre, pour tous engagements pertinents t1,t2
```

Vérifier la fonction exacte min des bornes N/BTC puis max avec l'ancre antérieure, sans sur-ancrage. Les réorganisations Bitcoin sont des actions adverses, avec cadence paramétrée ; elles ne sont pas exclues silencieusement. Publier séparément violation d'ancres compatibles, mise en STOP sûre et absence de reprise automatique sous retrait de graine/genesis. La garde D_btc n'est pas une preuve universelle d'absence d'arrêt.

**A5 / C6 — Stabilité conditionnelle du registre.** Pour u engagement honnête et v engagement ou installation de registre par adoption :

```text
epoch(u)=epoch(v)=e ∧ X(u)=X(v) ∧ D_e(C_u)=D_e(C_v)
⇒ R(u)=R(v) ∧ Control(u)=Control(v) ∧ Calendar(u)=Calendar(v)
```

X n'inclut ni registre ni graine complète ; les préfixes complets, contenus et ordre sont une prémisse explicite, jamais dissimulée dans « même contexte ». Tester A5 **sans filtrer les exécutions violant A3**, conserver la sonde `RegistryImmutable` inconditionnelle et publier ses contre-exemples ou sa portée bornée si elle passe. Un PASS A5 NE DOIT PAS être rapporté comme PASS A3/A4. C6 + CP_reg donne l'accord des registres dans le domaine qualifié ; C6 seule ne le donne pas.

### 23.5 Déterminisme complet

Rejeu incrémental, grand saut et reconstruction sans cache produisent mêmes classifications, FIFO, droits, fenêtres, suspicions, resets, dossiers/F_x, W_f, budgets et exclusions, pas seulement même racine de registre. Tester l'héritage consécutif, les frontières de comptes `maxreorg−1/maxreorg/maxreorg+1`, les deux bornes inclusives et le support strictement avant la coupure.

Le premier examen distingue les types TICKET ; ADD ne réinitialise jamais une identité existante. Une table exhaustive REACT rend une référence étrangère non pertinente, sans téléchargement arbitraire. Les fonctions d'ancre, de parent de production et de sélection sont uniques à entrées fixes. Les générations distinctes ne réarment pas une réservation `(IID,slot)`.

### 23.6 Recovery

**R1 — Absence ordinaire.** Avec données disponibles et métadonnées intègres, rejoindre sans nouveau checkpoint une continuation compatible avec ancre, mémoire Bitcoin, décision de base et absence de veto/inconnue pertinent. Une histoire seulement valide ne suffit pas.

**R2 — Crash.** Chaque crash entre préparation, témoin externe et commit conduit à reprise exacte ou attente détectable, jamais adoption ni émission monétaire partielle.

**R3 — Sauvegarde.** Une sauvegarde ancienne est détectée ; aucune réservation signée n'est réarmée, générations et clones compris.

**R4 — Autorités.** Sans acceptation fraîche du dossier RECOVERY exact, origine et ancre ne changent pas. BOOTSTRAP ne modifie aucune protection d'un nœud déjà initialisé, y compris après absence, STOP ou installation de release.

**R5 — Contexte perdu.** LOST_CONTEXT exige rapport exact et acte ponctuel ; la signature ne reprend pas implicitement. Un fait Bitcoin faux, notamment scellement, ne devient pas valide par récupération.

### 23.7 Progression et absence d'arrêt accidentel permanent

Définir `CompatibleContinuation(C,state)` comme : candidate valide complète, Bitcoin réconcilié, descendants de l'ancre, déconnexion ≤maxreorg, choix autorisé par BaseNDecision et aucun veto/UNKNOWN pertinent sur V. Une contradiction bloquante réelle est une violation explicite de l'un de ces prédicats par les données validées stabilisées, ou une dépendance genesis/graine retirée. Le mot « réelle » ne sert pas à éliminer les traces gênantes sans prédicat.

Sous disponibilité finale des données et ressources de validation, état durable intègre/réparé, Bitcoin finalement non ambigu avec graines courantes mûres, existence durable d'une continuation compatible, producteurs honnêtes actifs avec **occasions de production récurrentes** et livraisons équitables, vérifier progression sans acte administratif après : faible densité, plusieurs époques vides, cache perdu, scan interrompu, coupure manquée, ancien veto devenu hors périmètre et égalité rompue.

Rechercher nommément les cycles :

- production attend profondeur, profondeur attend production ;
- exclusion attend santé, santé attend exclusion ;
- support n'avance pas, état d'activité inchangé, producteurs restants toujours capables de produire ;
- données disponibles mais ancien HALT jamais réévalué ;
- réservations consommées sur branches rivales par livraison sélective.

Pour la voie lente, vérifier une progression conditionnelle : supports avancent de façon récurrente, une identité QUEUED silencieuse reste éligible, son poids tient dans les quotas futurs, elle n'est pas le dernier poids, les budgets finissent par se libérer ⇒ elle est finalement traitée selon l'ordre de file. Tester séparément les blocages intentionnels par arrondi ou identité trop lourde. Les rotations déjà préparées et couvertes par un nouveau support ne dépendent jamais de la santé.

Équité de livraison/validation/production annoncée explicitement ; **aucune équité de RECOVERY** pour faire passer une vivacité mécanique. L'horizon fini ou un témoin d'existence ne prouve pas une continuation productive universelle. Toute perte définitive des droits/clés, destruction de données ou contradiction profonde persistante reste hors de cette garantie, avec trace explicite.

### 23.8 H1 : non-promotion, non-vacuité et ordre d'arrivée

À même état et ensemble de candidats :

```text
AdoptedWithH1 ⊆ AdoptableByBaseN
```

Cela couvre MAINTAIN/continuation, pas seulement l'action de changement de pointe. Si la base choisit C, H1 peut autoriser C ou suspendre ; jamais adopter W à sa place. En égalité, H1 ne choisit aucun maximum. Si la base s'arrête, H1 ne la réarme pas. À événements de consensus constants, modifier **seules les données du détecteur** ne change ni rang ni registre ; modifier la référence d'un vrai ticket n'est pas cette expérience.

Propriétés non vacues obligatoires :

1. Une C maximale supérieure reconstruite et une W inférieure validée profonde avec RawLag(C,W)=TRUE et témoin complet arrêtent le nœud neuf une fois les deux connues, pour C→W, W→C et réception simultanée. C déjà adoptée ne contourne pas le veto ; W n'est jamais promue.
2. Une simple annonce, une référence étrangère démontrée ou une paire entre seuls perdants n'arrête pas C.
3. RawLag(W,C)=TRUE seule, W inférieure, n'arrête pas C ; deux maxima avec retard mutuel donnent MUTUAL_LAG.
4. UNKNOWN pertinent devient FALSE ou TRUE après données ; aucune éviction de cache ne lève un témoin encore pertinent. Fenêtre non mûre : diagnostic.
5. Cadence et progrès : rechercher les faux vetos avec empreintes fréquentes mais références anciennes. La cadence 13 140 seule ne borne pas la fraîcheur du progrès ; toute propriété « aucun faux veto » doit ajouter une hypothèse explicite de couverture du progrès post-divergence et la vérifier.

La propriété d'ordre porte sur le **résultat H1 après convergence des données**, non sur l'impossibilité d'une adoption antérieure sous éclipse. Les motifs de base peuvent différer si les ancres persistées diffèrent ; ils ne doivent pas permettre à C de continuer malgré le même témoin complet.

### 23.9 Invariants complémentaires et monnaie

Invariants de contrôle : aucun rollback automatique de l'ancre ; dépendances genesis identiques chez nouveau et ancien vérificateur ; sanctions `(IID,slot)` entre registres et générations ; aucune seconde signature exportée même après restauration ; opérations consommées une fois ; plafonds d'exclusion prospectifs respectés ; aucune exclusion avec support inchangé ; aucun retrait du dernier poids ; ADD sans reset ; rotations sous frein ; canaux initiaux requis et contradiction RELEASE refusée ; aucune autorisation RECOVERY rejouée.

Classe monétaire dédiée, distincte de C6 :

- **MON1 — Provenance et offre.** À chaque état visible engagé, `S_matérialisée(C) ≤ S_source(btc_ref(C))` selon les unités et conversions de l'application ; zéro monnaie issue de tickets, REACT ou score. M0 support et M1 dérivé ne sont pas additionnés deux fois.
- **MON2 — Unicité.** Un droit d'import Bitcoin est matérialisé au plus une fois par histoire, et une ressource exclusive consommée au plus une fois. Réinclusion des mêmes octets conserve l'identité ; duplication de notification ne crée rien.
- **MON3 — Atomicité/crash.** Avant commit, aucun effet de travail n'est exposé. Après crash/undo/reprise, le visible est l'ancien ou le nouvel état complet, jamais leur mélange ; frais = transferts, récompense zéro.
- **MON4 — Indépendance du chemin de rejeu.** Deux séquences admissibles de rollback/réapplication aboutissant à la même pointe et même contexte Bitcoin donnent exactement mêmes UTXO/ressources, imports, frais et offre, pas seulement un total identique.
- **MON5 — Retrait de source.** Une source Bitcoin retirée invalide/recontextualise ses dépendants ; undo autorisé atomique ou STOP si protection franchie, jamais maintien silencieux de monnaie déclarée sûre sans source. Une référence H1 M0 étrangère n'altère pas un import par ailleurs valide.

Un petit modèle de ces propriétés ne remplace pas la qualification applicative G1–G10. Les interactions avec swaps, conversions et états partagés exigent leur propre campagne et le gel conjoint.

### 23.10 Livrables et critères avant gel

Fournir modèle exécutable, constantes/bornes, domaines H_N, hypothèses d'équité, correspondance avec champs normatifs, versions/outils/empreintes, compteurs et file finale, sorties PASS/FAIL/INCOMPLET/NT, traces et causes, mutations détectées, couverture non vacue et limites de généralisation. Les campagnes interrompues et replays ne sont jamais annoncés exhaustifs.

Conserver l'ancien invariant fort, les anciennes traces et les modèles v0.5. Tester C6 sans filtrer A3 ; tester A3 et A4 sans les présupposer. CP_reg nécessite une analyse temporelle propre à N, unités, horizon et probabilité explicites ; **C6, règle A et explorations finies ne suffisent pas à lever cette condition bloquante**. L'analyse sous H_N de la v0.7 (§5.7.2, §17.4) fournit unités, horizon et probabilité ; elle reste conditionnelle, avec une composition esquissée et une extrapolation de la DP, et l'exploration TLA+ stricte du pivot profond est INCOMPLET. Une revue indépendante et les résultats de conservation, disponibilité, calendrier public et restauration restent requis.

## 24. Table de traçabilité

Les identifiants ci-dessous désignent les avis `etudes/aveugle/n-spec-v0.5/`, sauf la dernière ligne (v0.7). Le détail des dispositions et des propositions écartées figure dans `CHANGELOG-v0.6.md` ; toutes les règles applicables sont dans cette spécification.

| Source | Disposition normative | Sections |
|---|---|---|
| DIRECTION N v0.6 (1), Codex 3, Opus 2, Sonnet 2, correctif D | Règle A, C6/A5, CP_reg bloquante, aucun verrou | 2.5, 3, 5, 19.4, 23.4 |
| DIRECTION N v0.6 (2), Opus 1 | Paires orientées M×V, témoin complet, réévaluation indépendante des adoptions | 9.5, 12.6–12.7, 23.8 |
| DIRECTION N v0.6 (3), Opus 4, Sonnet 3 | Santé hors QUEUED, voie lente, rotations permises | 6.6, 14, 23.7 |
| Codex 1 | Dépendances genesis et scellement après réorg | 5.6, 11.4, 12.12, 23.9 |
| Codex 2, Opus 5 | BaseNDecision explicite, fonction d'ancre exacte avec borne BTC | 3.3, 9.5–9.6, 11.5, 23.4 |
| Codex 4 | Premier examen typé REACT et profondeur F_x | 4.7, 6.7 |
| Codex 5 | Activité de l'identité conservée après ADD | 4.6, 6.1 |
| Codex 6 | Pertinence H1 calculable par tables exhaustives | 12.3, 12.7 |
| Codex 7, Opus 7 | Grâce ancienne explicitée, risque de perte conservé | 6.7–6.8, 21.7 |
| Opus 3 | Faute et garde (IID,slot), contextes/générations distincts | 7.4, 10.1–10.4 |
| Opus 6, Sonnet 1 | Calendrier public, avance privée, retrait de la garantie k=77 | 3.3, 15, 23 |
| Opus 8 | Époques sans support, coupure, préengagement, tri des vecteurs | 5.2, 5.6, 5.9, 6.6, 20.2 |
| Sonnet 4 | Parent déterministe en égalité, réservation non réarmée | 7.3–7.4, 9.4 |
| Sonnet 5 | Comparaison multi-canaux DOIT, refus contradictoire | 12.11–12.12 |
| Sonnet 6 | Profondeurs 30/60 distinctes justifiées | 4.7, 12.2 |
| Sonnet 7, tous avis §23 | A1 lemme, A3/A4/A5 séparées | 23.1, 23.4 |
| Sonnet 8, Opus §23 | Classe monétaire MON1–MON5 | 23.9 |
| Tous avis : interactions et §23 | Transitions complètes, cycles de vivacité, ordre d'arrivée, BTC adverse | 15, 20, 23 |
| Invariant propriétaire H1 | Veto uniquement, aucune promotion ni certification de registre | 1.4, 9.5, 12, 23.8 |
| DIRECTION Domaine H_N (01/10), Lemme L1 D1, mandat orchestrateur (01/10) — **v0.7** | τ = 10 s ; K_reg, registry_min_blocks et maxreorg dérivés ; domaine H_N publié ; nœuds nouveaux ou de retour hors domaine CP_reg ; aucune mécanique modifiée (`CHANGELOG-v0.7.md`) | Préambule, 1.3, 2.5, 3.2–3.3, 5.1–5.2, 5.7.2, 5.8, 7.2, 8.4, 9.6, 11.5, 12.15, 15.5, 17, 19.2–19.4, 20.2, 20.4, 21.10, 23.1, 23.4, 23.10 |

---

## Annexe A — Évolutions futures des autorités de bootstrap

**Cette annexe n’active aucune règle. Les modes B et C sont absents du profil de lancement.**

### A.1 Option B — Opérateurs indépendants

Piste future :

- sept clés de checkpoint ;
- sept domaines administratifs distincts et publiés ;
- seuil 5/7 ;
- vérification indépendante de Bitcoin, N, registre et comptabilité.

Sept IID ou machines d’un même propriétaire ne satisfont pas l’hypothèse d’indépendance.

Une activation exige une nouvelle spécification, une politique publiée et un consentement explicite aux nouvelles racines de confiance.

Aucun fallback automatique depuis RELEASE.

### A.2 Option C — Combinaison

Piste future :

```text
3 signatures RELEASE sur 4
ET
5 signatures OPERATORS sur 7
```

Les deux groupes signent le même dossier.

Aucun mode automatique `A OU B`.

Cette combinaison cumule les exigences de disponibilité et ne prouve pas l’indépendance des groupes.

### A.3 Contraintes conservées

Toute évolution conserve :

- aucun vote administratif dans la fork-choice N ;
- aucune expiration par âge introduite implicitement ;
- aucun checkpoint périodique nécessaire au fonctionnement normal ;
- aucun `BOOTSTRAP` appliqué à une origine locale existante ;
- aucune récupération sans acceptation ponctuelle du dossier exact ;
- aucune signature administrative rendant valide une histoire invalide ;
- aucune promesse de convergence déduite du seul nombre de signataires ;
- l’invariant selon lequel **H1 ne fait jamais adopter**.