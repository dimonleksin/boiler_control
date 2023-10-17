FROM ubuntu
RUN apt update && apt install -y python3 pip git && pip3 install -r ../requiroments.txt && \
mkdir /app
WORKDIR /app
COPY ./* ./
RUN chmod +x ./main.py
CMD flask --app main.py run --host 0.0.0.0