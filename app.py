import streamlit as st
from functions import *
import plotly.express as px
import plotly.graph_objects as go

st.title("Crime Pattern Analysis")

state_opt = sorted([None] + list(set(data['Area_Name'].values)), key=lambda x: x[0] if x is not None else '')

state = st.sidebar.selectbox(label='Select The State', options=state_opt)
year_opt = [None]+list(data.Year.unique())
year = st.sidebar.selectbox(label='Choose The Year', options=year_opt)
if (year is not None) and (state is not None):
    if st.sidebar.button('Plot Crime Data'):
        st.plotly_chart(murdered_gender(state))
        st.plotly_chart(crimes_line_plot(state))
        st.plotly_chart(theft(state))
        fig, fig2, fig3 = victims(state, year)
        st.plotly_chart(kid_rape(state, year))
        st.plotly_chart(theft_byDist(state, year))
        st.plotly_chart(fig)
        st.plotly_chart(fig2)
        st.plotly_chart(fig3)   

            
    

