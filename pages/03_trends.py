import streamlit as st
from PIL import Image


@st.cache_data()
def make_corpus():
    import dhlab.text as dh
    import pandas as pd
    df = pd.read_csv('norske_aviser.csv', index_col = 0)
    urns = df['urn'].tolist()
    corp = dh.Corpus()
    corp.extend_from_identifiers(urns)
    return corp

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')


st.title('Fordeling av ord over år i norsk-amerikanske aviser')

search = st.text_input('Finn trender for ord, enkeltord skilt med komma', "", help="Kommaseparert liste med ord, ingen trunkering")
searchlist = [x.strip() for x in search.split(',')]

corpus = make_corpus()

import pandas as _

if not search == "":
    import dhlab.text as dh
    import pandas as pd
    # NB: /urn_frequencies and /frequencies return dhlabids, not urns
    trends = dh.Counts(corpus = corpus, words=searchlist)
    df = pd.merge(trends.counts.transpose(), corpus.corpus.set_index('dhlabid')[["year"]], left_index=True, right_index=True)
    df["year"] = pd.to_datetime(df.year, format="%Y")
    st.bar_chart(df.groupby('year').sum())
                             
                
                
