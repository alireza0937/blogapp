FROM python:alpine3.19
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
WORKDIR /app
COPY ./requirments.txt .
RUN pip install --upgrade pip \
    && pip install -r requirments.txt
COPY . /app