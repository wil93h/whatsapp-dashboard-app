FROM node:20-alpine

RUN npm install -g pnpm

WORKDIR /app

COPY comment_charts/package.json ./

RUN pnpm install

COPY comment_charts/ /app

EXPOSE 5173

CMD ["pnpm", "run", "dev:host"]
