
#
#Copyright 2020 Carsten Thiele
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of this software and
#associated documentation files (the "Software"), to deal in the Software without restriction, including
#without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
#sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject
#to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all copies or substantial
#portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT
#LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
#IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
#WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
#SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


import sys

import clr
import CmdBoxHandler
from VoiceEditorSettings import VoiceEditorSettings
from CmdEdit import CmdEdit
from FastButtonAreaHandler import FastButtonAreaHandler
from CmdEditSubstitute import CmdEditSubstitute



clr.AddReference('System.Windows.Forms')
clr.AddReference('System.Drawing')

from System.Drawing import Font, FontStyle
from System.Drawing import Point
from System.Windows.Forms import (Application, Button, Form, ScrollBars, Label,
    TextBox, Keys)
from System.Drawing.Text import InstalledFontCollection

fontCollection = InstalledFontCollection()
fonts = [f for f in fontCollection.Families]


class VoiceEditor(Form):

    def set_focus_on_command_window(self, sender, event):
      self.activeEntryWindow="command"
      self.ActiveControl = self.cmdBox
      self.cmdBox.Text =""

    def set_focus_on_view_window(self, sender, event):
      self.ActiveControl = self.viewBox
      self.viewBox.SelectionLength=0

    def set_focus_on_edit_window(self, sender, event):
      self.activeEntryWindow="edit"
      self.ActiveControl = self.editBox
      self.update_scale()


    def set_focus_on_status_window(self, sender, event):
      self.ActiveControl = self.statusBox

    def __init__(self):

        self.activeEntryWindow="command"

        self.fastButtonList={}
        self.fastTextBoxList={}

        self.Text = "Voice Editor"
        self.EditPanelHpos=950
