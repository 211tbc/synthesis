"""Subclass of MainFrameBase, which is generated by wxFormBuilder."""

import wx
import SynthesisController
from conf import settings
from clsSocketComm import serviceController
import os
import subprocess

# Implementing MainFrameBase
class MainFrame( SynthesisController.MyFrame4 ):
	def __init__( self, parent ):
		SynthesisController.MyFrame4.__init__( self, parent )
		dirsList = ""
		for dirs in settings.INPUTFILES_PATH:
			self.m_listboxDirectories.Append(unicode(dirs))
		
		#self.m_textProcessingFolder.SetValue(unicodeString)
		
		self.sc = serviceController(False)
		# get the status
		self.getStatus()
		

	
	def m_btnStartClick( self, event ):
		#self.m_btPython.Enable(True)
		#self.m_textProcessingFolder.AppendText("scott")
		# issue stop command against synthesis
		#self.m_staticTextStatus.SetLabel("Synthesis is Stopping")
		self.m_statusBar.SetStatusText("Starting Synthesis...Please wait.", 0)
		
		# issue stop command
		self.startService()
		
		self.getStatus()
		
	#def m_btnStopMouseOver(self, event):
	#	tip = self.m_btnStop.ToolTip.GetTip()
	#	print tip
	
	def m_btnStopClick( self, event ):
		#self.m_btPython.Enable(True)
		#self.m_textProcessingFolder.AppendText("scott")
		# issue stop command against synthesis
		#self.m_staticTextStatus.SetLabel("Synthesis is Stopping")
		self.m_statusBar.SetStatusText("Synthesis is Stopping", 0)
		
		# issue stop command
		self.stopService()
	
	def m_btPythonClick( self, event ):
		self.m_rtMain.AppendText(" Python!")
	
	def m_mniOpenClick( self, event ):
		fdlg = wx.FileDialog(self,"Choose a file","Open file",wx.EmptyString,"*.*",wx.FD_OPEN | wx.FD_FILE_MUST_EXIST);
		if fdlg.ShowModal() != wx.ID_OK:
			return;
		self.m_rtMain.LoadFile(fdlg.GetPath())
			
	def m_mniSaveClick( self, event ):
		fdlg = wx.FileDialog(self,"Choose a file","Save file",wx.EmptyString,"*.*",wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT);
		if fdlg.ShowModal() != wx.ID_OK:
			return;
		self.m_rtMain.SaveFile(fdlg.GetPath())
			
	#def m_mniExitClick( self, event ):
	#	self.Close()
	
	#def m_mniAboutClick( self, event ):
	#	wx.MessageBox("oneminutepython template. ","oneminutepython")
	
	def getStatus(self):
		synStatus = self.sc.getStatus("synthesis:status")
		self.m_statusBar.SetStatusText(synStatus, 0)		
	
	def startService(self):
		#os.system("python selector.py")
		#subprocess.Popen()
		print "Starting selector.py in %s...." % os.getcwd()
		pid = subprocess.Popen("python" +  " selector.py", shell=True, cwd=os.getcwd())
		#subprocess.call("python", "selector.py")
		self.getStatus()
	
	def stopService(self):
		import socket
		port = 8081
		host = 'localhost'
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.sendto("synthesis:stop", (host, port))
