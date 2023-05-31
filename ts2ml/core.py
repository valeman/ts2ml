# AUTOGENERATED! DO NOT EDIT! File to edit: ../nbs/00_core.ipynb.

# %% auto 0
__all__ = ['add_missing_slots']

# %% ../nbs/00_core.ipynb 3
import pandas as pd
from tqdm import tqdm
from typing import List, Optional

# %% ../nbs/00_core.ipynb 4
def add_missing_slots(
        df: pd.DataFrame,    # input dataframe with datetime, entity and value columns - time series format
        datetime_col: str,   # name of the datetime column
        entity_col: str,     # name of the entity column. If a time series is associated to a location, this column will be 'location_id'
        value_col: str,      # name of the value column
        freq: str='H',       # frequency of the time series. Default is hourly
        fill_value: int = 0  # value to use to fill missing slots
) -> pd.DataFrame:
    """
    Add missing slots to a time series dataframe.
    This function is useful to fill missing slots in a time series dataframe.
    For example, if a time series is associated to a location, this function will add missing slots for each location.
    Missing slots are filled with the value specified in the 'fill_value' parameter.
    By default, the frequency of the time series is hourly.
    """

    entity_ids = df[entity_col].unique()
    all_hours = pd.date_range(start=df[datetime_col].min(), end=df[datetime_col].max(), freq=freq)

    output = pd.DataFrame()

    for entity_id in tqdm(entity_ids):

        # keep only rides for this 'location_id'
        df_entity_id = df.loc[df[entity_col] == entity_id, [datetime_col, value_col]]

        # quick way to add missing dates with 0 in a Series
        # taken from https://stackoverflow.com/a/19324591
        df_entity_id.set_index(datetime_col, inplace=True)
        df_entity_id.index = pd.DatetimeIndex(df_entity_id.index)
        df_entity_id = df_entity_id.reindex(all_hours, fill_value=0)

        # add back 'location_id' column
        df_entity_id[entity_col] = entity_id

        output = pd.concat([output, df_entity_id])

    # move the purchase_day from index to column
    output = output.reset_index().rename(columns={'index': datetime_col})
    output = output[[datetime_col, entity_col, value_col]].copy()

    return output
