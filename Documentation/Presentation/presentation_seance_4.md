# Support de Présentation — Projet AWD (Séance 4 : Validation Intermédiaire)

**Projet :** Plateforme E-Commerce Multi-Acteurs OmniShop  
**Durée estimée :** 12 à 15 minutes  
**Format :** Présentation d'équipe + interventions individuelles (1 minute par membre)  

---

## Sommaire de la Présentation

1. **Partie Groupe (6-7 min)**
   - Slide 1 : Titre & Équipe
   - Slide 2 : Problématique & Proposition de Valeur (OmniShop)
   - Slide 3 : Acteurs & Cas d'Utilisation Généraux
   - Slide 4 : Architecture Globale Proposée (Gateway, Sécurité, Microservices, Broker)
   - Slide 5 : Stack Technologique & Justifications
   - Slide 6 : Organisation du Dépôt Git & Gestion de Projet (Kanban/GitHub Projects)
   - Slide 7 : Planning Prévisionnel & Gestion des Risques

2. **Partie Individuelle (1 min par microservice / par membre)**
   - Slide 8 : **Membre 1 — Identity & Access Service (OAuth2, RBAC, Sessions)** 🌟 *(Votre intervention)*
   - Slide 9 : Membre 2 — Catalog & Pricing Service (Stocks & Tarifs B2B/B2C)
   - Slide 10 : Membre 3 — Order & Cart Service (Commandes & Calculs)
   - Slide 11 : Membre 4 — Store & Merchant Service (Boutiques & Litiges)

