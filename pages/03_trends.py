import streamlit as st
import dhlab.text as dh
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image
import urllib


@st.cache(suppress_st_warning=True, show_spinner = False)
def make_crps():
    urns = pd.read_csv('norske_aviser.csv', index_col = 0)
    return dh.CorpusFromIdentifiers(list(urns.urn.values))


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')


st.title('Fordeling av ord over år i norsk-amerikanske aviser')

corpus = make_crps()
search = st.text_input('Finn trender for ord, enkeltord skilt med komma', "", help="Kommaseparert liste med ord, ingen trunkering")
searchlist = [x.strip() for x in search.split(',')]

if not search == "":
    trends = dh.Counts(corpus = corpus, words=searchlist)
    df = pd.merge(trends.counts.transpose(), corpus.corpus.set_index('urn')[["year"]], left_index=True, right_index=True)
    df["year"] = pd.to_datetime(df.year, format="%Y")
    #st.dataframe(trends.counts.transpose())
    #st.dataframe(df)
    st.bar_chart(df.groupby('year').sum())
                             
                
                