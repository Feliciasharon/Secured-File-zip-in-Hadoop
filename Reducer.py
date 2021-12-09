#!/usr/bin/python3.8

import sys
import heapq
import os
import random
import time

punc="+_=-}{][|\?/><*&~`!@#$%^&*().'',;:"
w=""
for line in sys.stdin:
    line = line.strip()
    a = line.split("\n")
    for i in a:
        w=i+" "+w
    
    
class HuffmanCoding:
	def __init__(self, w):
		self.w = w
		self.heap = []
		self.codes = {}
		self.reverse_mapping = {}
        
        
	class HeapNode:
		def __init__(self, char, freq):
			self.char = char
			self.freq = freq
			self.left = None
			self.right = None

		# defining comparators less_than and equals
		def __lt__(self, other):
			return self.freq < other.freq

		def __eq__(self, other):
			if(other == None):
				return False
			if(not isinstance(other, HeapNode)):
				return False
			return self.freq == other.freq

	# functions for compression:
	d=""
	def make_frequency_dict(self, text):
		frequency = {}
		for character in text:
			if not character in frequency:
				frequency[character] = 0
			frequency[character] += 1
		return frequency

	def make_heap(self, frequency):
		for key in frequency:
			node = self.HeapNode(key, frequency[key])
			heapq.heappush(self.heap, node)

	def merge_nodes(self):
		while(len(self.heap)>1):
			node1 = heapq.heappop(self.heap)
			node2 = heapq.heappop(self.heap)

			merged = self.HeapNode(None, node1.freq + node2.freq)
			merged.left = node1
			merged.right = node2

			heapq.heappush(self.heap, merged)


	def make_codes_helper(self, root, current_code):
		if(root == None):
			return

		if(root.char != None):
			self.codes[root.char] = current_code
			self.reverse_mapping[current_code] = root.char
			return

		self.make_codes_helper(root.left, current_code + "0")
		self.make_codes_helper(root.right, current_code + "1")


	def make_codes(self):
		root = heapq.heappop(self.heap)
		current_code = ""
		self.make_codes_helper(root, current_code)


	def get_encoded_text(self, text):
		encoded_text = ""
		for character in text:
			encoded_text += self.codes[character]
			#print("character-",character,", encodedtxt=",self.codes[character])
		return encoded_text


	def pad_encoded_text(self, encoded_text):
		extra_padding = 8 - len(encoded_text) % 8
		for i in range(extra_padding):
			encoded_text += "0"

		padded_info = "{0:08b}".format(extra_padding)
		encoded_text = padded_info + encoded_text
		return encoded_text


	def get_byte_array(self, padded_encoded_text):
		if(len(padded_encoded_text) % 8 != 0):
			d="Encoded text not padded properly"
			exit(0)

		b = bytearray()
		for i in range(0, len(padded_encoded_text), 8):
			byte = padded_encoded_text[i:i+8]
			b.append(int(byte, 2))
		return b


	def compress(self):
		
			p = w.rstrip()

			frequency = self.make_frequency_dict(p)
			self.make_heap(frequency)
			self.merge_nodes()
			self.make_codes()

			encoded_text = self.get_encoded_text(p)
			padded_encoded_text = self.pad_encoded_text(encoded_text)

			b = self.get_byte_array(padded_encoded_text)
			d=b
			return d,encoded_text
	
	
	def remove_padding(self, padded_encoded_text):
		padded_info = padded_encoded_text[:8]
		extra_padding = int(padded_info, 2)

		padded_encoded_text = padded_encoded_text[8:] 
		encoded_text = padded_encoded_text[:-1*extra_padding]

		return encoded_text

	def decode_text(self, encoded_text):
		current_code = ""
		decoded_text = ""

		for bit in encoded_text:
			current_code += bit
			if(current_code in dec):
				character = dec[current_code]
				decoded_text += character
				current_code = ""

		return decoded_text


	def decompress(self, encoded):
	        bit_string = ""
	        '''i=0
	        type(encoded)
	        byte=byte(encoded[i++])
	        while(len(byte) > 0):
                   byte = ord(byte)
                   bits = bin(byte)[2:].rjust(8, '0')
                   bit_string += bits
                   byte = byte(encoded[i++])
	        encoded_text = self.remove_padding(bit_string)
	        decompressed_text = self.decode_text(encoded_text)
	        return decompressed_text
	
	        '''
	        sample=encoded
	        leng=len(sample)
	        for i in range(0,leng):
	          byte=sample[i]
	          if(byte>0):
	              #byte = ord(byte)
	              bits = bin(byte)[2:].rjust(8, '0')
	              bit_string += bits
	        encoded_text = self.remove_padding(bit_string)
	        decompressed_text = self.decode_text(encoded_text)
	        return decompressed_text
	
