FROM nytimes/blender:2.91-cpu-ubuntu18.04

WORKDIR /glb2glb/worker

WORKDIR /glb2glb

ADD script.py .
