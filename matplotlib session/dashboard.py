from dash import Dash, html, dcc, Input, Output
import pandas as pd
import plotly.express as px

df=pd.read_csv('matplotlib session/train 1.csv')
num_cols=df.select_dtypes(include='number').columns
print(num_cols)

app=Dash()
app.title='interactive dashboard'
x=[1,2,3,4,5,6,7,8]
y=[12,13,14,15,10,9,6,2]
#**front end**
app.layout=html.Div([
    #*div 1 inside main(im)
    html.Div([
            html.H1('interactive dashboard',className='h1')
           ,html.Label('select a value to show in pie plot')
           #! dropdown is for drop down menu that have a options that user can choose from
           ,
           #*dropdown div
           html.Div([
               dcc.Dropdown(
                id='column dropdown'
                
                #this is the label(name) and value(choice)
               ,options=[{'label':col,'value':col}for col in num_cols]
               
               #make a default value for dorpdown
               ,value='Pclass')
                        
                    ])

               #!this is the graph it self
            

            ,html.Div([
               dcc.Graph(id='pie chart',className='graph')
               ,dcc.Graph(id='plot graph',figure=px.line(x=x,y=y,title='chart',labels={'x':'x','y':'y'}))
                    ])
                
                ]),

    #*div 2 IM
    html.Div([html.H1('hello again')], className='box',style={'float':'down','display':'block'})
    ])

#**Backend**
@app.callback(
    Output('pie chart','figure'),
    Input('column dropdown','value'))
def update_pie(col):
    # grouped=df.groupby('Age')[col].sum().reset_index()
    fig=px.pie(df,
               names=col
            #    ,values='Survived'
               ,title=f'dis of {col}'
               ,hole=.8
               ,color_discrete_sequence=px.colors.qualitative.Pastel
                )
                                                    #!<br> means break line , new line
    fig.update_traces( texttemplate="%{label}<br>%{value}<br>%{percent}"
                      ,textposition='outside')
    return fig

# @app.callback(
#     Output('plot graph','figure'),
#     Input('column dropdown','value'))
# def updata_plot():
#     px.line([1,2,3,4,4],[12,12,3,4,8,7,14])

if __name__=='__main__':
    app.run(debug=True)

