# Mandat — correctif N-SPEC v0.5 : immutabilité du registre d'époque (constat TLA+)

Contexte : lis RAPPORT-TLA-N.md (ce dossier), en particulier « Modèle conforme : cliché ancien remplacé dans la même époque »
(MC_spec_registryreorg, MC_replay_spec, MC_replay_spec_adopt). Constat : §5.2 date le cliché du registre en CRÉNEAUX
(cut(e)), §9.6 protège les réorgs en BLOCS (maxreorg + ancre). Après des créneaux vides, un bloc « ancien en créneaux »
reste réorganisable : un nœud honnête peut engager deux registres dans la même époque, sans RECOVERY, sans H1, sans mutation.

Contraintes propriétaire (non négociables) :
- PAS de verrou local de registre (supprimés en v0.5 : cause racine de la relecture aveugle précédente, divergences entre nœuds).
- H1 = détecteur seulement ; une preuve Bitcoin ne rend jamais canonique une histoire que la fork-choice N n'aurait pas choisie.
- Fork-choice mécanique, pas de vote ; N pur ; checkpoint A′ sans pouvoir sur un nœud synchronisé ; STOP + RECOVERY explicite.

Travail demandé :
1. Qualifier : défaut réel de la SPEC, ou propriété 6 du mandat trop forte (et alors laquelle est la bonne, formellement) ?
   Comparer avec Ouroboros Praos/Genesis, Sleepy, Snow White (stake distribution lag, common prefix en slots vs blocs, densité).
2. Au moins 3 options de correctif normatif, par ex. : cliché défini par profondeur en blocs ET créneaux ; règle de densité
   (époque/fenêtre sous densité minimale ⇒ pas de nouveau cliché / registre hérité) ; STOP quand une réorg changerait le
   registre d'une époque déjà engagée (distinguer d'un verrou) ; autre. Pour chacune : effet sur accord, vivacité
   (époques vides, retour après absence), grinding, complexité, cohérence avec §5.7, §9.6, §12.
3. Recommandation + patch normatif précis (texte à insérer dans N-SPEC, sections touchées).
4. Implémenter l'option recommandée dans une COPIE du modèle (NModel_v06.tla, sans toucher NModel.tla) et relancer :
   MC_safe, MC_spec_registryreorg, MC_replay_spec_adopt, MC_live, les deux mutations, les témoins d'époque vide.
   Les runs doivent rester < 10 min chacun ; un run interrompu n'est pas un PASS.
Livrable : CORRECTIF-REGISTRE.md dans ce dossier (français, direct, tableaux), + modèle et logs. Ne modifie pas le dépôt git.
