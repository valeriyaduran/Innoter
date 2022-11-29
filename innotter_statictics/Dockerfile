FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1


RUN pip3 install pipenv

WORKDIR /microservice

COPY Pipfile .
COPY Pipfile.lock .


RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

CMD ["uvicorn", "statictics.main:app", "--host", "0.0.0.0", "--port", "8080"]