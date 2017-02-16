obj-m+=MPUDP_send.o
obj-m+=MPUDP_recv.o


all:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) modules
	
clean:
	make -C /lib/modules/$(shell uname -r)/build/ M=$(PWD) clean
