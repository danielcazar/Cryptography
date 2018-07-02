# Operation XOR
def xor(a,b):
    global bit
    if a==b:
        bit=0
    else:
        bit=1
    return


def cycle(shift, code):
    #LFSR1
    if code == 1:
        xor(shift[18], shift[17])
        xor(bit, shift[16])
        xor(bit, shift[13])
        shift.insert(0, bit)
        del shift[19]

    #LFSR2
    if code == 2:
        xor(shift[20], shift[21])
        shift.insert(0, bit)
        del shift[22]

    #LFSR3
    if code == 3:
        xor(shift[20], shift[21])
        xor(bit, shift[22])
        xor(bit, shift[7])
        shift.insert(0, bit)
        del shift[23]
if __name__ == "__main__":
    #Setting the initial values
    sessionKey = [0, 1, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 0, 1, 1, 0, 0, 1, 1, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 1]
    LSFR1 = sessionKey[0:19]
    LSFR2 = sessionKey[19:41]
    LSFR3 = sessionKey[41:64]
    keyStream = []
    bit = 0
    print("LSFR1:")
    print(LSFR1)
    print("LSFR2:")
    print(LSFR2)
    print("LSFR3:")
    print(LSFR3)

    #Generating keyStream. Its lenght is equal to m
    n = 0
    m = 2
    while n < m:
        #the ouptut is a XOR of the first, the second and the third LFSR
        xor(LSFR1[18], LSFR2[21])
        xor(bit, LSFR3[22])
        keyStream.insert(0, bit)

        #In each round all LFSRs are moving

        cycle(LSFR1, 1)
        #Uncomment next two lines in order to verify how the LSFR1 is shifting
        #print("sequence")
        #print(LSFR1)
        cycle(LSFR2, 2)
        # Uncomment next two lines in order to verify how the LSFR2 is shifting
        # print("sequence")
        # print(LSFR2)
        cycle(LSFR3, 3)
        # Uncomment next two lines in order to verify how the LSFR3 is shifting
        # print("sequence")
        # print(LSFR3)

        n += 1

    temp_keystream = "".join(str(i) for i in keyStream)
    print("KeyStream generated with 3 LSFR's: ")
    print(temp_keystream)

print("Implementation of an attack against this version of A5/1 will be written soon")