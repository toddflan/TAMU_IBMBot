//----------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>		// defines perror(), herror() 
#include <fcntl.h>		// set socket to non-blocking with fcntrl()
#include <unistd.h>
#include <string.h>
#include <assert.h>		//add diagnostics to a program

#include <netinet/in.h>		//defines in_addr and sockaddr_in structures
#include <arpa/inet.h>		//external definitions for inet functions
#include <netdb.h>		//getaddrinfo() & gethostbyname()

#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <sys/select.h>		// for select() system call only
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

// readline function for getting txt from client

int readline(int sock, char* buff, int length)
{
	int bytes_read = 0;
	int read_num = 0;
	bool found_newline = false;
		
	read_num = read(sock, buff + bytes_read, length - bytes_read);
		
	if (read_num == -1)				// check for errors
	{
		if (errno != EINTR)
		{
			return -1;			// error
		}
		
		bytes_read = 0;			// restart loop if EINTR
	}
		
	bytes_read += read_num;
	
	for (int i = 0; i < bytes_read; i++)
	{
		if (buff[i] == '\n')						// check buffer for newline
		{
			buff[i+1] = '\0';
			found_newline = true;
			i = bytes_read;				// exit loop
		}
	}
	
	if (!found_newline)								// EOF check
	{
		buff[length-1] = '\0';
	}

	return bytes_read;
}

//----------------------------------------------------------------------------------
