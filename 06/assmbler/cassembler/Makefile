
IDIR =./include
CC=gcc
CFLAGS=-I$(IDIR)

SRC=./src
ODIR=./obj
LDIR =./lib
LIBS=-lm -lhash_table
LDFLAGS = -L./lib

_DEPS = const.h utils.h 
_OBJ = main.o const.o

#DEPS (include) files list 
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

#$(info $$DEPS is [${DEPS}])
#$(info $$OBJ is [${OBJ}])

# $@ means the left side of ":"
# $< means first item in list after ":" (in this case, it's the name of file like main.c or const.c)

# This will take *.c in src and h files, and compile it to obj/<name>.o
$(ODIR)/%.o: $(SRC)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) 

# $^ means the right side of ":" (the list of obj files)
assembler: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~


