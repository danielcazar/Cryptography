import random
import hashlib

blockSize = 16
verboseState = False

sbox = {0: 0xE, 1: 0x4, 2: 0xD, 3: 0x1, 4: 0x2, 5: 0xF, 6: 0xB, 7: 0x8, 8: 0x3, 9: 0xA, 0xA: 0x6, 0xB: 0xC, 0xC: 0x5,
        0xD: 0x9, 0xE: 0x0, 0xF: 0x7}
sbox_inv = {0xE: 0, 0x4: 1, 0xD: 2, 0x1: 3, 0x2: 4, 0xF: 5, 0xB: 6, 0x8: 7, 0x3: 8, 0xA: 9, 0x6: 0xA, 0xC: 0xB,
            0x5: 0xC, 0x9: 0xD, 0x0: 0xE, 0x7: 0xF}

pbox = {0: 0, 1: 4, 2: 8, 3: 12, 4: 1, 5: 5, 6: 9, 7: 13, 8: 2, 9: 6, 10: 10, 11: 14, 12: 3, 13: 7, 14: 11, 15: 15}

def apply_sbox(state, sbox):
    subStates = [state & 0x000f, (state & 0x00f0) >> 4, (state & 0x0f00) >> 8, (state & 0xf000) >> 12]
    for idx, subState in enumerate(subStates):
        subStates[idx] = sbox[subState]
    return subStates[0] | subStates[1] << 4 | subStates[2] << 8 | subStates[3] << 12

def keyGeneration():
    k = hashlib.sha1(hex(random.getrandbits(blockSize * 8)).encode('utf-8')).hexdigest()[2:2 + 20]
    return k

def encrypt(pt, k):
    state = pt
    if verboseState: print('**pt = {:04x}**'.format(state))

    subKeys = [int(subK, 16) for subK in [k[0:4], k[4:8], k[8:12], k[12:16], k[16:20]]]

    for roundN in range(0, 3):

        if verboseState: print(roundN, end=' ')
        state = state ^ subKeys[roundN]
        if verboseState: print(hex(state), end=' ')

        state = apply_sbox(state, sbox)
        if verboseState: print(hex(state), end=' ')

        state_temp = 0
        for bitIdx in range(0, blockSize):
            if (state & (1 << bitIdx)):
                state_temp |= (1 << pbox[bitIdx])
        state = state_temp
        if verboseState: print(hex(state))

    state = state ^ subKeys[-2]
    if verboseState: print(str(3), hex(state), end=' ')
    state = apply_sbox(state, sbox)
    if verboseState: print(hex(state), end=' ')
    state = state ^ subKeys[-1]
    if verboseState: print(hex(state))
    if verboseState: print('**ct = {:04x}**'.format(state))
    return state

def decrypt(ct, k):
    state = ct
    if verboseState: print('**ct = {:04x}**'.format(state))

    subKeys = [int(subK, 16) for subK in [k[0:4], k[4:8], k[8:12], k[12:16], k[16:20]]]

    if verboseState: print(str(3), hex(state), end=' ')

    state = state ^ subKeys[4]
    if verboseState: print(hex(state), end=' ')

    state = apply_sbox(state, sbox_inv)
    if verboseState: print(hex(state))

    for roundN in range(2, -1, -1):

        if verboseState: print(roundN, end=' ')
        state = state ^ subKeys[roundN + 1]
        if verboseState: print(hex(state), end=' ')

        state_temp = 0
        for bitIdx in range(0, blockSize):
            if (state & (1 << bitIdx)):
                state_temp |= (1 << pbox[bitIdx])
        state = state_temp
        if verboseState: print(hex(state), end=' ')

        state = apply_sbox(state, sbox_inv)
        if verboseState: print(hex(state))
    if verboseState: print(roundN, end=' ')

    state = state ^ subKeys[0]
    if verboseState: print('**pt = {:04x}**'.format(state))
    return state