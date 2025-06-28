FROM python:3.11-slim

RUN apt-get update && \
    apt-get install -y chromium-driver chromium && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENV CHROME_BIN=/usr/bin/chromium-browser

CMD ["gunicorn", "app:app"]