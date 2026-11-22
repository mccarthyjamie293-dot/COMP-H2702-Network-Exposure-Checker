# Local Network Exposure Checker

## About My Project

For this project, I made a network exposure checker using Python. My program checks four different ports on my computer to see if they are open or closed.

I also added banner grabbing so the program can pull information from the services running on some of the ports. When I run the program, it shows me the results and saves them into a text file.

## Why I Made It

The main point of my project is to check what services are running on a local network.

An open port just shows a service is accepting connections not that there is a security problem. I used my program to check which of the supplied ports were open and what services were running on them.

## Files I Used

- **network_checker.py** - This is my main Python code.
- **local_test_services.py** - This was provided to run the test services.
- **targets.txt** - This contains the IP address I tested.
- **ports.txt** - This contains the four ports I checked.
- **network_report.txt** - This is where my program saves the results.
- **README.txt** - This contains the original instructions for the test files.

## How To Run My Program

I used Python 3 and VS Code for my project, though any editor will work

1. Open the project folder in VS Code.
2. Open a terminal and type `python local_test_services.py`.
3. Keep that terminal running.
4. Open a new terminal and put in `python network_checker.py`.
5. The program checks the ports and shows the results.
6. Open on the left tab `network_report.txt` to see saved results.

## Ports I Tested

I used the IP address `127.0.0.1`, which is localhost.

I tested these four ports:

- **18080** - HTTP service
- **19090** - Banner service
- **20001** - Generic TCP service
- **20002** - Port that should be closed

I only used the local IP address and the ports given in the project files. I didn't scan any outside networks.

## Python Code I Used

I used functions to split my code into different parts instead of putting everything together.

I used lists to store the ports and a for loop to go through them. I also used if statements to check whether the ports were open or closed.

I used try and except so the program could handle errors without crashing.

## Testing My Program Against the Port Setup

I tested my program with the local test services running, and it found three open ports and one closed port.

I also stopped the test services and ran my program again. This time, all four ports showed as closed.

I tested what happened when the ports file was missing and when I entered invalid IP addresses or ports. The program displayed error messages instead of crashing.

## What My Program Can't Do

My program only checks the local IP address and the four approved ports. It isn't designed to scan other networks.

It also can't tell if a service is dangerous just because its port is open. More checks would be needed to find out if there was an actual security problem.