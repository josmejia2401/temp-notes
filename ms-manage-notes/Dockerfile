FROM python:alpine3.8
RUN mkdir /app
RUN mkdir ${USER}/data/
COPY . /app
WORKDIR /app
ENV ENVIRONMENT=production
RUN pip3 install -r requirements.txt
EXPOSE 9000
CMD [ "python3", "./app.py" ]
