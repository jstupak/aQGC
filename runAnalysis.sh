#!/bin/bash -x

if [ $# -lt 2 ]; then 
    echo "Usage: ./runAnalysis.sh <input pattern> <tag> [analysis script]"
    echo "Example: ./runAnalysis.sh 'PROC_sm_*/Events/run_*/unweighted_events.root' foo"
    exit
fi

inputs=$1
tag=$2
if [ $# -gt 2 ]; then
    analysisScript=$3
else
    analysisScript=$aQGCWorkDir/aQGC/analyzeDelphes.py
fi

for input in `ls $inputs`; do 
    python $analysisScript $input $tag
done
