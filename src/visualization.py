import plotly.express as px


def customer_segment_bar_chart(df):
    return px.bar(
        df,
        x="segment_name",
        title="Customer Segments Bar Chart",
        color="segment_name"
    )


def customer_segment_pie_chart(df):
    return px.pie(
        df,
        names="segment_name",
        title="Customer Segments Pie Chart"
    )


def gender_bar_chart(df):
    return px.bar(
        df,
        x="gender",
        title="Gender Wise Customers",
        color="gender"
    )


def gender_pie_chart(df):
    return px.pie(
        df,
        names="gender",
        title="Gender Distribution"
    )


def city_bar_chart(df):
    return px.bar(
        df,
        x="city",
        title="City Wise Customers",
        color="city"
    )


def category_bar_chart(df):
    return px.bar(
        df,
        x="category",
        y="total_spent",
        title="Category Wise Revenue",
        color="category"
    )


def category_pie_chart(df):
    return px.pie(
        df,
        names="category",
        values="total_spent",
        title="Category Revenue Share"
    )


def age_spending_scatter(df):
    return px.scatter(
        df,
        x="age",
        y="total_spent",
        color="gender",
        title="Age vs Spending"
    )


def churn_bar_chart(df):
    return px.bar(
        df,
        x="churn_prediction",
        title="Churn Prediction Count",
        color="churn_prediction"
    )


def purchase_prediction_bar_chart(df):
    return px.bar(
        df,
        x="name",
        y="predicted_purchase",
        title="Predicted Purchase Value",
        color="gender"
    )


def kmeans_3d_chart(df):
    return px.scatter_3d(
        df,
        x="age",
        y="total_spent",
        z="purchase_count",
        color="segment_name",
        hover_name="name",
        title="K-Means 3D Customer Segmentation"
    )


def stock_bar_chart(products_df):
    return px.bar(
        products_df,
        x="product_name",
        y="current_stock",
        title="Product Stock Levels",
        color="category"
    )


def low_stock_pie_chart(low_stock_df):
    return px.pie(
        low_stock_df,
        names="product_name",
        values="current_stock",
        title="Low Stock Product Share"
    )