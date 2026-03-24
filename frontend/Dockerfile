FROM node:20-alpine

RUN npm install -g pnpm

WORKDIR /app

# copiar todo el proyecto de una vez
COPY comment_charts .

# instalar deps DESPUÉS de copiar todo
RUN pnpm install

EXPOSE 5173

CMD ["pnpm", "run", "dev:host"]