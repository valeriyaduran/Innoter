FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

RUN pip3 install pipenv

WORKDIR /app

COPY ./Pipfile .
COPY ./Pipfile.lock .


RUN pipenv install --system --deploy --ignore-pipfile

COPY . .

RUN chmod +x ./entrypoint.sh
CMD ["./entrypoint.sh"]
