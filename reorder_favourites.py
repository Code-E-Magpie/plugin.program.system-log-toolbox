# ============================================================
#################################
# reorder_favourites.py by Code-E-Magpie
#################################
# ============================================================

# ============================================================
# File information
# ============================================================

# sourced from: plugin.program.orderfavourites > default.py (1.2.3a by doko-desuka)
# location: plugin.program.reorder-favourites > reorder_favourites.py
# type: system
# functionality: reorder favourites in favourites.xml

# ============================================================
# Import
# ============================================================

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import html, math, os, re, sys

import xml.etree.ElementTree as ET

# ============================================================
# Variables
# ============================================================

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') # id in addons.xml
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_DEVELOPER = ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name') # name in addons.xml
ADDON_VERSION = ADDON.getAddonInfo('version') # version in addons.xml
FAVOURITES = os.path.join(xbmcvfs.translatePath('special://userdata/'), 'favourites.xml') # count
FAVOURITES_FILE = os.path.join('special://userdata/', 'favourites.xml') # processing
FAVOURITES_RESULT = 'ordfav.result'
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
REORDER = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'reorder.png')
TEXT_ADDON = ADDON.getSetting('TEXT_ADDON')
TEXT_DARK = ADDON.getSetting('TEXT_DARK')
TEXT_DIM = ADDON.getSetting('TEXT_DIM')
TEXT_GENERAL = ADDON.getSetting('TEXT_GENERAL')
TEXT_HIGHLIGHT = ADDON.getSetting('TEXT_HIGHLIGHT')
TEXT_ITEM = ADDON.getSetting('TEXT_ITEM')
TEXT_VALUE = ADDON.getSetting('TEXT_VALUE')
THUMBNAILS_FORMAT = 'special://thumbnails/{folder}/{file}'

# ============================================================
# Addon_ID_Version / Addon_Title / Dialogue / Favourites / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ' '.join((ADDON_NAME).strip(' '))))
Dialogue = xbmcgui.Dialog()
Favourites = ('[COLOR %s]favourites > [/COLOR]' % TEXT_GENERAL)
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# FUNCTION: Log
# ============================================================

def Log(msg, level = xbmc.LOGDEBUG):
	xbmc.log(msg, level = level)

# ============================================================
# FUNCTION: TextBox
# ============================================================

ACTION_BACKSPACE = 110 # Backspace
ACTION_MOUSE_LEFT_CLICK = 100 # Mouse click
ACTION_MOUSE_LONG_CLICK = 108 # Mouse long click
ACTION_MOUSE_WHEEL_DOWN = 105 # Mouse wheel down
ACTION_MOUSE_WHEEL_UP = 104 # Mouse wheel up
ACTION_MOVE_DOWN = 4 # Down arrow key
ACTION_MOVE_LEFT = 1 # Left arrow key
ACTION_MOVE_MOUSE = 107 # Down arrow key
ACTION_MOVE_RIGHT = 2 # Right arrow key
ACTION_MOVE_UP = 3 # Up arrow key
ACTION_NAV_BACK = 92 # Backspace action
ACTION_PREVIOUS_MENU = 10 # ESC action
ACTION_SELECT_ITEM = 7 # Number Pad Enter

def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):

		def onAction(self, action):
			if action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()
			elif controlId != self.okbutton:
				self.noop = lambda: None

		def onInit(self): # group = 8000, background = 8100, noop = 8181
			self.title = 8200 # header
			self.msg = 8300 # textbox
			self.scrollbar = 8400 # scrollbar
			self.okbutton = 8500 # close button
			self.noop = lambda: None
			self.showDialog()

		def showDialog(self):
			close = '[COLOR %s]Close[/COLOR]' % TEXT_GENERAL
			self.getControl(self.title).setLabel(title)
			self.getControl(self.okbutton).setLabel(close)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# User Information
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: Development_Information
# ============================================================

