# file: fhe.py
#
# description: Test either the CPU or GPU implementation of cuFHE
#
# note: This file depends on at least one of either fhepy_gpu.so or fhepy_cpu.so
#

# Attempt to import GPU module, fallback to CPU module
try:
	import lib.fhepy_gpu as fhe
	use_gpu = True
except:
	import lib.fhepy_cpu as fhe
	use_gpu = False

import time
import timeit
from multiprocessing import process
from multiprocessing import Pool

def UseGPU():
	return use_gpu

def LoadPubKey(pubfile="pubkey.txt"):
	pubkey = fhe.PubKey()
	fhe.ReadPubKeyFromFile(pubkey, pubfile)
	return pubkey

def LoadPriKey(prifile="prikey.txt"):
	prikey = fhe.PriKey()
	fhe.ReadPriKeyFromFile(prikey, prifile)
	return prikey

def LoadKeys(pubfile="pubkey.txt", prifile="prikey.txt"):
	return LoadPubKey(), LoadPriKey()

def StorePubKey(pubkey, pubfile="pubkey.txt"):
	fhe.WritePubKeyToFile(pubkey, pubfile)
	print("Public key is stored in ./" + pubfile)

def StorePriKey(prikey, prifile="prikey.txt"):
	fhe.WritePriKeyToFile(prikey, prifile)
	print("Private key is stored in ./" + prifile)

def StoreKeys(pubkey, prikey, pubfile="pubkey.txt", prifile="prikey.txt"):
	StorePubKey(pubkey, pubfile)
	StorePriKey(prikey, prifile)

def PriKeyGen():
	prikey = fhe.PriKey()
	fhe.PriKeyGen(prikey)
	return prikey

def PubKeyGen(prikey):
	pubkey = fhe.PubKey()
	fhe.PubKeyGen(pubkey, prikey)
	return pubkey

def KeyGen():
	prikey = PriKeyGen()
	return PubKeyGen(prikey), prikey

def Init(pubkey):
	if use_gpu:
		fhe.Initialize(pubkey)
	else:
		pass

def PtxtMod():
	return fhe.Ptxt().PtxtSpace

def Encrypt(ptxt, prikey, count=1, pubkey=None):
	if pubkey is None:
		pubkey = PubKeyGen(prikey)
	if isinstance(ptxt, (int, long)):
		msg = ptxt
		ptxt = fhe.Ptxt()
		if count == 1:
			ptxt.message = msg;
			ctxt = Ctxt(pubkey)
			fhe.Encrypt(ctxt.ctxt_, ptxt, prikey)
			return ctxt

		msg_bin = bin(msg)[2:].zfill(count)
		msg_list = []
		ct = CtxtList(count, pubkey)
		for i in range(count):
			ptxt.message = int(msg_bin[i], 2)
			fhe.Encrypt(ct.ctxts_[count - i - 1].ctxt_, ptxt, prikey)
		return ct

def Decrypt(ctxt, prikey):
	ptxt = fhe.Ptxt()
	if isinstance(ctxt, Ctxt):
		fhe.Decrypt(ptxt, ctxt.ctxt_, prikey)
		return ptxt.message

	if isinstance(ctxt, CtxtList):
		ptxt_list = ""
		for c in reversed(ctxt.ctxts_):
			fhe.Decrypt(ptxt, c.ctxt_, prikey)
			ptxt_list += str(ptxt.message)
		return int(ptxt_list, 2)

def SetSeed():
	fhe.SetSeed(int(time.time()))

def Synchronize():
	if use_gpu:
		fhe.Synchronize()
	else:
		# if (pinit == 1)
		# 	p.close()
		# 	p.join()
		# 	p = Pool()
		# else:
		# 	p = Pool()
		pass

