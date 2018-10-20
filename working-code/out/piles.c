

void main() {
	int pileSize = 10;
	// int myPile[10] = {1, 2, 3}; 
	int myPile[pileSize];
	myPile[0] = 1;
	myPile[1] = 2;
	myPile[2] = 3;
	int* alsoPile = {1, 2, 3};
	int thingFromPile = myPile[3];
	thingFromPile = myPile[0];
	int i = 3;
	thingFromPile = myPile[i];
	myPile[0] = 1000;
	myPile[5] = myPile[0];
	// <incr>
	//         <have nr=i of>myPile</have>
	//     </incr> 
}


