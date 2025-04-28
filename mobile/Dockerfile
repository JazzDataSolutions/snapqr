# mobile/Dockerfile
FROM node:18-alpine

WORKDIR /app

# 1) Instala dependencias (cacheable)
COPY package.json yarn.lock ./
RUN yarn install --frozen-lockfile

# 2) Copia el resto
COPY . .

# 3) Exponer puertos Metro & Web
EXPOSE 19000 19001 19002 8081

CMD ["yarn", "start", "--tunnel"]

