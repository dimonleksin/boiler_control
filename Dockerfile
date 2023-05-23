FROM ubuntu
ARG FLASK_APP=/app/main.py
RUN apt update && apt install -y python3 pip git && pip3 install Flask requests && \
mkdir /app
WORKDIR /app
COPY ./ ./
RUN chmod +x ./run.py
CMD flask run