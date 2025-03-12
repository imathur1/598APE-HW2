#!/bin/bash
set -e

DATASET=${1:-diabetes}

CORRECT_ICON="\U2705"
WRONG_ICON="\U274C"

./genetic_benchmark "$DATASET" > "output/$DATASET.txt"

# Compare all lines except the last one, which has the runtime
if cmp --silent <(head -n -1 "output/$DATASET.txt") <(head -n -1 "output/${DATASET}_correct.txt"); then
    echo -e "$CORRECT_ICON $DATASET passed"
else
    echo -e "$WRONG_ICON $DATASET failed"
fi