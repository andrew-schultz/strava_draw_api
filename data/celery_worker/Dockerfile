FROM python:3.12-slim-bullseye

RUN pip install celery
COPY start /start-celeryworker
RUN sed -i 's/\r$//g' /start-celeryworker
RUN chmod +x /start-celeryworker
