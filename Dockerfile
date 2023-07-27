FROM tiangolo/uwsgi-nginx-flask:python3.8

RUN pip install pandas



COPY ./app /app