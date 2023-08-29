FROM python:3.11

LABEL Maintainer="GeekMasher"

WORKDIR /app

COPY . /app

# Install and setup cron/crontab + set permissions
RUN apt-get update -y && \
    apt-get install -y cron && \
    chmod +x /app/entrypoint.sh /app/do-dynamic-dns.py

RUN python3 -m pip install pipenv && python3 -m pipenv install --system

ENTRYPOINT [ "/app/entrypoint.sh" ]

