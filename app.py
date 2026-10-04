
import streamlit as st
from datetime import date, datetime
import calendar
import requests
import os

from dotenv import load_dotenv
from google import genai

from database import get_connection
from tithi import get_tithi
import lunar_month


# ============================================================
# 🤖 GEMINI AI CULTURAL ASSISTANT
# ============================================================

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    try:
        GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
    except Exception:
        GEMINI_API_KEY = None

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
gemini_client = None

if GEMINI_API_KEY:
    try:
        gemini_client = genai.Client(api_key=GEMINI_API_KEY)
    except Exception:
        gemini_client = None

def ask_cultural_ai(question, selected_date, festival_name=None):
    if not gemini_client:
        return ("⚠️ Gemini API key is not configured. Add GEMINI_API_KEY "
                "to your .env file or Streamlit Cloud Secrets.")

    festival_context = festival_name or "No specific festival"
    prompt = f"""You are an AI Cultural Assistant for a Maharashtra Cultural Calendar.
Answer the user's question simply and accurately. Focus on Maharashtra culture, Marathi festivals and traditions, Indian cultural/historical context, customs, celebrations and traditional practices.
Selected date: {selected_date.strftime("%d %B %Y")}
Selected festival: {festival_context}
User question: {question}
Use simple language. If unrelated to culture, politely say you are mainly for cultural questions. Do not invent dates or historical facts."""

    try:
        response = gemini_client.models.generate_content(model=GEMINI_MODEL, contents=prompt)
        answer = getattr(response, "text", None)
        return answer.strip() if answer else "⚠️ Gemini did not return an answer."
    except Exception as e:
        return f"⚠️ AI Assistant error: {e}"


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Maharashtra Cultural Calendar",
    page_icon="🌺",
    layout="wide"
)


# ============================================================
# SANKASHTI CHATURTHI DATES
# 2026 - 2030
# ============================================================

SANKASHTI_DATES = {

    # 2026
    date(2026, 1, 6),
    date(2026, 2, 5),
    date(2026, 3, 6),
    date(2026, 4, 5),
    date(2026, 5, 5),
    date(2026, 6, 3),
    date(2026, 7, 3),
    date(2026, 8, 2),
    date(2026, 8, 31),
    date(2026, 9, 29),
    date(2026, 10, 29),
    date(2026, 11, 27),
    date(2026, 12, 26),

    # 2027
    date(2027, 1, 25),
    date(2027, 2, 24),
    date(2027, 3, 25),
    date(2027, 4, 24),
    date(2027, 5, 23),
    date(2027, 6, 22),
    date(2027, 7, 22),
    date(2027, 8, 20),
    date(2027, 9, 19),
    date(2027, 10, 18),
    date(2027, 11, 17),
    date(2027, 12, 16),

    # 2028
    date(2028, 1, 14),
    date(2028, 2, 13),
    date(2028, 3, 13),
    date(2028, 4, 12),
    date(2028, 5, 11),
    date(2028, 6, 10),
    date(2028, 7, 10),
    date(2028, 8, 8),
    date(2028, 9, 7),
    date(2028, 10, 7),
    date(2028, 11, 5),
    date(2028, 12, 5),

    # 2029
    date(2029, 1, 3),
    date(2029, 2, 2),
    date(2029, 3, 3),
    date(2029, 4, 1),
    date(2029, 5, 1),
    date(2029, 5, 30),
    date(2029, 6, 29),
    date(2029, 7, 28),
    date(2029, 8, 27),
    date(2029, 9, 26),
    date(2029, 10, 26),
    date(2029, 11, 24),
    date(2029, 12, 24),

    # 2030
    date(2030, 1, 22),
    date(2030, 2, 21),
    date(2030, 3, 22),
    date(2030, 4, 20),
    date(2030, 5, 20),
    date(2030, 6, 18),
    date(2030, 7, 18),
    date(2030, 8, 16),
    date(2030, 9, 15),
    date(2030, 10, 15),
    date(2030, 11, 13),
    date(2030, 12, 13),
}


def is_sankashti_chaturthi(selected_date):
    return selected_date in SANKASHTI_DATES


# ============================================================
# EKADASHI DATES
# 2026 - 2030
# ============================================================

