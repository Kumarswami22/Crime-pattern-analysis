import pandas as pd
import numpy as np
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots


data = pd.read_csv('32_Murder_victim_age_sex.csv')
data.fillna(0,inplace=True)
data = data[data['Sub_Group_Name']!= '3. Total']

data = data.assign(
    Sub_Group_Name = lambda x:x['Sub_Group_Name'].replace({
        '2. Female Victims': 'Female',
        '1. Male Victims': 'Male'
    }),
    Area_Name= lambda x:x['Area_Name'].str.upper()
)

data2= pd.read_csv('01_District_wise_crimes_committed_IPC_2001_2012.csv')
data.fillna(0,inplace=True)
print(f'the data has:{data2.shape[0]} rows and no.of columns: {data2.shape[1]}\n')
data2.head()


def murdered_gender(state):
    df=data[data['Area_Name']==state]
    pivot_data = df.pivot_table(index='Year', columns='Sub_Group_Name', values='Victims_Total')

    fig = go.Figure(data=[
        go.Bar(name='Male Victims', x=pivot_data.index, y=pivot_data['Male']),
        go.Bar(name='Female Victims', x=pivot_data.index, y=pivot_data['Female'])
    ])

    fig.update_layout(
        title=f'Murdered Victims by Year By the Gender in the State of {state}.',
        xaxis_title='Year',
        yaxis_title='Number of Victims',
        barmode='group' 
    )
    
    return fig
def kid_rape(state,year):
    df=data2[(data2['STATE/UT']==state) & (data2['YEAR']==year)&(data2['DISTRICT']!='TOTAL')]
    fig = go.Figure(data=[
        go.Bar(name='RAPE',x=df.DISTRICT,y=df.RAPE),
        go.Bar(name='KIDNAPPING',x=df.DISTRICT,y=df['KIDNAPPING & ABDUCTION']),
        
    ])
    fig.update_layout(
        title=f'Rape Rates in {state} in the of {year}',
        xaxis_title='district',
        barmode='group',
        yaxis_title='no.of Rapes'
    )
    return fig
    
def murder_Bydistrict(state,year):
    df2 = data2[(data2['STATE/UT']==state)&(data2['YEAR']==year)&(data2['DISTRICT']!='TOTAL')]
    
    fig=go.Figure(data=[
        go.Bar(name='MURDER',x=df2.DISTRICT,y=df2.MURDER),
        go.Bar(name='ATTEMPT TO MURDER',x=df2.DISTRICT,y=df2['ATTEMPT TO MURDER'])
    ])
    fig.update_layout(
        barmode='group',
        xaxis_title='districts',
        title=f'Brutal Murders in {state} in the year of {year}.'
                    )
    return fig
    
def crimes_line_plot(state):
    df1=data2[(data2['DISTRICT']=='TOTAL')&(data2['STATE/UT']==state)]
    fig = go.Figure(data=[
        go.Scatter(name='MURDER',x=df1.YEAR,y=df1.MURDER),
        go.Scatter(name='RAPE',x=df1.YEAR,y=df1.RAPE),
        go.Scatter(name='KIDNAPPING',x=df1.YEAR,y=df1['KIDNAPPING & ABDUCTION']),
        go.Scatter(name='ATTEMPT TO MURDER',x=df1.YEAR,y=df1['ATTEMPT TO MURDER'])
    ])
    
    fig.update_layout(
        title=f'Crimes Rates in Each Districts in the state of {state}',
        autosize=False,
        xaxis_title='Year',
        width=800, 
        height=600)
    
    
    return fig
    
def theft(state):
    df1=data2[(data2['DISTRICT']=='TOTAL')&(data2['STATE/UT']==state)]
    fig=go.Figure(data=[
        go.Scatter(name='THEFT',x=df1.YEAR,y=df1.THEFT),
        go.Scatter(name='VECHILE THEFT',x=df1.YEAR,y=df1['AUTO THEFT']),
        go.Scatter(name='OTHER THEFT',x=df1.YEAR,y=df1['OTHER THEFT'])
    ])
    
    fig.update_layout(
        title=f'Theft ratio in every district in the state of {state} from 2010-2012',
        autosize=False, 
        width=800, 
        height=600
    )
    return fig
def theft_byDist(state,year):
    df2 = data2[(data2['STATE/UT']==state)&(data2['YEAR']==year)&(data2['DISTRICT']!='TOTAL')]
    fig=go.Figure(data=[
        go.Bar(name='THEFT',x=df2.DISTRICT,y=df2.THEFT),
        go.Bar(name='VECHILE THEFT',x=df2.DISTRICT,y=df2['AUTO THEFT'])
    ])
    fig.update_layout(
        barmode='group',
        title=f'Theft Ratios in {state} in the year of {year}.',
        xaxis_title='district'
    )

    return fig
    
    
def victims(state,year):
    transpose = data[data['Area_Name'] == state].set_index('Year').T
    
    transpose = transpose.assign(
        total_female=transpose.iloc[:, :10].apply(lambda x: pd.to_numeric(x, errors='coerce')).sum(axis=1),
        total_male=transpose.iloc[:, 10:].apply(lambda x: pd.to_numeric(x, errors='coerce')).sum(axis=1),
        total=transpose.iloc[:, :].apply(lambda x: pd.to_numeric(x, errors='coerce')).sum(axis=1)
    )
    column_selection = transpose.loc[:, transpose.columns == year]
    row_selection = transpose.iloc[:,20:]
    result = pd.concat([column_selection, row_selection],axis=1)
    result.columns.values[:2] = ['Male','Female']
    result = result.drop(index=['Victims_Total', 'Group_Name', 'Area_Name','Sub_Group_Name'], axis=0)
    result = result.iloc[1:,:]
    fig = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=["Female", "Male"])

    fig.add_trace(go.Pie(name='Male', labels=result.index, values=result.iloc[:,1].values), 1, 1)
    fig.add_trace(go.Pie(name='Female', labels=result.index, values=result.iloc[:,0].values), 1, 2)
    
    fig.update_layout(
        title=f'Murdered victims in the state of {state} in year {year}.'
                     )
    
    fig2 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=["Male", "Female"])

    fig2.add_trace(go.Pie(name='Male', labels=result.index, values=result.iloc[:,3].values), 1, 1)
    fig2.add_trace(go.Pie(name='Female', labels=result.index, values=result.iloc[:,2].values), 1, 2)
    
    fig2.update_layout(
        title=f'Overall Murdered victims in the state of {state} in From year 2001 to 2010.'
                     )
    
    
    fig3 = make_subplots(rows=1, cols=2, specs=[[{'type':'domain'}, {'type':'domain'}]], subplot_titles=["Overall Male & Female"])

    fig3.add_trace(go.Pie(name='Overall Male & Female', labels=result.index, values=result.iloc[:,4].values), 1, 1)
   
    
    fig3.update_layout(
        title=f'Overall Male & Femal Ratios Murdered victims in the state of {state} in From Year 2001 to 2010.'
            
                     )
    return fig,fig2,fig3
    

    
