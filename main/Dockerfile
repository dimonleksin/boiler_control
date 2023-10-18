FROM ubuntu:my
WORKDIR /app
COPY ./requiroments.txt ./
RUN pip3 install -r requiroments.txt && chmod +x ./main.py
COPY ./* ./
CMD flask --app main.py run --host 0.0.0.0