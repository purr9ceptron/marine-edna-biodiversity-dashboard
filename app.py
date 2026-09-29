import pandas as pd
import streamlit as st
from top_species import top_species

st.set_page_config(page_title="Marine eDNA Biodiversity", layout="wide")
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;700&family=Inter:wght@400;500&display=swap');
    .stApp { background: linear-gradient(180deg, #123A45 0%, #0B2027 45%, #071418 100%); }
    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }
    h1, h2, h3 { font-family: 'Space Grotesk', sans-serif; color: #E8DCC4; }
    [data-testid="stMetricValue"] { color: #6ECEBB; }
    [data-testid="stMetricLabel"] { color: #9FB8B4; }
    [data-testid="stMetric"] { background: rgba(255,255,255,0.04);
        border: 1px solid rgba(110,206,187,0.25); border-radius: 10px; padding: 16px; }
</style>
""", unsafe_allow_html=True)


@st.cache_data
def load():
    results = pd.read_csv("ESI22_COI_biodiversity_results.csv")
    asv = pd.read_csv("ESI22.COI.FilteredMergedASVtable.csv")
    return results, asv["Species"].nunique()


df, n_species = load()
st.title("Marine eDNA Biodiversity Dashboard")

# Samples with zero reads are treated separately: they may be failed samples.
empty = df["Richness"] == 0
default = float(round(df.loc[~empty, "Shannon Index"].quantile(0.25), 1))
threshold = st.slider("Flag sites with Shannon index below:", 0.0, 3.0, default, 0.1,
                      help="Default = the lowest quarter of samples that contain DNA.")

df["Status"] = "OK"
df.loc[df["Shannon Index"] < threshold, "Status"] = "Low biodiversity"
df.loc[empty, "Status"] = "No DNA detected"
at_risk = df[df["Status"] == "Low biodiversity"]

c1, c2, c3, c4, c5 = st.columns(5)
c1.metric("Water Samples", len(df))
c2.metric("Species Detected", n_species)
c3.metric("Highest Richness Site", df.loc[df["Richness"].idxmax(), "Sample"])
c4.metric("Low-Biodiversity Sites", len(at_risk))
c5.metric("No-DNA Samples", int(empty.sum()))

st.subheader("Biodiversity Results")
st.dataframe(df, use_container_width=True)

st.subheader("Flagged Low-Biodiversity Sites")
st.dataframe(at_risk, use_container_width=True)
st.caption("Samples with no DNA detected may be failed sequencing runs or controls, "
           "so they are listed separately rather than flagged as low biodiversity.")

st.subheader("Top Species by Total Reads")
st.dataframe(top_species(), use_container_width=True)

st.subheader("Inspect a Single Sample")
chosen = st.selectbox("Choose a sample:", df["Sample"])
st.dataframe(df[df["Sample"] == chosen], use_container_width=True)

for title, img in [("Species Richness", "ESI22_COI_richness_results.png"),
                   ("Shannon Diversity", "ESI22_COI_shannon_results.png"),
                   ("Simpson Diversity", "ESI22_COI_simpson_results.png")]:
    st.subheader(title)
    st.image(img)