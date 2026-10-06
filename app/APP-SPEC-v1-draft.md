> **Draft — gate RA not passed. Not normative for any network. No genesis authorisation.**
> **Brouillon — porte RA non franchie.** Ce document n'est normatif pour **aucun réseau**, n'accorde **aucune autorisation de genesis** et
> n'enregistre aucun PASS. Il ne reprend que les règles d'APP-SPEC v1 **déjà décidées**. Les autres dispositions sont signalées comme
> réservées ou non publiées selon leur statut.

# APP-SPEC v1 (M0) — référence applicative de N (version curée, brouillon)

> **N v0.7 — Architecture Frozen Candidate. Not mainnet-qualified. Not production-ready.** La couche applicative ne touche ni le moteur,
> ni ses encodages, ni H_N. Le tag `n-spec-v0.7-arch-freeze` reste intact.

## Statut et portée

- **Ce que c'est.** APP-SPEC v1 est la **référence applicative** que N-SPEC v0.7 §1.2 délègue à `application_spec_id` : elle dit ce que
  l'application M0 exige. Elle ne réécrit pas le moteur ; elle le cite. Elle s'appuie sur la révision applicative M0, qui remplace la
  lecture « M0/M1 » de N-SPEC v0.7 par un seul actif de règlement, M0.
- **Ce que ce n'est pas.** Ni un texte gelé, ni une cible de conformité, ni une spécification de formats. Les formats octet par octet et les
  vecteurs de deux générateurs indépendants restent dus avant la porte RA.
- **Sélection.** Seules les dispositions adoptées sont reprises, après retrait des éléments confidentiels et harmonisation du vocabulaire.
  Les reprises partielles n'incluent que la partie adoptée.
  - `[DÉCIDÉ]` : texte gelé de N-SPEC v0.7 (section citée) ou décision datée du projet ;
  - `[RA]` : disposition adoptée comme documentation applicative ; porte RA non franchie.

  Les règles encore en relecture, les points ouverts et les paramètres non décidés ne sont pas publiés ; leur numéro est conservé avec la
  mention *réservé — pas encore décidé*. La numérotation a donc des trous. Une règle décidée seulement en partie est reprise pour sa partie
  décidée et marquée *(partiel)*. Un élément retiré pour une autre raison est marqué *non publié*.
- **Rang.** N-SPEC v0.7 ([`spec/N-SPEC-v0.7.md`](../spec/N-SPEC-v0.7.md)) fait foi pour tout ce qui relève du moteur. Un renvoi `§x.y`
  sans nom de document vise N-SPEC v0.7.

### Note sur M0/M1 dans N-SPEC v0.7

N-SPEC v0.7 conserve sa rédaction applicative historique M0/M1. APP-SPEC v1 définit M0 comme seul actif de règlement, sans ressource M1 ni
alias `M1 := M0`. Pour le règlement §13, `amount:u64` conserve le type et la position de `m1_amount:u64`. Le moteur, les encodages N et le
tag gelé restent inchangés.

### Vocabulaire

- **M0** est l'**actif de règlement** du réseau ; paires **BTC/M0** et **X/M0** ; « verrou de règlement » dans la prose.
- Les identifiants **encodés ou techniques** gardent leur nom gelé : `swap_id`, domaine `N/SWAP`, paramètres `swap_btc_depth`,
  `swap_max_span`, `max_open_swaps`, marqueur `NSW0`, statuts §14.5. Les renommer changerait des octets ou créerait un écart avec les
  vecteurs.
- **Identité enregistrée** (*registered identity*) : identité enregistrée par TICKET (§4). **Producteur** (*producer*) : rôle de
  production des blocs (anciennement appelé « opérateur »).

---

## §0 Statut, conventions et règles de lecture

### 0.1 Rang du document

- **GEN-1.** `[RA]` N-SPEC v0.7 fait foi pour tout ce qui relève du moteur (§2, §4.1–4.8, §5–§12, §14–§17, §20.2–§20.7, encodages N, H_N).
  L'APP-SPEC ne modifie aucun octet, aucune valeur et aucune règle du moteur.
- **GEN-2.** `[DÉCIDÉ (03/10/2026)]` Toute contradiction entre ce document et N-SPEC v0.7 est un défaut de ce document. Elle se traite par STOP avec
  contre-exemple minimal, jamais par une lecture qui modifie le moteur.
- **GEN-3.** `[RA]` Partout où N-SPEC v0.7 nomme M1, « M0/M1 », « M1 dérivé » ou « BTC/M1 », c'est le texte de ce document qui
  s'applique. Il n'existe **aucun alias** `M1 := M0` : M1 est absent, ni renommé ni réservé comme ressource.

### 0.2 Marqueurs de statut

Voir « Statut et portée » ci-dessus.

### 0.3 Catégories et verdicts

- Catégories normatives : celles de N-SPEC §1.1 (validité historique, adoption locale, discipline de production, politique client).
- **GEN-4.** `[DÉCIDÉ (N-SPEC §9.1, §8.8)]` Une règle de **validité applicative** rend l'un des verdicts du moteur (§9.1) : `VALID`, `INVALID` (invalidité historique
  démontrée sur l'état engagé complet du parent), `MISSING_DATA` (donnée nécessaire absente ou couverture non vérifiée), `RESOURCE_LIMIT`
  (travail différé), `LOCAL_FAILURE` (état local illisible ou incohérent). Un objet applicatif `INVALID` invalide le bloc (§8.8).
- **GEN-5. Attendre ou s'arrêter, jamais se tromper** `[DÉCIDÉ]`. Une donnée absente, une couverture
  partielle ou un état local indisponible ne donnent **jamais** `INVALID`, jamais un remboursement par défaut, jamais une conclusion
  d'absence, jamais un « inconnu donc accepté ». Deux nœuds qui disposent des mêmes données ne peuvent pas rendre des verdicts de validité
  divergents pour le même bloc selon leur cache.

### 0.4 Vocabulaire et identifiants gelés

`[DÉCIDÉ]` Voir « Vocabulaire » ci-dessus. Termes employés dans ce document :

| Terme | Définition dans ce document |
|---|---|
| unité atomique M0 | 1 sat ; tout montant M0 **non signé** est un entier en unités atomiques |
| sortie transparente | sortie M0 de l'état UTXO applicatif, verrouillée par un script |
| M0 réservé | montant `amount` d'un verrou §13 ouvert, hors UTXO (`L`) |
| M0 shieldé | valeur du pool Sapling (`Z`) |
| repère du bloc | `B.ref`, bloc Bitcoin désigné par l'en-tête N (§8.4) ; seule vue Bitcoin qu'une règle applicative du bloc `B` peut lire |
| droit d'import | droit d'import défini par une sortie de burn M0 v3 admissible (§IMP) |
| liens N | `links_N(B,T) = T.height − B.height` (§2.5) |
| créneau N | `slot`, de durée `tau_ms` depuis `T0_ms` (§5.1) |

---

## §ID Identifiant applicatif `application_spec_id`

- **ID-1** `[RA]` La spécification applicative du premier réseau N est **APP-SPEC v1 (M0)**. C'est la première valeur instanciée de
  `application_spec_id` ; la lecture « M0/M1 » de N-SPEC v0.7 n'a jamais été engagée et ne reçoit aucun identifiant.
