import hashlib

KEY = '800770FF00FF08012'  # The secret key (initialization vector)
OTP_LENGTH = 6  # Length of the OTP (in hexadecimal digits)


# Generates a hash feedback OTP sequence
# PARAM otp_sequence: List containing the previous OTP (starting with the secret key)
# PARAM otp_num: The number representing the OTP to generate (starting from 1)
# Returns the OTP for the given otp_num
def gen_hf_otp(otp_sequence, otp_num):
    while len(otp_sequence) < otp_num:
        # Get the last OTP in the sequence
        last_otp = otp_sequence[-1]

        # Hash the last OTP to get the next OTP
        sha256_hash = hashlib.sha256(last_otp.encode())
        hash_hex = sha256_hash.hexdigest()

        # Truncate the hash to get the OTP (last 6 hexadecimal digits)
        next_otp = hash_hex[-OTP_LENGTH:]

        # Add the new OTP to the sequence
        otp_sequence.append(next_otp)

    # Return the OTP for the requested otp_num
    return otp_sequence[otp_num - 1]

### WORK IN PROGRESS ###
# TEST MAIN FUNCTION: generate and print a sequence of OTPs
def generate_otp_sequence():
    # Start with the secret key as the first OTP
    otp_sequence = [KEY]
    # How many OTPs you want to generate (using 10 to test)
    num_otps = 10

    for otp_num in range(1, num_otps + 1):
        # Generate the OTP for the current otp_num
        current_otp = gen_hf_otp(otp_sequence, otp_num)

        print("OTP #{}: {}".format(otp_num, current_otp))

# Run the OTP generation program
generate_otp_sequence()
