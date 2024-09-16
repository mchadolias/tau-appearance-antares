CXX = $(shell root-config --cxx)
CXXFLAGS = $(shell root-config --cflags) -fPIC
LDFLAGS = $(shell root-config --glibs)

BINDIR = bin

INCDIRS = -I$(ROOTSYS)/include

SOURCE = $(wildcard src/*.cc)
TARGET = $(patsubst %.cc,%,$(shell basename $(SOURCE)))

$(BINDIR)/$(TARGET): $(SOURCE)
	@mkdir -p ${BINDIR}
	@echo "Compiling ${TARGET} from ${SOURCE}..."
	@$(CXX) -O3 -o $@ $< $(LDFLAGS) $(CXXFLAGS) $(INCDIRS)

phony:

clean:
	@rm -f $(BINDIR)/*
