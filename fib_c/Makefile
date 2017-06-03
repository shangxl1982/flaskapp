.PHONY: all
fib_c_objs = fib_c.o

%.o :%.c
	$(CC) -c -o $@ $<

fib_c : $(fib_c_objs)
	$(CC) -o $@ $^

all: fib_c
clean:
	@rm -rf *.o fib_c
