#!/bin/bash

cd trec_eval-9.0.7
make
echo "RRF accuracies"
./trec_eval -m map -m P.5,10 qrels.txt rrf.txt
echo "Bordacount accuracies"
./trec_eval -m map -m P.5,10 qrels.txt bordacount.txt
echo "Condorcet accuracies"
./trec_eval -m map -m P.5,10 qrels.txt condorcet.txt
echo "Bayesfuse accuracies"
./trec_eval -m map -m P.5,10 qrels.txt bayesfuse.txt
echo "WeightedBordaFuse accuracies"
./trec_eval -m map -m P.5,10 qrels.txt weightedbordafuse.txt
cd ..

# replace text file locations if needed
# For speeding up evaluation of quality of rank aggregation