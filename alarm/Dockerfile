FROM ubuntu:my
WORKDIR /app
COPY ./requiroments.txt ./
RUN pip3 install -r requiroments.txt
COPY ./* ./
RUN chmod +x ./temp_alarm.py
CMD python3 temp_alarm.py