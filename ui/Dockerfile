FROM node:14-alpine

WORKDIR /app

COPY rollup.config.js ./
COPY package*.json ./

RUN npm install
COPY . /app

RUN npm run-script build

EXPOSE 8080
ENV HOST=0.0.0.0

CMD [ "npm", "start" ]
