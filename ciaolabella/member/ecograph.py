import plotly.express as px
from plotly.offline import plot
import pandas as pd
import plotly.graph_objects as go
import datetime
from dateutil.relativedelta import relativedelta
from .models import ECOPOINT
from django.db.models import Avg



def ecopoint(id):
    x1 = (datetime.datetime.now() - relativedelta(months=3)).strftime('%Y-%m')
    x4 = datetime.date.today().strftime('%Y-%m')

    my_df = pd.DataFrame(list(ECOPOINT.objects.filter(member_id=id, month_kb__gte=x1, month_kb__lte=x4).values('month_kb', 'point_amt')))
    if len(my_df) == 0:
        my_df = pd.DataFrame([[x4,0]], columns=['month_kb', 'point_amt'])

    # if len(my_df) == 0:
    #     my_df = pd.DataFrame([[x1,0],[x2,0],[x3,0],[x4,0]], columns=['month_kb', 'point_amt'])
    # elif len(my_df) < 4:
    #     for x in [x1, x2, x3, x4]:
    #         if my_df['month_kb'].isin(x) == False:
    #             my_df.insert({'month_kb':x, 'point_amt':0})

    total_df = pd.DataFrame(list(ECOPOINT.objects.filter(month_kb__gte=x1, month_kb__lte=x4).values('month_kb').annotate(point_amt=Avg('point_amt'))))


    fig = go.Figure([go.Bar(x=my_df['month_kb'], y=my_df['point_amt'], name='나의 에코포인트', marker_color='rgb(235, 71, 81)'),\
                     go.Bar(x=total_df['month_kb'], y=total_df['point_amt'], name='전체 에코포인트', marker_color='rgb(0, 185, 142)')])
    fig.update_layout(template='plotly_white')
    fig.update_traces(hovertemplate='%{y} ecopoint<extra></extra>')
    fig.update_layout(legend=dict(yanchor="middle", xanchor="right"))
    config = {'displayModeBar': False}
    plot_div = plot(fig, config=config , output_type='div')

    return plot_div
