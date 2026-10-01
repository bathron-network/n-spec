# Contrôle de cohérence — N-SPEC v0.7 (critère de gel 9)

1er octobre 2026. Objet : vérifier qu'aucune contradiction **non expliquée** ne reste entre fork-choice, registre, graine, calendrier et `maxreorg` avec les valeurs v0.7. Ce document ne modifie aucune règle. Toute incohérence qui exigerait une règle est posée comme **question au propriétaire** (§9).

Valeurs contrôlées : `τ = 10 s`, `L_epoch = 14 400` (40 h), `K_reg = 2 750`, `registry_min_blocks = maxreorg = 1 630`, `fee_maturity_links = reference_protection_links = 2 880`, `seed_guard = 43 200 s`, marge MTP `7 200 s`, d'où `G(τ) = 3 600` et `K_inst = K_reg + G = 6 350`. Coin du domaine H_N : β = 0,30, d = 0,70, `p_late = 10⁻²`, donc `a = 0,3049` et `h' = 0,4851`.

Méthode : arithmétique en espérance (avec écart-type σ de la production honnête binomiale), puis recalcul par `derivation/derive_k.py::compose` sur les courbes DP publiées pour les probabilités. Aucune simulation nouvelle. Statut de chaque conclusion : **analytique** (espérance et σ) ou **composition** (terme de `composition.csv`, lui-même esquissé et extrapolé).

## Verdict

**Aucune contradiction bloquante.** Les cinq liens (fork-choice, registre, graine, calendrier, maxreorg) restent cohérents avec les nouvelles valeurs. Il reste quatre points à arbitrer par le propriétaire et deux signalements, qui ne sont pas des contradictions :

| Id | Nature | Bloquant pour le critère 9 ? |
|---|---|---|
| Q1 | Le chemin de réintégration d'un nœud de retour qui garde son origine locale n'existe pas : un `BOOTSTRAP` y est ignoré par règle | Non (le nœud reste hors domaine, ce qui est sûr), mais la promesse de D1 est incomplète |
| Q2 | Bande d'environ 370 créneaux (≈ 1 h) où l'arithmétique ne force pas STOP pour une *installation* antidatée ; elle est couverte en probabilité par `T_profond` | Non (expliqué par la composition) |
| Q3 | Le coin du domaine (h ≈ 0,49) est sous le `rho_min = 7/10` des profils de livraison et du frein | Non pour la sûreté ; oui pour l'utilité de la livraison au coin |
| Q4 | `Q_B_work = 256` et `Delta_nom_ms = 1 000` dans le profil, alors que H_N suppose `Q_B = 1` et une borne de délai exprimée par `p_late` | Non (documentation) |
| S1 | Durées doublées ou presque des fenêtres en créneaux et en époques | Non |
| S2 | Le miroir TLA+ du pivot profond est proportionné sur la v0.6 | Non |

## 1. Un nœud synchronisé fait-il toujours STOP plutôt qu'adopter ?

**Fourche brute antérieure à `snapshot_cut`** (voie i). Pour qu'un synchronisé adopte une branche privée Y, il doit déconnecter tous les blocs honnêtes produits depuis la fourche.

| Instant de l'engagement | Créneaux depuis la coupure | Blocs honnêtes attendus h'·n (σ) | Comparé à maxreorg = 1 630 |
|---|---:|---:|---|
| Premier porteur légal (plancher MTP), `cut + K_inst` | 6 350 | 3 080 (σ ≈ 40) | > 1 630 : **STOP** |
| Porteur honnête nominal, `cut + K_reg + ≈ 6 780` | ≈ 9 530 | ≈ 4 623 (σ ≈ 49) | **STOP** |
| Engagement d'époque e, `≥ start(e) = cut + K_reg + L` | 17 150 | 8 319 (σ ≈ 65) | **STOP** (facteur 5,1) |

**Pivot** (voie ii). Y garde un compte sous le seuil (≤ b − 1) ; la déconnexion minimale d'un synchronisé vaut `≈ h'·(t − cut) − b` (`PIVOT-PROFOND-TLA.md` §5). Le STOP est garanti en espérance si `h'·(t − cut) > 2b`, soit `t − cut > 2 × 1 630 / 0,4851 ≈ 6 720` créneaux.

- **Engagements d'époque e** (signatures et adoptions de blocs de e, `t − cut ≥ 17 150`) : la déconnexion vaut ≈ 6 689 > 1 630, donc **STOP**. La condition `h' > 2b/(K_reg + L) = 0,190` est satisfaite avec un facteur 2,55 (h'_min = 0,4851).
- **Installations** (D3 : elles comptent dans CP_reg). Au plancher légal `cut + 6 350`, la déconnexion vaut ≈ 3 080 − 1 630 = 1 450 < 1 630 : l'arithmétique **ne force pas** STOP dans la bande `[cut + 6 350 ; cut + 6 720]`. Cette bande n'est atteignable que si la maturité Bitcoin de la graine existe réellement aussi tôt, c'est-à-dire avec des horodatages Bitcoin poussés vers le futur et des blocs rapides. Au porteur nominal (≈ `cut + 9 530`), la déconnexion vaut ≈ 2 993 > 1 630 : **STOP**.
- Cette bande n'est pas une contradiction non expliquée : c'est exactement l'événement que borne `T_profond` dans la composition (≈ 1,95 × 10⁻¹³ par époque pour (2 750 ; 1 630), sous le budget ε_ep/2). Elle n'existait pas en v0.6 au profil B : `K_inst = 13 200` dépassait `2b/h ≈ 11 755`. Elle apparaît parce que τ = 10 s réduit G de 6 000 à 3 600 créneaux et que K_reg est dérivé au plus juste. → **Q2**.

