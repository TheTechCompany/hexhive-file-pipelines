FROM balbatross/occt:latest

RUN apt-get install clang -y 

WORKDIR /step2glb

ADD step_to_gltf.cxx .
ADD make.sh .

RUN ./make.sh

ADD GA.stp .

ADD worker.py .
RUN apt-get install python -y

RUN pip install pika

CMD python worker.py 
#./step_to_gltf -o GA.glb GA.stp