EKADASHI_DATES = {

    # 2026
    date(2026, 1, 14),
    date(2026, 1, 29),
    date(2026, 2, 13),
    date(2026, 2, 27),
    date(2026, 3, 15),
    date(2026, 3, 29),
    date(2026, 4, 13),
    date(2026, 4, 27),
    date(2026, 5, 13),
    date(2026, 5, 27),
    date(2026, 6, 11),
    date(2026, 6, 25),
    date(2026, 7, 11),
    date(2026, 7, 25),
    date(2026, 8, 9),
    date(2026, 8, 24),
    date(2026, 9, 7),
    date(2026, 9, 22),
    date(2026, 10, 6),
    date(2026, 10, 22),
    date(2026, 11, 5),
    date(2026, 11, 21),
    date(2026, 12, 4),
    date(2026, 12, 20),

    # 2027
    date(2027, 1, 3),
    date(2027, 1, 18),
    date(2027, 2, 2),
    date(2027, 2, 17),
    date(2027, 3, 4),
    date(2027, 3, 18),
    date(2027, 4, 2),
    date(2027, 4, 17),
    date(2027, 5, 2),
    date(2027, 5, 16),
    date(2027, 6, 1),
    date(2027, 6, 14),
    date(2027, 6, 30),
    date(2027, 7, 14),
    date(2027, 7, 29),
    date(2027, 8, 12),
    date(2027, 8, 28),
    date(2027, 9, 11),
    date(2027, 9, 26),
    date(2027, 10, 11),
    date(2027, 10, 25),
    date(2027, 11, 10),
    date(2027, 11, 24),
    date(2027, 12, 9),
    date(2027, 12, 23),

    # 2028
    date(2028, 1, 8),
    date(2028, 1, 22),
    date(2028, 2, 6),
    date(2028, 2, 20),
    date(2028, 3, 7),
    date(2028, 3, 21),
    date(2028, 4, 5),
    date(2028, 4, 20),
    date(2028, 5, 5),
    date(2028, 5, 20),
    date(2028, 6, 3),
    date(2028, 6, 18),
    date(2028, 7, 2),
    date(2028, 7, 18),
    date(2028, 8, 1),
    date(2028, 8, 16),
    date(2028, 8, 30),
    date(2028, 9, 15),
    date(2028, 9, 29),
    date(2028, 10, 14),
    date(2028, 10, 28),
    date(2028, 11, 12),
    date(2028, 11, 27),
    date(2028, 12, 12),
    date(2028, 12, 27),

    # 2029
    date(2029, 1, 10),
    date(2029, 1, 26),
    date(2029, 2, 9),
    date(2029, 2, 25),
    date(2029, 3, 10),
    date(2029, 3, 26),
    date(2029, 4, 9),
    date(2029, 4, 24),
    date(2029, 5, 9),
    date(2029, 5, 24),
    date(2029, 6, 7),
    date(2029, 6, 22),
    date(2029, 7, 7),
    date(2029, 7, 21),
    date(2029, 8, 6),
    date(2029, 8, 20),
    date(2029, 9, 4),
    date(2029, 9, 18),
    date(2029, 10, 4),
    date(2029, 10, 18),
    date(2029, 11, 2),
    date(2029, 11, 16),
    date(2029, 12, 1),
    date(2029, 12, 16),
    date(2029, 12, 31),

    # 2030
    date(2030, 1, 14),
    date(2030, 1, 29),
    date(2030, 2, 13),
    date(2030, 2, 27),
    date(2030, 3, 15),
    date(2030, 3, 29),
    date(2030, 4, 14),
    date(2030, 4, 27),
    date(2030, 5, 13),
    date(2030, 5, 27),
    date(2030, 6, 11),
    date(2030, 6, 26),
    date(2030, 7, 11),
    date(2030, 7, 25),
    date(2030, 8, 9),
    date(2030, 8, 24),
    date(2030, 9, 7),
    date(2030, 9, 23),
    date(2030, 10, 6),
    date(2030, 10, 22),
    date(2030, 11, 5),
    date(2030, 11, 21),
    date(2030, 12, 5),
    date(2030, 12, 21),
}


def is_ekadashi(selected_date):
    return selected_date in EKADASHI_DATES


# ============================================================
# FESTIVAL IMAGES
# ============================================================

