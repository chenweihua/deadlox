FROM python:3.6.5-alpine3.7
WORKDIR "/home/docker/app"
COPY . /home/docker/app

RUN apk add --no-cache mariadb-dev \
        && apk add --no-cache --virtual .build-deps \
               build-base \
	&& pip install mysqlclient==1.3.12 sqlalchemy \ 
        && apk del .build-deps

ADD https://dl.google.com/cloudsql/cloud_sql_proxy.linux.amd64 /tmp
RUN chmod +x /tmp/cloud_sql_proxy.linux.amd64 
RUN mv /tmp/cloud_sql_proxy.linux.amd64 /home/docker/app/cloud_sql_proxy

CMD ["python", "deadlox.py"]
