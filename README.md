# README

## Introduction
The code is designed to parse an LDIF (LDAP Data Interchange Format) file containing information about users and groups, extract relevant information, and output it in a csv format.

## Installation
To use this code, you will need to have Python 3 installed on your system. You will also need to install the required dependeicies listed in the requirements.txt.

## Usage
To use this code, you will need to provide the path to an LDIF file as input. This can be done by modifying the `ldif_filename` variable at the top of the file. Once you have done this, you can run the code using the following command:
```
python <filename>.py <ldif_file.ldif>
```

The code will then parse the LDIF file, extract relevant information about users and groups, and output it in a readable format.

## Output
The output of this code will be a list of user details, including:
- First name
- Last name
- Email
- Distinguished Name (DN)
- JSON representation of the user's record
- Group name

Each line of output will represent a single user who is a member of a group. If a user is a member of multiple groups, they will be listed once for each group they belong to.

## Limitations
This code is designed to work with LDIF files that contain user and group information in a specific format. If your LDIF file is structured differently, this code may not work as expected. You can provide me with an example and I will try my best to fix it. Also, this code is designed to output results to the console, if you need to store the results in a file or in a different format you can either redirect the output (>), you will need to modify the code accordingly.