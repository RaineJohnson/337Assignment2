import hashlib
KEY = '800770FF00FF08012' # Secret key (initialization vector)
OTP_LENGTH = 6
SYNC_LENGTH = 100 # number of OTPs ahead that will be accepted

# Fills the list to contain the next (SYNC_LENGTH + 2) full hashes
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
    for i in range(len(next_hashes), SYNC_LENGTH + 2):
        byte_input = next_hashes[i - 1].encode()
        sha256_hash = hashlib.sha256(byte_input)
        hash_hex = sha256_hash.hexdigest()
        next_hashes.append(hash_hex)

# MAIN FUNCTION: asks user to enter OTPs until they exit the program
def enter_otp_sequence():
    # creates a list of the next SYNC_LENGTH hashes
    # (plus one to confirm synchronization, and one refill list later)
    next_hashes = []
    gen_hashes(next_hashes, KEY)
    otp_num = 1 # the number of the current OTP in the sequence

    while True:
        user_input = input('Enter OTP #' + str(otp_num) + ' (0 to quit): ')
        if user_input == '0':
            break

        cur_otp = next_hashes[0][-OTP_LENGTH:]  # last OTP_LENGTH digits of current hash

        # Grants access if the requested OTP is entered
        if user_input == cur_otp:
            print('Access Granted')
            otp_num += 1
            next_hashes = next_hashes[1:]
            gen_hashes(next_hashes)
            continue

        ''' Synchronization mechanism compares input to the next SYNC_LENGTH OTPs.
        If user_input is not the next OTP, but within the next SYNC_LENGTH,
        the program will skip ahead to that OTP, and ask for the following OTP
        to confirm that the user did not get lucky. '''
        access_granted = False
        for i in range(1, SYNC_LENGTH):
            cur_otp = next_hashes[i][-OTP_LENGTH:]
            confirmation_otp = next_hashes[i+1][-OTP_LENGTH:]

            if user_input == cur_otp:
                # Prompts user to enter the following OTP to confirm
                user_input = input('Synchronizing. Enter the next OTP: ')

                if user_input == confirmation_otp:
                    print('Access Granted')
                    access_granted = True
                    otp_num += (i + 2)
                    next_hashes = next_hashes[i+2:]
                    gen_hashes(next_hashes)
                    break
                else:
                    break


        if not access_granted:
            print('Access Denied')


# runs user input sequence
enter_otp_sequence()