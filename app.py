import streamlit as st
st.set_page_config(layout="wide")
from greek_accentuation.characters import *
import pandas as pd
import ast
pd.options.plotting.backend = "plotly"
import plotly.express as px
import plotly.graph_objects as go
from src.visualizations import create_histograms, create_barplot, create_pie_chart, create_3d_bar_plot

@st.experimental_memo
def load_tmwords_data():
	dfs = []
	for i in range(0,5):
		tdf = pd.read_parquet(f'data/tmWordsSingles_chunk_{i}.parquet')
		dfs.append(tdf)
	df = pd.concat(dfs,axis=0)	
	return df
df = load_tmwords_data()

df_abb = df[df.diplomatic.str.contains('\(')]


with st.expander('Show visualizations'):
	st.plotly_chart(create_histograms(df, df_abb, 'period_min', 'Frequencies of words vs abbreviations over time'))
	st.plotly_chart(create_barplot(df,df_abb))

	st.header("Abbreviation Type")
	st.plotly_chart(create_pie_chart(df_abb['abbr_type'].value_counts(), 'Pie chart of abbreviation type percentages - abbreviated'))
	st.plotly_chart(create_3d_bar_plot(df_abb.groupby(['abbr_type', 'period']).size().reset_index(name='count'), 'period', 'count', 'abbr_type', 'abbr_type over time'))
	
	st.header("Genre distribution")
	st.plotly_chart(create_pie_chart(df_abb['genre'].value_counts(), 'Pie chart of genre percentages - abbreviated'))
	st.plotly_chart(create_pie_chart(df['genre'].value_counts(), 'Pie chart of genre percentages - non-abbreviated and abbreviated'))


	st.header("State")
	st.plotly_chart(create_pie_chart(df_abb['state'].value_counts(), 'Pie chart of state percentages - abbreviated'))
	st.plotly_chart(create_pie_chart(df['state'].value_counts(), 'Pie chart of state percentages - non-abbreviated and abbreviated'))
	st.header("Gender distribution")
	st.plotly_chart(create_pie_chart(df_abb['gender'].value_counts(), 'Pie chart of gender percentages - abbreviated'))
	st.plotly_chart(create_pie_chart(df['gender'].value_counts(), 'Pie chart of gender percentages - non-abbreviated and abbreviated'))
with st.expander('SHOW ABBREVIATIONS ONLY'):
	st.dataframe(df_abb)

target_lemma = st.text_input('enter exact lemma: ', 'διά')
target = df[df.lemmatized == target_lemma]

st.title('EXPLORE TARGET WORD')
st.write(target)

for el in target.columns:
	try:

		st.header(f'typical {el} of {target_lemma}')
		col1, col2 = st.columns(2)
		# with col1:
		col1.write(target.groupby(by='lemmatized')[el].apply(pd.value_counts))
		col1.write(target.groupby(by='lemmatized')[el].apply(pd.value_counts,normalize=True))
		if el == 'gender':
			col2.write(target.groupby(by='lemmatized')[el].value_counts().unstack(fill_value=0))#.value_counts()
		# with col2:
		# 	st.write("test")
		#st.plotly_chart(create_pie_chart(target.groupby(by='lemmatized')[el].apply(pd.value_counts)))
		#st.plotly_chart(create_pie_chart(target.groupby(by='lemmatized')[el].apply(pd.value_counts,normalize=True)))

	except:
		pass

st.write('CREDITS: raw data from A.Keersmaekers https://github.com/alekkeersmaekers/duke-nlp, snippets for online version by André Walsøe, everything else from Audric-Charles Wannaz, March 2023')

