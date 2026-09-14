# Décisions d'architecture

Ce document trace les choix de conception significatifs et leur raison d'être,
au fil des évolutions du projet.

## 2026-09-14 — Choix initiaux

### Langage : Python

Retenu pour la rapidité d'itération (pas de compilation, cycles courts entre
retours et ajustements) et la richesse de l'écosystème desktop mature.

### Framework IHM : PySide6 (Qt6)

Alternatives envisagées : Tauri (Rust + webview), Electron.

- **Tauri** offre des binaires plus légers et une sécurité par défaut plus
  stricte, mais nécessite un rendu webview que l'environnement de
  développement ne peut pas vérifier visuellement de façon fiable avant
  livraison. Écarté pour cette raison précise (pas de rejet de principe :
  à reconsidérer si l'environnement de vérification évolue).
- **Electron** jugé trop lourd et daté par rapport à Tauri, sans bénéfice
  compensatoire ici.
- **PySide6** retenu : rendu natif, widgets riches, écosystème mature,
  et surtout vérifiable visuellement (capture d'écran via Qt `grab()`)
  avant chaque livraison.

### Séparation logique métier / IHM

Le projet est structuré en deux couches explicitement séparées :

- `src/calculatrice/moteur.py` : logique de calcul pure, aucune dépendance
  à Qt. Contient `calculer()` (fonction pure) et `MachineCalculatrice`
  (machine à états gérant l'affichage, à la manière d'une calculatrice
  physique : saisie, opération, second nombre, résultat sur `=`).
- `src/calculatrice/fenetre.py` : IHM Qt, ne fait que traduire les clics
  en appels au moteur et refléter son état.

**Raison** : cette séparation permet des tests unitaires rapides et fiables
sur la logique (sans dépendance à un environnement graphique), et limite le
risque de régression silencieuse quand l'IHM évolue indépendamment de la
logique (ou inversement).

### Stratégie de test à deux niveaux

- **Tests unitaires** (`tests/test_moteur.py`) sur la logique pure, via
  `pytest`. C'est la couche qui protège le plus efficacement contre les
  régressions au fil des évolutions incrémentales.
- **Tests d'intégration IHM** (`tests/test_fenetre.py`) via `pytest-qt`,
  qui simulent de vrais clics sur les boutons Qt et vérifient l'affichage
  résultant.
- **Vérification visuelle** : capture d'écran de l'IHM en fonctionnement
  (rendue via le driver Qt `offscreen`, l'environnement ne disposant pas
  nativement d'un serveur X complet avec support xcb) avant chaque livraison.
  Complémentaire aux tests automatisés, pas un substitut : les tests
  garantissent la non-régression entre deux sessions de travail, la capture
  garantit que le rendu correspond visuellement à l'attendu.

### Gestion de version

Dépôt Git poussé directement sur GitHub (`alnews2/EvaluationDeClaude`) via
un token d'accès personnel restreint à ce dépôt. Alternative écartée :
livraison de patches/archives à appliquer manuellement — plus sûre côté
partage de secret, mais moins fluide ; le token restreint et à expiration
a été jugé suffisamment sûr pour ce contexte.

### Formatage de l'affichage

Séparateur décimal `,` (convention française) plutôt que `.`. Les résultats
entiers sont affichés sans décimale superflue (`4` plutôt que `4.0`).
