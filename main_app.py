import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import datetime
from datetime import timedelta
import plotly.figure_factory as ff

st.set_page_config(layout="wide")
st.title('Hotel Sadhabishegam Trend Analyzer')


def get_df(df_path):
   
   df=pd.read_csv(df_path)
   df['review_date']=pd.to_datetime(df['review_date']).dt.date
   df=df.sort_values('review_date',ascending=False).reset_index(drop=True)
   
   return df


def filter_time_df(df,previous_n_days_lm,previous_n_days_ul):
   previous_n_days_ul = datetime.date.today() - timedelta(days = previous_n_days_ul)
   previous_n_days_lm = datetime.date.today() - timedelta(days = previous_n_days_lm)
   df=df[(df['review_date']<previous_n_days_ul) & (df['review_date']>previous_n_days_lm)].sort_values('review_date')
   return df

def process_df(df,):
   # df=filter_time_df(df,previous_n_days=previous_n_days,type=type)
   
   df=df.groupby(['review_date']).agg({'review_rating':['mean','count']}).reset_index()
   df.columns = ["_".join(pair) for pair in df.columns]
   df=df.rename({'review_date_':'review_date','review_rating_mean':'avg_rating','review_rating_count':'num_reviews'},axis='columns')
   
   return df

def resample_df_date(df,by):
   df=pd.DataFrame()
   df['review_rating'] = temp_df_time_filtered['review_rating']
   df.index=pd.to_datetime(pd.to_datetime(temp_df_time_filtered['review_date']).dt.date)
   # df=pd.DataFrame(df['review_rating'].resample('W').mean()).reset_index()
   df=pd.DataFrame(df.resample(by).agg({'review_rating':['mean','count']})).reset_index(col_level=1).droplevel(0,axis=1)
   df=df[df['mean'].notna()]
   df=df.rename({'mean':'avg_rating','count':'num_reviews'},axis='columns')
   df['avg_rating']=df['avg_rating'].round(2)

   return df

def plot_distplot(current_df,previous_df,previous_df_text='',current_df_text=''):
   current_df=current_df[current_df['review_rating'].notna()]
   previous_df=previous_df[previous_df['review_rating'].notna()]
   
   hist_data = [previous_df['review_rating'],current_df['review_rating']]
   group_labels = [previous_df_text,current_df_text] # name of the dataset
   fig = ff.create_distplot(hist_data, group_labels)
   # fig.update_traces(textposition="bottom right")
   st.plotly_chart(fig, use_container_width=True)

def get_percentage(num_a,num_b):
    return round(((num_a - num_b) / num_b) * 100,2)

def more_info_ratings_given(n):
         current_no=temp_df['num_reviews'].sum()
         prev_no=temp_df_2['num_reviews'].sum()
         #good
         good=len(temp_df_time_filtered[temp_df_time_filtered['review_rating']>=4])
         prev_good=len(temp_df_time_filtered_2[temp_df_time_filtered_2['review_rating']>=4])
         good_perc = round((good/len(temp_df_time_filtered)) * 100,2)
         prev_good_perc = round((prev_good/len(temp_df_time_filtered_2)) * 100,2)
         #bad
         bad=len(temp_df_time_filtered[temp_df_time_filtered['review_rating']<=2])
         prev_bad=len(temp_df_time_filtered_2[temp_df_time_filtered_2['review_rating']<=2])
         bad_perc=round((bad/len(temp_df_time_filtered)) * 100,2)
         prev_bad_perc=round((prev_bad/len(temp_df_time_filtered_2)) * 100,2)
         
         #avg
         avg=len(temp_df_time_filtered[temp_df_time_filtered['review_rating']==3])
         prev_avg=len(temp_df_time_filtered_2[temp_df_time_filtered_2['review_rating']==3])
         avg_perc=round((avg/len(temp_df_time_filtered)) * 100,2)
         prev_avg_perc=round((prev_avg/len(temp_df_time_filtered_2)) * 100,2)

         st.subheader(f'**Last {n} month(s) stats**')
         col1,col2,col3=st.columns(3)
         col1.metric('**Good Reviews**',f'{good}',)
         col2.metric('**Avg Reviews**',f'{avg}',)
         col3.metric('**Bad Reviews**',f'{bad}',)
         st.markdown(f'**Total Ratings over last {n} month(s): {current_no}**')
         st.markdown(f'**Good Percentage:{good_perc}%**')
         st.markdown(f'**Bad Percentage:{bad_perc}%**')
         st.markdown(f'**Avg Percentage:{avg_perc}%**')

         st.subheader(f'**Last to Last {n} month(s) stats**')
         col1,col2,col3=st.columns(3)
         col1.metric('**Good Reviews**',f'{prev_good}')
         col2.metric('**Avg Reviews**',f'{prev_avg}')
         col3.metric('**Bad Reviews**',f'{prev_bad}')
         st.markdown(f'**Total Ratings over last to last {n} month(s): {prev_no}**')
         st.markdown(f'**Good Percentage:{prev_good_perc}%**')
         st.markdown(f'**Bad Percentage: {prev_bad_perc}%**')
         st.markdown(f'**Avg Percentage: {prev_avg_perc}%**')
   
         

