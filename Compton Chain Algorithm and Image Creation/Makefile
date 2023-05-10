CC=gcc
BASEFLAGS= -Wall -lm -lpthread
CFLAGS= $(BASEFLAGS) -O2
CDBGFLAGS= $(BASEFLAGS) -g
CPRFFLAGS= $(BASEFLAGS) -pg
DEPS=truth_assign.h llist.h vector_ops.h lor.h ray_trace.h

%.o: %.c $(DEPS)
	$(CC) -c -o $@ $< $(CFLAGS)

compton_reconstruction: inverse_kinematics.o llist.o vector_ops.o
	$(CC) -o compton_reconstruction $^ $(CFLAGS)

debug_compton_reconstruction: inverse_kinematics.c llist.c vector_ops.c
	$(CC) -o debug_compton_reconstruction $^ -Wall -lm -g

renderer: lor_render.o vector_ops.o ray_trace.o llist.o
	$(CC) -o renderer $^ $(CFLAGS)

debug_renderer: lor_render.c vector_ops.c ray_trace.c llist.c
	$(CC) -o debug_renderer $^ $(CDBGFLAGS)

debug_ray_trace: ray_trace.c ray_test.c vector_ops.c
	$(CC) -o debug_ray_trace $^ $(CDBGFLAGS)

classical_pet: classical_pet.o llist.o vector_ops.o
	$(CC) -o classical_pet $^ $(CFLAGS)

debug_classical_pet: classical_pet.c llist.c vector_ops.c
	$(CC) -o debug_classical_pet $^ $(CDBGFLAGS)