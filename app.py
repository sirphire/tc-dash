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

    safe_sheet_name = quote(sheet_name, safe="")
    return f"https://docs.google.com/spreadsheets/d/{sheet_id}/gviz/tq?tqx=out:csv&sheet={safe_sheet_name}"


def is_location(value):
    value = str(value).strip()
    return bool(re.match(r"^[A-Z]{1,4}\d{1,4}(\s*&\s*[A-Z]{1,4}\d{1,4})*$", value))


@st.cache_data(ttl=30)
def load_data(sheet_url):
    compatible_url = sheet_csv_url(sheet_url, "compatible modal")
    all_models_url = sheet_csv_url(sheet_url, "All Modals")

    compatible_raw = pd.read_csv(compatible_url, header=None, dtype=str)
    models_raw = pd.read_csv(all_models_url, header=None, dtype=str)

    compatible_raw = compatible_raw.dropna(how="all").dropna(axis=1, how="all")
    models_raw = models_raw.dropna(how="all").dropna(axis=1, how="all")

    compatible_raw = compatible_raw.fillna("")
    models_raw = models_raw.fillna("")

    # Location column auto detect: K14, K13, J8, K10 & J8 type values
    location_scores = {}
    for col in compatible_raw.columns:
        location_scores[col] = compatible_raw[col].apply(is_location).sum()

    location_col = max(location_scores, key=location_scores.get)

    if location_scores[location_col] == 0:
        raise Exception("Location column detect nahi hua. compatible modal sheet me K14/K13/K10 jaisi location values check karo.")

    # Compatible column auto detect:
    # Location column ke baad jo sabse lambi text wali column hai use compatible maan rahe hain.
    possible_cols = [col for col in compatible_raw.columns if col != location_col]

    text_scores = {}
    for col in possible_cols:
        text_scores[col] = compatible_raw[col].astype(str).str.len().sum()

    compatible_col = max(text_scores, key=text_scores.get)

    compatible_df = compatible_raw[[location_col, compatible_col]].copy()
    compatible_df.columns = ["location", "compatible"]

    compatible_df["location"] = compatible_df["location"].astype(str).str.strip()
    compatible_df["compatible"] = compatible_df["compatible"].astype(str).str.strip()

    compatible_df = compatible_df[
        compatible_df["location"].apply(is_location)
    ]

    compatible_df = compatible_df[
        compatible_df["compatible"] != ""
    ]

    compatible_df = compatible_df.drop_duplicates().reset_index(drop=True)

    # All Modals sheet auto detect:
    # Jis column me sabse zyada non-empty values hain usko model column maan rahe hain.
    model_scores = {}
    for col in models_raw.columns:
        values = models_raw[col].astype(str).str.strip()
        values = values[values != ""]
        model_scores[col] = len(values)

    model_col = max(model_scores, key=model_scores.get)

    models_df = models_raw[[model_col]].copy()
    models_df.columns = ["model"]

    models_df["model"] = models_df["model"].astype(str).str.strip()
    models_df = models_df[models_df["model"] != ""]
    models_df = models_df[
        ~models_df["model"].str.lower().str.contains("all modals|all models", na=False)
    ]

    model_list = sorted(models_df["model"].drop_duplicates().tolist())

    return compatible_df, model_list, location_col, compatible_col, model_col


if not SHEET_URL:
    st.error("SHEET_URL missing hai. Streamlit secrets me Google Sheet link add karo.")
    st.stop()

try:
    df, model_list, location_col, compatible_col, model_col = load_data(SHEET_URL)
except Exception as e:
    st.error("Google Sheet data load nahi ho raha.")
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

        with st.expander("Matched Rows"):
            st.dataframe(result, use_container_width=True)

else:
    st.info("Dropdown se model select karo ya manually search karo.")

st.divider()

with st.expander("Full Backend Data"):
    st.dataframe(df, use_container_width=True)

with st.expander("Debug Info"):
    st.write("Detected location column:", location_col)
    st.write("Detected compatible column:", compatible_col)
    st.write("Detected model column:", model_col)
    st.write("Backend rows:", len(df))
    st.write("Model count:", len(model_list))
