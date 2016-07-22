# -*- coding: utf-8 -*-
"""
gui.py
Small GUI for using the web_explorer python utility.
Copyright (C) 2016  Nicolas Obriot
This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.
This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.
You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
Created on Wed Jul 20 18:50:00 2016
@author: Sabrina Woltmann, Nicolas Obriot
Last modified : 22/07/2016 by Nicolas Obriot
"""

#Starting with imports
import wx #Graphical interface
import sys # For logging events in the window and not terminal
import web_explorer # Our web Explorer class, for exploring the web

#Classes definitions (WX App and Frame for the WebExplorer App)
class explorerApp(wx.App):
    """ New derived App class for the Web Explorer. """
    def __init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True):
        wx.App.__init__(self, redirect=False, filename=None, useBestVisual=False, clearSigInt=True)
        self.myWebExplorer = web_explorer.webExplorer()

    def OnInit(self):
        self.frame = explorerFrame(None, "The Web Explorer 1.0")
        self.frame.Show(True)
        #Redirect the writing output to the log panel (logPanel object needs a "write" function)
        sys.stdout=self.frame.logPanel1
        return True

    def startWebExplore(self):
        """ Function verifying that everything is configured correctly and starts the web explorer. """
        # If there are some website in the list, retrieve them with a for loop
        start_exploring = True #Variable to flag if there is a problem

        # Pick up designated websites from the list
        websites = list (self.frame.websitesPanel1.startSiteList.GetStrings())
        if len(websites) == 0 :
            start_exploring = False
        self.myWebExplorer.set_explore_start_points(websites)

        # Retrieve the working directory
        if self.frame.configurationPanel1.workingDirectory is not None:
            self.myWebExplorer.set_main_directory(self.frame.configurationPanel1.workingDirectory)
            print "Working directory : " + self.frame.configurationPanel1.workingDirectory
        else:
            start_exploring = False

        # Retrieve the depth_level and redirect_count
        self.myWebExplorer.set_redirect_count(self.frame.configurationPanel1.redirect_count)
        self.myWebExplorer.set_exploring_depth(self.frame.configurationPanel1.depth_level)

        #Optional stuffs
        if self.frame.configurationPanel1.verboseCheckBox.IsChecked() :
            self.myWebExplorer.set_verbose(True)
            print "Verbose is active"
        if self.frame.configurationPanel1.debugCheckBox.IsChecked() :
            self.myWebExplorer.set_debug(True)
            print "Debugging is active"

        #Here we go, start the web explorer
        if start_exploring:
            self.myWebExplorer.explore()


