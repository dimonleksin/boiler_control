FROM ubuntu
RUN apt update && apt install -y python3 pip git && pip3 install Flask requests bs4 && \
mkdir /app
WORKDIR /app
COPY ./* ./
RUN chmod +x ./temp_alarm.py
CMD python3 temp_alarm.py