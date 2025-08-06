import streamlit as st
import pickle
import numpy as np

# Load the trained model
with open('house_prediction_model.pkl', 'rb') as f:
    lr_clf = pickle.load(f)

# Sample location list (replace with your actual locations used during training)
locations = [
    '1st Block Jayanagar', 'Indira Nagar', 'HSR Layout', 'Whitefield', 
    'Rajaji Nagar', 'Banashankari', 'Electronic City', 'Marathahalli'
    # Add more locations as per your dataset
]

# Streamlit app UI
st.title("🏠 Bangalore House Price Predictor")

st.markdown("### 📌 Enter the property details below")

# User inputs
location = st.selectbox("📍 Location", sorted(locations))
total_sqft = st.number_input("📐 Total Square Feet", min_value=300, max_value=10000, value=1000)
bath = st.number_input("🛁 Number of Bathrooms", min_value=1, max_value=10, value=2)
bhk = st.number_input("🛏️ Number of BHK", min_value=1, max_value=10, value=2)

# Predict function
def predict_price(location, total_sqft, bath, bhk):
    # Replace this with the actual column order used in training
    columns = ['total_sqft', 'bath', 'bhk'] + locations
    x = np.zeros(len(columns))
    x[0] = total_sqft
    x[1] = bath
    x[2] = bhk
    if location in locations:
        loc_index = columns.index(location)
        x[loc_index] = 1
    return lr_clf.predict([x])[0]

# Button to trigger prediction
if st.button("💰 Predict Price"):
    try:
        result = predict_price(location, total_sqft, bath, bhk)
        st.success(f"🏷️ Estimated Price: ₹ {result:.2f} Lakhs")
    except Exception as e:
        st.error(f"❌ Prediction failed: {e}")
