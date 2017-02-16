/* MPUDP_recv.c
 * Author: Daniel Lukaszewski
 * Date Last Modified: 2/16/17
 *
 * This program provides functions for the MPUDP kernel testing. Comment
 * out client and server code depending on machine.
 *
 * path_recv_manager: ensures packets coming in arrive with proper dest
 *                  ip for OpenVPN to recognize as same connection
 *                  (kind of like MPTCP joining subflows)
 */

#define MODULE

#include <linux/module.h>
#include <uapi/linux/in.h>   /* for struct sockaddr_in */   

extern void (*mpudp_recv_function)(struct sockaddr_in *);       /* calling function */

/************************************************************ path_manager*/


//replace vpn server address to master source address
void path_recv_manager(struct sockaddr_in * sin) {
  //printk("<1> $$ calling new in function\n");
  //client code:
  if (sin->sin_addr.s_addr==0x0B01080A) {  
	sin->sin_addr.s_addr=0x1602080A;
  } 
  //server code:
  //if (sin->sin_addr.s_addr==0x0101080A) {  
	//sin->sin_addr.s_addr=0x0202080A;
  //}                      
}

/*************************************************************** init_module
 * this function replaces the null pointer with a real one */
int init_module() {
  mpudp_recv_function = path_recv_manager;
  printk("<1> $$ recv module created\n");
  return 0;
}  /* init_module */

/************************************************************ cleanup_module
 * this function resets the function pointer back to null */
void cleanup_module() {
  mpudp_recv_function = 0;
  printk("<1> $$ recv module removed\n");
}  /* cleanup_module */
