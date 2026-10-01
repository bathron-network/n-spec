# Confrontation — Lemme de première divergence (Codex × Opus)

30 septembre 2026, orchestrateur. Sources : [LEMME-L1-codex.md](LEMME-L1-codex.md) (GPT-6 astra, TLA+), [LEMME-L1-opus.md](LEMME-L1-opus.md)
(agent Opus 5.5 indépendant, qui n'a lu ni le rapport Codex ni la note orchestrateur), [NOTE-ORCH-L1.md](NOTE-ORCH-L1.md) (points posés **avant**
les rapports). Aucun changement de N-SPEC.

## 1. Accord des deux analyses (et de la note orchestrateur)

| Énoncé du mandat | Codex | Opus | Orchestrateur |
|---|---|---|---|
| **L1** : même registre, graine et calendrier au premier bloc divergent | Démontré, avec argument de fermeture | Démontré (« lemme F ») | Le point 1 anticipait le piège |
| Justification « cliché strictement antérieur » | **Fausse littéralement** | **Fausse** | Idem (porteur de maturité) |
| Argument correct | Le porteur tardif ajoute +1 au compte, de façon identique pour toute candidate sur P | Idem : porteur ≥ start(e) = +1 symétrique | — |
| **L2** : calendriers communs sur [s, start(e)) | Vrai (même X Bitcoin) | Vrai au sens strict | — |
| Corollaire « toute la course se joue sous calendrier commun » | **Faux** | **Réfuté** (E1) | Point 2 |
| **P** comme dichotomie (i) brut / (ii) pivot | Exhaustive | Exhaustive, aucun « autre » | — |
| **P** comme borne ε_CP-fixe + ε_pivot | **Non démontrée** | **Réfutée** | Point 2 |

**Aucun « autre » structurel** : ni le TLA+ (12 sondes, `NoOtherStructural` jamais violé), ni le raisonnement d'Opus n'en trouvent.
La disjonction est donc solide. C'est la **traduction probabiliste de la voie (i)** qui manque.

## 2. Le trou, identifié de la même façon des deux côtés

Une branche privée Y bifurque avant `snapshot_cut(e)`. À start(e), elle est **en retard** : il n'y a donc pas de violation de préfixe commun
(CP) sous calendrier commun. Elle change ensuite de registre, donc de calendrier, et rattrape X **sous son propre calendrier**. Un honnête
finit par s'engager sur Y. L'événement ¬CP_reg(e) se produit sans événement antérieur couvert par ε(K).

- Codex : témoin TLA+ `MC_private_return_L1` (15 états), avec retour et livraison sélective : deux signatures au créneau 4 sous
  `R_A=⟨3,1,1⟩` et `R_B=⟨2,2,1⟩`. Il le nomme **ε_U = UNKNOWN**.
- Opus : contre-exécution E1. Le contenu pré-cliché de Y est composé **après** avoir vu S_e, en faisant défiler les clés de rotation
  (§6.9). On obtient alors `Q_reg ≈ 2^calcul` calendriers sélectionnables, et Q_reg **entre dans ¬CP_reg**, contrairement à ce qu'affirme le
  mandat.

**Qui peut s'engager sur Y ?** Les deux analyses et la note orchestrateur convergent sur la réponse.
- Un nœud **synchronisé** sur X est protégé par maxreorg. Il devrait déconnecter au moins h·13 200 blocs, soit plus de 2 880 dès que
  h > 0,22 (Opus : h > 0,134 sur 21 600). Le résultat est **HALTED_DEEP_REORG, pas une adoption**.
- Les **seuls exposés** sont les nœuds **nouveaux** ou **de retour** dont la pointe ou l'ancre est antérieure à F + 2 881 blocs, ainsi que
  les signataires alimentés sélectivement (témoin Codex). C'est le problème classique de la **longue portée ou du revenant** (Praos → Genesis),
  qui réapparaît ici par le registre.

## 3. Désaccords résiduels

