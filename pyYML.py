
from asciimatics.widgets import Frame, Layout, Text, Button, Label
from asciimatics.scene import Scene
from asciimatics.screen import Screen
import sys
import os
import yaml
from dict_deep import deep_set

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
            Button("back" if len(path) > 0 else "exit", back))

    def addSave(self):
        self.layout.add_widget(Button("save", saveChange))

    def textChange(self):
        self.save()


def saveChange():
    global path
    global filecontent
    global filename
    global currentcontent
    if isinstance(currentcontent, list):
        currentcontent = [x for x in currentcontent if x != path[-1]]
        currentcontent.append(frame.data["text"])
        deep_set(filecontent, path[:-1], currentcontent)
    else:
        deep_set(filecontent, path[:-1], frame.data["text"])
    with open(filename, 'w') as file:
        yaml.dump(filecontent, file)
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
    if filename.endswith("yml"):
        with open(filename) as file:
            filecontent = yaml.load(file, Loader=yaml.FullLoader)
            currentcontent = filecontent
            loop(filecontent)
    else:
        print("not supported yet")
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


def drawButtons(content):
    global screen
    global path
    global frame
    frame = SelectorFrame(screen)
    frame.addLabel(str(">".join(path)))
    for c in content:
        frame.addButton(c["label"])
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
    frame.addSave()
    frame.addBack()
    frame.fix()
    screen.play([Scene([frame], -1)])


while True:
    Screen.wrapper(main)
