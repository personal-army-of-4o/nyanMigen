#!/bin/bash

git clone https://github.com/yosysHQ/yosys.git
cd yosys
git checkout 1af994802ed75d5805191113f669409c3872fcf7
docker build .
