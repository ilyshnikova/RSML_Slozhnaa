#include <iostream>
#include <fstream>
#include <string>


int main() {
	double count = 0;

	std::ifstream in;
	in.open("answer.csv");

	std::string s;
	in >> s;

	std::cout << s << std::endl;

	int n = 0;

	for (size_t i = 0; i < 10; ++i) {
		for (size_t j = 0; j < 30; ++j) {
			in >> s;
			std::string n_s = std::to_string(n++) + "," + std::to_string(i);

			if (s == n_s) {
				count += 1;
			} else {
				std::cout << s << " : " << n_s << std::endl;
			}
		}
	}

	double res = double(count)/300.*100.;

	std::cout << count << std::endl;
	std::cout << res << std::endl;

	return 0;
}