- **ID-2** `[RA]` `application_spec_id = H("N/APP/SPEC", app_spec_bundle)`, au sens de §2.2. Le domaine `N/APP/SPEC` est
  distinct de `N/CONFORMANCE/SPEC`.
- **ID-3** — *réservé — pas encore décidé* (encodage canonique du paquet et de ses annexes).
- **ID-4** `[RA]` L'entrée du hash exclut toute auto-empreinte, le manifeste final et tout vecteur qui dépend de l'identifiant réel
  (même discipline acyclique que §20.7).
- **ID-5** `[DÉCIDÉ (N-SPEC §3.1, §5.6)]` L'identifiant est engagé par le manifeste v6 et par le descripteur pré-genesis ; un identifiant nul
  est interdit dans un manifeste activable. Les octets canoniques du paquet sont disponibles (§3.1 « Les documents engagés sont disponibles
  en octets canoniques »).
- **ID-6** `[RA]` L'identifiant est engagé par `txid` (G4, §21.4), par le domaine du **sighash applicatif** (§SCR, SIGHASH)
  et par le domaine du **gabarit CTV** (§SCR, CTV). Conséquence assumée : toute version applicative ultérieure change les `txid`, les
  identités des descendants pré-signés, les sighash et les gabarits (§VER).

---

## §M0 Ressource M0, unités et état engagé

### M0.1 Ressource et unités

- **M0-1** `[RA ; DÉCIDÉ]` APP-SPEC v1 définit **un seul actif de règlement : M0**, sous trois formes :
  transparente (UTXO), réservée (verrou §13 ouvert) et shieldée (pool Sapling). **Aucune ressource dérivée n'existe au genesis** : ni
  reçu, ni coffre, ni couleur, ni jeton dont la valeur se définit par rapport au M0.
