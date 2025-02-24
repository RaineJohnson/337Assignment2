import hashlib
KEY = '800770FF00FF08012'

# Fills the list to contain the next 101 full hashes
# PARAM next_hashes: the list that will contain the next 101 hashes
# PARAM first_input (optional): if next_hashes is empty, this value
#   will be used as input to generate the first hash to be added
def gen_hashes(next_hashes, first_input=''):
    if len(next_hashes) == 0:
        byte_input = first_input.encode()
        sha256_hash = hashlib.sha256(byte_input)
        hash_hex = sha256_hash.hexdigest()
        next_hashes.append(hash_hex)

    for i in range(len(next_hashes), 101):
        byte_input = next_hashes[i - 1].encode()
        sha256_hash = hashlib.sha256(byte_input)
        hash_hex = sha256_hash.hexdigest()
        next_hashes.append(hash_hex)


next_hashes = []
gen_hashes(next_hashes, KEY)
otp_num = 1

while True:
    user_input = input('Enter OTP #' + str(otp_num) + ' (0 to quit): ')
    if user_input == '0':
        break

    # Synchronization mechanism compares input to the next 100 OTPs.
    # If user_input is not the next OTP, but within the next 100,
    # the program will skip ahead to that OTP
    correct_otp_entered = False
    for i in range(100):
        cur_hash = next_hashes[i]
        cur_otp = cur_hash[-6:] # last 6 digits of cur_hash
        if user_input == cur_otp:
            print('Access Granted')
            correct_otp_entered = True
            otp_num += (i + 1)
            next_hashes = next_hashes[i+1:]
            gen_hashes(next_hashes)
            break

    if not correct_otp_entered:
        print('Access Denied')