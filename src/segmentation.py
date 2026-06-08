from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler


def create_segments(df):

    df = df.copy()

    features = df[
        [
            "age",
            "total_spent",
            "purchase_count",
            "last_purchase_days"
        ]
    ]

    scaler = StandardScaler()
    scaled_features = scaler.fit_transform(features)

    model = KMeans(
        n_clusters=4,
        random_state=42,
        n_init=10
    )

    df["segment"] = model.fit_predict(scaled_features)

    segment_names = {
        0: "Regular Customer",
        1: "High Value Customer",
        2: "At Risk Customer",
        3: "New Customer"
    }

    df["segment_name"] = df["segment"].map(segment_names)

    return df