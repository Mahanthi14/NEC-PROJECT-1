def recommend_products(df, customer_id):

    customer = df[df["customer_id"] == customer_id]

    if customer.empty:
        return []

    gender = customer.iloc[0]["gender"]

    female_products = [
        "Face Cream",
        "Shampoo",
        "Lipstick",
        "Saree",
        "Kurti",
        "Handbag",
        "Jewellery"
    ]

    male_products = [
        "Headphones",
        "Smart Watch",
        "Keyboard",
        "T-Shirt",
        "Shoes",
        "Wallet",
        "Trimmer"
    ]

    if gender.lower() == "female":
        return female_products

    elif gender.lower() == "male":
        return male_products

    return []