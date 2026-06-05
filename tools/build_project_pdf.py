from pathlib import Path

from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.pagesizes import LETTER
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import (
    ListFlowable,
    ListItem,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs"
OUT_DIR.mkdir(exist_ok=True)
PDF_PATH = OUT_DIR / "Potato_Disease_Classification_Project_Documentation.pdf"


BLUE = colors.HexColor("#2E74B5")
DARK_BLUE = colors.HexColor("#1F4D78")
LIGHT_BLUE = colors.HexColor("#E8EEF5")
LIGHT_GRAY = colors.HexColor("#F4F6F9")
BORDER = colors.HexColor("#B7C9DC")
TEXT = colors.HexColor("#222222")
MUTED = colors.HexColor("#555555")


def stylesheet():
    styles = getSampleStyleSheet()
    styles.add(
        ParagraphStyle(
            name="ProjectTitle",
            parent=styles["Title"],
            fontName="Helvetica-Bold",
            fontSize=25,
            leading=30,
            textColor=DARK_BLUE,
            alignment=TA_LEFT,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Subtitle",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=11,
            leading=15,
            textColor=MUTED,
            spaceAfter=14,
        )
    )
    styles.add(
        ParagraphStyle(
            name="H1Custom",
            parent=styles["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=BLUE,
            spaceBefore=16,
            spaceAfter=8,
        )
    )
    styles.add(
        ParagraphStyle(
            name="BodyCustom",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=10.2,
            leading=14,
            textColor=TEXT,
            spaceAfter=6,
        )
    )
    styles.add(
        ParagraphStyle(
            name="Small",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=MUTED,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableText",
            parent=styles["BodyText"],
            fontName="Helvetica",
            fontSize=9,
            leading=12,
            textColor=TEXT,
        )
    )
    styles.add(
        ParagraphStyle(
            name="TableHead",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=9,
            leading=12,
            textColor=DARK_BLUE,
        )
    )
    styles.add(
        ParagraphStyle(
            name="CalloutTitle",
            parent=styles["BodyText"],
            fontName="Helvetica-Bold",
            fontSize=10,
            leading=13,
            textColor=DARK_BLUE,
            spaceAfter=3,
        )
    )
    return styles


def p(text, style):
    return Paragraph(text, style)


def bullets(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles["BodyCustom"]), leftIndent=12) for item in items],
        bulletType="bullet",
        leftIndent=18,
        bulletFontName="Helvetica",
        bulletFontSize=9,
        bulletColor=BLUE,
    )


def steps(items, styles):
    return ListFlowable(
        [ListItem(p(item, styles["BodyCustom"]), leftIndent=14) for item in items],
        bulletType="1",
        leftIndent=18,
        bulletFontName="Helvetica-Bold",
        bulletFontSize=9,
        bulletColor=BLUE,
    )


def data_table(headers, rows, widths, styles):
    data = [[p(h, styles["TableHead"]) for h in headers]]
    for row in rows:
        data.append([p(str(cell), styles["TableText"]) for cell in row])
    table = Table(data, colWidths=widths, hAlign="LEFT", repeatRows=1)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), LIGHT_BLUE),
                ("GRID", (0, 0), (-1, -1), 0.5, BORDER),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 7),
                ("RIGHTPADDING", (0, 0), (-1, -1), 7),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    return table


def callout(title, body, styles):
    table = Table(
        [[p(title, styles["CalloutTitle"]), p(body, styles["BodyCustom"])]],
        colWidths=[1.35 * inch, 5.0 * inch],
        hAlign="LEFT",
    )
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), LIGHT_GRAY),
                ("BOX", (0, 0), (-1, -1), 0.5, colors.HexColor("#D8E2ED")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 7),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    return table


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(MUTED)
    canvas.drawCentredString(
        LETTER[0] / 2,
        0.48 * inch,
        f"Potato Disease Classification | Built by Vaibhav Nayak | Page {doc.page}",
    )
    canvas.restoreState()