festival_images = {

    "Makar Sankranti": "images/makar_sankranti.jpeg",
    "Republic Day": "images/republic_day.jpeg",
    "Maha Shivratri": "images/maha_shivratri.jpeg",
    "Chhatrapati Shivaji Maharaj Jayanti":
        "images/shivaji_maharaj.jpeg",
    "Holi": "images/holi.jpeg",
    "Gudi Padwa": "images/gudi_padwa.jpeg",
    "Ram Navami": "images/ram_navami.jpeg",
    "Hanuman Jayanti": "images/hanuman_jayanti.jpeg",
    "Dr. Babasaheb Ambedkar Jayanti":
        "images/ambedkar_jayanti.jpeg",
    "Akshaya Tritiya": "images/akshay_tritiya.jpeg",
    "Maharashtra Day": "images/maharashtra_day.jpeg",
    "Vat Purnima": "images/vat_purnima.jpeg",
    "Ashadhi Ekadashi": "images/ashadhi_ekadashi.jpeg",
    "Guru Purnima": "images/guru_purnima.jpeg",
    "Independence Day": "images/independence_day.jpeg",
    "Nag Panchami": "images/nag_panchami.jpeg",
    "Janmashtami": "images/janmasthami.jpeg",
    "Raksha Bandhan": "images/raksha_bandhan.jpeg",
    "Teachers Day": "images/teachers_day.jpeg",
    "Ganesh Chaturthi": "images/ganesh_chaturthi.jpeg",
    "Anant Chaturdashi": "images/anant_chaturdashi.jpeg",
    "Mahatma Gandhi Jayanti": "images/gandhi_jayanti.jpeg",
    "Navratri Begins": "images/navratri.jpeg",
    "Dussehra": "images/dussehra.jpeg",
    "Diwali": "images/diwali.jpeg",
    "Bhau Beej": "images/bhau_beej.jpeg",
    "Guru Nanak Jayanti": "images/guru_nanak_jayanti.jpeg",
    "Christmas": "images/christmas.jpeg",
    "Magha Gupta Navratri": "images/navratri.jpeg",
}


# ============================================================
# FESTIVAL EMOJIS
# ============================================================

festival_emojis = {

    "Makar Sankranti": "🪁",
    "Republic Day": "🇮🇳",
    "Maha Shivratri": "🔱",
    "Chhatrapati Shivaji Maharaj Jayanti": "⚔️",
    "Holi": "🎨",
    "Gudi Padwa": "🚩",
    "Ram Navami": "🏹",
    "Hanuman Jayanti": "🐒",
    "Dr. Babasaheb Ambedkar Jayanti": "📚",
    "Akshaya Tritiya": "🌾",
    "Maharashtra Day": "🚩",
    "Vat Purnima": "🌿",
    "Ashadhi Ekadashi": "🪷",
    "Guru Purnima": "🙏",
    "Independence Day": "🇮🇳",
    "Nag Panchami": "🐍",
    "Janmashtami": "🦚",
    "Raksha Bandhan": "🎀",
    "Teachers Day": "📚",
    "Ganesh Chaturthi": "🐘",
    "Anant Chaturdashi": "🙏",
    "Mahatma Gandhi Jayanti": "🕊️",
    "Navratri Begins": "🌺",
    "Dussehra": "🏹",
    "Diwali": "🪔",
    "Bhau Beej": "👫",
    "Guru Nanak Jayanti": "🪯",
    "Christmas": "🎄",
    "Magha Gupta Navratri": "🌺",
}


# ============================================================
# MARATHI TRANSLATIONS
# ============================================================

paksha_marathi = {
    "Shukla": "शुक्ल",
    "Krishna": "वद्य"
}


tithi_marathi = {

    "Pratipada": "प्रतिपदा",
    "Dvitiya": "द्वितीया",
    "Tritiya": "तृतीया",
    "Chaturthi": "चतुर्थी",
    "Panchami": "पंचमी",
    "Shashthi": "षष्ठी",
    "Saptami": "सप्तमी",
    "Ashtami": "अष्टमी",
    "Navami": "नवमी",
    "Dashami": "दशमी",
    "Ekadashi": "एकादशी",
    "Dvadashi": "द्वादशी",
    "Trayodashi": "त्रयोदशी",
    "Chaturdashi": "चतुर्दशी",
    "Purnima": "पौर्णिमा",
    "Amavasya": "अमावस्या"
}


nakshatra_marathi = {

    "Ashwini": "अश्विनी",
    "Bharani": "भरणी",
    "Krittika": "कृत्तिका",
    "Rohini": "रोहिणी",
    "Mrigashira": "मृगशीर्ष",
    "Ardra": "आर्द्रा",
    "Punarvasu": "पुनर्वसू",
    "Pushya": "पुष्य",
    "Ashlesha": "आश्लेषा",
    "Magha": "मघा",
    "Purva Phalguni": "पूर्वा फाल्गुनी",
    "Uttara Phalguni": "उत्तरा फाल्गुनी",
    "Hasta": "हस्त",
    "Chitra": "चित्रा",
    "Swati": "स्वाती",
    "Vishakha": "विशाखा",
    "Anuradha": "अनुराधा",
    "Jyeshtha": "ज्येष्ठा",
    "Mula": "मूळ",
    "Purva Ashadha": "पूर्वाषाढा",
    "Uttara Ashadha": "उत्तराषाढा",
    "Shravana": "श्रवण",
    "Dhanishtha": "धनिष्ठा",
    "Shatabhisha": "शततारका",
    "Purva Bhadrapada": "पूर्वाभाद्रपदा",
    "Uttara Bhadrapada": "उत्तराभाद्रपदा",
    "Revati": "रेवती"
}


