import os
from PIL import Image as PILImage
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import cm
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Image, Table, TableStyle, HRFlowable, PageBreak, KeepTogether
)
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """En-tête et pied de page avec numérotation 'Page X sur Y'"""
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
        self.drawString(1.8 * cm, A4[1] - 1.2 * cm, "PROJET AWD — OMNISHOP | VALIDATION SÉANCE 4")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        self.drawRightString(A4[0] - 1.8 * cm, A4[1] - 1.2 * cm, "Partie Individuelle : Identity & Access Service")
        
        self.setStrokeColor(colors.HexColor("#CBD5E0"))
        self.setLineWidth(0.8)
        self.line(1.8 * cm, A4[1] - 1.35 * cm, A4[0] - 1.8 * cm, A4[1] - 1.35 * cm)

        # Pied de page
        self.line(1.8 * cm, 1.4 * cm, A4[0] - 1.8 * cm, 1.4 * cm)
        self.setFont("Helvetica-Bold", 8)
        self.setFillColor(colors.HexColor("#2D3748"))
        self.drawString(1.8 * cm, 1.0 * cm, "Membre 1 — Responsable Microservice IAM & Authentification")
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#718096"))
        page_str = f"Page {self._pageNumber} sur {page_count}"
        self.drawRightString(A4[0] - 1.8 * cm, 1.0 * cm, page_str)
        self.restoreState()

def create_image_box(img_path, max_w, max_h):
    if not os.path.exists(img_path):
        return Paragraph(f"<i>Image introuvable : {os.path.basename(img_path)}</i>", ParagraphStyle('Missing', fontName='Helvetica', fontSize=8))
    
    with PILImage.open(img_path) as pil_img:
        w, h = pil_img.size
    
    ratio = w / h
    target_h = max_h
    target_w = target_h * ratio
    if target_w > max_w:
        target_w = max_w
        target_h = target_w / ratio
        
    img = Image(img_path, width=target_w, height=target_h)
    img_table = Table([[img]], colWidths=[max_w])
    img_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#F8FAFC")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#E2E8F0")),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
    ]))
    return img_table

