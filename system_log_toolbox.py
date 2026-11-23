# ============================================================
# system_log_toolbox.py by Code-E-Magpie
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

from collections import deque

# ============================================================
# Variables
# ============================================================

ADDON_ID = xbmcaddon.Addon().getAddonInfo('id')
ADDON = xbmcaddon.Addon(ADDON_ID)
ADDON_AUTHOR = ADDON.getAddonInfo('author')
ADDON_FANART = ADDON.getAddonInfo('fanart')
ADDON_ICON = ADDON.getAddonInfo('icon')
ADDON_NAME = ADDON.getAddonInfo('name')
ADDON_VERSION = ADDON.getAddonInfo('version')
HOME = xbmcvfs.translatePath('special://home/')
LOGPATH = xbmcvfs.translatePath('special://logpath/')
LOG_NEW = os.path.join(LOGPATH, 'kodi.log')
LOG_OLD = os.path.join(LOGPATH, 'kodi.old.log')
NOTIFICATION_DURATION = ADDON.getSettings().getInt('notification_duration')
PLUGIN_ID = int(sys.argv[1])
PLUGIN_URL = sys.argv[0]
TEXT_ADDON = ADDON.getSetting('text_addon')
TEXT_DARK = ADDON.getSetting('text_dark')
TEXT_DIM = ADDON.getSetting('text_dim')
TEXT_GENERAL = ADDON.getSetting('text_general')
TEXT_HIGHLIGHT = ADDON.getSetting('text_highlight')
TEXT_ITEM = ADDON.getSetting('text_item')
TEXT_VALUE = ADDON.getSetting('text_value')
TOOLBOX = os.path.join(ADDON.getAddonInfo('path'), 'resources', 'media', 'toolbox.png')
VIEW_LOG_LIMIT = ADDON.getSettings().getInt('view_log_limit')

# ============================================================
# Addon_ID_Version / Addon_Title / Dialogue / Log_Title
# ============================================================

Addon_ID_Version = ('[COLOR %s]%s [/COLOR][COLOR %s] %s[/COLOR]' % (TEXT_ITEM, ADDON_ID, TEXT_VALUE, ADDON_VERSION))
Addon_Title = ('[COLOR %s]%s[/COLOR]' % (TEXT_ADDON, ' '.join(ADDON_NAME)))
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

def Log(message, level = xbmc.LOGDEBUG):
	xbmc.log(message, level = level)

# ============================================================
# FUNCTION: Notification
# ============================================================

def Notification(title, message, times = NOTIFICATION_DURATION, icon = ADDON_ICON, sound = False):
	Dialogue.notification(title, message, icon, times, sound)

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

def TextBox(title, text):
	class TextBoxes(xbmcgui.WindowXMLDialog):

		def onAction(self, action):
			if action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

		def onClick(self, controlId):
			if (controlId == self.close_button):
				self.close()
			elif controlId != self.close_button:
				self.noop = lambda: None

		def onInit(self): # group = 8000, background = 8100, noop = 8181
			self.title = 8200
			self.text = 8300
			self.scrollbar = 8400
			self.close_button = 8500
			self.noop = lambda: None
			self.showDialog()

		def showDialog(self):
			close = '[COLOR %s]Close[/COLOR]' % TEXT_GENERAL
			self.getControl(self.title).setLabel(title)
			self.getControl(self.close_button).setLabel(close)
			self.getControl(self.text).setText(text)
			self.setFocusId(self.scrollbar)

	textbox = TextBoxes("Textbox.xml", ADDON.getAddonInfo('path'), 'default')
	textbox.doModal()
	del textbox

#####################################################################################

# ============================================================
# FUNCTION: Development_Information
# ============================================================

