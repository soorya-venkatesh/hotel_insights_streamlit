import streamlit as st
import pandas as pd
df=pd.read_csv('test.csv')

st.write(df)