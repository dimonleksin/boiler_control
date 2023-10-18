FROM ubuntu:my
WORKDIR /app
COPY ./requiroments.txt ./
RUN pip3 install -r requiroments.txt
COPY ./* ./
RUN chmod +x ./main.py
CMD flask --app main.py run --host 0.0.0.0