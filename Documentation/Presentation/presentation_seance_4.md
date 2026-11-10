# Support de Présentation — Projet AWD (Séance 4 : Validation Intermédiaire)

**Projet :** Plateforme SaaS All-in-One pour Entrepreneurs et Vendeurs en Ligne  
**Durée estimée :** 12 à 15 minutes  
**Format :** Présentation d'équipe + interventions individuelles (1 minute max par membre)  

---

## Sommaire de la Présentation

1. **Partie Groupe (6-7 min)**
   - Slide 1 : Titre & Composition de l'Équipe
   - Slide 2 : Idée Générale & Problématique
   - Slide 3 : Acteurs & Fonctionnalités par Module
   - Slide 4 : Architecture Globale Proposée (Gateway, Sécurité, Bus d'événements, Data)
   - Slide 5 : Découpage en Microservices & Bases de Données
   - Slide 6 : Choix Technologiques & Organisation Git
   - Slide 7 : Planning Prévisionnel & Gestion des Risques

2. **Partie Individuelle (1 minute chrono par membre)**
   - Slide 8 : **Membre 1 — Architecture, API Gateway & Identity & Access Service** *(Votre intervention)*
   - Slide 9 : **Membre 2 — Startup Builder & Brand Studio**
   - Slide 10 : **Membre 3 — Store Manager & Order/Inventory Manager**
   - Slide 11 : **Membre 4 — Marketing Studio, Analytics & AI Assistant**

3. **Partie Commune & Conclusion (2 min)**
   - Slide 12 : Le Microservice Commun Transverse (`Identity & Access` & Sécurité Partagée)
   - Slide 13 : Conclusion & Discussion (10 min)

---

## Diapositives Détaillées

### Slide 1 : Titre & Composition de l'Équipe
- **Sujet :** Plateforme SaaS All-in-One (B2B/B2C) pour porteurs de projet et vendeurs en ligne (Instagram, Facebook, TikTok).
- **Marché cible :** Afrique du Nord (Tunisie, Algérie, Maroc), évolutif à l'international.
- **Équipe (4 Membres) :**
  - **Membre 1 :** Architecture Globale, API Gateway, Identity & Access.
  - **Membre 2 :** Startup Builder & Brand Studio.
  - **Membre 3 :** Store Manager & Order / Inventory Manager.
  - **Membre 4 :** Marketing Studio, Analytics & AI Assistant.

---

### Slide 2 : Problématique & Proposition de Valeur
- **Constat :** Les jeunes créateurs et vendeurs sur réseaux sociaux utilisent aujourd'hui une multitude d'outils dispersés (notes pour l'idée, Canva pour la marque, Excel pour les stocks, messageries pour les commandes).
- **Proposition de valeur :** *« De la première idée à la croissance de son activité : les outils essentiels réunis dans une seule plateforme. »*
- **4 Objectifs clés :** Démarrer (parcours guidé) • Centraliser (boutique, commandes, stocks) • Améliorer (indicateurs analytiques) • Faire grandir (marketing & IA).

---

### Slide 3 : Acteurs & Fonctionnalités
- **4 Acteurs :**
  1. **Visiteur :** Découverte des offres et création de compte.
  2. **Débutant / Porteur de projet :** Création d'espace projet, parcours guidé, construction de marque.
  3. **Vendeur / Entrepreneur :** Gestion boutique, catalogue produits, commandes, stocks, campagnes et indicateurs.
  4. **Administrateur plateforme :** Gestion des comptes, rôles, signalements et supervision technique.
- **7 Modules Fonctionnels :** Startup Builder, Brand Studio, Store Manager, Order & Inventory, Marketing Studio, Business Analytics, AI Business Assistant.

---

### Slide 4 : Architecture Globale Proposée
*(Afficher le diagramme : `Documentation/Diagrams/architecture_globale.png`)*
- **Frontend Web Responsive :** Espace utilisateur & tableau de bord communiquant exclusivement via l'**API Gateway**.
- **API Gateway :** Routage centralisé (`/api/v1/*`), validation JWT *stateless* (JWKS) et rate limiting.
- **Principe Database per Service :** Chaque microservice possède sa base isolée (zéro accès croisé aux tables).
- **Communications Hybrides :** Synchrones (HTTP/REST pour réponses immédiates) et Asynchrones (Bus d'événements RabbitMQ/Kafka : `UserRegistered`, `OrderCreated`, `StockLow`, etc.).

---

### Slide 5 : Découpage en Microservices & Bases de Données
- `identity-service` : Comptes, profils, rôles RBAC, sessions (PostgreSQL + Redis).
- `startup-service` : Projets, objectifs, étapes, tâches (PostgreSQL).
- `brand-service` : Marques, slogans, assets visuels (PostgreSQL + Stockage objet S3).
- `store-service` : Boutiques, catégories, fiches produits, prix (PostgreSQL / MongoDB).
- `order-inventory-service` : Commandes, lignes, mouvements de stock, alertes (PostgreSQL).
- `marketing-service` : Campagnes, brouillons, calendrier éditorial (PostgreSQL).
- `analytics-ai-service` : Métriques, tableaux de bord, orchestrateur IA (PostgreSQL / Timescale).

---

### Slide 6 : Choix Technologiques & Organisation Git
- **Technologies envisagées :** Frontend React/Vue ; Backend homogène par service (Java Spring Boot ou Node.js/NestJS) ; PostgreSQL + Redis + Stockage objet S3 ; RabbitMQ/Kafka ; Docker.
- **Workflow Git :** Monorepo organisé (`Backend/`, `Frontend/`, `Documentation/`), branches `main`, `develop`, `feature/*`, `fix/*`, validation par Pull Request.

---

### Slide 7 : Planning & Gestion des Risques
- **Planning :**
  - *Séance 4 :* Cadrage, architecture, UML & contrats d'API.
  - *Séances 5-6 :* Développement des services, intégration du bus d'événements et Gateway.
  - *Séance 7 :* Tests d'intégration E2E, conteneurisation Docker et soutenance finale.
- **Principaux risques :** Cohérence commandes/stocks $\rightarrow$ règles strictes de réservation et événements compensatoires ; limites API externes $\rightarrow$ adaptateurs dédiés.

---

### Slide 8 : PARTIE INDIVIDUELLE — Membre 1 (1 minute chrono)
**Périmètre :** `Identity & Access Service` (+ Architecture & API Gateway)  
**Visuels projetés :** `class_diagram_auth_service.png` & `sequence_auth_flow.png`

- **Mission :** Gérer les utilisateurs et sécuriser l'accès à la plateforme.
- **Responsabilités :** Inscription & connexion (locale + OAuth2 Google/GitHub), gestion des profils, RBAC (isolation stricte entre Débutant, Vendeur et Administrateur), authentification/autorisation et gestion des sessions.
- **Conception :** Entités `User`, `UserProfile`, `Role`, `Permission`, `OAuthAccount`, `RefreshToken` (PostgreSQL + Redis).
- **Interactions :**
  - *Synchrone :* L'API Gateway valide les JWT de manière *stateless* via `GET /.well-known/jwks.json`.
  - *Asynchrone :* Publication de `UserRegisteredEvent` sur RabbitMQ (consommé par `Startup` et `Marketing` pour initialiser leurs espaces).
- **Contrats d'API :** `POST /api/v1/auth/register` (201/400/409), `POST /api/v1/auth/login` (200/401/403), `POST /api/v1/auth/refresh` (200/401), `GET /api/v1/users/me` (200/401).

---

### Slide 12 : Le Microservice Commun Transverse
- `identity-service` constitue le socle commun d'authentification et de propagation d'identité (`X-User-Id`, `X-User-Roles`) sur lequel s'appuient tous les autres microservices de l'équipe.

---

### Slide 13 : Conclusion & Questions
- Architecture modulaire, prête pour l'implémentation incrémentale.
- Merci pour votre attention — Place à la session de questions (10 minutes).
