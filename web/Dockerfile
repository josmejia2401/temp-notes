FROM node:14.1-alpine
ENV ENVIRONMENT=production 
WORKDIR /web
COPY package*.json ./
RUN npm install -g express
RUN npm install
COPY . .
RUN npm run build build_dev
# RUN ls -lsa
EXPOSE 9005
CMD ["npm", "run", "start_express"]
