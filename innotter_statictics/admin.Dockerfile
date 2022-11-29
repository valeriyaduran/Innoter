FROM node:12.16.1

WORKDIR /microservice

RUN npm install -g dynamodb-admin

CMD ["dynamodb-admin"]