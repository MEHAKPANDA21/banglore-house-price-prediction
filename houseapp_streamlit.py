import streamlit as st
import pickle
import numpy as np
import pandas as pd  

# ---------------- CONFIG ----------------
st.set_page_config(page_title="🏠 Bengaluru House Price Predictor", layout="centered")

# ---------------- LOAD MODEL ----------------
@st.cache_resource
def load_model_and_columns():
    try:
        with open('house_prediction_model.pkl', 'rb') as f:
            model = pickle.load(f)
    except FileNotFoundError:
        st.error("Missing file: 'house_prediction_model.pkl'")
        st.stop()

    try:
        with open('columns.pkl', 'rb') as f:
            loaded = pickle.load(f)
            if isinstance(loaded, pd.DataFrame):
                columns = loaded.columns.tolist()
            else:
                columns = loaded
        columns = [col.strip() for col in columns]
    except FileNotFoundError:
        st.error("Missing file: 'columns.pkl'")
        st.stop()

    return model, columns

model, columns = load_model_and_columns()

# ---------------- LOCATIONS ----------------
locations = sorted([col for col in columns if col not in ['total_sqft', 'bath', 'balcony', 'bhk']])
if "others" in locations:
    locations.remove("others")

bhk_options = [1, 2, 3, 4, 5, 6]

# ---------------- PREDICTION ----------------
@st.cache_data
def predict_price(location, total_sqft, bath, balcony, bhk):
    loc_index = np.where(np.array(columns) == location)[0]
    if len(loc_index) == 0:
        loc_index = np.where(np.array(columns) == "Whitefield")[0]
        if len(loc_index) == 0:
            try:
                mean_price = pd.read_csv("Bengaluru_House_Data.csv")["price"].mean()
                return f"₹{mean_price:.2f} Lakhs (Avg)"
            except FileNotFoundError:
                return "Error: Location not in model and no fallback data."

    input_features = np.zeros(len(columns))
    input_features[0] = total_sqft
    input_features[1] = bath
    input_features[2] = balcony
    input_features[3] = bhk
    input_features[loc_index[0]] = 1

    prediction = model.predict([input_features])[0]
    return f"₹{prediction:.2f} Lakhs"

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
    /* Remove top white padding */
    .block-container {
        padding-top: 1rem;
    }

    /* Input Box Styling - transparent */
    .input-card {
        background: transparent;
        padding: 1.5rem;
        border-radius: 0.8rem;
        box-shadow: none;
        max-width: 600px;
        margin: auto;
    }

    /* Prediction Card - Green background with white text */
    .prediction-card {
        background: #28a745; /* Green */
        padding: 1rem;
        border-radius: 0.8rem;
        text-align: center;
        color: white;
        box-shadow: 0px 3px 8px rgba(0,0,0,0.2);
        max-width: 350px;
        margin: 1.5rem auto;
    }
    .prediction-card h4 {
        font-size: 1rem;
        margin-bottom: 0.3rem;
        font-weight: normal;
        color: #e6e6e6;
    }
    .prediction-card h2 {
        font-size: 1.6rem;
        margin: 0;
        font-weight: bold;
        color: white;
    }
    .prediction-card p {
        font-size: 0.85rem;
        margin-top: 0.3rem;
        color: #f1f1f1;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- UI ----------------
st.title("✨ Bengaluru House Price Predictor")
st.markdown("Enter your house details below and get an **instant price estimate** 🏡")

with st.container():
    st.markdown('<div class="input-card">', unsafe_allow_html=True)

    location = st.selectbox("📍 Location", options=locations, index=0)
    total_sqft = st.slider("📐 Total Sqft", min_value=300, max_value=5000, step=10, value=1000)
    bath = st.number_input("🛁 Bathrooms", value=2, min_value=1, max_value=10)
    balcony = st.number_input("🌤️ Balconies", value=2, min_value=0, max_value=4)
    bhk = st.selectbox("🛏️ BHK", options=bhk_options, index=1)

    predict_btn = st.button("🚀 Predict Price", use_container_width=True)

    st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
if predict_btn:
    prediction = predict_price(location, total_sqft, bath, balcony, bhk)
    st.markdown(f"""
    <div class="prediction-card">
        <h4>Estimated Price</h4>
        <h2>{prediction}</h2>
        <p>{bhk} BHK • {location}</p>
    </div>
    """, unsafe_allow_html=True)
else:
    st.info("👆 Fill the details above and click **Predict Price**")

st.markdown("---")
st.caption("⚡ Powered by Streamlit | Trained on Bengaluru Housing Data")
