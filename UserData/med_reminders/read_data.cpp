#include "my_parser.h"

// ./<prog> <Column> <filename>
int main(int argc, char* argv[])
{
	string data = get_data(argv[2], argv[1]);	// call reading function

	cout << data;		// print

	return 0;
}
