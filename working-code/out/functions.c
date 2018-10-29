#include "htmlc/boolean.h"

// Note that the function cannot be called multiply
// because there is a built-in tag called multiply 

int multiplyFunction(int a, int b) {
	return a * b;
}


void main() {
	int result = multiplyFunction(5, 6);
}

