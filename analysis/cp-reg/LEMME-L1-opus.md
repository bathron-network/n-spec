# Lemme de première divergence — analyse indépendante (opus)

30 septembre 2026. Mandat : `../MANDAT-LEMME-PREMIERE-DIVERGENCE.md`, points 1 à 3, partie analytique seulement (le TLA+ est confié à Codex). Entrées lues : N-SPEC v0.6 (§2.5, §3.2, §5.1–5.9, §6.1–6.2, §6.6, §6.9, §7.1–7.3, §8.4, §9.2–9.7, §15), `CP-REG-opus.md`, `CP-REG-codex.md`, `CONFRONTATION-CP-REG.md`. `NOTE-ORCH-L1.md` et `LEMME-L1-codex.md` n'ont pas été ouverts.
Calculs : scripts jetables hors dépôt (DP exacte de l'avance privée, en additions positives), et courbes ε(K) de `sim-opus/table_analytique.json`.

## 0. Résultat en bref

- **L1 est vrai, mais la justification du mandat est fausse.** D_e ne dépend pas seulement du préfixe antérieur au cliché : le compte de la règle A court jusqu'au porteur de maturité, qui peut être le bloc divergent lui-même. Ce qui sauve L1 est un lemme de fermeture (§1) : le porteur tardif compte toujours pour exactement un bloc, sur chaque branche.
- **L2 est vrai au sens strict** : les calendriers sont communs sur tous les créneaux antérieurs à start(e), et s < start(e). **Son corollaire est faux** (« toute la course se joue sous calendrier commun ») : un engagement honnête peut venir après start(e), sous des calendriers déjà divergents, dont celui de la branche adverse, choisi par grinding.
- **P est vraie comme dichotomie structurelle**, mais **fausse comme borne** `ε_CP-fixe(K) + ε_pivot`. Il faut trois corrections : K vaut 13 200 créneaux et non 21 600 (les installations comptent) ; il manque un terme de course après start(e) où intervient Q_reg ; le pivot a un volet profond qui relève d'une borne CP à profondeur réduite.

## 1. Cadre et lemme de fermeture

Hypothèses utilisées, toutes citées dans la SPEC :

- **H-X** : le contexte X (règles, origine, faits Bitcoin) est commun, en particulier S_e et sa maturité m_e (§5.7.2, §5.4).
- **H-C6** : C6 (§5.7.2) ; R_j et Control_j sont fonctions de (D_j, X).
- **H-cal** : le calendrier de l'époque j est `producer(slot) = f(seed_j, tickets(R_j))` (§7.1), avec `seed_j = H(…, e, S_j, registry_root(R_j))` (§5.4). Aucun parent, contenu ni nonce n'entre dans la graine.
- **H-A** : la règle A telle qu'écrite au §5.2 (support brut strictement avant cut(e) ; compte inclusif sur [cut(e), seed_maturity(e,C)] ; héritage `A_e = A_{e−1}` sinon).

Notations : cut(e) = snapshot_cut(e) = (e−1)·L − 7 200 ; start(e) = e·L ; F est le dernier bloc commun à A et B (slot f) ; C|<t désigne les blocs de C dont le slot est inférieur à t.

**Lemme F (fermeture).** Pour toute branche C qui porte au moins un bloc de slot ≥ start(e), ou dont le porteur de m_e est antérieur à start(e) :

```
window_blocks(C,e) = #{b ∈ C : cut(e) ≤ slot(b) < start(e), slot(b) ≤ seed_maturity(e,C)} + [porteur(e,C) ≥ start(e)]
```

Par conséquent, D_e(C) est une fonction de C|<start(e) seul.

*Preuve.* Soit b₁ le premier bloc de C de slot ≥ start(e). Son époque e' est au moins e. Sa validation exige la maturité k_seed de S_{e'} dans son repère (§9.2). Or `seed_time` croît avec l'époque, donc height(S_{e'}) ≥ height(S_e) et le repère de b₁ contient m_e. Si le porteur n'est pas dans C|<start(e), c'est donc b₁ (et §5.2 le confirme : « aucun bloc d'une époque e ne peut précéder son propre porteur »). Aucun autre bloc de slot ≥ start(e) n'entre alors dans le compte. Que le porteur soit avant ou après start(e) se lit sur les repères de C|<start(e), et raw_support se lit sur C|<cut(e). Les observations de contrôle s'arrêtent à `activity_cutoff(e) = slot(A_e) − 1 440` (§6.2), et l'attribution des créneaux vides (§5.5) ne porte que sur des faits antérieurs. Par récurrence sur j ≤ e (§5.7.1), D_e(C) = Φ_e(C|<start(e)). ∎

Le « +1 » est indépendant de la branche. C'est ce point, et non l'ancienneté du cliché, qui neutralise le porteur tardif.

## 2. L1 — démontré (justification corrigée)

Soient a₁ et b₁ les premiers blocs de A et de B après F, et s = min(slot a₁, slot b₁). On a A|<s = B|<s. Soit j = epoch(s). Comme start(j) ≤ s, le lemme F donne D_j(A) = Φ_j(A|<start(j)) = Φ_j(B|<start(j)) = D_j(B). Par H-C6 et H-cal, registre, graine et calendrier de j sont identiques. ∎

La parenthèse du mandat (« D ne dépend que du préfixe antérieur à snapshot_cut ») est fausse telle quelle : le compte de fenêtre inclut des blocs de [cut, porteur], et le porteur peut être le bloc divergent. Les cas demandés :

- **Porteur = bloc divergent** (a₁ ferme la fenêtre de j) : le compte vaut c + 1, où c est le compte commun dans A|<s. Un bloc hypothétique de B au même créneau compterait aussi c + 1. Identique.
- **Époques vides et héritage.** Si a₁ est un bloc de reprise après plusieurs époques sans bloc, il est le porteur de chaque époque sautée j' ≤ j. Chaque compte vaut c_{j'} + 1, en général sous le seuil, d'où l'héritage (§5.9). C'est symétrique sur les deux branches.
- **Premiers blocs à des créneaux ou des époques différents** : L1 porte sur le plus précoce. Le plus tardif (par exemple b₁, à un créneau postérieur au cliché d'une époque ultérieure) peut déjà être produit sous un registre différent. L1 ne dit rien de lui, et il n'en a pas besoin.
- **Équivoque au même créneau** (trace Codex §5.4 : E et L au créneau 28 799) : le calendrier de l'époque 1 est commun. L1 tient.

## 3. L2 — démontré au sens strict ; corollaire réfuté

**L2 strict.** Par minimalité de e, D_j(A) = D_j(B) pour j < e, donc (H-C6, H-cal) les calendriers de tous les créneaux antérieurs à start(e) sont communs. Par le lemme F, D_e(A) ≠ D_e(B) implique A|<start(e) ≠ B|<start(e), donc s < start(e). L1 donne en outre e ≥ epoch(s) + 1. L'intervalle [s, start(e)) est donc non vide et entièrement sous calendrier commun. e' = e par définition. ∎

**Le corollaire est faux.** Les engagements d'époque e (signature ou adoption d'un bloc de e) ont lieu au plus tôt à start(e). La décision d'adoption compare alors des scores (§9.3) qui incluent des blocs de slot ≥ start(e). Ces blocs ont été produits sous R_e(A) sur A et sous R_e(B) sur B. Rien n'oblige la branche perdante à start(e) à rester perdante. Contre-exécution :

