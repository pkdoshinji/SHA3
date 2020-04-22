#!/usr/bin/env python3

import numpy as np


l_list = [0,1,2,3,4,5,6]
l = l_list[6]
w = (2 ** l)
b = 25 * w
capacity = 512
rate = b - capacity
d = 256


shifts = np.array([[0, 36, 3, 41, 18],
                  [1, 44, 10, 45, 2],
                  [62, 6, 43, 15, 61],
                  [28, 55, 25, 21, 56],
                  [27, 20, 39, 8, 14]])

RCs = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
       0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
       0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
       0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
       0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
       0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
       0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
       0x8000000000008080, 0x0000000080000001, 0x8000000080008008]


def get_bitstring(message):
    # Convert the message to a string of 1s and 0s
    bitstring = ''
    for character in message:
        byte = '{0:08b}'.format(ord(character))
        byte = byte[::-1] # Convert to Little-endian
        bitstring += byte
    bitstring += '01100000' # Add the SHA-3 suffix
    return bitstring


def string_to_array(string,w=64):
    # Convert a bitstring to (5x5xw) numpy array
    state_array = np.zeros([5,5,w], dtype=int)
    for x in range(5):
        for y in range(5):
            for z in range(w):
                if (w*(5*x+y)+z) < len(string):
                    state_array[y][x][z] = int(string[w*(5*x+y)+z])
    return state_array


def hex_to_array(hexnum, w=64):
    # Convert a hexstring to a 1-dimensional numpy array
    bitstring = '{0:064b}'.format(hexnum)
    bitstring = bitstring[-w:]
    array = np.array([int(bitstring[i]) for i in range(w)])
    return array


def pad(rate, message_length):
    # Pad the bitstring using pad10*1, as per the SHA-3 specifications
    j = (-(message_length+1))%rate
    return '0' * j + '1'


def theta(array, w=64):
    # For each column, XOR the parity of two adjacent columns
    array_prime = array.copy()
    C, D = np.zeros([5,w], dtype=int), np.zeros([5,w], dtype=int)
    for x in range(5):
        for y in range(5):
            C[x] ^= array[x][y] # C[x] is a lane, each entry represents the column parity
    for x in range(5):
        D[x] = C[(x-1)%5] ^ np.roll(C[(x+1)%5],1) # D[x] is a placeholder
    for x in range(5):
        for y in range(5):
            array_prime[x][y] ^= D[x] # For each lane, XOR the value of D[x]
    return array_prime


def rho(array, w=64):
    # Circular shift each lane by a precalculated amount (given by the shifts array)
    array_prime = array.copy()
    for x in range(5):
        for y in range(5):
            array_prime[x][y] = np.roll(array[x][y], shifts[x][y])
    return array_prime


def pi(array, w=64):
    # 'Rotate' each slice according to a modular linear transformation
    array_prime = array.copy()
    for x in range(5):
        for y in range(5):
            array_prime[x][y] = array[((x) + (3 * y)) % 5][x]
    return array_prime


def chi(array, w=64):
    # Bitwise transfoirmation of each row according to a nonlinear function
    array_prime = np.zeros(array.shape, dtype=int)
    for x in range(5):
        for y in range(5):
            array_prime[x][y] = array[x][y] ^ ((array[(x + 1) % 5][y]^1) & (array[(x + 2) % 5][y]))
    return array_prime


def iota(array, round_index, w=64):
    # XOR each lane with a precalculated round constant
    RC = hex_to_array(RCs[round_index],w)
    RC = np.flip(RC)
    array_prime = array.copy()
    array_prime[0][0] ^= RC
    return array_prime


def keccak(state):
    # The keccak function defines one transformation round, SHA-3 has 24 in total
    for round_index in range(24):
        state = iota(chi(pi(rho(theta(state)))),round_index)
    return state


def squeeze(array, bits):
   # 'Squeezing' phase of the sponge construction yields the hash
    hash = ''
    for i in range(5):
        for j in range(5):
            lane = array[j][i]
            lanestring = ''
            for m in range(len(lane)):
                lanestring += str(lane[m])
            for n in range(0,len(lanestring),8):
                byte = lanestring[n:n+8]
                byte = byte[::-1] #Convert from Little-endian
                hash += '{0:02x}'.format(int(byte,2))
    return hash[:int(bits/4)]



message = 'hello'

bitstring = get_bitstring(message)
padded = bitstring + pad(rate, len(bitstring)%rate)

state = string_to_array(padded)
state = keccak(state)

print(squeeze(state,d))
