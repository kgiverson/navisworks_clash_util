# Navisworks Clash Utility

Welcome to Navisworks Clash Utility.

It is our hope that this will be a first step in helping to bridge the gap between Navisworks clash detetection and actually having useful reporting of data.

This tool will group together clashes within a set distance around each clash on the x, y, or z axis, eliminating the need to browse through thousands of clashes in a clash report.  The distance from the clash can be set by the user. Data can then be exported to a csv file.

### Directions (for non-developers)

You have two options.  One would be to install Python.  Do do that check out (http://www.python.org) and install Python 2.7.

If you don’t want to install Python on your local machine you can also use a very nicely packaged virtual machine. Instructions for that approach below.

1. Download Oracle VM VirtualBox (https://www.virtualbox.org/wiki/Downloads)

2. Set up Vagrant (https://www.vagrantup.com/)

3. Clone this repository to your machine

4. Begin using the Clash Utility in conjunction with Navisworks

### Next steps ###

1. Take the button prototype and make it work more robustly so users don’t need to leave Navisworks
2. Add the ability to import the clash group data back into Navisworks
3. Make the batch file more user friendly and automatic
4. Add some machine learning capability so that the bounding boxes are not fixed and adjust based on user feedback