MAGPIE_TEXT = '%s[CR][CR]The official repository of %s add-ons.[CR]Distribution of the Magpie Repository is permitted.[CR][CR][COLOR silver]IMPORTANT:[CR]Distribution of %s add-ons are NOT permitted.[CR]%s add-ons are exclusively distributed via the Magpie Repository and / or %s on GitHub.[CR]The code and files of these add-ons are free for use, subject to crediting %s.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.magpie[CR][CR]To install Magpie Repository:[CR]Add the Kodi source https://Code-E-Magpie.github.io/repository.magpie/[CR]Use the \'Install from zip file\' method to install the Magpie Repository.[/COLOR]' % (' '.join('MAGPIE REPOSITORY'), ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, ADDON_DEVELOPER, TEXT_DARK)

DATABASE_TEXT = '[CR][CR][CR]%s[CR][CR]Database Toolbox with easy to use database maintenance tools.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.database-toolbox[/COLOR]' % (' '.join('DATABASE TOOLBOX'), TEXT_DARK)

MAINTENANCE_TEXT = '[CR][CR][CR]%s[CR][CR]Maintenance Toolbox with easy to read Kodi information (system, add-ons, network and internet).[CR]Clear cache + folders, surplus add-ons, temp folder and thumbnails.[CR]View logs and errors (new and old).[CR]Check repositories, sources and internet speed (Speedtest by Ookla).[CR]Backup and restore favourites, sources, logs, userdata, add-ons, add-on data etc.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.maintenance-toolbox[/COLOR]' % (' '.join('MAINTENANCE TOOLBOX'), TEXT_DARK)

REORDER_TEXT = '[CR][CR][CR]%s[CR][CR]Easy to use reordering of favourites for Kodi.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.reorder-favourites[/COLOR]' % (' '.join('REORDER FAVOURITES'), TEXT_DARK)

LOG_TEXT = '[CR][CR][CR]%s[CR][CR]System Log Toolbox easy to use system log viewer.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.system-log-toolbox[/COLOR]' % (' '.join('SYSTEM LOG TOOLBOX'), TEXT_DARK)

SPECIAL_TEXT = '[CR][CR][CR]%s[CR][CR]Special Favourites: Kodi special paths and customised examples.[CR]Special Sources: Kodi special paths (files & folders) and customised examples.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/Code-E-Magpie[/COLOR]' % (' '.join('FAVOURITES & SOURCES'), TEXT_DARK)

TEMPLATE_TEXT = '[CR][CR][CR]%s[CR][CR]Created to illustrate a GitHub repository with a simple folder structure linked to a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.template[/COLOR][CR][CR]Alternatively a GitHub repository linked to a Kodi source, without using a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.simple[/COLOR]' % (' '.join('TEMPLATE REPOSITORY'), TEXT_DARK, TEXT_DARK)

Development_Text = '[CR][CR][CR][COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Magpie Repository / Database Toolbox / Maintenance Toolbox / Reorder Favourites / System Log Toolbox / Favourites & Sources / Template Repository)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('Code-E-Magpie Development'), TEXT_VALUE, TEXT_GENERAL, (MAGPIE_TEXT + DATABASE_TEXT + MAINTENANCE_TEXT + REORDER_TEXT + LOG_TEXT + SPECIAL_TEXT + TEMPLATE_TEXT))

# ============================================================
# FUNCTION: User_Information
# ============================================================

INSTRUCTIONS_TEXT = '%s[CR][CR]Open the add-on to access the menu.[CR]Click on \'User Interface >\' to open the user interface.[CR][CR]Click on the favourite to be moved which will change colour.[CR]Then click on the favourite where it needs to go and it will move.[CR]Multiple changes can be made to different favourites or an individual favourite.[CR]\'Start Again\' can be used to cancel changes made in error without exiting the user interface. Favourites reload in the original order.[CR][CR]Click on the \'Close\' button to exit the user interface (changes pending). Follow the exit and save option dialogue boxes.[CR][CR]Choose from one of the exit options:[CR]Exit Only - no changes saved and exits. Favourites remain in the original order.[CR]Save Changes - save options dialogue box (changes pending).[CR][CR]Choose from one of the save options:[CR]Save + Exit - changes saved and exits the add-on. Exit and restart Kodi for the changes to take effect. Do not make further changes until Kodi is restarted.[CR]Save + Reload - changes saved and exits the add-on. Kodi profile reloads (and changes to favourites). Do not make further changes until the profile reloads.' % ' '.join('INSTRUCTIONS')

