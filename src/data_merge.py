import pandas as pd

def merge_old_new_data(old_data, new_data):
    merged_data = pd.concat(
        [old_data, new_data],
        ignore_index=True
    )

    merged_data = merged_data.drop_duplicates(
        subset="customer_id",
        keep="last"
    )

    return merged_data