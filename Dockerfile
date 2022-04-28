FROM python:3.10
WORKDIR /usr/src/app
COPY requirements.txt ./requiremetns.txt
RUN pip install -r requirements.txt --no-cache-dir
ADD . /usr/src/app
RUN chmod a+x entrypoint.sh
EXPOSE 5000
CMD [ "/bin/sh", "entrypoint.sh" ]