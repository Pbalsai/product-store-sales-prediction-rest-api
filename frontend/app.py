
import streamlit as st
import requests

# App Title
st.title("SuperKart Sales Forecasting")

# -----------------------------------------------------
# Input Fields
# -----------------------------------------------------

Product_Weight = st.number_input(
    "Product Weight",
    min_value=0.0,
    value=12.66
)

Product_Sugar_Content = st.selectbox(
    "Product Sugar Content",
    ["Low Sugar", "Regular", "No Sugar"]
)

Product_Allocated_Area = st.number_input(
    "Product Allocated Area",
    min_value=0.0,
    value=0.027
)

Product_MRP = st.number_input(
    "Product MRP",
    min_value=0.0,
    value=117.08
)

Store_Size = st.selectbox(
    "Store Size",
    ["Small", "Medium", "High"]
)

Store_Location_City_Type = st.selectbox(
    "Store Location City Type",
    ["Tier 1", "Tier 2", "Tier 3"]
)

Store_Type = st.selectbox(
    "Store Type",
    [
        "Supermarket Type1",
        "Supermarket Type2",
        "Departmental Store",
        "Food Mart",
    ]
)

Product_Id_char = st.selectbox(
    "Product ID Category",
    ["FD", "DR", "NC"]
)

Store_Age_Years = st.number_input(
    "Store Age (Years)",
    min_value=1,
    value=17
)

Product_Type_Category = st.selectbox(
    "Product Type Category",
    ["Perishables", "Non Perishables"]
)

# -----------------------------------------------------
# Create JSON payload
# -----------------------------------------------------

product_data = {
    "Product_Weight": Product_Weight,
    "Product_Sugar_Content": Product_Sugar_Content,
    "Product_Allocated_Area": Product_Allocated_Area,
    "Product_MRP": Product_MRP,
    "Store_Size": Store_Size,
    "Store_Location_City_Type": Store_Location_City_Type,
    "Store_Type": Store_Type,
    "Product_Id_char": Product_Id_char,
    "Store_Age_Years": Store_Age_Years,
    "Product_Type_Category": Product_Type_Category,
}

# -----------------------------------------------------
# Prediction
# -----------------------------------------------------

if st.button("Predict", type="primary"):

    response = requests.post(
        "https://crispy-space-capybara-jr476x4xgqjjfpjqw-7860.app.github.dev/v1/predict",
        json=product_data,
    )


    st.write("Status Code:", response.status_code)
    st.write("Response Text:")
    st.code(response.text)

    if response.status_code == 200:

        result = response.json()

        predicted_sales = result["predicted_sales"]

        st.success(
            f"Predicted Product Store Sales Total: {predicted_sales:.2f}"
        )

    else:
        st.error("API request failed.")
