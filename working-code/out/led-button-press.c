#include "htmlc/boolean.h"
#include "htmlc/avr/digital.c"

#include <avr/io.h>

// pin myButton:
#define __myButton_BIT_NR__ 0
#define __myButton_PORT__ PORTB
#define __myButton_DDR__ DDRB
#define __myButton_PIN__ PINB

// pin myLed:
#define __myLed_BIT_NR__ 1
#define __myLed_PORT__ PORTB
#define __myLed_DDR__ DDRB
#define __myLed_PIN__ PINB


void main() {

	// set myButton as input:
	digital_write(&__myButton_DDR__, __myButton_BIT_NR__, lie);

	// set myLed as output:
	digital_write(&__myLed_DDR__, __myLed_BIT_NR__, cake);
	while (cake) {

		// write <htmlc.elements.avr.pin_elements.digital_read.DigitalRead object at 0x04D778D0> to myLed:
		digital_write(&__myLed_PORT__, __myLed_BIT_NR__, digital_read(&__myButton_PIN__, __myButton_BIT_NR__));
	}
}


