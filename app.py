import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="TC Dash",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ---------- Force Light Modern UI CSS ----------
st.markdown("""
<style>
:root {
    color-scheme: light !important;
}

html, body, [data-testid="stAppViewContainer"], .stApp {
    background: linear-gradient(135deg, #fcf7f7 0%, #ffffff 48%, #f7f8fb 100%) !important;
    color: #111827 !important;
    color-scheme: light !important;
}

* {
    color-scheme: light !important;
}

.block-container {
    padding-top: 1.8rem;
    padding-bottom: 2rem;
    max-width: 1080px;
}

/* Hide Streamlit default menu/footer/header as much as possible */
#MainMenu {
    visibility: hidden;
}
footer {
    visibility: hidden;
}
header {
    visibility: hidden;
}
.stToolbar {
    display: none !important;
}

/* Base readable text */
html, body, .stApp,
p, li, span, div, label {
    color: #111827 !important;
}

/* Hero section */
.app-card {
    background: linear-gradient(180deg, #ffffff 0%, #fffdfd 100%) !important;
    border: 1px solid #f0dede;
    border-radius: 26px;
    padding: 30px 32px;
    box-shadow: 0 18px 45px rgba(25, 25, 25, 0.06);
    margin-bottom: 26px;
    position: relative;
    overflow: hidden;
}

.app-card:before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 6px;
    background: linear-gradient(90deg, #ff4b4b 0%, #ff7a7a 100%);
}

.utility-tag {
    display: inline-block;
    background: #fff4f4 !important;
    color: #d92d37 !important;
    border: 1px solid #ffd8d8;
    padding: 8px 14px;
    border-radius: 999px;
    font-size: 0.82rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-bottom: 18px;
}

.app-title {
    font-size: 3rem;
    font-weight: 700;
    color: #1f2937 !important;
    margin-bottom: 10px;
    letter-spacing: -0.04em;
    line-height: 1.08;
}

.app-title span {
    color: #d92d37 !important;
    font-weight: 700;
}

.app-subtitle {
    font-size: 1.12rem;
    color: #4b5563 !important;
    line-height: 1.65;
    margin-bottom: 0;
    font-weight: 400;
    max-width: 760px;
}

/* Input labels */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 1.02rem !important;
    font-weight: 500 !important;
    color: #1f2937 !important;
}

/* Input wrapper text */
div[data-testid="stSelectbox"] div,
div[data-testid="stTextInput"] div {
    font-size: 1.02rem !important;
    color: #111827 !important;
    font-weight: 400 !important;
}

/* Input boxes */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 16px !important;
    background-color: #ffffff !important;
    border: 1.5px solid #d6dbe4 !important;
    color: #111827 !important;
    min-height: 54px !important;
    box-shadow: none !important;
}

/* Dropdown selected value */
div[data-baseweb="select"] span {
    color: #111827 !important;
    font-weight: 400 !important;
    background-color: transparent !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Manual input text */
div[data-baseweb="input"] input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Placeholder */
div[data-baseweb="input"] input::placeholder {
    color: #667085 !important;
    opacity: 1 !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #667085 !important;
}

/* Force dropdown menu readable on all phones */
div[data-baseweb="popover"] {
    background-color: #ffffff !important;
    color: #111827 !important;
}

div[data-baseweb="popover"] * {
    background-color: #ffffff !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 400 !important;
}

ul[role="listbox"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    border: 1px solid #d1d5db !important;
    border-radius: 14px !important;
}

li[role="option"] {
    background-color: #ffffff !important;
    color: #111827 !important;
    font-weight: 400 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[role="option"] div,
li[role="option"] span {
    background-color: transparent !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 400 !important;
}

li[role="option"]:hover {
    background-color: #f8fafc !important;
    color: #111827 !important;
}

li[role="option"]:hover * {
    background-color: #f8fafc !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[aria-selected="true"],
li[aria-selected="true"] * {
    background-color: #fff5f5 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 500 !important;
}

/* Prevent browser dark-mode inversion */
input, textarea, select, button {
    color-scheme: light !important;
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Alerts */
.stAlert {
    border-radius: 18px;
    border: 1px solid rgba(22, 163, 74, 0.12);
}

.stAlert div {
    color: #166534 !important;
    font-weight: 400 !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 22px;
    padding: 20px 22px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.04);
}

[data-testid="stMetricLabel"] {
    font-size: 0.98rem !important;
    color: #667085 !important;
    font-weight: 500 !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.6rem !important;
    font-weight: 600 !important;
    color: #1f2937 !important;
}

/* Section headings */
.section-title {
    font-size: 1.35rem;
    font-weight: 600;
    color: #1f2937 !important;
    margin-top: 8px;
    margin-bottom: 14px;
}

/* Selected model card */
.selected-model {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 18px;
    padding: 15px 18px;
    margin: 18px 0 16px 0;
    box-shadow: 0 8px 22px rgba(0,0,0,0.035);
    font-size: 1.02rem;
    color: #1f2937 !important;
    font-weight: 400 !important;
}

.selected-model .label {
    color: #667085 !important;
    font-weight: 500 !important;
    margin-right: 8px;
}

.selected-model .value {
    color: #1f2937 !important;
    font-weight: 400 !important;
}

/* Compatible list cards */
.model-item {
    background: #ffffff !important;
    border: 1px solid #eceff3;
    border-radius: 16px;
    padding: 13px 15px;
    margin-bottom: 9px;
    box-shadow: 0 6px 16px rgba(0,0,0,0.03);
    color: #1f2937 !important;
    font-weight: 400 !important;
    font-size: 1rem !important;
    line-height: 1.45;
}

/* Expander */
details {
    background: #ffffff !important;
    border-radius: 16px !important;
    color: #111827 !important;
    border: 1px solid #eceff3;
}

details * {
    color: #111827 !important;
}

/* Mobile optimization */
@media screen and (max-width: 768px) {
    .block-container {
        padding-top: 1.1rem;
        padding-left: 0.95rem;
        padding-right: 0.95rem;
    }

    .app-card {
        padding: 22px 20px;
        border-radius: 22px;
        margin-bottom: 20px;
    }

    .utility-tag {
        font-size: 0.74rem;
        padding: 7px 11px;
    }

    .app-title {
        font-size: 2.45rem;
        line-height: 1.12;
    }

    .app-subtitle {
        font-size: 1.04rem;
        color: #475467 !important;
        font-weight: 400;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-size: 1.04rem !important;
        font-weight: 500 !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input {
        font-size: 1rem !important;
        color: #111827 !important;
        font-weight: 400 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #667085 !important;
        font-weight: 400 !important;
        -webkit-text-fill-color: #667085 !important;
    }

    [data-testid="stMetric"] {
        padding: 16px 18px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.15rem !important;
        font-weight: 600 !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.96rem !important;
    }

    .model-item {
        font-size: 0.98rem !important;
        font-weight: 400 !important;
    }

    .selected-model {
        font-size: 1rem !important;
    }

    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="app-card">
    <div class="utility-tag">SIRPHIRE UTILITY</div>
    <div class="app-title">Tempered <span>Compatibility</span> Dashboard</div>
    <p class="app-subtitle">
        Search a model and instantly view its compatible tempered glass location and supported model list.
    </p>
</div>
""", unsafe_allow_html=True)

