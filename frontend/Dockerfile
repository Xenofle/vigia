# Imagen de desarrollo: sirve el proyecto con el servidor de Vite.
# En el hito de despliegue se sustituirá por una compilación estática servida por Nginx.
FROM node:22-alpine

WORKDIR /app

COPY package.json package-lock.json ./
RUN npm ci

COPY . .

EXPOSE 5173

CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
