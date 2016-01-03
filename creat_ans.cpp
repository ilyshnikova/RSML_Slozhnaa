#include <iostream>

int main() {
	std::cout << "id,answer\n";

	int n = 0;
	for (size_t i = 0; i < 10; ++i) {
		for (size_t j = 0; j < 30; ++j) {
			std::cout << n++ << "," << i << std::endl;
		}
	}

	return 0;
}
