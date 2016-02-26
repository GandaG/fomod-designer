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
## Class intro
###########################################################################

class intro ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FOMOD Designer", pos = wx.DefaultPosition, size = wx.Size( 500,400 ), style = wx.CAPTION|wx.CLOSE_BOX|wx.MINIMIZE_BOX|wx.SYSTEM_MENU|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		self.SetBackgroundColour( wx.Colour( 229, 229, 229 ) )
		
		layout = wx.BoxSizer( wx.VERTICAL )
		
		self.title = wx.StaticText( self, wx.ID_ANY, u"FOMOD Designer", wx.DefaultPosition, wx.Size( 200,50 ), 0 )
		self.title.Wrap( -1 )
		self.title.SetFont( wx.Font( 30, 71, 90, 91, False, "Khmer OS System" ) )
		self.title.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		layout.Add( self.title, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_TOP|wx.FIXED_MINSIZE|wx.TOP, 15 )
		
		self.version = wx.StaticText( self, wx.ID_ANY, u"Version 0.0.0", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.version.Wrap( -1 )
		self.version.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 72, 90, 91, False, wx.EmptyString ) )
		self.version.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_BTNTEXT ) )
		
		layout.Add( self.version, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		layout.AddSpacer( ( 0, 20), 0, wx.EXPAND, 5 )
		
		self.not_implemented_text = wx.Button( self, wx.ID_ANY, u"New", wx.Point( -1,-1 ), wx.Size( 150,-1 ), wx.NO_BORDER )
		self.not_implemented_text.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.not_implemented_text.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		self.not_implemented_text.SetBackgroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DLIGHT ) )
		
		layout.Add( self.not_implemented_text, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 20 )
		
		
		layout.AddSpacer( ( 0, 3), 0, wx.EXPAND, 5 )
		
		self.open = wx.Button( self, wx.ID_ANY, u"Open", wx.Point( -1,-1 ), wx.Size( 150,-1 ), wx.NO_BORDER|wx.NO_BORDER )
		self.open.SetFont( wx.Font( wx.NORMAL_FONT.GetPointSize(), 70, 90, 90, False, wx.EmptyString ) )
		self.open.SetForegroundColour( wx.SystemSettings.GetColour( wx.SYS_COLOUR_3DDKSHADOW ) )
		
		layout.Add( self.open, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.LEFT|wx.RIGHT, 5 )
		
		
		layout.AddSpacer( ( 0, 18), 0, wx.EXPAND, 5 )
		
		self.recent = wx.StaticText( self, wx.ID_ANY, u"Recent Packages", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.recent.Wrap( -1 )
		self.recent.SetForegroundColour( wx.Colour( 48, 48, 48 ) )
		
		layout.Add( self.recent, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		recent_listChoices = []
		self.recent_list = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.Size( 300,110 ), recent_listChoices, wx.LB_NEEDED_SB )
		layout.Add( self.recent_list, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 5 )
		
		
		self.SetSizer( layout )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.not_implemented_text.Bind( wx.EVT_BUTTON, self.new_package )
		self.open.Bind( wx.EVT_BUTTON, self.open_package )
		self.recent_list.Bind( wx.EVT_LISTBOX_DCLICK, self.open_recent )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def new_package( self, event ):
		event.Skip()
	
	def open_package( self, event ):
		event.Skip()
	
	def open_recent( self, event ):
		event.Skip()
	

###########################################################################
## Class not_implemented
###########################################################################

class not_implemented ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"Not Implemented!", pos = wx.DefaultPosition, size = wx.Size( 370,127 ), style = wx.CAPTION|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		layout = wx.BoxSizer( wx.VERTICAL )
		
		self.m_staticText4 = wx.StaticText( self, wx.ID_ANY, u"Sorry, this part hasn't been implemented yet!", wx.DefaultPosition, wx.DefaultSize, 0 )
		self.m_staticText4.Wrap( -1 )
		layout.Add( self.m_staticText4, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.BOTTOM|wx.TOP, 20 )
		
		self.ok = wx.Button( self, wx.ID_ANY, u"Ok  :'(", wx.DefaultPosition, wx.DefaultSize, 0 )
		layout.Add( self.ok, 0, wx.ALIGN_CENTER_HORIZONTAL|wx.ALL, 10 )
		
		
		self.SetSizer( layout )
		self.Layout()
		
		self.Centre( wx.BOTH )
		
		# Connect Events
		self.ok.Bind( wx.EVT_BUTTON, self.exit_window )
	
	def __del__( self ):
		pass
	
	
	# Virtual event handlers, overide them in your derived class
	def exit_window( self, event ):
		event.Skip()
	

###########################################################################
## Class main
###########################################################################

class main ( wx.Frame ):
	
	def __init__( self, parent ):
		wx.Frame.__init__ ( self, parent, id = wx.ID_ANY, title = u"FOMOD Designer", pos = wx.DefaultPosition, size = wx.Size( 750,483 ), style = wx.DEFAULT_FRAME_STYLE|wx.TAB_TRAVERSAL )
		
		self.SetSizeHintsSz( wx.DefaultSize, wx.DefaultSize )
		
		self.main_statusbar = self.CreateStatusBar( 3, wx.ST_SIZEGRIP, wx.ID_ANY )
		self.main_toolbar = self.CreateToolBar( wx.TB_HORIZONTAL, wx.ID_ANY ) 
		self.new_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"New", wx.Bitmap( u"gui/logos/1456477402_add.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, u"Create a new package.", u"Create a new package.", None ) 
		
		self.open_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Open", wx.Bitmap( u"gui/logos/1456477639_file.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.save_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Save", wx.Bitmap( u"gui/logos/1456477689_disc-floopy.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.saveas_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Save As", wx.Bitmap( u"gui/logos/1456477799_disc-cd.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.main_toolbar.AddSeparator()
		
		self.delete_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Delete", wx.Bitmap( u"gui/logos/1456477717_error.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.refresh_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Refresh", wx.Bitmap( u"gui/logos/1456477730_refresh.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.main_toolbar.AddSeparator()
		
		self.options_item = self.main_toolbar.AddLabelTool( wx.ID_ANY, u"Options", wx.Bitmap( u"gui/logos/1456477700_configuration.png", wx.BITMAP_TYPE_ANY ), wx.NullBitmap, wx.ITEM_NORMAL, wx.EmptyString, wx.EmptyString, None ) 
		
		self.main_toolbar.Realize() 
		
		
		self.Centre( wx.BOTH )
	
	def __del__( self ):
		pass
	

