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