#!/bin/bash 
g++ -o pennant_calculation pennant_calculation.cpp
./pennant_calculation input.csv 10
head output/window_10.csv
