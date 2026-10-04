import os
import requests
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("NAVAMSHA_API_KEY")


# ----------------------------------------------
# API URLs
# ----------------------------------------------

PANCHANG_URL = "https://api.navamsha.in/api/v1/panchang/full"
SUN_TIMES_URL = "https://api.navamsha.in/api/v1/panchang/sun-times"
MOON_TIMES_URL = "https://api.navamsha.in/api/v1/panchang/moon-times"


# ----------------------------------------------
# Pune, Maharashtra
# ----------------------------------------------

LATITUDE = 18.5204
LONGITUDE = 73.8567
TIMEZONE = 5.5


# ==============================================
# GET COMPLETE PANCHANG
# ==============================================

#@st.cache_data(ttl=3600)
@st.cache_data(ttl=3600, show_spinner=False)
def get_tithi(selected_date):

    # ----------------------------------------------
    # CHECK API KEY
    # ----------------------------------------------

    if not API_KEY:
        raise ValueError(
            "NAVAMSHA_API_KEY not found in .env file."
        )

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "year": selected_date.year,
        "month": selected_date.month,
        "date": selected_date.day,
        "hours": 7,
        "minutes": 0,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE
    }


    # ==============================================
    # 1. PANCHANG
    # ==============================================

    response = requests.post(
        PANCHANG_URL,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    panchang_data = response.json()

    output = panchang_data["output"]


    # ==============================================
    # 2. SUNRISE / SUNSET
    # ==============================================

    try:

        response = requests.post(
            SUN_TIMES_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        sun_data = response.json()["output"]

        output["sun_times"] = {
            "sunrise": sun_data["rise"]["local_datetime"],
            "sunset": sun_data["set"]["local_datetime"]
        }

    except Exception as e:

        print("Sun times error:", e)

        output["sun_times"] = {
            "sunrise": "Not available",
            "sunset": "Not available"
        }


    # ==============================================
    # 3. MOONRISE / MOONSET
    # ==============================================

    try:

        response = requests.post(
            MOON_TIMES_URL,
            headers=headers,
            json=payload,
            timeout=20
        )

        response.raise_for_status()

        moon_data = response.json()["output"]

        output["moon_times"] = {
            "moonrise": moon_data["rise"]["local_datetime"],
            "moonset": moon_data["set"]["local_datetime"]
        }

    except Exception as e:

        print("Moon times error:", e)

        output["moon_times"] = {
            "moonrise": "Not available",
            "moonset": "Not available"
        }


    # ==============================================
    # RETURN COMPLETE PANCHANG DATA
    # ==============================================

    return output


# ==============================================
# GET TITHI NUMBER
# ==============================================

@st.cache_data(ttl=3600)
def get_tithi_number(selected_date):

    # ----------------------------------------------
    # CHECK API KEY
    # ----------------------------------------------

    if not API_KEY:
        raise ValueError(
            "NAVAMSHA_API_KEY not found in .env file."
        )

    headers = {
        "X-API-Key": API_KEY,
        "Content-Type": "application/json"
    }

    payload = {
        "year": selected_date.year,
        "month": selected_date.month,
        "date": selected_date.day,
        "hours": 7,
        "minutes": 0,
        "latitude": LATITUDE,
        "longitude": LONGITUDE,
        "timezone": TIMEZONE
    }


    # ----------------------------------------------
    # CALL PANCHANG API
    # ----------------------------------------------

    response = requests.post(
        PANCHANG_URL,
        headers=headers,
        json=payload,
        timeout=20
    )

    response.raise_for_status()

    data = response.json()["output"]


    # ----------------------------------------------
    # RETURN TITHI NUMBER
    # ----------------------------------------------

    return data["tithi"]["number"]