**E1 (course prolongée sous calendrier choisi).** β = 0,25, d = 0,4 (h = 0,30).

1. L'adversaire bifurque en F, peu avant cut(e), et tient Y privée. Y contient au moins un bloc adverse de slot dans ]f, cut(e)[, portant un ROTATE d'une de ses identités (§6.9 : « prend effet dans un registre ultérieur »). Y porte ensuite assez de blocs adverses dans la fenêtre pour passer le seuil A. C'est faisable si β·W_Y ≥ 2 880 : avec une fermeture tardive, W_Y ≈ 21 601 et 0,25·21 601 ≈ 5 400.
2. Les blocs de créneaux passés peuvent être signés plus tard. La validation historique ne lit aucune heure de signature ; §8.4 ne borne que le repère. L'adversaire compose donc le contenu pré-cliché de Y **après** avoir vu S_e, en essayant autant de clés de rotation qu'il peut en calculer. Chaque essai donne une racine R_e(Y), donc une graine et un calendrier d'époque e différents (§5.4). On a Q_reg(Y) de l'ordre de 2^calcul, et non 1 : §5.8 ne donne Q_reg = 1 qu'à préfixe fixé.
3. Jusqu'à start(e), Y reste derrière X (aucune viabilité, donc aucun événement mesuré par ε(K) à calendrier fixe). Les honnêtes installent R_e(X) et signent des blocs de e sur X.
4. Après start(e), l'adversaire rattrape X grâce au calendrier de e choisi sur Y. Un nœud honnête **nouveau**, ou **de retour** avec une pointe antérieure à F, arrive ensuite. La déconnexion depuis sa pointe est nulle et son ancre est antérieure à F. BaseNDecision rend donc UNIQUE_ADOPTION(Y) (§9.5). Il installe D_e(Y) et signe sur Y.
5. Les nœuds synchronisés de X voient Y maximale mais à plus de 2 880 déconnexions : HALTED_DEEP_REORG, sans adoption. Leurs engagements portent sur D_e(X). **CP_reg(e) est violée.**

