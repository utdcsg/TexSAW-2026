FROM node:lts-alpine AS base

WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

RUN npm ci

COPY . .

FROM base AS runner

ENV NODE_ENV=production
ENV PORT=3000

EXPOSE 3000

CMD ["npm", "start"]