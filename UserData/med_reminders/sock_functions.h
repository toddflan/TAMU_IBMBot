//----------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>		// defines perror(), herror() 
#include <fcntl.h>		// set socket to non-blocking with fcntrl()
#include <unistd.h>
#include <string.h>
#include <assert.h>		// add diagnostics to a program

#include <netinet/in.h>		// defines in_addr and sockaddr_in structures
#include <arpa/inet.h>		// external definitions for inet functions
#include <netdb.h>		// getaddrinfo() & gethostbyname()

#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/wait.h>
//#include <sys/select.h>		// for select() system call only
#include <sys/time.h>		// time() & clock_gettime()

#include <iostream>		// for cout
#include <fstream>		// file io

#define MAX_BUFF_SIZE 100

//----------------------------------------------------------------------------------

// code for err_sys

void err_sys(const char* x)
{
	perror(x);
	exit(1);
}

//----------------------------------------------------------------------------------
