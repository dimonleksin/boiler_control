FROM ubuntu:my
WORKDIR /app
COPY ./* ./
RUN pip3 install -r requiroments.txt && chmod +x ./main.py
CMD flask --app main.py run --host 0.0.0.0