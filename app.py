# app.py
import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="NYC Airbnb Explorer",
    layout="wide"
)

# -----------------------------
# Load data
# -----------------------------
@st.cache_data
def load_data(path):
    df = pd.read_csv(path)
    df = df[df["price"] > 0]
    return df

DATA_PATH = "data/AB_NYC_2019.csv"
df = load_data(DATA_PATH)

# -----------------------------
# Header
# -----------------------------
st.title("NYC Airbnb Explorer 🗽")
st.caption("Interactive overview of Airbnb listings in New York City")

st.divider()

# -----------------------------
# Sidebar filters
# -----------------------------
st.sidebar.header("Filters")

neigh_groups = ["All"] + sorted(df["neighbourhood_group"].unique())
selected_group = st.sidebar.selectbox("Neighbourhood group", neigh_groups)

price_cap = int(df["price"].quantile(0.95))
price_range = st.sidebar.slider(
    "Price range ($)",
    0,
    price_cap,
    (0, price_cap)
)

# Apply filters
filtered_df = df.copy()

if selected_group != "All":
    filtered_df = filtered_df[
        filtered_df["neighbourhood_group"] == selected_group
    ]

filtered_df = filtered_df[
    (filtered_df["price"] >= price_range[0]) &
    (filtered_df["price"] <= price_range[1])
]

# -----------------------------
# High-level metrics
# -----------------------------
c1, c2, c3 = st.columns(3)

c1.metric("Listings", f"{len(filtered_df):,}")
c2.metric("Median price", f"${int(filtered_df['price'].median())}")
c3.metric("Avg availability", f"{int(filtered_df['availability_365'].mean())} days")

st.divider()

# -----------------------------
# Map + distribution
# -----------------------------
left, right = st.columns([2, 1])

with left:
    st.subheader("Listings map")
    st.map(
        filtered_df.rename(
            columns={"latitude": "lat", "longitude": "lon"}
        )[["lat", "lon"]]
    )

with right:
    st.subheader("Price distribution")
    st.bar_chart(
        filtered_df["price"].value_counts(bins=40).sort_index()
    )

st.divider()

# -----------------------------
# Neighbourhood summary
# -----------------------------
st.subheader("Neighbourhood overview")

summary = (
    filtered_df
    .groupby("neighbourhood_group")["price"]
    .agg(["count", "median", "mean"])
    .reset_index()
    .sort_values("median", ascending=False)
)

summary.columns = [
    "Neighbourhood group",
    "Listings",
    "Median price",
    "Mean price"
]

st.dataframe(
    summary,
    use_container_width=True
)

# -----------------------------
# Footer
# -----------------------------
st.caption(
    "Built with Streamlit • Dataset: NYC Airbnb (2019)"
)