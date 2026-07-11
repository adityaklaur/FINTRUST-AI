# Dev-server image (works with the Vite /api proxy). For production, build with
# `npm run build` and serve the static dist/ behind a reverse proxy instead.
FROM node:22-alpine

WORKDIR /app
COPY package.json package-lock.json* ./
RUN npm install
COPY . .

EXPOSE 5173
CMD ["npm", "run", "dev", "--", "--host", "0.0.0.0"]