**Nœuds nouveaux ou de retour** : ils ne sont pas protégés par maxreorg (pointe antérieure à la fourche). Ils sont hors domaine par D1 (§12.15). → **Q1** pour le chemin de retour.

## 2. Ancre et Nbound

- `Nbound(T) = ancestor(T, 1 630 liens)`, `Bbound` = 100 confirmations Bitcoin du repère, soit ≈ 60 000 s, c'est-à-dire ≈ 6 000 créneaux et ≈ 2 900 blocs au coin du domaine. En régime nominal, Bbound est la plus profonde des deux et l'ancre vaut `min(Nbound, Bbound) = Bbound`. Dans tous les cas, l'ancre est à au moins `maxreorg` liens de la pointe : maxreorg déclenche `HALTED_DEEP_REORG` avant que l'ancre ne soit retirée. Aucun ordre de déclenchement contradictoire.
- Vecteur §20.4 ajusté (`T.height = 3 750` pour garder `Nbound = 2 120`). Les trois cas (Bbound plus bas, Nbound plus bas, ancienne ancre conservée) gardent le même sens.
- A4 (compatibilité des ancres entre honnêtes) : `maxreorg = 1 630 ≥ K_blocs(10⁻¹²) = 1 508` au coin. Une divergence en blocs à la profondeur de Nbound est donc bornée **par coupure**. Ce n'est pas une preuve A4 : pas d'union sur les coupures, pas de cas de partition ni de réorganisation Bitcoin (contre-exemple TLA+ v0.6 « ancres après livraisons séparées » toujours ouvert). A4 reste une obligation séparée, inchangée, et elle est signalée comme telle au §5.7.2.

## 3. Maturité des frais et protection des références

- `fee_maturity_links = 2 880 ≥ maxreorg = 1 630` et `reference_protection_links = 2 880 ≥ 1 630` : les contraintes du §3.3 tiennent.
- Une dépense de frais exige en plus que l'ancre protège F (G7) ; avec Bbound ≈ 16,7 h, la discipline de portefeuille attend en pratique la borne Bitcoin. Rien de nouveau : la relation était la même en v0.6.
- Durée : 2 880 liens valent ≈ 8 h à cadence pleine (contre 4,8 h en v0.6) et ≈ 16,5 h au coin. C'est un délai d'usage plus long, pas une contradiction. Abaisser ces valeurs vers 1 630 resterait conforme au §3.3 ; ce serait une décision de paramètre, non demandée ici.

