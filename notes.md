# Notes
## Commands
```bash
./dag.py -i sha1-compress-one-hand.ll -o sha1-compress-one-hand-dag.ll -d sha1-compress-one-hand-dag.dot -D sha1-compress-one-hand-dag-ops.dot -s sched2.xlsx -r sha1-regalloc2.txt -g sha1-compress-one-hand-graph-g.json -G sha1-compress-one-hand-graph-G.json -f sha1-compress-one-hand-graph-f.json -F sha1-compress-one-hand-graph-F.json
```

## EU Port Usage
```python
instr_port_uses = {
    'sha1c'  : [ None,
                {'sha1h': {'d1': 3, 'd2': 1}},
                {'vaddX': {'d1': 1, 'd2': 1}, 'vaddY': {'d2': 1, 'd3': 1}, 'vaddXY': {'d3': 1}}],

    'sha1h'  : [{'sha1c': {'d1': 5}, 'sha1p': {'d1': 9}, 'sha1m': {'d1': 5}}],

    'sha1m'  : [{'sha1p': {'d1': 1}},
                {'sha1h': {'d1': 5}},
                {'vaddXY': {'d3': 5}}],

    'sha1p'  : [{'sha1c': {'d1': 1}, 'sha1m': {'d1': 1}},
                {'sha1h': {'d1': 10}},
                {'vaddXY': {'d3': 10}}],

    'sha1su0': [{'sha1su1': {'d3': 12}},
                {'sha1su1': {'d2': 13}},
                {'sha1su1': {'d1': 14}}],

    'sha1su1': [{'sha1su0': {'d1': 16}},
                {'sha1su1': {'d1': 15}}],

    'vaddX'  : [ None,
                 None],

    'vaddXY' : [{'sha1su1': {'d1': 16}},
                 None],

    'vaddY'  : [ None,
                 None]
}
```
