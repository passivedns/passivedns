FROM node:latest as build-stage

ARG HOST

RUN sed -i -e "s+{{HOST}}+$HOST+g" "src/services/config.json"

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY ./ .

RUN npm run build

FROM nginx as production-stage

RUN mkdir /app
COPY --from=build-stage /app/dist /app
COPY nginx.conf /etc/nginx/nginx.conf
