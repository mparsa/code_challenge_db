# Dockerfile for deployment 
FROM python:3.6-alpine

EXPOSE 8000

RUN apk add --no-cache gcc python3-dev musl-dev

ADD . /dreambroker

WORKDIR /dreambroker

RUN pip install -r requirements.txt

CMD ["python", "dreambroker/manage.py", "runserver", "0.0.0.0:8000"]