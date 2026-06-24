# ============================================================
#################################
# system_log_toolbox.py by Code-E-Magpie
#################################
# ============================================================

# ============================================================
# File information
# ============================================================

# sourced from: plugin.program.database-toolbox > database_toolbox.py
# location: plugin.program.system-log-toolbox > system_log_toolbox.py
# type: system
# functionality: log toolbox

# ============================================================
# Import
# ============================================================

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, xbmcvfs
import os, re

# ============================================================
# Variables
# ============================================================

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id') # id in addons.xml
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_DEVELOPER = ADDON.getAddonInfo('author') # provider-name in addons.xml (developer)
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name') # name in addons.xml
ADDON_TITLE = (' '.join((ADDON_NAME).strip(' '))) # insert spaces between + remove leading & trailing
ADDON_VERSION = ADDON.getAddonInfo('version') # version in addons.xml
HOME = xbmcvfs.translatePath('special://home/')
LOGPATH = xbmcvfs.translatePath('special://logpath/')
LOG_NEW = os.path.join(LOGPATH, 'kodi.log')
LOG_OLD = os.path.join(LOGPATH, 'kodi.old.log')
NOTIFICATION_DURATION = ADDON.getSetting('NOTIFICATION_DURATION')
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
TEMP = xbmcvfs.translatePath('special://temp/')
TEXT_ADDON = ADDON.getSetting('TEXT_ADDON')
TEXT_DARK = ADDON.getSetting('TEXT_DARK')
TEXT_DIM = ADDON.getSetting('TEXT_DIM')
TEXT_GENERAL = ADDON.getSetting('TEXT_GENERAL')
TEXT_HIGHLIGHT = ADDON.getSetting('TEXT_HIGHLIGHT')
TEXT_ITEM = ADDON.getSetting('TEXT_ITEM')
TEXT_VALUE = ADDON.getSetting('TEXT_VALUE')
TOOLBOX = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'toolbox.png')
VIEW_LOG_LIMIT = int(ADDON.getSetting('VIEW_LOG_LIMIT'))

# ============================================================
# Addon_ID_Version / Addon_Title / Dialogue / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ADDON_TITLE))
Dialogue = xbmcgui.Dialog()
Log_Title = ('[COLOR %s]%s [/COLOR]' % (TEXT_ADDON, ADDON_NAME))

# ============================================================
# System / System_Errors
# ============================================================

System = ('[COLOR %s]log > [/COLOR]' % TEXT_GENERAL)
System_Errors = ('[COLOR %s]log errors > [/COLOR]' % TEXT_GENERAL)

# ============================================================
# FUNCTION: Log
# ============================================================

def Log(msg, level = xbmc.LOGDEBUG):
	xbmc.log(msg, level = level)

# ============================================================
# FUNCTION: Notification
# ============================================================

def Notification(title, message, times = NOTIFICATION_DURATION, icon = ADDON_ICON, sound = False):
	Dialogue.notification(title, message, icon, int(times), sound)

#####################################################################################

# ============================================================
# ------------------------------------------------------------
# Information
# ------------------------------------------------------------
# ============================================================

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
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

# ============================================================
# FUNCTION: Development_Information
# ============================================================

MAGPIE_TEXT = 'M A G P I E   R E P O S I T O R Y[CR][CR]The official repository of [COLOR silver]C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e[/COLOR] add-ons.[CR]Distribution of the Magpie Repository is permitted.[CR][CR][COLOR silver]IMPORTANT:[CR]Distribution of C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e add-ons are NOT permitted.[CR]C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e add-ons are exclusively distributed via the Magpie Repository and / or [COLOR silver]C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e[/COLOR] on GitHub.[CR]The code and files of these add-ons are free for use, subject to crediting C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e.[/COLOR][CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.magpie[CR][CR]To install Magpie Repository:[CR]Add the Kodi source https://Code-E-Magpie.github.io/repository.magpie/[CR]Use the \'Install from zip file\' method to install the Magpie Repository.[/COLOR]' % TEXT_DARK

DATABASE_TEXT = '[CR][CR][CR]D A T A B A S E   T O O L B O X[CR][CR]Database Toolbox with easy to use database maintenance tools.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.database-toolbox[/COLOR]' % TEXT_DARK

MAINTENANCE_TEXT = '[CR][CR][CR]M A I N T E N A N C E   T O O L B O X[CR][CR]Maintenance Toolbox with easy to read Kodi information (system, add-ons, network and internet).[CR]Clear cache + folders, surplus add-ons, temp folder and thumbnails.[CR]View logs and errors (new and old).[CR]Check repositories, sources and internet speed (Speedtest by Ookla).[CR]Backup and restore favourites, sources, logs, userdata, add-ons, add-on data etc.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.maintenance-toolbox[/COLOR]' % TEXT_DARK

