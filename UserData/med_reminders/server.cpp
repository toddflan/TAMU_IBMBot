//
// Simple Server
//

#include "sock_functions.h"

//----------------------------------------------------------------------------------

// simple server to get data from clients
// ./server <server IP> <port #>

int main(int argc, char* argv[])
{
	// get parameters from terminal
	char* ip_str = argv[1];			// server_ip is arg 1
	int port = atoi(argv[2]);		// port # is arg 2

	// define parameters
	int sock_fd, accept_fd = -1;
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

	// ready socket for connections with listen
	if ((listen(sock_fd, 10) < 0))
	{
		err_sys("Error calling listen(...).");
	}
	
	char input_txt[MAX_BUFF_SIZE];			// C-style strings for echo
	int len = sizeof(addr);				// make len the size of addr

	while(1)
	{
		if ((accept_fd = accept(sock_fd, (struct sockaddr*) &addr, (socklen_t*) &len)) < 0)
		{
			err_sys("Error calling accept(...).");
		}
	
		int bytes_read = read(accept_fd, input_txt, MAX_BUFF_SIZE);	// read from app

		close(accept_fd);	// close accept

		if (input_txt[2] == '?')		// close and end
		{
			close(sock_fd);
			return 0;
		}

		char med_number = input_txt[2];			// grab medication number
		if (!(med_number == '1' | med_number == '2' | med_number == '3'))
		{
			err_sys("Invalid med_number.");
		}

		char filename[14];
		filename[0] = 'm';		// build filename
		filename[1] = 'e';
		filename[2] = 'd';
		filename[3] = 's';
		filename[4] = '/';
		filename[5] = 'm';
		filename[6] = 'e';
		filename[7] = 'd';
		filename[8] = med_number;
		filename[9] = '.';
		filename[10] = 't';
		filename[11] = 'x';
		filename[12] = 't';
		filename[13] = '\0';		// null terminate

		std::ofstream file_out;				// output file in which to put data
		file_out.open(filename);
		file_out << "Name;Day;Hour;Minute.\n";		// column headers
		

		for (int i = 4; i < bytes_read; i++)		// chars 0 & 1 are garbage (UTF-8 stuff), chars 3 & 4 are for med number
		{
			file_out << input_txt[i];		// write to file and terminal
			std::cout << input_txt[i];
		}

		file_out.close();		// close output file
		std::cout << '\n';

		memset(input_txt, 0, sizeof(input_txt));	// clear input_txt

	}

	if (close(sock_fd) < 0)					// close socket
	{
		err_sys("close error");
	}

	return 0;			// indicates success
}

//----------------------------------------------------------------------------------
