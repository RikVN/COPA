#!/bin/bash

# Put COPA data sets in correct format for run_copa.py (JSON)
# Just keep all the data (-d all)

for lang in bg mk tr is mt; do
    for type in train dev test; do
        python src/copa_to_json.py -d all -i data/${lang}.copa.${type} -o data/${lang}.copa.${type}.all.json
    done
done
