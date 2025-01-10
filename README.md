# Plot5D

## Run through Dash

The easiest way to run Plot5D is to use [uv](https://github.com/astral-sh/uv) and Dash directly:

```sh
git clone https://github.com/nplinden/Plot5D.git
cd Plot5D
uv run main.py
``` 

## Run through Flask

Dash is based on the Flask framework, so you can also run Plot5D like any other Flask app:

```sh
git clone https://github.com/nplinden/Plot5D.git
cd Plot5D
uv venv
source .venv/bin/activate.sh
flask run --host 0.0.0.0
``` 
