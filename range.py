import bitcoin
import os

# Set the starting hexadecimal value
start_hex = "0000000000000000000000000000000000000000000000000000000000000002"

# Set a flag to indicate whether all the addresses have been found
all_addresses_found = False

# Check if a progress file exists
if os.path.exists("progress.txt"):
    # Read the last hexadecimal value from the progress file
    with open("progress.txt", "r") as f:
        start_hex = f.read().strip()

    # Convert the hexadecimal value to an integer
    start_int = int(start_hex, 16)
else:
    # Convert the starting hexadecimal value to an integer
    start_int = int(start_hex, 16)

# Set the ending hexadecimal value
end_hex = "fffffffffffffffffffffffffffffffebaaedce6af48a03bbfd25e8cd0364140"

# Convert the ending hexadecimal value to an integer
end_int = int(end_hex, 16)

while not all_addresses_found:
    # Iterate through all the integers in the range
    for i in range(start_int, end_int):
        # Convert the integer to a hexadecimal value
        private_key_hex = hex(i)[2:]

        # Pad the hexadecimal value with leading zeros if necessary
        private_key_hex = private_key_hex.zfill(64)

        # Generate the public key and address from the private key
        public_key = bitcoin.privkey_to_pubkey(private_key_hex)
        address = bitcoin.pubkey_to_address(public_key)

        # Log the current address and private key
        print(f"Address: {address}\nPrivate key: {private_key_hex}\n")

        # Check if the address exists in the address.txt file
        if os.path.exists("address.txt"):
            with open("address.txt", "r") as f:
                addresses = f.read().splitlines()
            if address in addresses:
                # Save the address and private key to foundit.txt
                with open("foundit.txt", "a") as f:
                    f.write(f"Address: {address}\nPrivate key: {private_key_hex}\n")

                # Remove the found address from the list of addresses
                addresses.remove(address)

                # If all the addresses have been found, set the flag to True
                if len(addresses) == 0:
                    all_addresses_found = True
                    break

    # Save the last hexadecimal value used to the progress file
    with open("progress.txt", "w") as f:
        f.write(private_key_hex)

# Save the remaining addresses to the address.txt file
with open("address.txt", "w") as f:
    for address in addresses:
        f.write(address + "\n")
