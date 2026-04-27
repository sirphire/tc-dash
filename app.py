import streamlit as st
import pandas as pd
import re
from urllib.parse import quote

st.set_page_config(
    page_title="TC Dash",
    page_icon="📱",
    layout="wide"
)

st.title("📱 Tempered Compatible Finder")
st.caption("Model search karo aur compatible tempered glass location dekho.")

SHEET_URL = st.secrets.get("SHEET_URL", "")


def get_sheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    if match:
        return match.group(1)
    return None


def sheet_csv_url(sheet_url, sheet_name):
    sheet_id = get_sheet_id(sheet_url)
    if not sheet_id:
        return sheet_url

    safe_sheet_name = quote(sheet_name)
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={safe_sheet_name}"


@st.cache_data(ttl=60)
def load_data(sheet_url):
    compatible_url = sheet_csv_url(sheet_url, "compatible modal")
    all_models_url = sheet_csv_url(sheet_url, "All Modals")

    compatible_raw = pd.read_csv(compatible_url, header=None)
    models_raw = pd.read_csv(all_models_url, header=None)

    # compatible modal sheet:
    # Column B = location
    # Column C = compatible model list
    compatible_df = compatible_raw.iloc[:, [1, 2]].copy()
    compatible_df.columns = ["location", "compatible"]

    compatible_df = compatible_df.dropna(subset=["location", "compatible"])
    compatible_df = compatible_df[
        ~compatible_df["location"].astype(str).str.lower().str.contains("s.no|location", na=False)
    ]
    compatible_df = compatible_df[
        ~compatible_df["compatible"].astype(str).str.lower().str.contains("compatible model names", na=False)
    ]

    # All Modals sheet:
    # Column C = model names
    models_df = models_raw.iloc[:, [2]].copy()
    models_df.columns = ["model"]
    models_df = models_df.dropna(subset=["model"])
    models_df = models_df[
        ~models_df["model"].astype(str).str.lower().str.contains("all modals", na=False)
    ]

    model_list = sorted(models_df["model"].astype(str).str.strip().unique())

    return compatible_df, model_list


if not SHEET_URL:
    st.error("SHEET_URL missing hai. Streamlit secrets me Google Sheet link add karo.")
    st.stop()

try:
    df, model_list = load_data(SHEET_URL)
except Exception as e:
    st.error("Google Sheet data load nahi ho raha. Sheet share setting aur sheet names check karo.")
    st.caption(str(e))
    st.stop()


col1, col2 = st.columns([2, 1])

with col1:
    selected_model = st.selectbox(
        "Model select/search karo",
        options=[""] + model_list,
        index=0
    )

with col2:
    manual_search = st.text_input(
        "Ya manually type karo",
        placeholder="Example: Redmi Note 7 Tempered"
    )

search_model = manual_search.strip() if manual_search.strip() else selected_model.strip()

if search_model:
    result = df[
        df["compatible"].astype(str).str.contains(search_model, case=False, na=False, regex=False)
    ]

    if result.empty:
        st.warning("Koi compatible result nahi mila.")
    else:
        locations = sorted(result["location"].astype(str).str.strip().unique())

        all_compatible = []
        for value in result["compatible"].astype(str):
            parts = [x.strip() for x in value.split(",") if x.strip()]
            all_compatible.extend(parts)

        all_compatible = sorted(set(all_compatible))

        st.success("Result found")

        kpi1, kpi2, kpi3 = st.columns(3)
        kpi1.metric("Search Model", search_model)
        kpi2.metric("Location", " & ".join(locations))
        kpi3.metric("Compatible Count", len(all_compatible))

        st.subheader("📍 Location")
        st.info(" & ".join(locations))

        st.subheader("✅ Compatible Model List")

        for model in all_compatible:
            st.write(f"- {model}")

        st.divider()

        with st.expander("Matched Rows"):
            st.dataframe(result, use_container_width=True)

else:
    st.info("Dropdown se model select karo ya manually search karo.")

st.divider()

with st.expander("Full Backend Data"):
    st.dataframe(df, use_container_width=True)
