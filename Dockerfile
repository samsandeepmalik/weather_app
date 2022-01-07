FROM python
WORKDIR /weather_app

RUN mkdir -p /weather_app/api
RUN mkdir -p /weather_app/config

RUN ls /weather_app

COPY ./api /weather_app/api
COPY ./config /weather_app/config
COPY ./weather_app.py /weather_app/weather_app.py
COPY ./requirements.txt /weather_app/requirements.txt

RUN pip install -r /weather_app/requirements.txt
RUN mkdir -p /weather_app/log

ENTRYPOINT ["python", "weather_app.py"]