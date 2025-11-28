FROM node:20-alpine

WORKDIR /app

COPY frontend/package.json ./
RUN npm install --production=false

COPY frontend ./frontend
WORKDIR /app/frontend
RUN npm install --production=false && npm run build

RUN npm install -g serve
EXPOSE 3000
CMD ["serve", "-s", "build", "-l", "3000"]
