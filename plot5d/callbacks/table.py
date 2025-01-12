from dash import callback, Output, Input, State
from dash.exceptions import PreventUpdate
from plot5d.plotdata import sample


@callback(
    [
        Output("table", "data"),
        Output("table", "columns"),
        Output("table", "page_count"),
    ],
    Input("parcoords_dropdown_memory", "data"),
    Input("parcoords_memory", "data"),
    Input("5DPlot", "selectedData"),
    Input("table", "page_current"),
    Input("column_dropdown", "value"),
    State("table", "page_size"),
)
def select_data_for_table(
    parcoords_dropdown_memory, parcoords_memory, selected, page_current, column_dropdown, page_size
):
    if selected is None:
        raise PreventUpdate
    if column_dropdown is None:
        raise PreventUpdate
    idx = [d["customdata"] for d in selected["points"]]
    df = sample.df.iloc[idx]
    page_count = len(df) // page_size + 1
    if len(df) > 0 and len(df) % page_size == 0:
        page_count -= 1

    if parcoords_memory and parcoords_dropdown_memory:
        for col_idx, ranges in parcoords_memory.items():
            col_name = parcoords_dropdown_memory[col_idx]
            queries = []
            for r in ranges:
                left, right = r
                queries.append(f"{left} <= {col_name} <= {right}")
            query = " | ".join(queries)
            print(query)
            df = df.query(query)

    df = df[column_dropdown]
    df = df.iloc[page_current * page_size : (page_current + 1) * page_size]
    return df.to_dict("records"), [{"name": c, "id": c} for c in df.columns], page_count
