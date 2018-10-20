// #include <avr/io.h>
// 
// #include  <avr/sfr_defs.h>
// 
// int main(void) {
// 	DDRD |= _BV(0);
// 	DDRD |= _BV(1);
// 	DDRB &= ~(1);
// 	DDRB &= ~(1<<2);
// 	
// 	while(1) {
// 		if (PINB & _BV(0))
// 			PORTD = _BV(0);
// 		else if(PINB & _BV(1))
// 			PORTD = 0b10;
// 	}
// } 


int main() {
	
	
	        DDRD |= _BV(0);	
	        DDRD |= _BV(1);	
	        DDRB &= ~(1);	
	        DDRB &= ~(1 << 2);	
	        	
	        while(1) {	
	            if (PINB & _BV(0))	
	                PORTD = _BV(0);	
	            else if(PINB & _BV(1))	
	                PORTD = 0b10;	
	        }
}


