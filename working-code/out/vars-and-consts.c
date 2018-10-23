#include "htmlc/boolean.h"

static const int A_CONSTANT = 4;
char myChar = 'a';

void main() {
	static const int b = 5;
	int aNumber = 2809;
	aNumber = 200;
	aNumber = A_CONSTANT;
	myChar = 'x';
}

