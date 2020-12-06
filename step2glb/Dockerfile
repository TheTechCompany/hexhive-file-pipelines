FROM balbatross/occt:latest

RUN apt-get install clang -y 

WORKDIR /step2glb

ADD step_to_gltf.cxx .
ADD make.sh .

RUN ./make.sh

ADD GA.stp .

CMD ./step_to_gltf -o GA.glb GA.stp
