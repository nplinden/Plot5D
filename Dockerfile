FROM python:3.10-slim

ENV PORTTCP=5000
EXPOSE 5000
ENV PATH="/root/.local/bin/:$PATH"
RUN apt update -y && apt upgrade -y && apt install -y git curl && apt-get install -y python3-pip
RUN mkdir /app && \
    cd    /app && \
    curl -LsSf https://astral.sh/uv/install.sh | sh  && \
    . $HOME/.local/bin/env && \
    git clone https://github.com/nplinden/Plot5D.git && \
    cd Plot5D && \
    uv venv

# Le plus simple est d'utiliser un script shell pour initier le service
CMD ["/app/Plot5D/run.sh"]