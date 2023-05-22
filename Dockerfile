FROM ubuntu
RUN apt update && apt install python3 pip git && pip3 install Flask requests