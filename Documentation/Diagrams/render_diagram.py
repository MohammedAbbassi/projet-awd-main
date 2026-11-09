import plantuml

code = """@startuml
left to right direction
skinparam packageStyle rectangle
skinparam roundcorner 8
skinparam shadowing false
skinparam actorStyle awesome
skinparam defaultFontName Arial
skinparam defaultFontSize 11
skinparam dpi 200

skinparam usecase {
  BackgroundColor #F8FAFC
  BorderColor #2B6CB0
  ArrowColor #2D3748
}

actor "Client (Acheteur)" as Client
actor "Marchand" as Marchand

rectangle "Plateforme OmniShop" {
  package "Espace Client" {
    usecase "Rechercher des produits" as UC_Search
    usecase "Gérer son panier" as UC_Cart
    usecase "Passer une commande" as UC_Order
    usecase "Payer la commande" as UC_Pay
    usecase "Suivre ses achats" as UC_Track
  }

  package "Administration & Sécurité" {
    usecase "S'authentifier" as UC_Auth
    usecase "Gérer les comptes utilisateurs" as UC_ManageUsers
    usecase "Gérer les abonnements marchands" as UC_ManageSubs
    usecase "Superviser la plateforme\\n(Litiges)" as UC_Supervise
  }

  package "Espace Marchand" {
    usecase "Configurer sa boutique" as UC_Store
    usecase "Gérer le catalogue\\n(Stocks/Prix B2B-B2C)" as UC_Catalog
    usecase "Traiter les commandes clients" as UC_ProcessOrder
    usecase "Consulter les statistiques\\n(Analytique)" as UC_Analytics
  }
}

actor "Administrateur" as Admin

' Client a gauche
Client --> UC_Auth
Client --> UC_Search
Client --> UC_Cart
Client --> UC_Order
Client --> UC_Track

' Include
UC_Order .[#2B6CB0].> UC_Pay : <<include>>

' Marchand a droite
UC_Auth <-- Marchand
UC_Store <-- Marchand
UC_Catalog <-- Marchand
UC_ProcessOrder <-- Marchand
UC_Analytics <-- Marchand

' Admin en bas
Admin --> UC_Auth
Admin --> UC_ManageUsers
Admin --> UC_ManageSubs
Admin --> UC_Supervise

@enduml"""

server_png = plantuml.PlantUML("https://www.plantuml.com/plantuml/img/")
png_b = server_png.processes(code)
with open("Documentation/Diagrams/use_case_omnishop.png", "wb") as f:
    f.write(png_b)

server_svg = plantuml.PlantUML("https://www.plantuml.com/plantuml/svg/")
svg_b = server_svg.processes(code)
with open("Documentation/Diagrams/use_case_omnishop.svg", "wb") as f:
    f.write(svg_b)

with open("Documentation/Diagrams/use_case_omnishop.puml", "w", encoding="utf-8") as f:
    f.write(code)

print("Diagram generated!")
