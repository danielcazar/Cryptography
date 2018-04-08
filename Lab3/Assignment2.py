#!/usr/bin/env python
# -*- coding: utf-8 -*-

import binascii
from Crypto.Cipher import AES
from Crypto import Random
import random

def pad(s):
    return s + (16 - len(s) % 16) * chr(16 - len(s) % 16)

def unpad(s):
    return s[:-ord(s[len(s) - 1:])]

# Modified version of AES. The IV is fixed and this allow us to exploit the Chosen Plaintext Attack.
def aes_cbc_encrypt(msg, iv_p=0):
    raw = pad(msg)
    if iv_p == 0:
        iv = Random.new().read(AES.block_size)
    else:
        iv = iv_p
    global key
    key = Random.new().read(AES.block_size)
    cipher = AES.new('P4ssw0rdP4ssw0rd', AES.MODE_CBC, iv)
    return cipher.encrypt(raw)

def xor_strings(xs, ys, zs):
    return "".join(chr(ord(x) ^ ord(y) ^ ord(z)) for x, y, z in zip(xs, ys, zs))

def xor_block(vector_init, previous_cipher, p_guess):
    xored = xor_strings(vector_init, previous_cipher, p_guess)
    return xored

def split_len(seq, length):
    return [seq[i:i + length] for i in range(0, len(seq), length)]

def game_cpa(plaintext):
    print "Start Distinguisher Game"
    print "*************************************************************"

    padding = 16

    # We assume that after sending a message (M0) to the challenger we receive a ciphertext call cipher1
    M0 = plaintext

    cipher1 = aes_cbc_encrypt("1" * (32) + M0)
    block1 = split_len(binascii.hexlify(cipher1), 32)

    #Setting up the Attacker
    b = chr(random.randint(0, 1))  # Random bit
    IV = str(cipher1[-16:])
    Ci = str(cipher1[0:16])
    M = "1"*padding + b # Message sent to the challenger after training phase. Message is composed of all 1s and string b

    # Make the trick. IV xor Ci xor M
    xored = xor_block(IV, Ci, M)
    # Encrypt the xored value
    cipher2 = aes_cbc_encrypt(xored, IV)
    block2 = split_len(binascii.hexlify(cipher2), 32)

    # Distinguisher made by the attacker. If Cipher2 = Cipher1, then Attacker wins.
    if block2[0] == block1[1]:
        print "Attacker Wins!!! "
        return  0
    else:
        print "Attacker Loses"
        return 1

print("Assignment #3")
print("CPA-Distinguisher AES CBC-mode")
print "*************************************************************"
# Run the Game
print(game_cpa("YELLOW SUBMARINE"))
