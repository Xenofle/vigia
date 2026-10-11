FROM node:22-alpine

WORKDIR /app

# Se copian primero los manifiestos para aprovechar la caché de capas:
# si no cambian las dependencias, Docker no repite la instalación.
COPY package.json package-lock.json ./
RUN npm ci --omit=dev

COPY src ./src

EXPOSE 4000

CMD ["node", "src/server.js"]
