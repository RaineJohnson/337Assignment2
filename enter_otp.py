import hashlib
KEY = '800770FF00FF08012' # Secret key (initialization vector)
OTP_LENGTH = 6
SYNC_LENGTH = 100 # number of OTPs ahead that will be accepted

# Fills the list to contain the next (SYNC_LENGTH + 1) full hashes
# PARAM next_hashes: the list that will contain the next hashes
# PARAM first_input (optional): if next_hashes is empty, this value
#   will be used as input to generate the first hash to be added
def gen_hashes(next_hashes, first_input=''):
    # if next_hashes is empty, generates the first hash based on first_input
    if len(next_hashes) == 0:
        byte_input = first_input.encode()
        sha256_hash = hashlib.sha256(byte_input)
        hash_hex = sha256_hash.hexdigest()
        next_hashes.append(hash_hex)

    # adds the next hashes in the sequence
    for i in range(len(next_hashes), SYNC_LENGTH + 1):
        byte_input = next_hashes[i - 1].encode()
        sha256_hash = hashlib.sha256(byte_input)
        hash_hex = sha256_hash.hexdigest()
        next_hashes.append(hash_hex)

# MAIN FUNCTION: asks user to enter OTPs until they exit the program
def enter_otp_sequence():
    # creates a list of the next SYNC_LENGTH hashes (plus one to refill list later)
    next_hashes = []
    gen_hashes(next_hashes, KEY)
    otp_num = 1 # the number of the current OTP in the sequence

    while True:
        user_input = input('Enter OTP #' + str(otp_num) + ' (0 to quit): ')
        if user_input == '0':
            break

        # Synchronization mechanism compares input to the next SYNC_LENGTH OTPs.
        # If user_input is not the next OTP, but within the next SYNC_LENGTH,
        # the program will skip ahead to that OTP
        correct_otp_entered = False
        for i in range(SYNC_LENGTH):
            cur_hash = next_hashes[i]
            cur_otp = cur_hash[-OTP_LENGTH:] # last OTP_LENGTH digits of cur_hash
            if user_input == cur_otp:
                print('Access Granted')
                correct_otp_entered = True
                otp_num += (i + 1)
                next_hashes = next_hashes[i+1:]
                gen_hashes(next_hashes)
                break

        if not correct_otp_entered:
            print('Access Denied')


# runs user input sequence
enter_otp_sequence()