MAGPIE_TEXT = '%s[CR][CR]The official repository of %s add-ons.[CR]Distribution of the Magpie Repository is permitted.[CR][CR]IMPORTANT:[CR]Distribution of %s add-ons are NOT permitted.[CR]%s add-ons are exclusively distributed via the Magpie Repository and / or %s on GitHub.[CR]The code and files of these add-ons are free for use, subject to crediting %s.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.magpie[CR][CR]To install Magpie Repository:[CR]Add the Kodi source https://Code-E-Magpie.github.io/repository.magpie/[CR]Use the \'Install from zip file\' method to install the Magpie Repository.[/COLOR]' % (' '.join('MAGPIE REPOSITORY'), ADDON_AUTHOR, ADDON_AUTHOR, ADDON_AUTHOR, ADDON_AUTHOR, ADDON_AUTHOR, TEXT_DARK)

MAINTENANCE_TEXT = '[CR][CR][CR]%s[CR][CR]Maintenance Toolbox with easy to read Kodi information (system, add-ons, network and internet).[CR]Clear cache + folders, surplus add-ons, temp folder and thumbnails.[CR]View logs and errors (new and old).[CR]Check repositories, sources and internet speed (Speedtest by Ookla).[CR]Backup and restore favourites, sources, logs, userdata, add-ons, add-on data etc.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.maintenance-toolbox[/COLOR]' % (' '.join('MAINTENANCE TOOLBOX'), TEXT_DARK)

REORDER_TEXT = '[CR][CR][CR]%s[CR][CR]Easy to use reordering of favourites for Kodi using dialogue boxes to exit and save.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.reorder-favourites[/COLOR]' % (' '.join('REORDER FAVOURITES'), TEXT_DARK)

REORDER_SE_TEXT = '[CR][CR][CR]%s[CR][CR]Easy to use reordering of favourites for Kodi using the menu to exit and save. Legacy version of Reorder Favourites.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.reorder-favourites[/COLOR]' % (' '.join('REORDER FAVOURITES SE'), TEXT_DARK)

LOG_TEXT = '[CR][CR][CR]%s[CR][CR]System Log Toolbox easy to use system log viewer.[CR][CR][COLOR %s]Add-on available from Magpie Repository. Further details on GitHub and within the add-on itself.[CR]https://github.com/Code-E-Magpie/plugin.program.system-log-toolbox[/COLOR]' % (' '.join('SYSTEM LOG TOOLBOX'), TEXT_DARK)

SPECIAL_TEXT = '[CR][CR][CR]%s[CR][CR]Special Favourites: Kodi special paths and customised examples.[CR]Special Sources: Kodi special paths (files & folders) and customised examples.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/Code-E-Magpie[/COLOR]' % (' '.join('FAVOURITES & SOURCES'), TEXT_DARK)

TEMPLATE_TEXT = '[CR][CR][CR]%s[CR][CR]Created to illustrate a GitHub repository with a simple folder structure linked to a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.template[/COLOR][CR][CR]Alternatively a GitHub repository linked to a Kodi source, without using a Kodi repository.[CR][CR][COLOR %s]Available on GitHub only.[CR]https://github.com/Code-E-Magpie/repository.simple[/COLOR]' % (' '.join('TEMPLATE REPOSITORY'), TEXT_DARK, TEXT_DARK)

Development_Text = '[CR][CR][CR][COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Magpie Repository / Maintenance Toolbox / Reorder Favourites / Reorder Favourites SE / System Log Toolbox / Favourites & Sources / Template Repository)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('Code-E-Magpie Development'), TEXT_VALUE, TEXT_GENERAL, (MAGPIE_TEXT + MAINTENANCE_TEXT + REORDER_TEXT + REORDER_SE_TEXT + LOG_TEXT + SPECIAL_TEXT + TEMPLATE_TEXT))

# ============================================================
# FUNCTION: User_Information
# ============================================================

INSTRUCTIONS_TEXT = '%s[CR][CR]Open the add-on to access the menu.[CR]Select one of the \'>\' menu items.' % ' '.join('INSTRUCTIONS')

NOTES_TEXT = '[CR][CR][CR]%s[CR][CR]The number of lines in the New System Log will increase as processes are run and by background activies.[CR]The file size of the New System Log also increases.[CR]The figures shown on the menu will not change unless the add-on is restarted.[CR]Custom Lines and Custom Linez filters are case sensitive.' % ' '.join('NOTES')