weekday_marathi = {

    "Sunday": "रविवार",
    "Monday": "सोमवार",
    "Tuesday": "मंगळवार",
    "Wednesday": "बुधवार",
    "Thursday": "गुरुवार",
    "Friday": "शुक्रवार",
    "Saturday": "शनिवार"
}


yoga_marathi = {

    "Vishkambha": "विष्कंभ",
    "Priti": "प्रीती",
    "Ayushman": "आयुष्मान",
    "Saubhagya": "सौभाग्य",
    "Shobhana": "शोभन",
    "Atiganda": "अतिगंड",
    "Sukarma": "सुकर्मा",
    "Dhriti": "धृती",
    "Shula": "शूल",
    "Ganda": "गंड",
    "Vriddhi": "वृद्धी",
    "Dhruva": "ध्रुव",
    "Vyaghata": "व्याघात",
    "Harshana": "हर्षण",
    "Vajra": "वज्र",
    "Siddhi": "सिद्धी",
    "Vyatipata": "व्यतीपात",
    "Variyana": "वरीयान",
    "Parigha": "परिघ",
    "Shiva": "शिव",
    "Siddha": "सिद्ध",
    "Sadhya": "साध्य",
    "Shubha": "शुभ",
    "Shukla": "शुक्ल",
    "Brahma": "ब्रह्म",
    "Indra": "इंद्र",
    "Vaidhriti": "वैधृती"
}


karana_marathi = {

    "Bava": "बव",
    "Balava": "बालव",
    "Kaulava": "कौलव",
    "Taitila": "तैतिल",
    "Garaja": "गरज",
    "Vanija": "वणिज",
    "Vishti": "विष्टी",
    "Shakuni": "शकुनी",
    "Chatushpada": "चतुष्पाद",
    "Naga": "नाग",
    "Kimstughna": "किंस्तुघ्न"
}


# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown(
    """
    <style>

    .main-title {
        text-align: center;
        font-size: 34px;
        font-weight: 800;
        margin-bottom: 5px;
    }

    .calendar-heading {
        text-align: center;
        font-size: 28px;
        font-weight: 800;
        margin: 8px 0 12px 0;
    }

    .weekday-header {
        background: linear-gradient(
            135deg,
            #6a1b9a,
            #9c27b0
        );
        color: white;
        text-align: center;
        font-weight: 800;
        padding: 10px 4px;
        border-radius: 9px;
        margin-bottom: 5px;
    }

    /* Calendar date buttons */

    div[data-testid="stButton"] button {
        min-height: 82px;
        width: 100%;
        border-radius: 12px;
        font-size: 15px;
        font-weight: 700;
        white-space: pre-wrap;
        line-height: 1.35;
        padding: 8px 5px;
    }

    /* Normal dates */

    div[data-testid="stButton"] button[kind="secondary"] {
        background-color: #ffffff;
        color: #222222 !important;
        border: 1px solid #bdbdbd;
    }

    div[data-testid="stButton"] button[kind="secondary"]:hover {
        background-color: #f3e5f5;
        border-color: #7e57c2;
        color: #222222 !important;
    }

    /* Festival / selected dates */

    div[data-testid="stButton"] button[kind="primary"] {
        background: linear-gradient(
            135deg,
            #ff8f00,
            #ffb300
        );
        color: #111111 !important;
        border: 2px solid #ef6c00;
    }

    div[data-testid="stButton"] button[kind="primary"]:hover {
        background: linear-gradient(
            135deg,
            #ffb300,
            #ffc107
        );
        color: #111111 !important;
    }

    .legend-container {
        display: flex;
        flex-wrap: wrap;
        gap: 8px;
        margin: 12px 0 18px 0;
    }

    .legend {
        padding: 7px 12px;
        border-radius: 20px;
        font-size: 13px;
        font-weight: 700;
    }

    .legend-festival {
        background: #fff3cd;
        color: #7a4a00;
        border: 1px solid #ffb300;
    }

    .legend-ekadashi {
        background: #f3e5f5;
        color: #6a1b9a;
        border: 1px solid #9c27b0;
    }

    .legend-sankashti {
        background: #e8f5e9;
        color: #1b5e20;
        border: 1px solid #43a047;
    }

    .legend-selected {
        background: #e3f2fd;
        color: #0d47a1;
        border: 1px solid #1976d2;
    }

    @media (max-width: 700px) {

        div[data-testid="stButton"] button {
            min-height: 72px;
            font-size: 11px;
            padding: 5px 2px;
        }

        .calendar-heading {
            font-size: 23px;
        }

        .weekday-header {
            font-size: 11px;
            padding: 8px 2px;
        }
    }

    </style>
    """,
    unsafe_allow_html=True
)


