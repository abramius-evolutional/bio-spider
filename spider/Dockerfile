FROM python:3.5
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
WORKDIR /code
ADD requirements.txt /code/
RUN apt-get update && apt-get install -y cron
RUN pip install -r requirements.txt
ADD run_spider.sh /code/
ADD run.sh /code/
RUN echo "*/10 * * * * sh /code/run_spider.sh >> /var/log/cron.log 2>&1" >> /var/spool/cron/crontabs/root
RUN chmod 600 /var/spool/cron/crontabs/root
RUN touch /var/log/cron.log