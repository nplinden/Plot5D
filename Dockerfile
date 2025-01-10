FROM ghcr.io/astral-sh/uv:bookworm

RUN apt update -y && apt upgrade -y && apt install -y git 

RUN git clone https://github.com/nplinden/Plot5D.git && \
    cd Plot5D && \
    uv venv