E1 est une exécution conforme aux règles. Pendant [s, start(e)), rien ne s'y produit qui relève d'une borne à calendrier fixe, et ce n'est pas un pivot (les supports bruts diffèrent). Structurellement, E1 relève de (i) (une branche maintenue au-delà du cliché). Mais son coût n'est **pas** couvert par ε(K) : la queue de rattrapage se calcule sous un calendrier choisi parmi Q_reg. Q_reg entre donc bien dans l'événement ¬CP_reg(e). Il intervient après la divergence des branches, mais avant la divergence des engagements.

**Rôle exact de maxreorg et de l'ancre.** La déconnexion se mesure depuis la pointe adoptée du nœud (§9.5). Pour un nœud synchronisé sur X dans le cas (i), elle vaut au moins le nombre de blocs de X dans [cut, start(e)), soit au moins h·21 600 − O(σ) selon la croissance de chaîne. Cette valeur dépasse 2 881 dès que h > 0,134. **maxreorg exclut donc tout basculement de nœud synchronisé après start(e) dans le domaine h > β ≥ 0,134.** Le prix est un arrêt, pas une adoption. L'ancre n'ajoute rien pour ces nœuds : `eligible = min(Nbound, Bbound)` la place au plus à 2 880 liens sous la pointe (§9.6). Pour un nœud de retour, l'ancre et la pointe de référence sont celles d'avant l'absence (§9.7). S'il est parti avant F, ou moins de 2 881 blocs après F, il n'est protégé par rien et choisit au rang. Un nouveau nœud n'a que l'ancre de son origine. **maxreorg n'exclut ni les nœuds non protégés, ni le pivot peu profond (2 déconnexions dans la trace Codex).**

## 4. P — dichotomie démontrée, borne réfutée

### 4.1 Dichotomie (démontrée)

A_{e−1} est commun. D_e diffère si et seulement si A_e(A) ≠ A_e(B). Chaque A_e(C) vaut raw_support(C,e) ou A_{e−1}. Trois cas :

- **(a)** les deux branches passent le seuil et leurs supports bruts diffèrent. Alors A|<cut ≠ B|<cut, donc f < cut(e) : c'est la **voie (i)**.
- **(b1)** une branche passe, l'autre non, avec des supports bruts égaux (f ≥ cut(e) ou préfixe brut commun) : c'est la **voie (ii), le pivot**.
- **(b2)** une branche passe, l'autre non, avec des supports bruts différents : f < cut(e), donc **voie (i)**.