SETTINGS_TEXT = '[CR][CR][CR]%s[CR][CR]Press the OK button in settings to save any changes made and after resetting a category to default.[CR]Some changes may require restarting the add-on.[CR][CR]Custom Lines and Custom Linez filter results based on the criteria entered and saved in settings (i.e. favourite custom searches)[CR]Exclude blank lines when viewing unfiltered system log[CR]Notification duration[CR]Logs Count highlight if number set exceeded (used to identify the exsistance of an extra log e.g. a crash log)[CR]View Log Limit prevents crashing (dependent on device / platform - file size: 1000 lines ≈ 170kb)[CR]Customise text colours with billions of text colour combinations[CR][CR]Choose from 140 colours for each one (there is also a none option):[CR]Text Add-on Colour: header (menu, notifications, logs and text boxes)[CR]Text Dark Colour: logs and text boxes[CR]Text Dim Colour: menu[CR]Text General Colour: main text (notifications, logs, text boxes and close button)[CR]Text Highlight Colour: values on menu requiring attention and logs[CR]Text Item Colour: items on menu and text boxes[CR]Text Value Colour: values on menu and text boxes' % ' '.join('SETTINGS')

ENVIRONMENT_TEXT = '[CR][CR][CR]%s[CR][CR]Kodi v21.3 Omega apk (Android app) with Confluence skin as default (including default font).[CR]Tablet (1340 x 800 aspect ratio 5:3) running Android 14 using QuickEdit apk (TryItAndSee / LearnAsYouGo iterative development and testing).[CR]Chromecast HD (1280 x 720 aspect ratio 16:9) running Android TV OS version 14 (user testing).[CR]100%% tested and working on Android.[CR]Not tested on other platforms.[CR]Code debugged and reengineered using https://aipy.dev/tools where required (pre 2.7.0).[CR]Code debugged and reengineered using https://stackoverflow.com/ai-assist (2.7.0 onwards).' % ' '.join('DEVELOPMENT ENVIRONMENT')

CHANGELOG_TEXT = '[CR][CR][CR]%s [LIGHT] (newest at the top)[/LIGHT][CR][CR]Version code x.y.z attributes[CR]x = major change / y = number of \'>\' menu items / z = minor change[CR][CR]version 3.9.0 (9 menu items)[CR]- reduced the number of times logs are read to count lines and errors[CR]- log file sizes added to menu (View Log Limit removed from menu)[CR]- New System Log Filters and Old System Log Filters options added to menu[CR]- custom lines filter options added to settings (case sensitive)[CR]- exclude blank lines when viewing unfiltered system logs option added to settings[CR]- number of lines displayed added to unfiltered system logs and filtered logs[CR]- datestamp added to first line of error in error logs and highlighted in filtered and unfiltered logs[CR]- minor changes to settings and Textbox.xml[CR][CR]version 2.7.3 (7 menu items)[CR]- Code-E-Magpie development content amended[CR]- minor changes to improve consistency with other add-ons including the handling of integers[CR][CR]version 2.7.2 (7 menu items)[CR]- headers, logs and notifications reworked to specify new or old[CR][CR]version 2.7.1 (7 menu items)[CR]- settings reworked to avoid clashes (different names to variables etc.)[CR]- minor changes to Textbox.xml to improve performance and consistency with other add-ons[CR]- minor changes to Log and TextBox functions to improve consistency with other add-ons[CR][CR]version 2.7.0 (7 menu items)[CR]- change to enable recent lines to be viewed in large logs (number of lines determined by the view log limit setting)[CR][CR]version 1.7.1 (7 menu items)[CR]- close button added to text colour customisation[CR]- empty log file notification reworked[CR][CR]version 1.7.0 (7 menu items)[CR]- initial code from Abacus Program 1.0.0 by %s (plugin.program.code-e-magpie)[CR]- code added from Maintenance Toolbox 1.4.0 by %s (plugin.program.maintenance-toolbox)[CR]- icon.png changed[CR]- variables and functions reworked[CR]- menu and logs reworked[CR]- user information reworked (instructions, notes, development and changelog)' % (' '.join('CHANGELOG'), ADDON_AUTHOR, ADDON_AUTHOR)

