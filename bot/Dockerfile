FROM python:3.9

COPY requirements.txt /tmp/bot/
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r /tmp/bot/requirements.txt && \
    mkdir /workdi_bot

COPY . /app
WORKDIR /app
