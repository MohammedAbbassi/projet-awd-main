import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, PageBreak
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas professionnel avec en-tête et pagination dynamique 'Page X sur Y'"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        # En-tête
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2B6CB0"))
        self.drawString(1.8 * cm, A4[1] - 1.2 * cm, "PROJET AWD — PLATEFORME OMNISHOP")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(A4[0] - 1.8 * cm, A4[1] - 1.2 * cm, "Conception UML : Diagramme de Cas d'Utilisation")
        
        self.setStrokeColor(colors.HexColor("#E2E8F0"))
        self.setLineWidth(0.8)
        self.line(1.8 * cm, A4[1] - 1.35 * cm, A4[0] - 1.8 * cm, A4[1] - 1.35 * cm)

        # Pied de page
        self.line(1.8 * cm, 1.4 * cm, A4[0] - 1.8 * cm, 1.4 * cm)
        self.setFont("Helvetica", 8)
        self.drawString(1.8 * cm, 1.0 * cm, "Validation Intermédiaire — Rendu Séance 4")
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(A4[0] - 1.8 * cm, 1.0 * cm, page_str)
        self.restoreState()

def generate_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(script_dir, "Diagramme_Cas_Utilisation_OmniShop.pdf")
    img_path = os.path.join(script_dir, "Diagrams", "use_case_omnishop.png")

    doc = SimpleDocTemplate(
        output_pdf,
        pagesize=A4,
        leftMargin=1.8 * cm,
        rightMargin=1.8 * cm,
        topMargin=1.8 * cm,
        bottomMargin=1.8 * cm
    )

    styles = getSampleStyleSheet()

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=3
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=8
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=10,
        spaceAfter=5,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=13,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=7,
        spaceAfter=3,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.8,
        leading=12.2,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=4
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8.5,
        leading=11.8,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=12,
        spaceAfter=2
    )

    table_header_style = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#1A365D")
    )

    table_cell_style = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2D3748")
    )

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("Diagramme de Cas d'Utilisation Général", title_style))
    story.append(Paragraph("<b>Projet AWD — Plateforme OmniShop</b> | Architecture & Modélisation Fonctionnelle", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2B6CB0"), spaceAfter=8))

    story.append(Paragraph("1. Vue Globale du Système OmniShop", h1_style))
    story.append(Paragraph(
        "Ce diagramme formalise l'ensemble des interactions entre les trois types d'acteurs identifiés et "
        "le périmètre applicatif de la <b>Plateforme OmniShop</b>.",
        body_style
    ))
    story.append(Spacer(1, 4))

    # Intégration de l'image (dimensionnée pour occuper la page 1 avec élégance)
    if os.path.exists(img_path):
        with PILImage.open(img_path) as pil_img:
            img_w, img_h = pil_img.size
        
        # Largeur max disponible : 17.4 cm
        # Hauteur max allouée sur Page 1 : 19.5 cm
        max_w = 17.4 * cm
        max_h = 19.5 * cm
        
        ratio = img_w / img_h
        target_h = max_h
        target_w = target_h * ratio
        
        if target_w > max_w:
            target_w = max_w
            target_h = target_w / ratio

        img = Image(img_path, width=target_w, height=target_h)
        
        img_table = Table([[img]], colWidths=[17.4 * cm])
        img_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
            ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#E2E8F0")),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
            ('TOPPADDING', (0, 0), (-1, -1), 4),
            ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ]))
        story.append(img_table)

    story.append(PageBreak())

    # ================= PAGE 2 =================
    story.append(Paragraph("2. Explication Détaillée du Diagramme", h1_style))
    
    story.append(Paragraph("2.1 Périmètre du Système : « Plateforme OmniShop »", h2_style))
    story.append(Paragraph(
        "Le grand cadre rectangulaire délimite le <b>système logiciel</b>. Tous les cas d'utilisation "
        "(ellipses) représentent des fonctionnalités logiques internalisées et exécutées par les microservices "
        "de la plateforme OmniShop. Les acteurs (figures humaines) sont externes et initient les processus métier.",
        body_style
    ))

    story.append(Paragraph("2.2 Description des Acteurs et de leurs Rôles", h2_style))

    story.append(Paragraph("<b>1. Client (Acheteur) — Positionné à gauche</b>", body_style))
    story.append(Paragraph("• <b>Rechercher des produits :</b> Consultation du catalogue dynamique, recherche multicritères, filtres par catégorie, prix et disponibilité.", bullet_style))
    story.append(Paragraph("• <b>Gérer son panier :</b> Ajout, modification des quantités, suppression d'articles et calcul automatique du sous-total.", bullet_style))
    story.append(Paragraph("• <b>Passer une commande :</b> Validation des articles du panier, renseignement des adresses de livraison/facturation et choix du transporteur.", bullet_style))
    story.append(Paragraph("• <b>Suivre ses achats :</b> Historique des commandes passées, consultation de l'état d'avancement de la livraison en temps réel.", bullet_style))
    story.append(Paragraph("• <b>S'authentifier :</b> Création de compte et connexion sécurisée (Tokens JWT / OAuth2).", bullet_style))

    story.append(Paragraph("<b>2. Marchand (Vendeur) — Positionné à droite</b>", body_style))
    story.append(Paragraph("• <b>Configurer sa boutique :</b> Gestion de l'identité commerciale du vendeur (logo, coordonnées, délais d'expédition, politique de retour).", bullet_style))
    story.append(Paragraph("• <b>Gérer le catalogue (Stocks/Prix B2B-B2C) :</b> Publication de fiches produits, ajustement des stocks en temps réel et gestion d'une double grille tarifaire (prix public TTC pour le B2C et tarifs dégressifs / HT pour le B2B).", bullet_style))
    story.append(Paragraph("• <b>Traiter les commandes clients :</b> Réception des ordres d'achat, préparation des colis, génération des bordereaux d'expédition et mise à jour du statut.", bullet_style))
    story.append(Paragraph("• <b>Consulter les statistiques (Analytique) :</b> Visualisation des indicateurs clés (chiffre d'affaires, panier moyen, volumes vendus, conversion).", bullet_style))
    story.append(Paragraph("• <b>S'authentifier :</b> Accès restreint et authentifié au portail de gestion marchand.", bullet_style))

    story.append(Paragraph("<b>3. Administrateur — Positionné en bas</b>", body_style))
    story.append(Paragraph("• <b>Gérer les comptes utilisateurs :</b> Modération des profils, activation, suspension ou suppression de comptes clients et marchands.", bullet_style))
    story.append(Paragraph("• <b>Gérer les abonnements marchands :</b> Gestion des formules d'abonnement (plans mensuels/annuels) et perception des commissions sur ventes.", bullet_style))
    story.append(Paragraph("• <b>Superviser la plateforme (Litiges) :</b> Arbitrage des réclamations clients non résolues par les marchands et surveillance de la conformité générale.", bullet_style))
    story.append(Paragraph("• <b>S'authentifier :</b> Authentification forte pour accéder à la console d'administration centrale.", bullet_style))

    story.append(Paragraph("2.3 Relations Clés et Justifications Techniques", h2_style))

    table_data = [
        [
            Paragraph("<b>Relation UML</b>", table_header_style),
            Paragraph("<b>Éléments liés</b>", table_header_style),
            Paragraph("<b>Justification Métier & Technique</b>", table_header_style)
        ],
        [
            Paragraph("<b>&laquo;include&raquo;</b><br/>(Inclusion obligatoire)", table_cell_style),
            Paragraph("Passer une commande<br/>&rarr; Payer la commande", table_cell_style),
            Paragraph("La validation finale d'un ordre d'achat requiert obligatoirement l'étape de paiement. "
                      "Le cas <i>Passer une commande</i> déclenche systématiquement le flux de transaction financière.", table_cell_style)
        ],
        [
            Paragraph("<b>Association transverse</b>", table_cell_style),
            Paragraph("Tous les acteurs<br/>&rarr; S'authentifier", table_cell_style),
            Paragraph("Point d'accès sécurisé commun. Assure le contrôle d'accès basé sur les rôles (RBAC) "
                      "et garantit l'intégrité et la confidentialité des données entre Clients, Marchands et Administrateurs.", table_cell_style)
        ]
    ]

    summary_table = Table(table_data, colWidths=[3.8 * cm, 4.4 * cm, 9.2 * cm])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 5),
        ('RIGHTPADDING', (0, 0), (-1, -1), 5),
    ]))
    story.append(summary_table)

    # Compilation
    doc.build(story, canvasmaker=NumberedCanvas)
    print("Clean PDF built successfully at:", output_pdf)

if __name__ == "__main__":
    generate_pdf()
