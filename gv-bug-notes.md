
```
gv_calloc(1, 32) = 0x10e44c210
gv_calloc(1, 16) = 0x10b6e5970
network simplex: 4 nodes 4 edges 1 iter 0.00 sec
Maxrank = 1, minrank = 0
gv_calloc(3, 8) = 0x10e44c1e0
gv_calloc(3, 4) = 0x10b6e5950
gv_calloc(2, 8) = 0x10b6e5930
gv_calloc(1, 104) = 0x10e934440
gv_calloc(1, 472) = 0x105776a00
gv_calloc(5, 8) = 0x10e68c990
gv_calloc(5, 8) = 0x10e68c950
gv_calloc(3, 8) = 0x10e44c1b0
gv_calloc(1, 104) = 0x10e934390
Process 76019 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BREAKPOINT (code=1, subcode=0x105299e10)
    frame #0: 0x0000000105299e14 libgvplugin_dot_layout.6.0.0.dylib` gv_calloc(nmemb=1, size=104)  + 352 at alloc.h:40
   37      fprintf(stderr, "gv_calloc(%zu, %zu) = %p\n", nmemb, size, p);
   38      if (((uintptr_t)p) == 0x10e934390) {
   39        __builtin_debugtrap();
-> 40      }
   41      if (nmemb > 0 && size > 0 && p == NULL) {
   42        fprintf(stderr,
   43                "out of memory when trying to allocate %" PRISIZE_T " bytes\n",
Target 0: (dot) stopped.
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = EXC_BREAKPOINT (code=1, subcode=0x105299e10)
  * frame #0: 0x0000000105299e14 libgvplugin_dot_layout.6.0.0.dylib` gv_calloc(nmemb=1, size=104)  + 352 at alloc.h:40
    frame #1: 0x00000001052989c8 libgvplugin_dot_layout.6.0.0.dylib` gv_alloc(size=104)  + 28 at alloc.h:51
    frame #2: 0x0000000105299684 libgvplugin_dot_layout.6.0.0.dylib` virtual_node(g=0x0000000104300ad0)  + 44 at fastgr.c:204
    frame #3: 0x0000000105238270 libgvplugin_dot_layout.6.0.0.dylib` build_skeleton(g=0x0000000104300ad0, subg=0x0000000104300930)  + 728 at cluster.c:361
    frame #4: 0x000000010522eb84 libgvplugin_dot_layout.6.0.0.dylib` class2(g=0x0000000104300ad0)  + 604 at class2.c:170
    frame #5: 0x00000001052a919c libgvplugin_dot_layout.6.0.0.dylib` init_mincross(g=0x0000000104300ad0)  + 444 at mincross.c:1050
    frame #6: 0x00000001052a88e8 libgvplugin_dot_layout.6.0.0.dylib` dot_mincross(g=0x0000000104300ad0)  + 1404 at mincross.c:372
    frame #7: 0x0000000105251a70 libgvplugin_dot_layout.6.0.0.dylib` dotLayout(g=0x0000000104300ad0)  + 192 at dotinit.c:310
    frame #8: 0x0000000105250b74 libgvplugin_dot_layout.6.0.0.dylib` doDot(g=0x0000000104300ad0)  + 480 at dotinit.c:444
    frame #9: 0x000000010525097c libgvplugin_dot_layout.6.0.0.dylib` dot_layout(g=0x0000000104300ad0)  + 48 at dotinit.c:492
    frame #10: 0x00000001008f2e70 libgvc.6.0.0.dylib` gvLayoutJobs(gvc=0x0000000103703980, g=0x0000000104300ad0)  + 1356 at gvlayout.c:84
    frame #11: 0x0000000100003948 dot` main(argc=4, argv=0x000000016fdfd058)  + 456 at dot.c:72
    frame #12: 0x0000000187ac50e0 dyld` start  + 2360
(lldb) f 2
frame #2: 0x0000000105299684 libgvplugin_dot_layout.6.0.0.dylib` virtual_node(g=0x0000000104300ad0)  + 44 at fastgr.c:204
   201   }
   202
   203   node_t *virtual_node(graph_t *g) {
-> 204       node_t *n = gv_alloc(sizeof(node_t));
   205       AGTYPE(n) = AGNODE;
   206       n->base.data = gv_alloc(sizeof(Agnodeinfo_t));
   207       n->root = agroot(g);
(lldb) c
Process 76019 resuming
gv_calloc(1, 472) = 0x105776780
gv_calloc(5, 8) = 0x10e68c910
gv_calloc(5, 8) = 0x10e68c8d0
gv_calloc(1, 128) = 0x10afdbb80
gv_calloc(1, 240) = 0x10ec0c700
gv_calloc(3, 4) = 0x10b6e5890
gv_calloc(3, 88) = 0x103a17140
gv_calloc(2, 8) = 0x10b6e5870
gv_calloc(3, 8) = 0x10e44c180
mincross: pass 0 iter 0 trying 0 cur_cross 0 best_cross 0
merge2: graph g, rank 0 has only 1 < 2 nodes
merge2: graph g, rank 1 has only 1 < 3 nodes
gv_calloc(1, 8) = 0x10b6e5810
gv_calloc(2, 4) = 0x10b6e57f0
gv_calloc(2, 88) = 0x10acbf260
gv_calloc(2, 8) = 0x10b6e57d0
delete_fast_node: g: 0x104300a00 n: 0x1001003b0
gv_calloc(1, 128) = 0x10afdbac0
gv_calloc(1, 240) = 0x10ec0c5c0
gv_calloc(1, 128) = 0x10afdba00
gv_calloc(1, 240) = 0x10ec0c480
Assertion failed: (aghead(e) != aghead(f)), function fast_edge, file fastgr.c, line 79.
Process 76019 stopped
* thread #1, queue = 'com.apple.main-thread', stop reason = hit program assert
    frame #4: 0x0000000105293d30 libgvplugin_dot_layout.6.0.0.dylib` fast_edge(e=0x000000010afdba00)  + 1088 at fastgr.c:79
   76                fprintf(stderr, "duplicate fast edge\n");
   77                return 0;
   78            }
-> 79            assert(aghead(e) != aghead(f));
   80        }
   81        for (i = 0; (f = ND_in(aghead(e)).list[i]); i++) {
   82            if (e == f) {
Target 0: (dot) stopped.
(lldb) p e
(edge_t *) 0x000000010afdba00
(lldb) p f
(edge_t *) 0x000000010afdbac0
(lldb) expr aghead(e)
(Agnode_t *) $0 = 0x000000010e934390
(lldb) expr aghead(f)
(Agnode_t *) $1 = 0x000000010e934390
(lldb) bt
* thread #1, queue = 'com.apple.main-thread', stop reason = hit program assert
    frame #0: 0x0000000187e0e0dc libsystem_kernel.dylib` __pthread_kill  + 8
    frame #1: 0x0000000187e45cc0 libsystem_pthread.dylib` pthread_kill  + 288
    frame #2: 0x0000000187d51a40 libsystem_c.dylib` abort  + 180
    frame #3: 0x0000000187d50d30 libsystem_c.dylib` __assert_rtn  + 284
  * frame #4: 0x0000000105293d30 libgvplugin_dot_layout.6.0.0.dylib` fast_edge(e=0x000000010afdba00)  + 1088 at fastgr.c:79
    frame #5: 0x0000000105298a00 libgvplugin_dot_layout.6.0.0.dylib` virtual_edge(u=0x00000001001003b0, v=0x000000010e934390, orig=0x0000000103b03880)  + 44 at fastgr.c:174
    frame #6: 0x000000010523cfc0 libgvplugin_dot_layout.6.0.0.dylib` map_path(from=0x00000001001003b0, to=0x000000010e934390, orig=0x0000000103b03880, ve=0x000000010afdbac0, type=5)  + 5064 at cluster.c:121
    frame #7: 0x000000010523b81c libgvplugin_dot_layout.6.0.0.dylib` make_interclust_chain(from=0x00000001001003b0, to=0x0000000100100250, orig=0x0000000103b03880)  + 304 at cluster.c:154
    frame #8: 0x0000000105236c28 libgvplugin_dot_layout.6.0.0.dylib` interclexp(subg=0x0000000104300a00)  + 4492 at cluster.c:208
    frame #9: 0x0000000105234700 libgvplugin_dot_layout.6.0.0.dylib` expand_cluster(subg=0x0000000104300a00)  + 840 at cluster.c:303
    frame #10: 0x00000001052aaa50 libgvplugin_dot_layout.6.0.0.dylib` mincross_clust(g=0x0000000104300a00, scratch=0x000000016fdfc540)  + 44 at mincross.c:547
    frame #11: 0x00000001052a8b80 libgvplugin_dot_layout.6.0.0.dylib` dot_mincross(g=0x0000000104300ad0)  + 2068 at mincross.c:386
    frame #12: 0x0000000105251a70 libgvplugin_dot_layout.6.0.0.dylib` dotLayout(g=0x0000000104300ad0)  + 192 at dotinit.c:310
    frame #13: 0x0000000105250b74 libgvplugin_dot_layout.6.0.0.dylib` doDot(g=0x0000000104300ad0)  + 480 at dotinit.c:444
    frame #14: 0x000000010525097c libgvplugin_dot_layout.6.0.0.dylib` dot_layout(g=0x0000000104300ad0)  + 48 at dotinit.c:492
    frame #15: 0x00000001008f2e70 libgvc.6.0.0.dylib` gvLayoutJobs(gvc=0x0000000103703980, g=0x0000000104300ad0)  + 1356 at gvlayout.c:84
    frame #16: 0x0000000100003948 dot` main(argc=4, argv=0x000000016fdfd058)  + 456 at dot.c:72
    frame #17: 0x0000000187ac50e0 dyld` start  + 2360
```
