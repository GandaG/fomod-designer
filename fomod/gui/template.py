# -*- coding: utf-8 -*- 

###########################################################################
## Python code generated with wxFormBuilder (version Jun 17 2015)
## http://www.wxformbuilder.org/
##
## PLEASE DO "NOT" EDIT THIS FILE!
###########################################################################

import wx
import wx.xrc

###########################################################################
## Class root
###########################################################################

class root ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FOMOD Designer", pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 229, 229, 229 ) )
		
		bSizer2 = wx.BoxSizer( wx.VERTICAL )
		
		self.title = wx.StaticText( self, wx.ID_ANY, u"FOMOD Designer", wx.DefaultPosition, wx.Size( 200,50 ), 0 )
		self.title.Wrap( -1 )
		self.title.SetFont( wx.Font( 30, 71, 90, 91, False, "Khmer OS System" ) )
		self.title.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		bSizer2.Add( self.title, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.FIXED_MINSIZE|wx.TOP, 15 )
		
		self.version = wx.StaticText( self, wx.ID_ANY, u"Version 0.0.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.version.Wrap( -1 )
		self.version.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 72, 90, 91, False, wx.EmptyString ) )
		self.version.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		bSizer2.Add( self.version, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 20), 0, wx.EXPAND, 5 )
		
		self.new = wx.Button( self, wx.ID_ANY, u"New", wx.Point( -1,-1 ), wx.Size( 150,-1 ), wx.NO_BORDER )
		self.new.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.new.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.new.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		bSizer2.Add( self.new, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 20 )
		
		
		bSizer2.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )
		
		self.open = wx.Button( self, wx.ID_ANY, u"Open", wx.Point( -1,-1 ), wx.Size( 150,-1 ), wx.NO_BORDER|wx.NO_BORDER )
		self.open.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.open.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		bSizer2.Add( self.open, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5 )
		
		
		bSizer2.AddSpacer( ( 0, 10), 0, wx.EXPAND, 5 )
		
		
		self.SetSizer( bSizer2 )
		self.Layout()
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

