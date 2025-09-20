import pandas as pd
from dash import Dash,html,dcc,Input,Output
import plotly.express as px

df=pd.read_csv('matplotlib session/train 1.csv')
num_cols=df.select_dtypes('number').columns

#!to deal with outliers
for col in num_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    lower_outliers = df[df[col] < lower_bound][col].values
    upper_outliers = df[df[col] > upper_bound][col].values
    df[col].replace(lower_outliers, lower_bound, inplace=True)
    df[col].replace(upper_outliers, upper_bound, inplace=True)



#! very important
print(df['Age'].nlargest(10))

app=Dash()
app.title='Taitanic Data'

fig=px.histogram(df,'Age',nbins=7,color='Pclass',text_auto=True,color_discrete_sequence=px.colors.qualitative.Pastel)
fig.update_traces(marker=dict(line=dict(color="black", width=1)),)
#!to avoid problems comes from nbin
fig.update_xaxes(range=[0, df["Age"].max()])

app.layout=html.Div([
            html.H1('Taitanic Dataset'),

            html.Div([
                    dcc.Graph(
                        figure=px.histogram(
                                        df
                                        ,x='Pclass'
                                        ,color='Survived'
                                        ,text_auto=True
                                        ,barmode='group'
                                        ,labels={'Survived':'Survival status'}
                                        ,title='<b>Survives for each class'
                                        ,color_discrete_sequence=px.colors.qualitative.Pastel
                                        )
                             )
                    ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top'}),
            
            html.Div([
                    dcc.Graph(figure=fig)
                        
                    ], style={'display': 'inline-block', 'width': '48%', 'vertical-align': 'top'}),
            html.Div([dcc.Graph(figure=px.histogram(
                                                df
                                                ,x='Pclass'
                                                ,color='Sex'
                                                ,facet_col='Survived'
                                                ,barmode='group'
                                                ,text_auto=True
                                                ,color_discrete_sequence=['#19183b','#e43636']
                                                    )
                                )
                    ],style={'display': 'block', 'width': '70%', 'vertical-align': 'top','margin':'0 auto'})
                    
                    
                    ])

app.run(debug=True)
