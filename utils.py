import pandas as pd
import streamlit as st
import dhlab.text as dh
from dhlab.text.utils import urnlist

@st.cache_data
def load_csv(filepath: str, **kwargs) -> pd.DataFrame:
    """
    `pd.read_csv(filepath: str, **kwargs, iterator=False)` wrapper for caching data using `@st.cache_data`.
    """
    return pd.read_csv(filepath, **kwargs, iterator=False)

@st.cache_data
def load_norske_aviser():
    """
    Loads `./norske_aviser.csv`
    """
    return load_csv('norske_aviser.csv', index_col=0)

@st.cache_data
def _make_corpus(urns: list) -> dh.Corpus:
    """For caching"""
    corpus = dh.Corpus()
    corpus.extend_from_identifiers(urns)
    return corpus

def make_corpus(urns: list | pd.DataFrame | pd.Series | dh.Corpus) -> dh.Corpus:
    """
    Creates corpus from urns
    """
    urns = urnlist(urns) # Generate urnlist manually for caching
    return _make_corpus(urns)
