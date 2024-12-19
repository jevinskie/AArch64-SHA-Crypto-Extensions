TARGETS := sha1-arm sha1-arm-O0 sha1-arm-asan sha1-arm-ubsan \
	sha1-arm.ii sha1-wrappers.ii sha1-arm-unrolled.ii \
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
	sha1-arm-O3-no-inline-no-unroll.asm sha1-arm-O3-no-inline-no-unroll-demangled.asm sha1-arm-O3-no-inline-no-unroll.ll sha1-arm-O3-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled.asm sha1-arm-unrolled-demangled.asm sha1-arm-unrolled.ll sha1-arm-unrolled-demangled.ll \
	sha1-arm-unrolled-no-inline.asm sha1-arm-unrolled-no-inline-demangled.asm sha1-arm-unrolled-no-inline.ll sha1-arm-unrolled-no-inline-demangled.ll \
	sha1-arm-unrolled-no-unroll.asm sha1-arm-unrolled-no-unroll-demangled.asm sha1-arm-unrolled-no-unroll.ll sha1-arm-unrolled-no-unroll-demangled.ll \
	sha1-arm-unrolled-no-inline-no-unroll.asm sha1-arm-unrolled-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-no-inline-no-unroll.ll sha1-arm-unrolled-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled-O0.asm sha1-arm-unrolled-O0-demangled.asm sha1-arm-unrolled-O0.ll sha1-arm-unrolled-O0-demangled.ll \
	sha1-arm-unrolled-O0-no-inline.asm sha1-arm-unrolled-O0-no-inline-demangled.asm sha1-arm-unrolled-O0-no-inline.ll sha1-arm-unrolled-O0-no-inline-demangled.ll \
	sha1-arm-unrolled-O0-no-unroll.asm sha1-arm-unrolled-O0-no-unroll-demangled.asm sha1-arm-unrolled-O0-no-unroll.ll sha1-arm-unrolled-O0-no-unroll-demangled.ll \
	sha1-arm-unrolled-O0-no-inline-no-unroll.asm sha1-arm-unrolled-O0-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-O0-no-inline-no-unroll.ll sha1-arm-unrolled-O0-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled-Oz.asm sha1-arm-unrolled-Oz-demangled.asm sha1-arm-unrolled-Oz.ll sha1-arm-unrolled-Oz-demangled.ll \
	sha1-arm-unrolled-Oz-no-inline.asm sha1-arm-unrolled-Oz-no-inline-demangled.asm sha1-arm-unrolled-Oz-no-inline.ll sha1-arm-unrolled-Oz-no-inline-demangled.ll \
	sha1-arm-unrolled-Oz-no-unroll.asm sha1-arm-unrolled-Oz-no-unroll-demangled.asm sha1-arm-unrolled-Oz-no-unroll.ll sha1-arm-unrolled-Oz-no-unroll-demangled.ll \
	sha1-arm-unrolled-Oz-no-inline-no-unroll.asm sha1-arm-unrolled-Oz-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-Oz-no-inline-no-unroll.ll sha1-arm-unrolled-Oz-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled-Os.asm sha1-arm-unrolled-Os-demangled.asm sha1-arm-unrolled-Os.ll sha1-arm-unrolled-Os-demangled.ll \
	sha1-arm-unrolled-Os-no-inline.asm sha1-arm-unrolled-Os-no-inline-demangled.asm sha1-arm-unrolled-Os-no-inline.ll sha1-arm-unrolled-Os-no-inline-demangled.ll \
	sha1-arm-unrolled-Os-no-unroll.asm sha1-arm-unrolled-Os-no-unroll-demangled.asm sha1-arm-unrolled-Os-no-unroll.ll sha1-arm-unrolled-Os-no-unroll-demangled.ll \
	sha1-arm-unrolled-Os-no-inline-no-unroll.asm sha1-arm-unrolled-Os-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-Os-no-inline-no-unroll.ll sha1-arm-unrolled-Os-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled-O2.asm sha1-arm-unrolled-O2-demangled.asm sha1-arm-unrolled-O2.ll sha1-arm-unrolled-O2-demangled.ll \
	sha1-arm-unrolled-O2-no-inline.asm sha1-arm-unrolled-O2-no-inline-demangled.asm sha1-arm-unrolled-O2-no-inline.ll sha1-arm-unrolled-O2-no-inline-demangled.ll \
	sha1-arm-unrolled-O2-no-unroll.asm sha1-arm-unrolled-O2-no-unroll-demangled.asm sha1-arm-unrolled-O2-no-unroll.ll sha1-arm-unrolled-O2-no-unroll-demangled.ll \
	sha1-arm-unrolled-O2-no-inline-no-unroll.asm sha1-arm-unrolled-O2-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-O2-no-inline-no-unroll.ll sha1-arm-unrolled-O2-no-inline-no-unroll-demangled.ll \
	sha1-arm-unrolled-O3.asm sha1-arm-unrolled-O3-demangled.asm sha1-arm-unrolled-O3.ll sha1-arm-unrolled-O3-demangled.ll \
	sha1-arm-unrolled-O3-no-inline.asm sha1-arm-unrolled-O3-no-inline-demangled.asm sha1-arm-unrolled-O3-no-inline.ll sha1-arm-unrolled-O3-no-inline-demangled.ll \
	sha1-arm-unrolled-O3-no-unroll.asm sha1-arm-unrolled-O3-no-unroll-demangled.asm sha1-arm-unrolled-O3-no-unroll.ll sha1-arm-unrolled-O3-no-unroll-demangled.ll \
	sha1-arm-unrolled-O3-no-inline-no-unroll.asm sha1-arm-unrolled-O3-no-inline-no-unroll-demangled.asm sha1-arm-unrolled-O3-no-inline-no-unroll.ll sha1-arm-unrolled-O3-no-inline-no-unroll-demangled.ll \
	sha1-compress-one.ll sha1-compress-one-microcoded.ll

