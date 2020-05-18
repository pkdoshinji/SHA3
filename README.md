# SHA-3
Python implementation of the SHA3-256 hash

The Secure Hash Algorithm-3 is a family of cryptographic hash functions based on the Keccak algorithm designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche. There are four SHA3 hash functions: SHA3-224, SHA3-256, SHA3-384, and SHA3-512. (The numerical suffix designates the bit length of the output hash.) All four SHA3 functions make use of a *sponge construction*, a framework for extracting output of arbitrary length.

The command-line tool presented here is an implementation of the SHA3-256 hash function. While it produces accurate results, it has not been optimized for either performance or security. Rather, it is intended primarily as a pedagogical tool.   

## Usage
The string to be hashed is entered on the command line using the "-m" switch:
> ./SHA3.py -m "hello"
> 3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392
>
> ./SHA3.py -m ""
> a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a

(default output is 256 bits, or SHA3-256)


> ./SHA3.py -m "hello" -o 512
> 75d527c368f2efe848ecf6b073a36767800805e9eef2b1857d5f984f036eb6df891d75f72d9b154518c1cd58835286d1da9a38deba3de98b5a53e5ed78a84976

(512-bit output gives SHA3-512)

For the NIST specifications of the SHA3 hash, see https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf
