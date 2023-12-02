//readADC.c
// sample program to read one ADC channel 
#include <iostream>
#include <fstream>
#include "crate_lib.h"
#include "kbhit.c"
#include <chrono>
#include <ctime>
#include <limits>
typedef std::numeric_limits< double > dbl;


using namespace std;
using namespace std::chrono;

//put here the location (address N) of each module 
constexpr int N_DWDISP = 1;
constexpr int N_ADC = 19;		//ADC slot
constexpr int N_DISCR = 2;		// TRIGGER slot
constexpr int N_TDC = 17; 		// TDC slot
constexpr int N_FF = 15;  		// flip flop slot

int send_command(short crate_id,char N, char F, char A){
	CRATE_OP cr_op;
	cr_op.N = N;
	cr_op.F = F;
	cr_op.A = A;
	short res = CFSA(crate_id, &cr_op);
	if (res <0 ){
		cout << "Error sending function "<< F << " to module "<< N << endl; 
	}
	return cr_op.DATA;
}
// function overload 
int send_command(short crate_id,char N, char F, char A, int DATA){
	CRATE_OP cr_op;
	cr_op.N = N;
	cr_op.F = F;
	cr_op.A = A;
	cr_op.DATA = DATA;
	short res = CFSA(crate_id, &cr_op);
	if (res <0 ){
		cout << "Error sending function "<< F << " to module "<< N << endl; 
	}
	return cr_op.DATA;
}

int main (int argc, char *argv[]) {

	int nbr_prior_arg = 3;   // nbr  of arguement  before channels

	if (argc < (nbr_prior_arg+1) ) { /// at least one channel
		cout << "Three arguments expected (adc channel and max number of event (-1) for  infinity)" << endl;
		exit(1);
	}	

	const int nbr_channels = argc - nbr_prior_arg; // removing first 3 arguments


	//C111 data structure F, N,A,Q,X,DATA
	CRATE_OP cr_op;
	short crate_id, res;

	//open crate: default ip address for all Lab controllers: 192.168.0.98
	crate_id = CROPEN("192.168.0.98");
	if (crate_id < 0) {
		cout << "ERROR: Unable to connect with specified IP address ! \n";
		return 0;
	}
	cout << "Crate opened " << crate_id << endl;

	//scan the crate for modules (optional)
	unsigned int scan_result;
	res = CSCAN(crate_id, &scan_result);
	if (res < 0)
		cout << "Error scanning the crate : " << res << endl;
	for (int i=0; i < 24; i++ ) {
		if (scan_result & (1 << i))
			cout << "Station " << i+1 << " is filled with a module. \n";
	}
	//opne output data file
	bool done = false;
	string adcname;
	cout << "Enter filename for data file: ";
	cin >> adcname;
	//check status of data file
	done = false;
	while (!done) {
		std::ifstream fdata(adcname.c_str());
		if (fdata.is_open()) {
			cout << "Enter a different filename: ";
			cin >> adcname ;
		}

		else
			done = true;
	}
	std::ofstream fdata(adcname.c_str()); //open data file

	cout << "After opening fdata"<<endl;
	res = CCCZ(crate_id);
	cout << "After create CCCZ"<<endl;
	if (res<0){
		cout << "Error executing CCCZ operation: " << res << endl;
		return 0;
	}


	//clear ADC (all channels)
	cout << "Clearing ADC (all channels)..."<<endl;
	send_command(crate_id, N_ADC, 9, atoi(argv[nbr_prior_arg]));  	

	//clear ADC DISCR (all channels)
	cout << "Clearing ADC DISCR (all channels)"<<endl;
	send_command(crate_id, N_DISCR, 9, atoi(argv[nbr_prior_arg]+1));  	

	//clear TDC (all channels)
	cout << "Clearing TDC (all channels) ..."<<endl;
	send_command(crate_id, N_TDC, 9, atoi(argv[nbr_prior_arg]));  	

	//clear Flip/Flop function code 18
	cout << "Clearing Flip-Flop ..."<<endl;
	send_command(crate_id, N_FF, 18,0, 0xFF);  	

	int patt; //FF pattern
	int xadc1; //ADC data
	//std::cout << "patt prem "<< patt << std::endl;
	auto start = high_resolution_clock::now();
	int numberCounts = 0;
	while(1) {
		//check if trigger generated (check FlipFlop)
		patt = send_command(crate_id, N_FF,0,0);  	
		if (patt == 3) {
			numberCounts++;
			if (numberCounts % atoi(argv[2])  == 0){
				auto stop = high_resolution_clock::now();
				auto duration = duration_cast<microseconds>(stop - start);
				auto start = high_resolution_clock::now();
				cout << "Total number of counts: "<< numberCounts << " in "  << duration.count()/1e6 << " seconds" << endl;
			} 
			double crt_time  = std::chrono::duration_cast<std::chrono::duration<double,std::milli>>(std::chrono::high_resolution_clock::now().time_since_epoch()).count();
			std::cout.precision(dbl::max_digits10);
			// write time to file
			fdata << std::fixed << crt_time << "\t";

			//////////////////////////////////////////////////

			//read Z
			xadc1 = send_command(crate_id,N_DISCR, 0, atoi(argv[nbr_prior_arg]+1));  	
			//write Trigger to file
			fdata << xadc1 << "\t";

			for (int i = 0; i < nbr_channels; i++) {
				//read ADC first channel
				xadc1 = send_command(crate_id,N_ADC, 0, atoi(argv[i+nbr_prior_arg]));  	
				//write adc to file          
				fdata << xadc1 << "\t";

			}

			for (int i = 0; i < nbr_channels; i++) {
				//read TDC first channel
				xadc1 = send_command(crate_id,N_TDC, 0, atoi(argv[i+nbr_prior_arg]));  	
				//write tdc to file
				if (i != (nbr_channels-1)) {
					fdata << xadc1 << "\t";
				}
				else {
					fdata << xadc1 << endl;
				}
			}


			// CLEAR ADC
			send_command(crate_id,N_ADC, 9, atoi(argv[nbr_prior_arg]));  	
			//clear DISCR (all channels)
			send_command(crate_id,N_DISCR, 9, atoi(argv[nbr_prior_arg]+1));  	
			// CLEAR TDC
			send_command(crate_id,N_TDC, 9, atoi(argv[nbr_prior_arg]));  	
			//clear Flipflop
			send_command(crate_id,N_FF, 18,0,0xFF);  	
			if (kbhit()) { //to ext the loop by pushing keyborard
				cout << endl << "Ending loop" << endl;
				break;
			}
			else if ((numberCounts >= atoi(argv[1])) && (atoi(argv[1]) != -1)){
				cout<< "Max data reached, exiting"<<endl;
				break;
			}
		}
	}
	//close crate 
	CRCLOSE(crate_id);
	cout << endl << "Bye bye !" << endl;

	return 0;
}




