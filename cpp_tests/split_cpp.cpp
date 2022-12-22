#include <vector>
#include <string>
#include <iostream>
#include "./debug/debug.h"

using namespace std;

vector<string> split(string s, string splitter) {
	bool b = true;
	int i = 0;
	vector<string> arr;
	string _s;
	string __s;

	while(i < s.size()) {
		for(int x = 0; x < splitter.length(); x++) {
			if(i + x < s.length()) {
				if(s[i+x] != splitter[x]) {
					b = false;
					break;
				}
			}
		}
		if(b) {
			arr.push_back(__s);
			i += splitter.length() - 1;
			__s = "";
		}
		else {
			__s += s[i];
		}
		_s = "";
		i += 1;
		b = true;
	}
	arr.push_back(__s);
	return arr;
}

// TODO: SPLIT "" USING POINTERS

int main(void){
	string test_string;
	for(int i = 0; i < 100000; i++) {
		test_string += "     1";
	}
	start_time
	std::cout << '[';
	split(test_string, "  ");
	// for(auto s : split(test_string, "  ")) {
		// std::cout << s;
		// std::cout << ',';
	// }
	std::cout << ']' << std::endl;
	end_time
	// [Cpu_time_used: 0.041570]
	// py_split [0.011415243148803711]
	return 0;
}
