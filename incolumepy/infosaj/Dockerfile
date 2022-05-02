FROM alpine:3.15

RUN  apk update && apk upgrade && rm -rf /var/cache/apk/*

# COPY conf.d/* /etc/apache2/

CMD  [ "/usr/sbin/httpd", "-D", "FOREGROUND"]

