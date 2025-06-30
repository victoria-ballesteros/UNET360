FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=development

COPY package.json ./

RUN npm install --legacy-peer-deps

COPY . .

CMD ["npm", "run", "dev"]

# FROM node:20-alpine AS builder

# WORKDIR /app

# COPY package*.json ./
# RUN npm install

# COPY . .
# RUN npm run build

# FROM nginx:alpine

# COPY --from=builder /app/dist /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]
