FROM ghcr.io/astral-sh/uv:alpine

ENV PORTTCP=5000
EXPOSE 5000

RUN apk add git python3

RUN mkdir -p /app/Plot5D && \
    git clone https://github.com/nplinden/Plot5D.git /app/Plot5D

RUN chmod a+x /app/Plot5D/run.sh && \
    cd /app/Plot5D && \
    uv venv --python 3.12

# CMD ["/app/Plot5D/run.sh"]
ENTRYPOINT ["sh", "/app/Plot5D/run.sh"]