#        self.EditPanelHpos=10
        self.font_size=10

        self.Width  = 500
        self.Height = 500

        self.setupCmdBox()
        self.setupViewBox()
        self.setupEditBox()
        self.setupStatusBox()
        self.setupScaleBox()

        self.cmdBoxHandler=CmdBoxHandler.CmdBoxHandler\
            (self,self.cmdBox,self.editBox,self.scaleBox,self.viewBox,self.statusBox)

        self.fastButtonAreaHandler=FastButtonAreaHandler(self)

        self.commandButton = Button()
        self.commandButton.Text = 'command'
        self.commandButton.Location = Point(self.EditPanelHpos, 60)
        self.commandButton.Click += self.set_focus_on_command_window

        self.editButton = Button()
        self.editButton.Text = 'edit'
        self.editButton.Location = Point(self.EditPanelHpos,100)
        self.editButton.Click += self.set_focus_on_edit_window

        self.saveButton = Button()
        self.saveButton.Text = 'save'
        self.saveButton.Location = Point(self.EditPanelHpos, 20)
        self.saveButton.Click+=self.set_focus_on_edit_window
        self.saveButton.Click+=self.save_file

        self.viewButton = Button()
        self.viewButton.Text = 'view'
        self.viewButton.Location = Point(self.EditPanelHpos, 240)
        self.viewButton.Click += self.set_focus_on_view_window

        self.filterButton = Button()
        self.filterButton.Text = 'filter'
        self.filterButton.Location = Point(self.EditPanelHpos, 280)
        self.filterButton.Click += self.set_focus_on_command_window
        self.filterButton.Click += self.apply_filter

        self.listButton = Button()
        self.listButton.Text = 'list'
        self.listButton.Location=Point(self.EditPanelHpos+80,20)
        self.listButton.Click += self.set_focus_on_command_window
        self.listButton.Click+=self.list_directory

        self.duplicateButton = Button()
        self.duplicateButton.Text = 'duplicate'
        self.duplicateButton.Location=Point(self.EditPanelHpos, 320)
        self.duplicateButton.Click += self.set_focus_on_command_window
        self.duplicateButton.Click += self.insert_duplicate_template

        self.yankButton = Button()
        self.yankButton.Text = 'yank'
        self.yankButton.Location=Point(self.EditPanelHpos, 360)
        self.yankButton.Click += self.set_focus_on_command_window
        self.yankButton.Click += self.insert_yank_template

        self.insertButton = Button()
        self.insertButton.Text = 'insert'
        self.insertButton.Location=Point(self.EditPanelHpos, 400)
        self.insertButton.Click += self.set_focus_on_command_window
        self.insertButton.Click += self.insert_insert_template

        self.substituteButton = Button()
        self.substituteButton.Text = 'substitute'
        self.substituteButton.Location=Point(self.EditPanelHpos, 440)
        self.substituteButton.Click += self.set_focus_on_command_window
        self.substituteButton.Click += self.insert_substitute_template

        self.recentFilesButton = Button()
        self.recentFilesButton.Text = 'recent files'
        self.recentFilesButton.Location=Point(self.EditPanelHpos, 480)
        self.recentFilesButton.Click += self.set_focus_on_command_window
        self.recentFilesButton.Click+=self.list_recent_files

        self.recentDirectoriesButton = Button()
        self.recentDirectoriesButton.Text = 'recent directories'
        self.recentDirectoriesButton.Location=Point(self.EditPanelHpos, 520)
        self.recentDirectoriesButton.Click += self.set_focus_on_command_window
        self.recentDirectoriesButton.Click+=self.list_recent_directories

        self.favouriteFilesButton = Button()
        self.favouriteFilesButton.Text = 'favourite files'
        self.favouriteFilesButton.Location=Point(self.EditPanelHpos, 560)
        self.favouriteFilesButton.Click += self.set_focus_on_command_window
        self.favouriteFilesButton.Click+=self.list_favourite_files

        self.favouriteDirectoriesButton = Button()
        self.favouriteDirectoriesButton.Text = 'favourite directories'
        self.favouriteDirectoriesButton.Location=Point(self.EditPanelHpos, 600)
        self.favouriteDirectoriesButton.Click += self.set_focus_on_command_window
        self.favouriteDirectoriesButton.Click+=self.list_favourite_directories

        self.expandButton = Button()
        self.expandButton.Text = 'expand'
        self.expandButton.Location=Point(self.EditPanelHpos, 640)
        self.expandButton.Click += self.set_focus_on_edit_window
        self.expandButton.Click+=self.expand_camelback_identifiers

        self.contractButton = Button()
        self.contractButton.Text = 'contract'
        self.contractButton.Location=Point(self.EditPanelHpos, 680)
        self.contractButton.Click += self.set_focus_on_edit_window
        self.contractButton.Click+=self.contract_edit_line

        self.previousButton = Button()
        self.previousButton.Text = 'previous'
        self.previousButton.Location=Point(self.EditPanelHpos, 720)
        self.previousButton.Click += self.set_focus_on_edit_window
        self.previousButton.Click+=self.switch_to_previous_file

        self.variableButton = Button()
        self.variableButton.Text = 'variables'
        self.variableButton.Location=Point(self.EditPanelHpos, 760)
        self.variableButton.Click += self.set_focus_on_edit_window
        self.variableButton.Click+=self.list_variables

        self.templatesButton = Button()
        self.templatesButton.Text = 'templates'
        self.templatesButton.Location=Point(self.EditPanelHpos, 800)
        #self.templatesButton.Click += self.set_focus_on_edit_window
        self.templatesButton.Click+=self.list_templates

        self.markersButton = Button()
        self.markersButton.Text = 'markers'
        self.markersButton.Location=Point(self.EditPanelHpos, 840)
        #self.markersButton.Click += self.set_focus_on_edit_window
        self.markersButton.Click+=self.list_markers

        self.tokenButton = Button()
        self.tokenButton.Text ='tokenise'
        self.tokenButton.Location=Point(self.EditPanelHpos, 880)
        self.tokenButton.Click+=self.list_tokens


        self.label = Label()
        self.label.Text = "Nothing So Far"
        self.label.Location = Point(20, 170)
        self.label.Height = 25
        self.label.Width = 250

        self.Controls.Add(self.cmdBox)
        self.Controls.Add(self.viewBox)
        self.Controls.Add(self.editBox)
        self.Controls.Add(self.statusBox)
        self.Controls.Add(self.scaleBox)
        self.Controls.Add(self.commandButton)
        self.Controls.Add(self.saveButton)
        self.Controls.Add(self.editButton)
        self.Controls.Add(self.viewButton)
        self.Controls.Add(self.listButton)
        self.Controls.Add(self.filterButton)
        self.Controls.Add(self.duplicateButton)
        self.Controls.Add(self.yankButton)
        self.Controls.Add(self.insertButton)
        self.Controls.Add(self.substituteButton)
        self.Controls.Add(self.recentFilesButton)
        self.Controls.Add(self.recentDirectoriesButton)
        self.Controls.Add(self.favouriteFilesButton)
        self.Controls.Add(self.favouriteDirectoriesButton)
        self.Controls.Add(self.expandButton)
        self.Controls.Add(self.contractButton)
        self.Controls.Add(self.previousButton)
        self.Controls.Add(self.variableButton)
        self.Controls.Add(self.templatesButton)
        self.Controls.Add(self.markersButton)
        self.Controls.Add(self.tokenButton)

	#self.ActiveControl = self.cmdBox

    def setupCmdBox(self):
        cmdBox = TextBox()
        cmdBox.Text = "list directory"
        cmdBox.Location = Point(self.EditPanelHpos+80, 60)
        cmdBox.Width = 860
        cmdBox.Height = 100
        #cmdBox.ScrollBars = ScrollBars.Vertical
        cmdBox.AcceptsTab = True
        #cmdBox.AcceptsReturn = True
        #cmdBox.WordWrap = True
        cmdBox.Font = Font("Consolas", 10)
        cmdBox.KeyDown+=self.cmdBoxOnEnter
        cmdBox.MouseWheel+=self.cmdBoxOnMouseWheel
        self.cmdBox = cmdBox

    def setupScaleBox(self):
        scaleBox = TextBox()
        scaleBox.Location = Point(self.EditPanelHpos+80, 140)
        scaleBox.Width = 860
        scaleBox.Height = 40
        scaleBox.ScrollBars = ScrollBars.Vertical
        scaleBox.AcceptsTab = True
        scaleBox.AcceptsReturn = True
        #scaleBox.WordWrap = True
        scaleBox.Font = Font("Consolas", 10)
