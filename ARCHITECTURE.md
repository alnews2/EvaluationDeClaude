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

## 2026-09-14 — Construction multi-plateforme (CI)

### Problème

PyInstaller ne fait pas de compilation croisée : un exécutable Windows ne
peut être produit qu'en exécutant PyInstaller sur Windows (idem pour
macOS). L'environnement de développement utilisé ici est Linux uniquement.

### Solution retenue : GitHub Actions

Un workflow (`.github/workflows/build.yml`) se déclenche à chaque push sur
`main` et à la demande. Il :

1. Lance la suite de tests sur `ubuntu-latest` (garde-fou avant toute
   construction).
2. Construit l'exécutable en parallèle sur `ubuntu-latest` et
   `windows-latest` via PyInstaller, et publie chaque binaire comme
   artefact téléchargeable.

**Raison** : c'est l'approche standard pour ce problème (plutôt qu'un
bricolage de cross-compilation, peu fiable pour des bindings Qt). Elle a
aussi l'avantage de garantir que les tests passent avant toute
construction, et de tracer chaque build dans l'historique GitHub Actions.

**Limite connue** : l'exécutable Windows n'est pas signé numériquement.
Windows SmartScreen pourra afficher un avertissement au premier lancement
("Éditeur inconnu") — normal pour un exécutable non signé, pas un signe de
dysfonctionnement. Une signature de code est envisageable si le projet
grossit, mais suppose l'achat d'un certificat, jugé disproportionné ici.

### Distribution des exécutables via GitHub Release plutôt qu'artefacts CI

Les artefacts de workflow GitHub Actions sont téléchargeables uniquement
via une redirection vers un stockage Azure Blob, que l'environnement de
développement local n'a pas le droit d'atteindre (restriction réseau de
sécurité). Pour rester capable de récupérer et vérifier moi-même les
binaires produits avant de les remettre, le workflow publie donc les
exécutables comme fichiers attachés à une GitHub Release
(tag `dernieres-constructions`, mise à jour à chaque construction réussie)
plutôt que comme simples artefacts de run. Les releases sont accessibles
sur un domaine autorisé.

### Formatage de l'affichage

Séparateur décimal `,` (convention française) plutôt que `.`. Les résultats
entiers sont affichés sans décimale superflue (`4` plutôt que `4.0`).

## 2026-09-17 — Versionnement et journal des modifications

### Adoption de SemVer + Keep a Changelog

Le projet adopte le [Versionnement Sémantique](https://semver.org/lang/fr/)
(`pyproject.toml`, champ `version`) et tient un `CHANGELOG.md` au format
[Keep a Changelog](https://keepachangelog.com/fr/1.1.0/).

**Choix pour la plage de versions** : le projet reste en `0.y.z` (phase de
développement initial selon SemVer) tant que l'application n'est pas jugée
stable dans ses fonctionnalités de base. Les incréments mineurs (`0.x.0`)
correspondent à des ajouts de fonctionnalité ou des changements visibles
notables ; les incréments de correctif (`0.x.y`) seraient réservés aux
corrections de bug sans changement de comportement voulu.

**Historique reconstitué rétroactivement** : les versions 0.1.0 à 0.3.0
n'avaient pas été formellement taguées au moment de leur livraison ; des
tags Git annotés (`v0.1.0`, `v0.2.0`, `v0.3.0`) ont été créés a posteriori
sur les commits correspondants pour que le changelog et ses liens de
comparaison GitHub restent exacts et vérifiables.
