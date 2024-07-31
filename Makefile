TARGETS := sha1-arm-test

CXXFLAGS := -Wall -Wextra -Wpedantic -std=c++2b
CXXFLAGS += -fsanitize=address

all: $(TARGETS)

.PHONY: clean compile_commands.json scan tidy

clean:
	rm -rf *.dSYM/
	rm -f $(TARGETS)
	rm -f compile_commands.json

ssha1-arm-test: sha1-arm-test.cpp
	$(CXX) -o $@ $^ $(CXXFLAGS)

compile_commands.json:
	bear -- $(MAKE) -B -f $(MAKEFILE_LIST)

scan:
	scan-build -V $(MAKE) -B -f $(MAKEFILE_LIST)

tidy:
	clang-tidy sha1-arm-test.cpp
