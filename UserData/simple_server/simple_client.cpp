//
// echo program client
//

//----------------------------------------------------------------------------------

#include <stdio.h>
#include <stdlib.h>
#include <errno.h>					// defines perror(), herror() 
#include <fcntl.h>					// set socket to non-blocking with fcntrl()
#include <unistd.h>
#include <string.h>
#include <assert.h>					//add diagnostics to a program

#include <netinet/in.h>			//defines in_addr and sockaddr_in structures
#include <arpa/inet.h>			//external definitions for inet functions
#include <netdb.h>					//getaddrinfo() & gethostbyname()

#include <sys/socket.h>			//
#include <sys/stat.h>
#include <sys/types.h>
#include <sys/uio.h>
#include <sys/wait.h>
#include <sys/select.h>			// for select() system call only
#include <sys/time.h>				// time() & clock_gettime()

#define MAX_BUFF_SIZE 25		// max length

//----------------------------------------------------------------------------------

// function for writing errors to terminal

void err_sys(const char* x)
{
	perror(x);
	exit(1);
}

//----------------------------------------------------------------------------------

// writen function to write to server

int writen(int sock, char* buff, int length)
{
	int write_num = 0;
	int bytes_written = 0;
	
	while (bytes_written < length)			// loop write until done
	{
		write_num = write(sock, buff + bytes_written, length - bytes_written);
		
		if (write_num == 0)		// if nothing to write, end loop
		{
			break;
		}
		else if (write_num == -1)
		{
			if (errno != EINTR)
			{
				return -1;			// error
			}
			
			bytes_written = 0;				// start while loop over if EINTR
		}
		
		bytes_written += write_num;
	}
	
	return bytes_written;
}

//----------------------------------------------------------------------------------

// readline function for getting txt from server

int readline(int sock, char* buff, int length)
{
	int bytes_read = 0;
	int read_num = 0;
	bool found_newline = false;
		
	read_num = read(sock, buff + bytes_read, length - bytes_read);

	if (read_num == -1)
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

int main(int argc, char* argv[])
{
	// define needed parameters
	int sock_fd = -1;												// default will cause error if not changed
	struct sockaddr_in addr_echo;
	char* my_IP_str = argv[1];
	uint16_t my_port = atoi(argv[2]);

	// converting IP string to sin_addr
	int IP_check = inet_pton(AF_INET, my_IP_str, &(addr_echo.sin_addr));
	
	if (IP_check == -1)
	{
		err_sys("inet_pton(...) - error");
	}
	if (IP_check == 0)
	{
		err_sys("inet_pton(...) - entered IP Address is invalid.");
	}
	
	// assign members of sockaddr_in
	bzero((char*)&addr_echo, sizeof(addr_echo));
	addr_echo.sin_family = AF_INET;									// assign other members of addr_echo
	addr_echo.sin_port = htons(my_port);						// get port # to network byte order
	
	// open socket
	if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		err_sys("Error calling socket(...).");
	}
	
	// connect socket
	if ((connect(sock_fd, (struct sockaddr*) &addr_echo, sizeof(addr_echo))) < 0)
	{
		err_sys("Error calling connect(...).");
	}
	
	int n = 0;												// int for read and write returns
	char txt_line[MAX_BUFF_SIZE];			// C-style strings for read and write
	char output_txt[MAX_BUFF_SIZE];
	
	while (fgets(txt_line, MAX_BUFF_SIZE, stdin) != NULL)
	{
		if (!strchr(txt_line, '\n'))			// if input exceeds MAX_BUFF_SIZE (no '\n' char)
		{
			while(fgetc(stdin) != '\n');		// get rid of chars till newline
		}
		
		fputs("\n", stdout);			// formatting
		
		if ((n = writen(sock_fd, txt_line, strlen(txt_line))) < 0)
		{
			err_sys("writen error");
		}
		
		if ((n = readline(sock_fd, output_txt, MAX_BUFF_SIZE)) < 0)
		{
			err_sys("readline error");
		}
			
		if (fputs(output_txt, stdout) == EOF)			// output echo'd text
		{
			err_sys("Error with fputs.");
		}
		
		fputs("\n", stdout);		// formatting
	}
	
	return 0;			// indicates success
}

//----------------------------------------------------------------------------------