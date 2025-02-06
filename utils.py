import pandas as pd
import streamlit as st

@st.cache_data
def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """
    `pd.read_csv(filepath: str, **kwargs, iterator=False)` wrapper for caching data using `@st.cache_data`.
    """
    return pd.read_csv(filepath, **kwargs, iterator=False)