df=get_df(df_path='./sadhabishegam_reviews1.csv')
lastest_update=df['review_date'].loc[0].strftime('%d/%m/%Y')
st.markdown(f'Last update happened on {lastest_update}. Update happens every Monday,Thursday and Saturday')

col1,col2=st.columns(2)
col1.metric('Average Rating',str(df['review_rating'].mean().round(2)))
col2.metric('Total Reviews',str(len(df)))


tab1, tab2, tab3 = st.tabs(["past 4 months", "past 1 month", "past 15 months"])

with tab1:

   temp_df_time_filtered=filter_time_df(df,previous_n_days_lm=120,previous_n_days_ul=0)#current step
   temp_df_time_filtered_2=filter_time_df(df,previous_n_days_lm=120*2,previous_n_days_ul=120)#previous step
   
   temp_df = process_df(temp_df_time_filtered)
   temp_df_2= process_df(temp_df_time_filtered_2)
   weekly_df=resample_df_date(temp_df_time_filtered,by='W')
   
   col1,col2=st.columns(2)
   with col1:
      percentage_diff=get_percentage(temp_df_time_filtered['review_rating'].mean().round(2),temp_df_time_filtered_2['review_rating'].mean().round(2))
      st.metric('Average Rating',str(temp_df_time_filtered['review_rating'].mean().round(2)),f'{percentage_diff}%')
      with st.popover("More Info"):
         current_avg=temp_df_time_filtered['review_rating'].mean().round(2)
         prev_avg=temp_df_time_filtered_2['review_rating'].mean().round(2)
         st.markdown(f'Average Rating over last 4 months: {current_avg}')
         st.markdown(f'Average Rating over last to last 4 months: {prev_avg}')
         st.markdown(f'perentage increase/decrease {percentage_diff}%')
   
   with col2:
      percentage_diff=get_percentage(temp_df['num_reviews'].sum(),temp_df_2['num_reviews'].sum()) 
      st.metric('Total ratings given',str(temp_df['num_reviews'].sum()),f'{percentage_diff}%')
      with st.popover("More Info"):
          more_info_ratings_given(4)   
   
   fig = px.line(weekly_df, x="review_date", y="avg_rating",text="avg_rating",\
               title='Google Ratings over the past 4 month averaged on weekly basis',hover_data=['num_reviews'])   
   fig.update_traces(textposition="bottom right")
   st.plotly_chart(fig, use_container_width=True)
   st.write('**Rating Distribution**')
   plot_distplot(temp_df_time_filtered,temp_df_time_filtered_2,previous_df_text='last 4 months',current_df_text='last to last 4 months')
  
