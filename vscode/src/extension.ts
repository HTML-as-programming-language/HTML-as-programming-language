'use strict';

import * as vscode from 'vscode';
import {
	LanguageClient,
	LanguageClientOptions,
	ServerOptions,
} from 'vscode-languageclient';
import { ActionTreeProvider } from './action-tree';

let client: LanguageClient;

// this method is called when the extension is activated
export function activate(context: vscode.ExtensionContext) {

    console.log('"html-as-programming-language" is now active!');

    // var config = vscode.workspace.getConfiguration('htmlc');
    
    let disposable = vscode.commands.registerCommand('extension.kikker', () => {
        vscode.window.showInformationMessage('Ik ben een kikker!');
    });

    startLangServer();
    context.subscriptions.concat([
        client.start(),
        disposable
    ]);

    vscode.window.registerTreeDataProvider("htmlc-actions", new ActionTreeProvider());
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
		documentSelector: ["html"]
	}

    client = new LanguageClient("htmlc", serverOptions, clientOptions);
}