NOTES_TEXT = '[CR][CR][CR]%s[CR][CR]Default X image displayed where thumbnail is unavailable.[CR]Up to two lines of fixed text displayed below an image (from start of favourite text).[CR]Up to three lines of scrolling text displayed when the cursor is on an image (from start to end of favourite text).[CR]\'Save + Reload\' may crash Kodi if there is a large number of favourites (i.e. large favourites.xml file). Profile reload automatically runs Kodi startup.' % ' '.join('NOTES')

SETTINGS_TEXT = '[CR][CR][CR]%s[CR][CR]Click on \'Reorder Favourites Settings >\' to open the user settings.[CR]Customise text colours with billions of text colour combinations[CR][CR]Choose from 140 colours for each one (there is also a none option):[CR]TEXT_ADDON = header (menu, logs and text boxes)[CR]TEXT_DARK = menu, logs and text boxes[CR]TEXT_DIM = menu[CR]TEXT_GENERAL = main text (menu, logs, text boxes and buttons)[CR]TEXT_HIGHLIGHT = logs and text boxes[CR]TEXT_ITEM = text boxes[CR]TEXT_VALUE = text boxes[CR][CR]Press the OK button in settings to save any changes made and after resetting a category to default. Restart the add-on to see the changes.' % ' '.join('SETTINGS')

ENVIRONMENT_TEXT = '[CR][CR][CR]%s[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100%% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered using https://aipy.dev/tools where required.' % ' '.join('DEVELOPMENT ENVIRONMENT')

CHANGELOG_TEXT = '[CR][CR][CR]%s [LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes (1.5.0 onwards)[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 3.4.0 (4 menu items & 2 user interface buttons)[CR]- reorder favourites code improved to retrieve more thumbnails[CR][CR]version 2.4.0 (4 menu items & 2 user interface buttons)[CR]- save and exit options removed from menu[CR]- save and exit options added using dialogue boxes[CR][CR]version 1.6.0 (6 menu items & 2 user interface buttons)[CR]- settings created to customise text colours with billions of text colour combinations[CR]- text colour customisation includes text boxes and user interface buttons[CR]- added favourite and interface row count to user interface header[CR]- added dummy button containing full favourite text to user interface[CR]- minor changes to menu text formats to improve consistency with other add-ons[CR]- minor changes to function names to improve consistency with other add-ons[CR]- logs reworked[CR][CR]version 1.5.1 (5 menu items & 2 user interface buttons)[CR]- minor changes to menu text formats to improve consistency with other add-ons[CR][CR]version 1.5.0 (5 menu items & 2 user interface buttons)[CR]- Textbox.xml background image name change[CR]- minor changes to improve consistency with other add-ons[CR][CR]version 1.2.4 (4 menu items for user interface & 2 user interface buttons)[CR]- menu updated with User Information dialogue box (Instructions / Notes / Development / Changelog)[CR]- menu updated with Developer, Name, Version and Addon ID[CR]- user interface ids in xml renumbered[CR]- user interface remote scrolling within borders[CR]- user interface images and layout improved[CR]- variables and functions reworked[CR]- dialogue boxes and logs reworked[CR]- simplified addon.xml content to reduce maintenance[CR][CR]version 1.0.0 (4 menu items for user interface & 2 user interface buttons)[CR]- code from Order Favourites 1.2.3a by doko-desuka (plugin.program.orderfavourites)[CR]- user interface resized to full screen[CR]- improved layout using new images and default image[CR]- visible scrollbar and resized text[CR]- menu and dialogue boxes reworked[CR]- user instructions added to addon.xml[CR]- icon.png changed and fanart.jpg added' % ' '.join('CHANGELOG')

User_Information_Text = '[COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Settings / Development Environment / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('USER INFORMATION'), TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + SETTINGS_TEXT + ENVIRONMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text + Development_Text)

####################################################################################

# ============================================================
# ------------------------------------------------------------
# User Interface
# ------------------------------------------------------------
# ============================================================

