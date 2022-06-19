# -*- coding: utf-8 -*-
import streamlit as st
import dhlab.text as dh
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image
import urllib
import streamlit as st
import dhlab.text as dh
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image
import urllib


@st.cache(suppress_st_warning=True, show_spinner = False)
def make_corpus():
    urns = pd.read_csv('norske_aviser.csv', index_col = 0)
    #corpus = dh.CorpusFromIdentifiers(list(urns.urn.values))
    return urns #corpus


st.title('Oversikt over korpuset')

corpus = make_corpus()

counts = corpus.groupby("title").count().sort_values(by='year', ascending = False)[["urn"]]
counts.columns = ['counts']
rows = []
for title in counts.index:
    rows.append(
        [
            title,
            counts.loc[title].values[0],
            int(corpus[corpus.title == title]['year'].min()),
            int(corpus[corpus.title == title]['year'].max())
        ]
    )

st.markdown("### Korpus med antall utgaver, samt første og siste utgivelsesår")
st.dataframe(pd.DataFrame(rows, columns = ['avistittel', 'antall', 'fra', 'til']))


st.markdown("### Velg en avis for å se fordeling av utgaver over år")

yearcounts = corpus.groupby(["title", "year"]).count()[['urn']]
yearcounts = yearcounts.reset_index(level = 1)
yearcounts.columns = ['år', 'antall']
yearcounts['år'] = yearcounts['år'].astype('int')

choose = st.selectbox("Velg en avis for å se fordeling", set(yearcounts[yearcounts.antall > 1].index))
st.bar_chart(yearcounts.loc[choose].set_index('år'))