with tab2:
   temp_df_time_filtered=filter_time_df(df,previous_n_days_lm=30,previous_n_days_ul=0)
   temp_df_time_filtered_2=filter_time_df(df,previous_n_days_lm=30*2,previous_n_days_ul=30)
  
   temp_df = process_df(temp_df_time_filtered)
   temp_df_2= process_df(temp_df_time_filtered_2)
   daily_df=resample_df_date(temp_df_time_filtered,by='D')

   col1,col2=st.columns(2)
   with col1:
      percentage_diff=get_percentage(temp_df_time_filtered['review_rating'].mean().round(2),temp_df_time_filtered_2['review_rating'].mean().round(2))
      st.metric('Average Rating',str(temp_df_time_filtered['review_rating'].mean().round(2)),f'{percentage_diff}%')
      with st.popover("More Info"):
         current_avg=temp_df_time_filtered['review_rating'].mean().round(2)
         prev_avg=temp_df_time_filtered_2['review_rating'].mean().round(2)
         st.markdown(f'Average Rating over last 1 month: {current_avg}')
         st.markdown(f'Average Rating over last to last month: {prev_avg}')
         st.markdown(f'perentage increase/decrease {percentage_diff}%')
   
   with col2:
      percentage_diff=get_percentage(temp_df['num_reviews'].sum(),temp_df_2['num_reviews'].sum()) 
      st.metric('Total ratings given',str(temp_df['num_reviews'].sum()),f'{percentage_diff}%')
      with st.popover("More Info"):
         more_info_ratings_given(1)   
   
   
   # fig = px.line(temp_df, x="review_date", y="avg_rating", text="avg_rating",\
   #               title='Google Ratings over the past 1 month averaged on a daily basis',hover_data=['num_reviews'])
   fig = px.line(daily_df, x="review_date", y="avg_rating",text="avg_rating",\
               title='Google Ratings over the past 1 month averaged on daily basis',hover_data=['num_reviews'])
   fig.update_traces(textposition="bottom right")
   st.plotly_chart(fig, use_container_width=True)
   st.write('**Rating Distribution**')
   plot_distplot(temp_df_time_filtered,temp_df_time_filtered_2,previous_df_text='last 1 month',current_df_text='last to last 1 month')

with tab3:
   
   temp_df_time_filtered=filter_time_df(df,previous_n_days_lm=456,previous_n_days_ul=0)
   temp_df_time_filtered_2=filter_time_df(df,previous_n_days_lm=456*2,previous_n_days_ul=456)
   temp_df = process_df(temp_df_time_filtered)
   temp_df_2= process_df(temp_df_time_filtered_2)
   monthly_df=resample_df_date(temp_df_time_filtered,by='ME ')
   
   col1,col2=st.columns(2)
   with col1:
         percentage_diff=get_percentage(temp_df_time_filtered['review_rating'].mean().round(2),temp_df_time_filtered_2['review_rating'].mean().round(2))
         st.metric('Average Rating',str(temp_df_time_filtered['review_rating'].mean().round(2)),f'{percentage_diff}%')
         with st.popover("More Info"):
            current_avg=temp_df_time_filtered['review_rating'].mean().round(2)
            prev_avg=temp_df_time_filtered_2['review_rating'].mean().round(2)
            st.markdown(f'Average Rating over last 1 month: {current_avg}')
            st.markdown(f'Average Rating over last to last month: {prev_avg}')
            st.markdown(f'perentage increase/decrease {percentage_diff}%')
      
   with col2:
      percentage_diff=get_percentage(temp_df['num_reviews'].sum(),temp_df_2['num_reviews'].sum()) 
      st.metric('Total ratings given',str(temp_df['num_reviews'].sum()),f'{percentage_diff}%')
      with st.popover("More Info"):
         more_info_ratings_given(15)   
   
   fig = px.line(monthly_df, x="review_date", y="avg_rating",text="avg_rating",\
               title='Google Ratings over the past 15 month averaged on monthly basis',hover_data=['num_reviews'])
   fig.update_traces(textposition="bottom right")
   st.plotly_chart(fig, use_container_width=True)
   st.write('**Rating Distribution**')
   plot_distplot(temp_df_time_filtered,temp_df_time_filtered_2,previous_df_text='last 15 months',current_df_text='last to last 15 months')
