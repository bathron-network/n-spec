# Confrontation CP_reg — Opus × Codex (30/09/2026)

Sources : `CP-REG-opus.md` (DP exacte + Monte-Carlo, `sim-opus/`), `CP-REG-codex.md` (enveloppe par union + attaque constructive, `sim/`).
Mandat : `../MANDAT-CP-REG.md`. Aucune mécanique N modifiée (feu vert propriétaire).

## Convergences
| Point | Opus | Codex |
|---|---|---|
| Seul régime prouvable | D = 0 : bloc honnête livré avant la réservation suivante (Δ + 2σ ≤ τ − 1 s = 5 s) | idem ; aucune case Δ/τ ≥ 1 ne passe sa réduction |
| Condition nécessaire | h = (1−β)·d > β (β sur poids **total**) | idem (« NC : pas de dérive honnête positive ») |
| d = 0,2 | aucun K pour β ≥ 0,20 | idem |
| Calendrier public + rétention + équivoque | §15 (k = 77 ⇒ 10⁻¹⁶) surestime de 8–10 ordres | idem ; compter des **créneaux non vides**, pas des blocs |
| Règle A pilotable | g·W < 2 880 ≤ (g+β)·W (zone d ≈ 0,2) | trace exécutable (2 déconnexions) ; 0,32 % à β = 0,20, d = 0,20, K = 512 (16 M répétitions) |
| Rustine | aucune | aucune |
| Domaine H_N | 9 hypothèses | 11 hypothèses (même squelette) |

## Divergences
| Cas | Opus (coupure fixe, adversaire optimal, exact) | Codex (union sur départs, 3 fenêtres, conversions temporelles, majorant) |
|---|---|---|
| β 0,20 · d 0,7 · 10⁻⁹ | 289 créneaux / 217 blocs | 4 424 créneaux / 856 blocs |
| β 0,25 · d 0,4 | 19 700 créneaux / 10 800 blocs (10⁻¹²) | 770 900 créneaux, 53 jours (10⁻⁹) |

Écart 3–15× (dense) à ~40× (creux) : **objets différents**, pas un défaut de calcul. Codex le dit : « suffisante et très conservatrice,
pas un minimum nécessaire » ; son attaque constructive reste loin sous son enveloppe (2,6 % vs 57 % à β = 0,25, K = 64).
K réel ∈ [attaque exécutable, enveloppe Codex] ; la DP Opus est la meilleure borne serrée **pour une coupure fixe**.

## Objection structurelle (Codex) — ouverte
`ε_CP = UNKNOWN` tant que manque la réduction « registres/calendriers concurrents sur branches différentes » → « calendrier commun ».
Opus ne la traite pas. Suite : `../MANDAT-LEMME-PREMIERE-DIVERGENCE.md` (L1, L2, P : ε ≤ ε_CP-fixe(K) + ε_pivot).

## Reste pour conclure
1. Lemme de première divergence (réduction) — en cours.
2. Mesure de Δ sur le banc horloge (décide si N est dans le seul régime prouvable).
3. Décisions propriétaire : Δ ≤ 5 s publié ou τ allongé ; couple (β_max, d_min) ; zone pilotable de A = hors domaine (STOP) ou défaut.

Rédaction : orchestrateur (Opus 5.5), d'après la lecture provisoire de l'agent Fable interrompu (quota) et les deux rapports.
