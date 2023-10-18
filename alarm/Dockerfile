FROM ubuntu:my
WORKDIR /app
COPY ./requiroments.txt ./
RUN pip3 install -r requiroments.txt && chmod +x ./temp_alarm.py
COPY ./* ./
CMD python3 temp_alarm.py