# ============================================================
# TITLE
# ============================================================

st.markdown(
    '<div class="main-title">🌺 Maharashtra Cultural Calendar</div>',
    unsafe_allow_html=True
)

st.write(
    "Explore Marathi festivals, traditions, Panchang, "
    "Sankashti Chaturthi, Ekadashi and cultural information."
)


# ============================================================
# CURRENT DATE
# ============================================================

today = date.today()


# ============================================================
# CALENDAR STATE
# ============================================================

if "calendar_year" not in st.session_state:
    st.session_state.calendar_year = today.year

if "calendar_month" not in st.session_state:
    st.session_state.calendar_month = today.month

if "selected_date" not in st.session_state:
    st.session_state.selected_date = today

if "manual_date_picker" not in st.session_state:
    st.session_state.manual_date_picker = today


# ============================================================
# CALENDAR CALLBACK FUNCTIONS
# ============================================================

def previous_month():

    year = st.session_state.calendar_year
    month = st.session_state.calendar_month

    if month == 1:
        year -= 1
        month = 12
    else:
        month -= 1

    new_date = date(year, month, 1)

    st.session_state.calendar_year = year
    st.session_state.calendar_month = month
    st.session_state.selected_date = new_date
    st.session_state.manual_date_picker = new_date


def next_month():

    year = st.session_state.calendar_year
    month = st.session_state.calendar_month

    if month == 12:
        year += 1
        month = 1
    else:
        month += 1

    new_date = date(year, month, 1)

    st.session_state.calendar_year = year
    st.session_state.calendar_month = month
    st.session_state.selected_date = new_date
    st.session_state.manual_date_picker = new_date


def go_to_today():

    st.session_state.calendar_year = today.year
    st.session_state.calendar_month = today.month
    st.session_state.selected_date = today
    st.session_state.manual_date_picker = today


def select_calendar_date(selected):

    st.session_state.selected_date = selected
    st.session_state.calendar_year = selected.year
    st.session_state.calendar_month = selected.month
    st.session_state.manual_date_picker = selected


def manual_date_changed():

    selected = st.session_state.manual_date_picker

    st.session_state.selected_date = selected
    st.session_state.calendar_year = selected.year
    st.session_state.calendar_month = selected.month


# ============================================================
# CURRENT CALENDAR MONTH
# ============================================================

calendar_year = st.session_state.calendar_year
calendar_month = st.session_state.calendar_month


month_names = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
]


# ============================================================
# MONTH NAVIGATION
# ============================================================

st.divider()

previous_col, title_col, next_col = st.columns([1, 2, 1])


with previous_col:

    st.button(
        "⬅️ Previous",
        use_container_width=True,
        key="previous_month",
        on_click=previous_month
    )


with title_col:

    st.markdown(
        f"""
        <div class="calendar-heading">
            🌺 {month_names[calendar_month - 1]} {calendar_year}
        </div>
        """,
        unsafe_allow_html=True
    )


with next_col:

    st.button(
        "Next ➡️",
        use_container_width=True,
        key="next_month",
        on_click=next_month
    )


# ============================================================
# TODAY BUTTON
# ============================================================

today_col1, today_col2, today_col3 = st.columns([1, 1, 1])


with today_col2:

    st.button(
        "📍 Go to Today",
        use_container_width=True,
        key="go_today",
        on_click=go_to_today
    )


# ============================================================
# GET FESTIVALS FOR CURRENT MONTH
# ============================================================

monthly_festivals = {}

