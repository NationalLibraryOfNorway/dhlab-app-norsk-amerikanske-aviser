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

@st.cache(suppress_st_warning=True, show_spinner = False)
def aggregate(corpus):
    yearcounts = corpus.groupby(["title", "year"]).count()[['urn']]
    yearcounts = yearcounts.reset_index(level = 1)
    yearcounts.columns = ['år', 'antall']
    yearcounts['år'] = yearcounts['år'].astype('int')
    return yearcounts

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

st.markdown("### Korpuset vist med antall utgaver samt første og siste utgivelsesår\nklikk på kolonnens tittel for å endre sortering")
st.dataframe(pd.DataFrame(rows, columns = ['Tittel', 'Antall', 'Fra', 'Til']))


st.markdown("### Fordeling av utgaver over år for en avis")

yearcounts = aggregate(corpus)

choose = st.selectbox("Velg en avis - skriv eller klikk", set(yearcounts[yearcounts.antall > 1].index))
st.bar_chart(yearcounts.loc[choose].set_index('år'))