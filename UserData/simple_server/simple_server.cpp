//
// Simple Server
//

#include "simple_server_functions.h"

//----------------------------------------------------------------------------------

// simple server to get data from clients
// ./server <server IP> <port #>

int main(int argc, char* argv[])
{
	// get parameters from terminal
	char* ip_str = argv[1];			// server_ip is arg 1
	int port = atoi(argv[2]);		// port # is arg 2

	// define parameters
	int sock_fd = -1;
	int IP_check = -1;
	struct sockaddr_in addr;
	
	// build addr
	bzero((char*)&addr, sizeof(addr));
	addr.sin_family = AF_INET;	
	addr.sin_port = htons(port);
	
	// converting typed IP string to sin_addr
	if ((IP_check = inet_pton(AF_INET, ip_str, &(addr.sin_addr))) == -1)
	{
		err_sys("inet_pton(...) - error");
	}
	else if (IP_check == 0)
	{
		err_sys("inet_pton(...) - entered IP Address is invalid.");
	}
	
	// call socket
	if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		err_sys("Error with socket()");
	}
	
	// call bind
	if (bind(sock_fd, (struct sockaddr*) &addr, sizeof(addr)) < 0)
	{
		err_sys("Error with bind()");
	}
	/*
	// define needed parameters
	int sock_fd = -1, accept_fd = -1;			// defaults will cause errors if not changed
	int my_port = atoi(argv[2]);
	struct sockaddr_in addr_echo;
	struct sigaction sa;

	// open socket, get socket fd
	if ((sock_fd = socket(AF_INET, SOCK_STREAM, 0)) < 0)
	{
		err_sys("Error calling socket(...).");
	}
	
	// assign addr_echo members
	bzero((char*)&addr_echo, sizeof(addr_echo));
	addr_echo.sin_family = AF_INET;	
	addr_echo.sin_port = htons(my_port);							// get port # to network byte order
	addr_echo.sin_addr.s_addr = INADDR_ANY;						// any address
	
	// bind address to socket
	if ((bind(sock_fd, (struct sockaddr*) &addr_echo, sizeof(addr_echo))) < 0)
	{
		err_sys("Error calling bind(...).");
	}
	*/
	// ready socket for connections with listen
	if ((listen(sock_fd, 10) < 0))
	{
		err_sys("Error calling listen(...).");
	}
	
	/*
	sa.sa_handler = sigchld_handler;		// get rid of dead processes
	sigemptyset(&sa.sa_mask);
	sa.sa_flags = SA_RESTART;
	
	if (sigaction(SIGCHLD, &sa, NULL) == -1)
	{
		err_sys("sigaction error");
	}
	*/
	char input_txt[MAX_BUFF_SIZE];				// C-style strings for echo
	int len = sizeof(addr);						// make len the size of addr
	
	/*
	// accept connections to clients
	while(1)
	{
		if ((accept_fd = accept(sock_fd, (struct sockaddr*) &addr_echo, (socklen_t*) &len)) < 0)
		{
			err_sys("Error calling accept(...).");
		}
		
		if (!fork())
		{
			int n = 1;
		
			while (n)
			{
				n = readline(accept_fd, input_txt, MAX_BUFF_SIZE);
				
				if (n > 0)				// n = 0 if EOF was read in readline, skip writen
				{
					n = writen(accept_fd, input_txt, strlen(input_txt));
				}
			}
			
			if (close(accept_fd) < 0)
			{
				err_sys("close error");
			}
			
			exit(0);		// close child
		}
	}
	*/
	
	if ((accept_fd = accept(sock_fd, (struct sockaddr*) &addr, (socklen_t*) &len)) < 0)
	{
		err_sys("Error calling accept(...).");
	}
	
	read(accept_fd, input_txt, MAX_BUFF_SIZE);
	
	if (fputs(input_txt, stdout) == EOF)			// output text
	{
		err_sys("Error with fputs.");
	}
	
	fputs("\n", stdout);		// formatting
	
	if (close(sock_fd) < 0)					// close socket
	{
		err_sys("close error");
	}
	
	return 0;			// indicates success
}

//----------------------------------------------------------------------------------