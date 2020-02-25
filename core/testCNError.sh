#!/bin/bash
for (( k = 2; k < 16; k++ )); do
  for (( lim = 5; lim < 60; lim+=5 )); do
    python3 CNError.py $k $lim | tee -a ResultBGRMethod.csv
    # echo "python3 CNError.py $k $lim" | tee test.csv

  done
done
