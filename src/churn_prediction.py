from sklearn.ensemble import RandomForestClassifier

def train_churn_model(df):

    X = df[
        [
            "age",
            "total_spent",
            "purchase_count",
            "last_purchase_days"
        ]
    ]

    y = df["churn"]

    model = RandomForestClassifier()

    model.fit(X, y)

    df["churn_prediction"] = model.predict(X)

    return df