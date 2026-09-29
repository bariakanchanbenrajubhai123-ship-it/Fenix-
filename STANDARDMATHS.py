# ============================================================
# GSEB STD. 10 STANDARD MATHEMATICS
# DETAILED ASSIGNMENT SOLVER
#
# Install:
# pip install streamlit google-genai pymupdf reportlab pillow
#
# API KEY:
# Set environment variable:
# GEMINI_API_KEY="YOUR_API_KEY"
# ============================================================

import os
import io
import re
import fitz
import streamlit as st

from google import genai

from reportlab.lib.pagesizes import A4
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    PageBreak
)
from reportlab.lib.styles import (
    getSampleStyleSheet,
    ParagraphStyle
)
from reportlab.lib.enums import TA_CENTER
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont


# ============================================================
# 1. APP SETTINGS
# ============================================================

st.set_page_config(
    page_title="GSEB Std 10 Maths Answer Key",
    page_icon="📘",
    layout="wide"
)

st.title("📘 GSEB Std. 10 Standard Mathematics")
st.subheader("Detailed Assignment Solution Generator")


# ============================================================
# 2. GEMINI API
# ============================================================

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    st.error(
        "GEMINI_API_KEY सेट नहीं है। "
        "पहले अपनी Gemini API key को environment variable में सेट करें।"
    )
    st.stop()

client = genai.Client(api_key=API_KEY)

MODEL = "gemini-2.5-flash"


# ============================================================
# 3. PDF TEXT EXTRACTION
# ============================================================

def extract_pdf_text(uploaded_file):

    pdf_bytes = uploaded_file.read()

    doc = fitz.open(
        stream=pdf_bytes,
        filetype="pdf"
    )

    all_text = []

    for page_number, page in enumerate(doc, start=1):

        text = page.get_text("text")

        if text.strip():

            all_text.append(
                f"""
========================
PAGE {page_number}
========================

{text}
"""
            )

    return "\n".join(all_text)


# ============================================================
# 4. CLEAN TEXT
# ============================================================

def clean_text(text):

    text = text.replace("\x00", "")

    text = re.sub(
        r"\n{4,}",
        "\n\n",
        text
    )

    return text.strip()


# ============================================================
# 5. DETAILED GSEB MATHS PROMPT
# ============================================================

def create_prompt(pdf_text):

    return f"""

તમે Gujarat Secondary and Higher Secondary Education Board
(GSEB) ના ધોરણ 10 Standard Mathematics ના અનુભવી શિક્ષક છો.

નીચે આપેલી assignment PDF માંના બધા પ્રશ્નોના
DETAILED SOLUTIONS બનાવવાના છે.

===========================================================
IMPORTANT
===========================================================

ધોરણ:
10

વિષય:
Standard Mathematics

બોર્ડ:
Gujarat Board / GSEB

===========================================================
MAIN RULES
===========================================================

1. PDF માં આવેલો એકપણ પ્રશ્ન છોડવો નહીં.

2. દરેક પ્રશ્નનો નંબર જાળવો.

3. પ્રશ્નનો અર્થ બદલવો નહીં.

4. જો પ્રશ્ન સ્પષ્ટ રીતે વાંચી શકાય નહીં તો
   ઉપલબ્ધ માહિતીના આધારે સૌથી યોગ્ય interpretation કરો.

5. દરેક જવાબ school notebook માં લખી શકાય
   તે રીતે તૈયાર કરો.

6. માત્ર final answer આપવો નહીં.

7. દરેક calculation બતાવો.

8. જ્યાં theorem જરૂરી હોય ત્યાં theorem નું નામ લખો.

9. જ્યાં formula જરૂરી હોય ત્યાં પહેલા formula લખો.

10. જ્યાં proof હોય ત્યાં proper mathematical steps આપો.

===========================================================
MATHEMATICS ANSWER FORMAT
===========================================================

દરેક પ્રશ્ન માટે શક્ય હોય ત્યાં નીચેનું format રાખો:

પ્રશ્ન નંબર:

પ્રશ્ન:
[Question]

આપેલ:
[Given]

શોધવાનું છે:
[To find / Prove]

સૂત્ર / પ્રમેય:
[Formula / Theorem]

ઉકેલ:
[Step-by-step solution]

ગણતરી:
[All important calculations]

અંતિમ જવાબ:
[Final Answer]

===========================================================
FOR THEOREM / PROOF QUESTIONS
===========================================================

જો પ્રશ્નમાં સાબિત કરવાનું હોય તો:

આપેલ:

સાબિત કરવાનું છે:

રચના:

સાબિતી:

Step 1:
...

Step 2:
...

Step 3:
...

અંતે:
અતઃ સાબિત થયું કે ...

===========================================================
FOR TRIANGLE / GEOMETRY QUESTIONS
===========================================================

- Given
- To prove
- Construction, જો જરૂરી હોય
- Theorem
- Mathematical reasoning
- Step-by-step proof
- Conclusion

જો પ્રશ્નમાં કોઈ ચોક્કસ relation આપવામાં આવી હોય,
તો તેને solution માં સ્પષ્ટ રીતે ઉપયોગ કરો.

ઉદાહરણ:

AP/BP = AQ/CQ

આ relation ને માત્ર final answer માં નહીં,
પરંતુ solution ના યોગ્ય step માં ઉપયોગ કરો.

===========================================================
FOR
