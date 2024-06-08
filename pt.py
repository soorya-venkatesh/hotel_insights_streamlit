import streamlit as st
import pandas as pd
import random
df=pd.read_csv('./test.csv')
df.loc[len(df.index)] = ['ahem',random.random()]
df.to_csv('test.csv',index=False)
print(df)