C_CXX_FLAGS := -Wall -Wextra -Wpedantic -Weverything -Warray-bounds -Wno-poison-system-directories -Wno-documentation-unknown-command -Wno-gnu-statement-expression-from-macro-expansion -Wno-gnu-line-marker
C_CXX_FLAGS += -Wno-nullability-extension
C_CXX_FLAGS += -fsafe-buffer-usage-suggestions
C_CXX_FLAGS += -Wno-unsafe-buffer-usage
C_CXX_FLAGS += -mcpu=apple-m1
CFLAGS := $(C_CXX_FLAGS) -std=gnu2x  -Wno-declaration-after-statement -Wno-pre-c2x-compat
CXXFLAGS := $(C_CXX_FLAGS) -std=gnu++2b -fforce-emit-vtables -Wno-c++98-compat-pedantic -Wno-c++20-compat-pedantic -I 3rdparty/cifra
LDFLAGS := -lfmt
ifeq ($(shell uname -s),Darwin)
CXXFLAGS += -isystem /opt/homebrew/opt/fmt/include
LDFLAGS += -L/opt/homebrew/opt/fmt/lib
endif
DBG_FLAGS := -fno-omit-frame-pointer -g3 -gfull -glldb -gcolumn-info -gdwarf-aranges -ggnu-pubnames
VERBOSE_FLAGS := -v -Wl,-v
NOOPT_FLAGS := -O0
FAST_FLAGS := -O3 -fvectorize -funroll-loops
SMOL_FLAGS := -Oz
NOOUTLINE_FLAGS := -mno-outline
ASAN_FLAGS := $(NOOPT_FLAGS) $(DBG_FLAGS) -fsanitize=address -fsanitize-address-use-after-return=always -fsanitize-address-use-after-scope
UBSAN_FLAGS := $(NOOPT_FLAGS) $(DBG_FLAGS) -fsanitize-recover=all -fsanitize=undefined -fsanitize=implicit-integer-truncation -fsanitize=implicit-integer-arithmetic-value-change -fsanitize=implicit-conversion -fsanitize=integer -fsanitize=nullability -fsanitize=float-divide-by-zero -fsanitize=local-bounds
# UBSAN_FLAGS += -fsanitize=implicit-integer-conversion
ASMFLAGS := -fverbose-asm -fno-exceptions -fno-rtti -fno-unwind-tables -fno-asynchronous-unwind-tables -DSHA1_REDIR_DISABLE

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

