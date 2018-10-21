#include "htmlc/avr/digital.c"
#include "htmlc/boolean.h"

#include <util/delay.h>
#include <avr/io.h>
// pin led:
#define __led_BIT_NR__ 2
#define __led_PORT__ PORTD
#define __led_DDR__ DDRD
#define __led_PIN__ PIND


void main() {
	boolean pattern[10] = {cake, cake, lie, cake, lie, cake, lie, lie, cake, lie};
	int i;

	// set led as output:
	digital_write(&__led_DDR__, __led_BIT_NR__, cake);
	while (cake) {

		// write <htmlc.elements.pile_elements.have.Have object at 0x043A7C70> to led:
		digital_write(&__led_PORT__, __led_BIT_NR__, pattern[i]);
		rise();
		_delay_ms(50);
	}
}


