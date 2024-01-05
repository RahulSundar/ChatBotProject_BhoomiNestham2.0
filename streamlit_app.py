from collections import namedtuple
import altair as alt

import os, time
import pandas as pd
import math
import glob
import base64
from io import StringIO

import openai
import tiktoken
encoding = tiktoken.get_encoding("cl100k_base")
encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")
# -------------IMPORTING CORE FUNCTIONALITIES OF THE SpeeKAR_BOT-------------
from src.embeddinggenerator import *
from src.chatbotfunctions import chatbot

# -------------------AUDIO FUNCTIONALITY-------------------------
from mutagen.wave import WAVE

# --------------------HTML BUILDER AND FUNCTIONALITIES-----------------------------------#
from htbuilder import (
    HtmlElement,
    div,
    ul,
    li,
    br,
    hr,
    a,
    p,
    img,
    styles,
    classes,
    fonts,
)
from htbuilder.units import percent, px
from htbuilder.funcs import rgba, rgb

import streamlit as st
from audiorecorder import audiorecorder


from PIL import Image


# ------------------DEFAULTS--------------------#
os.environ["OPENAI_API_KEY"] = SECRET_API_TOKEN
SECRET_API_TOKEN = os.environ["SECRET_TOKEN"]
openai.api_key = os.environ["OPENAI_API_KEY"]

# -----------------------HELPER FUNCTIONS--------------------------#
def image(src_as_string, **style):
    return img(src=src_as_string, style=styles(**style))


def link(link, text, **style):
    return a(_href=link, _target="_blank", style=styles(**style))(text)


def layout(*args):
    style = """
    <style>
      # MainMenu {visibility: display;}
      footer {visibility: display;}
     .stApp { bottom: 105px; }
    </style>
    """
    style_div = styles(
        position="fixed",
        left=0,
        bottom=0,
        margin=px(0, 50, 0, 50),
        width=percent(100),
        color="black",
        text_align="left",
        height="auto",
        opacity=1,
    )

    style_hr = styles(
        display="block",
        margin=px(8, 8, "auto", "auto"),
        border_style="inset",
        border_width=px(1.5),
    )

    body = p()
    foot = div(style=style_div)(hr(style=style_hr), body)

    st.markdown(style, unsafe_allow_html=True)

    for arg in args:
        if isinstance(arg, str):
            body(arg)

        elif isinstance(arg, HtmlElement):
            body(arg)

    st.markdown(str(foot), unsafe_allow_html=True)


# -------------------------------FUNCTIONS FOR RESPONSE GENERATION-------------#

def generate_kARanswer(query, text_split):
    ans, context, keys = chatbot_slim(query, text_split)
    return ans, context, keys


# -------------------------------------------------------------------------#
# --------------------------GUI CONFIGS------------------------------------#
# -------------------------------------------------------------------------#
# App title
st.set_page_config(page_title="Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot")
st.header("Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot")


# Hugging Face Credentials
with st.sidebar:
    st.title("Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot")
    st.success(
        "Access to this Gen-AI Powered Chatbot is provided by  [Rahul Sundar](https://www.linkedin.com/in/rahul-sundar-311a6977/)!!",
        icon="✅",
    )
    hf_email = "rahulsundar@smail.iitm.ac.in"
    hf_pass = "PASS"
    st.markdown(
        "📖 This app is hosted by [Rahul Sundar](https://github.com/RahulSundar)."
    )
    #image = Image.open("speekar_logo.png")
    #st.image(
    #    image,
    #    caption=None,
    #    width=None,
    #    use_column_width=None,
    #    clamp=False,
    #    channels="RGB",
    #    output_format="auto",
    #)


# ---------------------------------------------------------#
# -----------------LOAD THE DOCUMENT INDICES-----------------#
# ---------------------------------------------------------#
st.title("Please let me know what your queries are!")


if "messages" not in st.session_state.keys():
    st.session_state.messages = []

# ------------------------------------------------------------------------------#
# -------------------------QUERY AUDIO INPUT - RETURNING TEXT QUERY-------------#
# ------------------------------------------------------------------------------#

if st.session_state.messages != []:
    for message in st.session_state.messages[::-1]:
        with st.chat_message(message["role"]):
            st.write(message["content"])



myargs = [
    "Made in India",
    "" " with ❤️ by ",
    link("https://github.com/RahulSundar", "@RahulSundar"),
    br(),
    link("https://github.com/RahulSundar", "Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot"),
    br(),
    link("https://www.linkedin.com/in/rahul-sundar-311a6977/", "@RahulSundar"),
    br(),
    link("https://github.com/RahulSundar", "Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot"),
]


def footer():
    myargs = [
        "Made in India",
        "" " with ❤️ by ",
        link("https://www.linkedin.com/in/rahul-sundar-311a6977/", "@Rahul"),
        link("https://github.com/RahulSundar", "Bhoomi-Nestham-V2.0 @ Gen AI-Chat Bot"),
    ]
    layout(*myargs)


footer()
