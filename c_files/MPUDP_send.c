/* MPUDP_send.c
 * Author: Daniel Lukaszewski
 * Date Last Modified: 2/16/17
 *
 * This program provides functions for the MPUDP kernel testing. Comment
 * out client and server code depending on machine.
 *
 * path_manager: checks address and changes to alternate 50% of time
 */

#define MODULE
#define MAX_UNSIGNED_SHORT 65535

#include <linux/module.h>
#include <uapi/linux/in.h>   /* for struct sockaddr_in */   

extern int (*mpudp_send_function)(struct sockaddr_in *);       /* calling function */
extern void get_random_bytes(void *buf, int nbytes); /* random function */

/************************************************************ path_manager*/
int path_manager(struct sockaddr_in * usin) {
  unsigned short t;
  //printk("<1> $$ calling new function\n");
  //client code:
  if (usin->sin_addr.s_addr==0x1602080A) {
    get_random_bytes(&t,2);
    if (t<=16383) {
	    usin->sin_addr.s_addr=0x0B01080A;
	    return 1; /* read dest addr after change */
    }
  //server code:
  //if (usin->sin_addr.s_addr==0x0202080A) {
    //get_random_bytes(&t,2);
    //if (t<=16383) {
	    //usin->sin_addr.s_addr=0x0101080A;
	    //return 1; /* read dest addr after change */
    //}
  }
  return 0;                      
} 


/*************************************************************** init_module
 * this function replaces the null pointer with a real one */
int init_module() {
  mpudp_send_function = path_manager;
  printk("<1> $$ send module created\n");
  return 0;
}  /* init_module */

/************************************************************ cleanup_module
 * this function resets the function pointer back to null */
void cleanup_module() {
  mpudp_send_function = 0;
  printk("<1> $$ send module removed\n");
}  /* cleanup_module */