User_Information_Text = '[COLOR %s][B]%s[/B][CR][COLOR %s][LIGHT](Instructions / Notes / Settings / Development Environment / Changelog)[/LIGHT][/COLOR][/COLOR][CR][CR][COLOR %s]%s[/COLOR]' % (TEXT_ITEM, ' '.join('USER INFORMATION'), TEXT_VALUE, TEXT_GENERAL, (INSTRUCTIONS_TEXT + NOTES_TEXT + SETTINGS_TEXT + ENVIRONMENT_TEXT + CHANGELOG_TEXT))

def User_Information():
	TextBox('[B]%s[/B][CR]%s' % (Addon_Title, Addon_ID_Version), User_Information_Text + Development_Text)

#####################################################################################

# ============================================================
# FUNCTION: Count_Log_Files (excludes subfolders)
# ============================================================

def Count_Log_Files(folder_path):

	try:
		files = os.listdir(folder_path)
	except OSError:
		return 0

	return sum(1 for name in files if os.path.isfile(os.path.join(folder_path, name)) and name.lower().endswith(".log"))

# ============================================================
# FUNCTION: Count_Log_Lines
# ============================================================

def Count_Log_Lines(file_path):

	if not os.path.exists(file_path):
		return 0, 0

	log_error_pattern = re.compile(r"-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--", re.DOTALL)

	with open(file_path, "r", encoding = "UTF-8", errors = "replace") as file:
		content = file.read()

	count_log_lines = sum(1 for line in content.splitlines() if line.strip())
	count_log_errors = len(log_error_pattern.findall(content))

	return count_log_lines, count_log_errors

# ============================================================
# FUNCTION: Size_Convert
# ============================================================

def Size_Convert(num, suffix = 'B'):

	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)

		num /= 1024.0
	return "%.02f %s%s" % (num, 'G', suffix)

# ============================================================
# FUNCTION: Size_File
# ============================================================

def Size_File(file_path):

	try:
		if not os.path.exists(file_path):
			return 0

		if not os.path.isfile(file_path):
			return 0

		return os.path.getsize(file_path)

	except (OSError, PermissionError):
		return 0

# ============================================================
# FUNCTION: System_Log
# ============================================================

