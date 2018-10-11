// Include these two files for CPU computing.
#include <include/cufhe_cpu.h>
using namespace cufhe;

#include <iostream>
using namespace std;


//int twoBitAdd(int)
int8_t dump_ptxt(Ptxt* p) {
  int8_t out = 0;

  for (int i = 0; i < 8; i++) {
    out |= p[i].message_ << i;
  }

  return out;
}

// Initialize a plaintext array
void init_ptxt(Ptxt* p, int8_t n) {
  for (int i = 0; i < 8; i++) {
    p[i].message_ = n & 0x1;
    n >>= 1;
  }
}

int main() {
  uint32_t N = 3;
  SetSeed();  // set random seed


//  plaintext
  Ptxt apt;
  Ptxt bpt;
  Ptxt zpt;
  Ptxt cipt;
  Ptxt copt; 
  

  Ctxt act;
  Ctxt bct ;
  Ctxt zct ;
  Ctxt cict;
  Ctxt coct;


  cout<< "------ Key Generation ------" <<endl;
  PriKey pri_key;
  PubKey pub_key;
  KeyGen(pub_key, pri_key);

// set values to the inputs for testing purpouses
  apt.message_ = 1;
  bpt.message_ = 1;
  cipt.message_ = 0;

  cout<<"A: "<<apt.message_<<endl;
  cout<<"B: "<<bpt.message_<<endl;
  cout<<"--- Your Data is Being Encrypted ---" <<endl; 
    
  Encrypt(act, apt, pri_key);
  Encrypt(bct, bpt, pri_key);
  Encrypt(cict, cipt, pri_key);

  cout<<"" << endl;

  cout<<"--- Testing the Full Adder---" <<endl;
  
  Fa(zct, coct, act, bct, cict, pub_key);
 
  cout<<"--- Decrypting ---"<< endl;
  Decrypt(zpt, zct, pri_key);
  Decrypt(copt,coct, pri_key);
   
  cout<<"Output bit is: " <<flush;
  cout<< zpt.message_ << flush;
  cout<<""<<endl;

  cout<<"Carry Out is: "<<flush; 
  cout<< copt.message_ << flush;
  cout<<""<<endl;
 } 