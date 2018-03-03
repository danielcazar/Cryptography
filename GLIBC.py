#!/usr/bin/python

#Glibc - random() function
def glibc(initial_value):
    int32 = lambda x: x & 0xffffffff - 0x100000000 if x & 0xffffffff > 0x7fffffff else x & 0xffffffff
    int64 = lambda \
        x: x & 0xffffffffffffffff - 0x10000000000000000 if x & 0xffffffffffffffff > 0x7fffffffffffffff else x & 0xffffffffffffffff

    r = [0] * 344
    r[0] = initial_value

    for i in range(1, 31):
        r[i] = int32(int64(16807 * r[i - 1]) % 0x7fffffff)

        if r[i] < 0:
            r[i] = int32(r[i] + 0x7fffffff)

    for i in range(31, 34):
        r[i] = int32(r[i - 31])

    for i in range(34, 344):
        r[i] = int32(r[i - 31] + r[i - 3])

    i = 344 - 1
    list = []

    while i<400:
        i += 1
        r.append(int32(r[i - 31] + r[i - 3]))
        var=int32((r[i] & 0xffffffff) >> 1)
        list.append(var)

    return list

#statistical test
def statistical_test_glibc(o):

    #Calculating modulus
    modulus = abs(o[31] - (o[0] + o[28]))

    #Checking randomness
    for i in range(31, 57):
        variable1=(o[i - 31] + o[i - 3])%modulus
        variable2=(o[i - 31] + o[i - 3] + 1)%modulus
        if (o[i] == variable1  or o[i] == variable2):
            print \
                "0 = The sequence generated Is Pseudo-Random"
        else:
            print \
                "1 = The sequence generated Is Random"

if __name__ == '__main__':
    print "Solution for Laboratory#1 - Assignment#2"
    print "======================================================================"
    print "Sequence GLIBC - random() Function"
    print "======================================================================"
    print(glibc(1))
    print("=================================================================")
    print("Checking every number from the sequence")
    print("=================================================================")
    statistical_test_glibc(glibc(1))
