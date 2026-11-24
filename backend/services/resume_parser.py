
import io
import pdfplumber
from docx import Document


def extract_text_from_pdf(file_content: bytes) -> str:
    text = ""

    with pdfplumber.open(io.BytesIO(file_content)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

    return text.strip()


def extract_text_from_docx(file_content: bytes) -> str:
    document = Document(io.BytesIO(file_content))

    extracted_parts = []

    # Extract normal paragraphs
    for paragraph in document.paragraphs:
        if paragraph.text.strip():
            extracted_parts.append(paragraph.text.strip())

    # Extract information stored inside tables
    for table in document.tables:
        for row in table.rows:
            row_data = []

            for cell in row.cells:
                cell_text = cell.text.strip()

                if cell_text:
                    row_data.append(cell_text)

            if row_data:
                extracted_parts.append(" | ".join(row_data))

    return "\n".join(extracted_parts).strip()


def extract_resume_text(filename: str, file_content: bytes) -> str:
    extension = "." + filename.rsplit(".", 1)[-1].lower()

    if extension == ".pdf":
        text = extract_text_from_pdf(file_content)

    elif extension == ".docx":
        text = extract_text_from_docx(file_content)

    else:
        raise ValueError("Unsupported resume format")

    # Normalize extracted bullet characters
    text = text.replace("(cid:127)", "•")
    text = text.replace("(cid:149)", "•")

    return text.strip()
