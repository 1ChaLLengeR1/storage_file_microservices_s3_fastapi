FROM python:3.9-slim-buster

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./../requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

CMD ["uvicorn", "main:app", "--reload", "--log-level" , "debug", "--host", "0.0.0.0", "--port", "7000"]