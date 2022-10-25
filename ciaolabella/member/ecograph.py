import plotly.express as px
from plotly.offline import plot
import pandas as pd
import plotly.graph_objects as go

from .models import ECOPOINT



def ecopoint(id):
    df = pd.DataFrame(list(ECOPOINT.objects.filter(user_nb=id).values()))
    df['time'] = df['save_tm'].dt.strftime("%Y%m%d")
    df = df.groupby(['time'])['point_amt'].sum().reset_index(name='ecopoint')

    fig = go.Figure([go.Bar(x=df['time'], y=df['ecopoint'])])
    config = {'displayModeBar': False}
    fig.update_traces(marker_color='rgb(197, 241, 231)', marker_line_color='rgb(0, 185, 142)',
                    marker_line_width=1.5, opacity=0.6)
    fig.update_layout(template='plotly_white')
    fig.update_traces(hovertemplate='%{y} eco point<extra></extra>')

    plot_div = plot(fig, config=config , output_type='div')
    

    return plot_div
    
