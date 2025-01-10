import numpy as np
import pandas as pd
from pathlib import Path
from plotly.subplots import make_subplots
import plotly.graph_objects as go
from itertools import product
from pathlib import Path


class PlotData:
    def __init__(self, path):
        p = Path(path)
        if p.exists():
            self.df = pd.read_csv(p)
        else:
            np.random.seed(1)
            Q1 = np.arange(1, 201, 0.5)
            Q2 = Q1 ** np.sqrt(2 + np.random.normal(1, 0.1, Q1.shape))
            Q3 = np.random.choice([100, 200, 300, 400, 500], Q1.shape)
            Q4 = np.log(Q3 * np.random.normal(1, 0.2, Q3.shape)) * np.log(Q2)
            Q5 = np.astype((np.floor(Q4) % 27 % 5 + 10) * 100, int)
            self.df = pd.DataFrame(data={"Q1": Q1, "Q2": Q2, "Q3": Q3, "Q4": Q4, "Q5": Q5})
            self.df.to_csv(p, index=False)

    def subplots(
        self,
        rows,
        cols,
        x,
        y,
        color,
        #  figsize,
        x_min,
        x_max,
        y_min,
        y_max,
        color_min,
        color_max,
    ):
        """
        rows = ('Q5', [1100, 1200, 1300, 1400])
        cols = ('Q3', [100, 200, 300, 400])
        """
        if x_min is None:
            x_min = -np.inf
        if x_max is None:
            x_max = np.inf
        if y_min is None:
            y_min = -np.inf
        if y_max is None:
            y_max = np.inf
        if color_min is None:
            color_min = -np.inf
        if color_max is None:
            color_max = np.inf
        rowname = rows[0]
        colname = cols[0]
        nrows, ncols = len(rows[1]), len(cols[1])
        fig = make_subplots(
            rows=nrows,
            cols=ncols,
            shared_xaxes=True,
            shared_yaxes=True,
            vertical_spacing=0.1,
            horizontal_spacing=0.05,
            column_titles=[f"{colname}={cols[1][c]}" for c in range(ncols)],
            row_titles=[f"{rowname}={rows[1][r]}" for r in range(nrows)],
        )
        # logger.info("figsize=({}, {})", nrows, ncols)
        df = self.df[
            (self.df[x] < x_max)
            & (self.df[x] > x_min)
            & (self.df[y] < y_max)
            & (self.df[y] > y_min)
            & (self.df[color] < color_max)
            & (self.df[color] > color_min)
        ]
        for row, col in product(range(1, nrows + 1), range(1, ncols + 1)):
            rowval = rows[1][row - 1]
            colval = cols[1][col - 1]
            _df = df[(df[rowname] == rowval) & (df[colname] == colval)]
            fig.add_trace(
                go.Scatter(
                    x=_df[x],
                    y=_df[y],
                    customdata=_df.index,
                    mode="markers",
                    marker=dict(
                        size=10,
                        color=_df[color],
                        coloraxis="coloraxis",
                    ),
                ),
                row=row,
                col=col,
            )

        for col in range(1, ncols + 1):
            fig.update_xaxes(title_text=x, row=nrows, col=col)
        for row in range(1, nrows + 1):
            fig.update_yaxes(title_text=y, row=row, col=1)

        fig.update_layout(
            coloraxis=dict(colorscale="Viridis"),
            coloraxis_colorbar=dict(title=color),
            showlegend=False,
            # width=figsize[0],
            # height=figsize[1],
            dragmode="lasso",
        )
        return fig


datapath = Path("data")
if not datapath.exists():
    datapath.mkdir()
sample = PlotData("data/samples.csv")
