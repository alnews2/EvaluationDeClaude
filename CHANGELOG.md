# Journal des modifications

Toutes les modifications notables de ce projet sont documentées dans ce
fichier.

Le format s'inspire de [Keep a Changelog](https://keepachangelog.com/fr/1.1.0/),
et ce projet adhère au [Versionnement Sémantique](https://semver.org/lang/fr/)
(SemVer). Le projet étant en développement initial (version `0.y.z`), l'API
et le comportement de l'application peuvent encore changer sans préavis
majeur d'une version mineure à l'autre.

## [Non publié]

### Modifié

- CI : la publication de la release automatique (`publier_release`)
  n'utilise plus l'action tierce `softprops/action-gh-release` mais des
  appels directs à `gh` (CLI officielle GitHub), avec 3 tentatives
  automatiques en cas d'échec transitoire. Objectif : plus de robustesse
  et moins de dépendances externes au workflow.

## [0.4.0] - 2026-09-17

### Modifié

- Le résultat affiché est désormais entouré d'un cadre (bordure arrondie,
  fond légèrement distinct) pour le distinguer visuellement du reste de
  la fenêtre.

## [0.3.0] - 2026-09-16

### Ajouté

- Mention « Application générée par l'intelligence artificielle Claude de
  la société Anthropic. » affichée en italique en bas de la fenêtre.

## [0.2.0] - 2026-09-14

### Ajouté

- Intégration continue (GitHub Actions) : exécution automatique de la
  suite de tests puis construction des exécutables Linux et Windows à
  chaque évolution poussée sur `main`.
- Publication automatique des exécutables sous forme de GitHub Release
  (tag `dernieres-constructions`, mise à jour à chaque build réussi).

## [0.1.0] - 2026-09-14

### Ajouté

- Version initiale de la calculatrice : les quatre opérations (addition,
  soustraction, multiplication, division), avec gestion de la division
  par zéro et des nombres décimaux.
- Interface graphique de bureau (PySide6 / Qt6).
- Suite de tests (unitaires sur le moteur de calcul, intégration sur
  l'IHM via `pytest-qt`).
- Documentation d'architecture (`ARCHITECTURE.md`) et `README.md`.

[Non publié]: https://github.com/alnews2/EvaluationDeClaude/compare/v0.4.0...HEAD
[0.4.0]: https://github.com/alnews2/EvaluationDeClaude/compare/v0.3.0...v0.4.0
[0.3.0]: https://github.com/alnews2/EvaluationDeClaude/compare/v0.2.0...v0.3.0
[0.2.0]: https://github.com/alnews2/EvaluationDeClaude/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/alnews2/EvaluationDeClaude/releases/tag/v0.1.0