def generate_pdf():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_pdf = os.path.join(script_dir, "Fiche_Individuelle_Membre1_Identity_Access.pdf")
    class_img = os.path.join(script_dir, "Diagrams", "class_diagram_auth_service.png")
    seq_img = os.path.join(script_dir, "Diagrams", "sequence_auth_flow.png")

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
        fontSize=16,
        leading=20,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=2
    )

    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13,
        textColor=colors.HexColor("#4A5568"),
        spaceAfter=6
    )

    h1_style = ParagraphStyle(
        'SectionH1',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'SectionH2',
        parent=styles['Heading3'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=12,
        textColor=colors.HexColor("#2D3748"),
        spaceBefore=5,
        spaceAfter=2,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['BodyText'],
        fontName='Helvetica',
        fontSize=8.2,
        leading=11.2,
        textColor=colors.HexColor("#2D3748"),
        spaceAfter=3
    )

    bullet_style = ParagraphStyle(
        'BulletDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#2D3748"),
        leftIndent=10,
        spaceAfter=1.5
    )

    speech_style = ParagraphStyle(
        'SpeechBox',
        parent=styles['Normal'],
        fontName='Helvetica-Oblique',
        fontSize=8,
        leading=11.2,
        textColor=colors.HexColor("#1A365D")
    )

    table_th = ParagraphStyle('TH', fontName='Helvetica-Bold', fontSize=7.8, leading=10, textColor=colors.HexColor("#1A365D"))
    table_td = ParagraphStyle('TD', fontName='Helvetica', fontSize=7.2, leading=9.5, textColor=colors.HexColor("#2D3748"))

    story = []

    # ================= PAGE 1 =================
    story.append(Paragraph("Partie Individuelle : Identity & Access Service (IAM)", title_style))
    story.append(Paragraph("<b>Membre 1</b> — Responsable Authentification, Gestion des Utilisateurs & Autorisations", subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1.2, color=colors.HexColor("#2B6CB0"), spaceAfter=5))

    # Bloc Speech
    speech_text = (
        "<b>Speech de Présentation (1 minute chrono) :</b><br/>"
        "« <i>Bonjour, je suis responsable du microservice <b>Identity & Access Service</b>, garant de la sécurité et des accès d'OmniShop. "
        "Notre mission couvre l'inscription/connexion locale et fédérée via <b>OAuth2/OpenID Connect</b> (Google, GitHub), la gestion des profils, et un cloisonnement strict par <b>RBAC</b> "
        "entre acheteurs débutants et marchands professionnels. "
        "Nous combinons des <b>JWT asymétriques RS256</b> (stateless pour l'API Gateway via <b>JWKS</b>) et des <b>Refresh Tokens sous Redis</b> pour une révocation instantanée. "
        "Enfin, nous émettons des événements asynchrones sur <b>RabbitMQ</b> comme <code>UserRegisteredEvent</code> pour déclencher sans couplage la création de boutique côté marchand.</i> »"
    )
    speech_table = Table([[Paragraph(speech_text, speech_style)]], colWidths=[17.4 * cm])
    speech_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 0.8, colors.HexColor("#BEE3F8")),
        ('TOPPADDING', (0, 0), (-1, -1), 4),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 4),
        ('LEFTPADDING', (0, 0), (-1, -1), 6),
        ('RIGHTPADDING', (0, 0), (-1, -1), 6),
    ]))
    story.append(speech_table)
    story.append(Spacer(1, 4))

    # Section 1 : Conception - Diagramme de classes
    story.append(Paragraph("1. Conception du Microservice (Diagramme de Classes UML)", h1_style))
    story.append(Paragraph(
        "Modélisation du modèle relationnel et sécuritaire du microservice sous PostgreSQL (intégrité ACID) et Redis (cache & sessions) :",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(create_image_box(class_img, 17.4 * cm, 10.5 * cm))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Détail des Entités & Responsabilités Métier :</b>", h2_style))
    story.append(Paragraph("• <b>User :</b> Racine d'agrégat (UUID, email unique vérifié, hachage de mot de passe Argon2/BCrypt, statut de compte).", bullet_style))
    story.append(Paragraph("• <b>Role & Permission (RBAC) :</b> Cloisonnement granulaire (<code>ROLE_CLIENT</code>, <code>ROLE_MERCHANT</code>, <code>ROLE_ADMIN</code>). Un client accède uniquement à ses commandes ; un marchand administre son catalogue et ses tarifs B2B.", bullet_style))
    story.append(Paragraph("• <b>OAuthAccount :</b> Liaison de comptes externes (fournisseur Google/GitHub, identifiant distant, synchro de profil).", bullet_style))
    story.append(Paragraph("• <b>RefreshToken :</b> Jeton persistant chiffré stocké sous Redis avec TTL (7j) et détection de rejeu / vol de session.", bullet_style))

    story.append(PageBreak())

    # ================= PAGE 2 =================
    # Section 2 : Interactions
    story.append(Paragraph("2. Interactions avec les Autres Microservices", h1_style))
    story.append(Paragraph(
        "Ce diagramme de séquence illustre la coexistence de communications <b>synchrones</b> (OAuth2, JWKS) "
        "et <b>asynchrones</b> (Message Broker) :",
        body_style
    ))
    story.append(Spacer(1, 2))

    story.append(create_image_box(seq_img, 17.4 * cm, 9.5 * cm))
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Exemples de Communications :</b>", h2_style))
    story.append(Paragraph(
        "• <b>Communication Synchrone (API Gateway & JWKS) :</b> L'API Gateway interroge au démarrage <code>GET /.well-known/jwks.json</code> pour mettre en cache la clé publique RSA. Elle vérifie ainsi la signature des requêtes entrantes de façon 100% autonome et <i>stateless</i> sans surcharger le microservice d'authentification.",
        body_style
    ))
    story.append(Paragraph(
        "• <b>Communication Asynchrone (RabbitMQ) :</b> Lors d'une inscription, <code>auth-user-service</code> publie l'événement <code>UserRegisteredEvent</code>. Le <code>notification-service</code> consomme l'événement pour expédier le courriel de confirmation, et le <code>store-service</code> instancie automatiquement l'espace marchand brouillon.",
        body_style
    ))
    story.append(Spacer(1, 3))

    # Section 3 : Contrats d'API
    story.append(Paragraph("3. Contrats d'API & Spécifications des Endpoints", h1_style))

    api_data = [
        [
            Paragraph("<b>Méthode & URI</b>", table_th),
            Paragraph("<b>Description Métier</b>", table_th),
            Paragraph("<b>Payload / Paramètres</b>", table_th),
            Paragraph("<b>Codes de Réponse</b>", table_th),
            Paragraph("<b>Événement Broker</b>", table_th)
        ],
        [
            Paragraph("<code>POST /api/v1/auth/register</code>", table_td),
            Paragraph("Inscription nouvel utilisateur", table_td),
            Paragraph("<code>email, password, role, firstName, lastName</code>", table_td),
            Paragraph("<b>201</b> Created<br/><b>400</b> Bad Request<br/><b>409</b> Conflict (Email pris)", table_td),
            Paragraph("<code>UserRegisteredEvent</code>", table_td)
        ],
        [
            Paragraph("<code>POST /api/v1/auth/login</code>", table_td),
            Paragraph("Authentification locale", table_td),
            Paragraph("<code>email, password</code>", table_td),
            Paragraph("<b>200</b> OK (Access+Refresh Tokens)<br/><b>401</b> Unauthorized<br/><b>403</b> Compte suspendu", table_td),
            Paragraph("<code>UserLoggedInEvent</code>", table_td)
        ],
        [
            Paragraph("<code>POST /api/v1/auth/refresh</code>", table_td),
            Paragraph("Renouvellement token expiré", table_td),
            Paragraph("<code>refreshToken</code>", table_td),
            Paragraph("<b>200</b> OK (Nouveau couple JWT)<br/><b>401</b> Unauthorized (Jeton révoqué)", table_td),
            Paragraph("—", table_td)
        ],
        [
            Paragraph("<code>GET /api/v1/auth/oauth2/authorize/{p}</code>", table_td),
            Paragraph("Lancement flux OAuth2 (Google/GitHub)", table_td),
            Paragraph("<code>provider = google | github</code>", table_td),
            Paragraph("<b>302</b> Found (Redirection vers mire de login tierce)", table_td),
            Paragraph("—", table_td)
        ],
        [
            Paragraph("<code>GET /api/v1/auth/oauth2/callback/{p}</code>", table_td),
            Paragraph("Callback OAuth2 et échange token", table_td),
            Paragraph("<code>code, state</code>", table_td),
            Paragraph("<b>200</b> OK (Tokens émis)<br/><b>400</b> Code invalide", table_td),
            Paragraph("<code>UserRegisteredEvent</code> (si 1ère fois)", table_td)
        ],
        [
            Paragraph("<code>POST /api/v1/auth/logout</code>", table_td),
            Paragraph("Déconnexion & révocation", table_td),
            Paragraph("<code>refreshToken</code> (Bearer JWT)", table_td),
            Paragraph("<b>204</b> No Content<br/><b>401</b> Non authentifié", table_td),
            Paragraph("—", table_td)
        ],
        [
            Paragraph("<code>GET /.well-known/jwks.json</code>", table_td),
            Paragraph("Diffusion clés publiques RSA", table_td),
            Paragraph("Aucun (Public)", table_td),
            Paragraph("<b>200</b> OK (JSON Web Key Set)", table_td),
            Paragraph("—", table_td)
        ]
    ]

    api_table = Table(api_data, colWidths=[4.1 * cm, 3.4 * cm, 3.5 * cm, 3.7 * cm, 2.7 * cm])
    api_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#EBF8FF")),
        ('BOX', (0, 0), (-1, -1), 0.5, colors.HexColor("#CBD5E0")),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, colors.HexColor("#E2E8F0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('TOPPADDING', (0, 0), (-1, -1), 3),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 3),
        ('LEFTPADDING', (0, 0), (-1, -1), 4),
        ('RIGHTPADDING', (0, 0), (-1, -1), 4),
    ]))
    story.append(api_table)

    # Build
    doc.build(story, canvasmaker=NumberedCanvas)
    print("PDF generated at:", output_pdf)

if __name__ == "__main__":
    generate_pdf()
