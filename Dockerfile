FROM python:3.10-alpine
WORKDIR /usr/src/app
COPY ./ /usr/src/app
RUN pip install -r requirements.txt --no-cache-dir
EXPOSE 5000
CMD python app.py