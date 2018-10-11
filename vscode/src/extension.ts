'use strict';

import * as vscode from 'vscode';

// this method is called when the extension is activated
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('Congratulations, your extension "html-as-programming-language" is now active!');

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with  registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('extension.kikker', () => {
        // The code you place here will be executed every time your command is executed

        // Display a message box to the user
        vscode.window.showInformationMessage('Ik ben een kikker!');
    });

    context.subscriptions.push(disposable);
}

// this method is called when the extension is deactivated
export function deactivate() {
}