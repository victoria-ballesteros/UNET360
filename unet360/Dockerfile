# Etapa 1: Build
FROM node:20-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm install --legacy-peer-deps

COPY . .
RUN npm run build

# Etapa 2: Servir con un servidor estático (como nginx)
FROM nginx:alpine

COPY --from=builder /app/dist /usr/share/nginx/html

# Elimina configuración default de nginx si quieres una custom
RUN rm /etc/nginx/conf.d/default.conf

# Puedes copiar tu propia config si lo necesitas
# COPY nginx.conf /etc/nginx/conf.d

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
