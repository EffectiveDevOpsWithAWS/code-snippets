FROM node:argon

RUN mkdir -p /usr/local/helloworld/
COPY helloworld.js package.json /usr/local/helloworld/

WORKDIR /usr/local/helloworld/

RUN npm install

EXPOSE 3000
CMD [ "node", "helloworld.js" ]
