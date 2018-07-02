#!/usr/bin/python
from fractions import gcd

#function that calculate a random sequence with LCG(Linear Congruential Generator)
def LCG(modulus, a, c, seed):
    count = 0
    #A sequence with 9 numbers
    lista = []
    while count < 9:
        seed=(a * seed + c) % modulus
        lista.append(seed)
        #print('{0:08b}'.format(seed))
        count += 1
    return lista

#function used in mulinv()
# return (g, x, y) a*x + b*y = gcd(x, y)
def egcd(a, b):
    if a == 0:
        return (b, 0, 1)
    else:
        g, x, y = egcd(b % a, a)
        return (g, y - (b // a) * x, x)

#function used to calculate a
# x = mulinv(b) mod n, (x * b) % n == 1
def mulinv(b, n):
    g, x, _ = egcd(b, n)
    if g == 1:
        return x % n

def find_modulus(seed):
#unknown c, a and modulus

#What we have:
    seed0 = seed[0]
    seed1 = seed[1]
    seed2 = seed[2]
    seed3 = seed[3]
    seed4 = seed[4]
    seed5 = seed[5]
    seed6 = seed[6]
    seed7 = seed[7]
    seed8 = seed[8]

    list_seed = seed
#Solution
#d0 = seed1 - seed0 = a*seed0 + c - seed0 = seed0*(a - 1) + c
#d1 = seed2 - seed1 = a*seed1 + c - seed1 = seed1*(a - 1) + c
#d1 - d0 = (seed1 - seed0)*(a - 1) = d0*(a - 1)
#d1 = a*d0
#d2 = seed3 - seed2 = a*seed2 + c - seed2 = seed2*(a - 1) + c
#d2 - d1 = (seed2 - seed1)*(a - 1) = d1*(a - 1)
#d2 = a*d1
#Now, try to do an operation in order to get 0 (mod modulus)
#d2*d0 - d1*d1 = (a*a*d0 * d0) - (a*d0 * a*d0) = 0 (mod modulus)

    d0 = seed1 - seed0
    d1 = seed2 - seed1
    d2 = seed3 - seed2
    d3 = seed4 - seed3
    d4 = seed5 - seed4
    d5 = seed6 - seed5
    d6 = seed7 - seed6
    d7 = seed8 - seed7

    trick1 = d2*d0 - d1*d1
    trick2 = d3*d1 - d2*d2
    trick3 = d4*d2 - d3*d3
    trick4 = d5*d3 - d4*d4
    trick5 = d6*d4 - d5*d5
    trick6 = d7*d5 - d6*d6

    modulus = abs(reduce(gcd,[trick1, trick2, trick3, trick4, trick5, trick6]))
    a = (seed2 - seed1) * mulinv(abs(seed1 - seed0), modulus) % modulus
    c = (seed1 - seed0 * a) % modulus

#Predicting seed
    seed_predicted1 = (seed0 * a + c) % modulus
    seed_predicted2 = (seed1 * a + c) % modulus
    seed_predicted3 = (seed2 * a + c) % modulus
    seed_predicted4 = (seed3 * a + c) % modulus
    seed_predicted5 = (seed4 * a + c) % modulus
    seed_predicted6 = (seed5 * a + c) % modulus
    seed_predicted7 = (seed6 * a + c) % modulus
    seed_predicted8 = (seed7 * a + c) % modulus
    list_seed_predicted= [seed0,seed_predicted1, seed_predicted2, seed_predicted3, seed_predicted4, seed_predicted5, seed_predicted6, seed_predicted7, seed_predicted8]

#Check randomness
    statistical_test(list_seed,list_seed_predicted)

def statistical_test(seed, seed_predicted):
    if seed == seed_predicted:
        print \
            "0 = The sequence generated Is Pseudo-Random"
    else:
        print \
            "1 = The sequence generated Is Random"

if __name__ == '__main__':
    # Generate the LCG sequence
    print "Solutions for Assignment #1"
    print "======================================================================"
    print "LCG"
    print "======================================================================"
    print "Sequence #1"
    print (LCG(2 ** 32, 22695477, 1, 123))
    print "Sequence #2"
    print (LCG(9, 4, 1, 0))
    print "\nStatistical Test for Sequence #1"
    find_modulus(LCG(2 ** 32, 22695477, 1, 123))
    print "Statistical Test for Sequence #2"
	find_modulus(LCG(9, 4, 1, 0))