# Obligations et limites de qualification

Lire les statuts exécutés dans `RESULTATS.json`. Cette table distingue la portée du moniteur de la portée de l'obligation complète.

| Obligation | Instrumentation livrée | Limite / qualification |
|---|---|---|
| A1/D1 | Fonctions déterministes de chaque famille, Registry équivalence, H1Order, Oracle monétaire | Déterminisme global de toutes les sous-machines composées : NT. |
| A2 | Miroir sans observation locale du cliché ; permutations H1, réévaluation | Les vecteurs Bitcoin du miroir sont fixes ; les réorgs sont une autre famille. |
| A3 / CP_reg | CPreg de fixtures ; CPregGlobal dans le générateur de productions | FAIL sous le domaine non borné en livraison ; H_N qualifié propre à N : NT et bloquant. |
| A4 | Comparaison de toutes les ancres honnêtes dans AnchorBTCChecked | FAIL sous livraisons séparées ; une borne réseau ajoutée après construction ne répare pas l'histoire antérieure. |
| A5 / C6 | Moniteur local conservé ; C6 et C6Global sur engagements persistants | Contrôle limité à ADD et calendrier abstrait ; contrôle complet NT. Aucun filtre A3. |
| A-Rule | RegistryWindowChecked, seuils et fermeture ; supports dans le miroir | Maturité fixe réduite dans le miroir ; porteurs tardifs et rejet testés séparément. |
| Strong | RegistryImmutable historique inchangé, replays et générateur | PASS/FAIL séparés de C6 ; moniteur local oublie les anciennes époques. |
| H1-Subset | Audit de chaque autorisation dans H1OrdersChecked | Base N abstraite dans cette famille ; aucune promotion permise. |
| H1-NonVacuity | Données finales complètes et témoins CommonVeto/Maintain | Toutes permutations et livraisons groupées de six événements, deux nœuds. |
| H1-Relevance | H1Scan, dossiers étrangers/pertinents, UNKNOWN puis décidable | Scans réduits ; cryptographie et octets Bitcoin NT. |
| R1–R5 | Miroir absence/retour ; PersistenceChecked et AuthoritiesChecked | Pas de restauration composée de tout le nœud ; pas d'équité RECOVERY. |
| L1 | Deux époques vides, production tardive et avancement A atteints | Témoins d'existence, aucune croissance infinie. |
| L2 | Suffixe de réunion avec WF des réceptions et protections compatibles | Reprise générale infinie NT. |
| L3 | Frein mécanique, exclusions à e10/e17, rotation, équité de l'avancement | Conditions de support/calendrier données en entrée ; leur réalisation jointe par N reste NT. |
| S1 | Témoin durable externe, deux clones, toutes générations du modèle | Intégrité/disponibilité externe supposées ; protocole distribué NT. |
| S2 | Contextes/générations effectifs distincts, négatif non effectif | Sonde algébrique ; signatures cryptographiques et loterie non nécessaires à son prédicat. |
| G0 | Inventaire initial, scellement a1 retiré avec S0/repère inchangés | Nouveau refus et ancien STOP ; dépendances Bitcoin abstraites. |
| MON1–MON5 | Source BTC 10, imports/consommations, frais, commit/undo/crash | Noyau réduit ; sources typées multiples et émissions ticket/REACT, conversions et application complète NT. |

Un FAIL de CP_reg, A4 ou Strong sous les entrées publiées ne doit pas être renommé en erreur d'outil. Inversement, les erreurs de syntaxe, les successeurs incomplets et les timeouts des premiers essais ne sont pas des violations normatives. Les tests supplémentaires « convergence des réservations » et « cadence implique progrès frais » recherchent des affirmations plus fortes que la SPEC ; leurs FAIL ne constituent pas des violations de celle-ci.
