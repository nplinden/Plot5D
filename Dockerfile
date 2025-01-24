FROM ghcr.io/astral-sh/uv:alpine

ENV PORTTCP=5000
EXPOSE 5000

RUN apk add git python3

RUN mkdir -p /app/Plot5D
COPY plot5d/ /app/Plot5D/plot5d
COPY assets/ /app/Plot5D/assets
COPY main.py pyproject.toml /app/Plot5D/

RUN cd /app/Plot5D && \
    uv venv && \
    uv pip install .

CMD [ "uv", "run", "--directory", "/app/Plot5D", "/app/Plot5D/main.py" ]