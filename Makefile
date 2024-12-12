TARGETS := sha1-arm sha1-arm-O0 sha1-arm-asan sha1-arm-ubsan \
	sha1-arm.ii \
	sha1-arm.asm sha1-arm-demangled.asm sha1-arm.ll sha1-arm-demangled.ll \
	sha1-arm-no-inline.asm sha1-arm-no-inline-demangled.asm sha1-arm-no-inline.ll sha1-arm-no-inline-demangled.ll \
	sha1-arm-no-unroll.asm sha1-arm-no-unroll-demangled.asm sha1-arm-no-unroll.ll sha1-arm-no-unroll-demangled.ll \
	sha1-arm-no-inline-no-unroll.asm sha1-arm-no-inline-no-unroll-demangled.asm sha1-arm-no-inline-no-unroll.ll sha1-arm-no-inline-no-unroll-demangled.ll \
	sha1-arm-O0.asm sha1-arm-O0-demangled.asm sha1-arm-O0.ll sha1-arm-O0-demangled.ll \
	sha1-arm-O0-no-inline.asm sha1-arm-O0-no-inline-demangled.asm sha1-arm-O0-no-inline.ll sha1-arm-O0-no-inline-demangled.ll \
	sha1-arm-O0-no-unroll.asm sha1-arm-O0-no-unroll-demangled.asm sha1-arm-O0-no-unroll.ll sha1-arm-O0-no-unroll-demangled.ll \
	sha1-arm-O0-no-inline-no-unroll.asm sha1-arm-O0-no-inline-no-unroll-demangled.asm sha1-arm-O0-no-inline-no-unroll.ll sha1-arm-O0-no-inline-no-unroll-demangled.ll \
	sha1-arm-Oz.asm sha1-arm-Oz-demangled.asm sha1-arm-Oz.ll sha1-arm-Oz-demangled.ll \
	sha1-arm-Oz-no-inline.asm sha1-arm-Oz-no-inline-demangled.asm sha1-arm-Oz-no-inline.ll sha1-arm-Oz-no-inline-demangled.ll \
	sha1-arm-Oz-no-unroll.asm sha1-arm-Oz-no-unroll-demangled.asm sha1-arm-Oz-no-unroll.ll sha1-arm-Oz-no-unroll-demangled.ll \
	sha1-arm-Oz-no-inline-no-unroll.asm sha1-arm-Oz-no-inline-no-unroll-demangled.asm sha1-arm-Oz-no-inline-no-unroll.ll sha1-arm-Oz-no-inline-no-unroll-demangled.ll \
	sha1-arm-Os.asm sha1-arm-Os-demangled.asm sha1-arm-Os.ll sha1-arm-Os-demangled.ll \
	sha1-arm-Os-no-inline.asm sha1-arm-Os-no-inline-demangled.asm sha1-arm-Os-no-inline.ll sha1-arm-Os-no-inline-demangled.ll \
	sha1-arm-Os-no-unroll.asm sha1-arm-Os-no-unroll-demangled.asm sha1-arm-Os-no-unroll.ll sha1-arm-Os-no-unroll-demangled.ll \
	sha1-arm-Os-no-inline-no-unroll.asm sha1-arm-Os-no-inline-no-unroll-demangled.asm sha1-arm-Os-no-inline-no-unroll.ll sha1-arm-Os-no-inline-no-unroll-demangled.ll \
	sha1-arm-O2.asm sha1-arm-O2-demangled.asm sha1-arm-O2.ll sha1-arm-O2-demangled.ll \
	sha1-arm-O2-no-inline.asm sha1-arm-O2-no-inline-demangled.asm sha1-arm-O2-no-inline.ll sha1-arm-O2-no-inline-demangled.ll \
	sha1-arm-O2-no-unroll.asm sha1-arm-O2-no-unroll-demangled.asm sha1-arm-O2-no-unroll.ll sha1-arm-O2-no-unroll-demangled.ll \
	sha1-arm-O2-no-inline-no-unroll.asm sha1-arm-O2-no-inline-no-unroll-demangled.asm sha1-arm-O2-no-inline-no-unroll.ll sha1-arm-O2-no-inline-no-unroll-demangled.ll \
	sha1-arm-O3.asm sha1-arm-O3-demangled.asm sha1-arm-O3.ll sha1-arm-O3-demangled.ll \
	sha1-arm-O3-no-inline.asm sha1-arm-O3-no-inline-demangled.asm sha1-arm-O3-no-inline.ll sha1-arm-O3-no-inline-demangled.ll \
	sha1-arm-O3-no-unroll.asm sha1-arm-O3-no-unroll-demangled.asm sha1-arm-O3-no-unroll.ll sha1-arm-O3-no-unroll-demangled.ll \
	sha1-arm-O3-no-inline-no-unroll.asm sha1-arm-O3-no-inline-no-unroll-demangled.asm sha1-arm-O3-no-inline-no-unroll.ll sha1-arm-O3-no-inline-no-unroll-demangled.ll


