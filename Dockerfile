FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install pandas


COPY ./app /app

# 并将/app目录中的文件权限设为可读可写
RUN chmod -R 777 /app
