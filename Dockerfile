FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install pipenv

WORKDIR /app

COPY Pipfile /app
COPY Pipfile.lock ./


RUN pipenv install --system --deploy --ignore-pipfile

COPY . /app

RUN chmod +x /app/entrypoint.sh
CMD ["/app/entrypoint.sh"]