Il n'existe pas d'autre cas. Par le lemme F, un pivot exige f < start(e), donc des comptes différents sur des blocs de slot inférieur à start(e). Une divergence purement postérieure à start(e) (même porteur tardif, +1 de chaque côté) ne change pas D_e.

**Branche privée sur plusieurs époques.** Si f < cut(j) et que X porte des blocs honnêtes dans ]f, cut(j)[, alors D_j diffère, sauf si les deux branches héritent. Dans le domaine g·W > 2 880 (§6), X passe le seuil avec une forte probabilité. La première divergence tombe donc sur la première époque j telle que cut(j) > f, ou sur l'époque du pivot. L'adversaire ne peut la repousser qu'en zone de faible densité, où les deux branches héritent. Même là, c'est sans dommage pour P : l'intervalle commun [s, start(e)) s'allonge, et K avec lui.

**Engagements par signature des deux côtés.** Un signataire honnête sur Y tient Y au moment de sa signature. Soit il la tenait avant start(e) (vues honnêtes scindées sous calendrier commun, donc (i) ou (ii) à calendrier fixe), soit il l'a adoptée après (E1). Même analyse que pour l'adoption.

### 4.2 Correction 1 — K de la voie (i) : 13 200, pas 21 600

CP_reg compte les **installations** (§5.7.2 : « v est un autre engagement ou une installation de registre par adoption »). Une installation a lieu à l'adoption du porteur, dont le créneau vérifie `slot_time ≥ MTP(ref) − 7 200 s ≥ seed_time(e) − 7 200 s = freeze_time + 36 000 s` (§8.4, §5.4). Cela donne porteur ≥ freeze_slot + 6 000 = cut + 13 200. Une installation honnête à t ≥ cut + 13 200, face à une autre vue honnête qui diverge avant cut, est une violation CP en créneaux de profondeur ≥ 13 200. On peut vérifier les deux ordres (U tenue avant V, ou l'inverse) : dans chacun, la chaîne adoptée la plus tard est viable à t sur une fourche d'âge au moins t − f. En pratique, sans manipulation des horodatages Bitcoin, m_e n'existe qu'à freeze + 17 à 19 h environ, soit K ≈ 16 000 à 19 000. **La borne publiable est 13 200** (la même que le W de Codex). Le chiffre 21 600 ne vaut que si l'on restreint CP_reg aux engagements d'époque e.

### 4.3 Correction 2 — terme de course après start(e)

On décompose au temps T = start(e) :

```
ε_(i) ≤ ε_fix(K_inst = 13 200)                                    [viabilité avant start(e)]
      + Σ_δ Pr_fix[marge à T = −δ] · min(1, Q_reg · ρ'^δ / (1−ρ'))  [rattrapage sous calendrier choisi]
      + ε_CG(21 600 créneaux, 2 881 blocs)                          [échec de maxreorg pour les synchronisés]
```

Ici ρ' = β'/h, où β' tient compte des exclusions d'honnêtes sur Y (voie lente, au plus 1 % par 7 époques, §6.6). Le second terme ne concerne que les engagements de nœuds non protégés (§3). Illustration par DP exacte de l'attaque privée (avance stationnaire au cliché, puis 21 600 créneaux sous calendrier commun, puis union sur Q_reg) :

| β | d | sans grinding | Q_reg = 2³², β' = β + 0,01 | Q_reg = 2⁶⁴, β' = β + 0,01 |
|---:|---:|---:|---:|---:|
| 0,20 | 0,7 | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ | < 10⁻³⁰⁰ |
| 0,20 | 0,4 | 3·10⁻¹³⁴ | 6·10⁻¹²⁹ | 1·10⁻¹²³ |
| 0,25 | 0,4 | 3·10⁻²² | 1·10⁻¹⁶ | **5·10⁻¹²** |
| 0,30 | 0,7 | 7·10⁻²²² | 9·10⁻²¹⁷ | 1·10⁻²¹¹ |

Ces chiffres modélisent une attaque privée et non la marge BKMQR : ce sont des ordres de grandeur, pas une borne. Lecture : le terme est négligeable partout, sauf au bord du domaine (0,25 ; 0,4), où il atteint la cible 10⁻¹² et gagne une dizaine d'ordres de grandeur sur le cas sans grinding.

