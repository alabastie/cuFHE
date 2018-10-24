// Include these two files for CPU computing.
#include <include/cufhe_cpu.h>
using namespace cufhe;

#include <iostream>
using namespace std;


//int twoBitAdd(int)


int main() {
  uint32_t N = 3;
  SetSeed();  // set random seed
// create plane text array and cyphre array
  bool correct;
  PriKey pri_key;
  PubKey pub_key;
  //int N = 2; //This is the number of values in each array

  Ptxt* apt = new Ptxt;
  Ptxt* bpt = new Ptxt;
  Ptxt* zpt = new Ptxt;
  Ptxt* cipt = new Ptxt;
  Ptxt* copt = new Ptxt; 
  

  Ctxt* act = new Ctxt;
  Ctxt* bct = new Ctxt;
  Ctxt* zct = new Ctxt;
  Ctxt* cict = new Ctxt;
  Ctxt* coct = new Ctxt; 

 
//create the key
  cout<< "------ Key Generation ------" <<endl;
  KeyGen(pub_key, pri_key);

//create data
  	cout<<"A:"<<flush;
  	apt.message_ = rand() % Ptxt::kPtxtSpace;
  	cout<< apt.message_ << flush;
  	cout<<""<<endl;

  	cout<<"B:"<<flush;
  	
  	bpt.message_ = rand() % Ptxt::kPtxtSpace;
  	cout<< bpt.message_ << flush;
  	cout<<""<<endl;

    cout<<"Cin:"<<flush;
    
    cipt.message_ = rand() % Ptxt::kPtxtSpace;
    cout<< cipt.message_ << flush;
    cout<<""<<endl;

//encrypt the data
  cout<<"--- Your Data is Being Encrypted ---" <<endl; 
    
  Encrypt(act, apt, pri_key);
  Encrypt(bct, bpt, pri_key);
  Encrypt(cict, cipt, pri_key);

  cout<<"" << endl;

  cout<<"--- Testing the Full Adder---" <<endl;
  FA(act, bct, cict, zct, coct, pub_key)
 
  cout<<"--- Decrypting ---"<< endl;
  Decrypt(zpt, zct, pri_key);
  Decrypt(copt,coct, pri_key);
   
  cout<<"Output bit is: " <<flush;
  cout<< zpt.message_ << flush;
  cout<<""<<endl;

  cout<<"Carry Out is: "<<flush; 
  cout<< cpt[i].message_ << flush;
  cout<<""<<endl;
 } 