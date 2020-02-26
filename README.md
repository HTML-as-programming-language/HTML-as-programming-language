# Hyper Text MACHINE Language
### HTML-as-programming-language
[![Build Status](https://travis-ci.com/HTML-as-programming-language/HTML-as-programming-language.svg?branch=master)](https://travis-ci.com/HTML-as-programming-language/HTML-as-programming-language)
We aim to build a programming language that looks like HTML. The current syntax is HTML-inspired / XML-based but we hope it to be fully 100% HTML-based in the future.

* [Examples](#examples)
* [Installation & requirements](#installation--requirements)
* [Visual Studio Code extention](#Visual-Studio-Code-extention)
* [Language Server](#Language-Server)
* [Usage](#usage)
* [Write code for Arduino/AVR microcontrollers](#Write-code-for-Arduino/AVR-microcontrollers)

<br/>

# Examples
## [Functions](https://github.com/HTML-as-programming-language/HTML-as-programming-language/wiki/Variables-and-Constants)
```html
<def multiplyFunction returns=int> <!-- You can create functions -->
    <param a type=int/>
    <param b type=int/>

    <return>a * b</return>
</def>

<def main>
    <var result type=int> <!-- Create variables -->
        <multiplyFunction> <!-- and store the result of the function in the variable -->
            <param>5</param>
            <param>6</param>
        </multiplyFunction>
    </var>
</def>
```

## [If/Else](https://github.com/HTML-as-programming-language/HTML-as-programming-language/wiki/expressions%2C-if-else)
```html
<!-- starting expression with condition -->
<expression x="a > 1">
	<!-- if a > 1 -->
	<ya-really>
		<!-- printf "a is greater than one (1) -->
		<printf>
			"a is greater than one (1)"
		</printf>
	</ya-really>

	<!-- else if a == 0 -->
	<maybe x="a == 0">
		<printf>
			"a is equal zero (0)"
		</printf>
	</maybe>

	<!-- else -->
	<no-wai>
		<printf>
			"a is minor than zero (0)"
		</printf>
	</no-wai>
</expression>
```

## [Math](https://github.com/HTML-as-programming-language/HTML-as-programming-language/wiki/Assignments)
```html
<def main>
    <var myInt=6/> <!-- Create variables -->
    <assign myInt=10/> <!-- reassign variables -->
    <multiply myInt>myInt</multiply> <!-- * -->
    <divide myInt>3</divide> <!-- / -->
    <minus myInt>10</minus> <!-- - -->
    <add myInt>2</add> <!-- + -->
    <modulo myInt>myInt</modulo> <!-- % the remainder when divided -->
</def>
```

## [Arrays](https://github.com/HTML-as-programming-language/HTML-as-programming-language/wiki/Piles-%28arrays%29)
```html
<pile myVeryCoolPile type="boolean">  <!-- Array of booleans -->
    <thing>cake</thing> <!-- True -->
    <thing>lie</thing> <!-- False -->
    <thing>cake</thing>
    <thing>lie</thing>
    <thing>cake</thing>
    <thing>lie</thing>
    <thing>lie</thing>
    <thing>cake</thing>
    <thing>lie</thing>
</pile>
```

## And many more on the wiki
https://github.com/HTML-as-programming-language/HTML-as-programming-language/wiki

<br/>

# Installation & requirements

### Requirements
* Python 3 (tested with Python 3.7)

   To compile and upload to Arduino/AVR microcontrollers:

* avr-gcc
* avrdude


### Installation
PyPi package ([project page](https://pypi.org/project/HTML-as-programming-language/)):
```
pip install HTML-as-programming-language
```

# Visual Studio Code extention
Get live code diagnostics by downloading [HTML-as-programming-language](https://marketplace.visualstudio.com/items?itemName=HTML-as-programming-language.html-as-programming-language) for VSCode.

(This extention requires 'HTML-as-programming-language' itself)

# Language Server
If you do not wish to use VSCode but still want live code diagnostics you can use the HTML-language-server.

The language server can be started with the following command:
```
htmlclangsvr
```


# Usage
Transpile HTML-code to C-code:
```
htmlc my-code.html
```
This wil output C-code to ./out/my-code.c

If you want to write code for Arduino/AVR, read the next section.


## Write code for Arduino/AVR microcontrollers:

To write code for Adruino/AVR microcontrollers, (Arduino UNO for example) you need to put a DOCTYPE tag in your HTML file.

For example:
```HTML
<!DOCTYPE avr/atmega328p>
```
Simply type 'avr/' followed by the microcontroller name.
(atmega328p is the name of the microcontroller used by Arduino UNO)

### Compile
To compile your AVR/Arduino code:
```
htmlc my-code.html -compile
```

### Upload to Arduino/Microcontroller
To upload your code to an arduino or other AVR microcontroller:
```
htmlc my-code.html -upload
```
