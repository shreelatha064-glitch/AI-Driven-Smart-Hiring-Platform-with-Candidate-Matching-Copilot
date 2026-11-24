
import re


# -------------------------------------------------
# Common resume section headings
# -------------------------------------------------


SECTION_HEADINGS = {
    "summary": [
        "professional summary",
        "career summary",
        "profile",
        "profile summary",
        "career objective", 
        "objective",
        "about me",
        "personal profile"
    ],

    "education": [
        "education",
        "educational background",
        "academic background",
        "academic qualifications",
        "qualifications",
        "educational qualifications"
    ],

    "skills": [
        "skills",
        "key skills",
        "technical skills",
        "core skills",
        "technical competencies",
        "areas of expertise",
        "technical expertise",
        "technical proficiencies",
        "professional skills"
    ],

    "projects": [
        "projects",
        "academic projects",
        "personal projects",
        "key projects",
        "project experience",
        "project work"
    ],

    "experience": [
        "experience",
        "work experience",
        "professional experience",
        "employment history",
        "work history",
        "internship experience",
        "professional background"
    ],

    "certifications": [
        "certifications",
        "certificates",
        "licenses and certifications",
        "professional certifications",
        "professional qualifications"
    ],

    "activities": [
        "leadership",
        "leadership roles",
        "leadership & activities",
        "extracurricular activities",
        "achievements",
        "interests",
        "hobbies",
        "referees",
        "references"
    ]
}

# -------------------------------------------------
# Clean extracted text
# -------------------------------------------------


def clean_resume_text(text: str) -> str:
    # Replace unusual PDF bullet characters
    text = text.replace("(cid:127)", "•")
    text = text.replace("(cid:149)", "•")
    text = text.replace("\x00", "")

    # Normalize different bullet characters
    text = text.replace("▪", "•")
    text = text.replace("●", "•")
    text = text.replace("◦", "•")

    # Replace Windows-style line endings
    text = text.replace("\r\n", "\n")
    text = text.replace("\r", "\n")

    # Remove excessive blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    return text.strip()


# -------------------------------------------------
# Detect email
# -------------------------------------------------

def extract_email(text: str) -> str | None:

    match = re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return match.group(0) if match else None


# -------------------------------------------------
# Detect candidate name
# -------------------------------------------------


def extract_name(text: str) -> str | None:
    lines = [
        line.strip()
        for line in text.splitlines()
        if line.strip()
    ]

    ignored_words = {
        "resume",
        "curriculum vitae",
        "professional summary",
        "career objective",
        "education",
        "skills",
        "experience",
        "projects",
        "certifications",
        "contact",
        "about me"
    }

    for line in lines[:10]:

        # Skip lines that are section headings
        if line.lower().strip(":") in ignored_words:
            continue

        # Remove email addresses
        cleaned = re.sub(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
            "",
            line
        )

        # Remove phone numbers
        cleaned = re.sub(
            r"\+?\d[\d\s()-]{7,}\d",
            "",
            cleaned
        )

        # Keep only the first part before contact separators
        cleaned = re.split(r"[|•]", cleaned)[0]

        # Remove unwanted characters
        cleaned = re.sub(
            r"[^A-Za-z\s'-]",
            " ",
            cleaned
        )

        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        words = cleaned.split()

        # A typical candidate name contains 2–4 words
        if not 2 <= len(words) <= 4:
            continue

        # Reject lines containing common non-name phrases
        if any(word.lower() in ignored_words for word in words):
            continue

        # Allow normal capitalization, lowercase, or uppercase
        if all(re.fullmatch(r"[A-Za-z]+(?:['-][A-Za-z]+)*", word) for word in words):
            return " ".join(word.capitalize() for word in words)

    return None



# -------------------------------------------------
# Identify section heading
# -------------------------------------------------


def identify_heading(line: str) -> str | None:
    normalized = line.strip().lower()

    normalized = normalized.strip(":")
    normalized = re.sub(r"[^a-z\s&]", "", normalized)
    normalized = re.sub(r"\s+", " ", normalized).strip()

    for section, headings in SECTION_HEADINGS.items():
        for heading in headings:
            if normalized == heading.lower():
                return section

    return None


# -------------------------------------------------
# Extract a particular resume section
# -------------------------------------------------


def extract_section(text: str, section_name: str) -> str:
    lines = text.splitlines()

    collected_lines = []
    collecting = False

    for line in lines:
        stripped_line = line.strip()

        if not stripped_line:
            continue

        # Check whether the line starts with a recognized heading
        heading_found = None
        heading_content = ""

        for section, headings in SECTION_HEADINGS.items():
            for heading in headings:
                pattern = (
                    r"^\s*" + re.escape(heading) +
                    r"\s*:?\s*(.*)$"
                )

                match = re.match(pattern, stripped_line, re.IGNORECASE)

                if match:
                    heading_found = section
                    heading_content = match.group(1).strip()
                    break

            if heading_found:
                break

        # A new section heading has been found
        if heading_found is not None:
            if heading_found == section_name:
                collecting = True

                if heading_content:
                    collected_lines.append(heading_content)
            else:
                if collecting:
                    break

                collecting = False

            continue

        # Collect content belonging to the requested section
        if collecting:
            collected_lines.append(stripped_line)

    return "\n".join(collected_lines).strip()


# -------------------------------------------------
# Extract all candidate information
# -------------------------------------------------


def extract_candidate_information(text: str) -> dict:
    text = clean_resume_text(text)

    candidate_name = extract_name(text)
    candidate_email = extract_email(text)

    summary = extract_section(text, "summary")
    education = extract_section(text, "education")
    skills = extract_section(text, "skills")
    projects = extract_section(text, "projects")
    experience = extract_section(text, "experience")
    certifications = extract_section(text, "certifications")
    activities = extract_section(text, "activities")

    return {
        "full_name": candidate_name,
        "email": candidate_email,
        "summary": summary or None,
        "education": education or None,
        "skills": skills or None,
        "projects": projects or None,
        "experience": experience or None,
        "certifications": certifications or None,
        "activities": activities or None
    }