REORDER_TEXT = '[CR][CR][CR]R E O R D E R   F A V O U R I T E S[CR][CR]Easy to use reordering of favourites for Kodi.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.reorder-favourites[/COLOR]' % TEXT_DARK

LOG_TEXT = '[CR][CR][CR]S Y S T E M   L O G   T O O L B O X[CR][CR]System Log Toolbox easy to use system log viewer.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.system-log-toolbox[/COLOR]' % TEXT_DARK

SPECIAL_TEXT = '[CR][CR][CR]F A V O U R I T E S   &   S O U R C E S[CR][CR]Special Favourites: Kodi special paths and customised examples.[CR]Special Sources: Kodi special paths (files & folders) and customised examples.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/Code-E-Magpie[/COLOR]' % TEXT_DARK

TEMPLATE_TEXT = '[CR][CR][CR]T E M P L A T E   R E P O S I T O R Y[CR][CR]Created to illustrate a GitHub repository with a simple folder structure linked to a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.template[/COLOR][CR][CR]Alternatively a GitHub repository linked to a Kodi source, without using a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.simple[/COLOR]' % (TEXT_DARK, TEXT_DARK)

Development_Information_Text = '[CR][CR][CR][COLOR %s][B]C o d e - E - M a g p i e   D e v e l o p m e n t[/B][CR][COLOR %s][LIGHT](Magpie Repository / Database Toolbox / Maintenance Toolbox / Reorder Favourites / System Log Toolbox / Favourites & Sources / Template Repository)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, TEXT_VALUE, TEXT_GENERAL, (MAGPIE_TEXT + DATABASE_TEXT + MAINTENANCE_TEXT + REORDER_TEXT + LOG_TEXT + SPECIAL_TEXT + TEMPLATE_TEXT))

# ============================================================
# FUNCTION: User_Information
# ============================================================

INSTRUCTIONS_TEXT = 'I N S T R U C T I O N S[CR][CR]Open the add-on to access the menu.[CR]Select one of the \'>\' menu items.[CR][CR]\'System Log Toolbox Settings >\' user settings:[CR]• set notification duration[CR]• logs highlight if count exceeds number set (used to identify the exsistance of an extra log e.g. a crash log)[CR]• view log limit to prevent crashing (dependent on device / platform - file size: 1000 lines ~ 170kb)[CR]• customise text colours with billions of text colour combinations[CR][CR]Choose from 140 colours for each one (there is also a none option):[CR]TEXT_ADDON = header (notifications, logs and text boxes)[CR]TEXT_DARK = logs and text boxes[CR]TEXT_DIM = menu text[CR]TEXT_GENERAL = main text (notifications, logs and text boxes)[CR]TEXT_HIGHLIGHT = values on menu requiring attention and logs[CR]TEXT_ITEM = items on menu and text boxes[CR]TEXT_VALUE = values on menu and text boxes[CR][CR]\'Exit Only >\' exits the add-on'

NOTES_TEXT = '[CR][CR][CR]N O T E S[CR][CR]The number of lines in New System Log and New System Log Errors will increase as processes are run and by background activies.[CR]The number of lines shown on the menu will not change unless the menu is reloaded (even after viewing a log).[CR]The number of lines shown at the top of the log may therefore be higher than the menu.[CR][CR]Press the OK button in settings to save any changes made and after resetting a category to default.[CR]Some changes may require restarting the add-on.'

DEVELOPMENT_TEXT = '[CR][CR][CR]D E V E L O P M E N T[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered where required using https://aipy.dev/tools'

CHANGELOG_TEXT = '[CR][CR][CR]C H A N G E L O G [LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 1.7.0 (7 menu items)[CR]- initial code from Database Toolbox 1.10.0 by C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e (plugin.program.database-toolbox)[CR]- code added from Maintenance Toolbox 1.4.0 by C[COLOR dimgray]o[/COLOR]d[COLOR dimgray]e[/COLOR]-[COLOR dimgray]E[/COLOR]-[COLOR dimgray]M[/COLOR]a[COLOR dimgray]g[/COLOR]p[COLOR dimgray]i[/COLOR]e (plugin.program.maintenance-toolbox)[CR]- icon.png changed[CR]- variables and functions reworked[CR]- menu and logs reworked[CR]- user information reworked (instructions, notes, development and changelog)'

User_Information_Text = '[COLOR %s][B]U S E R   I N F O R M A T I O N[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Development / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + DEVELOPMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text + Development_Information_Text)

#####################################################################################

