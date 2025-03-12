CXX := g++
CXXFLAGS := -std=c++17 -Wall -Wextra -I include -I.
LDFLAGS := -lprofiler

# Enable profiling via a macro
ifndef PROFILE
    PROFILE := 0
endif
CXXFLAGS += -DPROFILE=$(PROFILE)

# Directories
SRC_DIR := src
INC_DIR := include
OBJ_DIR := obj
BENCH_DIR := benchmark

# Find all .cpp files
SRCS := $(wildcard $(SRC_DIR)/*.cpp)
OBJS := $(SRCS:$(SRC_DIR)/%.cpp=$(OBJ_DIR)/%.o)

# Benchmark program
BENCH_SRC := $(BENCH_DIR)/genetic_benchmark.cpp
BENCH_BIN := genetic_benchmark

# Default target
all: directories $(BENCH_BIN)

directories:
	@mkdir -p $(OBJ_DIR)
	@mkdir -p $(BENCH_DIR)

# Compile each .cpp to .o
$(OBJ_DIR)/%.o: $(SRC_DIR)/%.cpp
	@echo "Compiling $<..."
	@$(CXX) $(CXXFLAGS) -c $< -o $@

# Link the objects + the main benchmark source
$(BENCH_BIN): $(BENCH_SRC) $(OBJS)
	@echo "Building benchmark program..."
	@$(CXX) $(CXXFLAGS) $< $(OBJS) -o $@ $(LDFLAGS)

clean:
	@rm -rf $(OBJ_DIR) $(BENCH_BIN)

rebuild: clean all

.PHONY: all clean rebuild directories test view-profile

test:
	./test.sh diabetes
	./test.sh cancer
	./test.sh housing

view-profile:
	~/go/bin/pprof -http "0.0.0.0:8080" ./genetic_benchmark ./my_profile.prof
