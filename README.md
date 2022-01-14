nsfw-server
===========

This project uses [Yahoo Open NSFW (Not Safe For Work)](https://github.com/yahoo/open_nsfw) to detect images that contain pornographic content.
OpenNSFW uses Caffe pretrained neural network models and has a very big success rate.

Since I found Caffe difficult to install, I modified the [Caffe Docker](https://github.com/BVLC/caffe/tree/master/docker) to create this project to run Yahoo Open NSFW. I have also modified the Yahoo script to accept remote urls instead of only local images.

You can use it command line or start the build in server. The output is a float number from 0-1. Scores above 0.8 are NSFW. Everything below 0.2 is completely clean.

Installation
============

To install:

- Clone the project.
- Install [Docker](https://www.docker.com/) - [Ubuntu instructions here](https://docs.docker.com/install/linux/docker-ce/ubuntu/)
- Run sudo ./build_docker.sh (This will take some time)

Run
===
- As a web service (./run_server.sh as root):
    
        docker run -ti -p 28000:28000 caffe:cpu  python server.py 7981

Then to use the service:

Visit: http://127.0.0.1:28000/[url] (Image link after final /)

For example: [http://127.0.0.1:28000/http://www.personal.psu.edu/jul229/mini.jpg](http://127.0.0.1:28000/http://www.personal.psu.edu/jul229/mini.jpg)
