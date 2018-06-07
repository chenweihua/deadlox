FROM python:3.6.5-alpine3.7
MAINTAINER Takuya Noguchi <takninnovationresearch@gmail.com>
WORKDIR "/home/docker/app"
COPY . /home/docker/app

RUN apk add --update --no-cache mariadb-client-libs \
	&& apk add --no-cache --virtual .build-deps \
		mariadb-dev \
		gcc \
		musl-dev \
	&& pip install mysqlclient==1.3.12 sqlalchemy tabulate \
	&& apk del .build-deps

#RUN mkdir -p "/home/docker/app"
#COPY "/deadlock.py" "/home/docker/app/"
#CMD ["python", "/home/docker/app/deadlock.py"]
CMD ["python", "deadlox.py"]
