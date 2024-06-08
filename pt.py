import streamlit as st
import pandas as pd
import random
import os

try:
    value=os.environ['TEST_SECRET']
except:
    value='key not there'

df=pd.read_csv('./test.csv')
df.loc[len(df.index)] = [value,random.random()]
df.to_csv('test.csv',index=False)
print(df)

