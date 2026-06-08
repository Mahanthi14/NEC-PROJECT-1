import os
import pandas as pd
import streamlit as st

from src.data_loader import load_csv, save_csv
from src.data_merge import merge_old_new_data
from src.preprocessing import clean_data
from src.segmentation import create_segments
from src.churn_prediction import train_churn_model
from src.purchase_prediction import predict_purchase_value, get_products_by_amount
from src.recommendation import recommend_products
from src.inventory_alert import check_low_stock
from src.dashboard_filters import apply_filters
from src.visualization import (
    customer_segment_bar_chart,
    customer_segment_pie_chart,
    gender_bar_chart,
    gender_pie_chart,
    city_bar_chart,
    category_bar_chart,
    category_pie_chart,
    age_spending_scatter,
    churn_bar_chart,
    purchase_prediction_bar_chart,
    kmeans_3d_chart,
    stock_bar_chart,
    low_stock_pie_chart
)
from src.report_generator import generate_report


st.set_page_config(
    page_title="AI Customer Intelligence Dashboard",
    page_icon="📊",
    layout="wide"
)

st.title("📊 AI-Driven Customer Intelligence Dashboard")
st.write(
    "Customer segmentation, predictions, recommendations, filters, "
    "inventory alerts, visualizations and reports."
)

os.makedirs("outputs", exist_ok=True)
os.makedirs("reports", exist_ok=True)


old_data = load_csv("data/old_customers.csv")
products_data = load_csv("data/products.csv")

old_data = clean_data(old_data)
old_data = create_segments(old_data)
old_data = train_churn_model(old_data)
old_data = predict_purchase_value(old_data)

low_stock_data = check_low_stock(products_data)


st.sidebar.title("Navigation")

menu = st.sidebar.radio(
    "Select Page",
    [
        "Home Dashboard",
        "Data Upload & Merge",
        "Customer Segmentation",
        "Predictions",
        "Recommendation System",
        "Inventory Alerts",
        "Graphs",
        "Reports"
    ]
)

st.sidebar.header("Filters")

city = st.sidebar.selectbox(
    "Select City",
    ["All"] + sorted(old_data["city"].dropna().unique().tolist())
)

gender = st.sidebar.selectbox(
    "Select Gender",
    ["All"] + sorted(old_data["gender"].dropna().unique().tolist())
)

category = st.sidebar.selectbox(
    "Select Category",
    ["All"] + sorted(old_data["category"].dropna().unique().tolist())
)

filtered_data = apply_filters(
    old_data,
    city,
    gender,
    category
)


if menu == "Home Dashboard":

    st.header("🏠 Business Overview")

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", len(filtered_data))
    col2.metric("Total Revenue", f"₹{filtered_data['total_spent'].sum():,.0f}")

    if filtered_data.empty:
        col3.metric("Average Spending", "₹0")
    else:
        col3.metric("Average Spending", f"₹{filtered_data['total_spent'].mean():,.0f}")

    col4.metric("Low Stock Products", len(low_stock_data))

    st.write("Filtered Records:", len(filtered_data))

    if filtered_data.empty:
        st.warning("No customers found for selected filters.")
    else:
        st.subheader("Home Visualizations")

        col5, col6 = st.columns(2)

        with col5:
            st.plotly_chart(city_bar_chart(filtered_data), use_container_width=True)

        with col6:
            st.plotly_chart(gender_pie_chart(filtered_data), use_container_width=True)

        st.subheader("Customer Data")
        st.dataframe(filtered_data, use_container_width=True)

    if len(low_stock_data) > 0:
        st.warning("⚠️ Some products are low in stock.")


