FROM node:14-alpine3.10

RUN npm i -g gltfpack

WORKDIR /gltfpack

ADD exported.glb .

CMD gltfpack -i exported.glb -c -tc -o packed.glb

