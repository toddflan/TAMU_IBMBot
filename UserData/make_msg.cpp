#include<iostream>
#include<fstream>
#include<string>

using namespace std;

// function to get a string of data by column header
string get_data(char* filename_in, string column_header)
{
	ifstream input_file;
	input_file.open(filename_in);

	if (!input_file)
	{
		cout << "Error opening file...\n";
		return "ERROR";
	}	

	char current_char = '?';		// parameters needed to get desired data
	int column_number = 0;
	int string_index = 0;
	int match = 0;

	while ((input_file >> current_char) && current_char != ';')	// read column headers
	{
		if (current_char == ',' && match == 1)
		{
			break;			// found it, move on
		}
		else if (current_char == column_header[string_index])
		{
			string_index++;		// go to next char
			match = 1;		// match so far
		}
		else				// doesn't match, reset
		{
			while((input_file >> current_char) && current_char != ',');	// read rest of column name
			string_index = 0;
			match = 0;
			column_number++;
		}
	}
	
	if (match != 1)		// didn't find a match
	{
		cout << "Unable to find column name.\n";
		return "ERROR";
	}

	if (current_char != ';')	// check we read the whole data line
	{
		while ((input_file >> current_char) && current_char != ';');	// read rest of line
	}

	int find_column = column_number;	// int to find column

	while (find_column != 0)	// get to right column
	{
		while((input_file >> current_char) && current_char != ',');       // read rest of column name
		find_column--;
	}

	string data_out;		// string to output
	input_file >> noskipws;		// don't skip whitespace

	while((input_file >> current_char) && current_char != ',' && current_char != ';')
	{
		if (current_char != '\n')
		{	
			data_out += current_char;	// add char to output string
		}
	}

	input_file >> skipws;		// back to default

	input_file.close();		// close the ifstream

	return data_out;
}

// ./<FILE> <FILENAME_IN> <FILENAME_OUT>
int main(int argc, char* argv[])
{
	string msg = "Hello! Don't forget to take ";		// begin string to speak to user

	msg += get_data(argv[1], "Name");	// get medicine name
	msg += " at ";

	int hour;		// build time string
	int minute;
	string time;

	hour = stoi(get_data(argv[1], "Hour"));		// read hour and minute as int's
	minute = stoi(get_data(argv[1], "Minute"));

	if (hour < 12 && hour >= 0)		// format time with hours
	{
		time = "am";
		if (hour == 0)
		{
			hour = 12;
		}
	}
	else if (hour == 12)
	{
		time = "pm";
	}
	else if (hour > 12 && hour <= 23)
	{
		time = "pm";
		hour -= 12;
	}
	else
	{
		cout << "Invalid hours.\n";
		return 1;
	}

	if (minute == 0)		// format time with minutes
	{
		time = to_string(hour) + ' ' + time + ".\n";
	}
	else if (minute > 0 && minute <= 59)
	{
		time = to_string(hour) + ' ' + to_string(minute) + ' ' + time + ".\n";
	}
	else
	{
		cout << "Invalid minutes.\n";
		return 1;
	}

	msg += time;

	ofstream output_file;
	output_file.open(argv[2]);

	if (!output_file)	// check if opening output file went well
	{
		cout << "Error opening file...\n";
		return 1;
	}

	output_file << msg;		// write message to output file

	output_file.close();		// close output file

	return 0;
}