class explorerFrame(wx.Frame):
    """ New derived Frame class for the Web Explorer. """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, title=title, size=wx.Size(700, 350))
        #Create a tol level menu : See the explorerMenuBar class for the content
        self.SetMenuBar(self.explorerMenuBar())
        #Create a small status bar at the bottom of the window
        self.CreateStatusBar()
        #Prepare the different objects of the window
        self.websitesPanel1 = websitesPanel(self, size=(250,100))
        self.configurationPanel1 = configurationPanel(self, size=(450,100))
        self.logPanel1 = logPanel(self, size=(700,250))

        #Now the layout of the Window, adding the declared panels :
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.horizontalSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalSizer1.Add(self.websitesPanel1, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, border=5)
        self.horizontalSizer1.Add(self.configurationPanel1, 0, wx.EXPAND | wx.RIGHT | wx.TOP, border=5)
        self.mainSizer.Add(self.horizontalSizer1, 1, wx.EXPAND)
        self.mainSizer.Add(self.logPanel1, 1, wx.EXPAND | wx.ALL, border=5)
        # Main sizer options for the window
        self.SetSizerAndFit(self.mainSizer)
        self.Centre()

        #Finally show the frame(window)
        self.Show(True)

    #Function for setting the Explorer Menu bar
    def explorerMenuBar(self):
        """ Small function containing static setup of the menu bar information"""
        # First, a file menu :
        fileMenu = wx.Menu()
        aboutMenu = fileMenu.Append(wx.ID_ABOUT, "&About","Shows informations about the program")
        helpMenu = fileMenu.Append(wx.ID_HELP, "&Help","Displays help to use the program")
        fileMenu.AppendSeparator()
        exitMenu = fileMenu.Append(wx.ID_EXIT,"&Exit"," Terminate the program")
        #Then that's it for now
        #Add the filemenu to our MenuBar
        menuBar = wx.MenuBar()
        menuBar.Append(fileMenu,"&File") # Adding the "filemenu" to the MenuBar

        #Binding the functions to the menubar
        self.Bind(wx.EVT_MENU, self.aboutAction, aboutMenu)
        self.Bind(wx.EVT_MENU, self.helpAction, helpMenu)
        self.Bind(wx.EVT_MENU, self.exitAction, exitMenu)

        # Done, we return the menuBar Object
        return menuBar

    #function handler when pressing the exit menu in the filemenu
    def exitAction(self,event):
        self.Close(True)  # Close the frame.

    def aboutAction(self,event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, """The WebExplorer utility is open-source software distributed under the terms and conditions of the Free Software Foundation's GNU General Public License. The program can be used for visiting websites and retrieving their text content along with links to other websites.""", "About the Web Explorer", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.

    def helpAction(self,event):
        # A message dialog box with an OK button. wx.OK is a standard ID in wxWidgets.
        dlg = wx.MessageDialog(self, "For help using this software, please visit : https://github.com/nobriot/web_explorer/", "Help", wx.OK)
        dlg.ShowModal() # Show it
        dlg.Destroy() # finally destroy it when finished.


class websitesPanel(wx.Panel):
    """ New derived Panel class for the start website selection. """
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        #We define here how the left panel, used for adding websites is built
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.horizontalSizer = wx.BoxSizer(wx.HORIZONTAL)
        # All the buttons/fields/objects
        self.startSiteListLabel= wx.StaticText(self, -1, "Configure which websites to explore", style=wx.LB_EXTENDED|wx.LB_NEEDED_SB)
        self.addStartSiteTextField= wx.TextCtrl(self, -1, value="",size=(-1,25), style=wx.TE_PROCESS_ENTER)
        self.addStartSiteButton= wx.Button(self, -1, label="Add")
        self.startSiteList= wx.ListBox(self, -1, size=(-1,-1), style=wx.LB_EXTENDED|wx.LB_NEEDED_SB)
        self.removeStartSiteButton= wx.Button(self, -1, label="Remove selected website(s)")
        # The sizers layout
        self.horizontalSizer.Add(self.addStartSiteTextField, 5, wx.FIXED_MINSIZE | wx.ALL, border=3)
        self.horizontalSizer.Add(self.addStartSiteButton, 1, wx.FIXED_MINSIZE | wx.ALIGN_RIGHT | wx.ALL, border=3)

        self.mainSizer.Add(self.startSiteListLabel, 0, wx.ALIGN_CENTRE | wx.FIXED_MINSIZE | wx.ALL, border=5)
        self.mainSizer.Add(self.horizontalSizer, 0, wx.FIXED_MINSIZE, 5)
        self.mainSizer.Add(self.startSiteList, 1, wx.EXPAND | wx.ALL, border=5)
        self.mainSizer.Add(self.removeStartSiteButton, 0, wx.ALIGN_CENTRE | wx.SHAPED | wx.ALL, border=2)

        self.SetSizer(self.mainSizer)
        self.Layout()

        #Bindings between controls and functions
        self.Bind(wx.EVT_BUTTON, self.addStartSiteAction, self.addStartSiteButton)
        self.Bind(wx.EVT_BUTTON, self.removeStartSiteAction, self.removeStartSiteButton)
        self.Bind(wx.EVT_TEXT_ENTER, self.addStartSiteAction, self.addStartSiteTextField)

    # Binding functions / Button handlers
    def addStartSiteAction(self, event):
        #We take the input string and put it in the ListBox
        if len(self.addStartSiteTextField.GetValue())>0:
            self.startSiteList.Append(str(self.addStartSiteTextField.GetValue()),0)
        #We clear the content of the input field
        self.addStartSiteTextField.SetValue("")

    def removeStartSiteAction(self, event):
        # Remove what is selected in the ListBox
        selections = list(self.startSiteList.GetSelections())
        selections.reverse()
        for index in selections:
            self.startSiteList.Delete(index)


class configurationPanel(wx.Panel):
    """ New derived Panel class for the explore configuration. """
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)
        #Variables keps by the panel :
        self.workingDirectory = None
        self.depth_level = 1
        self.redirect_count = 1

        #We define here how the left panel, used for adding websites is built
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)
        self.horizontalSizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.horizontalSizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.verticalSizer21 = wx.BoxSizer(wx.VERTICAL) #Number at the end means it is the first which belong to hSizer1
        self.verticalSizer22 = wx.BoxSizer(wx.VERTICAL)
        self.horizontalSizer211 = wx.BoxSizer(wx.HORIZONTAL) #Number at the end means it is the first which belong to vSizer21
        self.horizontalSizer212 = wx.BoxSizer(wx.HORIZONTAL)

        # All the buttons/fields/objects
        self.welcomeText = wx.StaticText(self,-1, label="Configure the Web Explorer functionalities and click on 'Start Exploring'")
        self.workingDirectoryLabel = wx.StaticText(self, -1, "Please select a working directory:")
        self.selectWorkingDirectoryButton = wx.Button(self, -1, "Select")
        self.selectWorkingDirectoryLabel = wx.StaticText(self, -1, "None selected")
        self.webLevelSettingLabel = wx.StaticText(self, -1, "Depth level : ")
        self.webLevelSettingBox = wx.SpinCtrl(self, value="1", id=wx.ID_ANY, size=(50,25), min=1, max=10, style=wx.SP_ARROW_KEYS)
        self.redirectSettingLabel = wx.StaticText(self, -1, "Redirections count : ")
        self.redirectSettingBox = wx.SpinCtrl(self, value="1", id=wx.ID_ANY, size=(50,25), min=0, max=200, style=wx.SP_ARROW_KEYS)
        self.verboseCheckBox =  wx.CheckBox(self, -1, label="Verbose mode")
        self.debugCheckBox =  wx.CheckBox(self, -1, label="Debugging mode")
        self.startButton= wx.Button(self, -1, label="Start Exploring")

        # The sizers layout
        self.horizontalSizer1.Add(self.selectWorkingDirectoryButton, 0, wx.FIXED_MINSIZE | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)
        self.horizontalSizer1.Add(self.selectWorkingDirectoryLabel, 0, wx.EXPAND | wx.ALIGN_CENTER_VERTICAL | wx.ALL, border=2)

        self.horizontalSizer211.Add(self.webLevelSettingLabel, 3, wx.ALIGN_LEFT | wx.ALL, border=5)
        self.horizontalSizer211.Add(self.webLevelSettingBox, 1, wx.FIXED_MINSIZE | wx.ALIGN_RIGHT | wx.ALL, border=2)
        self.horizontalSizer212.Add(self.redirectSettingLabel, 3, wx.ALIGN_LEFT | wx.ALL, border=5)
        self.horizontalSizer212.Add(self.redirectSettingBox, 1, wx.FIXED_MINSIZE | wx.ALIGN_RIGHT | wx.ALL, border=2)
        self.verticalSizer21.AddSpacer(5)
        self.verticalSizer21.Add(self.horizontalSizer211, 0, wx.EXPAND | wx.ALL, border=2)
        self.verticalSizer21.Add(self.horizontalSizer212, 0, wx.EXPAND | wx.ALL, border=2)

        self.verticalSizer22 = wx.StaticBoxSizer(wx.StaticBox(self,-1, "Options"), wx.VERTICAL)
        self.verticalSizer22.Add(self.verboseCheckBox, 5, wx.FIXED_MINSIZE | wx.ALL, border=5)
        self.verticalSizer22.Add(self.debugCheckBox, 5, wx.FIXED_MINSIZE | wx.ALL, border=5)

        self.horizontalSizer2.Add(self.verticalSizer21, 1, wx.FIXED_MINSIZE | wx.ALL, border=5)
        self.horizontalSizer2.Add(self.verticalSizer22, 1, wx.FIXED_MINSIZE | wx.ALL, border=5)

        # Put our sizers in the main one
        self.mainSizer.Add(self.welcomeText, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.FIXED_MINSIZE | wx.ALL, border=5)
        self.mainSizer.AddSpacer(15)
        self.mainSizer.Add(self.workingDirectoryLabel, 0, wx.ALIGN_LEFT | wx.ALL, border=2)
        self.mainSizer.Add(self.horizontalSizer1, 1, wx.FIXED_MINSIZE, border=2)
        self.mainSizer.AddSpacer(15)
        self.mainSizer.Add(self.horizontalSizer2, 4, wx.SHAPED, border=2)
        self.mainSizer.Add(self.startButton, 0, wx.ALIGN_BOTTOM | wx.ALIGN_RIGHT | wx.FIXED_MINSIZE | wx.ALL, border=5)

        self.SetSizer(self.mainSizer)
        self.Layout()

        # Bindings between controls and functions
        self.Bind(wx.EVT_BUTTON, self.selectWorkingDirectoryAction, self.selectWorkingDirectoryButton)
        self.Bind(wx.EVT_SPINCTRL, self.setRedirectCountAction, self.redirectSettingBox)
        self.Bind(wx.EVT_SPINCTRL, self.setWebLevelCountAction, self.webLevelSettingBox)
        self.Bind(wx.EVT_BUTTON, self.startExploreAction, self.startButton)

    # Binding functions / Button handlers
    def selectWorkingDirectoryAction(self,event):
        ''' Binding function when the user picks a directory. '''
        #We make a directory dialog :
        dlg = wx.DirDialog(self, message="Select the working directory", style=wx.DD_DIR_MUST_EXIST)
        if dlg.ShowModal() == wx.ID_OK: #Show the dialog and fetch back the directory
            self.workingDirectory = dlg.GetPath()
            if len(dlg.GetPath()) > 50 : #If it is too long we insert some line returns every 50 char
                text = ""
                i= 0
                while i < len(dlg.GetPath()):
                    text += dlg.GetPath()[i:i+50] + "\n"
                    i+=50
                text += dlg.GetPath()[i:]
                self.selectWorkingDirectoryLabel.SetLabel(text)
            else:
                self.selectWorkingDirectoryLabel.SetLabel(dlg.GetPath())
            #self.Layout()
        dlg.Destroy() # finally destroy it when finished.

    def setRedirectCountAction(self,event):
        # Value has been changed, so we update the class variable
        self.redirect_count = self.redirectSettingBox.GetValue()

    def setWebLevelCountAction(self,event):
        # Value has been changed, so we update the class variable
        self.depth_level = self.webLevelSettingBox.GetValue()

    # Event handling functions
    def startExploreAction(self, event):
        # Call the app function which handles the web exploring
        app.startWebExplore()

class logPanel(wx.Panel):
    """ New derived Panel class for the event logging panel. """
    def __init__(self, *args, **kwds):
        wx.Panel.__init__(self, *args, **kwds)

        #We define here how the left panel, used for adding websites is built
        self.mainSizer = wx.BoxSizer(wx.VERTICAL)

        # All the buttons/fields/objects
        self.executionTextTitle = wx.StaticText(self,-1, "Execution log",style=wx.ALIGN_LEFT)
        self.executionText = wx.TextCtrl(self,-1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)

        # The sizers layout
        self.mainSizer.Add(self.executionTextTitle, 0, wx.ALIGN_LEFT | wx.ALL, border=2)
        self.mainSizer.Add(self.executionText, 1,  wx.EXPAND | wx.ALL, border=2)

        self.SetSizer(self.mainSizer)
        self.Layout()

    def write(self,message):
        self.executionText.AppendText(message)


if __name__ == '__main__':
    app = explorerApp(0) #Use 0 for stdio trace in terminal and no argument for stdio redirected to the app
    app.MainLoop()