- **M0-2** `[RA]` Un burn de `q` sats importé crée exactement `q` unités atomiques M0 (1 unité = 1 sat).
- **M0-3** `[RA]` Tout montant M0 **non signé** (valeur de sortie, `amount`, frais, `Z`, `L`) est un `u64` en
  unités atomiques, compris dans `MoneyRange` = [0, 21 × 10¹⁴]. **`valueBalance` est signé** (`i64`) : une valeur négative, qui représente
  un dépôt `t→z`, est valide ; sa **valeur absolue** est ≤ 21 × 10¹⁴. Les agrégats (somme des entrées, somme des sorties, somme des frais
  d'un bloc, `Z` après chaque transaction, `L`) sont calculés en arithmétique exacte et doivent rester dans `MoneyRange` ; tout dépassement
  rend la transaction ou l'objet invalide ; aucun calcul n'est fait modulo la taille de l'entier (§2.1).
- **M0-4** `[DÉCIDÉ (N-SPEC §1.4 inv. 1 et 12, §3.2)]` TICKET, REACT, KEYREG, ROTATE, score et récompense créent zéro M0 ; la récompense de
  bloc vaut 0 ; les frais transfèrent une ressource existante.

### M0.2 État applicatif engagé

- **M0-5** — *réservé — pas encore décidé* (liste exacte des éléments de l'état applicatif engagé).
- **M0-6** `[RA]` Les éléments de l'état applicatif engagé vivent dans l'état engagé par `application_state_root`, jamais dans `CBlockIndex`, un index
  facultatif ou une base latérale.
- **M0-7** — *réservé — pas encore décidé* (construction d'`application_state_root`).
- **M0-8** `[DÉCIDÉ (N-SPEC §8.3)]` `state_root = H("N/STATE", kernel_commit || application_state_root)` ; les sorties système utilisent un
  contexte calculable avant `application_state_root`, sans circularité avec `block_id`.

### M0.3 État initial

- **M0-9** `[RA]` L'état applicatif initial de `ntest` est **vide** : zéro M0 transparent, zéro import, aucun verrou, aucun reçu, arbre
  Sapling vide, `Z = 0`. Aucune prémine. `initial_application_state` encode cet état vide.
- **M0-10** — *réservé — pas encore décidé* (sort des burns antérieurs à `h_start` et des burns au format legacy).

### M0.4 Fonction `Apply` et ordre d'exécution

- **M0-11** `[DÉCIDÉ (N-SPEC §8.8, §9.2)]` `Apply(parent_state, objects, bitcoin_context, system_effects)` est déterministe et atomique,
  indépendante du mempool, des pairs et de l'horloge locale. `bitcoin_context` est la vue au repère `B.ref` et ses faits extraits ; aucune
  autre vue Bitcoin n'est lue.
- **M0-12** — *réservé — pas encore décidé* (ordre applicatif dans un bloc).
- **M0-13** `[DÉCIDÉ (N-SPEC §8.5, §9.1) ; RA]` Les résultats partiels ne sont jamais visibles. Un état local indisponible
  (parent non chargé, undo absent, base illisible) donne `MISSING_DATA` ou `LOCAL_FAILURE`, jamais `INVALID`. L'invalidité applicative
  n'est prononcée que sur l'état engagé complet et vérifié du parent.

---

## §OBJ Objets, transactions applicatives et types

### OBJ.1 Objets du corps lus par l'application

- **OBJ-1** `[DÉCIDÉ (N-SPEC §8.2) ; RA]` L'application exécute les objets `0001` (transaction applicative typée) et `0004`
  (**création d'un verrou de règlement BTC/M0**, §13). Elle fournit en outre aux objets moteur `0002` (KEYREG) et `0003` (ROTATE) leurs
  **reçus de frais** (§FEE). Code de type, position, encodage et taille du `0004` (226 o hors script) sont inchangés ; seul le libellé change.
- **OBJ-2** `[DÉCIDÉ (N-SPEC §8.2)]` L'enveloppe `0001` est `version:u16 = 1 || access_mode:u8 || application_transaction:V(bytes)`,
  avec `00 = POSSEDE`, `01 = PARTAGE` ; le mode est vérifié et signé par l'application ; aucune autre valeur n'est acceptée.
- **OBJ-3** — *réservé — pas encore décidé* (formes partagées en v1).

### OBJ.2 Transaction applicative (`application_transaction`)

- **OBJ-4** `[RA]` La transaction `0001` n'accepte qu'une **liste fermée** de formes définies par APP-SPEC v1 ; toute autre
  forme invalide la transaction, donc le bloc (§8.8).
- **OBJ-5** — *réservé — pas encore décidé* (encodage de la transaction, projections d'identité et de signature).
- **OBJ-6** — *réservé — pas encore décidé* (contraintes structurelles sur entrées et sorties).
- **OBJ-7** `[DÉCIDÉ (N-SPEC §21.2)]` Conservation d'un transfert : `Σ entrées transparentes + max(valueBalance, 0) = Σ sorties
  transparentes + max(−valueBalance, 0) + frais`, avec `frais ≥ 0` ; une transition multi-entrées est indivisible, y compris en rejet et
  rollback.

### OBJ.3 Anciens types refusés et numéros réservés

- **OBJ-8** `[RA ; DÉCIDÉ]` *(partiel)* Sont **refusés** et leurs numéros **réservés, jamais réutilisés** avec un
  autre sens : aucune règle ne leur est attachée sauf le rejet.

  | Numéro legacy | Nom legacy | Motif |
  |---:|---|---|
  | 1–4 | `PROREG`, `PROUPSERV`, `PROUPREG`, `PROUPREV` | ancien registre de consensus abandonné |
  | 20 | `TX_LOCK` | M1 retiré |
  | 21 | `TX_UNLOCK` | M1 retiré |
  | 22 | `TX_TRANSFER_M1` | M1 retiré |
  | 31 | `TX_BURN_CLAIM` | l'import passe par §IMP |
  | 32 | `TX_MINT_M0BTC` | l'import passe par §IMP, sans statut `FINAL` (§1.4 inv. 18) |
  | 33 | `TX_BTC_HEADERS` | données Bitcoin par le scan du moteur (télécharger, vérifier, scanner, jeter) |
  | 34 | `TX_OPERATOR_LEASE` | ancien registre de consensus abandonné |
  | 40–45 | `HTLC_CREATE_M1`, `HTLC_CLAIM`, `HTLC_REFUND`, `HTLC_CREATE_3S`, `HTLC_CLAIM_3S`, `HTLC_REFUND_3S` | HTLC natifs retirés ; les HTLC sont des scripts génériques sur M0 |

  Une transaction au format de sérialisation legacy n'est pas décodable comme `application_transaction` et invalide l'objet.
  (La correspondance de ces numéros avec l'encodage de v1 est réservée — pas encore décidée.)
- **OBJ-9** `[RA]` Il n'existe ni coffre, ni reçu M1, ni couleur, ni base latérale, ni exception de comptabilité.
- **OBJ-10** `[RA]` Claim par préimage, remboursement par délai, trois secrets, pivot à covenant : **scripts génériques** sur M0
  (BIP-199 et §SCR), sans règle de consensus propre.

---

## §IMP Import M0 des burns Bitcoin

### IMP.1 Source unique

- **IMP-1** `[RA]` Le M0 n'est créé que par l'import d'un burn M0 v3 admissible (`MonetaryBurnValid`). Toute autre transition
  crée zéro M0 (MON1).
- **IMP-2** `[RA ; DÉCIDÉ (N-SPEC §4.9, §4.10, §1.4 inv. 19)]` Un burn de `q` sats crée exactement `q` unités ; aucun frais
  n'est prélevé à l'import ; la référence temporelle optionnelle n'a aucun effet sur le montant ni sur le droit : référence absente,
  inconnue, sur A ou sur B produit le même droit d'import. `MonetaryBurnValid` et `TemporalReferenceValid` sont deux prédicats séparés.

### IMP.2 Burn M0 v3 (forme exacte)

- **IMP-3** `[DÉCIDÉ (N-SPEC §4.9)]` « Selon la forme monétaire, un payload de 29 ou 30 octets devient 61 ou 62 octets. » Les longueurs
  admises de la donnée de métadonnées sont exactement **29, 30, 61, 62** ; la présence de la référence se lit par la longueur, jamais par
  devinette.
- **IMP-4** `[DÉCIDÉ (N-SPEC §3.4, §4.9)]` *(partiel)* Le texte gelé
  fixe deux contraintes et **délègue** les formes exactes à l'application : (1) le discriminant réseau est le `network_tag` de **4 octets**
  du registre publié commun à M0 v3 et TICKET (§3.4) ; (2) la donnée de métadonnées mesure **29 ou 30 octets** sans référence, **61 ou 62**
  avec la référence de 32 octets (§4.9). Le format exact dans ces contraintes est réservé — pas encore décidé.
- **IMP-5** — *réservé — pas encore décidé* (règle de sorties multiples et reconnaissance des métadonnées).
- **IMP-6** `[DÉCIDÉ (03/10/2026)]` Les burns faits dans une transaction **coinbase** Bitcoin sont **exclus** de
  l'import M0 : une coinbase ne définit aucun droit d'import.
- **IMP-7** `[DÉCIDÉ (N-SPEC §4.10)]` Un mauvais réseau produit zéro droit et zéro empreinte sur le réseau examiné. Toute divergence entre
  parseurs sur le réseau, l'importation ou les sorties multiples interdit le gel.
- **IMP-8** `[DÉCIDÉ (04/10/2026)]` Le montant minimal d'un burn importable est de **1 000 sats**, sur ntest et le mainnet.
- **IMP-9** — *réservé — pas encore décidé* (types de destination de la sortie d'import).

### IMP.3 Droit, marqueur et unicité

- **IMP-10** `[RA]` `import_id = H("N/APP/IMPORT", chain_id || btc_txid || U32(vout))`, où `(btc_txid, vout)` est
  l'outpoint de la sortie de burn (octets bruts du condensat, §2.2). Une variante malléée du burn ne coexiste pas avec l'original dans une
  même histoire Bitcoin valide : si une réorganisation Bitcoin la substitue, l'import original est défait par rollback (IMP-15) et la
  variante devient une **autre** source ; les descendants peuvent devoir être re-signés.
- **IMP-11** `[RA]` L'ensemble des `import_id` matérialisés fait partie de l'état engagé. Un marqueur survit à la dépense du M0
  importé et n'est retiré que par l'undo du bloc qui l'a créé. Doublon dans un bloc ou entre blocs : rejet atomique (MON2).
- **IMP-12** `[RA ; DÉCIDÉ (04/10/2026)]` Un import n'utilise qu'un burn contenu dans l'ascendance de `B.ref`,
  avec au moins `import_maturity_btc` confirmations Bitcoin **dans `B.ref`** (confirmations inclusives). Aucune vue Bitcoin locale plus récente ou différente n'est lue. `import_maturity_btc = 30` confirmations inclusives dans `B.ref`, sur ntest et le mainnet.

### IMP.4 Matérialisation

- **IMP-13** `[DÉCIDÉ (03/10/2026)]` L'import est **automatique** : au bloc `B`, l'application importe tout
  burn admissible dont la maturité est atteinte dans `B.ref` et pas encore matérialisé, dans l'ordre canonique (hauteur Bitcoin, position de
  la transaction dans son bloc, `vout`). **Aucune réclamation n'est exigée** et aucun producteur ne peut ignorer un burn mûr : un bloc qui
  omet un import exigible (hors report de quota, IMP-13 bis) est invalide sur état complet ; un état ou une couverture indisponible donne
  `MISSING_DATA`.
- **IMP-13 bis** `[DÉCIDÉ (03/10/2026), principe seulement]` *(partiel)* Un **quota d'imports par
  bloc** est fixé **après mesure**. S'il existe, il est **déterministe** (file FIFO reportée au bloc suivant, comme les FIFO
  d'admission §4.8) et règle seulement le délai d'accès aux fonds ; il n'est jamais un `RESOURCE_LIMIT` ni une adaptation au CPU local. Sa valeur (ou son absence) est réservée — pas encore décidée.
- **IMP-13 ter** `[DÉCIDÉ (03/10/2026)]` *(partiel)* La **publication des données
  d'accompagnement** (transaction Bitcoin, preuve de Merkle, transaction précédente, témoins) peut être faite **par n'importe qui**
  (utilisateur, producteur, service). Ce n'est pas une réclamation : **aucun acte de publication distinct
  n'est exigé ; les données vérifiées restent nécessaires**. La publication ne confère aucun droit ni priorité, son auteur n'est pas engagé, et chaque nœud vérifie ces données contre ses en-têtes ; sans données vérifiées, le nœud rend `MISSING_DATA`. (Le canal de transport est réservé — pas encore décidé.)
- **IMP-18** — *réservé — pas encore décidé* (identité de la sortie d'import).
- **IMP-14** `[RA]` Deux sommes distinctes : `S_mat(C)` (imports matérialisés dans l'histoire N) et `S_src(btc_ref(C))`
  (burns admissibles et mûrs dans la vue, exhaustifs) ; `S_mat ≤ S_src` (G3). Les sources en attente (admissibles mais non mûres, ou
  reportées par quota) sont publiées à part, hors offre.

### IMP.5 Retrait du burn

- **IMP-15** `[RA ; DÉCIDÉ (N-SPEC §11.2, MON5)]` Si la vue Bitcoin de travail maximal retire le burn, le bloc N dont le repère
  disparaît devient `BTC_ORPHANED` avec tous ses descendants ; rollback atomique ou STOP (`maxreorg`, ancre). Les dépendants transparents,
  réservés ou shieldés sont défaits **par le rollback de bloc**, sans traçage des notes. La provenance suit
  Bitcoin, jamais l'inverse.
- **IMP-16** `[DÉCIDÉ (N-SPEC §11.2)]` La disparition d'une **référence N** d'un burn M0 n'annule pas l'importation.

### IMP.6 Données Bitcoin

- **IMP-17** `[RA ; DÉCIDÉ]` Tout fait applicatif (import, paiement §13, BTCSTATE) provient du scan
  « télécharger, vérifier, scanner, jeter » du moteur (§4.8, §8.5), au repère du bloc. « Jeter » vise les blocs bruts : le nœud
  **conserve** les faits extraits, preuves et états de couverture nécessaires au rejeu et au rollback (au moins sur `maxreorg` et jusqu'à
  résolution des verrous §13 ouverts), ou sait les **récupérer vérifiablement** ; sans eux : `MISSING_DATA`, jamais une conclusion d'absence.

---

## §BTC Faits Bitcoin applicatifs

- **BTC-1** `[DÉCIDÉ]` Une seule vue et un seul scan, partagés avec le moteur. Un fait applicatif est lu
  **au repère du bloc** `B.ref`, jamais au-delà, jamais sur une vue locale plus récente.
- **BTC-2** `[DÉCIDÉ]` La **couverture** d'un intervalle est liée aux **hashes** des blocs Bitcoin de la branche, pas à
  des hauteurs ; une réorganisation Bitcoin invalide ou recontextualise couverture, curseurs et caches.
- **BTC-3** `[DÉCIDÉ]` Trois classes de prédicats, chacune avec ses données exigées :

  | Classe | Exemples | Données exigées |
  |---|---|---|
  | présence | paiement prouvé, BTCSTATE `TX_CONFIRMED`, en-tête (difficulté, MTP, hauteur) | en-têtes de `B.ref` + transaction + preuve de Merkle |
  | authentification d'une entrée | prevout, montant, script, témoin d'une entrée Bitcoin | transaction, preuve, prevout et témoin vérifiés (`wtxid`, BIP141), sans scan exhaustif |
  | absence, complétude, premier événement | import exhaustif, **premier** paiement §13, absence de paiement avant remboursement | **scan exhaustif** vérifié de l'intervalle sur la branche |

- **BTC-4** `[DÉCIDÉ]` Données manquantes ⇒ `MISSING_DATA` (ou attente), jamais conclusion d'absence ; une source RPC
  tierce n'est pas une autorité ; un bloc Bitcoin falsifié, tronqué ou réordonné est rejeté contre l'en-tête.

---

## §SCR Scripts, covenants du socle et délais

### SCR.1 Socle actif au genesis

- **SCR-1** `[DÉCIDÉ ; RA]` *(partiel)* Opcodes de covenant et de délai **actifs au genesis** : `OP_CHECKLOCKTIMEVERIFY`
  (CLTV), `OP_CHECKSEQUENCEVERIFY` (CSV, qualifié), `OP_TEMPLATEVERIFY` (CTV) **dans la forme définie en CTV-1 seulement**, `OP_BTCSTATEVERIFY`
  (BTCSTATE). Le langage de script de base (hash, comparaison, multisig, hashlock) est celui du socle, avec les encodages canoniques.
  **Signatures utilisateur** : ECDSA secp256k1 (signature basse-S, clé comprimée valide, §2.4) est la seule
  vérification **déjà spécifiée**, ce qui n'est pas une décision ; les opcodes de signature de v1 sont réservés — pas encore décidés.
- **SCR-2** `[RA]` *(partiel)* `OP_CHECKSIGFROMSTACK` (CSFS), `OP_CAT`, `OP_CHECKOUTPUTVALUE`, `OP_CHECKOUTPUTSCRIPT` sont **inactifs** :
  leur exécution fait **échouer le script**, sans NOP permissif. Toute activation ultérieure exige une révision applicative coordonnée
  (§VER), opcode par opcode, sur preuves ; aucune promesse de soft fork.
- **SCR-3** — *réservé — adoption à documenter*.
- **SCR-4** — *réservé — adoption à documenter*.

### SCR.2 Échéances absolues en créneaux N (CLTV)

- **CLTV-1** `[RA]` Les échéances **absolues** des gabarits interchaînes s'expriment en **créneaux N** : un créneau suit le temps
  (`start_ms(s) = T0_ms + s × tau_ms`), alors qu'une hauteur N peut glisser sous faible densité.
- **CLTV-2** — *réservé — pas encore décidé* (champ, origine et bornes du verrou absolu).
- **CLTV-3** — *réservé — pas encore décidé* (validité d'une transaction sous verrou absolu).
- **CLTV-4** — *réservé — pas encore décidé* (sémantique de l'opérande de `OP_CHECKLOCKTIMEVERIFY`).

### SCR.3 Délais relatifs en liens N (CSV)

- **CSV-1** `[RA ; DÉCIDÉ]` Les délais **relatifs** s'expriment en **liens N**, comptés entre le
  bloc `O` qui contient la sortie dépensée et le bloc `B` qui contient la dépense, sur la branche examinée : `links_N(O, B) = B.height −
  O.height`, recalculés par branche. Le type « temps » de BIP-68 est refusé ; un délai relatif n'est jamais compté en créneaux.
- **CSV-2** — *réservé — pas encore décidé* (encodage et validité des délais relatifs).
- **CSV-3** — *réservé — pas encore décidé* (sémantique de l'opérande de `OP_CHECKSEQUENCEVERIFY`).
- **CSV-4** `[RA]` **« CSV qualifié »** : sémantique en liens N écrite, vecteurs à deux générateurs, et mutants tués (« enfant expiré
  créé », « CSV type temps accepté », « délai relatif compté en créneaux au lieu de liens », réorganisation entre création de l'enfant et
  dépense). **Sans CSV qualifié, pas de genesis**.

### SCR.4 Limites publiées des délais

- **SCR-5** `[RA]` Les hauteurs Bitcoin du §13 (`h0`, `H`, `btc_depth`) ne changent pas. Ni les créneaux ni les liens ne garantissent
  qu'une transaction sera **observée ou incluse** avant une échéance externe (censure, indisponibilité, réorganisation) : ce sont des bornes
  de validité, pas des garanties de livraison. Cette limite est publiée (§PUB).

### SCR.5 CTV

- **CTV-1** `[RA ; DÉCIDÉ]` `OP_TEMPLATEVERIFY` n'est actif que dans sa **forme définie ci-dessous**. Le gabarit engage, en
  plus de la version, du type, du verrou absolu, du nombre d'entrées, des délais relatifs et des sorties :
  1. **l'index de l'entrée en cours** (comme BIP-119) ;
  2. **l'absence de données Sapling** : une transaction qui satisfait un CTV a un bundle Sapling **vide** (`valueBalance = 0`, aucun spend,
     aucun output) ;
  3. `chain_id` et `application_spec_id`, dans le domaine du hash du gabarit, par une projection distincte de celle du sighash.
- **CTV-2** — *réservé — pas encore décidé* (hash du gabarit).
- **CTV-3** `[RA]` Une forme plus riche (engager `valueBalance` et la liste des `cmu`) **ne suffit pas** à qualifier une extension :
  projection complète, ordre, autorisations, données de récupération et absence de circularité restent à démontrer ; jamais un engagement
  naïf des preuves ou signatures. v1 n'en définit aucune.
- **CTV-4** — *non publié*.

### SCR.6 Sighash applicatif

- **SIGHASH-1** `[RA]` Le domaine du sighash applicatif engage `chain_id` et `application_spec_id`, par une projection qui exclut
  ses propres signatures ; la spécification applicative fixe les deux projections (sighash, gabarit CTV) et prouve leur absence de circularité.
- **SIGHASH-2** — *réservé — pas encore décidé* (calcul du sighash).

### SCR.7 BTCSTATE

- **BTCSTATE-1** `[RA ; DÉCIDÉ]` `OP_BTCSTATEVERIFY` est actif et évalué **au repère du bloc** `B.ref`
  seulement. Une marge locale n'est pas une règle de validité ; un fait retiré passe par le rollback du repère
  (§11.2).
- **BTCSTATE-2** `[RA]` BTCSTATE est un **prédicat générique de présence, non consommant** : en mode `TX_CONFIRMED`, il vérifie qu'un
  fait existe dans la vue au repère du bloc ; plusieurs scripts peuvent être satisfaits par le même fait Bitcoin. Ce n'est pas un mécanisme
  de règlement à paiement unique ; un contrat qui a besoin de l'unicité passe par le §13. Aucune promesse d'unicité universelle n'est faite.
  Le mode `TX_CONFIRMED` reste actif.
- **BTCSTATE-3** — *réservé — pas encore décidé* (requêtes de v1 et leurs formats).
- **BTCSTATE-4** `[RA ; DÉCIDÉ (GEN-5)]` Un fournisseur local absent ou une base d'en-têtes illisible donne `LOCAL_FAILURE` ou
  `MISSING_DATA`, **jamais** « requête fausse donc transaction invalide ». Mutant à tuer : « BTCSTATE lu au-delà du repère ».

---

## §13 Règlement BTC/M0 à un saut

Principe `[DÉCIDÉ ; RA]` : **seul l'actif change** par rapport à N-SPEC v0.7 §13. Fenêtres `h0`/`H`, `btc_depth = 6`,
marqueur `NSW0`, financement consommé une fois, premier paiement, résolution unique, scan complet avant remboursement, `MISSING_DATA` et
rollback sont ceux du texte gelé. Le minimum `> 0` n'est pas relevé. Les identifiants techniques (`swap_id`, `N/SWAP`, `NSW0`, `swap_*`)
gardent leur nom gelé.

### 13.1 Contrat

- **13-1** `[RA (N-SPEC §13.1)]` « Le verrou réserve des **M0** au bénéficiaire si un paiement Bitcoin admissible est constaté, sinon à la
  destination de remboursement. »
- **13-2** `[DÉCIDÉ (N-SPEC §13.1)]` La résolution ne nécessite pas de transaction native supplémentaire du bénéficiaire. Elle reste
  réorganisable.

### 13.2 Création (objet `0004`)

- **13-3** `[DÉCIDÉ (N-SPEC §13.2) ; RA]` Payload, octets inchangés (226 o hors script, longueur comprise) :

  ```text
  version:u16 = 0
  chain_id:32
  funding_ref:32
  owner:32
  beneficiary:32
  refund_destination:32
  amount:u64            # unités atomiques M0 ; même type et même position que m1_amount
  btc_amount_sats:u64
  h0:u32
  H:u32
  btc_depth:u32
  btc_script:V(bytes)
  nonce:32
  ```

  `swap_id = H("N/SWAP", payload)`. `chain_id` égale celui du réseau.
- **13-4** `[DÉCIDÉ (N-SPEC §13.2) ; RA]` Conditions : `amount > 0`, `btc_amount_sats > 0`, `len(btc_script) ≤ 80`, `btc_depth = 6`,
  `h0 ≤ parent.ref.height + 1`, `H ≥ h0 + 12`, `H − h0 + 1 ≤ 144`, `B.ref.height ≤ H`.
- **13-5** `[RA]` `funding_ref` désigne une **sortie M0 transparente** non dépensée (son `object_id`) ; elle est consommée par la
  création. Bilan exact : `valeur(funding) = amount + restitution éventuelle + frais` ; `amount` quitte l'UTXO et entre dans `L`.
- **13-6** — *réservé — pas encore décidé* (restitution et frais de création en v1).
- **13-7** `[DÉCIDÉ (N-SPEC §13.2)]` Le financement autorise tous les champs et n'est consommé qu'une fois. Toute modification du payload
  change l'identité et exige les autorisations correspondantes.
- **13-8** — *réservé — pas encore décidé* (construction d'autorisation du financement).
- **13-9** `[RA]` *(partiel)* `beneficiary` et `refund_destination` (32 octets) désignent des destinations transparentes ; une adresse
  Sapling n'y tient pas.
- **13-10** `[DÉCIDÉ]` *(partiel)* **Limite globale de règlements ouverts** : au plus `max_open_swaps = 4 096` verrous §13
  ouverts dans l'état de la chaîne. Un verrou compte de sa création à son paiement ou à son remboursement. Les clôtures du bloc (résolutions
  exigibles) sont appliquées avant les créations ; à 4 096 ouverts, toute nouvelle création est **invalide** ; les
  fermetures passent toujours. La protection supplémentaire contre l'occupation des places §13 reste à décider après mesure.

### 13.3 Paiement

- **13-11** `[DÉCIDÉ (N-SPEC §13.3)]` Marqueur : `6a 28 <ASCII "NSW0" || network_tag4 || swap_id32>` ; données 40 o, script **42 o**. Le
  marqueur n'accorde ni score ni empreinte temporelle de consensus.
- **13-12** `[DÉCIDÉ (N-SPEC §13.3)]` Plusieurs premiers pushes reconnus `NSW0` rendent la transaction inadmissible pour tous les verrous.
- **13-13** `[DÉCIDÉ (N-SPEC §13.3)]` Le paiement n'est pas coinbase, possède le marqueur, une sortie au script exact `btc_script`, un
  montant suffisant (≥ `btc_amount_sats`) et une inclusion `h0 ≤ b ≤ H`.
- **13-14** `[DÉCIDÉ (N-SPEC §13.3) ; RA]` Retenir le **premier** paiement dans l'ordre Bitcoin, puis la première sortie admissible par
  `vout`. Un paiement n'est déclaré « premier » qu'avec une couverture **vérifiée** du préfixe pertinent de `[h0, H]` (blocs Bitcoin
  téléchargés et vérifiés contre les en-têtes de la branche) ; sinon `MISSING_DATA`.
- **13-15** `[RA]` **Un paiement Bitcoin ne résout jamais deux verrous** : la garantie « un paiement Bitcoin = un seul usage » est
  propre au règlement §13 (entre verrous §13) ; elle ne s'étend pas aux scripts (BTCSTATE, BTCSTATE-2).

### 13.4 Résolution

- **13-16** `[DÉCIDÉ (N-SPEC §13.4) ; RA]`

  ```text
  if first admissible payment exists
     and its depth in B.ref ≥ btc_depth:
      transfer reserved M0 to beneficiary          # sortie système transparente
      state = PAID

  else if B.ref.height ≥ H + btc_depth − 1:
      require complete scan of [h0,H]               # couverture vérifiée sur la branche
      require no admissible payment
      transfer reserved M0 to refund_destination    # sortie système transparente
      state = REFUNDED
  ```

- **13-17** `[DÉCIDÉ (N-SPEC §13.4)]` Résolutions exigibles avant les objets facultatifs, par `swap_id`. Un verrou nouveau est examiné
  immédiatement.
- **13-18** `[RA ; DÉCIDÉ]` Sans scan complet **vérifié** de `[h0, H]`, l'état reste `MISSING_DATA` ; aucun délai
  écoulé ne vaut absence de paiement ; jamais un remboursement par défaut ; jamais `INVALID` pour une couverture partielle.
- **13-19** `[RA]` *(partiel)* Transfert par **sortie système transparente** (G4, contexte non circulaire), valeur `amount`, script de la destination
  (13-9). La sortie déplace `L` vers `T`, sans émission ; elle n'est pas transplantable. (Identité exacte de la sortie réservée — pas encore décidée.)

### 13.5 Discipline du payeur (politique client)

- **13-20** `[DÉCIDÉ (N-SPEC §13.5) ; RA]` Ne pas payer avant inclusion du verrou et satisfaction de la politique client ; ne pas
  commencer si `best_validated_BTC.height > H − 12` ; revérifier après attente de stabilité. RBF n'est pas une annulation garantie. Un
  paiement après `H` peut transférer les BTC **sans droit aux M0 réservés**.

### 13.6 Rollback

- **13-21** `[DÉCIDÉ (N-SPEC §13.6, §21.9 G9)]` Une résolution retirée est rejouée. Un verrou retiré peut être réinclus avec les mêmes octets
  jusqu'à `H`, sous validité du financement et du contexte (`h0 ≤ parent.ref.height + 1`, `H ≥ h0 + 12`, `H − h0 + 1 ≤ 144`,
  `B.ref.height ≤ H`). Un paiement Bitcoin ne recrée pas un verrou disparu. Aucune atomicité interchaînes générale n'est promise après cette
  disparition.

---

## §SAP Sapling sur M0

Statut `[DÉCIDÉ ; RA]` : **Sapling sur M0 au testnet et au mainnet, sauf démonstration
d'impossibilité** (plafond, coût, nœud léger), sous la porte Sapling. Si l'impossibilité est démontrée, les règles de cette section
passent en **NA motivé (décision datée)**, toute donnée Sapling est rejetée (bundle non vide ⇒ transaction invalide), et rien n'est présenté
comme PASS. « Plus tard » seulement avec une justification solide approuvée par le propriétaire du projet.

### SAP.1 Forme

- **SAP-1** `[RA]` Spends et outputs Sapling (Groth16, Jubjub, paramètres de la cérémonie MPC Zcash) sur le M0 ; `t→z`, `z→z`,
  `z→t`. Sprout est absent. librustzcash est épinglée (Sapling seul) ; les paramètres (≈ 51,5 Mo) sont authentifiés par les empreintes
  publiées.
- **SAP-2** — *réservé — pas encore décidé* (encodage du bundle Sapling).
- **SAP-3** `[DÉCIDÉ]` Sapling n'est pas post-quantique ; il est **exclu** de toute exception de taille réservée aux
  transactions post-quantiques.

### SAP.2 État engagé et orthogonalité

- **SAP-4** `[RA]` Nullifiers, arbre incrémental des engagements, ensemble des racines admissibles et valeur du pool `Z` sont
  dans `application_state_root`. Rien dans `CBlockIndex` ni dans un index facultatif.
- **SAP-5** `[RA]` Orthogonalité exigible : aucune lecture sémantique des données Sapling par registre, graine, calendrier,
  score, départage ou H1. Les objets Sapling entrent dans `objects_root`, donc dans `kernel_commit` : « Sapling hors `kernel_commit` » est
  faux et ne doit pas être écrit.

### SAP.3 Turnstile en échec fermé

- **SAP-6** `[RA]` `Z ≥ 0` est vérifié **après chaque transaction**, dans l'ordre encodé, explicitement plus strict que le
  contrôle par bloc de ZIP-209 : avec `Z = 0`, un retrait suivi d'un dépôt dans le même bloc est rejeté même si le solde final est nul ;
  l'ordre inverse peut passer.
- **SAP-7** `[RA]` Deux cas, à ne jamais confondre :
  - **état local indisponible** (valeur de `Z` du parent absente du cache, base illisible, undo manquant) : **aucun verdict** ; `MISSING_DATA`
    ou `LOCAL_FAILURE` ; le nœud suspend, reconstruit ou récupère vérifiablement l'état, puis revalide. Jamais une invalidité historique ;
  - **état complet démontré invalide** : `Z` du parent est connu par l'état engagé vérifié et une transaction le rend négatif : le bloc est
    **historiquement invalide**.

  « Échec fermé » : jamais « inconnu donc accepté », jamais « inconnu donc invalide ». Mutants à tuer : « valeur absente ⇒ bloc accepté » et
  « valeur absente ⇒ bloc déclaré invalide ».
- **SAP-8** `[RA]` Le turnstile protège le transparent, **pas** les détenteurs de notes, et ne borne pas la perte
  cumulée si le pool reçoit de nouveaux dépôts. Limite publiée (§PUB).

### SAP.4 Nullifiers

- **SAP-9** `[RA]` Un nullifier apparaît au plus une fois : intra-transaction, intra-bloc et dans l'état. Après rollback, il est
  retiré avec le bloc qui l'a introduit. L'ensemble des nullifiers ne s'élague pas.

### SAP.5 Ancres

- **SAP-10** `[RA]` Une dépense référence une racine **admissible de la branche examinée** ; une ancre d'une branche
  abandonnée est refusée ; aucune fenêtre d'expiration n'est ajoutée en v1.
- **SAP-11** — *réservé — pas encore décidé* (admissibilité, déduplication et undo des racines).
- **SAP-12** `[RA ; DÉCIDÉ (N-SPEC G6, G8)]` Une transaction shieldée n'est jamais réécrite pour s'adapter à une autre branche ; elle est
  réincluable telle quelle seulement si ses ancres existent, ses nullifiers sont libres et le turnstile tient au moment de la réinclusion.

### SAP.6 Reprise complète en réorganisation ≤ 1 630

- **SAP-13** `[RA]` L'undo de chaque bloc contient les nullifiers ajoutés, la frontière de l'arbre, les racines ajoutées et la
  variation de `Z`. Il est conservé au moins `maxreorg + 1 = 1 631` blocs, même quand les corps sont élagués, et ne relit jamais un bloc
  élagué.
- **SAP-14** `[RA]` Le rejeu (rollforward après crash) applique **les mêmes** effets que la connexion normale (nullifiers,
  arbre, racines, `Z`) et est **idempotent**.
- **SAP-15** `[RA]` Différentiel exigé : exécution continue / undo-rejeu / crash / reconstruction sans cache, sur
  1 à 1 630 blocs, état Sapling compris (MON4).

### SAP.7 Politique d'ancre (portefeuilles, hors validité)

- **SAP-16** `[RA]` Politique publiée : choisir une ancre profonde **réduit** le risque qu'un burn retiré emporte les `z→z` de
  tiers sans lien, **sans l'annuler** (une réorganisation jusqu'à `maxreorg` reste possible) ; test « burn retiré → transactions shieldées
  sans lien ». Cache de témoins du portefeuille ≥ 1 631. Une ancre profonde ne préserve ni le bloc retiré, ni nécessairement les nullifiers libres, ni `Z` ; elle rend seulement possible la
  réinclusion conditionnelle (SAP-12) de la transaction dans la nouvelle branche, si ses nullifiers y sont libres et si le turnstile y
  tient.

### SAP.8 Plafond Sapling — forme décidée, valeurs à déterminer après mesures

- **SAP-17** `[RA]` **Exigé** : un plafond applicatif **déterministe**, vérifiable par **comptage avant toute
  vérification de preuve**, qui garde le pire bloc admis dans `Δ_val = 100 ms` par saut sur la classe matérielle de référence, à froid,
  avec les variantes du §10.6 et deux sauts.
- **SAP-18** `[DÉCIDÉ (04/10/2026)]` *(partiel)* Le plafond Sapling est déterministe, **par bloc**, exprimé **en unités de coût**,
  compté avant toute vérification de preuve, avec les mêmes paramètres sur les deux réseaux. Un budget commun s'appliquera si le budget
  pondéré commun est adopté. Les valeurs restent à décider après mesures.
- **SAP-19** `[RA ; DÉCIDÉ]` La validité ne dépend que de comptages ; jamais « mon CPU dépasse 100 ms » comme règle ;
  jamais `Δ_val` relevé (aucun passage à 250 ms) ; aucune re-dérivation de H_N pour sauver Sapling.
- **SAP-20** `[RA]` Si vérification en lots : équivalence de décision lot ⇔ individuel exigée ; vérification en
  mempool isolée en CPU (politique).

### SAP.9 Stockage

- **SAP-21** `[RA]` La croissance des nullifiers (≈ 605 Mo/an à 6 spends par bloc) et celle des racines admissibles sont
  comptées dans la qualification du stockage avec le nœud élagué sur la classe matérielle de référence.

---

## §CONS Conservation et partition de M0

- **CONS-1** `[RA]` Au genesis d'APP-SPEC v1, **aucune ressource dérivée n'existe**. Toute ressource dérivée future, définie par une
  autre spécification applicative, déclare sa règle d'agrégation avant activation.
- **CONS-2** `[RA ; DÉCIDÉ (N-SPEC G2)]` Formule de transfert : `Σ entrées transparentes + max(valueBalance, 0) = Σ sorties transparentes +
  max(−valueBalance, 0) + frais` (OBJ-7).
- **CONS-3** `[RA]` Partition **explicite et disjointe** : à tout état visible engagé `C`,

  ```text
  S_mat(C) = T(C) + F_imm(C) + L(C) + Z(C) + D(C)
  S_mat(C) ≤ S_src(btc_ref(C))
  ```

  - `T` : sorties M0 transparentes non dépensées, hors frais immatures et hors extinctions comptées dans `D`, quel que soit leur script ; la
    ventilation par scripts (libre, HTLC, escrow, covenant, reçus de frais) est un **diagnostic** d'audit, jamais une catégorie normative ;
  - `F_imm` : sorties de frais immatures (`fee_maturity_links = 2 880`), comptées une seule fois, ici et pas dans `T` ;
  - `L` : M0 réservés par des verrous §13 ouverts (hors UTXO) ;
  - `Z` : valeur du pool Sapling ;
  - `D` : M0 éteints par une extinction normative ; **`D = 0` en v1** (CONS-4). Le terme est conservé pour qu'une
    version future qui autoriserait une extinction la comptabilise ici, jamais ailleurs.
  Une unité change de catégorie seulement par une transition engagée (dépense, maturation, création ou résolution de verrou, passage
  `t↔z`).
- **CONS-4** `[DÉCIDÉ (03/10/2026)]` *(partiel)* **La destruction de M0 est interdite** : toute sortie qui détruirait du M0
  (hors frais) est refusée. **`D = 0`** et l'invariant décidé est :
  **M0 total = BTC brûlés importés**, c'est-à-dire `T + F_imm + L + Z = S_mat` (somme des imports matérialisés), à tout état visible engagé.
- **CONS-5** `[RA]` MON1 révisé : « À chaque état visible engagé, `S_mat(C) ≤ S_src(btc_ref(C))` et la partition ci-dessus est exacte ;
  zéro M0 issu de tickets, REACT, score ou récompense. »
- **CONS-6** `[RA]` MON2 : un droit d'import est matérialisé au plus une fois par histoire ; **un nullifier Sapling apparaît au plus une
  fois par histoire**.
- **CONS-7** `[RA]` MON3 : UTXO, imports, verrous §13, reçus, nullifiers, arbre, ancres et `Z` sont validés dans le **même commit
  atomique** ; après crash, l'état visible est l'ancien ou le nouveau complet.
- **CONS-8** `[RA]` MON4 : deux séquences admissibles de rollback et de réapplication qui aboutissent à la même pointe et au même
  contexte Bitcoin donnent **les mêmes** UTXO, imports, verrous, frais, reçus, nullifiers, arbre, ancres, `Z` et offre, pas seulement un
  total.
- **CONS-9** `[RA]` MON5 : les dépendants shieldés d'une source retirée sont défaits par le rollback de bloc ; aucune application ne lit
  un fait Bitcoin hors du repère de son bloc.
- **CONS-10** `[RA]` G1 : la provenance s'entend comme « toute valeur provient, par des transitions conservatrices, d'un
  ensemble de droits d'import uniques » ; aucune attribution publique d'une unité à un burn particulier n'est exigée après mélange ou passage
  shieldé.

---

## §R2P R2-pivot : durée de vie minimale réelle des contrats enfants

- **R2P-1** `[RA ; DÉCIDÉ]` M0 est l'actif de règlement interchaîne **sans connaître les autres chaînes** ; les LP
  règlent **sans confiance** sur M0. Il n'y a plus de règle de consensus HTLC : une borne **supérieure** sur la hauteur de claim n'est pas
  exprimable en script, et le claim tardif n'est **plus rejeté**.
- **R2P-2** `[RA]` **Gabarit normatif de contrat pivot** : la branche de remboursement de tout contrat enfant imposé par un pivot à
  covenant porte un délai **relatif** `<L_min> OP_CHECKSEQUENCEVERIFY` en liens N, en plus de son échéance absolue (CLTV en créneaux). Le
  gabarit CTV du claim parent **engage toutes les branches de remboursement requises** de l'enfant (script complet de la sortie enfant) ;
  sinon le claimant pourrait faire naître un enfant sans ce délai.
- **R2P-3** `[RA]` Ce que cela garantit : sur la branche examinée, la branche de remboursement de l'enfant n'est **pas ouverte** dans
  les `L_min` liens qui suivent l'inclusion de l'enfant ; une branche portant au plus un bloc par créneau (§1.4 inv. 6), ces liens couvrent un
  écart nominal d'au moins `L_min` créneaux. Ce que cela **ne garantit pas** : une fenêtre réelle depuis la **découverte** de l'enfant par
  son bénéficiaire ; une branche révélée tard (rétention, partition, réorganisation) peut contenir à la fois l'enfant et son remboursement.
  La garantie s'entend sous hypothèses de disponibilité et de profondeur de réorganisation, complétée par une politique LP publiée
  (surveillance, marges, profondeur exigée avant d'agir).
- **R2P-4** — *réservé — pas encore décidé* (statut normatif du gabarit pour les outils).
- **R2P-5** `[RA — principe seulement]` `L_min` et les échéances des gabarits sont des **valeurs de gabarit**, fixées sur
  l'analyse des marges interchaînes ; elles ne sont pas des paramètres de consensus. Aucune valeur n'est choisie ici.

---

## §FEE Frais, reçus de frais et politiques

- **FEE-1** `[DÉCIDÉ (N-SPEC §8.8, §3.2) ; RA]` Les frais sont en M0 et **transférés au producteur en sorties immatures** ; la
  récompense de bloc vaut 0. Une transaction peut payer ses frais depuis le pool via `valueBalance`.
- **FEE-2** — *réservé — pas encore décidé* (sortie de frais : destination et identité).
- **FEE-3** `[DÉCIDÉ (N-SPEC G7, §21.7)]` Une sortie de frais issue du bloc `F` n'est dépensable dans `B` que si `links_N(F, parent(B)) ≥ 2 880`,
  par toutes les voies, y compris indirectes (CTV, §13, reçus).
- **FEE-4** `[DÉCIDÉ (04/10/2026)]` *(partiel)* Seuil de poussière de consensus : **1 000 unités atomiques M0** sur les sorties des
  transactions `0001`, reçus KEYREG/ROTATE et financements compris. La sortie de frais est exemptée et conserve son montant exact ;
  imports et résolutions §13 suivent leurs minima propres. Aucun minimum de frais de consensus. Le prix par octet relève du relais :
  départ ntest à **0,05 sat/octet**, Sapling ×10 ; valeurs mainnet après mesures. La protection supplémentaire contre l'occupation des
  places §13 reste à décider après mesure.
- **FEE-5** `[DÉCIDÉ (N-SPEC §4.2, §6.9), principe seulement]` *(partiel)* **Reçu de frais** KEYREG/ROTATE : « Le reçu engage
  réseau, IID, opération et montant. Il est consommé une fois et préexiste, ou résulte d'un objet applicatif antérieur du même bloc. »
  (Forme concrète réservée — pas encore décidée.)
- **FEE-6** `[DÉCIDÉ (N-SPEC §3.2)]` `keyreg_fee` et `rotation_fee` restent à 1 000 unités atomiques M0 ; seuls les KEYREG du descripteur
  initial sont exemptés.
- **FEE-7** `[DÉCIDÉ]` Mempool et relais : politiques distinctes de la validité ; isolation des travaux coûteux (Sapling
  compris), priorité aux blocs, budget par pair, réinclusion topologique (§9.7) ; un seuil de poussière de mempool ne borne pas les blocs
  d'un producteur adverse.

---

## §PROF Tableau unique des profondeurs

*Réservé — pas encore décidé* (tableau de synthèse ; les profondeurs décidées figurent dans les règles ci-dessus et au §3.2 de N-SPEC v0.7).

---

## §VER Procédure de version applicative

- **VER-1** `[RA]` APP-SPEC v1 ne contient **aucun crochet** pour M1 ni pour un domaine C.
- **VER-2** `[RA]` `application_spec_id` est engagé dans le manifeste, donc dans le genesis : **aucun remplacement, même « à date
  fixe », n'est autorisé aujourd'hui** ; une date d'activation n'est pas une procédure.
- **VER-3** `[RA]` *(partiel)* Avant toute promesse, la procédure de version est écrite. (Son contenu minimal est réservé — pas encore
  décidé.)
- **VER-4** `[RA ; DÉCIDÉ]` Comme G4 change les `txid` à chaque version, **aucune compatibilité
  automatique n'est promise. Aucune promesse de soft fork.**
- **VER-5** `[DÉCIDÉ]` Un futur pool post-quantique sera une **nouvelle version applicative** (migration entre
  pools comprise), sans changer le moteur N.

---

## §PUB Publications obligatoires

- **PUB-1** `[RA]` Aucune API « sûr » ni « final » ; profondeur, unité et K(ε) toujours contextualisés (§14.5, §16).
- **PUB-2** `[RA]` Échelles de temps (739 blocs ≈ 2 à 4 h) ; risques interchaînes (secret révélé puis claim réorganisé, STOP, attente
  possible de plusieurs heures) ; limite SCR-5 (créneaux et liens ne garantissent ni observation ni inclusion).
- **PUB-3** `[RA]` **Perte de l'agrégat public `M1_supply`** ; la mesure d'exposition BTC/M0 est un modèle de risque hors consensus,
  calculable sur les en-têtes et l'état N, sans équivalence annoncée.
- **PUB-4** `[RA]` **Matrice cryptographique** : contrôle N en ECDSA, production et checkpoints en ML-DSA-44, Sapling en
  Groth16/Jubjub (non post-quantique), sorties utilisateur selon le schéma de signature retenu (pas encore décidé) ; jamais « BATHRON entièrement post-quantique » ; « N signe en ML-DSA »
  corrigé ; CVE-2019-7167 attribuée à **Sprout**.
- **PUB-5** `[RA]` Confidentialité d'un règlement sous covenant non assurée (montants, hashlocks, délais visibles) ; débit shieldé
  publié avec le plafond ; risque « pool vidé » pour qui shielde son inventaire (SAP-8) ; origine des paramètres Sapling (MPC) et empreintes.
- **PUB-6** `[RA]` BTCSTATE est documenté comme prédicat de présence **non consommant** ; aucun outil ne le présente comme mécanisme de
  règlement à paiement unique.

---

## Sections non publiées dans ce brouillon

Tables de traçabilité, points ouverts, décisions en attente et notes de relecture du texte de travail : *non publié*.
