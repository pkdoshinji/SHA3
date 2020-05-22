#!/usr/bin/env python3

''' 
Author: Patrick kelly
Last updated: May 22, 2020
'''

import sys
import numpy as np
import argparse

# Keccak constants, hard-coded for the SHA3 family of hashes 
l_list = [0,1,2,3,4,5,6]
l = l_list[6]
w = (2 ** l)
b = 25 * w

# Precalculated values for rho function bitshifts
shifts = [[0, 36, 3, 41, 18],
          [1, 44, 10, 45, 2],
          [62, 6, 43, 15, 61],
          [28, 55, 25, 21, 56],
          [27, 20, 39, 8, 14]]

# Precalculated values for iota function round constants
RCs = [0x0000000000000001, 0x0000000000008082, 0x800000000000808a,
       0x8000000080008000, 0x000000000000808b, 0x0000000080000001,
       0x8000000080008081, 0x8000000000008009, 0x000000000000008a,
       0x0000000000000088, 0x0000000080008009, 0x000000008000000a,
       0x000000008000808b, 0x800000000000008b, 0x8000000000008089,
       0x8000000000008003, 0x8000000000008002, 0x8000000000000080,
       0x000000000000800a, 0x800000008000000a, 0x8000000080008081,
       0x8000000000008080, 0x0000000080000001, 0x8000000080008008]

def get_bitstring(message):
    # Convert the message string to a bitstring of 1s and 0s
    bitstring = ''
    for character in message:
        byte = '{0:08b}'.format(ord(character))
        byte = byte[::-1] # Convert to Little-endian
        bitstring += byte
    bitstring += '01100000' # Add the SHA-3 suffix
    return bitstring

def get_bitstring_from_file(filename):
    # Open a binary file and convert to bitstring
    with open(filename, 'rb') as fh:
        bytetext = fh.read()
    return bytes_to_bitstring(bytetext)

def bytes_to_bitstring(in_bytes):
    bitstring = ''
    for bytechar in in_bytes:
        byte = '{0:08b}'.format(bytechar)
        byte = byte[::-1]
        bitstring += byte
    bitstring += '01100000'
    return bitstring

def string_to_array(string,w=64):
    # Convert a bitstring to (5,5,w) numpy array
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
    # Bitwise transformation of each row according to a nonlinear function
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
                byte = byte[::-1] # Convert from Little-endian
                hash += '{0:02x}'.format(int(byte,2))
    return hash[:int(bits/4)]

def usage():
    print(f"[***] Usage: {sys.argv[0]} [-m <message string> | -i <filename>] -o <output-bits (224, 256, 384, or 512)>")
    exit()

def main():
    # The main event
    # Command line options (-m) with argparse module:
    parser = argparse.ArgumentParser()

    group = parser.add_mutually_exclusive_group()
    group.add_argument("-m", "--message", type=str, help="string to be hashed")
    group.add_argument("-i", "--input_file", type=str, help="input file to be hashed")
    parser.add_argument("-o", "--output_bits", type=str, help="hash function output bits (224, 256, 384, 512)")

    args = parser.parse_args()
    message = args.message
    filename = args.input_file

    # Get output bits value and validate; default is 256.
    if not args.output_bits:
        outbits = 256
    elif args.output_bits in ['224','256','384','512']:
        outbits = int(args.output_bits)
    else:
        usage()

    # Calculate capacity and rate from outbits
    capacity = 2 * outbits
    rate = b - capacity

    # Convert the input string or file to a bitstring
    if message:
        bitstring = get_bitstring(message)
    elif filename:
        bitstring = get_bitstring_from_file(filename)

    # Pad the bitstring according to the pad10*1 function (see SHA3 specifications)
    padded = bitstring + pad(rate, len(bitstring)%rate)

    # The sponge function absorbs <rate> bits per round, so (len(padded) // rate) rounds total 
    sponge_rounds = len(padded) // rate

    # Initialize the state array 
    state = np.zeros(b, dtype=int).reshape(5,5,w)

    # For each sponge round, absorb <rate> bits and process the state array with the keccak permutation
    for i in range(sponge_rounds):
        current_string = padded[(i*rate):(i*rate) + rate]
        array = string_to_array(current_string, w=64)
        state = np.bitwise_xor(state, array)
        state = keccak(state)

    # The 'squeeze' phase outputs the final hash value
    print(squeeze(state, outbits))
    exit()

if __name__ == '__main__':
    main()
