# Stage 1: Build React app
FROM node:18 AS build

WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .

RUN npm run build

# Stage 2: Serve with lightweight web server
# FROM nginx:alpine
# COPY --from=build /app/build /usr/share/nginx/html

# Expose the port
EXPOSE 3000

# Default command
CMD ["npm", "start"]
