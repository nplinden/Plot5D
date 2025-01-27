FROM ghcr.io/astral-sh/uv:alpine

ENV PORTTCP=5000
EXPOSE 5000

RUN apk add git python3

RUN mkdir -p /app/Plot5D
COPY assets/ /app/Plot5D/assets
COPY components/ /app/Plot5D/components
COPY main.py callbacks.py pyproject.toml README.md /app/Plot5D/

CMD [ "uv", "run", "--directory", "/app/Plot5D", "/app/Plot5D/main.py" ]