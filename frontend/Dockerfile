FROM node:20-alpine

# Instalar pnpm
RUN npm install -g pnpm

# Directorio de trabajo
WORKDIR /app

# Copiar SOLO dependencias (para cache eficiente)
COPY comment_charts/package.json ./

# Instalar dependencias
RUN pnpm install

# Copiar el resto del proyecto
COPY comment_charts /app

# Exponer puerto de Vite
EXPOSE 5173

# Ejecutar Vite en modo host (necesario para Docker)
CMD ["pnpm", "run", "dev:host"]