## 4. Règle A : fenêtre `[snapshot_cut(e), seed_maturity(e)]` à τ = 10 s

Délai nominal entre `freeze_slot` et le premier porteur honnête de `m_e` : garde de 43 200 s, + ≈ 3 600 s de retard de la MTP, + 29 blocs Bitcoin (≈ 17 400 s), + `d_ref` = 6 blocs (≈ 3 600 s), soit ≈ 67 800 s ≈ **6 780 créneaux**.

| Fenêtre | Longueur (créneaux) | Blocs honnêtes attendus (σ) | Ratio à b = 1 630 |
|---|---:|---:|---:|
| Nominale `K_reg + 6 780` | ≈ 9 530 | ≈ 4 623 (49) | 2,8 |
| Minimale légale (porteur au plancher MTP) `K_reg + G` | 6 350 | 3 080 (40) | 1,9 |

- **La règle A avance normalement dans le domaine.** L'héritage n'apparaît que si la densité de blocs (tous producteurs confondus) tombe sous ≈ 1 630 / 9 530 ≈ 0,17 sur la fenêtre (0,26 au plancher). C'est du même ordre qu'en v0.6 (2 880 / 18 500 ≈ 0,16), et c'est le régime de faible densité déjà traité par le §5.9.
- La robustesse du compte (voie ii peu profonde) est le terme `T_court ≈ 7,6 × 10⁻¹⁵` par époque.
- Aucune interaction nouvelle avec la graine : `seed_maturity` reste une maturité engagée sur la branche, et `K_inst` est le plancher que le §8.4 impose déjà.

## 5. Fenêtres en créneaux et en époques : durées modifiées (signalement S1)

Aucune valeur n'est changée. Les durées sont multipliées par 10/6.

| Paramètre | Valeur | v0.6 (6 s) | v0.7 (10 s) | Contradiction ? |
|---|---:|---:|---:|---|
| `L_epoch` | 14 400 créneaux | 24 h | **40 h** | Non ; E = 2 192 époques sur 10 ans (composition) |
| `ommer_horizon` | 1 440 créneaux | 2,4 h | **4 h** | Non. Il reste inférieur à maxreorg en créneaux (≥ 1 630), comme en v0.6 (1 440 < 2 880) : après la guérison d'une partition plus longue, le crédit d'activité peut être perdu (G10 le dit déjà) |
| `evidence_horizon` | 14 400 créneaux | 24 h | **40 h** | Non. Il reste supérieur à la profondeur maxreorg en temps (≈ 9,3 h **en moyenne** au coin, non une borne supérieure) : une équivoque sur une branche réorganisable reste prouvable |
| Fenêtre temporelle d'activité (7 époques) | 7 × L | 7 j | **11,7 j** | Non |
| Contestation (2 époques) | 2 × L | 2 j | **3,3 j** | Non |
| Voie lente, plafonds (7 époques) | 7 × L | 7 j | **11,7 j** | Non |
| Délai d'effet du frein (« 4 à 5 époques », §6.6) | — | 4–5 j | **6,7–8,3 j** | Non |
| `grace_react` | 4 032 hauteurs BTC | ≈ 28 j | ≈ 28 j | Non. Le rapport grâce / cycle d'exclusion diminue, mais la grâce reste plus longue que les fenêtres |
| Fenêtres de densité (100 / 1 000 créneaux) | — | 10 min / 1,7 h | **16,7 min / 2,8 h** | Non |
| `Deep(C,W)` de H1 (> maxreorg liens) | — | > 2 880 | **> 1 630** | Non. H1 examine des paires un peu moins profondes, et RawLag exige de toute façon `G_anchor` ≈ 6 mois |

## 6. Anti-grinding (§5.8)

