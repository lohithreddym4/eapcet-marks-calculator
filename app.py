import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

st.title("📊 EAPCET Score Calculator")

url = st.text_input("Enter your EAPCET response sheet URL:")

if st.button("Calculate Score") and url:
    try:
        headers = {
            "User-Agent": (
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/114.0.0.0 Safari/537.36"
            )
        }

        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, 'html.parser')
        panels = soup.select('.question-pnl')
        total = len(panels)
        correct = 0

        for panel in panels:
            panel_html = str(panel)
            chosen_match = re.search(r'Chosen Option\s*:</td>\s*<td[^>]*>\s*(\d)', panel_html)
            chosen = chosen_match.group(1) if chosen_match else None

            right_td = panel.select_one('td.rightAns')
            correct_match = re.match(r'^\s*(\d)', right_td.text.strip()) if right_td else None
            correct_option = correct_match.group(1) if correct_match else None

            if chosen and correct_option and chosen == correct_option:
                correct += 1

        st.success(f"✅ Correct Answers: {correct}")
        st.error(f"❌ Wrong/Unanswered: {total - correct}")
        st.info(f"🎯 Final Score: {correct}")

    except requests.exceptions.HTTPError as http_err:
        st.error(f"HTTP error occurred: {http_err}")
    except Exception as e:
        st.error(f"Something went wrong: {str(e)}")
