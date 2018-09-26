import lib.fhe as fhe
import operator
import time
import random
import timeit


# def shitADD (a.ctxts_[].ctxt_, b.ctxts_.ctxt_, n)
# 	p.ctxt_ = [2*n]	#product holder
# 	ctxt_p2 = [2*n]

# 	for i in range n
# 		for j in range n
# 			AND(temp[i][j+i], a.ctxts_[j].ctxt_, b.ctxts_[i].ctxt_, st[0], self.pubkey_)

# 	temp[0] = temp[0] + temp[1]
# 	for i in range n
# 		temp[0] = temp[0] + temp[i]

# Rand Seeds
random.seed()
fhe.SetSeed()

# Keys
pubkey, prikey = fhe.KeyGen()
#fhe.StoreKeys(pubkey, prikey)
fhe.Init(pubkey)

c1 = fhe.test0(pubkey)
c2 = fhe.test0(pubkey)
# c3 = fhe.test0(pubkey)
# c4 = fhe.test0(pubkey)

c1 = c1*c2

p1 = c1.Decrypt(prikey)
p2 = c2.Decrypt(prikey)
# p3 = c3.Decrypt(prikey)
# p4 = c4.Decrypt(prikey)

print(p1)
print(p2)
# print(p3)
# print(p4)
