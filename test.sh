#!/bin/bash
set -e

DATASET=${1:-diabetes}

CORRECT_ICON="\U2705"
WRONG_ICON="\U274C"

./genetic_benchmark "$DATASET" | tee "output/$DATASET.txt"


# Compare only the lines that matter:
# - Lines containing "Test MSE"
# - Lines containing "Program:"
# - Lines containing "Length:"
# - Lines containing "Depth:"
if cmp --silent \
  <(grep -E "Test MSE|Program:|Length:|Depth:" "output/$DATASET.txt") \
  <(grep -E "Test MSE|Program:|Length:|Depth:" "output/${DATASET}_correct.txt"); then
    echo -e "$CORRECT_ICON $DATASET passed"
else
    echo -e "$WRONG_ICON $DATASET failed"
fi