sha1-cifra.o: 3rdparty/cifra/sha1-cifra.c 3rdparty/cifra/sha1-cifra.h
	$(CC) -c -o $@ $< $(CFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-cifra-O0.o: 3rdparty/cifra/sha1-cifra.c 3rdparty/cifra/sha1-cifra.h
	$(CC) -c -o $@ $< $(CFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-cifra-asan.o: 3rdparty/cifra/sha1-cifra.c 3rdparty/cifra/sha1-cifra.h
	$(CC) -c -o $@ $< $(CFLAGS) $(ASAN_FLAGS)

sha1-cifra-ubsan.o: 3rdparty/cifra/sha1-cifra.c 3rdparty/cifra/sha1-cifra.h
	$(CC) -c -o $@ $< $(CFLAGS) $(UBSAN_FLAGS)

sha1-wrappers.o: sha1-wrappers.cpp sha1-wrappers.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-wrappers-O0.o: sha1-wrappers.cpp sha1-wrappers.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-wrappers-asan.o: sha1-wrappers.cpp sha1-wrappers.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(ASAN_FLAGS)

sha1-wrappers-ubsan.o: sha1-wrappers.cpp sha1-wrappers.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(UBSAN_FLAGS)

sha1-arm-unrolled.o: sha1-arm-unrolled.cpp sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-arm-unrolled-O0.o: sha1-arm-unrolled.cpp sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-arm-unrolled-asan.o: sha1-arm-unrolled.cpp sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(ASAN_FLAGS)

sha1-arm-unrolled-ubsan.o: sha1-arm-unrolled.cpp sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(UBSAN_FLAGS)

sha1-arm.o: sha1-arm.cpp sha1-wrappers.h sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-arm-O0.o: sha1-arm.cpp sha1-wrappers.h sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-arm-asan.o: sha1-arm.cpp sha1-wrappers.h sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(ASAN_FLAGS)

sha1-arm-ubsan.o: sha1-arm.cpp sha1-wrappers.h sha1-arm-unrolled.h
	$(CXX) -c -o $@ $< $(CXXFLAGS) $(UBSAN_FLAGS)

sha1-arm: sha1-arm.o teeny-sha1.o sha1-cifra.o sha1-wrappers.o sha1-arm-unrolled.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LDFLAGS) $(SMOL_FLAGS) $(NOOUTLINE_FLAGS)

sha1-arm-O0: sha1-arm-O0.o teeny-sha1-O0.o sha1-cifra-O0.o sha1-wrappers-O0.o sha1-arm-unrolled-O0.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LDFLAGS) $(NOOPT_FLAGS) $(DBG_FLAGS)

sha1-arm-asan: sha1-arm-asan.o teeny-sha1-asan.o sha1-cifra-asan.o sha1-wrappers-asan.o sha1-arm-unrolled-asan.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LDFLAGS) $(ASAN_FLAGS)

sha1-arm-ubsan: sha1-arm-ubsan.o teeny-sha1-ubsan.o sha1-cifra-ubsan.o sha1-wrappers-ubsan.o sha1-arm-unrolled-ubsan.o
	$(CXX) -o $@ $^ $(CXXFLAGS) $(LDFLAGS) $(UBSAN_FLAGS)

run-asan: sha1-arm-asan
	ASAN_OPTIONS=print_stacktrace=1 ./$^

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

%.dot.png: %.dot
	dot -o$@ -Tpng $^

%.dot.pdf: %.dot
	dot -o$@ -Tpdf $^

sha1-compress-one.ll: sha1-arm-unrolled-O3.ll
	llvm-extract -o $(basename $@)_extract.bc --func=sha1_arm_unrolled_compress_one $^
	llvm-dis -o $@ $(basename $@)_extract.bc
	rm $(basename $@)_extract.bc

sha1-compress-one-microcoded.ll: sha1-arm-unrolled-O3.ll
	llvm-extract -o $(basename $@)_extract.bc --func=sha1_arm_unrolled_compress_one_microcoded $^
	llvm-dis -o $@ $(basename $@)_extract.bc
	rm $(basename $@)_extract.bc
compile_commands.json:
	bear -- $(MAKE) -B -f $(MAKEFILE_LIST) RUNNING_BEAR=1
	$(MAKE) -f $(MAKEFILE_LIST) clean-targets

scan:
	scan-build -V $(MAKE) -B -f $(MAKEFILE_LIST)

tidy:
	clang-tidy sha1-arm.cpp
