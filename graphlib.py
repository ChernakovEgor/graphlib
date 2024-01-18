import plotly.graph_objects as go
from plotly.subplots import make_subplots
from io import BytesIO
import pandas


class Candlestick:
    def __init__(self, pair: str, timeframe: str, anomaly_time, data: pandas.DataFrame):
        self.__pair = pair
        self.__timeframe = timeframe
        self.__anomaly_time = anomaly_time
        self.__data = data

    def plot(self):
        self.__data["color"] = "green"
        self.__data.loc[self.__data["open"] > self.__data["close"], "color"] = "red"
        candle_chart = go.Candlestick(
            x=self.__data["close_time"],
            open=self.__data["open"],
            high=self.__data["high"],
            low=self.__data["low"],
            close=self.__data["close"],
        )
        self.__data.head()
        bar_chart = go.Bar(
            x=self.__data["close_time"],
            y=self.__data["volume"],
            opacity=0.3,
            marker={"color": self.__data["color"]},
        )
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        fig.add_trace(candle_chart, row=1, col=1)
        fig.add_trace(bar_chart, row=1, col=1, secondary_y=True)

        fig.update_layout(
            # autosize=False,
            width=1000,
            height=1000,
            title=f"{self.__pair} {self.__timeframe}<br><sup>{self.__anomaly_time[:-4]} UTC</sup>",
            plot_bgcolor="white",
            font_family="Courier New",
            font_size=20,
            showlegend=False,
            annotations=[
                dict(
                    name="rains watermark",
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
            ],
        )
        fig.update(layout_xaxis_rangeslider_visible=False)
        fig.update_xaxes(
            mirror=True,
            showline=True,
            linecolor="white",
            gridcolor="lightgrey",
            tickangle=90,
        )
        candle_range = [
            self.__data["low"].min() * 0.95,
            self.__data["high"].max() * 1.05,
        ]
        fig.update_yaxes(
            mirror=True,
            # ticks='outside',
            showline=True,
            linecolor="white",
            gridcolor="lightgrey",
            range=candle_range
            # range = [0, self.__data['high'].max() * 2]
        )

        fig.update_yaxes(
            mirror=True,
            showline=True,
            linecolor="white",
            gridcolor="white",
            range=[0, self.__data["volume"].max() * 4],
            showticklabels=False,
            secondary_y=True,
        )
        # fig.add_vline(x=datetime(1970, 1, 1), line_width=1, line_dash="dash", line_color="red", annotation_text='yay')
        self.fig = fig

    def as_image(self):
        return self.fig.to_image()
