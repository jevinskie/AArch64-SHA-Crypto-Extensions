TARGETS := sha1-arm-test sha1-arm-test.asm

CXXFLAGS := -Wall -Wextra -Wpedantic -Weverything -Wno-c++98-compat -Wno-poison-system-directories -std=c++2b
CXXFLAGS += -g3 -gfull -glldb -gcolumn-info -gdwarf-aranges -ggnu-pubnames
CXXFLAGS += -O0
# CXXFLAGS += -v -Wl,-v
# CXXFLAGS += -O3 -fvectorize -funroll-loops
CXXFLAGS += -fsanitize=address

all: $(TARGETS)

.PHONY: clean compile_commands.json scan tidy

clean:
	rm -rf *.dSYM/
	rm -f $(TARGETS)
	rm -f compile_commands.json

ssha1-arm-test: sha1-arm-test.cpp
	$(CXX) -o $@ $^ $(CXXFLAGS)

sha1-arm-test.asm: sha1-arm-test.cpp
	$(CXX) -S -o $@ $^ $(CXXFLAGS) -fverbose-asm -fno-exceptions -fno-rtti -fno-unwind-tables -fno-asynchronous-unwind-tables -fno-inline -Oz

compile_commands.json:
	bear -- $(MAKE) -B -f $(MAKEFILE_LIST)

scan:
	scan-build -V $(MAKE) -B -f $(MAKEFILE_LIST)

tidy:
	clang-tidy sha1-arm-test.cpp
