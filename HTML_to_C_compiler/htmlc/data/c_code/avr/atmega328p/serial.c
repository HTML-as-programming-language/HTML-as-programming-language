#include <stdint-gcc.h>

void serial_begin(uint8_t baud) {

    uint8_t brc = (F_CPU / 16 / baud) - 1;

    UBRR0H = (brc >> 8);
    UBRR0L = brc;

    // enable tx & rx
	UCSR0B |= _BV(RXEN0) | _BV(TXEN0);
	// 8 bit chars:
	UCSR0C |= _BV(UCSZ00) | _BV(UCSZ01);
}

void serial_transmit(uint8_t data) {
	loop_until_bit_is_set(UCSR0A, UDRE0);
	UDR0 = data;
}

void serial_print(uint8_t message[]) {
	for (int i = 0; message[i] != 0; i++)
		serial_transmit(message[i]);
}

uint8_t serial_receive() {
	loop_until_bit_is_set(UCSR0A, RXC0);
	return UDR0;
}
