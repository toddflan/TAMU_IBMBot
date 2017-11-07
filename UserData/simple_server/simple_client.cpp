//
//
//

#include "simple_server_functions.h"

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