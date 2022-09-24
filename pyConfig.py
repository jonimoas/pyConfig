
from asciimatics.widgets import Frame, Layout, Text, Button, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
from xmltodict import parse, unparse

from dict_deep import deep_set, deep_del
import sys
import os
import yaml
import json
import traceback


filename = ""
textContent = ""
filecontent = None
currentcontent = None
screen = None
frame = None
path = []


class SelectorFrame(Frame):
    global filename
    global textContent
    global path

    def __init__(self, screen):
        super(SelectorFrame, self).__init__(screen,
                                            screen.height * 2 // 3,
                                            screen.width * 2 // 3,
                                            hover_focus=True,
                                            can_scroll=False,
                                            title=filename,
                                            reduce_cpu=True)
        self.layout = Layout([1], fill_frame=True)
        self.add_layout(self.layout)
        self.data = {"text": textContent}

    def addButton(self, content):
        callback = createButtonCallback(content)
        self.layout.add_widget(
            Button(content, callback))

    def addText(self, content):
        self.layout.add_widget(
            Text(path[-2], "text", self.textChange))

    def addLabel(self, content):
        self.layout.add_widget(
            Label(content))

    def addBack(self):
        self.layout.add_widget(
            Button("Back" if len(path) > 0 else "Exit", back))

    def addSave(self):
        self.layout.add_widget(Button("Save", saveChange))

    def textChange(self):
        self.save()

    def addInsert(self):
        self.layout.add_widget(
            Button("Insert", insert))

    def addFieldName(self):
        self.layout.add_widget(
            Text("New Field Name", "text", self.textChange))

    def addFieldButton(self):
        self.layout.add_widget(
            Button("Insert", saveField))

    def addDeleteButton(self):
        self.layout.add_widget(
            Button("Delete", deleteField))


def deleteField():
    global filecontent
    global path
    content = filecontent
    for p in path[:-2]:
        content = content[p]
    if isinstance(content[path[-2]], list):
        print(str(path[-1]))
        print(content[path[-2]])
        print(path[:-2])
        deep_set(filecontent, path[:-1],
                 [x for x in content[path[-2]] if str(x) != str(path[-1])])
    elif isinstance(content, dict):
        deep_del(filecontent, path[:-1])
    saveToFile()
    path.pop()
    back()


def saveField():
    global frame
    if len(path) == 0:
        filecontent[frame.data["text"]] = ""
        path.append(frame.data["text"])
    else:
        path.append(frame.data["text"])
        deep_set(filecontent, path, "")
    createButtonCallback(frame.data["text"])()


def saveToFile():
    global filename
    global filecontent
    with open(filename, 'w') as file:
        if filename.endswith("yml"):
            yaml.dump(filecontent, file)
        elif filename.endswith("json"):
            json.dump(filecontent, file)
        elif filename.endswith("xml"):
            file.write(unparse(filecontent))


def saveChange():
    global frame
    global path
    global filecontent
    global currentcontent
    if isinstance(currentcontent, list):
        currentcontent = [x for x in currentcontent if x != path[-1]]
        currentcontent.append(frame.data["text"])
        deep_set(filecontent, path[:-1], currentcontent)
    else:
        deep_set(filecontent, path[:-1], frame.data["text"])
    saveToFile()
    back()


def back():
    global path
    if len(path) == 0:
        os._exit(0)
    try:
        tag = path[-2]
        path = path[:-2]
        createButtonCallback(tag)()
    except:
        path = []
        loop(filecontent)


def insert():
    global path
    global filecontent
    global currentcontent
    currentcontent = filecontent
    for p in path:
        currentcontent = currentcontent[p]
    if isinstance(currentcontent, list):
        insertValue()
    elif isinstance(currentcontent, dict):
        insertField()


def createButtonCallback(tag):
    def changecurrentcontent():
        global path
        path.append(tag)
        global filecontent
        global currentcontent
        currentcontent = filecontent
        try:
            for p in path:
                currentcontent = currentcontent[p]
            loop(currentcontent)
        except:
            if isinstance(currentcontent, list):
                edit(tag)
            else:
                edit(currentcontent)
    return changecurrentcontent


def main(wrapperScreen):
    global screen
    global filecontent
    global currentcontent
    global filename
    screen = wrapperScreen
    if len(sys.argv) == 1:
        print("No FileName")
        back()
    filename = sys.argv[1]
    try:
        if filename.endswith("yml"):
            with open(filename) as file:
                filecontent = yaml.load(file, Loader=yaml.FullLoader)
        elif filename.endswith("json"):
            with open(filename) as file:
                filecontent = json.loads(file.read())
        elif filename.endswith("xml"):
            with open(filename, encoding='utf-8') as file:
                filecontent = parse(file.read())
        currentcontent = filecontent
        loop(filecontent)
    except Exception as e:
        print("error opening file")
        print(e)
        back()


def loop(content):
    toDraw = []
    try:
        items = content.items()
    except (AttributeError, TypeError):
        if isinstance(content, list):
            for c in content:
                toDraw.append({"label": c})
        else:
            toDraw.append({"label": content})
    else:
        for item in items:
            toDraw.append({"label": item[0]})
    drawButtons(toDraw)


def edit(content):
    drawEdit(content)


def insertValue():
    global path
    path.append("")
    drawEdit("")


def insertField():
    drawInsertField()


def drawButtons(content):
    global screen
    global path
    global frame
    frame = SelectorFrame(screen)
    frame.addLabel(str(">".join(path)))
    for c in content:
        frame.addButton(c["label"])
    if isinstance(currentcontent, list) or isinstance(currentcontent, dict):
        frame.addInsert()
    frame.addBack()
    frame.fix()
    screen.play([Scene([frame], -1)])


def drawEdit(content):
    global screen
    global path
    global textContent
    global frame
    textContent = content
    frame = SelectorFrame(screen)
    frame.addLabel(str(">".join(path)))
    frame.addText(content)
    frame.addDeleteButton()
    frame.addSave()
    frame.addBack()
    frame.fix()
    screen.play([Scene([frame], -1)])


def drawInsertField():
    global frame
    frame = SelectorFrame(screen)
    frame.addLabel(str(">".join(path)))
    frame.addFieldName()
    frame.addFieldButton()
    frame.addBack()
    frame.fix()
    screen.play([Scene([frame], -1)])


while True:
    Screen.wrapper(main)