# ============================================================
# CLASS: ReorderFavourites
# ============================================================

class ReorderFavourites(xbmcgui.WindowXMLDialog):

# ============================================================
# FUNCTION: __init__
# ============================================================

	# Initialise the class, map control IDs and action IDs to custom handler methods.
	def __init__(self, *args, **kwargs):
		xbmcgui.WindowXMLDialog.__init__(self, *args, **kwargs)

		# Map control IDs to custom handler methods. IDs in /resources/skins/default/1080i/ReorderFavourites.xml
		self.idHandlerDict = {8320: self.doSelect, 8500: self.close, 8501: self.startAgain,}

		# Map action IDs to custom handler methods.
		# See https://github.com/xbmc/xbmc/blob/master/xbmc/input/actions/ActionIDs.h
		self.actionHandlerDict = {
			# All click / select actions are already handled by 'idHandlerDict' above.
			# 7: self.doSelect, # ACTION_SELECT_ITEM
			9: self.doUnselectClose, # ACTION_PARENT_DIR
			10: self.doUnselectClose, # ACTION_PREVIOUS_MENU
			92: self.doUnselectClose, # ACTION_NAV_BACK
			# 100: self.doSelect, # ACTION_MOUSE_LEFT_CLICK
			# 108: self.doSelect, # ACTION_MOUSE_LONG_CLICK
			110: self.doUnselectClose, # ACTION_BACKSPACE
			8320: self.doUnselectClose, # ACTION_MOUSE_RIGHT_CLICK
		}
		self.noop = lambda: None

# ============================================================
# FUNCTION: doCustomModal
# ============================================================

	def doCustomModal(self, favouritesGen):
		allItems = [ ]
		artDict = {'thumb': None}

		for index, data in enumerate(favouritesGen):
			# Every ListItem contains the original favourite (label, thumb and URL).
			# Favourites are written back to the xml file when saving (only the order changes).
			listitem = xbmcgui.ListItem(data[0], path=data[2])
			artDict['thumb'] = data[1] # Slightly faster than recreating a dict on every item.
			listitem.setArt(artDict)
			listitem.setProperty('index', str(index)) # Helps resetting.
			allItems.append(listitem)

		self.allItems = allItems
		self.indexFrom = None # Integer index of the source item (or None when nothing is selected).
		self.isDirty = False # Bool indicating if there are any changes.
		self.doModal()

		return self.makeResult() if self.isDirty else ''

# ============================================================
# FUNCTION: doSelect
# ============================================================

	def doSelect(self):
		selectedPosition = self.panel.getSelectedPosition()
		if self.indexFrom == None:
			# Select a new item to reorder.
			self.indexFrom = selectedPosition
			self.panel.getSelectedItem().setProperty('selected', '1')

		else:
			# Reorder if item already selected.
			if self.indexFrom != selectedPosition:
				# Reorder uses the .pop() and .insert() methods of the 'self.allItems' list.
				itemFrom = self.allItems.pop(self.indexFrom)
				self.allItems.insert(selectedPosition, itemFrom)
				self.isDirty = True

				# Reset the selection state.
				self.indexFrom = None
				itemFrom.setProperty('selected', '')

				# Update the panel by clearing it and reloading all the items.
				self.panel.reset()
				self.panel.addItems(self.allItems)
				self.panel.selectItem(selectedPosition)

			else: # Unselect item if its reselected.
				self.indexFrom = None
				self.panel.getSelectedItem().setProperty('selected', '')

# ============================================================
# FUNCTION: doUnselectClose
# ============================================================

	def doUnselectClose(self):
		# Unselect item if one is selected, otherwise close it.
		if self.indexFrom != None:
			self.allItems[self.indexFrom].setProperty('selected', '')
			self.indexFrom = None

		else:
			self.close()

# ============================================================
# FUNCTION: makeResult
# ============================================================

	def makeResult(self):
		INDENT_STRING = ' ' * 4
		return '<favourites>\n' + '\n'.join((INDENT_STRING + listitem.getPath()) for listitem in self.allItems) + '\n</favourites>\n'

# ============================================================
# FUNCTION: onAction
# ============================================================

	def onAction(self, action):
		self.actionHandlerDict.get(action.getId(), self.noop)()

