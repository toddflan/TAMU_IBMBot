#include "my_parser.h"		// needed includes and functions

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
	else if (minute > 0 && minute < 10)		// will say hour 'oh' minute
	{
		time = to_string(hour) + " o " + to_string(minute) + ' ' + time + ".\n";
	}
	else if (minute >= 10 && minute <= 59)
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
