import hashlib
import json

# Define the secret key and OTP parameters
KEY = '800770FF00FF08012'  # The secret key (initialization vector)
OTP_LENGTH = 6  # Length of the OTP (in hexadecimal digits)

# Function to generate OTPs based on hashing the previous hash
def generate_otp(key, num_otps):
    previous_hash = key  # Start with the key as the first hash
    otps = []  # List to store OTPs

    # Loop to generate OTPs
    for i in range(num_otps):
        # Hash the previous hash
        sha256_hash = hashlib.sha256(previous_hash.encode())  # Hash the previous hash
        hash_hex = sha256_hash.hexdigest()  # Get alphanumerical full hash from binary
        # Truncate the hash to get the OTP (last 6 hexadecimal digits)
        otp = hash_hex[-OTP_LENGTH:]

        # Add OTP to the list
        otps.append(otp)

        print("Hash {}: {}".format(i, hash_hex))
        # Set the current hash as the previous hash for the next iteration
        previous_hash = hash_hex

    return otps


# Generate a number of OTPs based on user input
user_input = input('How many OTPs would you like to generate?: ')
num_otps = 1
if user_input.isnumeric():
    num_otps = int(user_input)
otp_list = generate_otp(KEY, num_otps)

# Save the OTP list to a JSON file
with open('otps.json', 'w') as f:
    json.dump(otp_list, f)

# Print the OTPs to the console and confirmation of write to .json file
print("\nGenerated {} OTPs:".format(num_otps))
for i, otp in enumerate(otp_list, start=1):
    print("OTP {}: {}".format(i, otp))

print("\nThe OTPs have been saved to 'otps.json'.")
