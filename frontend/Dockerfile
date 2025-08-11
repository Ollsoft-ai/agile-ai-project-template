FROM node:22-alpine AS base

WORKDIR /usr/src/app

# install deps only; code will be bind-mounted
COPY package*.json ./
RUN npm ci

EXPOSE 5173
CMD ["npm", "run", "dev"] 