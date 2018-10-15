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
    
    vscode.commands.registerCommand('extension.kikker', () => {
        vscode.window.showInformationMessage('Ik ben een kikker!');
    });

    vscode.commands.registerCommand('htmlc.transpile', () => htmlc());

    vscode.commands.registerCommand('htmlc.compile', () => htmlc(["-compile"]));

    vscode.commands.registerCommand('htmlc.upload', () => htmlc(["-upload"]));

    startLangServer();

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
    client.start();
}

function htmlc(args?: string[]) {

    if (!vscode.window.activeTextEditor)
        return vscode.window.showErrorMessage("Please open a HTML file first");

    const terminal = vscode.window.createTerminal(`transpile HTML to C`);
    var fileName = vscode.window.activeTextEditor.document.fileName.split("\\").join("/");
    terminal.sendText(`htmlc ${fileName} ${(args || []).join(" ")}`);
    terminal.show();
}