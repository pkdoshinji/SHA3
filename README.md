# SHA-3
Python implementation of the SHA3-256 hash

The Secure Hash Algorithm-3 is a family of cryptographic hash functions based on the Keccak algorithm designed by Guido Bertoni, Joan Daemen, Michaël Peeters, and Gilles Van Assche. There are four SHA3 hash functions: SHA3-224, SHA3-256, SHA3-384, and SHA3-512. (The numerical suffix designates the bit length of the output hash.) All four SHA3 functions make use of a *sponge construction*, a framework for extracting output of arbitrary length.

The command-line tool presented here is an implementation of the SHA3-224, SHA3-256, SHA3-384, and SHA3-512 hash functions. While it produces accurate results, it has not been optimized for either performance or security. Rather, it is intended primarily as a pedagogical tool.   

## Usage
The string to be hashed is entered on the command line using the "-m" switch. Alternately, the directory path of a binary file can be entered using the "-i" switch. The number of output bits is specified with the "-o" switch (default is 256 bits):

`./SHA3.py -m "hello"`</br>
3338be694f50c5f338814986cdf0686453a888b84f424d792af4b9202398f392</br>
**(default mode is SHA3-256)**

`./SHA3.py -m ""`</br>
a7ffc6f8bf1ed76651c14756a061d662f580ff4de43b49fa82d80a4b80f8434a</br> 
**(default mode is SHA3-256)**

`./SHA3.py -m "" -o 224`</br> 
6b4e03423667dbb73b6e15454f0eb1abd4597f9a1b078e3f5b5a6bc7</br> 
**(224-bit output mode gives SHA3-224)**

`SHA3.py -i "/usr/bin/xeyes"`</br>
bcdb7ca8a7cf2fe83c440f0f77752d8e4b22e61419afaee3feb667fb8e6c0f2d</br>
**(SHA3-256 hash of the binary ELF file xeyes)**

`./SHA3.py -m "hello" -o 512`</br>
75d527c368f2efe848ecf6b073a36767800805e9eef2b1857d5f984f036eb6df891d75f72d9b154518c1cd58835286d1da9a38deba3de98b5a53e5ed78a84976</br> 
**(512-bit output mode gives SHA3-512)**

For the NIST specifications of the SHA3 hash, see https://nvlpubs.nist.gov/nistpubs/FIPS/NIST.FIPS.202.pdf
