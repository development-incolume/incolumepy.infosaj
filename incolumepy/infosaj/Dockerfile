FROM alpine:3.15

RUN  export HTTP_PROXY=http://10.1.101.101:8080 \
     && export HTTPS_PROXY=http://10.1.101.101:8080 \
     && apk update \
     && apk upgrade  \
     && apk add apache2 \
     && apk add apache2-proxy \
     && apk add apache2-ssl \
     && rm -rf /var/cache/apk/*

EXPOSE 80 443

CMD  [ "/usr/sbin/httpd", "-D", "FOREGROUND"]

