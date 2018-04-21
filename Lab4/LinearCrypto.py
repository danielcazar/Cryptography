import SPN as cipher
import itertools as it
import collections

def getNibbleBit(bits, n):
    return int(bin(bits)[2:].zfill(4)[n])

def getShortBit(bits, n):
    return int(bin(bits)[2:].zfill(16)[n])

sbox_in = ["".join(seq) for seq in it.product("01", repeat=4)]
sbox_out = [bin(cipher.sbox[int(seq, 2)])[2:].zfill(4) for seq in sbox_in]
sbox_b = collections.OrderedDict(zip(sbox_in, sbox_out))
probBias = [[0 for x in range(len(sbox_b))] for y in range(len(sbox_b))]

print('Linear Approximation Table: ')
for bits in sbox_b.items():
    input_bits, output_bits = bits
    X1, X2, X3, X4 = [int(bits, 2) for bits in [input_bits[0], input_bits[1], input_bits[2], input_bits[3]]]
    Y1, Y2, Y3, Y4 = [int(bits, 2) for bits in [output_bits[0], output_bits[1], output_bits[2], output_bits[3]]]

    equations_in = [0, X4, X3, X3 ^ X4, X2, X2 ^ X4, X2 ^ X3, X2 ^ X3 ^ X4, X1, X1 ^ X4,
                    X1 ^ X3, X1 ^ X3 ^ X4, X1 ^ X2, X1 ^ X2 ^ X4, X1 ^ X2 ^ X3, X1 ^ X2 ^ X3 ^ X4]

    equations_out = [0, Y4, Y3, Y3 ^ Y4, Y2, Y2 ^ Y4, Y2 ^ Y3, Y2 ^ Y3 ^ Y4, Y1, Y1 ^ Y4,
                     Y1 ^ Y3, Y1 ^ Y3 ^ Y4, Y1 ^ Y2, Y1 ^ Y2 ^ Y4, Y1 ^ Y2 ^ Y3, Y1 ^ Y2 ^ Y3 ^ Y4]

    for x_idx in range(0, len(equations_in)):
        for y_idx in range(0, len(equations_out)):
            probBias[x_idx][y_idx] += (equations_in[x_idx] == equations_out[y_idx])

# print linear approximation table
for bias in probBias:
    for bia in bias:
        print('{:d}'.format(bia - 8).zfill(2), end=' ')
    print('')

################Attacking#############################

k = cipher.keyGeneration()
k5_bin = bin(int(k,16))[2:].zfill(5*cipher.blockSize)[-16:]

print('\nTest key k = {:}'.format(k), end = ' ')
print( '(k_5 = {:}).'.format(hex(int(k5_bin,2))[2:].zfill(4)))

lApproxAllsk = [0]*(1+0xFF)
for pt in range(10000):
    ct = cipher.encrypt(pt, k)
    for pskb_4_8 in range(1 + 0xF):
        for pskb_12_16 in range(1 + 0xF):
            ct_4_8 = int(bin(ct)[2:].zfill(16)[4:8], 2)
            ct_12_16 = int(bin(ct)[2:].zfill(16)[12:16], 2)

            #xor ciphertext with subKey bits
            v_4_8, v_12_16 = ct_4_8^pskb_4_8, ct_12_16^pskb_12_16

            #run backwards through sbox
            u_4_8, u_12_16 = cipher.sbox[v_4_8], cipher.sbox[v_12_16]

            #Compute linear approximation: U_4,6 ^ U_4,8 ^ U_4,14 ^ U_4,16 ^ P_5 ^ P_7 ^ P_8
            lApprox = getNibbleBit(u_4_8, 1)^getNibbleBit(u_4_8, 3)^getNibbleBit(u_12_16, 1)^getNibbleBit(u_12_16, 3)
            lApprox = lApprox^getShortBit(pt, 4)^getShortBit(pt, 6)^getShortBit(pt, 7)
            lApproxAllsk[(pskb_4_8<<4)+pskb_12_16] += lApprox
            
attackResults = [fabs(lAprx - 5000)/10000.0 for lAprx in lApproxAllsk]

maxResult, maxIdx = 0,0
for rIdx, result in enumerate(attackResults):
    if result > maxResult:
        maxResult = result
        maxIdx = rIdx

print('Highest Bias is {:} for subKey bits {:}.'.format(maxResult, hex(maxIdx)[2:]))
print(attackResults)