### 4.4 Correction 3 — le pivot a deux volets

- **Pivot peu profond** (trace Codex, 2 déconnexions). Il exige que le compte honnête soit voisin du seuil : g·W < b ≤ (g+β)·W. Il est gouverné par la condition de robustesse du compte.
- **Pivot profond.** La branche « sous le seuil » est une branche privée Y, bifurquée en f ≥ cut, qui ferme tôt sa fenêtre (W_min = 13 200) avec peu de blocs, puis prend l'avantage en score. Pour que count(Y) < b, il faut que les blocs honnêtes communs dans [cut, f] soient moins de b, soit f − cut ≲ b/h. Or Y n'est installable qu'après son porteur, soit t ≥ cut + 13 200. La fourche a donc un âge d'au moins **K_piv = 13 200 − 2 880/h** créneaux, et c'est une violation CP à calendrier fixe si t < start(e). Si t ≥ start(e), la course continue sous deux calendriers fixés : le support brut est commun, donc Q = 2 (seuil passé ou hérité), sans grinding de contenu.

Ni l'analyse Opus ni l'analyse Codex ne traitaient ce second volet : la zone « g·W < b ≤ (g+β)·W » ne le couvre pas.

### 4.5 Recherche de contre-exemple (point 2, par raisonnement)

J'ai cherché une exécution avec D_e(A) ≠ D_e(B) hors des voies (i) et (ii). J'ai examiné quatre candidats :

- une divergence créée après start(e) par le porteur tardif ;
- un porteur postérieur au bloc divergent ;
- des époques vides ;
- une équivoque au même créneau.

Le lemme F et la dichotomie de 4.1 les éliminent tous. **Aucun « autre » structurel n'existe.** En revanche, E1 est un contre-exemple à l'inclusion « (i) ⊆ violation CP à calendrier fixe », et le pivot profond un contre-exemple à « (ii) ⊆ zone de compte ».

## 5. Garantie composée et domaine H_N (point 3)

Par époque, avec X commun et la réconciliation Bitcoin supposée (H_N-7) :

```
Pr[¬CP_reg(e)] ≤ ε_fix(13 200)                                   (i) avant start(e)
               + ε_CG(21 600 ; 2 881)                            protection maxreorg des synchronisés
               + 1_{nœuds non protégés admis} · ε_post(Q_reg)    (i) après start(e), §4.3
               + ε_pivot-court(β, d, W_min = 13 200, b = 2 880)  zone de compte
               + ε_fix(13 200 − 2 880/h)                         pivot profond
```

Il faut ensuite composer par union sur les époques de l'horizon et sur Q_B (graines Bitcoin), comme dans `CP-REG-opus.md` §6. Q_reg n'apparaît que dans ε_post.

Chiffres, avec D = 0 et ε_fix tiré des courbes exactes de `sim-opus` (interpolation log-linéaire) :

| β | d | h | ε_fix(13 200) | ε_fix(21 600) | Compte honnête sur W_min (marge) | K_piv | ε_fix(K_piv) |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 0,20 | 0,7 | 0,56 | ≈ 0 | ≈ 0 | 7 392 (≫ 2 880) | 8 057 | ≈ 0 |
| 0,20 | 0,4 | 0,32 | < 10⁻⁵⁰ | ≈ 0 | 4 224 (25σ) | 4 200 | ≈ 2·10⁻¹⁸ |
| **0,25** | **0,4** | 0,30 | **≈ 8·10⁻⁹** | ≈ 7·10⁻¹⁴ | 3 960 (20σ) | **3 600** | **≈ 5·10⁻³** |
| 0,30 | 0,7 | 0,49 | ≈ 0 | ≈ 0 | 6 468 | 7 322 | ≈ 0 |
| 0,20 | 0,2 | 0,16 | ∞ (h < β) | ∞ | 2 112 : **zone pivot** | — | — |

