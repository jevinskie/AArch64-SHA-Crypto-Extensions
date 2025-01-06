#!/usr/bin/env bash

set -e -u -o pipefail

/usr/bin/time -l -h -p picire -i ./pipeline-raw.dot --test ./classifier.sh --parallel -j $(nproc)