# ============================================================
# FUNCTION: Count_Log_Errors
# ============================================================

def Count_Log_Errors(file_path):

	try:
		with open(file_path, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			content = file.read()
			content = content.replace('\n', '[CR]').replace('\r', '')
			pattern = r"-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--"
			count_log_errors = len(re.findall(pattern, content))

			return count_log_errors

	except FileNotFoundError:
		return 0

	except IOError:
		Log(Log_Title + System_Errors + 'Count Log Errors: error reading file', xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]File Error[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except re.error as e:
		Log(Log_Title + System_Errors + 'Count Log Errors: exception[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

	except Exception as e:
		Log(Log_Title + System_Errors + 'Count Log Errors: exception[CR]%s' % str(e), xbmc.LOGERROR)
		return '[COLOR %s][LIGHT]Exception[/LIGHT][/COLOR]' % TEXT_HIGHLIGHT

# ============================================================
# FUNCTION: Count_Log_Files (excludes subfolders)
# ============================================================

def Count_Log_Files(folder_path):

	try:
		files = os.listdir(folder_path)

	except OSError:
		return 0

	count_log_files = 0

	for file in files:
		file_path = os.path.join(folder_path, file)
		if os.path.isfile(file_path):
			if file.endswith('.log'):

				count_log_files += 1

	return count_log_files

# ============================================================
# FUNCTION: Count_Log_Lines
# ============================================================

def Count_Log_Lines(file_path):

	if not os.path.exists(file_path):
		return 0

	count_log_lines = 0

	try:
		with open(file_path, 'r', encoding = 'utf-8', errors = 'replace') as file:
			for line in file:
				if line.strip():

					count_log_lines += 1

	except UnicodeDecodeError:
		with open(file_path, 'r', encoding = 'latin-1', errors = 'replace') as file:
			for line in file:
				if line.strip():

					count_log_lines += 1

	return count_log_lines

# ============================================================
# FUNCTION: System_Log
# ============================================================

def System_Log(log_file):

	if Count_Log_Lines(log_file) > VIEW_LOG_LIMIT:
		Notification(Addon_Title, '[COLOR %s]System Log: unable to view more than %s lines[/COLOR]' % (TEXT_GENERAL, VIEW_LOG_LIMIT))
		return False

	system_log = []

	try:
		with open(log_file, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			content = file.read().replace('\n', '[NL]')
			content = ('[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, content))
			matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(content)
			for item in matches:
				string = '-->Python callback/script returned the following error<--%s-->End of Python script error report<--' % item
				content = content.replace(string, '[COLOR %s]%s[/COLOR]' % (TEXT_VALUE, string))
			content = content.replace('WARNING', '[COLOR %s]WARNING[/COLOR]' % TEXT_HIGHLIGHT).replace('ERROR', '[COLOR %s]ERROR[/COLOR]' % TEXT_VALUE).replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR %s]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]' % TEXT_ITEM)
			content = content.replace('\\\\', '\\').replace(HOME, '')

			if content:
				system_log.append((log_file, content))

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System + 'System Log: file error[CR]%s' % e, xbmc.LOGINFO)

	else:
		Notification(Addon_Title, '[COLOR %s]System Log: 0 lines in log[/COLOR]' % TEXT_GENERAL)

	for log_file, content in system_log:
		TextBox('[B]%s[/B][COLOR %s][CR]System Log: [COLOR %s]%s[LIGHT] lines[/COLOR] (oldest at the top)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, Count_Log_Lines(log_file)), content)

# ============================================================
# FUNCTION: System_Log_Errors
# ============================================================

def System_Log_Errors(log_file):

	system_log_errors = []

	try:
		with open(log_file, 'r', encoding = 'utf-8', errors = 'ignore') as file:
			content = file.read()
			content = content.replace('\n', '[CR]').replace('\r', '')
			matches = re.compile(r"-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(content)[::-1]

			if matches:
				system_log_errors.append(log_file)

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System_Errors + 'System Log Errors: file error[CR]%s' % e, xbmc.LOGINFO)

	if system_log_errors:
		string = ''

		index = 0

		for match in matches:
			print(index, match)

			index += 1			

			string += '[COLOR %s]System Log Error: [/COLOR][COLOR %s]%s[/COLOR][COLOR %s]%s[/COLOR][CR]' % (TEXT_ITEM, TEXT_VALUE, str(index), TEXT_GENERAL, match.replace(HOME, '/').replace('										', ''))

		TextBox('[B]%s[/B][COLOR %s][CR]System Log Errors: [COLOR %s]%s[/COLOR][LIGHT] (newest at the top)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, TEXT_VALUE, Count_Log_Errors(log_file)), string)

	else:
		Notification(Addon_Title, '[COLOR %s]System Log Errors: 0 errors found[/COLOR]' % TEXT_GENERAL)

#####################################################################################

# ============================================================
# Menu Entry Point
# ============================================================

if '/Addon_Header' in PLUGIN_URL:
	ADDON.openSettings()

elif '/New_System_Log_Errors' in PLUGIN_URL:
	System_Log_Errors(LOG_NEW)

elif '/New_System_Log' in PLUGIN_URL:
	System_Log(LOG_NEW)

elif '/Old_System_Log_Errors' in PLUGIN_URL:
	System_Log_Errors(LOG_OLD)

elif '/Old_System_Log' in PLUGIN_URL:
	System_Log(LOG_OLD)

elif '/Exit_Only' in PLUGIN_URL:
	xbmc.executebuiltin('Action(Back)')
	Log(Log_Title + '[COLOR %s]menu > [/COLOR][COLOR %s][LIGHT]Finished (Exit Only)[/LIGHT][/COLOR]' % (TEXT_GENERAL, TEXT_DARK), xbmc.LOGINFO)

elif '/User_Information' in PLUGIN_URL:
	User_Information()

else:
	# Create the menu items.
	xbmcplugin.setContent(PLUGIN_ID, 'files')

	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]    S e t t i n g s  >' % Addon_Title)
	Addon_Header.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	New_System_Log_Errors = xbmcgui.ListItem('[COLOR %s]New System Log Errors: [/COLOR][COLOR %s]%s[/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE if Count_Log_Errors(LOG_NEW) == 0 else TEXT_HIGHLIGHT, Count_Log_Errors(LOG_NEW)))
	New_System_Log_Errors.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	New_System_Log = xbmcgui.ListItem('[COLOR %s]New System Log: [/COLOR][COLOR %s]%s[LIGHT] lines[/LIGHT][/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE, Count_Log_Lines(LOG_NEW)))
	New_System_Log.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Old_System_Log_Errors = xbmcgui.ListItem('[COLOR %s]Old System Log Errors: [/COLOR][COLOR %s]%s[/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE if Count_Log_Errors(LOG_OLD) == 0 else TEXT_HIGHLIGHT, Count_Log_Errors(LOG_OLD)))
	Old_System_Log_Errors.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Old_System_Log = xbmcgui.ListItem('[COLOR %s]Old System Log: [/COLOR][COLOR %s]%s[LIGHT] lines[/LIGHT][/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE, Count_Log_Lines(LOG_OLD)))
	Old_System_Log.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Count_Log_Files = xbmcgui.ListItem('[COLOR %s]Count Log Files: [/COLOR][COLOR %s]%s[LIGHT] in folder[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_HIGHLIGHT if Count_Log_Files(TEMP) > int(ADDON.getSetting('LOGS_HIGHLIGHT')) else TEXT_VALUE, Count_Log_Files(TEMP)))
	Count_Log_Files.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	View_Log_Limit = xbmcgui.ListItem('[COLOR %s]View Log Limit: [/COLOR][COLOR %s]%s[LIGHT] lines[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, VIEW_LOG_LIMIT))
	View_Log_Limit.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Exit_Only = xbmcgui.ListItem('Exit Only  >')
	Exit_Only.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	User_Information = xbmcgui.ListItem('U s e r   I n f o r m a t i o n  >')
	User_Information.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Addon_Developer = xbmcgui.ListItem('[COLOR %s]Developer: [/COLOR]%s' % (TEXT_DIM, ADDON_DEVELOPER))
	Addon_Developer.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Name = xbmcgui.ListItem('[COLOR %s]Name: %s[/COLOR]' % (TEXT_DIM, ADDON_NAME))
	Addon_Name.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Version = xbmcgui.ListItem('[COLOR %s]Version: %s[/COLOR]' % (TEXT_DIM, ADDON_VERSION))
	Addon_Version.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_ID = xbmcgui.ListItem('[COLOR %s]Addon ID: %s[/COLOR]' % (TEXT_DIM, ADDON_ID))
	Addon_ID.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	# Append to PLUGIN_URL as it already ends with a slash.
	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addon_Header', Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'New_System_Log_Errors', New_System_Log_Errors, False),
			(PLUGIN_URL + 'New_System_Log', New_System_Log, False),
			(PLUGIN_URL + 'Old_System_Log_Errors', Old_System_Log_Errors, False),
			(PLUGIN_URL + 'Old_System_Log', Old_System_Log, False),
			(PLUGIN_URL, Count_Log_Files, False),
			(PLUGIN_URL, View_Log_Limit, False),
			(PLUGIN_URL + 'Exit_Only', Exit_Only, False),
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