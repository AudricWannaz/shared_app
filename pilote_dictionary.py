import streamlit as st
from greek_accentuation.characters import *
import pandas as pd
import ast


if 'df' not in st.session_state:
	dfs = []
	for i in range(0,4):
		tdf = pd.read_parquet(f'data/tmWordsSingles_chunk_{i}.parquet')
		dfs.append(tdf)
	df = pd.concat(dfs,axis=0)	
	st.session_state['df'] = df

df = st.session_state['df']


df_abb = df[df.diplomatic.str.contains('\(')]
with st.expander('SHOW ABBREVIATIONS ONLY'):
	st.write(df_abb)

target_lemma = st.text_input('enter exact lemma: ', 'διά')
target = singles[singles.lemmatized == target_lemma]

st.title('EXPLORE TARGET WORD')
st.write(target)

for el in target.columns:
	try:
		st.header(f'typical {el} of {target_lemma}')
		st.write(target.groupby(by='lemmatized')[el].apply(pd.value_counts))
		st.write(target.groupby(by='lemmatized')[el].apply(pd.value_counts,normalize=True))
	except:
		pass

st.write('CREDITS: raw data from A.Keersmaekers https://github.com/alekkeersmaekers/duke-nlp, snippets for online version by André Walsøe, everything else from Audric-Charles Wannaz, March 2023')

