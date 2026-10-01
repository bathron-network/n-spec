# Banc réseau N — plan (v1, 01/10)

Autorité : DIRECTION.md, ligne « Mandat orchestrateur — dernier chantier avant gel ». Objet : mesurer Δ et la marge d'horloge, puis dériver
τ. On **ne suppose pas τ = 6 s**, et aucune règle N n'est modifiée.

## Quantité décisive

Régime prouvable des deux analyses CP_reg : « D = 0 », c'est-à-dire qu'un bloc honnête du créneau s est reçu **et validé** par tout
honnête avant sa réservation du créneau s+1. Réservation à `start(s+1) + 1 000 ms` (§7.2) ; signature au plus tard à `start(s) + 2 000 ms`.

```text
Condition D=0 :  t_sign + Δ_net(p) + Δ_val + skew(p) ≤ τ + 1 000 ms,  avec t_sign ≤ 2 000 ms
          ⇔     Δ_net(p) + Δ_val + skew(p) ≤ τ − 1 000 ms
```

(pour τ = 6 s : 5 s, soit exactement la valeur « Δ + horloge ≤ 5 s » de la confrontation CP_reg). On mesure directement, dans l'horloge du
récepteur, le **retard observé** `L = t_recv_local − t_send_local(émetteur)`. Il contient le réseau et le décalage d'horloge relatif, qu'on
sépare par un estimateur NTP à 4 horodatages (offset θ, délai δ, filtre au δ minimal).

## Dispositif

- Nœuds : vps1 (VPS, 6 cœurs), vps2 (VPS, 4 cœurs, même hébergeur), Mac (domestique, derrière NAT : connexions sortantes seulement). RTT vps1↔vps2 ≈ 17 ms.
  Trois points européens : **Δ sur un saut européen = borne basse**. Le cas mondial (multi-sauts, intercontinental) est **émulé** par tc netem
  appliqué au seul port du banc, jamais au démon bathrond ni à ssh.
- `nbench.py` (Python asyncio, sans dépendance) : maillage TCP complet, diffusion par inondation (relais au premier reçu, dédoublonnage
  par id), trames `[len|type|payload]`.
- Blocs : un producteur par créneau de mesure (tourniquet), cadence 1 s. Mélange de tailles : 50 % en-tête seul (2 820 o), 40 % 64 Kio,
  10 % maximum consensus (2 820 + 262 144 o). La cadence de mesure (1 s) est plus dense que tout τ candidat ; c'est un **stress**, pas un
  choix de τ.
- Charge de fond : flux de « transactions » de 3 Kio (taille d'une opération PQ signée), 32/s par nœud, inondé.
- Horloge : ping NTP applicatif toutes les 2 s par paire, plus un relevé `timedatectl timesync-status` toutes les 10 min.
- Coupures : toutes les 20 min, `iptables DROP` sur le port du banc depuis un pair, pendant 10, 30 ou 60 s (vraie perte TCP, pas une fermeture
  propre), puis rattrapage par inventaire. On mesure le temps de retour à jour.
- Validation Core : micro-banc séparé (SHAKE256 loterie, hachage du corps 256 Kio, vérification ML-DSA-44 si une implémentation compilée
  est disponible, sinon valeur publiée citée et marquée NT), plus les durées de connexion de bloc du démon actuel à titre indicatif.

## Phases (≈ 7 h, nuit du 01/10)

| Phase | Réseau | Durée |
|---|---|---|
| P0 | natif | 4 h (≈ 14 400 créneaux, p99.9 par sens exploitable) |
| P1 | netem « intercontinental » : +75 ms ±15 ms par sens, perte 0,5 % | 1 h 30 |
| P2 | netem « dégradé » : +150 ms ±40 ms par sens, perte 2 % | 1 h 30 |

## Sorties

Par sens et par phase : p50/p95/p99/p99.9/max de Δ_net (retard corrigé de l'offset), de L brut et du jitter ; offset et dérive d'horloge ;
temps de rattrapage après coupure ; Δ_val. Puis, pour τ ∈ {6, 8, 10, 12} : marge `τ − 1 000 − (Δ_net,p + Δ_val + skew)` à p99.9 et au
maximum, **en multi-sauts** (h sauts = somme de h tirages indépendants, h = 1…6), ainsi que la fraction de créneaux qui violeraient D = 0.

## Statuts

Mesure directe (P0, un saut européen) ≠ émulation (P1/P2) ≠ extrapolation multi-sauts. Aucune de ces valeurs n'est une hypothèse publiée
tant que le propriétaire n'a pas arrêté τ.

## v2 après critique Codex (lancée le 30/09, 23 h 54, run `r1`, T0 = 1790805240)

Corrections apportées avant lancement :
- **Émission découplée** : une file et une tâche d'écriture par pair. La production ne bloque jamais ; les attentes en file supérieures à 0,5 s et
  les abandons sont journalisés.
- **Horodatages** : `send_ns` (origine, après construction du bloc), `write_ns` (écriture socket, réécrit à chaque saut), `recv_ns`. On obtient
  un retard de lien (réseau + noyau) distinct du retard de bout en bout.
- **Rattrapage par inventaire** : on ne renvoie que les créneaux manquants, avec le type `sync`, exclu des statistiques de propagation.
- **Toutes les arrivées journalisées**, pas seulement la première ; complétude calculée par rapport aux blocs produits.
- **Cadence 0,5 s** : environ 9 600 blocs par couple origine→récepteur en P0, environ 3 600 en P1 et P2. Les p99.9 sont donnés avec leur
  IC ; un maximum observé n'est pas une borne.
- **netem** : prio + fq_codel dans les bandes des autres flux ; filtre sur le seul port du banc ; échec journalisé (`netem_FAILED`) ;
  compteurs `tc -s` relevés. **netem n'agit qu'en sortie des VPS** : les sens VPS→VPS et VPS→Mac sont retardés, **Mac→VPS ne l'est pas**.
- **Coupures** : chaîne iptables dédiée `NBCUT` sur vps2, qui alterne lien seul (vps1→vps2) et isolement complet de vps2 (10, 30, 60 s) ;
  nettoyage sur sortie.
- **Validation** : `valbench.py`, avec ML-DSA-44 (pqcrypto 1.0.0) sur vps2. Vérification p50 153 µs, p99 298 µs ; borne cryptographique
  d'un bloc maximal (109 signatures + hachages) ≈ **34 ms**, hors accès à l'état. Pour la condition, on retiendra Δ_val = 100 ms, avec une
  sensibilité à 250 et 500 ms.
