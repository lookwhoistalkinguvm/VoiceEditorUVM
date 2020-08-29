# VoiceEditorUVM

VoiceEditor for UVM

## INSTALLATION

0) Demo video at : 
https://youtu.be/yHlBrfDe0wI 

1) Install IronPython
https://ironpython.net/download/

2) Download latest VoiceEditorUVM release and unpack.

Define user env variable that points to installation directory eg :

VOICEEDITORROOT = C:\%HOMEPATH%\Projects\VoiceEditorUVM

3) Set/add the following environment variables :
IRONPYTHONPATH += %VOICEEDITORROOT%\src
IRONPYTHONPATH += %VOICEEDITORROOT%\src_uvm

4) cd %VOICEEDITORROOT%\run
   Run create_snapshot BAT script : run_create_snapshot.bat

5) In the same directory as 4), invoke the editor : run.bat


## USAGE ALL MODES


-- Command Box

To place the cursor into this box press the button labelled "command".

Similar to VI's command mode. All commands are issued by typing them into this box and pressing return.

Entering a number into this box and pressing return causes the editor to jump to that line number.

When the cursor is placed in this box the mouse wheel can be used to scroll up and down in the file. Furthermore, the up arrow key will cause the editor to scroll up and down key will cause it to scroll down.


–- Edit Box

To place the cursor into this box press the button labelled "edit".

The up arrow key will cause the editor to scroll up and the down arrow key will cause it to scroll down.

This box is the only means of editing the file. The view box only displays the file content. Once an edit has been performed inside the edit box it can be committed into the flow of text by pressing the insert button or by pressing return. However, pressing return will also insert a new line.

When scrolling above the start of the file new lines will automatically be added. It is not possible to scroll beyond the end of the file. To add lines to the end of the file you have to press return when at the ultimate line.


-- Various Buttons down the middle of the editor GUI.

Clicking the list button will list the current working directory and puts the editor into filesystem mode. Available options are listed in the view box and can be selected by entering their corresponding choice number in the command box and pressing return. Moving or copying is a two-stage process. After having selected the move or duplicate choice number you will need to specify the list of files to perform the operation on by entering comma separated list of choice numbers for nonconsecutive choices, and/or pairs of choice numbers separated by a colon to specify ranges (eg: 1,3,10:12). Then you need to navigate to the target directory and select choice number 6 (insert). At that point a Python script and associated .bat file will be created that you will need to explicitly run in order for the operation to be actually carried out. The file to run is: %VOICEEDTORROOT%\run\run_duplicate_move_delete.bat. When using the editor invoice control mode voice shortcut for running the script is 'run file operation'.


Lines can be cut from the flow of text by clicking the yank button. Yanked lines are stored in a buffer and can be reinserted by clicking the insert button.

The substitute button allows the substitution of one text by another in a defined range of lines. If the range of lines is left at the default settings then the substitution will be performed on the entire file. Simply follow the instructions in the command box.

The 'contract' button deflates the line entered into the edit box by removing all unnecessary white spaces. This makes it easier to enter code by voice given that Dragon NaturallySpeaking likes to insert spaces where they don't belong when you are trying to dictate variables and other code. Pressing the contract button also causes the line in the edit box to be committed into the text flow.

The expand button does the opposite of the contract button.

The filter button can be used to invoke the function that allows the lines in the file to be filtered (in a grep like manner). When clicking on this button you will be prompted to enter a regular expression in the command box. Enter return for the filtering to be actioned. Changing the regular expression in the command box and pressing return results in filtering on the newly entered expression. Entering an integer number is interpreted as a line number and causes the view box display to jump to the given line number. Clicking the filter button the second time causes an exit from the function. 

The template button gives access to the library of templates defined in the %VOICEEDITORROOT%\templates directory.

The templates\09_tb.template template file is earmarked for containing a particular test environments IntelliSense information. The templates\09_tb.template file that comes as part of this release is specific to the www.github.com/lookwhoistalkinguvm/symbol_gen_demo project. The contents of this file needs to be generated dynamically using a script for each specific project. Such a script is not part of the release.


## USAGE MANUAL MODE

VoiceEditor was conceived as a voice controllable editor. To place the cursor into the command, edit or view boxe click on the corresponding button named command, edit or view. Otherwise the application won't know where the cursor has been placed. This is not an issue when using it in voice control mode because navigation from box to box happens by saying 'click box_name'.


## TIP

If the editor appears to be stuck for any reason first try clicking the list button and if that doesn't work the filter button.

## Useful Commands (command box)

comment out lines start_line:end_line
comment in lines start_line:end_line

Use filter functions to grep for lines matching a particular pattern (such as debug print statements) and then issue the following command:
remove lines





   
