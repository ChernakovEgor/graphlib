import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
from io import BytesIO
import pandas

# if not os.path.exists("images"):
#     os.mkdir("images")


def draw_and_save(pair: str, timeframe: str , anomaly_time, data: pandas.DataFrame) -> BytesIO:
    data['color'] =  'green'
    data.loc[data['open'] > data['close'],'color'] = 'red'
    candle_chart = go.Candlestick(x=data['close_time'],
                    open=data['open'],
                    high=data['high'],
                    low=data['low'],
                    close=data['close'])
    bar_chart = go.Bar(x=data['close_time'], y=data['volume'], opacity=0.3, marker={'color': data['color']})
    fig = make_subplots(specs=[[{"secondary_y": True}]])
    fig.add_trace(candle_chart, row=1, col=1)
    fig.add_trace(bar_chart, row=1, col=1, secondary_y=True)
    
    fig.update_layout(
        width=1000,
        height=1000,
        title=f"{pair} {timeframe}<br><sup>{anomaly_time[:-4]} UTC</sup>",
        plot_bgcolor='white',
        font_family="Courier New",
        font_size=20,
        showlegend=False,
        annotations=[
        dict(
            name="host bot watermark",
        text="@GainsBeforeRains_bot",
        textangle=-30,
        opacity=0.1,
        font=dict(color="black", size=60),
        xref="paper",
        yref="paper",
        x=0.5,
        y=0.5,
        showarrow=False,
        )
    ]
    )
    fig.update(layout_xaxis_rangeslider_visible=False)
    candle_range = [data['low'].min() * 0.95, data['high'].max() * 1.05]
    fig.update_xaxes(
        mirror=True,
        #ticks='outside',
        showline=True,
        linecolor='white',
        gridcolor='lightgrey',
        tickangle=90,
        range=candle_range
    )
    fig.update_yaxes(
        mirror=True,
        #ticks='outside',
        showline=True,
        linecolor='white',
        gridcolor='lightgrey'
    )

    fig.update_yaxes(
        mirror=True,
        showline=True,
        linecolor='white',
        gridcolor='white',
        range = [0, data['volume'].max() * 5],
        showticklabels=False,
        secondary_y=True
    )
    #fig.add_vline(x=datetime(1970, 1, 1), line_width=1, line_dash="dash", line_color="red", annotation_text='yay')
    # fig.show()
    path = f"images/{anomaly_time}_{pair}_{timeframe}.png"
    image = BytesIO()
    fig.write_image(image)
    return image