try:

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    first_day = date(
        calendar_year,
        calendar_month,
        1
    )

    last_day_number = calendar.monthrange(
        calendar_year,
        calendar_month
    )[1]

    last_day = date(
        calendar_year,
        calendar_month,
        last_day_number
    )

    query = """
    SELECT
        event_date,
        event_name,
        event_name_marathi,
        category,
        description,
        description_marathi,
        image_url
    FROM festivals
    WHERE event_date BETWEEN %s AND %s
    ORDER BY event_date
    """

    cursor.execute(
        query,
        (first_day, last_day)
    )

    records = cursor.fetchall()

    for record in records:

        monthly_festivals[
            record["event_date"]
        ] = record

    cursor.close()
    connection.close()

except Exception as e:

    st.error(
        f"Calendar database error: {e}"
    )


# ============================================================
# LEGEND
# ============================================================

#st.markdown(''
    
 #   <div class="legend-container">

  #      <div class="legend legend-festival">
    #        🎉 Festival
   #     </div>

     #   <div class="legend legend-ekadashi">
       #     🪷 Ekadashi
      #  </div>
#
 #       <div class="legend legend-sankashti">
  #          🐘 Sankashti
   #     </div>

    #    <div class="legend legend-selected">
     #       🔵 Selected Date
      #  </div>
#
 #   </div>
    
  #  unsafe_allow_html=True
#')


# ============================================================
# WEEKDAY HEADER
# ============================================================

weekday_short = [
    "Mon",
    "Tue",
    "Wed",
    "Thu",
    "Fri",
    "Sat",
    "Sun"
]


weekday_columns = st.columns(7)

for index, column in enumerate(weekday_columns):

    with column:

        st.markdown(
            f"""
            <div class="weekday-header">
                {weekday_short[index]}
            </div>
            """,
            unsafe_allow_html=True
        )


# ============================================================
# BUILD CLICKABLE CALENDAR
# ============================================================

month_calendar = calendar.monthcalendar(
    calendar_year,
    calendar_month
)


for week_index, week in enumerate(month_calendar):

    columns = st.columns(7)

    for day_index, day_number in enumerate(week):

        with columns[day_index]:

            # ------------------------------------------------
            # Empty calendar cell
            # ------------------------------------------------

            if day_number == 0:

                st.write("")

                continue


            current_date = date(
                calendar_year,
                calendar_month,
                day_number
            )


            festival = monthly_festivals.get(
                current_date
            )


            festival_exists = festival is not None

            ekadashi_exists = is_ekadashi(
                current_date
            )

            sankashti_exists = is_sankashti_chaturthi(
                current_date
            )

            selected = (
                current_date
                == st.session_state.selected_date
            )

            today_date = (
                current_date == today
            )


            # ------------------------------------------------
            # BUILD BUTTON TEXT
            # ------------------------------------------------

            button_text = f"{day_number}"


            if today_date:

                button_text += "  🔵"


            if festival_exists:

                english_name = festival["event_name"]

                marathi_name = (
                    festival["event_name_marathi"]
                    or english_name
                )

                emoji = festival_emojis.get(
                    english_name,
                    "🎉"
                )

                button_text += (
                    f"\n{emoji} {marathi_name}"
                )


            if ekadashi_exists:

                button_text += (
                    "\n🪷 एकादशी"
                )


            if sankashti_exists:

                button_text += (
                    "\n🐘 संकष्टी"
                )


            # ------------------------------------------------
            # BUTTON TYPE
            # ------------------------------------------------

            if selected or festival_exists:

                button_type = "primary"

            else:

                button_type = "secondary"


            # ------------------------------------------------
            # CLICKABLE DATE BUTTON
            # ------------------------------------------------

            st.button(
                button_text,
                key=(
                    f"calendar_"
                    f"{calendar_year}_"
                    f"{calendar_month}_"
                    f"{day_number}"
                ),
                use_container_width=True,
                type=button_type,
                on_click=select_calendar_date,
                args=(current_date,)
            )


# ============================================================
# SELECTED DATE
# ============================================================

selected_date = st.session_state.selected_date


st.divider()

st.subheader(
    "📖 Selected Date"
)

st.success(
    f"📅 {selected_date.strftime('%d %B %Y')}"
)


# ============================================================
# MANUAL DATE SELECTION
# ============================================================

# Synchronize the date picker with the selected calendar date.

st.session_state.manual_date_picker = selected_date

st.date_input(
    "Or select a date manually:",
    key="manual_date_picker",
    on_change=manual_date_changed
)


# ============================================================
# FESTIVAL INFORMATION
# ============================================================

st.divider()

st.subheader(
    "🎉 Festival Information"
)