def AND(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.AND(result, input1, input2, stream)
	else:
		#result1 = p.map(fhe.AND, args=(result, input1, input2, pubkey)) #may need a ctx.
		#p1.start()
		fhe.AND(result, input1, input2, pubkey)

def NAND(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.NAND(result, input1, input2, stream)
	else:
		fhe.NAND(result, input1, input2, stream)

def OR(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.OR(result, input1, input2, stream)
	else:
		#p3 = process( target = fhe.OR, args = (result, input1, input2, stream))
		fhe.OR(result, input1, input2, pubkey)
		#p3.start()

def NOR(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.NOR(result, input1, input2, stream)
	else:
		fhe.NOR(result, input1, input2, pubkey)

def XOR(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.XOR(result, input1, input2, stream)
	else:
		#p2 = process(target = fhe.XOR, args = (result, input1, input2, pubkey)) #may need ctx. like the AND
		fhe.XOR(result, input1, input2, pubkey)
		#p2.start()

def XNOR(result, input1, input2, stream=None, pubkey=None):
	if use_gpu:
		fhe.XNOR(result, input1, input2, stream)
	else:
		fhe.XNOR(result, input1, input2, pubkey)

def NOT(result, input1, stream=None):
	if use_gpu:
		fhe.NOT(result, input1, stream)
	else:
		fhe.NOT(result, input1)


class Stream:
	def __init__(self):
		if use_gpu:
			self.stream = fhe.Stream()
		else:
			self.stream = None

	def Create(self):
		if use_gpu:
			self.stream.Create()
		else:
			pass

		return self.stream


class Ctxt:
	def __init__(self, pubkey=None, zero = False):
		self.ctxt_ = fhe.Ctxt()
		self.pubkey_ = pubkey
		if zero:
			ctxt_2 = Ctxt(self.pubkey_)
			print(self.pubkey_)
			print (ctxt_2.pubkey_)
			NOT(ctxt_2.ctxt_, self.ctxt_)	#I know that i cant do the .ctxt_2 thing but its just supposed to be a temp variable
			print type(self.pubkey_)
			AND(self.ctxt_, self.ctxt_, ctxt_2.ctxt_, pubkey = pubkey)

	def Decrypt(self, prikey):
		return Decrypt(self, prikey)

	def Encrypt(self, msg, prikey):
		Encrypt(msg, prikey, self.pubkey_)
		return self

	def __and__(self, other):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		AND(result.ctxt_, self.ctxt_, other.ctxt_, st, self.pubkey_)
		Synchronize()
		return result

	def __xor__(self, other):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		XOR(result.ctxt_, self.ctxt_, other.ctxt_, st, self.pubkey_)
		Synchronize()
		return result

	def __or__(self, other):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		OR(result.ctxt_, self.ctxt_, other.ctxt_, st, self.pubkey_)
		Synchronize()
		return result

	def __invert__(self):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		NOT(result.ctxt_, self.ctxt_, st)
		Synchronize()
		return result

	def __eq__(self, other):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		XNOR(result.ctxt_, self.ctxt_, other.ctxt_, st, self.pubkey_)
		Synchronize()
		return result

	def __ne__(self, other):
		result = Ctxt(self.pubkey_)
		st = Stream().Create()
		Synchronize()
		XOR(result.ctxt_, self.ctxt_, other.ctxt_, st, self.pubkey_)
		Synchronize()
		return result

	def __lt__(self, other):
		return ~self & other

	def __le__(self, other):
		return ~self | other

	def __gt__(self, other):
		return self & ~other

	def __ge__(self, other):
		return self | ~other


class CtxtList:
	def __init__(self, length=0, pubkey=None, zero = False):
		self.ctxts_ = [Ctxt(pubkey, zero=zero) for i in range(length)]
		self.pubkey_ = pubkey


	def Decrypt(self, prikey):
		return Decrypt(self, prikey)

	def __and__(self, other):
		result = CtxtList(len(self.ctxts_), self.pubkey_)
		st = [Stream().Create() for i in range(len(self.ctxts_))]
		Synchronize()
		for i in range(len(self.ctxts_)):
			AND(result.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[i], self.pubkey_)
		Synchronize()
		return result

	def __xor__(self, other):
		result = CtxtList(len(self.ctxts_), self.pubkey_)
		st = [Stream().Create() for i in range(len(self.ctxts_))]
		Synchronize()
		for i in range(len(self.ctxts_)):
			XOR(result.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[i], self.pubkey_)
		Synchronize()
		return result

	def __or__(self, other):
		result = CtxtList(len(self.ctxts_), self.pubkey_)
		st = [Stream().Create() for i in range(len(self.ctxts_))]
		Synchronize()
		for i in range(len(self.ctxts_)):
			OR(result.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[i], self.pubkey_)
		Synchronize()
		return result

	def __invert__(self):
		result = CtxtList(len(self.ctxts_), self.pubkey_)
		st = [Stream().Create() for i in range(len(self.ctxts_))]
		Synchronize()
		for i in range(len(self.ctxts_)):
			AND(result.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, st[i], self.pubkey_)
		Synchronize()
		return result

	# ripple carry adder
    def __add__(self, other):
        x = CtxtList(len(self.ctxts_), self.pubkey_)    # temporaries
        y = CtxtList(len(self.ctxts_), self.pubkey_)
        z = CtxtList(len(self.ctxts_), self.pubkey_)
        c = CtxtList(len(self.ctxts_), self.pubkey_)    # carry
        r = CtxtList(len(self.ctxts_), self.pubkey_)    # result
        st = [Stream().Create() for i in range(2*len(self.ctxts_))]
        Synchronize()
        XOR(r.ctxts_[0].ctxt_, self.ctxts_[0].ctxt_, other.ctxts_[0].ctxt_, st[0], self.pubkey_)
        AND(c.ctxts_[0].ctxt_, self.ctxts_[0].ctxt_, other.ctxts_[0].ctxt_, st[1], self.pubkey_)
        for i in range(1, len(self.ctxts_)):
            XOR(x.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[2*i], self.pubkey_)
            AND(y.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[2*i+1], self.pubkey_)
        Synchronize()
        for i in range(1, len(self.ctxts_)):
            AND(z.ctxts_[i-1].ctxt_, x.ctxts_[i].ctxt_, c.ctxts_[i-1].ctxt_, st[0], self.pubkey_)
            XOR(r.ctxts_[i].ctxt_, x.ctxts_[i].ctxt_, c.ctxts_[i-1].ctxt_, st[1], self.pubkey_)
            Synchronize()
            OR(c.ctxts_[i].ctxt_, z.ctxts_[i-1].ctxt_, y.ctxts_[i].ctxt_, st[0], self.pubkey_)
            Synchronize()
        return r

    def __mul__(self, other):
        temp = [CtxtList(2*len(self.ctxts_), self.pubkey_, zero=True) for i in range(len(self.ctxts_))]
        st = [Stream().Create() for i in range(len(self.ctxts_))]

        Synchronize()

        for i in range (len(self.ctxts_)):
            for j in range (len(self.ctxts_)):
                AND(temp[i].ctxts_[j+i].ctxt_, self.ctxts_[j].ctxt_, other.ctxts_[i].ctxt_, st[j], self.pubkey_)
                Synchronize()

        for i in range (1, len(self.ctxts_)) :
            temp[0] = temp[0] + temp[i]
            Synchronize()

        return temp[0]


       # Notes to Keith: 
       #
       # so just double check me on the length of for loops, they may beed to be one less than they are
       # AKA an-1 and bn-1.
       #
       #
       # For the last row, we have to switch up our direction of adding from going left->right to going right->left
       # There is definitely probably some errors with which carry i am adding the product with, but i hope that 
       # at least this basicly psudo code will give the basic guideline on how this is done
       # 
       #
       # For the Final Prodcut values (P0-9 in the book), for the main loops the values going from LSB -> MSB will be 
       # product[an].ctxts_[j].ctxt, so gettign a new value once every row (just look at the diagram in book),
       # it is just the last product that is calculated in each row. 
       #
       # However, for the final line of code, the way I have it set up is using a different variable to hold 
       # those final values, mostly because it is late and I can't think too great. we will have to find a way to combine them
       # into one final variable.ctxts_
       #
       #
       #
       #If there are any questions, just text me I'll probably be up or watiing in the doctor's office






	def__mul__(self, other):
		temp = [CtxtList(2*len(self.ctxts_), self.pubkey_, zero=True) for i in range(len(self.ctxts_))]
		temp2 = [CtxtList(2*len(self.ctxts_), self.pubkey_, zero=True) for i in range(len(self.ctxts_))] #temp can just be a single ctxt it doesnt need to itterate with i
		carryin = [CtxtList(2*len(self.ctxts_), self.pubkey_, zero=True) for i in range(len(self.ctxts_))]
		product = [CtxtList(2*len(self.ctxts_), self.pubkey_, zero=True) for i in range(len(self.ctxts_))] #this needs to be length of other 
		st = [Stream().Create() for i in range(len(self.ctxts_))]

		an = len(self.ctxts_)
		bn = len(other.ctxts_)

#initializing the first products for the first row
		for i in range(an)
			AND(product[i].ctxts_[0].ctxt_, self[an-i].ctxts_, other[0].ctxts_, self.pubkey_) # makes all the first row input products


		for j in range(bn):

			AND(product[0].ctxts_[j].ctxt_, self[an].ctxts_, other[j].ctxts_, self.pubkey_) #the far left product

			for i in range (an):
				
				AND(temp2[i].ctxts_, self[an-1-i].ctxts_, other[j+1].ctxts_, self.pubkey_)
				carryin[i].ctxts_ = product[i].ctxts_ [j].ctxt_+ temp2[i].ctxts_
				product[i+1].ctxts_[j+1].ctxt_ = product[i].ctxts_[j].ctxt_ + temp2[i].ctxts_

		#----This is the last row ----
		AND(product[an].ctxts_[bn].ctxt_, self[an].ctxts_, other[bn].ctxts_, self.pubkey_) #the last product coming in from the left

		for i in range(an):
			productFinal[i].ctxt = product[an-i].ctxts_[bn] + carryin[i].ctxts_[bn] #this just adds the product (from LSB to MSB this time) with the carry in from the previous value
			carryin[i].ctxts_[bn+1] = product[an-i].ctxts_[bn] + carryin[i].ctxts_[bn]#this is the carry out addition; still need to figure that out.
			#productFinal is the bottom product values, in the textbook that is P5, where productFinal[0] is P5 and productFinal[an] is P9



def test0 (pubkey_):
	c = Ctxt(pubkey = pubkey_, zero = True)
	return c 

 #    def __add__(self, other):
 #        k = len(self.ctxts_)
 #        st = []
 #        for i in range(3*k):
 #            st.append(Stream())
 #            st[i].Create()
 #        Synchronize()

 #        ksa_p = CtxtList(k, self.pubkey_)
 #        ksa_g = CtxtList(k, self.pubkey_)
	# ksa_c = CtxtList(k, self.pubkey_)
	# ksa_s = CtxtList(k, self.pubkey_)

 #        for i in range(k):
 #            AND(ksa_g.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[3*i].stream, self.pubkey_)
 #            XOR(ksa_p.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[3*i+1].stream, self.pubkey_)
 #            XOR(ksa_s.ctxts_[i].ctxt_, self.ctxts_[i].ctxt_, other.ctxts_[i].ctxt_, st[3*i+2].stream, self.pubkey_)
	# Synchronize()

 #        begin = 0
 #        step = 1
	# while begin+step < k:
	#     for i in range(begin+step, k):
 #                id = i - begin - step
 #                ctxt = ksa_p.ctxts_[i].ctxt_
	#         AND(ksa_p.ctxts_[i].ctxt_, ctxt, ksa_p.ctxts_[i-step].ctxt_, st[2*id].stream, self.pubkey_)
	#         AND(ksa_c.ctxts_[i].ctxt_, ctxt, ksa_g.ctxts_[i-step].ctxt_, st[2*id+1].stream, self.pubkey_)
 #            Synchronize()

	#     for i in range(begin+step, k):
 #                id = i - begin - step
	#         OR(ksa_g.ctxts_[i].ctxt_, ksa_c.ctxts_[i].ctxt_, ksa_g.ctxts_[i].ctxt_, st[id].stream, self.pubkey_)
 #            Synchronize()
 #            step += 1
 #            begin += 1

 #        for i in range(1,k):
 #             XOR(ksa_s.ctxts_[i].ctxt_, ksa_s.ctxts_[i].ctxt_, ksa_g.ctxts_[i-1].ctxt_, st[i].stream, self.pubkey_)
 #        Synchronize()
 #        return ksa_s
