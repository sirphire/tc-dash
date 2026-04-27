import streamlit as st
import pandas as pd
import re

st.set_page_config(
    page_title="TC Dash",
    page_icon="📱",
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
    background: linear-gradient(135deg, #fff7f7 0%, #ffffff 45%, #f7f8fb 100%) !important;
    color: #111827 !important;
    color-scheme: light !important;
}

* {
    color-scheme: light !important;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
    max-width: 1100px;
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

/* Main readable text */
html, body, .stApp,
p, li, span, div, label {
    color: #111827 !important;
}

/* Hero card */
.app-card {
    background: #ffffff !important;
    border: 1px solid #f0dede;
    border-radius: 24px;
    padding: 30px 32px;
    box-shadow: 0 18px 45px rgba(25, 25, 25, 0.08);
    margin-bottom: 24px;
}

.badge {
    display: inline-block;
    background: #ff3b45 !important;
    color: #ffffff !important;
    padding: 7px 14px;
    border-radius: 999px;
    font-size: 0.85rem;
    font-weight: 800;
    margin-bottom: 14px;
    letter-spacing: 0.03em;
}

.app-title {
    font-size: 3rem;
    font-weight: 850;
    color: #20212b !important;
    margin-bottom: 8px;
    letter-spacing: -0.04em;
    line-height: 1.1;
}

.app-subtitle {
    font-size: 1.2rem;
    color: #374151 !important;
    line-height: 1.6;
    margin-bottom: 0;
    font-weight: 550;
}

/* Input labels */
div[data-testid="stSelectbox"] label,
div[data-testid="stTextInput"] label {
    font-size: 1.05rem !important;
    font-weight: 750 !important;
    color: #111827 !important;
}

/* Input/dropdown text */
div[data-testid="stSelectbox"] div,
div[data-testid="stTextInput"] div {
    font-size: 1.03rem !important;
    color: #111827 !important;
}

/* Input boxes */
div[data-baseweb="select"] > div,
div[data-baseweb="input"] > div {
    border-radius: 16px !important;
    background-color: #ffffff !important;
    border: 1.5px solid #d1d5db !important;
    color: #111827 !important;
}

/* Dropdown selected value */
div[data-baseweb="select"] span {
    color: #111827 !important;
    font-weight: 700 !important;
    background-color: transparent !important;
}

/* Manual input text */
div[data-baseweb="input"] input {
    color: #111827 !important;
    background-color: #ffffff !important;
    font-weight: 700 !important;
    -webkit-text-fill-color: #111827 !important;
}

/* Placeholder darker */
div[data-baseweb="input"] input::placeholder {
    color: #4b5563 !important;
    opacity: 1 !important;
    font-weight: 650 !important;
    -webkit-text-fill-color: #4b5563 !important;
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
    font-weight: 700 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[role="option"] div,
li[role="option"] span {
    background-color: transparent !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[role="option"]:hover {
    background-color: #f3f4f6 !important;
    color: #111827 !important;
}

li[role="option"]:hover * {
    background-color: #f3f4f6 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
}

li[aria-selected="true"],
li[aria-selected="true"] * {
    background-color: #fee2e2 !important;
    color: #111827 !important;
    -webkit-text-fill-color: #111827 !important;
    font-weight: 800 !important;
}

/* Prevent browser dark-mode color inversion */
input,
textarea,
select,
button {
    color-scheme: light !important;
    background-color: #ffffff !important;
    color: #111827 !important;
}

/* Alerts */
.stAlert {
    border-radius: 18px;
    border: 1px solid rgba(22, 163, 74, 0.15);
}

.stAlert div {
    color: #14532d !important;
    font-weight: 750 !important;
}

/* Warning */
div[data-testid="stAlert"] {
    font-size: 1rem !important;
}

/* Metrics */
[data-testid="stMetric"] {
    background: #ffffff !important;
    border: 1px solid #eeeeee;
    border-radius: 20px;
    padding: 20px 22px;
    box-shadow: 0 10px 28px rgba(0,0,0,0.05);
}

[data-testid="stMetricLabel"] {
    font-size: 1rem !important;
    color: #374151 !important;
    font-weight: 750 !important;
}

[data-testid="stMetricValue"] {
    font-size: 2.7rem !important;
    font-weight: 850 !important;
    color: #20212b !important;
}

/* Section headings */
h2, h3 {
    color: #20212b !important;
    font-weight: 850 !important;
    letter-spacing: -0.03em;
}

/* Normal text */
p, li, span, div {
    font-size: 1rem;
}

/* Selected model text */
.selected-model {
    background: #ffffff !important;
    border: 1px solid #eeeeee;
    border-radius: 16px;
    padding: 14px 16px;
    margin: 18px 0 16px 0;
    box-shadow: 0 8px 22px rgba(0,0,0,0.04);
    font-size: 1.05rem;
    font-weight: 700;
    color: #20212b !important;
}

/* Compatible list cards */
.model-item {
    background: #ffffff !important;
    border: 1px solid #eeeeee;
    border-radius: 14px;
    padding: 12px 15px;
    margin-bottom: 8px;
    box-shadow: 0 6px 18px rgba(0,0,0,0.035);
    color: #20212b !important;
    font-weight: 650;
}

/* Expander */
details {
    background: #ffffff !important;
    border-radius: 16px !important;
    color: #111827 !important;
}

details * {
    color: #111827 !important;
}

/* Dataframe light fix */
[data-testid="stDataFrame"] {
    background: #ffffff !important;
    color: #111827 !important;
}

/* Mobile optimization */
@media screen and (max-width: 768px) {
    .block-container {
        padding-top: 1.2rem;
        padding-left: 1rem;
        padding-right: 1rem;
    }

    .app-card {
        padding: 22px 20px;
        border-radius: 20px;
        margin-bottom: 20px;
    }

    .badge {
        font-size: 0.75rem;
        padding: 6px 11px;
    }

    .app-title {
        font-size: 2.35rem;
        line-height: 1.12;
    }

    .app-subtitle {
        font-size: 1.08rem;
        color: #374151 !important;
        font-weight: 650;
    }

    div[data-testid="stSelectbox"] label,
    div[data-testid="stTextInput"] label {
        font-size: 1.08rem !important;
        font-weight: 800 !important;
    }

    div[data-baseweb="select"] span,
    div[data-baseweb="input"] input {
        font-size: 1.02rem !important;
        color: #111827 !important;
        font-weight: 750 !important;
        -webkit-text-fill-color: #111827 !important;
    }

    div[data-baseweb="input"] input::placeholder {
        color: #4b5563 !important;
        font-weight: 700 !important;
        -webkit-text-fill-color: #4b5563 !important;
    }

    [data-testid="stMetric"] {
        padding: 16px 18px;
    }

    [data-testid="stMetricValue"] {
        font-size: 2.2rem !important;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.98rem !important;
    }

    .model-item {
        font-size: 1rem;
        font-weight: 700;
    }
}
</style>
""", unsafe_allow_html=True)

# ---------- Header ----------
st.markdown("""
<div class="app-card">
    <div class="badge">SIRPHIRE UTILITY</div>
    <div class="app-title">📱 Tempered Compatible Finder</div>
    <p class="app-subtitle">
        Search a model and instantly find its tempered glass location and compatible models.
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
            f'<div class="selected-model">Selected Model: {search_model}</div>',
            unsafe_allow_html=True
        )

        metric_col1, metric_col2 = st.columns(2)
        metric_col1.metric("Location", " & ".join(locations))
        metric_col2.metric("Compatible Count", len(all_compatible))

        st.subheader("✅ Compatible Model List")

        for model in all_compatible:
            st.markdown(
                f'<div class="model-item">{model}</div>',
                unsafe_allow_html=True
            )

        with st.expander("Matched Rows"):
            st.dataframe(result, use_container_width=True)

else:
    st.info("Select a model from the dropdown or type it manually.")
