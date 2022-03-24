import streamlit as st
import dhlab.text as dh
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image
import urllib

@st.cache(suppress_st_warning=True, show_spinner = False)
def sumword(NGRAM, words = None, ddk = None, topic = None, period = None, lang = None, title = None):
    wordlist =   [x.strip() for x in words.split(',')]
    # check if trailing comma, or comma in succession, if so count comma in
    if '' in wordlist:
        wordlist = [','] + [y for y in wordlist if y != '']
    ref = NGRAM(wordlist, ddk = ddk, topic = topic, period = period, lang = lang, title = title).sum(axis = 1)
    ref.columns = 'tot'
    return ref


@st.cache(suppress_st_warning=True, show_spinner = False)
def ngram(NGRAM, word = None, ddk = None, subject = None, period = None, lang = None, title = None):
    res = NGRAM(word, ddk = ddk, topic = subject, period = period, lang = lang, title = title)
    res = res.rolling(window = smooth_slider).mean()
    res.index = pd.to_datetime(res.index, format='%Y')
    return res

@st.cache(suppress_st_warning=True, show_spinner = False)
def make_corpus():
    urns = pd.read_csv('norske_aviser.csv', index_col = 0)
    corpus = dh.CorpusFromIdentifiers(list(urns.urn.values))
    return corpus

@st.cache(suppress_st_warning=True, show_spinner = False)
def konk(corpus = None, query = None): 
    conc = dh.Concordance(corpus, query, limit = 10000)
    return conc

def show_konks(conc, query):
    conc['link'] = conc['urn'].apply(lambda c: f"[{c.split('_')[2]}](https://www.nb.no/items/{c})")
    conc['date'] = conc['urn'].apply(lambda c: f"{c.split('_')[2][:4]}")
    conc['conc'] = conc['conc'].apply(lambda c: c.replace('<b>', '**').replace('</b>','**'))
    return conc[['link','date','conc']].sort_values(by = 'date')

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les mer på [DHLAB-siden](https://nbviewer.jupyter.org/github/DH-LAB-NB/DHLAB/blob/master/DHLAB_ved_Nasjonalbiblioteket.ipynb)')


st.title('Søk i norsk-amerikanske aviser')

corpus = make_corpus()
search = st.text_input('Søkeuttrykk', "")
#st.write(search)
#st.write(corpus.corpus.head(5))
#konks = konk(corpus = corpus, query = search)
konks = api.concordance(urns=list(corpus.corpus.urn.values), words=search, limit = 100)
st.markdown('\n\n'.join([' '.join([str(y) for y in x]) for x in show_konks(konks, search).itertuples()]))