import plotly.graph_objects as go
from .seaborn_colorpalette import sns_paired


class GraphGenerator:
    """ビューから呼び出されて、グラフをhtmlにして返す"""
    pie_line_color = '#000'
    plot_bg_color = 'rgb(255,255,255)'
    paper_bg_color = 'rgb(255,255,255)'
    month_bar_color = 'indianred'
    font_color = 'dimgray'
    color_palette = sns_paired()
    payment_color = 'tomato'
    income_color = 'forestgreen'

    def month_pie(self, labels, values):
        """月間支出のパイチャート"""
        colors = self.color_palette[0:len(labels)]
        fig = go.Figure()
        fig.add_trace(go.Pie(labels=labels,
                             values=values))

        fig.update_traces(hoverinfo='label+percent',
                          textinfo='value',
                          textfont_size=14,
                          marker=dict(line=dict(color=self.pie_line_color,
                                                width=2),
                                      colors=colors))
        fig.update_layout(
            margin=dict(
                autoexpand=True,
                l=20,
                r=0,
                b=0,
                t=30, ),
            height=300,
        )

        return fig.to_html(include_plotlyjs=False)

    def month_daily_bar(self, x_list, y_list):
        """月間支出の日別バーチャート"""
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=x_list,
            y=y_list,
            marker_color=self.month_bar_color,
        ))

        fig.update_layout(
            paper_bgcolor=self.paper_bg_color,
            plot_bgcolor=self.plot_bg_color,
            font=dict(size=14,
                      color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0,
                r=0,
                b=20,
                t=10, ),
            yaxis=dict(
                showgrid=False,
                linewidth=1,
                rangemode='tozero'))
        fig.update_yaxes(automargin=True)

        return fig.to_html(include_plotlyjs=False)

    def transition_plot(self,
                        x_list_payment=None,
                        y_list_payment=None,
                        x_list_income=None,
                        y_list_income=None):
        """推移ページの複合グラフ"""
        fig = go.Figure()

        if x_list_payment and y_list_payment:
            fig.add_trace(go.Scatter(
                x=x_list_payment,
                y=y_list_payment,
                mode='lines',
                name='payment',
                opacity=0.5,
                line=dict(color=self.payment_color,
                          width=5, )
            ))

        if x_list_income and y_list_income:
            fig.add_trace(go.Bar(
                x=x_list_income, y=y_list_income,
                name='income',
                marker_color=self.income_color,
                opacity=0.5,
            ))

        fig.update_layout(
            paper_bgcolor=self.paper_bg_color,
            plot_bgcolor=self.plot_bg_color,
            font=dict(size=14, color=self.font_color),
            margin=dict(
                autoexpand=True,
                l=0, r=0, b=20, t=30, ),
            yaxis=dict(
                showgrid=False,
                linewidth=1,
                rangemode='tozero'))
        # fig.update_yaxes(visible=False, fixedrange=True)
        fig.update_yaxes(automargin=True)
        return fig.to_html(include_plotlyjs=False)