try:

    connection = get_connection()

    cursor = connection.cursor(
        dictionary=True
    )

    query = """
    SELECT
        event_name,
        event_name_marathi,
        category,
        description,
        description_marathi,
        image_url
    FROM festivals
    WHERE event_date = %s
    """

    cursor.execute(
        query,
        (selected_date,)
    )

    festival = cursor.fetchone()

    cursor.close()
    connection.close()


    if festival:

        english_name = festival["event_name"]

        marathi_name = (
            festival["event_name_marathi"]
            or english_name
        )

        description_marathi = (
            festival["description_marathi"]
            or festival["description"]
            or "माहिती उपलब्ध नाही."
        )

        emoji = festival_emojis.get(
            english_name,
            "🎉"
        )


        st.success(
            f"{emoji} {marathi_name}"
        )


        st.write(
            f"**English Name:** {english_name}"
        )


        st.write(
            f"**Category:** {festival['category']}"
        )


        st.write(
            f"**About:** {description_marathi}"
        )


        festival_image = festival_images.get(
            english_name
        )


        if festival_image:

            st.image(
                festival_image,
                caption=marathi_name,
                width=500
            )

        else:

            st.info(
                "Festival image not available."
            )


    else:

        st.info(
            "No festival information has been added "
            "for this date."
        )


except Exception as e:

    st.error(
        f"Database connection error: {e}"
    )


# ============================================================
# PANCHANG
# ============================================================

st.divider()

st.subheader(
    "🌙 Marathi Panchang"
)


try:

    panchang = get_tithi(
        selected_date
    )


    # --------------------------------------------------------
    # TITHI
    # --------------------------------------------------------

    tithi = panchang.get(
        "tithi",
        {}
    )

    tithi_name = tithi.get(
        "name",
        "Not available"
    )

    paksha = tithi.get(
        "paksha",
        "Not available"
    )


    # --------------------------------------------------------
    # NAKSHATRA
    # --------------------------------------------------------

    nakshatra = panchang.get(
        "nakshatra",
        {}
    )

    nakshatra_name = nakshatra.get(
        "name",
        "Not available"
    )

    nakshatra_pada = nakshatra.get(
        "pada",
        "Not available"
    )


    # --------------------------------------------------------
    # YOGA
    # --------------------------------------------------------

    yoga = panchang.get(
        "yoga",
        {}
    )

    yoga_name = yoga.get(
        "name",
        "Not available"
    )


    # --------------------------------------------------------
    # KARANA
    # --------------------------------------------------------

    karana = panchang.get(
        "karana",
        {}
    )

    karana_name = karana.get(
        "name",
        "Not available"
    )


    # --------------------------------------------------------
    # WEEKDAY
    # --------------------------------------------------------

    weekday = panchang.get(
        "weekday",
        {}
    )

    weekday_name = weekday.get(
        "name",
        "Not available"
    )


    # --------------------------------------------------------
    # SUN
    # --------------------------------------------------------

    sun_times = panchang.get(
        "sun_times",
        {}
    )

    sunrise = sun_times.get(
        "sunrise",
        "Not available"
    )

    sunset = sun_times.get(
        "sunset",
        "Not available"
    )


    # --------------------------------------------------------
    # MOON
    # --------------------------------------------------------

    moon_times = panchang.get(
        "moon_times",
        {}
    )

    moonrise = moon_times.get(
        "moonrise",
        "Not available"
    )

    moonset = moon_times.get(
        "moonset",
        "Not available"
    )


    # --------------------------------------------------------
    # FORMAT TIMES
    # --------------------------------------------------------

    def format_time(value):

        if not value or value == "Not available":

            return "Not available"

        try:

            return datetime.fromisoformat(
                value
            ).strftime("%I:%M %p")

        except Exception:

            return value


    sunrise = format_time(sunrise)

    sunset = format_time(sunset)

    moonrise = format_time(moonrise)

    moonset = format_time(moonset)


    # --------------------------------------------------------
    # MARATHI TRANSLATIONS
    # --------------------------------------------------------

    paksha_name_marathi = paksha_marathi.get(
        paksha,
        paksha
    )


    tithi_name_marathi = tithi_marathi.get(
        tithi_name,
        tithi_name
    )


    nakshatra_name_marathi = nakshatra_marathi.get(
        nakshatra_name,
        nakshatra_name
    )


    yoga_name_marathi = yoga_marathi.get(
        yoga_name,
        yoga_name
    )


    karana_name_marathi = karana_marathi.get(
        karana_name,
        karana_name
    )


    weekday_name_marathi = weekday_marathi.get(
        weekday_name,
        weekday_name
    )


    # --------------------------------------------------------
    # LUNAR MONTH
    # --------------------------------------------------------

    try:

        lunar_month_name = (
            lunar_month.get_lunar_month(
                selected_date
            )
        )

    except Exception:

        lunar_month_name = (
            "महिना उपलब्ध नाही"
        )


    # --------------------------------------------------------
    # DISPLAY PANCHANG
    # --------------------------------------------------------

    st.write(
        f"**मराठी महिना:** {lunar_month_name}"
    )


    st.success(
        f"📜 **मराठी तिथी:** "
        f"{paksha_name_marathi} "
        f"{tithi_name_marathi}"
    )


    st.write(
        f"**पक्ष:** {paksha} "
        f"({paksha_name_marathi})"
    )


    st.write(
        f"**तिथी:** {tithi_name} "
        f"({tithi_name_marathi})"
    )


    st.write(
        f"**नक्षत्र:** {nakshatra_name} "
        f"({nakshatra_name_marathi})"
    )


    st.write(
        f"**नक्षत्र पाद:** {nakshatra_pada}"
    )


    st.write(
        f"**योग:** {yoga_name} "
        f"({yoga_name_marathi})"
    )


    st.write(
        f"**करण:** {karana_name} "
        f"({karana_name_marathi})"
    )


    st.write(
        f"**वार:** {weekday_name} "
        f"({weekday_name_marathi})"
    )


    st.write(
        f"🌅 **सूर्योदय:** {sunrise}"
    )


    st.write(
        f"🌇 **सूर्यास्त:** {sunset}"
    )


    st.write(
        f"🌙 **चंद्रोदय:** {moonrise}"
    )


    st.write(
        f"🌙 **चंद्रास्त:** {moonset}"
    )


    # --------------------------------------------------------
    # SANKASHTI
    # --------------------------------------------------------

    if is_sankashti_chaturthi(selected_date):

        st.success(
            "🐘 **आज संकष्टी चतुर्थी आहे!**"
        )

        st.write(
            "🙏 भगवान श्री गणेशाची पूजा आणि "
            "संकष्टी चतुर्थी व्रत केले जाते."
        )

    else:

        st.info(
            "आज संकष्टी चतुर्थी नाही."
        )


    # --------------------------------------------------------
    # EKADASHI
    # --------------------------------------------------------

    if is_ekadashi(selected_date):

        st.success(
            "🪷 **आज एकादशी आहे!**"
        )

        st.write(
            "🙏 भगवान श्री विष्णूची पूजा आणि "
            "एकादशी व्रत केले जाते."
        )

    else:

        st.info(
            "आज एकादशी नाही."
        )