C_CXX_FLAGS := -Wall -Wextra -Wpedantic -Weverything -Warray-bounds -Wno-poison-system-directories -Wno-documentation-unknown-command -Wno-gnu-statement-expression-from-macro-expansion
C_CXX_FLAGS += -Wno-nullability-extension
C_CXX_FLAGS += -fsafe-buffer-usage-suggestions
C_CXX_FLAGS += -Wno-unsafe-buffer-usage
C_CXX_FLAGS += -mcpu=apple-m1
CFLAGS := $(C_CXX_FLAGS) -std=gnu2x  -Wno-declaration-after-statement -Wno-pre-c2x-compat
CXXFLAGS := $(C_CXX_FLAGS) -std=gnu++2b -Wno-c++98-compat-pedantic -Wno-c++20-compat-pedantic -I 3rdparty/cifra
DBG_FLAGS := -fno-omit-frame-pointer -g3 -gfull -glldb -gcolumn-info -gdwarf-aranges -ggnu-pubnames
VERBOSE_FLAGS := -v -Wl,-v
NOOPT_FLAGS := -O0
FAST_FLAGS := -O3 -fvectorize -funroll-loops
SMOL_FLAGS := -Oz
NOOUTLINE_FLAGS := -mno-outline
ASAN_FLAGS := $(NOOPT_FLAGS) $(DBG_FLAGS) -fsanitize=address -fsanitize-address-use-after-return=always -fsanitize-address-use-after-scope
UBSAN_FLAGS := $(NOOPT_FLAGS) $(DBG_FLAGS) -fsanitize-recover=all -fsanitize=undefined -fsanitize=implicit-integer-truncation -fsanitize=implicit-integer-arithmetic-value-change -fsanitize=implicit-conversion -fsanitize=integer -fsanitize=nullability -fsanitize=float-divide-by-zero -fsanitize=local-bounds
# UBSAN_FLAGS += -fsanitize=implicit-integer-conversion
ASMFLAGS := -fverbose-asm -fno-exceptions -fno-rtti -fno-unwind-tables -fno-asynchronous-unwind-tables

all: $(TARGETS)

.PHONY: clean-targets clean-compile-commands clean compile_commands.json scan tidy run-asan run-ubsan

clean-targets:
	rm -rf *.dSYM/
	rm -f $(TARGETS)
	rm -rf *.o

clean-compile-commands:
	rm -f compile_commands.json

clean: clean-targets clean-compile-commands

teeny-sha1.o: 3rdparty/teeny-sha1/teeny-sha1.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

teeny-sha1-O0.o: 3rdparty/teeny-sha1/teeny-sha1.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

teeny-sha1-asan.o: 3rdparty/teeny-sha1/teeny-sha1.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(ASAN_FLAGS)

teeny-sha1-ubsan.o: 3rdparty/teeny-sha1/teeny-sha1.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(UBSAN_FLAGS)

sha1-cifra.o: 3rdparty/cifra/sha1-cifra.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-cifra-O0.o: 3rdparty/cifra/sha1-cifra.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-cifra-asan.o: 3rdparty/cifra/sha1-cifra.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(ASAN_FLAGS)

sha1-cifra-ubsan.o: 3rdparty/cifra/sha1-cifra.c
	$(CC) -c -o $@ $^ $(CFLAGS) $(UBSAN_FLAGS)

sha1-arm: sha1-arm.cpp teeny-sha1.o sha1-cifra.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-arm-O0: sha1-arm.cpp teeny-sha1-O0.o sha1-cifra-O0.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-arm-asan: sha1-arm.cpp teeny-sha1-asan.o sha1-cifra-asan.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(ASAN_FLAGS)

run-asan: sha1-arm-asan
	ASAN_OPTIONS=print_stacktrace=1 ./$^

sha1-arm-ubsan: sha1-arm.cpp teeny-sha1-ubsan.o sha1-cifra-ubsan.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(UBSAN_FLAGS)

run-ubsan: sha1-arm-ubsan
	UBSAN_OPTIONS=print_stacktrace=1 ./$^


%.ii: %.cpp
	$(CXX) -o $@ $^ $(CXXFLAGS) -E


%.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS)

%.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS)

%-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-inline

%-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-inline

%-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-O0.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS)

%-O0.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS)

%-O0-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-inline

%-O0-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-inline

%-O0-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O0-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O0-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-O0-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O0 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-Oz.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS)

%-Oz.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS)

%-Oz-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-inline

%-Oz-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-inline

%-Oz-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-Oz-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-Oz-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-Oz-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Oz $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-Os.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS)

%-Os.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS)

%-Os-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-inline

%-Os-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-inline

%-Os-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-Os-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-Os-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-Os-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -Os $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-O2.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS)

%-O2.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS)

%-O2-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-inline

%-O2-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-inline

%-O2-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O2-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O2-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-O2-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O2 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-O3.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS)

%-O3.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS)

%-O3-no-inline.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-inline

%-O3-no-inline.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-inline

%-O3-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O3-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-unroll-loops

%-O3-no-inline-no-unroll.asm: %.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops

%-O3-no-inline-no-unroll.ll: %.cpp
	$(CXX) -emit-llvm -S -o $@ $^ $(CXXFLAGS) $(ASMFLAGS) -O3 $(NOOUTLINE_FLAGS) -fno-inline -fno-unroll-loops


%-demangled.asm: %.asm
	c++filt -t < $^ | c++filt -n -t | c++filt -t > $@

%-demangled.ll: %.ll
	c++filt -t < $^ | c++filt -n -t | c++filt -t > $@


compile_commands.json:
	bear -- $(MAKE) -B -f $(MAKEFILE_LIST) RUNNING_BEAR=1
	$(MAKE) -f $(MAKEFILE_LIST) clean-targets

scan:
	scan-build -V $(MAKE) -B -f $(MAKEFILE_LIST)

tidy:
	clang-tidy sha1-arm.cpp
