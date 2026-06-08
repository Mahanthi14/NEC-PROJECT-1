def apply_filters(
    df,
    city,
    gender,
    category
):

    filtered_df = df.copy()

    # Remove extra spaces
    filtered_df["city"] = filtered_df["city"].astype(str).str.strip()
    filtered_df["gender"] = filtered_df["gender"].astype(str).str.strip()
    filtered_df["category"] = filtered_df["category"].astype(str).str.strip()

    # City Filter
    if city != "All":
        filtered_df = filtered_df[
            filtered_df["city"].str.lower() == city.strip().lower()
        ]

    # Gender Filter
    if gender != "All":
        filtered_df = filtered_df[
            filtered_df["gender"].str.lower() == gender.strip().lower()
        ]

    # Category Filter
    if category != "All":
        filtered_df = filtered_df[
            filtered_df["category"].str.lower() == category.strip().lower()
        ]

    return filtered_df