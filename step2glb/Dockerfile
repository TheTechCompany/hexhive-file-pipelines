FROM ubuntu:16.04
RUN apt-get update \
    && apt-get -y install \
        build-essential \
        cmake \
        git \
        vim \
        wget \
        git \
        rapidjson-dev \
        tcl-dev \
        tk-dev \
        libfreetype6-dev \
        libgl1-mesa-dev \
        libxmu-dev \
        libxi-dev

RUN cd / \
    && git clone https://git.dev.opencascade.org/repos/occt.git

RUN cd /occt \
    && git checkout -b docker V7_5_0 \
    && mkdir build

WORKDIR /occt

RUN cmake -G "Unix Makefiles" -D USE_RAPIDJSON:BOOL="ON" .

ADD rapidjson/include/rapidjson /usr/include/rapidjson

RUN echo $(ls /usr/include/rapidjson)

RUN cd /occt \
    && make -j4 install \
    && cd /

WORKDIR /step2glb

ADD step_to_gltf.cxx .
ADD make.sh .

RUN ./make.sh
