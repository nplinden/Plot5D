from dash import Output, Input, State, clientside_callback, ClientsideFunction
from dash.exceptions import PreventUpdate
import base64
from io import StringIO
import pandas as pd

def define_clientside_callbacks(app):
    @app.callback(
            Output("storage", "data"), 
            Output("df_upload", "children"), 
            Input("df_upload", "contents"),
            State("df_upload", "filename")
                )
    def store_data(contents, filename):
        if contents is None:
            raise PreventUpdate
        _, string = contents.split(",")
        decoded = base64.b64decode(string).decode("utf-8")
        df = pd.read_csv(StringIO(decoded))
        return df.to_dict("records"), filename

    clientside_callback(
        ClientsideFunction(namespace="clientside", 
                        function_name="update_dropdown"),
        Output("row_dropdown", "options"),
        Output("col_dropdown", "options"),
        Output("x_dropdown", "options"),
        Output("y_dropdown", "options"),
        Output("color_dropdown", "options"),
        Input('storage', 'data'),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside",
                           function_name="update_discrete_dropdown"),
        Output('row_val_dropdown', 'options'),
        Input('row_dropdown', 'value'),
        State('storage', 'data'),
    )

    clientside_callback(
        ClientsideFunction(namespace="clientside",
                           function_name="update_discrete_dropdown"),
        Output('col_val_dropdown', 'options'),
        Input('col_dropdown', 'value'),
        State('storage', 'data'),
    )

    # clientside_callback(
    #     ClientsideFunction(namespace="clientside",
    #                        function_name="update_subplot"),
    #     Input('row_dropdown', 'value'),
    #     Input('col_dropdown', 'value'),
    #     Input('row_val_dropdown', 'value'),
    #     Input('col_val_dropdown', 'value'),
    #     State('storage', 'data'),
    # )