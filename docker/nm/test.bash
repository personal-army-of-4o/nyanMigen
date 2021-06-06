#/bin/bash

sudo docker run -v `pwd`/../examples:/workdir nm python3 /workdir/blink.py generate -t v
