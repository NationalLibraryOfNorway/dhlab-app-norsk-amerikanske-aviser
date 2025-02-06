import streamlit as st
import dhlab.text as dh
import pandas as pd
from PIL import Image

import utils


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')


st.title('Fordeling av ord over år i norsk-amerikanske aviser')

aviser = utils.load_norske_aviser()
corpus = utils.make_corpus(aviser)

search = st.text_input('Finn trender for ord, enkeltord skilt med komma', "", help="Kommaseparert liste med ord, ingen trunkering")
searchlist = [x.strip() for x in search.split(',')]

if not search == "":
    # NB: /urn_frequencies and /frequencies return dhlabids, not urns
    trends = dh.Counts(corpus = corpus, words=searchlist)
    df = pd.merge(trends.counts.transpose(), corpus.corpus.set_index('dhlabid')[["year"]], left_index=True, right_index=True)
    df["year"] = pd.to_datetime(df.year, format="%Y")
    st.bar_chart(df.groupby('year').sum())
                             
                
                
