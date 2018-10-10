/*
 * Test cudaStreamSynchronize wrapper
 */

#include <include/cufhe_gpu.cuh>
using namespace cufhe;

#include <iostream>
using namespace std;

int main() {
  SetSeed(); // set random seed

  PriKey pri_key; // private key
  PubKey pub_key; // public key
  Ptxt* pt = new Ptxt[3];
  Ctxt* ct = new Ctxt[3];
  Stream st1, st2;

  cout<< "------ Key Generation ------" <<endl;
  KeyGen(pub_key, pri_key);

  Initialize(pub_key); // essential for GPU computing

  Synchronize();

  for (int i = 0; i < 2; i++) {
    pt[i].message_ = rand() % Ptxt::kPtxtSpace;
    cout<< "i: "<<i<<"  message: " + pt[i].message_<<endl;
    Encrypt(ct[i], pt[i], pri_key);
  }

  And(ct[2], ct[1], ct[0], st1);

  StreamSynchronize(st1);

  Xor(ct[0], ct[1], ct[2], st2);

  StreamSynchronize(st2);

  Decrypt(pt[2], ct[0], pri_key);

  cout<<"out: " + pt[2].message_<<endl;

  if ((pt[0].message_ & pt[1].message_) ^ pt[1].message_ == pt[2].message_)
    cout<<"PASS"<<endl;
  else
    cout<<"FAIL"<<endl;

  return 0;
}