def System_Log(log_file, log_key):

	Custom_Log_Key = ADDON.getSetting('custom_log_lines')
	Custom_Log_Keyz = ADDON.getSetting('custom_log_linez')
	Exclude_Blank_Lines = 'no blanks' if ADDON.getSetting('exclude_log_lines') == 'true' else 'blanks'
	New_Old = 'New System Log' if log_file == LOG_NEW else 'Old System Log'

	log_keys = ['ALL', 'custom lines', 'custom linez', 'debug', 'error', 'exclude general', 'exclude info', 'info', 'notice', 'warning']
	log_labels = ['System Log Lines [COLOR %s]subject to limit: %s [/COLOR][COLOR %s][LIGHT](%s)[/LIGHT][/COLOR]' % (TEXT_DARK, VIEW_LOG_LIMIT, TEXT_DIM, Exclude_Blank_Lines),
		'Custom Lines [COLOR %s](%s)[/COLOR]' % (TEXT_DIM, Custom_Log_Key),
		'Custom Linez [COLOR %s](%s)[/COLOR]' % (TEXT_DIM, Custom_Log_Keyz),
		'Debug Lines [COLOR %s](debug <general>:)[/COLOR]' % TEXT_DIM,
		'Error Lines [COLOR %s](error <general>:)[/COLOR]' % TEXT_DIM,
		'Exclude General Lines [COLOR %s](<general>:)[/COLOR]' % TEXT_DIM,
		'Exclude Info Lines [COLOR %s](info <general>:)[/COLOR]' % TEXT_DIM,
		'Info Lines [COLOR %s](info <general>:)[/COLOR]' % TEXT_DIM,
		'Notice Lines [COLOR %s](notice <general>:)[/COLOR]' % TEXT_DIM,
		'Warning Lines [COLOR %s](warning <general>:)[/COLOR]' % TEXT_DIM]

	if log_key != 'ALL':
		dialogue_header = '[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, ' '.join('System Log Filters'))
		choice = Dialogue.select(dialogue_header, log_labels)

		if choice == -1:
			return False

		log_key = log_keys[choice]

	count_log_lines = 0
	system_log = []

	try:
		tail = deque(maxlen = VIEW_LOG_LIMIT) if log_key == 'ALL' else []

		with open(log_file, 'r', encoding = 'UTF-8', errors = 'replace') as file:
			exclude_blanks = ADDON.getSetting('exclude_log_lines') == 'true'

			for line in file:
				if (not exclude_blanks) or line.strip():
					count_log_lines += 1
					tail.append(line)

		if count_log_lines == 0:
			Notification(Addon_Title, '[COLOR %s]%s: 0 lines in log[/COLOR]' % (TEXT_GENERAL, New_Old))
			return False

		if log_key == 'ALL':
			filtered_lines = tail
		elif log_key == 'custom lines':
			filtered_lines = [line for line in tail if Custom_Log_Key in line]
		elif log_key == 'custom linez':
			filtered_lines = [line for line in tail if Custom_Log_Keyz in line]
		elif log_key == 'debug':
			filtered_lines = [line for line in tail if 'debug <general>:' in line.lower()]
		elif log_key == 'error':
			filtered_lines = [line for line in tail if 'error <general>:' in line.lower()]
		elif log_key == 'exclude general':
			filtered_lines = [line for line in tail if '<general>:' not in line.lower()]
		elif log_key == 'exclude info':
			filtered_lines = [line for line in tail if 'info <general>:' not in line.lower()]
		elif log_key == 'info':
			filtered_lines = [line for line in tail if 'info <general>:' in line.lower()]
		elif log_key == 'notice':
			filtered_lines = [line for line in tail if 'notice <general>:' in line.lower()]
		elif log_key == 'warning':
			filtered_lines = [line for line in tail if 'warning <general>:' in line.lower()]
		else:
			filtered_lines = tail

		line_count = len(filtered_lines)
		content = ''.join(filtered_lines)

		pattern_a = "-->Python callback/script returned the following error<--"
		pattern_z = "-->End of Python script error report<--"
		block_regex = re.compile(r"^[^\n]*%s.*?%s" % (re.escape(pattern_a), re.escape(pattern_z)), re.DOTALL | re.MULTILINE)

		last_index = 0
		log_parts = []

		for m in block_regex.finditer(content):
			start, end = m.span()
			full_block = m.group(0)

			log_parts.append(content[last_index:start])

			newline_index = full_block.find('\n')
			if newline_index != -1:
				header_text = full_block[:newline_index + 1]
				rest = full_block[newline_index + 1:]
			else:
				header_text = full_block
				rest = ''

			footer_index = rest.rfind(pattern_z)
			if footer_index != -1:
				body_text = rest[:footer_index]
				footer_text = rest[footer_index:]
			else:
				body_text = rest
				footer_text = ''

			header = '[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, header_text)
			body = '[COLOR %s]%s[/COLOR]' % (TEXT_VALUE, body_text)
			footer = '[COLOR %s]%s[/COLOR]' % (TEXT_ITEM, footer_text)

			replacement = header + body + footer
			log_parts.append(replacement)

			last_index = end

		log_parts.append(content[last_index:])

		content = ''.join(log_parts)
		content = re.sub(r'\bWARNING\b', '[COLOR %s]WARNING[/COLOR]' % TEXT_HIGHLIGHT, content)
		content = re.sub(r'\bERROR\b', '[COLOR %s]ERROR[/COLOR]' % TEXT_HIGHLIGHT, content)
		content = '[COLOR %s]%s[/COLOR]' % (TEXT_GENERAL, content)
		content = content.replace(HOME, '')

		if content:
			system_log.append((log_file, content))

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System + '%s: file error %s' % (New_Old, e), xbmc.LOGINFO)

	for log_file, content in system_log:
		TextBox('[B]%s[/B][COLOR %s][CR]%s: [COLOR %s]%s[LIGHT] of %s lines  [/LIGHT][/COLOR]Limit: %s [LIGHT](%s)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, New_Old, TEXT_VALUE, line_count, count_log_lines, VIEW_LOG_LIMIT, Exclude_Blank_Lines if log_key == 'ALL' else log_key), content)

# ============================================================
# FUNCTION: System_Log_Errors
# ============================================================

def System_Log_Errors(log_file):

	New_Old_Errors = 'New System Log Errors' if log_file == LOG_NEW else 'Old System Log Errors'

	pattern_a = "-->Python callback/script returned the following error<--"
	pattern_z = "-->End of Python script error report<--"
	block_regex = re.compile(r"^[^\n]*%s.*?%s" % (re.escape(pattern_a), re.escape(pattern_z)), re.DOTALL | re.MULTILINE)

	system_log_errors = []

	try:
		with open(log_file, 'r', encoding = 'UTF-8', errors = 'replace') as file:
			content = file.read()
			blocks = block_regex.findall(content)
			count_log_errors = len(blocks)
			matches = blocks[::-1]

			if matches:
				system_log_errors.append(log_file)

		if count_log_errors == 0:
			Notification(Addon_Title, '[COLOR %s]%s: 0 lines in log[/COLOR]' % (TEXT_GENERAL, New_Old_Errors))
			return False

	except (OSError, UnicodeDecodeError) as e:
		Log(Log_Title + System_Errors + '%s: file error %s' % (New_Old_Errors, e), xbmc.LOGINFO)

	if system_log_errors:
		string = ''

		index = 0
		for match in matches:
			index += 1

			cleaned = match.replace(HOME, 'special://home/')
			string += '[COLOR %s]%s: [/COLOR][COLOR %s]%s[/COLOR][CR]' % (TEXT_ITEM, New_Old_Errors.rstrip("s"), TEXT_VALUE, str(index))
			string += '[COLOR %s]%s[/COLOR][CR][CR][CR]' % (TEXT_GENERAL, cleaned)

		TextBox('[B]%s[/B][COLOR %s][CR]%s: [COLOR %s]%s[/COLOR][LIGHT] (newest at the top)[/LIGHT][/COLOR]' % (Addon_Title, TEXT_ITEM, New_Old_Errors, TEXT_VALUE, count_log_errors), string)

	else:
		Notification(Addon_Title, '[COLOR %s]%s: 0 errors found[/COLOR]' % (TEXT_GENERAL, New_Old_Errors))

#####################################################################################

# ============================================================
# Menu Entry Point
# ============================================================

if '/Addon_Header' in PLUGIN_URL:
	ADDON.openSettings()

elif '/New_System_Log_Errors' in PLUGIN_URL:
	System_Log_Errors(LOG_NEW)

elif '/New_System_Log_All' in PLUGIN_URL:
	System_Log(LOG_NEW, 'ALL')

elif '/New_System_Log_Filters' in PLUGIN_URL:
	System_Log(LOG_NEW, '')

elif '/Old_System_Log_Errors' in PLUGIN_URL:
	System_Log_Errors(LOG_OLD)

elif '/Old_System_Log_All' in PLUGIN_URL:
	System_Log(LOG_OLD, 'ALL')

elif '/Old_System_Log_Filters' in PLUGIN_URL:
	System_Log(LOG_OLD, '')

elif '/Exit_Only' in PLUGIN_URL:
	xbmc.executebuiltin('Action(Back)')

elif '/User_Information' in PLUGIN_URL:
	User_Information()

else:
	xbmcplugin.setContent(PLUGIN_ID, 'files')

	new_log_lines, new_log_errors = Count_Log_Lines(LOG_NEW)
	old_log_lines, old_log_errors = Count_Log_Lines(LOG_OLD)

	Equals = xbmcgui.ListItem('[COLOR %s]==================================================[/COLOR]' % TEXT_DIM)
	Equals.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_FANART})

	Addon_Header = xbmcgui.ListItem('[B]%s[/B]%s' % (Addon_Title, ' '.join('  Settings >')))
	Addon_Header.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	New_System_Log_Errors = xbmcgui.ListItem('[COLOR %s]New System Log Errors:[/COLOR][COLOR %s] %s[/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE if new_log_errors == 0 else TEXT_HIGHLIGHT, new_log_errors))
	New_System_Log_Errors.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	New_System_Log_All = xbmcgui.ListItem('[COLOR %s]New System Log:[/COLOR][COLOR %s] %s [LIGHT]lines[/LIGHT][/COLOR]  >  [COLOR %s][LIGHT](file size: %s)[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, new_log_lines, TEXT_DIM, Size_Convert(Size_File(LOG_NEW))))
	New_System_Log_All.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	New_System_Log_Filters = xbmcgui.ListItem('[COLOR %s]New System Log Filters[/COLOR]  >  ' % TEXT_ITEM)
	New_System_Log_Filters.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Old_System_Log_Errors = xbmcgui.ListItem('[COLOR %s]Old System Log Errors:[/COLOR][COLOR %s] %s[/COLOR]  >' % (TEXT_ITEM, TEXT_VALUE if old_log_errors == 0 else TEXT_HIGHLIGHT, old_log_errors))
	Old_System_Log_Errors.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Old_System_Log_All = xbmcgui.ListItem('[COLOR %s]Old System Log:[/COLOR][COLOR %s] %s [LIGHT]lines[/LIGHT][/COLOR]  >  [COLOR %s][LIGHT](file size: %s)[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_VALUE, old_log_lines, TEXT_DIM, Size_Convert(Size_File(LOG_OLD))))
	Old_System_Log_All.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Old_System_Log_Filters = xbmcgui.ListItem('[COLOR %s]Old System Log Filters[/COLOR]  >  ' % TEXT_ITEM)
	Old_System_Log_Filters.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Logs_Count = xbmcgui.ListItem('[COLOR %s]Logs Count:[/COLOR][COLOR %s] %s  [/COLOR][COLOR %s][LIGHT](.log files in special://home/temp)[/LIGHT][/COLOR]' % (TEXT_ITEM, TEXT_HIGHLIGHT if Count_Log_Files(LOGPATH) > ADDON.getSettings().getInt('logs_count') else TEXT_VALUE, Count_Log_Files(LOGPATH), TEXT_DIM))
	Logs_Count.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Exit_Only = xbmcgui.ListItem('Exit Only  >')
	Exit_Only.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	User_Information = xbmcgui.ListItem(' '.join('User Information >'))
	User_Information.setArt({'fanart': TOOLBOX, 'thumb': ADDON_ICON})

	Addon_Developer = xbmcgui.ListItem('[COLOR %s]Developer: [/COLOR]%s' % (TEXT_DIM, ADDON_AUTHOR))
	Addon_Developer.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Name = xbmcgui.ListItem('[COLOR %s]Name: %s[/COLOR]' % (TEXT_DIM, ADDON_NAME))
	Addon_Name.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_Version = xbmcgui.ListItem('[COLOR %s]Version: %s[/COLOR]' % (TEXT_DIM, ADDON_VERSION))
	Addon_Version.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	Addon_ID = xbmcgui.ListItem('[COLOR %s]Add-on ID: %s[/COLOR]' % (TEXT_DIM, ADDON_ID))
	Addon_ID.setArt({'fanart': ADDON_FANART, 'thumb': ADDON_ICON})

	xbmcplugin.addDirectoryItems(
		PLUGIN_ID,
		(
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'Addon_Header', Addon_Header, False),
			(PLUGIN_URL, Equals, False),
			(PLUGIN_URL + 'New_System_Log_Errors', New_System_Log_Errors, False),
			(PLUGIN_URL + 'New_System_Log_All', New_System_Log_All, False),
			(PLUGIN_URL + 'New_System_Log_Filters', New_System_Log_Filters, False),
			(PLUGIN_URL + 'Old_System_Log_Errors', Old_System_Log_Errors, False),
			(PLUGIN_URL + 'Old_System_Log_All', Old_System_Log_All, False),
			(PLUGIN_URL + 'Old_System_Log_Filters', Old_System_Log_Filters, False),
			(PLUGIN_URL, Logs_Count, False),
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