FROM node:18-alpine AS build

WORKDIR /app

COPY package*.json ./

RUN npm ci

COPY . .

RUN NODE_OPTIONS="--max-old-space-size=2048" npm run build


FROM nginx:alpine

COPY --from=build /app/build /usr/share/nginx/html
COPY nginx/default.conf /etc/nginx/conf.d/default.conf

RUN sed -i 's/user  nginx;/user  nginx;/' /etc/nginx/nginx.conf && \
    chown -R nginx:nginx /usr/share/nginx/html && \
    chown -R nginx:nginx /var/cache/nginx /var/log/nginx /etc/nginx

USER nginx

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
