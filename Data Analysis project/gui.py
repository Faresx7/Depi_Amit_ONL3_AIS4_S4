import pandas as pd
import numpy as np
import plotly.express as px
import streamlit as st
from plotly.subplots import make_subplots

st.set_page_config(page_title="Ultra Marathons Dashboard", layout="wide")

# -------------------
# Load & Clean Data
# -------------------
data = pd.read_csv('data analysis project/small_file.csv')
data.columns = data.columns.str.replace(' ', '_')
data = data.dropna(subset=['Athlete_year_of_birth'])

# Age fix
data['Age'] = data['Year_of_event'] - data['Athlete_year_of_birth']
condition = data['Athlete_year_of_birth'] > data['Year_of_event']
data.loc[condition, ['Athlete_year_of_birth','Year_of_event']] = data.loc[condition, ['Year_of_event','Athlete_year_of_birth']].values
data['Age'] = data['Year_of_event'] - data['Athlete_year_of_birth']
data = data[(data['Age'] >= 12) & (data['Age'] <= 75)]

# Gender encoding
data = data.drop(data[data['Athlete_gender']=='X'].index)
data['Athlete_gender'] = data['Athlete_gender'].replace({'F':0,'M':1}).astype(int)

# Distance clean
data['Event_distance/length'] = np.where(
    data['Event_distance/length'].str.contains('mi', na=False),
    data['Event_distance/length'].str.extract(r'(\d+)').astype(float)[0] * 1.6,
    data['Event_distance/length']
)
data = data[~data['Event_distance/length'].str.contains('h', na=False)]
data['Event_distance/length'] = data['Event_distance/length'].str.split(r'[^0-9\.]').str.get(0).astype(float)

# -------------------
# Pre-computed Datasets
# -------------------
p80_22=data[(data['Year_of_event']>=1980) & (data['Year_of_event']<=2022)]
p80_90=data[(data['Year_of_event']>=1980) & (data['Year_of_event']<=1990)]
p90_00=data[(data['Year_of_event']>=1990) & (data['Year_of_event']<=2000)]
p00_10=data[(data['Year_of_event']>=2000) & (data['Year_of_event']<=2010)]
p10_20=data[(data['Year_of_event']>=2010) & (data['Year_of_event']<=2020)]

decades=['1980s','1990s','2000s','2010s']

# Mean distance per decade
means=[p80_90['Event_distance/length'].mean(),
       p90_00['Event_distance/length'].mean(),
       p00_10['Event_distance/length'].mean(),
       p10_20['Event_distance/length'].mean()]
mean_df=pd.DataFrame({'decades':decades,'means':means})

fig_pie=px.pie(names=mean_df['decades'],
       values=mean_df['means'],
       title='<b>Percent of total distance in each decade',
       color=mean_df['decades'],
       color_discrete_map={'1990s':'#576fc7','2000s':'#ffb433','2010s':'#98d8ef'},
       hover_name=mean_df['decades'])

# Gender per decade (percent)
def gender_percent(df):
    male_count = df[df['Athlete_gender']==1].shape[0]
    male = (male_count/df.shape[0])*100
    return male, 100-male

male_means=[]
female_means=[]
for d in [p80_90,p90_00,p00_10,p10_20]:
    m,f=gender_percent(d)
    male_means.append(round(m,2))
    female_means.append(round(f,2))

mean_gender = pd.DataFrame({
    'Decade': decades*2,
    'Gender': ['Male']*4 + ['Female']*4,
    'Mean': male_means + female_means
})
fig_histogram=px.histogram(mean_gender,
             x='Decade',
             y='Mean',
             color='Gender',
             barmode='group',
             text_auto=True,
             title='<b>Percent of Athletes gender for each decade (Histogram)',
             color_discrete_sequence=px.colors.qualitative.Pastel,
             labels={'Mean':'Percent'}
             )

fig_line1 = px.line(
    mean_gender,
    x='Decade',
    y='Mean',
    color='Gender',
    markers=True,
    title='<b>Percent of Athletes genders each decade (Line)'
)

# Gender per year
gender_per_year_DF=p80_22.copy()
gender_count_per_year = gender_per_year_DF.groupby(['Year_of_event', 'Athlete_gender']).size().unstack(fill_value=0).rename(columns={0:'Female_count', 1:'Male_count'}).reset_index()
df_long = gender_count_per_year.melt(id_vars='Year_of_event',value_vars=['Male_count', 'Female_count'],var_name='Gender',value_name='Count')

fig_line2=px.line(df_long,x='Year_of_event',y='Count',color='Gender',title='<b>Athletes genders every year',markers=True)

# Avg Speed per year
p80_22['Athlete_average_speed'] = pd.to_numeric(p80_22['Athlete_average_speed'], errors='coerce').astype('float')
p80_22.loc[p80_22['Year_of_event'] <= 1995, 'Athlete_average_speed'] *= 0.001
avg_s_80_22 = p80_22.groupby('Year_of_event')['Athlete_average_speed'].mean().reset_index()
fig_line5=px.line(avg_s_80_22,x='Year_of_event',y='Athlete_average_speed',title='<b>Average Speed for each year',labels={'Year_of_event': 'Year','Athlete_average_speed': 'Average Speeds (km/h)'},markers=True,color_discrete_sequence=["#0077FF"])

# Finishers per year
num_of_finishers80_22 = p80_22.groupby('Year_of_event')['Event_number_of_finishers'].sum().reset_index()
fig_line6=px.line(num_of_finishers80_22,x='Year_of_event',y='Event_number_of_finishers',markers=True,title="<b>Number of Finishers each Year")

# Mean Age per year
mean_age_80_22=p80_22.groupby(["Year_of_event",'Athlete_gender'])['Age'].mean().reset_index()
gender_map={0:'Female',1:'Male'}
mean_age_80_22['Athlete_gender']=mean_age_80_22['Athlete_gender'].map(gender_map)
fig_line7=px.line(mean_age_80_22,x="Year_of_event",y='Age',color='Athlete_gender',labels={'Year_of_event':'Year','Age':'Mean Age'},title='<b>Mean Age for each year')

# -------------------
# Streamlit Layout
# -------------------
st.title("🏃‍♂️ Ultra Marathons Analysis Dashboard")

# Two charts per row
col1, col2 = st.columns(2)
with col1: st.plotly_chart(fig_pie, use_container_width=True)
with col2: st.plotly_chart(fig_histogram, use_container_width=True)

col3, col4 = st.columns(2)
with col3: st.plotly_chart(fig_line1, use_container_width=True)
with col4: st.plotly_chart(fig_line2, use_container_width=True)

col5, col6 = st.columns(2)
with col5: st.plotly_chart(fig_line5, use_container_width=True)
with col6: st.plotly_chart(fig_line6, use_container_width=True)

st.plotly_chart(fig_line7, use_container_width=True)
