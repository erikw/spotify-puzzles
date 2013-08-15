#!/usr/bin/env python
# Reverse binary representation of a number
# Input: decimal number
# Output: decimal number obtained by reversing the binary representation of the input.
# TODO  read python style doc, var naming

import sys
import math

def reverse_bin(bin_no):
    return "0b" + bin_no[::-1][:-2]

def main1():
    print(int(reverse_bin(bin(int(sys.stdin.readline()))), 2))

if __name__ == '__main__':
    main1()     # Simplest possilbe.
    #main2()    # Readable version of main1()
    #main3()    # Not using Pythons bin/int for bin<->int conversions but implements the manual algorithms.

#def read_number():
    #return int(sys.stdin.readline())


#def main2():
    #input_dec = read_number()
    #input_bin = bin(input_dec)
    #output_bin = reverse_bin(input_bin)
    #output_dec = int(output_bin, 2)
    
    #print(output_dec)


# VER3 - Not using Python's built in bin/int functions.
#def dec2bin(dec_no):
    #digits = round(math.ceil(math.log(dec_no, 2)))
    ##print("digits={:d}".format(digits))
    #substract_value = 2**(digits - 1)
    #bin_no = ""
    #while digits > 0:
        #if dec_no >= substract_value:
            #dec_no -= substract_value
            #bin_no += "1"
        #else:
            #bin_no += "0"
        #digits -= 1
        #substract_value /= 2
    #return bin_no



#def reverse_string(str):
    #return str[::-1]

#def bin2dec(bin_no):
    #dec_no = 0;
    #add_val = 2 ** (len(bin_no) - 1)
    #for i in bin_no:
        #if (int(i) == 1):
            #dec_no += add_val
        #add_val /= 2
    #return int(dec_no)

#def main():
    #input_dec = read_number()
    #input_bin = dec2bin(input_dec)
    #output_bin = reverse_string(input_bin)
    #output_dec = bin2dec(output_bin)
    #print(output_dec)
