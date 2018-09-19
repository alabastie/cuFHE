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

  Ptxt* apt = new Ptxt[N];
  Ptxt* bpt = new Ptxt[N];
  Ptxt* zpt = new Ptxt[N];
  Ptxt* cipt = new Ptxt[N];
  Ptxt* copt = new Ptxt[N]; 
  

  Ctxt* act = new Ctxt[N];
  Ctxt* bct = new Ctxt[N];
  Ctxt* zct = new Ctxt[N];
  Ctxt* cict = new Ctxt[N];
  Ctxt* coct = new Ctxt[N]; 

 


//create the key
  cout<< "------ Key Generation ------" <<endl;
  KeyGen(pub_key, pri_key);

//create data
  	cout<<"A:"<<flush;
  	for(int i = N-1; i>=0; i--){
  		apt[i].message_ = rand() % Ptxt::kPtxtSpace;
  		cout<< apt[i].message_ << flush;
  	}
  	cout<<""<<endl;

  	cout<<"B:"<<flush;
  	for(int i = N-1; i>=0; i--){
  		bpt[i].message_ = rand() % Ptxt::kPtxtSpace;
  		cout<< bpt[i].message_ << flush;
  	}
  	cout<<""<<endl;
//encrypt the data
  cout<<"--- Your Data is Being Encrypted ---" <<endl;
    
    for (int i = N-1; i >= 0; i--){
    Encrypt(act[i], apt[i], pri_key);
    Encrypt(bct[i], bpt[i], pri_key);
    cout<<"."<<flush;
	}
   cout<<"" << endl;
   cout<<"--- Testing the 2 bit adder Function ---" <<endl;
   
   //first iteration doesnt have vaues for the carrys or output
   Xor(zct[0], act[0], bct[0], pub_key);
   And(cict[0], act[0], bct[0], pub_key);
//carry out is used often as a placeholder to hold the value of the current opperation to bring it over to the next opperation
   for (int i = 1; i < N; i++){
   		Xor(coct[i], bct[i], cict[i-1], pub_key); //using copt as a holder
   		Xor(zct[i], act[i], coct[i], pub_key); //gets the z value
   		// calculate the carry in for the next value = Ci(A+B) + A*B
   		cout<<"First two XOR" <<endl;
   		Xor(coct[i], act[i], bct[i], pub_key); // (A+B)
   		cout<<"First OR" << endl;
   		And(coct[i], cict[i], coct[i], pub_key); // ci(a+b)
   		cout<<"First And" << endl;
   		And(coct[i-1], act[i], bct[i], pub_key); //  A*B 
   		cout<< "Second And"<<endl;
   		Or(cict[i], coct[i], coct[i-1], pub_key); // Final Value
   		cout<< "." <<endl;
   } 

   cout<<"--- Decrypting ---"<< endl;
   for(int i = N-1; i>=0; i--){
   	Decrypt(zpt[i], zct[i], pri_key);
   	Decrypt(cipt[i],cict[i], pri_key);
   }
   cout<<"Output is: " <<flush;
    for(int i = N-1; i>=0; i--){
  
  		cout<< zpt[i].message_ << flush;
  	
  	}
  	cout<<""<<endl;
    /*cout<<"Carry Out is: "<<flush; //Ci is the carry out, in effect
    for(int i = N-1; i>=0; i--){
  
  		cout<< cipt[i].message_ << flush;
  	
  	}
  	cout<<""<<endl;*/
  	cout<<"Overflow is: "<<flush;
  	cout<< cipt[N-1].message_ << endl;
}  