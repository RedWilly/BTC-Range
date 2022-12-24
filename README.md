# BTC-Range

This Python script generates Bitcoin addresses and private keys, checks them against a list of addresses in the "address.txt" file, and saves any matching address and private key to the "foundit.txt" file.

The script uses the bitcoin library to generate the addresses and private keys from a hexadecimal value, which is a representation of a number in base 16. The script starts from the hexadecimal value "000000000000000000000000000000000000000000000000000000000000001f" and generates addresses and private keys until it reaches the hexadecimal value "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140".

To ensure that the script can be resumed from where it left off in case of an interruption, the script saves the last hexadecimal value used in a progress file named "progress.txt". If the progress file exists when the script is run, it will start from the hexadecimal value in the file instead of the starting hexadecimal value.
For example, if the last hexadecimal value used was "1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef", the progress.txt file would look like this:
```
1234567890abcdef1234567890abcdef1234567890abcdef1234567890abcdef
```

The script also handles the "address.txt" and "foundit.txt" files by reading the addresses from the "address.txt" file and writing any matching address and private key to the "foundit.txt" file. When all the addresses have been found, the script saves the remaining addresses (if any) back to the "address.txt" file.

Overall, this script is useful for generating and checking a large number of Bitcoin addresses and private keys, and for keeping track of the progress and results in separate files. It can be modified to fit different requirements, such as changing the starting and ending hexadecimal values or adjusting the file handling logic.

## Modules Require

To install the bitcoin module, you can use the following command:
```
pip install bitcoin
```
This will install the bitcoin module and its dependencies, which include the ecdsa and hashlib modules. The bitcoin module provides various functions for generating and converting Bitcoin addresses and private keys, as well as for handling transactions and blocks.

In addition to the bitcoin module, the script also uses the os module to handle files and directories. The os module is a built-in module in Python and does not need to be installed separately. It provides functions for interacting with the operating system, such as reading and writing files, checking for the existence of a file or directory, and creating or deleting a file or directory.