- Séparation nominale entre coupure de cliché et seuil de graine : 70 700 s (19,6 h) ; marge 63 499 s (17,6 h), contre 86 400 et 79 199 s en v0.6. La garde de 12 h, en secondes, est intacte.
- Même en poussant les horodatages Bitcoin de 2 h vers le futur, la graine n'est révélée que ≳ 17 h après la coupure. Le contenu pré-cliché est donc figé avant la révélation sur toute branche publique.
- La surface de grinding qui subsiste (contenu pré-cliché composé après S_e sur une branche **privée**, E1 d'Opus) ne touche que les nœuds non protégés (D1, hors domaine) : pour un synchronisé, elle aboutit à STOP (§1). Aucune contradiction.
- K_reg n'est pas ici le cas « K_reg = 1, rôle anti-grinding à décider » (DERIVATION-K §5) : CP_reg exige déjà 2 739 créneaux.
- `Q_B = 1` est une hypothèse de H_N. Le profil client garde `Q_B_work = 256` comme borne de campagne (§15.4–15.5). → **Q4**.

## 7. Calendrier et graine

τ ne change ni la loterie (§7.1), ni la graine (§5.4, en secondes et en hauteurs Bitcoin), ni l'attribution des créneaux vides (§5.5). Le calendrier reste public dès R_e et S_e connus ; H_N-15 l'intègre à l'adversaire. Les phases du §7.2 (ms absolues) laissent 9 s de budget D = 0. **Pas de contradiction.**

## 8. Modèles TLA+ v0.6

- **Constantes abstraites** : `KReg = 1`, `MaxReorg ∈ {1, 2, 4}`, `SlotsPerEpoch = 2`, `Dbtc = 3`, etc. (`PORTEE-ET-MAPPING.md` : « pas de conversion 3↔100 ni 3↔2880 »). Les résultats structurels (D + A ferme le finding v0.5, C6 8/8, H1 indépendant de l'ordre 9/9, voie lente, 13/13 mutations) **restent valides** : ils ne dépendent pas des valeurs numériques.
- **Signalement S2** : le miroir `RegistryModel_PivotDeep.tla` annonce des proportions « qui respectent le réel » (v0.6) : `K_reg = L/2`, `MatMin = freeze + ⌈0,42 L⌉`, `BtcMat ≈ freeze + 0,75 L`. En v0.7, le réel donne `K_reg/L ≈ 0,19`, `G/L = 0,25` et `b/L ≈ 0,11`. Les témoins (atteignabilité) restent valides, mais la phrase de proportion ne l'est plus, et la transposition arithmétique du §5 de `PIVOT-PROFOND-TLA.md` (b = 2 880, 13 200) est remplacée par le §1 ci-dessus. L'exploration stricte reste **INCOMPLET**. Un re-proportionnement du miroir serait utile ; ce n'est pas une mécanique.

## 9. Questions au propriétaire (aucune règle ajoutée)

**Q1 — Retour d'un nœud qui garde son origine.** D1 met les revenants hors domaine « jusqu'à initialisation depuis une origine A′/RELEASE récente ». Or le §12.12 ignore tout `BOOTSTRAP` sur un nœud qui a une origine locale, et le §7.6 interdit à un producteur de jeter sa mémoire de signature. Les seuls chemins existants sont donc :
- (a) réinstallation en nœud neuf, en observateur, ou avec rotation pour un producteur ;
- (b) `RECOVERY` explicite, exceptionnelle par construction.

Faut-il :
- (i) accepter ces deux seuls chemins ;
- (ii) autoriser une **revendication** CP_reg (diagnostic d'API, sans aucun pouvoir sur la fork-choice) quand la chaîne adoptée est compatible, ancêtre ou descendante, avec un `BOOTSTRAP` récent comparé sur deux canaux ;
- (iii) autre ?

L'option (ii) serait une règle de politique client nouvelle ; elle n'est pas activée en v0.7.

**Q2 — Bande d'installation au plancher MTP.** Entre `cut + 6 350` et `cut + 6 720` créneaux, une installation pivot antidatée n'est pas convertie en STOP par l'arithmétique (§1) ; elle est seulement bornée en probabilité par `T_profond`. Deux options :
- accepter cette couverture probabiliste, qui est le dimensionnement dérivé ;
- choisir `K_reg ≥ ≈ 3 120` (≥ 3 700 avec une marge de 7σ) pour que l'arithmétique force STOP en espérance. C'est un choix de paramètre plus conservateur, pas une mécanique, et il rejoint la question 3 de `PIVOT-PROFOND-TLA.md` sur le rôle de la marge MTP.

**Q3 — Coin du domaine et `rho_min`.** Au coin (β = 0,30 abstentionniste, d = 0,70), la densité attendue vaut ≈ 0,49. Elle est sous :
- le `rho_min = 7/10` de livraison (§14.2) ;
- le seuil de santé du frein (§6.6) ;
- la condition de dimensionnement `1 − α − β > rho_min` (§14.3 : 1 − 0,21 − 0,30 = 0,49).

La sûreté n'est pas en cause (la règle A demande ≈ 0,17). Mais au coin, la livraison du profil de laboratoire est suspendue et le frein reste actif (voie lente seulement). Faut-il accepter ce mode dégradé, publier un profil de livraison propre à H_N, ou restreindre le domaine de vivacité ?

**Q4 — Profil client.**
- `Q_B_work = 256` reste une borne de campagne alors que H_N suppose `Q_B = 1` : faut-il le garder tel quel (laboratoire) ou l'aligner ?
- `Delta_nom_ms = 1 000` est sous la latence W1 mesurée (p50 de 1,3 à 1,7 s à un saut). La contrainte du §3.3 reste satisfaite même avec 9 s, mais la valeur nominale ne décrit plus le réseau du domaine. Faut-il l'aligner ? C'est de la documentation, pas une mécanique.

## 10. Signalements hors critère 9 (pour mémoire)

- Horloges : des nœuds macOS ont été mesurés à 85–120 ms, à la limite de H_N-8 (≤ 100 ms).
- `p_late ≤ 10⁻²` par fenêtre et H_late ne sont pas certifiés par le banc (réserves Codex de `SYNTHESE-BANC-TAU.md`). Le banc ne démontre pas non plus que STOP se déclenche en W2.
- L'écart DP/MC (facteur 1,3 à 1,8) reste non expliqué ; la DP, conservatrice, est publiée.

## Reproduction

```sh
cd etudes/n-spec/cp-reg/derivation
python3 - <<'EOF'
import sys, numpy as np; sys.argv=['x']; sys.path.insert(0,'.')
import derive_k as D
z = np.load('results/dp_curves.npz')
c = {(float(k.split('_')[0]), float(k.split('_')[1]), float(k.split('_')[2]), k.split('_')[3]): z[k] for k in z.keys()}
print(D.compose(c, 0.3, 0.7, 0.01, 10, 1e-9, 1))                     # ligne b=b_min : 1629 / 2739
print(D.compose(c, 0.3, 0.7, 0.01, 10, 1e-9, 1, b=1630, kreg=2740))  # b_max = 1629 < 1630
print(D.compose(c, 0.3, 0.7, 0.01, 10, 1e-9, 1, b=1630, kreg=2750))  # b_max = 1634, eps_H ≈ 4.61e-10
EOF
```


## Corrections après revue Codex T2 (01/10)

La revue (`orchestration/reviews/n-spec-v07-codex.md`) a relevé trois erreurs, corrigées dans la v0.7 :
- les diagnostics d'API (§12.15, §17.6) sont des **propositions non activées** ;
- le STOP d'un nœud synchronisé est **probabiliste**, au plus `T_CG`, et non déterministe ;
- le seuil indicatif de 19 créneaux est retiré.

La fenêtre de H_N-4 est fixée à K(10⁻¹²) = 1 913 créneaux, et le statut de `tau_ms` (décision, non dérivée) est corrigé. Les durées comme « 9,3 h » sont des moyennes, non des bornes. Restent à traiter : Q1 (réintégration d'un nœud de retour qui conserve son origine) et Q3 (livraison suspendue au coin du profil B).
