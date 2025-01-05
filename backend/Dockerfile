FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY ./requirements/requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


CMD ["sh", "-c", "python ./file_management/manage.py makemigrations && python ./file_management/manage.py migrate && python ./file_management/manage.py runserver 0.0.0.0:8000"]