# Plateforme SaaS All-in-One pour Entrepreneurs et Vendeurs en Ligne
> **Projet AWD — Architecture Orientée Microservices (Validation Intermédiaire — Séance 4)**

Une plateforme web SaaS B2B/B2C tout-en-un destinée aux personnes souhaitant lancer une activité (porteurs de projet / débutants) et aux commerçants vendant déjà via les réseaux sociaux (Instagram, Facebook, TikTok). Elle centralise la structuration de projet, la création de marque, la boutique, les commandes, les stocks, le marketing, l'analytique et l'assistance IA.

---

## Répartition de l'Équipe & Responsabilités

| Membre | Pôle & Microservices | Responsabilités Clés |
| :--- | :--- | :--- |
| **Membre 1** | **Architecture & Identity** | Architecture globale, API Gateway, `identity-service` (inscription/connexion, profils, rôles RBAC, sécurité et sessions) |
| **Membre 2** | **Startup & Brand** | `startup-service` (projets de création, objectifs, étapes, tâches) et `brand-service` (identité de marque, logos, ressources visuelles) |
| **Membre 3** | **Store & Operations** | `store-service` (boutiques, catalogue produits, prix) et `order-inventory-service` (commandes, mouvements et alertes de stock) |
| **Membre 4** | **Marketing, Analytics & AI** | `marketing-service` (campagnes, calendrier éditorial), `analytics-service` (indicateurs) et `ai-assistant-service` (assistant IA) |

---

## Architecture Globale du Système

L'architecture suit le principe **Database per Service**, avec un point d'entrée unique via l'**API Gateway** et un bus d'événements asynchrones (**RabbitMQ / Kafka**) pour le découplage entre services :

![Architecture Globale](Documentation/Diagrams/architecture_globale.png)

---

## Organisation Générale du Dépôt Git

```
projet-awd-main/
├── Backend/                               # Code source des microservices & API Gateway
│   ├── api-gateway/                       # Routage, authentification & limitation de débit
│   ├── identity-service/                  # Comptes, profils, rôles & permissions
│   ├── startup-service/                   # Projets de création, étapes & tâches
│   ├── brand-service/                     # Identité de marque & gestion des médias
│   ├── store-service/                     # Boutiques & catalogue produits
│   ├── order-inventory-service/           # Commandes, expéditions & stocks
│   ├── marketing-service/                 # Campagnes & calendrier éditorial
│   ├── analytics-service/                 # Agrégation des événements & indicateurs
│   └── ai-assistant-service/              # Orchestrateur d'assistance IA
│
├── Frontend/                              # Application Web Responsive (React / Vue / Angular)
│
├── Documentation/                         # Dossiers techniques, diagrammes & présentations
│   ├── Dossier_Technique.md               # Document technique global (Rendu Blackboard)
│   │
│   ├── Diagrams/                          # Diagrammes UML & Architecture (PlantUML, PNG, SVG, PDF)
│   │   ├── architecture_globale.*         # Diagramme d'architecture globale
│   │   ├── use_case_global.*              # Diagramme de cas d'utilisation général
│   │   ├── Diagramme_Cas_Utilisation.pdf  # Fiche explicative du cas d'utilisation
│   │   └── ...                            # Diagrammes de classes & séquences par microservice
│   │
│   └── Presentation/                      # Supports de soutenance orale (Séance 4)
│
└── README.md                              # Documentation générale du dépôt
```

---

## Workflow Git

- **`main`** : Version stable et présentable.
- **`develop`** : Intégration des fonctionnalités validées.
- **`feature/<nom>`** : Développement d'une fonctionnalité ou d'un microservice.
- **`fix/<nom>`** : Correction ciblée.
- Chaque contribution passe par une **Pull Request**, une revue de code et des tests avant fusion.

---

## Livrables de la Séance 4

- **Diagramme d'Architecture Globale :** [`Documentation/Diagrams/architecture_globale.png`](Documentation/Diagrams/architecture_globale.png)
- **Dossier Technique Global :** [`Documentation/Dossier_Technique.md`](Documentation/Dossier_Technique.md)
- **Diagramme de Cas d'Utilisation :** [`Documentation/Diagrams/Diagramme_Cas_Utilisation.pdf`](Documentation/Diagrams/Diagramme_Cas_Utilisation.pdf)
