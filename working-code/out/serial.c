#include "htmlc/boolean.h"
#include "htmlc/avr/atmega328p/serial.c"
#include "htmlc/boolean.h"



void main() {
	serial_begin(9600, 16000000);
	serial_print("I will echo everything you say\n\n");
	while (cake) {
		serial_transmit(serial_receive());
	}
}


