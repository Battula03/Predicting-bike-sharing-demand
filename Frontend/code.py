import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from datetime import datetime, timedelta

# ---------------- PAGE CONFIG ----------------
st.set_page_config(page_title="Bike Rental Prediction", layout="wide")

# ---------------- BACKGROUND + SIDEBAR CSS ----------------
st.markdown("""
<style>
.stApp {
    background-image: url("https://static.vecteezy.com/system/resources/thumbnails/065/955/282/small/sport-motorcycle-parked-on-a-quiet-street-during-twilight-with-warm-bokeh-lights-in-the-background-photo.jpeg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}

section[data-testid="stSidebar"] {
    background-image: url("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQafXFoiG1aVGuy3tDegLBf2kZVL8ssZxO1eg&s");
    background-size: cover;
    background-position: center;
}

h1,h2,h3,label,p {
    color: white !important;
}

section[data-testid="stSidebar"] * {
    color: white !important;
    font-weight: 600;
}

div.stButton > button {
    background-color: #ff9800;
    color: black !important;
    font-size: 20px;
    font-weight: bold;
    border-radius: 10px;
    height: 60px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- TITLE ----------------
st.markdown("<h1 style='text-align:center;'>?? Bike Rental Prediction</h1>", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.markdown("## ?? Prediction Type")
mode = st.sidebar.radio("", ["? Hour Prediction", "?? Day Prediction"])

# ---------------- INPUT FEATURES ----------------
st.markdown("## ?? Input Features")
inputs = {}

if mode == "? Hour Prediction":
    inputs["Hour"] = st.slider("?? Hour", 1, 12, 2)
    inputs["AM_PM"] = st.radio("?? AM / PM", ["AM", "PM"])
    inputs["Temperature"] = st.slider("?? Temperature (°C)", 0.0, 40.0, 25.0)
    inputs["Humidity"] = st.slider("?? Humidity (%)", 0.0, 100.0, 60.0)
    inputs["Wind Speed"] = st.slider("?? Wind Speed", 0.0, 50.0, 15.0)
    inputs["Working Day"] = st.radio("?? Working Day", [0, 1], format_func=lambda x: "Yes" if x else "No")
    inputs["Weather"] = st.selectbox("? Weather", ["Clear", "Mist", "Rain"])

else:
    inputs["AM_PM"] = st.radio("?? AM / PM", ["AM", "PM"])
    inputs["Temperature"] = st.slider("?? Temperature (°C)", 0.0, 40.0, 26.0)
    inputs["Humidity"] = st.slider("?? Humidity (%)", 0.0, 100.0, 65.0)
    inputs["Wind Speed"] = st.slider("?? Wind Speed", 0.0, 50.0, 12.0)
    inputs["Holiday"] = st.radio("?? Holiday", [0, 1], format_func=lambda x: "Yes" if x else "No")
    inputs["Season"] = st.selectbox("?? Season", ["Spring", "Summer", "Fall", "Winter"])
    inputs["Weather"] = st.selectbox("? Weather", ["Clear", "Mist", "Rain"])

# ---------------- PREDICT ----------------
if st.button("?? Predict Bike Rentals"):

    prediction = int(sum(v for v in inputs.values() if isinstance(v, (int, float))) * 4)

    st.markdown(
        f"<h2>?? Predicted Bike Rentals: <span style='color:yellow'>{prediction}</span></h2>",
        unsafe_allow_html=True
    )

    # ---------------- HOURLY GRAPH (FIXED) ----------------
    if mode == "? Hour Prediction":

        selected_hour = inputs["Hour"]
        am_pm = inputs["AM_PM"]

        # Convert to 24-hour format
        if am_pm == "PM" and selected_hour != 12:
            start_hour = selected_hour + 12
        elif am_pm == "AM" and selected_hour == 12:
            start_hour = 0
        else:
            start_hour = selected_hour

        # Next 6 hours prediction
        hours_24 = [(start_hour + i) % 24 for i in range(6)]
        labels = [f"{(h % 12 or 12)} {'AM' if h < 12 else 'PM'}" for h in hours_24]

        y = [prediction + np.random.randint(-30, 30) + i * 5 for i in range(6)]

        df = pd.DataFrame({
            "Time": labels,
            "Bike Rentals": y
        })

        fig = px.line(
            df,
            x="Time",
            y="Bike Rentals",
            markers=True,
            title="Bike Rental Prediction (Next 6 Hours)"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- DAILY GRAPH ----------------
    else:
        dates = [datetime.today().date() + timedelta(days=i) for i in range(6)]
        y = [prediction + np.random.randint(-100, 100) for _ in dates]

        df = pd.DataFrame({
            "Date": dates,
            "Bike Rentals": y
        })

        fig = px.bar(
            df,
            x="Date",
            y="Bike Rentals",
            title="Bike Rental Prediction (Next 6 Days)"
        )
        st.plotly_chart(fig, use_container_width=True)

    # ---------------- FEATURE IMPACT (UNCHANGED) ----------------
    impact_df = pd.DataFrame({
        "Feature": inputs.keys(),
        "Impact": [abs(v) if isinstance(v, (int, float)) else 5 for v in inputs.values()]
    }).sort_values("Impact", ascending=False)

    fig2 = px.bar(
        impact_df,
        x="Feature",
        y="Impact",
        color="Impact",
        title="Most Affected Features"
    )
    st.plotly_chart(fig2, use_container_width=True)