# ============================================================
# FUNCTION: onClick
# ============================================================

	def onClick(self, controlId):
		self.idHandlerDict.get(controlId, self.noop)()

# ============================================================
# FUNCTION: onInit
# ============================================================

	def onInit(self):

		header = '[B]%s[/B][CR][COLOR %s]Favourites: [COLOR %s]%s  [/COLOR][LIGHT]Rows: [COLOR %s]%s[/COLOR][/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, Count_Favourites(FAVOURITES), TEXT_VALUE, math.ceil(Count_Favourites(FAVOURITES)/5))
		close = '[COLOR %s][B]%s[/B][/COLOR]' % (TEXT_GENERAL, ' '.join('Close'))
		start_again = '[COLOR %s][B]%s[CR][CR]%s[/B][/COLOR]' % (TEXT_GENERAL, ' '.join('Start'), ' '.join('Again'))

		self.title = self.getControl(8200).setLabel(header)
		self.panel = self.getControl(8320)
		self.panel.reset()
		self.panel.addItems(self.allItems)
		self.setFocusId(8310) # Focus on the group containing the panel, not the panel itself.
		self.close = self.getControl(8500).setLabel(close)
		self.startAgain = self.getControl(8501).setLabel(start_again)

# ============================================================
# FUNCTION: startAgain
# ============================================================

	def startAgain(self):

		if Dialogue.yesno(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Start Again)[CR][COLOR %s]Changes will be lost.[CR]Favourites will reload in the original order.[/LIGHT][/COLOR][CR]Start again ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Start Again[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Cancel[/COLOR]' % TEXT_HIGHLIGHT)):

			self.indexFrom = None
			self.allItems = sorted(self.allItems, key = lambda listitem: int(listitem.getProperty('index')))
			self.panel.reset()
			self.panel.addItems(self.allItems)

			Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Start Again[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

#####################################################################################

# ============================================================
# FUNCTION: Count_Favourites
# ============================================================

def Count_Favourites(file_path):

	try:
		with open(file_path, 'r', encoding = 'utf-8') as file:
			content = file.read()
			temp = content.replace('\r', '').replace('\n', '').replace('\t', '')
			count_favourites = len(re.compile(r'<favourite.+?</favourite>').findall(temp))

			return count_favourites

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + Favourites + 'Count Favourites: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except re.error as e:
		Log(Log_Title + Favourites + 'Count Favourites: file content error[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Data_Generator_Favourites
# ============================================================

def Data_Generator_Favourites():

	try:
		file = xbmcvfs.File(FAVOURITES)
		contents = file.read()
		file.close()

	except Exception:
		return 

	try:
		root = ET.fromstring(contents)

	except Exception:
		return

	for favourite in root.findall('.//favourite'):
		name = favourite.get('name') or ''
		name = html.unescape(name)

		thumb_attr = favourite.get('thumb') or ''
		thumb_attr = html.unescape(thumb_attr).strip()

		thumb_result = ''

		if thumb_attr:
			# Some thumb URLs are virtual (plugin://, image://, resource://) translatePath may help for resource:// and file://
			try:
				translated = xbmcvfs.translatePath(thumb_attr)
			except Exception:
				translated = thumb_attr

			# Get cache filename
			try:
				cacheFilename = xbmc.getCacheThumbName(thumb_attr)
			except Exception:
				cacheFilename = ''

			# If getCacheThumbName returns something and not a placeholder, check for the actual file
			if cacheFilename and 'ffffffff' not in cacheFilename:
				# Construct the cache path using Kodi's thumbnails pattern
				# getCacheThumbName returns something like 'a/abcdef012345.tbn'
				# Resolve to Thumbnails folder
				thumbs_path = THUMBNAILS_FORMAT.format(folder=cacheFilename[0], file=cacheFilename)
				thumbs_path = xbmcvfs.translatePath(thumbs_path)

				# Use it if it exist and try common extension replacements (.jpg/.png)
				if xbmcvfs.exists(thumbs_path):
					thumb_result = thumbs_path
				else:
					# try replacing .tbn with common extensions if original url had one
					if thumb_attr.lower().endswith('.jpg'):
						alt = thumbs_path.replace('.tbn', '.jpg', 1)
						if xbmcvfs.exists(alt):
							thumb_result = alt
					elif thumb_attr.lower().endswith('.png'):
						alt = thumbs_path.replace('.tbn', '.png', 1)
						if xbmcvfs.exists(alt):
							thumb_result = alt

				# If the cache file is in a different place, try the raw cache name in Thumbnails root
				if not thumb_result:
					# try special://Thumbnails/<firstchar>/<cacheFilename>
					try_root = xbmcvfs.translatePath('special://Thumbnails/{0}/{1}'.format(cacheFilename[0], cacheFilename))
					if xbmcvfs.exists(try_root):
						thumb_result = try_root

			# If cache file won't map use the translated path if it exists
			if not thumb_result and translated and xbmcvfs.exists(translated):
				thumb_result = translated

			# Fall back to the original thumb_attr if previous doesn't work
			if not thumb_result:
				thumb_result = thumb_attr

		else:
			thumb_result = ''

		yield name, thumb_result, ET.tostring(favourite, encoding='unicode')

# ============================================================
# FUNCTION: Save_Favourites
# ============================================================

def Save_Favourites(xmlText):
	if not xmlText:
		return False

	try:
		file = xbmcvfs.File(FAVOURITES_FILE, 'w')
		file.write(xmlText)
		file.close()

	except Exception as e:
		Log(Log_Title + Favourites + 'Save Favourites: %s' % str(e), xbmc.LOGERROR)

	return True

# ============================================================
# FUNCTION: Window_Property_Clear
# ============================================================

def Window_Property_Clear(prop):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	window.clearProperty(prop)

# ============================================================
# FUNCTION: Window_Property_Get
# ============================================================

def Window_Property_Get(prop):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	return window.getProperty(prop)

# ============================================================
# FUNCTION: Window_Property_Set
# ============================================================

def Window_Property_Set(prop, data):
	window = xbmcgui.Window(xbmcgui.getCurrentWindowId())
	window.setProperty(prop, data)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Exit Options
# ------------------------------------------------------------
# ============================================================

# ============================================================
# FUNCTION: Exit_Only
# ============================================================

def Exit_Only():

	Window_Property_Clear(FAVOURITES_RESULT)
	xbmc.executebuiltin('Action(Back)')
	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Finished (Exit Only)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Reorder_Favourites
# ============================================================

def Reorder_Favourites():

	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Started[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)
	User_Interface = ReorderFavourites('ReorderFavourites.xml', ADDON.getAddonInfo('path'), 'default', '1080i')

	try:
		result = User_Interface.doCustomModal(Data_Generator_Favourites())
		Window_Property_Set(FAVOURITES_RESULT, result)

	except Exception as e:
		Log(Log_Title + Favourites + 'User Interface: %s' % str(e), xbmc.LOGERROR)

		Window_Property_Clear(FAVOURITES_RESULT)

	finally:
		if Dialogue.yesno(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Exit Options)[CR][COLOR %s] > Save Changes: Save Options for pending changes.[CR] > Exit Only: Changes will be lost.[/LIGHT][/COLOR][CR]Save changes ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Save Changes[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Exit Only[/COLOR]' % TEXT_HIGHLIGHT)):

			if Dialogue.yesno(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Save Options)[CR][COLOR %s] > Save + Reload: Changes saved and profile reloads.[CR] > Save + Exit: Changes saved and restart required.[/LIGHT][/COLOR][CR]Save + Reload or Save + Exit ?[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM), yeslabel = ('[COLOR %s]Save + Reload[/COLOR]' % TEXT_VALUE), nolabel = ('[COLOR %s]Save + Exit[/COLOR]' % TEXT_HIGHLIGHT)):
				
				Save_Reload()

			else:
				Save_Exit()

		else:
			Exit_Only()

		del User_Interface

# ============================================================
# FUNCTION: Save_Exit
# ============================================================

def Save_Exit():

	try:
		if Save_Favourites(Window_Property_Get(FAVOURITES_RESULT)):
			Window_Property_Clear(FAVOURITES_RESULT)
			Dialogue.ok(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Save + Exit)[CR][COLOR %s]Changes to favourites saved.[CR]Exit and restart Kodi for the changes to take effect.[/LIGHT][/COLOR][CR]Do not make further changes until Kodi is restarted.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
		xbmc.executebuiltin('Action(Back)')

	except Exception as e:
		Log(Log_Title + Favourites + 'Save + Exit: %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Finished (Save + Exit)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

# ============================================================
# FUNCTION: Save_Reload
# ============================================================

def Save_Reload():

	try:
		if not Save_Favourites(Window_Property_Get(FAVOURITES_RESULT)):
			xbmc.executebuiltin('Action(Back)')

		else:
			Window_Property_Clear(FAVOURITES_RESULT)

			Dialogue.ok(Addon_Title, '[COLOR %s]Reorder Favourites: [LIGHT](Save + Reload)[CR][COLOR %s]Changes to favourites saved.[CR]Current Kodi profile will reload (and changes to favourites).[/LIGHT][/COLOR][CR]Do not make further changes until the profile has reloaded.[/COLOR]' % (TEXT_GENERAL, TEXT_ITEM))
			xbmc.executebuiltin('LoadProfile(%s)' % xbmc.getInfoLabel('System.ProfileName'))

	except Exception as e:
		Log(Log_Title + Favourites + 'Save + Reload: %s' % str(e), xbmc.LOGERROR)

	Log(Log_Title + Favourites + '[COLOR %s][LIGHT]Finished (Save + Reload)[/LIGHT][/COLOR]' % TEXT_DARK, xbmc.LOGINFO)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Entry Point
# ------------------------------------------------------------
# ============================================================

if '/Addon_Header' in PLUGIN_URL:
	ADDON.openSettings()

elif '/User_Interface' in PLUGIN_URL:
	Reorder_Favourites()

elif '/Exit_Menu' in PLUGIN_URL:
	xbmc.executebuiltin('Action(Back)')

elif '/User_Information' in PLUGIN_URL:
	User_Information()

else:
	# Create the menu items.
	xbmcplugin.setContent(PLUGIN_ID, 'files')

	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]%s' % (Addon_Title, ' '.join('  Settings >')))
	Addon_Header.setArt({'fanart': REORDER, 'thumb': ADDON_ICON})

	User_Interface = xbmcgui.ListItem('[B]%s[/B]' % ' '.join('User Interface >'))
	User_Interface.setArt({'fanart': REORDER, 'thumb': ADDON_ICON})

	Exit_Menu = xbmcgui.ListItem(' '.join('Exit Menu >'))
	Exit_Menu.setArt({'fanart': REORDER, 'thumb': ADDON_ICON})

	User_Information = xbmcgui.ListItem(' '.join('User Information >'))
	User_Information.setArt({'fanart': REORDER, 'thumb': ADDON_ICON})

	Addon_Developer = xbmcgui.ListItem('[COLOR %s]Developer: [/COLOR]%s' % (TEXT_DIM, ADDON_DEVELOPER))
	Addon_Developer.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Name = xbmcgui.ListItem('[COLOR %s]Name: %s[/COLOR]' % (TEXT_DIM, ADDON_NAME))
	Addon_Name.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Version = xbmcgui.ListItem('[COLOR %s]Version: %s[/COLOR]' % (TEXT_DIM, ADDON_VERSION))
	Addon_Version.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_ID = xbmcgui.ListItem('[COLOR %s]Add-on ID: %s[/COLOR]' % (TEXT_DIM, ADDON_ID))
	Addon_ID.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	# Append to PLUGIN_URL as it already ends with a slash.
	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addon_Header', Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'User_Interface', User_Interface, False),
			(PLUGIN_URL + 'Exit_Menu', Exit_Menu, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'User_Information', User_Information, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL, Addon_Developer, False),
			(PLUGIN_URL, Addon_Name, False),
			(PLUGIN_URL, Addon_Version, False),
			(PLUGIN_URL, Addon_ID, False)
		)
	)
	xbmcplugin.endOfDirectory(PLUGIN_ID)