elif menu == "Data Upload & Merge":

    st.header("📂 Old Data + New Data Merge")

    st.subheader("Old Customer Data")
    st.write(f"Old Data Records: {len(old_data)}")
    st.dataframe(old_data, use_container_width=True)

    uploaded_file = st.file_uploader(
        "Upload New Customer CSV File",
        type=["csv"]
    )

    if uploaded_file is not None:

        new_data = pd.read_csv(uploaded_file)

        st.subheader("New Uploaded Data")
        st.dataframe(new_data, use_container_width=True)

        updated_data = merge_old_new_data(old_data, new_data)
        updated_data = clean_data(updated_data)
        updated_data = create_segments(updated_data)
        updated_data = train_churn_model(updated_data)
        updated_data = predict_purchase_value(updated_data)

        save_csv(updated_data, "outputs/updated_dataset.csv")

        st.success("✅ Old and new data merged successfully")

        st.subheader("Updated Customer Data")
        st.write(f"Updated Total Records: {len(updated_data)}")
        st.dataframe(updated_data, use_container_width=True)

        st.subheader("Updated Data Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(city_bar_chart(updated_data), use_container_width=True)

        with col2:
            st.plotly_chart(category_pie_chart(updated_data), use_container_width=True)

        csv = updated_data.to_csv(index=False).encode("utf-8")

        st.download_button(
            "Download Updated Dataset",
            data=csv,
            file_name="updated_customers.csv",
            mime="text/csv"
        )

    else:
        st.info("Upload new customer CSV file to merge with old 100 customer records.")


elif menu == "Customer Segmentation":

    st.header("👥 Customer Segmentation")

    if filtered_data.empty:
        st.warning("No customers found for selected filters.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(customer_segment_bar_chart(filtered_data), use_container_width=True)

        with col2:
            st.plotly_chart(customer_segment_pie_chart(filtered_data), use_container_width=True)

        st.subheader("K-Means 3D Visualization")
        st.plotly_chart(kmeans_3d_chart(filtered_data), use_container_width=True)

        st.subheader("Segmented Customer Data")
        st.dataframe(filtered_data, use_container_width=True)


elif menu == "Predictions":

    st.header("🤖 AI Predictions")

    st.subheader("Amount Based Product Prediction")

    amount = st.number_input(
        "Enter Purchase Amount",
        min_value=0,
        value=1000,
        step=500
    )

    if st.button("Predict Products"):

        result = get_products_by_amount(amount)

        st.success(f"Eligibility: {result['eligibility']}")

        if result["products"]:
            st.subheader("Products Available for This Amount")

            for product in result["products"]:
                st.success(product)
        else:
            st.error("No products available for this amount.")

    if filtered_data.empty:
        st.warning("No customers found for selected filters.")
    else:
        st.subheader("Churn Prediction Table")

        churn_view = filtered_data[
            [
                "customer_id",
                "name",
                "gender",
                "city",
                "category",
                "total_spent",
                "purchase_count",
                "last_purchase_days",
                "churn_prediction"
            ]
        ]

        st.dataframe(churn_view, use_container_width=True)

        st.subheader("Purchase Value Prediction Table")

        purchase_view = filtered_data[
            [
                "customer_id",
                "name",
                "gender",
                "city",
                "category",
                "total_spent",
                "predicted_purchase"
            ]
        ]

        st.dataframe(purchase_view, use_container_width=True)

        st.subheader("Prediction Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(churn_bar_chart(filtered_data), use_container_width=True)

        with col2:
            st.plotly_chart(purchase_prediction_bar_chart(filtered_data), use_container_width=True)


elif menu == "Recommendation System":

    st.header("🎯 Product Recommendation System")

    if filtered_data.empty:
        st.warning("No customers found for selected filters.")
    else:
        customer_id = st.selectbox(
            "Select Customer ID",
            filtered_data["customer_id"].tolist()
        )

        selected_customer = filtered_data[
            filtered_data["customer_id"] == customer_id
        ]

        st.subheader("Selected Customer Details")
        st.dataframe(selected_customer, use_container_width=True)

        recommendations = recommend_products(
            filtered_data,
            customer_id
        )

        st.subheader("Recommended Products")

        if recommendations:
            for product in recommendations:
                st.success(product)
        else:
            st.warning("No recommendations found.")

        st.subheader("Recommendation Visualizations")

        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(category_bar_chart(filtered_data), use_container_width=True)

        with col2:
            st.plotly_chart(gender_pie_chart(filtered_data), use_container_width=True)


elif menu == "Inventory Alerts":

    st.header("📦 Inventory Stock Alerts")

    st.subheader("All Product Stock")
    st.dataframe(products_data, use_container_width=True)

    st.subheader("Inventory Visualizations")

    st.plotly_chart(stock_bar_chart(products_data), use_container_width=True)

    st.subheader("Low Stock Products")

    if len(low_stock_data) > 0:

        st.error("⚠️ Low stock products found")
        st.dataframe(low_stock_data, use_container_width=True)

        st.plotly_chart(low_stock_pie_chart(low_stock_data), use_container_width=True)

        for index, row in low_stock_data.iterrows():
            st.warning(
                f"Restock Alert: {row['product_name']} has only "
                f"{row['current_stock']} items left. "
                f"Minimum required stock is {row['min_stock']}."
            )

    else:
        st.success("✅ All products have enough stock.")


elif menu == "Graphs":

    st.header("📈 All Business Visualizations")

    if filtered_data.empty:
        st.warning("No customers found for selected filters.")
    else:
        col1, col2 = st.columns(2)

        with col1:
            st.plotly_chart(customer_segment_bar_chart(filtered_data), use_container_width=True)

        with col2:
            st.plotly_chart(customer_segment_pie_chart(filtered_data), use_container_width=True)

        col3, col4 = st.columns(2)

        with col3:
            st.plotly_chart(category_bar_chart(filtered_data), use_container_width=True)

        with col4:
            st.plotly_chart(category_pie_chart(filtered_data), use_container_width=True)

        col5, col6 = st.columns(2)

        with col5:
            st.plotly_chart(gender_bar_chart(filtered_data), use_container_width=True)

        with col6:
            st.plotly_chart(city_bar_chart(filtered_data), use_container_width=True)

        st.plotly_chart(age_spending_scatter(filtered_data), use_container_width=True)

        st.subheader("K-Means 3D Visualization")
        st.plotly_chart(kmeans_3d_chart(filtered_data), use_container_width=True)

        st.subheader("Inventory Stock Graph")
        st.plotly_chart(stock_bar_chart(products_data), use_container_width=True)


elif menu == "Reports":

    st.header("📄 Reports")

    total_customers = len(filtered_data)
    total_revenue = filtered_data["total_spent"].sum()
    low_stock_count = len(low_stock_data)

    col1, col2, col3 = st.columns(3)

    col1.metric("Filtered Customers", total_customers)
    col2.metric("Filtered Revenue", f"₹{total_revenue:,.0f}")
    col3.metric("Low Stock Products", low_stock_count)

    if not filtered_data.empty:
        st.subheader("Report Visualizations")

        col4, col5 = st.columns(2)

        with col4:
            st.plotly_chart(category_pie_chart(filtered_data), use_container_width=True)

        with col5:
            st.plotly_chart(customer_segment_bar_chart(filtered_data), use_container_width=True)

    if st.button("Generate PDF Report"):

        report_path = generate_report(
            total_customers,
            total_revenue,
            low_stock_count
        )

        st.success("✅ PDF Report Generated Successfully")

        with open(report_path, "rb") as file:
            st.download_button(
                "Download PDF Report",
                data=file,
                file_name="customer_report.pdf",
                mime="application/pdf"
            )