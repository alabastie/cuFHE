################################################################################
# Copyright 2018 Gizem S. Cetin <gscetin@wpi.edu>
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER
# DEALINGS IN THE SOFTWARE.
################################################################################

import lib.fhe as fhe
import operator
import time
import random
import timeit

inputs1 = [0, 1]
circuits1 = ['__invert__']

inputs2 = [(0, 0), (0, 1), (1, 0), (1, 1)]
circuits2 = ['__and__', '__or__', '__xor__', '__lt__', '__le__', '__eq__',
			'__ne__', '__gt__', '__ge__']

# Rand Seeds
random.seed()
fhe.SetSeed()

# Keys
pubkey, prikey = fhe.KeyGen()
print(pubkey)
#fhe.StoreKeys(pubkey, prikey)
fhe.Init(pubkey)

# ADDITION
if fhe.UseGPU():
	length = 30
else:
	length = 2
m1, m2 = random.getrandbits(length-1), random.getrandbits(length-1)
c1 = fhe.Encrypt(m1, prikey, length)
c2 = fhe.Encrypt(m2, prikey, length)
start_time = timeit.default_timer()
c = c1 * c2
elapsed = timeit.default_timer() - start_time
result = c.Decrypt(prikey)
print m1, " * " , m2, " = ", result
print elapsed, " sec"

# ei1 = [fhe.Encrypt(i, prikey) for i in inputs1]

# for circuit in circuits1:
# 	for i in range(len(inputs1)):
# 		i = inputs1[i]
# 		c1 = ei1[i]
# 		func = getattr(operator, circuit)
# 		start_time = timeit.default_timer()
# 		c = func(c1)
# 		elapsed_time = timeit.default_timer() - start_time
# 		result = c.Decrypt(prikey)
# 		passed = "PASS" if (result == (func(i) & 1)) else "FAIL"
# 		print "Test " + circuit + ": " + passed
# 		print "In " + str(elapsed_time) + " seconds"

# ei2 = [(fhe.Encrypt(i[0], prikey), fhe.Encrypt(i[1], prikey)) for i in inputs2]

# for circuit in circuits2:
# 	for i in range(len(inputs2)):
# 		c1, c2 = ei2[i]
# 		i = inputs2[i]
# 		func = getattr(operator, circuit)
# 		start_time = timeit.default_timer()
# 		c = func(c1, c2)
# 		elapsed_time = timeit.default_timer() - start_time
# 		result = c.Decrypt(prikey)
# 		passed = "PASS" if (result == func(i[0], i[1])) else "FAIL"
# 		print "Test " + circuit + ": " + passed
# 		print "In " + str(elapsed_time) + " seconds"

# # Encryption & Decryption
# msg = random.randint(0,1)
# ctxt = fhe.Encrypt(msg, prikey)
# print "Encrypted message : ", msg
# msg = fhe.Decrypt(ctxt, prikey)
# print "Decrypted message : ", msg

# # Homomorphic Evaulations
# # AND
# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# start_time = timeit.default_timer()
# c = c1 & c2
# elapsed = timeit.default_timer() - start_time
# result = c.Decrypt(prikey)
# print m1, " & " , m2, " = ", result
# print elapsed, " sec"

# # XOR
# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 ^  c2
# result = c.Decrypt(prikey)
# print m1, " ^ " , m2, " = ", result

# # OR
# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 | c2
# result = c.Decrypt(prikey)
# print m1, " | " , m2, " = ", result

# # NOT
# m1 = random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c = ~c1
# result = c.Decrypt(prikey)
# print "~", m1, " = ", result

# # COMPARE
# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 < c2
# result = c.Decrypt(prikey)
# print m1, " < " , m2, " = ", result

# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 <= c2
# result = c.Decrypt(prikey)
# print m1, " <= " , m2, " = ", result

# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 == c2
# result = c.Decrypt(prikey)
# print m1, " == " , m2, " = ", result

# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 != c2
# result = c.Decrypt(prikey)
# print m1, " != " , m2, " = ", result

# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 > c2
# result = c.Decrypt(prikey)
# print m1, " > " , m2, " = ", result

# m1, m2 = random.randint(0,1), random.randint(0,1)
# c1 = fhe.Encrypt(m1, prikey)
# c2 = fhe.Encrypt(m2, prikey)
# c = c1 >= c2
# result = c.Decrypt(prikey)
# print m1, " >= " , m2, " = ", result

# # Multibit Evaluations

# # Bitwise AND
# length = 4
# m1, m2 = random.getrandbits(length), random.getrandbits(length)
# c1 = fhe.Encrypt(m1, prikey, length)
# c2 = fhe.Encrypt(m2, prikey, length)
# start_time = timeit.default_timer()
# c = c1 & c2
# elapsed = timeit.default_timer() - start_time
# result = c.Decrypt(prikey)
# print m1, " & " , m2, " = ", result
# print elapsed, " sec"
