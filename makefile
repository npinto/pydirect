# Makefile for the example program. This file contains
# rules for single processor machines (make DIRect)
# and PVM and MPI versions (make DIRectpvm and DIRectmpi)
# Alton Patrick, Joerg Gablonsky
# 04-15-2001
F77 = f77
# Specify the location of the pvm or mpi header file.
INCLUDE_DIR = . 

# Specify the location of the pvm or mpi libraries 
LIB_DIR = . 

# Give the names of the libraries that must be linked.
LIBS = 

# MPI on SP2
#F77 = mpxlf
#INCLUDE_DIR = . 
#LIB_DIR = . 
#LIBS = 

# PVM on SP2:
#F77 = mpxlf
#INCLUDE_DIR = $(PVM_ROOT)/include
#LIB_DIR = $(PVM_ROOT)/lib/$(PVM_ARCH)
#LIBS = -lpvm3pe -lfpvm3 -lgpvm3


TARG = 

OBJS =	main.o myfunc.o \
       DIRect.o DIRserial.o DIRsubrout.o 

OBJS_MPI =	mainparallel.o myfunc.o \
       DIRect.o DIRparallel.o DIRsubrout.o DIRmpi.o

OBJS_PVM =	mainparallel.o myfunc.o \
       DIRect.o DIRparallel.o DIRsubrout.o DIRpvm.o

FFLAGS = $(TARG) -pg
FFLAGS = $(TARG) 
MPIFLAGS = $(TARG) 
PVMFLAGS = $(TARG) 

TestDIRect:	$(OBJS)
	$(F77) $(FFLAGS) -o $@ $(OBJS) 

TestDIRectmpi:	$(OBJS_MPI)
	$(F77) $(MPIFLAGS) -L$(LIB_DIR) $(LIBS) $(OBJS_MPI) -o $@ 

TestDIRectpvm:	$(OBJS_PVM)
	$(F77) $(PVMFLAGS) -L$(LIB_DIR) $(LIBS) -o $@ $(OBJS_PVM) 

clean:
	rm -f *.o

DIRmpi.o: DIRmpi.f
	$(F77) -I$(INCLUDE_DIR) -c DIRmpi.f -o DIRmpi.o

DIRpvm.o: DIRpvm.f
	$(F77) -I$(INCLUDE_DIR) -c DIRpvm.f -o DIRpvm.o
