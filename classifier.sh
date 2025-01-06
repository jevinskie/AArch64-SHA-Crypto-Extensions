#!/usr/bin/env bash

# set -e -u -o pipefail
# set -x
# set -u -o pipefail

# timeout --foreground 10
~/code/gfx/graphviz/prefix/bin/dot -vvv -Tdot $1 2>&1 | grep -q "Assertion failed: (aghead(e) != aghead(f)), function fast_edge, file fastgr.c, line 79"

# if [[ $? == 134 ]]; then
#     exit 0
# else
#     exit 1
# fi
