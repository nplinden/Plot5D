from flask import Flask
from dash import Dash
import dash_bootstrap_components as dbc

server = Flask("Plot5D")
app = Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Plot5D"
