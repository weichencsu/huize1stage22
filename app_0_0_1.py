# coding=utf-8
import streamlit as st
from multipage import MultiPage
from Renamepages import page1, page2, page3, page4, page5, page6

MAGE_EMOJI_URL = "streamlitBKN.png"
st.set_page_config(page_title='Oresome IoT',page_icon=MAGE_EMOJI_URL, initial_sidebar_state = 'auto', layout="wide")
#page_icon = favicon,
st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container{{
                max-width: 1600px;
                padding-top: 1rem;
                padding-right: 1rem;
                padding-left: 1rem;
                padding-bottom: 1rem;
            }}

            .fullScreenFrame > div {{
                display: flex;
                justify-content: left;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

app = MultiPage()

# add applications
app.add_page('📘  1764 Ramp #287-POE Pipe', page1.app)
app.add_page('📕  1764 Bend Section-POE Pipe', page2.app)
app.add_page('📗  1764 Junction-POE Pipe', page3.app)
app.add_page('📔  1764 Ramp #288-Steel Pipe', page4.app)
app.add_page('📒  1404 Entry-Steel Pipe', page5.app)
app.add_page('📙  1398 Mid Well-Steel Pipe', page6.app)

# Run application
if __name__ == '__main__':
    app.run()
