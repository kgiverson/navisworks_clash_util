# Navisworks Clash Utility

Welcome to Navisworks Clash Utility.  This project was started by team The Clash during the AEC Hackathon 2.1 in Chicago March 6-8.  (http://aechackathon.com/chicago/) and won best overall hack.  Our goal was to make working with the Clash Detective in Navisworks less manual and painful.

It is our hope that this will be a first step in helping to bridge the gap between Navisworks clash detetection and actually having useful reporting of data.

This tool will group together clashes from a Navisworks clash XML export.   It determines a group using a set distance around each clash on the x, y, and z axis, eliminating the need to browse through thousands of clashes in a clash report.  The distance from the clash can be set by the user. Data is then exported to a csv file.

## Installation Directions

If you already have Python 2 installed on your computer you can skip to Usage below.

### Straight Python

The easiest way to use the utility is to install (use an already installed) Python on your machine.   Downloads and information on installation can be found at Python's website (https://www.python.org/downloads/).   We have tested this utility using Python 2.7 on OSX and Windows 7 but should work on any environment with Python installed.

### Using a virtual machine

If you don’t want to install Python on your local machine you can also use a very nicely packaged virtual machine.  (You could also follow their cloud instructions to use at AWS).

1. Download Oracle VM VirtualBox (https://www.virtualbox.org/wiki/Downloads)
2. Set up Vagrant (https://www.vagrantup.com/)
3. Download and setup Data Science Toolbox (http://datasciencetoolbox.org/#start)
4. Clone this repository (or download the zip file) to your machine
5. Update the clash_util.ini file for the path information relevant to your project
5. Begin using the Clash Utility in conjunction with Navisworks

## Usage

You first need to run the clash detective and export the data using Navisworks report export choosing the XML output option. It's important to select all options for your export so the utility has as much data as it can to work.

Once you have your XML export you need to run the script. 

1. Open a terminal window or Windows a Command Prompt (Click the "Start | Program Files | Accessories | Command Prompt" to open a Command Prompt)
2. Type "<PATH TO PYTHON INTERPRETER> clash_util.py <NAME OF XML EXPORT FILE>.   

The script has a heal featre you can see by running it with the '-h' option.

## Next steps

Here are some potential next steps for this project that we came up with during the AEC Hackathon 2.1:

1. Take the button prototype (located in AECHACK directory) and make it work robustly so users don’t need to leave Navisworks UI to group clashes.
2. Add the ability to import the clash group data back into Navisworks. 
3. Make the batch file more user friendly and automatic for Windows users.
4. Add some machine learning capability so that the bounding boxes are not fixed and adjust based on user feedback.

## Credits

Members of the The Clash team during AEC Hackathon 2.1 - Chicago where:

- Tyler Davis - The Whiting-Turner Contracting Company
- Ian Huffman - Mortenson
- Kevin Iverson - Clayco
- Hilary Sinkoff - Technologist at Large
- Chelsey Smith - Akta
- Kyle Wright - Walsh Construction

