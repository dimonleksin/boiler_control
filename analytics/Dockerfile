FROM ubuntu:my
WORKDIR /app
COPY ./requiroments.txt ./
RUN pip3 install -r requiroments.txt
COPY ./* ./
RUN chmod +x ./analytics.py
CMD python3 analytics.py