FROM python:slim
RUN apt-get update && apt-get install -y libtiff5-dev libjpeg62-turbo-dev libopenjp2-7-dev zlib1g-dev \
    libfreetype6-dev liblcms2-dev libwebp-dev tcl8.6-dev tk8.6-dev python3-tk \
    libharfbuzz-dev libfribidi-dev libxcb1-dev
WORKDIR /twitter_clone
COPY ./requirements.txt /twitter_clone/requirements.txt
RUN pip install -r requirements.txt 
COPY . /twitter_clone
CMD bash -c "python manage.py migrate && gunicorn twitter_clone.wsgi -b 0.0.0.0:8000"