3. **Partie Commune & Conclusion (2 min)**
   - Slide 12 : Le Microservice Commun Transverse (Gestion d'Identité & Sécurité Partagée)
   - Slide 13 : Conclusion & Session de Questions/Réponses (10 min)

---

## Diapositives Détaillées

---

### Slide 1 : Titre & Composition de l'Équipe
- **Titre du projet :** OmniShop — Plateforme E-Commerce Hybride B2B/B2C en Architecture Microservices
- **Membres du groupe :**
  - **Membre 1 :** Responsable *Identity & Access Service*
  - **Membre 2 :** Responsable *Catalog & Inventory Service*
  - **Membre 3 :** Responsable *Order & Cart Service*
  - **Membre 4 :** Responsable *Store & Merchant Service*

---

### Slide 2 : Problématique & Présentation d'OmniShop
- **Constat :** Les plateformes e-commerce traditionnelles séparent souvent artificiellement les acheteurs particuliers (B2C) et professionnels (B2B).
- **Notre solution OmniShop :** 
  - Une place de marché unifiée multi-vendeurs avec gestion fine des accès.
  - Double tarification transparente (prix unitaire public vs tarifs dégressifs HT négociés B2B).
  - Architecture modulaire résiliente capable d'absorber des montées en charge asymétriques.

---

### Slide 3 : Périmètre Fonctionnel & Acteurs
*(Affichage du diagramme de cas d'utilisation généré : `Documentation/Diagrams/use_case_omnishop.png`)*
- **3 Acteurs Clés :**
  - **Client (Acheteur) :** Navigation, panier persistant, commande sécurisée, suivi d'expédition.
  - **Marchand (Vendeur) :** Paramétrage boutique, catalogue multi-tarifs, traitement des commandes, analytique.
  - **Administrateur :** Modération des comptes, abonnements marchands, arbitrage des litiges.
- **Règles métier structurantes :** Relation `<<include>>` entre *Passer commande* et *Payer la commande*.

---

### Slide 4 : Architecture Globale Proposée
- **Frontend :** SPA / PWA réactive (React / Next.js).
- **Point d'entrée unique :** **API Gateway** (Spring Cloud Gateway ou Kong) assurant le routage dynamique, le rate-limiting et la validation stateless des tokens JWT.
- **Microservices Métier :**
  - `identity-service` (PostgreSQL + Redis)
  - `catalog-service` (MongoDB pour la flexibilité des attributs produits)
  - `order-service` (PostgreSQL pour la conformité transactionnelle)
  - `store-service` (PostgreSQL)
- **Communications Asynchrones :** **RabbitMQ** comme bus d'événements pour le découplage des opérations lentes (notifications, création de boutiques).

---

### Slide 5 : Stack Technologique
- **Backend :** Java (Spring Boot) / Node.js (TypeScript) avec Docker & Docker Compose.
- **Bases de données :** Polyglot Persistence (PostgreSQL relationnel pour les flux financiers & profils ; MongoDB pour le catalogue ; Redis pour les sessions & cache).
- **Communication :** RESTful APIs documentées OpenAPI 3.0 + AMQP (RabbitMQ).
- **Sécurité :** OAuth2, OpenID Connect, JWT (RS256) avec clés publiques JWKS.

---

### Slide 6 : Organisation Git & Méthodologie
- **Dépôt Git :** Organisation modulaire avec branches par fonctionnalité (`feature/auth-oauth`, `feature/catalog-b2b`), pull requests et revues de code obligatoires.
- **Gestion de projet :** Tableau Kanban (GitHub Projects) avec jalons hebdomadaires.

---

### Slide 7 : Planning & Gestion des Risques
- **Séance 4 (actuelle) :** Cadrage, architecture globale, contrats d'API et diagrammes de conception.
- **Séance 5-6 :** Développement des microservices indépendants et du broker.
- **Séance 7 :** Intégration globale, passerelle API Gateway et tests end-to-end.
- **Risques identifiés & parades :**
  - *Latence inter-services* $\rightarrow$ Adoption de JWT stateless (JWKS) et mise en cache Redis.
  - *Désynchronisation de données* $\rightarrow$ Pattern Outbox & événements idempotents sur RabbitMQ.

---

### Slide 8 : 🌟 PARTIE INDIVIDUELLE — Membre 1 (1 minute chrono)

**Microservice :** `Identity & Access Service`  
**Intervenant :** Membre 1  
**Visuels projetés :** 
1. Diagramme de classes (`Documentation/Diagrams/class_diagram_auth_service.png`)
2. Diagramme de flux OAuth2 & événements (`Documentation/Diagrams/sequence_auth_flow.png`)

#### Contenu présenté :
- **Mission :** Gérer les utilisateurs et sécuriser l'accès à la plateforme.
- **Responsabilités clés :**
  - Inscription/connexion locale et fédérée via **OAuth2 & OpenID Connect** (Google, GitHub).
  - Gestion des profils utilisateurs et traçabilité des comptes.
  - Modèle d'autorisation **RBAC** (rôles et permissions granulaires) garantissant un cloisonnement strict entre l'espace acheteur débutant et le cockpit vendeur marchand.
  - Gestion sécurisée des sessions via couple **Access Token (JWT court)** et **Refresh Token (Redis avec révocation temps réel)**.
- **Contrats d'API principaux :**
  - `POST /api/v1/auth/register` (201 / 400 / 409)
  - `POST /api/v1/auth/login` (200 / 401)
  - `GET /api/v1/auth/oauth2/authorize/{provider}` (302)
  - `GET /.well-known/jwks.json` (200, diffusion des clés publiques)
- **Interactions :**
  - *Synchrone :* L'API Gateway vérifie les JWT de façon autonome via JWKS.
  - *Asynchrone :* Émission de `UserRegisteredEvent` sur RabbitMQ pour déclencher l'accueil utilisateur et l'instanciation de boutique.

---

### Slide 12 : Le Microservice Commun Transverse
- Présenté par un membre pour l'ensemble du groupe.
- `identity-service` constitue la brique commune développée en synergie :
  - Standardise le schéma d'authentification pour toute l'équipe.
  - Fournit la bibliothèque commune de validation des tokens et de propagation du contexte d'identité (`SecurityContext` partagé).

---

### Slide 13 : Conclusion & Questions
- Architecture découplée, évolutive et prête pour la phase d'implémentation.
- Merci de votre attention — Place aux questions (10 minutes).

