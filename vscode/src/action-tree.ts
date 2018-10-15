import * as vscode from 'vscode';

export class ActionTreeProvider implements vscode.TreeDataProvider<Action> {

    getTreeItem(element: Action): vscode.TreeItem {
		return element;
    }
    
    getChildren(element: Action): Thenable<Action[]> {
        if (element)
            return Promise.resolve([]);
        
        return Promise.resolve([
            new Action("hoi", "doei!"),
            new Action("haha", "blabla!")
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