except requests.exceptions.HTTPError as e:

    st.error(
        f"❌ Panchang API error: {e}"
    )

except requests.exceptions.RequestException as e:

    st.error(
        f"❌ Unable to connect to Panchang API: {e}"
    )

except Exception as e:

    st.error(
        f"❌ Panchang error: {e}"
    )


# ============================================================
# 🤖 AI CULTURAL ASSISTANT
# ============================================================

st.divider()
st.markdown("### 🤖 AI Cultural Assistant")
st.write("Ask about Maharashtra's festivals, traditions, history and culture.")
st.caption(f"📅 Selected date: {selected_date.strftime('%d %B %Y')}")

ai_question = st.text_area(
    "💬 Ask your cultural question",
    placeholder="Example: Why is Gudi Padwa celebrated in Maharashtra?",
    height=100,
    key="ai_cultural_question"
)

if st.button("🤖 Ask AI", type="primary", use_container_width=True, key="ask_cultural_ai"):
    if not ai_question.strip():
        st.warning("Please enter a question first.")
    else:
        selected_festival_name = None
        try:
            connection = get_connection()
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT event_name FROM festivals WHERE event_date = %s LIMIT 1", (selected_date,))
            selected_festival = cursor.fetchone()
            cursor.close()
            connection.close()
            if selected_festival:
                selected_festival_name = selected_festival["event_name"]
        except Exception:
            pass

        with st.spinner("🤖 thamba jara..."):
            ai_answer = ask_cultural_ai(ai_question, selected_date, selected_festival_name)
        st.markdown("### 💡 AI Answer")
        st.markdown(ai_answer)


# ============================================================
# ABOUT
# ============================================================

st.divider()

st.subheader(
    "ℹ️ About This Calendar"
)

st.write(
    "This application provides Maharashtra-related "
    "festival information, Marathi Panchang details "
    "and cultural information based on the selected date."
)

