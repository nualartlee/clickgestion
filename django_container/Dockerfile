FROM python:3.6
ENV PYTHONUNBUFFERED 1
RUN mkdir /app
ADD . /app/
WORKDIR /app
RUN pip install -r requirements.txt
RUN pip freeze >> requirements_all.txt
