#!/usr/bin/python
# coding=utf-8

import sys, getopt, os, struct
from Crypto.Cipher import AES
from Crypto.Hash import MD5, SHA256
import  Crypto.Util.Counter

MyKey = "9765432112345679" * 2
BlockSize = 16 * 64 * 1024
Padding = "@"

def encrypt(mode, IV, input_name, output_name):

	if mode != "ECB" and mode != "CBC" and mode != "CFB" and mode != "OFB" and mode != "CTR":
		print "Available modes: ECB, CBC, CFB, OFB, CTR."
		print "Please choose again!"
		sys.exit()

	if(mode == "ECB"):
		mode = AES.MODE_ECB
	elif (mode == "CFB"):
		mode = AES.MODE_CFB
	elif (mode == "OFB"):
		mode = AES.MODE_OFB
	elif (mode == "CBC"):
		mode =  AES.MODE_CBC
	elif (mode == "CTR"):
		mode = AES.MODE_CTR

	MyHash = SHA256.new(MyKey)
	key = MyHash.digest()
	MyHash = MD5.new(IV)
	IV = MyHash.digest()

	if (mode != AES.MODE_CTR):
		encryptor = AES.new(key, mode, IV)
	else:
		ctr = Crypto.Util.Counter.new(128, initial_value=long(IV.encode("hex"), 16))
		encryptor = AES.new(key, AES.MODE_CTR, counter=ctr)

	filesize = os.path.getsize(input_name)
	print "File size: ", filesize

	with open(input_name, "rb") as f_in:
		with open(output_name,"wb") as f_out:
			f_out.write(struct.pack('<Q',filesize))
			f_out.write(IV)

			while True:
				block = f_in.read(BlockSize)
				if len(block) == 0:
					break
				elif len(block) % 16 != 0:
					block = block + Padding * (16 - len(block) % 16)
				f_out.write(encryptor.encrypt(block))
	return

def decrypt(mode, input_name, output_name):
	if mode != "ECB" and mode != "CBC" and mode != "CFB" and mode != "OFB" and mode != "CTR":
		print "Available modes: ECB, CBC, CFB, OFB, CTR...."
		print "Please choose again!"
		sys.exit()

	if(mode == "ECB"):
		mode = AES.MODE_ECB
	elif (mode == "CFB"):
		mode = AES.MODE_CFB
	elif (mode == "OFB"):
		mode = AES.MODE_OFB
	elif (mode == "CTR"):
		mode = AES.MODE_CTR
	elif (mode == "CBC"):
		mode =  AES.MODE_CBC

	MyHash = SHA256.new(MyKey)
	key = MyHash.digest()

	with open(input_name, "rb") as f_in:
		size = struct.unpack('<Q',f_in.read(struct.calcsize('Q')))[0]
		size = long(size)
		IV = f_in.read(16)

		if (mode != AES.MODE_CTR):
			decryptor = AES.new(key, mode, IV)
		else:
			ctr = Crypto.Util.Counter.new(128, initial_value=long(IV.encode("hex"), 16))
			decryptor = Crypto.Cipher.AES.new(key, AES.MODE_CTR, counter=ctr)


		with open(output_name, "wb") as f_out:
			while True:
				block = f_in.read(BlockSize)
				if len(block) == 0:
					break
				content = decryptor.decrypt(block)
				f_out.write(content)
			f_out.truncate(size)
	return

def main(argv):
    #Change variable between encrypt and decrypt
    variable="encrypt"
    if variable=="encrypt":
        try:
            opts, args = getopt.getopt(argv,"hm:i:")
        except getopt.GetoptError:
            print "encrypt.py –m <mode> –i <IV> <input_file> <output_file>"
            sys.exit(2)

        if( len(args) != 3 and len(args) != 2):
            print "Type as: encrypt.py –m <mode> –i <IV> <input_file> <output_file>"
            sys.exit(2)

        input_file = args[0]
        if(len(args) == 2):
            output_file = args[1]
        else:
            output_file = input_file + ".enc"

        for opt, arg in opts:
            if opt == "-h":
                print "encrypt.py -m <mode> -i <IV> <input_file> <output_file>"
                sys.exit()
            elif opt == "-m":
                mode = arg.upper()
            elif opt == "-i":
                IV = arg

        encrypt(mode, IV, input_file, output_file)
        return

    if variable == "decrypt":
        try:
            opts, args = getopt.getopt(argv, "hm:")
        except getopt.GetoptError:
            print "decrypt.py –m <mode <infile> <outfile>"
            sys.exit(2)

        if (len(args) != 3 and len(args) != 2):
            print "decrypt.py –m <mode <infile> <outfile>"
            sys.exit(2)

        input_file = args[0]
        if (len(args) == 2):
            output_file = args[1]
        else:
            output_file = input_file + ".dec"

        for opt, arg in opts:
            if opt == "-h":
                print "decrypt.py –m <mode <infile> <outfile>"
                sys.exit()
            elif opt == "-m":
                mode = arg.upper()
        decrypt(mode, input_file, output_file)
        return

if __name__ == "__main__":
	main(sys.argv[1:])