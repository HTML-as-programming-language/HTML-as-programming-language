# HTML-as-programming-language

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

### Visual Studio Code extention
Get live code diagnostics by downloading [HTML-as-programming-language](https://marketplace.visualstudio.com/items?itemName=HTML-as-programming-language.html-as-programming-language) for VSCode.

(This extention requires 'HTML-as-programming-language' itself)

### Language Server
If you wish not to use VSCode but still want live code diagnostics you can use the HTML-language-server.

The language server can be started with the following command:
```
htmlclangsvr
```


### Usage
* Transpile HTML-code to C-code:
    ```
    htmlc my-code.html
    ```
    This wil output C-code to ./out/my-code.c

* Upload to Arduino/AVR microcontrollers:

    wip