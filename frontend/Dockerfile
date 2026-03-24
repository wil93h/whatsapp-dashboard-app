FROM node:20-alpine

# instalar pnpm
RUN npm install -g pnpm

WORKDIR /app

# copiar dependencias
COPY comment/package.json pnpm-lock.yaml* ./

RUN pnpm install

# copiar el resto
COPY . .

EXPOSE 5173

CMD ["pnpm", "run", "dev:host"]