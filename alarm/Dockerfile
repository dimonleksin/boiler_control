FROM ubuntu
RUN apt update && apt install -y python3 pip && pip3 install -r ../requiroments.txt && \
mkdir /app
WORKDIR /app
COPY ./* ./
RUN chmod +x ./temp_alarm.py
CMD python3 temp_alarm.py