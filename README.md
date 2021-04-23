# GITogether

## Overview

**GITogether** is a modern web application for creating and finding groups of shared interest at Georgia Tech. It is built on Flask, an extensible, reliable, and efficient web application framework for Python3. Users can create, find, and join interest groups with others on campus, and receive up-to-date information on meeting times and activities. Usage is as simple as registering an account and then exploring the clean, intuitive interface that GITogether provides.



## Release Notes (v1.1)

### New Feature List

- added support for categorizing new clubs
- integrated category data with the tag database in the backend
- searching by auto-generated club tags
- new clean and streamlined user interface
- persistent club favoriting

### Fixed Bugs

- tag auto-generation missing a known keyword
- string searching of clubs not finding an existing club
- password encryption issue where passwords were stored as strings of bytes instead of bytes themselves
- UI elements disappearing at periodic refreshing intervals
- favoriting is user-specific and isolated
- various search bar errors involving result formatting and accuracy of query

### Current Bugs/Defects

- club creators cannot specify club image file
- club creators cannot specify additional, self-generated tags for the club
- all changes created in the edit button are being reflected in the UI but description information and social media links are not being properly modified in the backend
- search by category is restricted to a single category per query

## Installation Guide

### Requisite Software for Installation

Users must have a web browser capable of rendering HTML5/CSS3 formatting languages and supporting the HyperText Transfer Protocol (HTTP) protocol stack (examples: up-to-date Firefox, Chrome, Chromium, Edge, Opera, etc.), and they must have the at least Python v3.7.x installed locally on their machine and added to their PATH environment variables (this can be done on installation).

### Dependencies

The Python pip3 (package manager) is required to obtain dependent libraries for the application. One may install pip3 for Python3 using the following instructions: https://www.linuxscrew.com/install-pip (for Linux/MacOS users) and https://stackoverflow.com/questions/41501636/how-to-install-pip3-on-windows#41501815 (for Windows users).

Once Python3 and pip3 are successfully installed, obtain the dependent libraries by opening up a terminal and entering the following:

```bash
    pip3 install --upgrade pip  # to upgrade your pip3 to the most recent version (one may need sudo)
    pip3 install flask          # to install Flask, the web application framework for GITogether
    pip3 install flask_mail     # an extension for Flask that enables automated emails
    pip3 install bcrypt         # the cryptography library used for password security
```

Once that is done, all other libraries needed are included in the Python3 standard library, so one should now meet all requirements for building/running GITogether.

For more information on the libraries used / troubleshooting, see:

https://flask.palletsprojects.com/en/1.1.x/ (`flask`)
https://flask-mail.readthedocs.io/en/latest/ (`flask-mail`)
https://pypi.org/project/bcrypt/ (`bcrypt`)

### Download Instructions

All the source code for GITogether is accessible here on our GitHub remote repository (https://github.com/christinanguyen1/JIB-307-GITogether). To download the latest version, all one needs to do is download and extract a `.zip` file form the `Code` button on the repository site, or use either of the following methods for git cloning:

```bash
    git clone https://github.com/christinanguyen1/JIB-307-GITogether.git # (if using HTTPS (PREFERRED))
    git clone git@github.com:christinanguyen1/JIB-307-GITogether.git     # (if using one's own SSH key)
```

### Installation and Running Instructions

Due to the portability of our codebase, once the requisite software and pip3 libraries are installed (see above if needed), there is no further installation required. To run GITogether, navigate to the downloaded directory and enter the following into a terminal:

```bash
    cd py_backend/pyserv/  # navigate where the server.py script is located
    python3 server.py      # run the flask server
```

Now, navigate to `http://127.0.0.1:5000/` in your web browser of choice and you should see the login page for GITogether. Congratulations, you are now running GITogether!

### Troubleshooting

If you run into any issues regarding privileges (like running something as non-root), ensure that you invoked the command with `sudo [command]`, but ensure that you know what command you are executing. If a certain command could not be found, double-check that you spelled it correctly, and if it persists, navigate to the appropriate website about what you are missing. To resolve issues with Python3 and pip3, one can re-install Python3 from https://www.python.org/downloads/ and follow the above `Dependencies` step to get the appropriate libraries and ensure pip3 is working as expected.

