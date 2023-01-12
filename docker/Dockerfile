FROM ubuntu:20.04

RUN apt-get update && apt-get install -y python3.9
RUN apt-get update && apt-get install -y python3-pip

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
ENTRYPOINT [ "streamlit", "run"]
CMD ["/app/src/main.py"]
EXPOSE 8501
