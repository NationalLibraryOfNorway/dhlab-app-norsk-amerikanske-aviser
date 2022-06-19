import streamlit as st
from PIL import Image
import urllib

image = Image.open('NB-logo-no-eng-svart.png')
st.image(image, width = 200)
st.markdown('Les om [Digital Humaniora - DH](https://nb.no/dh-lab) ved Nasjonalbiblioteket')

st.title("Korpus over norsk-amerikanske aviser")
st.markdown("Velg en undersøkelse fra menyen til venstre")
                
                