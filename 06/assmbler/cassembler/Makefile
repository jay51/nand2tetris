
IDIR =./include
CC=gcc
CFLAGS=-I$(IDIR)

SRC=./src

ODIR=./obj
LDIR =./lib

LIBS=-lm

_DEPS = const.h

#DEPS (include) files list 
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

_OBJ = main.o 
OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

#$(info $$DEPS is [${DEPS}])
#$(info $$OBJ is [${OBJ}])

# $@ means the left side of :
# $< means first item in list
$(ODIR)/%.o: $(SRC)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

# $^ means the right side of :
assembler: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~


