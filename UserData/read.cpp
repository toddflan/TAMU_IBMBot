#include<iostream>
#include<fstream>

int main(int argc, char* argv[])
{
	std::ifstream testfile;
	testfile.open("test_userprofile.txt");

	if (!testfile)
	{
		std::cout << "Error opening file...\n";
		return 1;
	}	

	char current_char = '?';
	int column_number = 0;
	int string_index = 0;
	int match = 0;

	while ((testfile >> current_char) && current_char != ';')
	{
		if (current_char == ',' && match == 1)
		{
			break;
			//column_number++;	// hit next column
		}
		else if (current_char == argv[1][string_index])
		{
			string_index++;		// go to next char
			match = 1;		// match so far
		}
		else
		{
			while((testfile >> current_char) && current_char != ',');	// read rest of column name
			string_index = 0;
			match = 0;
			column_number++;
		}
	}
	
	if (current_char != ';')
	{
		while ((testfile >> current_char) && current_char != ';');	// read rest of line
	}

	int find_column = column_number;	// int to find column

	while (find_column != 0)	// get to right column
	{
		while((testfile >> current_char) && current_char != ',');       // read rest of column name
		find_column--;
	}

	while((testfile >> current_char) && current_char != ',' && current_char != ';')
	{
		std::cout << current_char;
	}

	std::cout << '\n';

	return 0;
}
