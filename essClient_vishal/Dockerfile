# Here node alpine is used, if you are using windows then use windows compatible image
FROM node:18-alpine as build 

WORKDIR /app
COPY . /app

RUN npm install
RUN npm run build

EXPOSE 5173

CMD ["npm","run","dev"]
