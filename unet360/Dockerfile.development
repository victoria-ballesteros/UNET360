FROM node:20-alpine

WORKDIR /app

ENV NODE_ENV=development

COPY package.json ./

RUN npm install --legacy-peer-deps

COPY . .

CMD ["npm", "run", "dev"]