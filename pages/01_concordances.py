import streamlit as st
import dhlab.api.dhlab_api as api
import pandas as pd
from PIL import Image

import utils


def show_konks(conc, query):
    conc['link'] = conc['urn'].apply(lambda c: f"[{c.split('_')[2]}](https://www.nb.no/items/{c})")
    conc['date'] = conc['urn'].apply(lambda c: f"{c.split('_')[5][:4]}")
    conc['conc'] = conc['conc'].apply(lambda c: c.replace('<b>', '**').replace('</b>','**'))
    return conc[['link','date','conc']].sort_values(by = 'date')


image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')


st.title('Søk i norsk-amerikanske aviser')

corpus = utils.load_norske_aviser()
search = st.text_input('Søkeuttrykk', "", help="Bruk trunkerte uttrykk som nordm*")
samplesize = int(st.number_input("Maks antall konkordanser:", min_value=5, value=100, help="Minste verdi er 5, default er 100"))

if not search == "":
    konks = api.concordance(urns=list(corpus.urn.values), words=search, limit = 5000)
    
    if (samplesize < len(konks)):
        konkordanser = '\n\n'.join(
        [' '.join([str(y) for y in x]) for x in 
         show_konks(konks.sample(min(int(samplesize), len(konks))), search).itertuples()])
       
        if st.button(f"Klikk her for flere konkordanser. Sampler {samplesize} av {len(konks)}"):
            konkordanser = '\n\n'.join(
        [' '.join([str(y) for y in x]) for x in 
         show_konks(konks.sample(min(int(samplesize), len(konks))), search).itertuples()])
       
            
    else:
        if len(konks) == 0:
            st.write(f"Ingen treff")
            konkordanser = "-- ingen --"
        else:
            st.write(f"Viser alle {len(konks)} konkordansene ")
            konkordanser = '\n\n'.join(
        [' '.join([str(y) for y in x]) for x in 
         show_konks(konks.sample(min(int(samplesize), len(konks))), search).itertuples()]
            )
    
    st.markdown(konkordanser)
                             
                
                