def keys():
    hash = random.getrandbits(20)
    
    global key
    key=bin(hash)
    return key

def symbol(h):
    s=""
    for x in h.reverse_mapping:
        s=s+str(h.reverse_mapping[x])+" : "+str(x)+" / "
        
    return h.reverse_mapping
'''    
def encrypt(h):
    s=""
    for x in h.reverse_mapping:
        s1=str(x);
        n=len(s1)
        s2=key[2:n]
        s3=str(bin(int(s1,2) ^ int(s2,2)))
        s=s+str(h.reverse_mapping[x])+" : "+s3[2:len(s3)]+" / "
    return s
'''
def encrypt(h):
    global en
    en={}
    
    for x in h.reverse_mapping:
        
        s1=str(x);
        n=len(s1)
        #print(s1)
        
        s2=key[2:n+2]
        #print(s2)
        s3=bin(int(s1,2) ^ int(s2,2))
        
        
        s3=s3[2:len(s3)]
        es=''
        for i in range(n-len(s3)):
            es=es+'0'
        es+=s3;
        en[es]=h.reverse_mapping[x]
    return en
    
def decrypt(h):
    global dec
    dec={}
    
    for x in en:
        s1=str(x)
        n=len(s1)
        s2=key[2:n+2]
        s3=str(bin(int(s1,2) ^ int(s2,2)))
        s3=s3[2:len(s3)]
        es=''
        for i in range(n-len(s3)):
            es=es+'0'
        es+=s3;
        
        dec[es]=en[x]
    
    return dec


def analysis(decomp,comp):
    #size=sys.getsizeof(decomp)
    #size2=sys.getsizeof(comp)
    file_size=len(decomp)
    comprfile_size=len(comp)
    percentage=100-comprfile_size*100/file_size
    s="The size of Original text file(in bytes) ="+str(len(decomp)) +"\nThe size of Compressed text file(in bytes) ="+str(len(comp))+"\nThe Percentage of compression = "+str(round(percentage,2))+ "%"
    return s
    
    
           		
h = HuffmanCoding(w)

begin=time.time()
output,cp= h.compress()
end=time.time()

k=keys()
sym=symbol(h)

begin2=time.time()
e=encrypt(h)
end2=time.time()

d=decrypt(h)
output2=h.decompress(output)
a=analysis(output2,output)

#print("Original text\n"+str(w)+"\n\nCompressed text\n"+str(cp)+"\n\nSymbol table\n"+str(sym))
print('%s\n%s' %  ("","Original text\n"+str(w)+"\n\nCompressed text\n"+str(cp)+"\n\nSecret Key\n"+str(k)+"\n\nSymbol table\n"+str(sym)+"\n\nEncrypted Symbol table\n"+str(e)+"\n\nDecrypted Symbol table\n"+str(d)+ "\n\nDecompressed text\n"+str(output2)+"\n\nAnalysis\n"+str(a)+"\n\nCompression time\n"+str(end-begin)+"\n\nEncryption time of symbol tale\n"+str(end2-begin2)))