SHEET_URL = st.secrets.get("SHEET_URL", "")


# ---------- Google Sheet Helpers ----------
def get_sheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if match:
        return match.group(1)
    return None


def excel_export_url(sheet_url):
    sheet_id = get_sheet_id(sheet_url)
    if not sheet_id:
        return sheet_url
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"


@st.cache_data(ttl=60)
def load_data(sheet_url):
    url = excel_export_url(sheet_url)

    compatible_raw = pd.read_excel(
        url,
        sheet_name="compatible modal",
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    models_raw = pd.read_excel(
        url,
        sheet_name="All Modals",
        header=None,
        dtype=str,
        engine="openpyxl"
    )

    compatible_raw = compatible_raw.fillna("")
    models_raw = models_raw.fillna("")

    # compatible modal sheet:
    # Column B = location
    # Column C = compatible model list
    compatible_df = compatible_raw.iloc[:, [1, 2]].copy()
    compatible_df.columns = ["location", "compatible"]

    compatible_df["location"] = compatible_df["location"].astype(str).str.strip()
    compatible_df["compatible"] = compatible_df["compatible"].astype(str).str.strip()

    compatible_df = compatible_df[
        (compatible_df["location"] != "") &
        (compatible_df["compatible"] != "")
    ]

    compatible_df = compatible_df[
        ~compatible_df["location"].str.lower().str.contains("s.no|location|nan", na=False)
    ]

    compatible_df = compatible_df[
        ~compatible_df["compatible"].str.lower().str.contains("compatible model names|nan", na=False)
    ]

    compatible_df = compatible_df.drop_duplicates().reset_index(drop=True)

    # All Modals sheet:
    # Column C = model names
    models_df = models_raw.iloc[:, [2]].copy()
    models_df.columns = ["model"]

    models_df["model"] = models_df["model"].astype(str).str.strip()

    models_df = models_df[
        (models_df["model"] != "") &
        (~models_df["model"].str.lower().str.contains("all modals|all models|nan", na=False))
    ]

    model_list = sorted(models_df["model"].drop_duplicates().tolist())

    return compatible_df, model_list


# ---------- Load Data ----------
if not SHEET_URL:
    st.error("SHEET_URL is missing. Please add your Google Sheet link in Streamlit secrets.")
    st.stop()

try:
    df, model_list = load_data(SHEET_URL)
except Exception as e:
    st.error("Unable to load Google Sheet data.")
    st.caption(str(e))
    st.stop()


# ---------- Search UI ----------
col1, col2 = st.columns([2, 1])

with col1:
    selected_model = st.selectbox(
        "Select or search a model",
        options=[""] + model_list,
        index=0
    )

with col2:
    manual_search = st.text_input(
        "Or type manually",
        placeholder="Example: Redmi Note 7 Tempered"
    )

search_model = manual_search.strip() if manual_search.strip() else selected_model.strip()


# ---------- Results ----------
if search_model:
    result = df[
        df["compatible"].astype(str).str.contains(search_model, case=False, na=False, regex=False)
    ]

    if result.empty:
        st.warning("No compatible result found.")
    else:
        locations = sorted(result["location"].astype(str).str.strip().unique())

        all_compatible = []
        for value in result["compatible"].astype(str):
            parts = [x.strip() for x in value.split(",") if x.strip()]
            all_compatible.extend(parts)

        all_compatible = sorted(set(all_compatible))

        st.success("Result found")

        st.markdown(
            f'''
            <div class="selected-model">
                <span class="label">Selected model:</span>
                <span class="value">{search_model}</span>
            </div>
            ''',
            unsafe_allow_html=True
        )

        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Location", " & ".join(locations))
        metric_col2.metric("Compatible Count", len(all_compatible))

        st.markdown('<div class="section-title">Compatible Model List</div>', unsafe_allow_html=True)

        for model in all_compatible:
            st.markdown(
                f'<div class="model-item">{model}</div>',
                unsafe_allow_html=True
            )

        with st.expander("Matched Rows"):
            st.dataframe(result, use_container_width=True)

else:
    st.info("Select a model from the dropdown or type it manually.")
