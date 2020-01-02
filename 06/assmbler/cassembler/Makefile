
IDIR =./include
CC=gcc
CFLAGS=-I$(IDIR)

SRC=./src
ODIR=./obj
LDIR =./lib
LIBS=-lm -lhash_table
LDFLAGS = -L./lib

_DEPS = const.h utils.h 
_OBJ = main.o

#DEPS (include) files list 
DEPS = $(patsubst %,$(IDIR)/%,$(_DEPS))

OBJ = $(patsubst %,$(ODIR)/%,$(_OBJ))

#$(info $$DEPS is [${DEPS}])
#$(info $$OBJ is [${OBJ}])

# $@ means the left side of :
# $< means first item in list

# This will take all the dependincies, and compile it to obj/main.o
$(ODIR)/%.o: $(SRC)/%.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS) 

# $^ means the right side of :
assembler: $(OBJ)
	$(CC) -o $@ $^ $(CFLAGS) $(LDFLAGS) $(LIBS)

.PHONY: clean

clean:
	rm -f $(ODIR)/*.o *~ core $(INCDIR)/*~


