#!/bin/bash

make clean
make -j

./test.sh diabetes
./test.sh cancer
./test.sh housing