FROM ubuntu
RUN apt update && apt install -y python3 pip && mkdir /app
WORKDIR /app
COPY ./* ./
COPY ../requiroments.txt /app/
RUN pip3 install -r requiroments.txt && chmod +x ./temp_alarm.py
CMD python3 temp_alarm.py