#        scaleBox.KeyDown+=self.scaleBoxOnEnter
#        scaleBox.MouseWheel+=self.scaleBoxOnMouseWheel
        self.scaleBox = scaleBox
        scaleBox.Multiline = True
#        scaleBox.Maxlines=2
        scaleBox.ReadOnly=True

    def setupEditBox(self):
        editBox = TextBox()
        editBox.Text = ""
        editBox.Location = Point(self.EditPanelHpos+80,100)
        editBox.Width = 860
        editBox.Height = 200
        #editBox.ScrollBars = ScrollBars.Vertical
        editBox.AcceptsTab = True
        #editBox.AcceptsReturn = True
        #editBox.WordWrap = True
        editBox.Font = Font("Consolas", 10)
        editBox.KeyDown+=self.editBoxOnEnter
#        editBox.MouseWheel+=self.editBoxOnMouseWheel
        self.editBox = editBox


    def setupStatusBox(self):
        statusBox = TextBox()
        statusBox.Text = ""
        statusBox.Location = Point(self.EditPanelHpos+80, 220)
        statusBox.Width = 860
        statusBox.Height = 100
        #statusBox.ScrollBars = ScrollBars.Vertical
        statusBox.AcceptsTab = True
        #statusBox.AcceptsReturn = True
        #statusBox.WordWrap = True
	statusBox.Font = Font("Consolas", 10)
        self.statusBox = statusBox
        statusBox.ReadOnly=True


    def setupViewBox(self):
        viewBox = TextBox()
        viewBox.Text = "The Default Text"
        viewBox.Location = Point(self.EditPanelHpos+80, 240)
        viewBox.Width = 860
        viewBox.Height = 800
        viewBox.Multiline = True
        viewBox.ScrollBars = ScrollBars.Vertical
        viewBox.AcceptsTab = True
        viewBox.AcceptsReturn = True
        viewBox.WordWrap = True
	viewBox.Font = Font("Consolas", 10)
        #viewBox.ReadOnly=True
        viewBox.KeyDown+=self.viewBoxOnEnter
        self.viewBox = viewBox

    def editBoxOnEnter(self,sender,e):
        key = e.KeyCode
        modifiers = e.Modifiers
        if key == Keys.Enter:
         self.cmdBoxHandler.processCmd("return")
        if key == Keys.Down:
            self.cmdBoxHandler.processCmd("down")
        if key == Keys.Up:
            self.cmdBoxHandler.processCmd("up")
        if key == Keys.Insert:
            self.cmdBoxHandler.processCmd("insert")
        if key == Keys.F2:
            self.cmdBoxHandler.processCmd("scale letters")
        if key == Keys.F3:
            self.cmdBoxHandler.processCmd("insert line break")
        if key == Keys.F4:
            self.cmdBoxHandler.processCmd("remove line break")
        if key == Keys.F5:
            self.cmdBoxHandler.processCmd("auto menu start sequence")
        if key == Keys.F6:
            self.cmdBoxHandler.processCmd("auto menu wish bone sequences")
        if key == Keys.A and modifiers == Keys.Alt :
            self.cmdBoxHandler.processCmd("auto menu object macro templates")

    def cmdBoxOnMouseWheel(self,sender,e):

        if(e.Delta < 0):
            self.cmdBoxHandler.processCmd("scroll_down")
        else:
            self.cmdBoxHandler.processCmd("scroll_up")
        return

        for scrollRepetition in range(1,VoiceEditorSettings.scrollSpeed):
            if(e.Delta < 0):
                self.cmdBoxHandler.processCmd("down")
            else:
                self.cmdBoxHandler.processCmd("up")

    def cmdBoxOnEnter(self,sender,e):
        key = e.KeyCode
        modifiers = e.Modifiers

        if key == Keys.Enter:
            previousCommand=self.cmdBoxHandler.cmd
            self.cmdBoxHandler.processCmd(self.cmdBox.Text)
            if(
                isinstance(self.cmdBoxHandler.cmd,CmdEdit)
                and isinstance(previousCommand,CmdEdit)
                    ):
                if(self.cmdBox.Text.isdigit()):
                    self.ActiveControl = self.editBox
            if(not isinstance(self.cmdBoxHandler.cmd, CmdEditSubstitute)):
                self.cmdBox.Text=""
        if key == Keys.Escape:
            self.cmdBoxHandler.processCmd("escape command")

        if key == Keys.Up:
            self.cmdBoxHandler.processCmd("up")
        if key == Keys.Down:
            self.cmdBoxHandler.processCmd("down")

        if key == Keys.F5:
            self.cmdBoxHandler.processCmd("auto menu start sequence")
        if key == Keys.F6:
            self.cmdBoxHandler.processCmd("auto menu wish bone sequences")
        if key == Keys.A and modifiers == Keys.Alt :
            self.cmdBoxHandler.processCmd("auto menu object macro templates")

    def viewBoxOnEnter(self,sender,e):
        key = e.KeyCode
