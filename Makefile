TARGETS := sha1-arm-test \
	sha1-arm-test.asm sha1-arm-test-demangled.asm \
	sha1-arm-test-no-inline.asm sha1-arm-test-no-inline-demangled.asm

CXXFLAGS := -Wall -Wextra -Wpedantic -Weverything -Warray-bounds -Wno-c++98-compat-pedantic -Wno-c++20-compat-pedantic -Wno-poison-system-directories -std=c++2b
CXXFLAGS += -fsafe-buffer-usage-suggestions
# CXXFLAGS += -g3 -gfull -glldb -gcolumn-info -gdwarf-aranges -ggnu-pubnames
# CXXFLAGS += -O0
# CXXFLAGS += -v -Wl,-v
# CXXFLAGS += -O3 -fvectorize -funroll-loops
CXXFLAGS += -Oz
# CXXFLAGS += -fsanitize=address
CXXFLAGS += -mcpu=apple-m1

all: $(TARGETS)

.PHONY: clean compile_commands.json scan tidy

clean:
	rm -rf *.dSYM/
	rm -f $(TARGETS)
	rm -f compile_commands.json

ssha1-arm-test: sha1-arm-test.cpp
	$(CXX) -o $@ $^ $(CXXFLAGS)

sha1-arm-test.asm: sha1-arm-test.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) -fverbose-asm -fno-exceptions -fno-rtti -fno-unwind-tables -fno-asynchronous-unwind-tables -mno-outline

sha1-arm-test-no-inline.asm: sha1-arm-test.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) -fverbose-asm -fno-exceptions -fno-rtti -fno-unwind-tables -fno-asynchronous-unwind-tables -fno-inline -mno-outline

%-demangled.asm: %.asm
	c++filt -t < $^ | c++filt -n -t | c++filt -t > $@

compile_commands.json:
	bear -- $(MAKE) -B -f $(MAKEFILE_LIST)

scan:
	scan-build -V $(MAKE) -B -f $(MAKEFILE_LIST)

tidy:
	clang-tidy sha1-arm-test.cpp
