FROM node:buster AS frontend-builder

WORKDIR /app
COPY package*.json ./

RUN npm install

COPY ./ .

RUN npm run build

FROM nginx:latest AS frontend
COPY --from=frontend-builder /app/dist /www
EXPOSE 80
