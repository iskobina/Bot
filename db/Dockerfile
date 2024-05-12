FROM postgres:15.0

ARG REPUSER
ARG REPPASSWORD

COPY init.sql /docker-entrypoint-initdb.d/init.sql
RUN chmod 777 /docker-entrypoint-initdb.d/init.sql

RUN sed -i 's/USERREP/'"$REPUSER"'/g' /docker-entrypoint-initdb.d/init.sql
RUN sed -i 's/PASSREP/'"$REPPASSWORD"'/g' /docker-entrypoint-initdb.d/init.sql