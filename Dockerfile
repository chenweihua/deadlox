FROM python:3.6.5-alpine3.7
WORKDIR "/home/docker/app"
COPY . /home/docker/app

RUN apk add --no-cache mariadb-dev \
        && apk add --no-cache --virtual .build-deps \
               build-base \
	&& pip install mysqlclient==1.3.12 sqlalchemy \ 
	&& apk del .build-deps

CMD ["python", "deadlox.py"]