def build():
    styles = stylesheet()
    doc = SimpleDocTemplate(
        str(PDF_PATH),
        pagesize=LETTER,
        leftMargin=1 * inch,
        rightMargin=1 * inch,
        topMargin=0.85 * inch,
        bottomMargin=0.85 * inch,
        title="Potato Disease Classification Project Documentation",
        author="Vaibhav Nayak",
    )

    story = [
        p("Potato Disease Classification", styles["ProjectTitle"]),
        p(
            "End-to-end deep learning project: model training, FastAPI backend, React frontend, and free deployment.",
            styles["Subtitle"],
        ),
        callout(
            "Live summary",
            "This app lets a user upload a potato leaf image and returns a disease prediction with confidence. "
            "The model predicts Early Blight, Late Blight, or Healthy.",
            styles,
        ),
        Spacer(1, 10),
        p("1. Problem Statement", styles["H1Custom"]),
        p(
            "The goal of this project is to identify potato leaf health from an image. "
            "A user uploads a leaf photo, and the application classifies it into one of three categories.",
            styles["BodyCustom"],
        ),
        bullets(["Early Blight", "Late Blight", "Healthy"], styles),
        p("2. Data Collection and Preprocessing", styles["H1Custom"]),
        p(
            "The model was trained using potato leaf images organized by disease category. "
            "Images were resized and converted into arrays so they could be used by the neural network.",
            styles["BodyCustom"],
        ),
        data_table(
            ["Step", "What happened"],
            [
                ["Collect images", "Used categorized potato leaf images for Early Blight, Late Blight, and Healthy leaves."],
                ["Preprocess", "Converted images into arrays and resized them to the model input size."],
                ["Prepare labels", "Mapped each image to the correct class name for supervised learning."],
            ],
            [1.55 * inch, 4.8 * inch],
            styles,
        ),
        p("3. Model Building", styles["H1Custom"]),
        p(
            "A Keras deep learning model was trained to learn visual patterns from potato leaf images. "
            "The final model was saved as a .keras file and later loaded by the API for live predictions.",
            styles["BodyCustom"],
        ),
        bullets(
            [
                "Input: potato leaf image",
                "Model file: saved_models/1/1.keras",
                "Output: predicted class and confidence score",
            ],
            styles,
        ),
        p("4. FastAPI Backend", styles["H1Custom"]),
        p(
            "The backend was built with FastAPI. It exposes a REST endpoint that accepts an uploaded image, "
            "loads the Keras model, runs prediction, and returns JSON.",
            styles["BodyCustom"],
        ),
        data_table(
            ["Endpoint", "Purpose"],
            [
                ["/", "Health check endpoint. Returns a message confirming the API is running."],
                ["/prediction", "POST endpoint used by the React frontend to upload a leaf image and receive prediction results."],
            ],
            [1.55 * inch, 4.8 * inch],
            styles,
        ),
        Spacer(1, 6),
        callout(
            "API URL",
            "https://vaibhavnayak-potato-disease-api.hf.space/prediction",
            styles,
        ),
        p("5. React Website", styles["H1Custom"]),
        p(
            "The frontend was built in React. It provides a simple image upload interface, sends the selected image "
            "to the FastAPI endpoint, and displays the predicted label and confidence percentage.",
            styles["BodyCustom"],
        ),
        bullets(
            [
                "User uploads or drags a potato leaf image.",
                "React sends the image to the backend using REACT_APP_API_URL.",
                "The result is shown in a table with label and confidence.",
            ],
            styles,
        ),
        p("6. Free Deployment", styles["H1Custom"]),
        p(
            "The application was deployed using a free, beginner-friendly setup: Hugging Face Spaces for the ML API "
            "and Vercel for the React frontend.",
            styles["BodyCustom"],
        ),
        data_table(
            ["Part", "Platform", "Why it was used"],
            [
                ["Backend API", "Hugging Face Spaces", "Good free option for ML demos and Docker-based FastAPI apps."],
                ["Frontend", "Vercel", "Simple free hosting for React applications with GitHub-based deployment."],
                ["Model serving", "Docker", "Defines Python, dependencies, files, and the API startup command."],
            ],
            [1.25 * inch, 1.65 * inch, 3.45 * inch],
            styles,
        ),
        p("7. End-to-End Flow", styles["H1Custom"]),
        steps(
            [
                "Train the potato leaf disease classification model in Keras.",
                "Save the trained model as a .keras file.",
                "Build a FastAPI backend and load the saved model.",
                "Create a /prediction endpoint that accepts uploaded leaf images.",
                "Build a React frontend for image upload and result display.",
                "Deploy the backend to Hugging Face Spaces using Docker.",
                "Deploy the frontend to Vercel and connect it to the backend API URL.",
                "Share the Vercel app link so others can test it from the browser.",
            ],
            styles,
        ),
        p("8. How To Test", styles["H1Custom"]),
        p(
            "I will try attaching a few leaf images along with the LinkedIn post so you can test the app quickly. "
            "If you do not find sample images attached, please navigate to the GitHub repository and feel free to use "
            "the sample leaf images from there.",
            styles["BodyCustom"],
        ),
        callout(
            "Reader note",
            "This project is for learning and demonstration. Real agricultural decisions should use expert validation "
            "and field-level diagnosis.",
            styles,
        ),
        p("9. Credits", styles["H1Custom"]),
        p(
            "Thanks to Codebasics and Dhaval Patel for the learning resources and project inspiration that helped shape "
            "this end-to-end machine learning application.",
            styles["BodyCustom"],
        ),
        p("10. Tech Stack", styles["H1Custom"]),
        data_table(
            ["Layer", "Tools"],
            [
                ["Model", "Python, TensorFlow, Keras"],
                ["Backend", "FastAPI, Uvicorn, Pillow, NumPy"],
                ["Frontend", "React, Axios, Material UI"],
                ["Deployment", "Hugging Face Spaces, Docker, Vercel"],
            ],
            [1.55 * inch, 4.8 * inch],
            styles,
        ),
    ]

    doc.build(story, onFirstPage=footer, onLaterPages=footer)
    print(PDF_PATH)


if __name__ == "__main__":
    build()
