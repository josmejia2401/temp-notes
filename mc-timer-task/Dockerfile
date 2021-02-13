FROM python:alpine3.8
RUN mkdir /app
RUN mkdir ${USER}/data/
ARG LOG_DIR=/logs
# Create Log Directory
RUN mkdir -p ${LOG_DIR}
# Environment Variables
ENV LOG_FILE_LOCATION=${LOG_DIR}/
ENV ENVIRONMENT=production
COPY . /app
WORKDIR /app
ENV ENVIRONMENT=production
RUN pip3 install -r requirements.txt
EXPOSE 9010
CMD [ "python3", "./app.py" ]
