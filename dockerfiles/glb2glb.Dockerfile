FROM ikester/blender-autobuild:2.82a-bionic


WORKDIR /glb2glb/worker

WORKDIR /glb2glb

ADD script.py .
