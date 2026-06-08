from sklearn.linear_model import LinearRegression


def predict_purchase_value(df):

    X = df[
        [
            "age",
            "purchase_count",
            "last_purchase_days"
        ]
    ]

    y = df["total_spent"]

    model = LinearRegression()

    model.fit(X, y)

    df["predicted_purchase"] = model.predict(X)

    return df


def get_products_by_amount(amount):

    if amount >= 30000:
        return {
            "eligibility": "Premium Customer",
            "products": [
                "Laptop",
                "Smart Watch",
                "Jewellery",
                "Headphones"
            ]
        }

    elif amount >= 15000:
        return {
            "eligibility": "Regular Customer",
            "products": [
                "Smart Watch",
                "Shoes",
                "Handbag",
                "Keyboard"
            ]
        }

    elif amount >= 5000:
        return {
            "eligibility": "Basic Customer",
            "products": [
                "Face Cream",
                "Shampoo",
                "T-Shirt",
                "Rice Bag"
            ]
        }

    else:
        return {
            "eligibility": "Not Eligible",
            "products": []
        }