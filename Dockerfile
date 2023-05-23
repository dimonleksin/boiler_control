FROM ubuntu
RUN apt update && apt install python3 pip git && pip3 install Flask requests && \
mkdir /app
WORKDIR /app
COPY ./ ./
RUN chmod +x ./run.py
CMD ./run.py