1. **Opus : « l'objection se ferme dans le domaine » ; Codex : « ε_U UNKNOWN ».** L'orchestrateur tranche **pour Codex sur le statut**.
   L'ε_post d'Opus vient d'une DP sur **une** stratégie (attaque privée), avec β' = β + 0,01 postulé. C'est une borne **inférieure**
   constructive du risque, pas une borne supérieure sur toutes les stratégies. Opus le dit lui-même (« ordre de grandeur, pas une borne »).
   Sur le fond, les deux s'accordent : le terme ne concerne **que** les nœuds non protégés, et il est très probablement négligeable dans
   (β ≤ 0,20, d ≥ 0,4).
2. **K de la voie (i) : 13 200 (Opus) contre « K effectivement couvert avant l'événement » (Codex).** Les deux positions sont compatibles.
   Une installation peut avoir lieu dès cut + 13 200 créneaux (marge MTP 7 200 s + garde 43 200 s, rapportées en créneaux). Codex rappelle
   que début d'époque, fermeture et premier engagement sont trois instants distincts. **On retient K = 13 200 si les installations
   comptent dans CP_reg** (le §5.7.2 dit oui : « engagements et installations »).
3. **Le pivot profond (Opus seul).** Une branche privée ferme tôt sa fenêtre sous le seuil, puis prend l'avantage. C'est une violation CP de
   profondeur réduite K_piv = 13 200 − 2 880/h. À (0,20 ; 0,4), la marge est courte : 4 200 disponibles pour 2 840 requis. **À faire vérifier
   par Codex** (témoin TLA+ demandé par Opus) avant de s'en servir.
4. **Domaine H_N.** Codex rappelle qu'aucun d_min n'est adopté dans N-SPEC §17 ou §23.4. La zone pivot n'est donc pas « hors domaine par
   construction » **tant que le propriétaire n'a pas publié le domaine**. C'est exact : il s'agit d'une décision, pas d'un calcul.

## 4. Où on en est, en une phrase

**La réduction marche pour tous les nœuds synchronisés** (elle ramène le problème à du calendrier commun, et maxreorg fait le reste). **Elle ne
marche pas pour les nœuds nouveaux ou de retour**, et ce trou-là, c'est la longue portée, pas un défaut propre au registre. Ce n'est donc pas
(encore) une objection structurelle à N. C'est une **question de domaine** : que garantit-on à un nœud qui n'a pas suivi la chaîne ?

## 5. Décisions demandées au propriétaire (aucune règle nouvelle proposée)

- **D1. Nœuds non protégés** : les déclarer **hors domaine CP_reg** ou les couvrir ?
  - *Hors domaine* : un nœud nouveau ou absent ne revendique CP_reg qu'après s'être initialisé depuis une origine (checkpoint A′/RELEASE)
    postérieure d'au moins 2 881 blocs à toute fourche pertinente. C'est la subjectivité faible assumée. Recommandation orchestrateur, parce
    que H1 et l'origine de confiance existent déjà pour cela.
  - *Couverts* : il faudrait publier une borne sur Q_reg (calcul adverse sur les rotations) et démontrer ε_post comme borne supérieure. Cela
    représente un gros travail analytique, sans garantie de succès.
- **D2. Domaine publié** : (β_max ; d_min) = (0,20 ; 0,4) ou (0,30 ; 0,7), avec D = 0, conditionnés au banc réseau (Δ + horloge ≤ 5 s à
  τ = 6 s, sinon τ plus grand). Sans publication, la zone pivot reste « dans le domaine ».
- **D3. Installations dans CP_reg** : confirmer la lecture du §5.7.2 (oui), et donc K = 13 200.

## 6. Suite proposée (boucle orchestrateur)

1. Après D1 à D3 : **Codex**, lot court (son quota hebdo est à environ 95 %, report possible au reset) : témoin TLA+ du pivot profond, et
   classe « installation d'un côté, engagement de l'autre après start(e) ».
2. Réécriture de la garantie composée dans le domaine choisi, avec la preuve « nœud synchronisé ⇒ HALT » écrite proprement (elle est
   aujourd'hui dispersée entre Opus §4.3 et la note orchestrateur).
3. En parallèle : **banc réseau** (Δ, dérive d'horloge, p99.9 sur les VPS). C'est le deuxième test avant gel, et il est indépendant de tout
   ce qui précède.