Pour la ligne (0,25 ; 0,4), avec une fermeture réaliste (W ≈ 16 000), on obtient K_piv ≈ 6 400 et ε ≈ 10⁻⁴.

**La zone pivot est-elle hors domaine par construction ?**

- **Pivot peu profond : oui dès d_min = 0,4** (pour β ≤ 0,30, D = 0). La condition robuste g·W_min − 6σ > 2 880 donne h > 0,242, soit d > 0,30 (β = 0,20), d > 0,32 (β = 0,25) ou d > 0,35 (β = 0,30). La zone dangereuse est d ≈ 0,2 à 0,3. H_N, qui exige d ≥ 0,4, l'exclut. Réserve : à D = 1, g = h/(1+h) vaut 0,242 à (0,20 ; 0,4), exactement au bord. Mais D ≥ 1 est déjà sans borne prouvable.
- **Pivot profond : non, pas à (β = 0,25 ; d = 0,4).** ε ≈ 5·10⁻³ au pire réglementaire, et ≈ 10⁻⁴ en réaliste. Cette case était déjà disqualifiée par ε_fix(13 200) ≈ 8·10⁻⁹ > 10⁻¹². Le choix (0,20 ; 0,4) passe, de justesse sur K_piv (4 200 contre 2 840 requis pour 10⁻¹²). (β ≤ 0,30 ; d ≥ 0,7) passe largement.
- **ε_post** est négligeable dans tout le domaine (β ≤ 0,20, d ≥ 0,4) ou (β ≤ 0,30, d ≥ 0,7), même à Q_reg = 2⁶⁴. Il ne compte qu'au bord (0,25 ; 0,4), déjà exclu.

Conclusion : **dans les domaines (β_max = 0,20 ; d_min = 0,4) et (β_max = 0,30 ; d_min = 0,7), avec D = 0, l'objection Codex se ferme** par la composition ci-dessus. Mais elle se ferme avec ses cinq termes et K = 13 200, pas avec la formule à deux termes du mandat. Hors de ces domaines, elle reste ouverte.

## 6. Questions au propriétaire (pas des règles)

1. CP_reg inclut-il bien les **installations** (lecture littérale du §5.7.2) ? Si oui, K de la voie (i) vaut 13 200. Si on les exclut, il vaut 21 600, mais une installation honnête contredite reste alors hors de toute garantie publiée.
2. **Nœuds non protégés** (nouveaux, ou de retour avec une pointe antérieure à F ou à moins de 2 881 blocs après F) : H_N doit-il les déclarer hors domaine (engagement sans garantie CP_reg jusqu'à une resynchronisation profonde), ou les couvrir avec ε_post et une borne de calcul publiée sur Q_reg ? La SPEC ne borne pas aujourd'hui le nombre de racines R_e sélectionnables sur une branche privée (rotations, §6.9).
3. Faut-il publier **W_min = 13 200** (et non 14 400 ou la valeur nominale d'environ 18 500) comme longueur de référence de la condition de robustesse du compte (H_N-5) et du pivot profond ?
4. Faut-il demander à Codex d'ajouter au moniteur TLA une classe « installation d'un côté, engagement de l'autre après start(e) », ainsi qu'un témoin du pivot profond ?

## 7. Verdict

**L1 : DÉMONTRÉ** (sous H-X et C6 ; la justification « cliché strictement antérieur » est remplacée par le lemme F, porteur tardif = +1 symétrique). **L2 : DÉMONTRÉ au sens strict** (calendriers communs sur [s, start(e)), s < start(e)) ; **RÉFUTÉ pour son corollaire** « toute la course sous calendrier commun » (contre-exécution E1). **P : DÉMONTRÉE comme dichotomie structurelle ; RÉFUTÉE comme borne ε_CP-fixe + ε_pivot** (contre-exécution E1 avec Q_reg, pivot profond, K = 13 200 et non 21 600) ; **DÉMONTRÉE SOUS HYPOTHÈSE** sous la forme composée du §5, dans le domaine explicite D = 0, (β ≤ 0,20, d ≥ 0,4) ou (β ≤ 0,30, d ≥ 0,7), X commun.
