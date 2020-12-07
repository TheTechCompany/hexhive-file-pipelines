FROM nytimes/blender:2.91-cpu-ubuntu18.04

RUN apt-get update && apt-get install -y python3 python3-pip

RUN pip3 install pika pymongo

WORKDIR /glb2glb

ADD script.py .

ADD worker.py .
ADD wait-for-it.sh .

CMD ["./wait-for-it.sh", "rabbit1:5672", "--", "/usr/bin/python3", "worker.py"]