#        if key == Keys.Enter:
#         self.cmdBoxHandler.processCmd("return")

#         for oneLine in self.viewBox.Lines :
#          oneLine.rstrip("\r\n")
#          oneLine.rstrip()


    def update_scale(self):
        self.cmdBoxHandler.processCmd("scale words")

    def save_file(self,sender, event):
        self.cmdBoxHandler.processCmd("save file")

    def list_directory(self,sender,e):
        self.cmdBoxHandler.processCmd("list directory")

    def apply_filter(self,sender,e):
        self.cmdBoxHandler.processCmd("toggle filter")

    def insert_duplicate_template(self,sender,e):
        self.cmdBox.Text="duplicate lines [start line]:[end line]"

    def insert_yank_template (self,sender,e):
        self.cmdBox.Text="yank lines [start line]:[end line]"

    def insert_insert_template (self,sender,e):
        self.cmdBox.Text="insert lines [insertion line number]"

    def insert_substitute_template (self,sender,e):
        self.cmdBoxHandler.processCmd("substitute")

    def list_recent_files(self,sender,e):
        self.cmdBoxHandler.processCmd("list recent files")

    def list_recent_directories(self,sender,e):
        self.cmdBoxHandler.processCmd("list recent directories")

    def list_favourite_files(self,sender,e):
        self.cmdBoxHandler.processCmd("list favourite files")

    def list_favourite_directories(self,sender,e):
        self.cmdBoxHandler.processCmd("list favourite directories")

    def expand_camelback_identifiers(self,sender,e):
        self.cmdBoxHandler.processCmd("expand camelback identifiers")

    def contract_edit_line(self,sender,e):
        self.cmdBoxHandler.processCmd("contract edit line")

    def switch_to_previous_file(self,sender,e):
        self.cmdBoxHandler.processCmd("switch to previous file")

    def list_variables(self,sender,e):
        if (self.fileIsBeingEdited()):
            self.set_focus_on_edit_window
            if (self.fileIsPythonFile()):
                self.fastButtonAreaHandler.processCommand("fast button list variables")
            elif (self.fileIsUVMFile()):
                self.fastButtonAreaHandler.processCommand("fast button list UVM variables")
            else:
                self.statusBox.Text="List variables function currently only supports Python and UVM files"
        else:
            self.statusBox.Text="Must be editing a file to list variables"


    def list_templates(self,sender,e):
        self.set_focus_on_edit_window
        self.fastButtonAreaHandler.processCommand("fast button list templates")

    def list_markers(self,sender,e):
        self.fastButtonAreaHandler.processCommand("fast button list markers")

    def list_tokens(self,sender,e):
        self.fastButtonAreaHandler.processCommand("fast button list tokens")

    def zoom_out(self, sender, event):
      if self.font_size>10 :
       self.font_size-=10
      self.textbox.Font = Font("Consolas", self.font_size)
      self.viewBox.Font = Font("Consolas", self.font_size)


    def zoom_in(self, sender, event):
      if self.font_size<60 :
       self.font_size+=10
      self.textbox.Font = Font("Consolas", self.font_size)
      self.viewBox.Font = Font("Consolas", self.font_size)


    def create_fast_button(self,buttonName,buttonHorizontalPosition,buttonVerticalPosition):
        self.fastButtonList[buttonName] = Button()
        self.fastButtonList[buttonName].Text=buttonName
        self.fastButtonList[buttonName].Location=Point(buttonHorizontalPosition,buttonVerticalPosition)
        #self.fastButtonList[buttonName].Click+=self.set_focus_on_edit_window
        self.fastButtonList[buttonName].Click+=self.fast_button_clicked
        self.Controls.Add(self.fastButtonList[buttonName])



    def destroy_fast_button(self,buttonName):
        if (buttonName in self.fastButtonList):
            self.Controls.Remove(self.fastButtonList[buttonName])
        else:
            self.statusBox.Text=" Coding error: no such fast button: %s"%buttonName



    def create_fast_text_box(
     self,textBoxName,textBoxText,boxHorizontalPosition,boxVerticalPosition,boxWidth):
        self.fastTextBoxList[textBoxName] = TextBox()
        self.fastTextBoxList[textBoxName].Text=textBoxText
        self.fastTextBoxList[textBoxName].Location=Point(boxHorizontalPosition,boxVerticalPosition)
        self.fastTextBoxList[textBoxName].Width=boxWidth
        self.fastTextBoxList[textBoxName].Height=VoiceEditorSettings.fastBoxHeight
        #self.fastTextBoxList[textBoxName].ScrollBars = ScrollBars.Vertical
        self.fastTextBoxList[textBoxName].AcceptsTab = True
        #self.fastTextBoxList[textBoxName].AcceptsReturn = True
        #self.fastTextBoxList[textBoxName].WordWrap = True
        self.fastTextBoxList[textBoxName].Font=Font("Consolas",VoiceEditorSettings.fastBoxFontSize)
        self.fastTextBoxList[textBoxName].ReadOnly=True
        self.Controls.Add(self.fastTextBoxList[textBoxName])



    def destroy_fast_box(self,textBoxName):
        if (textBoxName in self.fastTextBoxList):
            self.Controls.Remove(self.fastTextBoxList[textBoxName])
        else:
            self.statusBox.Text=" Coding error: no such fast text box: %s"%textBoxName



    def destroy_fast_buttons_and_boxes(self):

        for box in self.fastTextBoxList:
         self.destroy_fast_box(box)

        for button in self.fastButtonList:
         self.destroy_fast_button(button)



    def fast_button_clicked(self,sender,e):

        self.fastButtonAreaHandler.processCommand(sender.Text)



    def recover_active_window(self):


        if (self.activeEntryWindow=="command"):
                self.ActiveControl = self.cmdBox
        else:
                self.ActiveControl=self.editBox



    def fileIsBeingEdited(self):

        return (isinstance(self.cmdBoxHandler.cmd,CmdEdit))



    def fileIsPythonFile(self):

        if (self.fileIsBeingEdited()):

            if(self.cmdBoxHandler.cmd.fullFileName.endswith(".py")):
                return 1

        return 0



    def fileIsUVMFile(self):

        if (self.fileIsBeingEdited()):

            if(self.cmdBoxHandler.cmd.fullFileName.endswith(".svh")):
                return 1
            if(self.cmdBoxHandler.cmd.fullFileName.endswith(".sv")):
                return 1
            if(self.cmdBoxHandler.cmd.fullFileName.endswith(".v")):
                return 1

        return 0



form = VoiceEditor()
Application.Run(form)
