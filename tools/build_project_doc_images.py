from pathlib import Path
import textwrap

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
OUT_DIR = ROOT / "docs" / "linkedin_images"
OUT_DIR.mkdir(parents=True, exist_ok=True)

W, H = 1400, 1800
MARGIN = 95
BLUE = (46, 116, 181)
DARK_BLUE = (31, 77, 120)
TEXT = (34, 34, 34)
MUTED = (86, 86, 86)
LIGHT_BLUE = (232, 238, 245)
LIGHT_GRAY = (246, 248, 250)
BORDER = (188, 203, 219)
WHITE = (255, 255, 255)


def font(size, bold=False):
    candidates = [
        "C:/Windows/Fonts/arialbd.ttf" if bold else "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf" if bold else "C:/Windows/Fonts/calibri.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    return ImageFont.load_default()


F_TITLE = font(58, True)
F_SUB = font(30)
F_H1 = font(36, True)
F_BODY = font(27)
F_BODY_BOLD = font(27, True)
F_SMALL = font(22)
F_TABLE = font(23)
F_TABLE_BOLD = font(23, True)


def draw_wrapped(draw, text, x, y, max_width, fnt, fill=TEXT, line_gap=8):
    words = text.split()
    lines = []
    line = ""
    for word in words:
        candidate = word if not line else f"{line} {word}"
        if draw.textbbox((0, 0), candidate, font=fnt)[2] <= max_width:
            line = candidate
        else:
            if line:
                lines.append(line)
            line = word
    if line:
        lines.append(line)

    for line in lines:
        draw.text((x, y), line, font=fnt, fill=fill)
        y += fnt.size + line_gap
    return y


def bullet_list(draw, items, x, y, max_width):
    for item in items:
        draw.ellipse((x, y + 10, x + 10, y + 20), fill=BLUE)
        y = draw_wrapped(draw, item, x + 28, y, max_width - 28, F_BODY)
        y += 8
    return y


def numbered_list(draw, items, x, y, max_width):
    for i, item in enumerate(items, 1):
        draw.text((x, y), f"{i}.", font=F_BODY_BOLD, fill=BLUE)
        y = draw_wrapped(draw, item, x + 45, y, max_width - 45, F_BODY)
        y += 8
    return y


def h1(draw, text, y):
    draw.text((MARGIN, y), text, font=F_H1, fill=BLUE)
    return y + 55


def paragraph(draw, text, y):
    return draw_wrapped(draw, text, MARGIN, y, W - 2 * MARGIN, F_BODY) + 22


def callout(draw, title, body, y):
    x = MARGIN
    width = W - 2 * MARGIN
    temp = Image.new("RGB", (W, H), WHITE)
    temp_draw = ImageDraw.Draw(temp)
    body_lines = []
    line = ""
    for word in body.split():
        cand = word if not line else f"{line} {word}"
        if temp_draw.textbbox((0, 0), cand, font=F_BODY)[2] <= width - 260:
            line = cand
        else:
            body_lines.append(line)
            line = word
    if line:
        body_lines.append(line)
    box_h = max(110, 52 + len(body_lines) * 36)
    draw.rounded_rectangle((x, y, x + width, y + box_h), radius=12, fill=LIGHT_GRAY, outline=BORDER, width=2)
    draw.text((x + 25, y + 24), title, font=F_BODY_BOLD, fill=DARK_BLUE)
    yy = y + 24
    for line in body_lines:
        draw.text((x + 250, yy), line, font=F_BODY, fill=TEXT)
        yy += 36
    return y + box_h + 28


def table(draw, headers, rows, widths, y):
    x = MARGIN
    row_h = 72
    total_w = sum(widths)
    for row_idx, row in enumerate([headers] + rows):
        fill = LIGHT_BLUE if row_idx == 0 else WHITE
        max_lines = 1
        wrapped_cells = []
        for col_idx, value in enumerate(row):
            max_chars = max(12, int(widths[col_idx] / 13))
            wrapped = textwrap.wrap(value, width=max_chars) or [""]
            wrapped_cells.append(wrapped)
            max_lines = max(max_lines, len(wrapped))
        this_h = max(row_h, 38 + max_lines * 31)
        xx = x
        for col_idx, value in enumerate(row):
            draw.rectangle((xx, y, xx + widths[col_idx], y + this_h), fill=fill, outline=BORDER, width=2)
            fnt = F_TABLE_BOLD if row_idx == 0 else F_TABLE
            color = DARK_BLUE if row_idx == 0 else TEXT
            ty = y + 18
            for line in wrapped_cells[col_idx]:
                draw.text((xx + 15, ty), line, font=fnt, fill=color)
                ty += 31
            xx += widths[col_idx]
        y += this_h
    return y + 26


def footer(draw, page):
    draw.line((MARGIN, H - 82, W - MARGIN, H - 82), fill=(220, 226, 232), width=2)
    draw.text((MARGIN, H - 58), "Potato Disease Classification | Built by Vaibhav Nayak", font=F_SMALL, fill=MUTED)
    txt = f"Page {page}"
    tw = draw.textbbox((0, 0), txt, font=F_SMALL)[2]
    draw.text((W - MARGIN - tw, H - 58), txt, font=F_SMALL, fill=MUTED)


def new_page(page):
    img = Image.new("RGB", (W, H), WHITE)
    draw = ImageDraw.Draw(img)
    footer(draw, page)
    return img, draw


def save(img, page):
    path = OUT_DIR / f"potato_disease_project_page_{page}.png"
    img.save(path, quality=95)
    print(path)


def build():
    img, d = new_page(1)
    y = 90
    d.text((MARGIN, y), "Potato Disease Classification", font=F_TITLE, fill=DARK_BLUE)
    y += 78
    y = draw_wrapped(
        d,
        "End-to-end deep learning project: model training, FastAPI backend, React frontend, and free deployment.",
        MARGIN,
        y,
        W - 2 * MARGIN,
        F_SUB,
        fill=MUTED,
    ) + 34
    y = callout(
        d,
        "Live summary",
        "Users upload a potato leaf image and receive a disease prediction with confidence. The model predicts Early Blight, Late Blight, or Healthy.",
        y,
    )
    y = h1(d, "1. Problem Statement", y)
    y = paragraph(
        d,
        "The goal is to identify potato leaf health from an image. A user uploads a leaf photo, and the app classifies it into one of three categories.",
        y,
    )
    y = bullet_list(d, ["Early Blight", "Late Blight", "Healthy"], MARGIN, y, W - 2 * MARGIN) + 18
    y = h1(d, "2. Data Collection and Preprocessing", y)
    y = paragraph(
        d,
        "The model was trained using potato leaf images organized by disease category. Images were resized and converted into arrays for the neural network.",
        y,
    )
    y = table(
        d,
        ["Step", "What happened"],
        [
            ["Collect images", "Used categorized potato leaf images for all three classes."],
            ["Preprocess", "Converted images into arrays and resized them to model input size."],
            ["Prepare labels", "Mapped each image to the correct disease class."],
        ],
        [330, 880],
        y,
    )
    y = h1(d, "3. Model Building", y)
    y = paragraph(
        d,
        "A Keras deep learning model was trained to learn visual leaf patterns. The trained model was saved as saved_models/1/1.keras.",
        y,
    )
    save(img, 1)

    img, d = new_page(2)
    y = 90
    y = h1(d, "4. FastAPI Backend", y)
    y = paragraph(
        d,
        "The backend loads the Keras model, accepts an uploaded image, runs prediction, and returns a JSON response.",
        y,
    )
    y = table(
        d,
        ["Endpoint", "Purpose"],
        [
            ["/", "Health check endpoint confirming that the API is running."],
            ["/prediction", "POST endpoint used by React to upload a leaf image and receive prediction results."],
        ],
        [330, 880],
        y,
    )
    y = callout(d, "API URL", "https://vaibhavnayak-potato-disease-api.hf.space/prediction", y)
    y = h1(d, "5. React Website", y)
    y = paragraph(
        d,
        "The frontend provides a simple image upload interface, sends the selected file to FastAPI, and displays the predicted label and confidence percentage.",
        y,
    )
    y = bullet_list(
        d,
        [
            "Upload or drag a potato leaf image.",
            "React sends the image using REACT_APP_API_URL.",
            "The result appears as label plus confidence.",
        ],
        MARGIN,
        y,
        W - 2 * MARGIN,
    ) + 18
    y = h1(d, "6. Free Deployment", y)
    y = table(
        d,
        ["Part", "Platform", "Why"],
        [
            ["Backend API", "Hugging Face Spaces", "Free ML demo hosting with Docker support."],
            ["Frontend", "Vercel", "Free React hosting with GitHub deploys."],
            ["Model serving", "Docker", "Defines Python, dependencies, and startup command."],
        ],
        [270, 360, 580],
        y,
    )
    save(img, 2)

    img, d = new_page(3)
    y = 90
    y = h1(d, "7. End-to-End Flow", y)
    y = numbered_list(
        d,
        [
            "Train the potato leaf disease classification model in Keras.",
            "Save the trained model as a .keras file.",
            "Build a FastAPI backend and load the saved model.",
            "Create the /prediction endpoint for uploaded leaf images.",
            "Build a React frontend for upload and result display.",
            "Deploy the backend to Hugging Face Spaces using Docker.",
            "Deploy the frontend to Vercel and connect it to the backend URL.",
            "Share the live app link so others can test it from the browser.",
        ],
        MARGIN,
        y,
        W - 2 * MARGIN,
    ) + 22
    y = h1(d, "8. How To Test", y)
    y = paragraph(
        d,
        "I will try attaching a few leaf images with the LinkedIn post. If you do not find them, please navigate to the GitHub repository and feel free to use the sample leaf images from there.",
        y,
    )
    y = callout(
        d,
        "Reader note",
        "This project is for learning and demonstration. Real agricultural decisions should use expert validation and field-level diagnosis.",
        y,
    )
    y = h1(d, "9. Credits", y)
    y = paragraph(
        d,
        "Thanks to Codebasics and Dhaval Patel for the learning resources and project inspiration that helped shape this end-to-end machine learning application.",
        y,
    )
    y = h1(d, "10. Tech Stack", y)
    y = table(
        d,
        ["Layer", "Tools"],
        [
            ["Model", "Python, TensorFlow, Keras"],
            ["Backend", "FastAPI, Uvicorn, Pillow, NumPy"],
            ["Frontend", "React, Axios, Material UI"],
            ["Deployment", "Hugging Face Spaces, Docker, Vercel"],
        ],
        [330, 880],
        y,
    )
    save(img, 3)


if __name__ == "__main__":
    build()
