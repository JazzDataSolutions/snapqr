FROM node:18-alpine

WORKDIR /app

COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

COPY . .

EXPOSE 8081 19000 19001 19002

CMD ["yarn", "start", "--host", "0.0.0.0"]

