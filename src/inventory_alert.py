def check_low_stock(products_df):

    low_stock = products_df[
        products_df["current_stock"]
        <=
        products_df["min_stock"]
    ]

    return low_stock