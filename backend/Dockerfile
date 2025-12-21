FROM python:3.12.3-slim

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

RUN pip install gunicorn

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "DIDIM.wsgi:application"]