#!/bin/bash
. $HOME/.local/bin/env
export PORTTCP=5000
cd /app/Plot5D
uv run main.py