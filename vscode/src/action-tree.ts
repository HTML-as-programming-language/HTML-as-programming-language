import * as vscode from 'vscode';

export class ActionTreeProvider implements vscode.TreeDataProvider<Action> {

    getTreeItem(element: Action): vscode.TreeItem {
        return element;
    }

    getChildren(element: Action): Thenable<Action[]> {
        if (element)
            return Promise.resolve([]);

        return Promise.resolve([
            new Action(
                `Transpile HTML to C`, 
                `This action will transpile your HTML-code to a C-code file.`,
                {
                    command: "htmlc.transpile",
                    title: ""
                }
            ),

            new Action(
                `Compile`,
                `This action will transpile your HTML-code to a C-code file and then compile that C-code.\n
                You file should contain a <!DOCTYPE ...> tag to specify what compiler to use.\n
                \n
                To use the AVR-GCC compiler the doctype tag should look like this:\n
                <!DOCTYPE avr/*micro-controller-name-here*)>\n
                \n
                For example if you want to compile for Arduino UNO:\n
                <!DOCTYPE avr/atmega328p>`,
                {
                    command: "htmlc.compile",
                    title: ""
                }
            ),

            new Action(
                `Compile & upload`,
                `This action will do the same as the action above,\n
                but it will also upload the compiled hex-code to your AVR-microcontroller`,
                {
                    command: "htmlc.upload",
                    title: ""
                }
            ),
        ]);
    }

}

class Action extends vscode.TreeItem {

    constructor(
        public label: string,
        public tooltipText: string,
        public command?: vscode.Command
    ) {
        super(label);
    }

    get tooltip(): string {
        return this.tooltipText
    }

}