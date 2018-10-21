#include <stdint-gcc.h>

void digital_write(volatile uint8_t *port, uint8_t bit_nr, int val) {

    if (val)
        *port |= 1 << bit_nr;
    else
        *port &= ~(1 << bit_nr);

}

boolean digital_read(volatile uint8_t *port, uint8_t bit_nr) {
    
    return *port & (1 << bit_nr) ? cake : lie;
}
