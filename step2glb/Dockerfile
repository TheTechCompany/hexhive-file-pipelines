FROM balbatross/occt:latest

RUN apt-get install clang -y 

WORKDIR /step2glb

ADD step_to_gltf.cxx .
ADD make.sh .

RUN ./make.sh

ADD GA.stp .

ADD worker.py .
RUN apt-get install python3 python3-pip -y

RUN pip3 install pika

ADD wait-for-it.sh .

CMD ./wait-for-it.sh rabbit1:5672 -- python3 worker.py 
#./step_to_gltf -o GA.glb GA.stp
