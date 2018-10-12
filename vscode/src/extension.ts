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

    console.log('"html-as-programming-language" is now active!');

    var config = vscode.workspace.getConfiguration('htmlc');
    
    let disposable = vscode.commands.registerCommand('extension.kikker', () => {
        vscode.window.showInformationMessage('Ik ben een kikker!');
    });

    startLangServer();
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

function startLangServer() {

    const serverOptions: ServerOptions = {
        command: "htmlclangsvr"
	};
	const clientOptions: LanguageClientOptions = {
		documentSelector: ["html", "plaintext"]
	}

    client = new LanguageClient("htmlc", serverOptions, clientOptions);
}
