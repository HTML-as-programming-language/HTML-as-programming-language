'use strict';

import * as vscode from 'vscode';
import {
	LanguageClient,
	LanguageClientOptions,
	ServerOptions,
} from 'vscode-languageclient';

let client: LanguageClient;

// this method is called when the extension is activated
export function activate(context: vscode.ExtensionContext) {

    // Use the console to output diagnostic information (console.log) and errors (console.error)
    // This line of code will only be executed once when your extension is activated
    console.log('"html-as-programming-language" is now active!');

    var config = vscode.workspace.getConfiguration('htmlc');
    var compilerDir: string = config.get("compilerDir") || "./";
    compilerDir.replace("\\", "/");
    console.log(`compilerDir: ${compilerDir}`);
    var langServer = startLangServer(compilerDir);

    // The command has been defined in the package.json file
    // Now provide the implementation of the command with  registerCommand
    // The commandId parameter must match the command field in package.json
    let disposable = vscode.commands.registerCommand('extension.kikker', () => {
        // The code you place here will be executed every time your command is executed

        // Display a message box to the user
        vscode.window.showInformationMessage('Ik ben een kikker!');
    });

    context.subscriptions.concat([
        client.start(),
        disposable
    ]);

}

// this method is called when the extension is deactivated
export function deactivate() {
    if (client)
        client.stop();
}

function startLangServer(dir: string) {

    const serverOptions: ServerOptions = {
        command: "python",
        args: [dir + (dir.endsWith("/") ? "" : "/") + "lang_server.py"]
	};
	const clientOptions: LanguageClientOptions = {
		documentSelector: ["html", "plaintext"]
	}

    client = new LanguageClient("htmlc", serverOptions, clientOptions);
}