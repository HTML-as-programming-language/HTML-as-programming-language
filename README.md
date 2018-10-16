# HTML-as-programming-language
[![Build Status](https://travis-ci.com/HTML-as-programming-language/HTML-as-programming-language.svg?branch=master)](https://travis-ci.com/HTML-as-programming-language/HTML-as-programming-language)
We aim to build a programming language that looks like HTML

* [Installation & requirements](#installation-&-requirements)
* [Visual Studio Code extention](#Visual-Studio-Code-extention)
* [Language Server](#Language-Server)
* [Usage](#usage)
* [Write code for Arduino/AVR microcontrollers](#Write-code-for-Arduino/AVR-microcontrollers)

## Installation & requirements

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

## Visual Studio Code extention
Get live code diagnostics by downloading [HTML-as-programming-language](https://marketplace.visualstudio.com/items?itemName=HTML-as-programming-language.html-as-programming-language) for VSCode.

(This extention requires 'HTML-as-programming-language' itself)

## Language Server
If you wish not to use VSCode but still want live code diagnostics you can use the HTML-language-server.

The language server can be started with the following command:
```
htmlclangsvr
```


## Usage
Transpile HTML-code to C-code:
```
htmlc my-code.html
```
This wil output C-code to ./out/my-code.c

If you want to write code for Arduino/AVR read the next section.


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
