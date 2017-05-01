#!/usr/bin/python
# -*- coding: utf-8 -*-

import os, signal, gi, time, json

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')

from urllib2 import Request, urlopen, URLError
from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify
from gi.repository import GObject

APPINDICATOR_ID = 'McController'

IP = "grapefruit.vingu.online"

TEST_PORT = "25123"
PANGEA_PORT = "25001"
SURVIVAL_PORT = "25555"

indicator = None
server_status = None

def main():
	GObject.timeout_add_seconds(1, update_widget)
	global indicator
	global server_status
	server_status = get_status()
	indicator = appindicator.Indicator.new(APPINDICATOR_ID, 
		os.path.abspath('../icon/minecraft.png'), 
		appindicator.IndicatorCategory.SYSTEM_SERVICES)

	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(build_menu())
	notify.init(APPINDICATOR_ID)
	notify.Notification.new("<b>Notification</b>", 'mc-controller gestartet.', None).show()
	gtk.main()

def update_widget():
	global indicator
	global server_status
	if not server_status == get_status():
		server_status = get_status()
		indicator.set_menu(build_menu())
		notify.Notification.new("<b>Notification</b>", 'Server status changed.', None).show()

	# Update current status.
	return True

def build_menu():
	global server_status
	menu = gtk.Menu()

	##########################################################
	# Survival
	submenu_survival = gtk.Menu()
	item_start_survival = gtk.MenuItem('Start server')
	item_start_survival.connect('activate', start_server, "survival")

	item_stop_survival = gtk.MenuItem('Stop server')
	item_stop_survival.connect('activate', stop_server, "survival")

	show_logs_survival = gtk.MenuItem('Show logs')
	show_logs_survival.connect('activate', show_logs, "survival")

	save_survival = gtk.MenuItem('Create backup')
	save_survival.connect('activate', create_backup, "survival")

	submenu_survival.append(item_start_survival)
	submenu_survival.append(item_stop_survival)
	submenu_survival.append(show_logs_survival)
	submenu_survival.append(save_survival)

	item_survival = gtk.MenuItem(server_status["survival"] + "Survival-Server" )
	item_survival.set_submenu(submenu_survival)
	menu.append(item_survival)


	##########################################################
	# PANGEA

	submenu_pangea = gtk.Menu()
	item_start_pangea = gtk.MenuItem('Start server')
	item_start_pangea.connect('activate', start_server, "pangea")

	item_stop_pangea = gtk.MenuItem('Stop server')
	item_stop_pangea.connect('activate', stop_server, "pangea")

	show_logs_pangea = gtk.MenuItem('Show logs')
	show_logs_pangea.connect('activate', show_logs, "pangea")

	save_pangea = gtk.MenuItem('Create backup')
	save_pangea.connect('activate', create_backup, "pangea")

	submenu_pangea.append(item_start_pangea)
	submenu_pangea.append(item_stop_pangea)
	submenu_pangea.append(show_logs_pangea)
	submenu_pangea.append(save_pangea)

	item_pangea = gtk.MenuItem(server_status["pangea"] + 'Pangea-Server')
	item_pangea.set_submenu(submenu_pangea)
	menu.append(item_pangea)


	##########################################################
	# Test

	submenu_test = gtk.Menu()
	item_start_test = gtk.MenuItem('Start server')
	item_start_test.connect('activate', start_server, "test")

	item_stop_test = gtk.MenuItem('Stop server')
	item_stop_test.connect('activate', stop_server, "test")

	show_logs_test = gtk.MenuItem('Show logs')
	show_logs_test.connect('activate', show_logs, "test")

	save_test = gtk.MenuItem('Create backup')
	save_test.connect('activate', create_backup, "test")

	submenu_test.append(item_start_test)
	submenu_test.append(item_stop_test)
	submenu_test.append(show_logs_test)
	submenu_test.append(save_test)

	item_test = gtk.MenuItem(server_status["test"] + 'Test-Server')
	item_test.set_submenu(submenu_test)
	menu.append(item_test)

	# Joke
	item_joke = gtk.MenuItem('Random joke :D')
	item_joke.connect('activate', joke)
	menu.append(item_joke)
	menu.append(gtk.SeparatorMenuItem())

	# Update
	item_update = gtk.MenuItem('Update mc-controller!  (^.^)')
	item_update.connect('activate', update)
	menu.append(item_update)

	# Quit
	item_quit = gtk.MenuItem('Quit!  :<')
	item_quit.connect('activate', quit)
	menu.append(item_quit)

	menu.show_all()
	return menu

def fetch_joke():
	request = Request('http://api.icndb.com/jokes/random?limitTo=[nerdy]')
	response = urlopen(request)
	joke = json.loads(response.read())['value']['joke']
	return joke

def joke(_):
	notify.Notification.new("<b>Joke</b>", fetch_joke(), None).show()

def start_server(_, server):
	notify.Notification.new("<b>Notification</b>", 'Server '+ server+ ' wird gestartet.', None).show()
	linux_cmd = 'ssh robin@grapefruit.vingu.online make start_' + server
	os.system("gnome-terminal -e '" + linux_cmd + "'")

def stop_server(_, server):
	notify.Notification.new("<b>Notification</b>", 'Server '+ server + ' wird gestoppt.', None).show()
	linux_cmd = 'ssh robin@grapefruit.vingu.online make stop_' + server
	os.system("gnome-terminal -e '" + linux_cmd + "'")

def show_logs(_, server):
	notify.Notification.new("<b>Notification</b>", 'Zeige server logs von ' + server + '', None).show()
	linux_cmd = 'ssh robin@grapefruit.vingu.online make show_logs_' + server
	os.system("gnome-terminal -e '" + linux_cmd + "'")

def update(_):
	notify.Notification.new("<b>Notification</b>", 'Aktualisiere...', None).show()
	default_path = os.getcwd()
	process_id = os.getpid()
	os.chdir(default_path + "/../")
	os.system("gnome-terminal -e " + 'git pull origin master && cd src/ && python mc-controller.py &')
	os.chdir(default_path)
	os.system("kill " + str(process_id))

def create_backup(_, server):
	default_path = os.getcwd()
	os.chdir("/home")
	dialog = gtk.FileChooserDialog("Select folder to create a backup of "+ server + "-server!", 
		None, gtk.FileChooserAction.SAVE,
		(gtk.STOCK_CANCEL, gtk.ResponseType.CANCEL,
			gtk.STOCK_SAVE, gtk.ResponseType.OK))

	dialog.set_default_response(gtk.ResponseType.OK)

	filter = gtk.FileFilter()
	filter.set_name("All files")
	filter.add_pattern("*")
	dialog.add_filter(filter)

	filter = gtk.FileFilter()
	filter.set_name("Images")
	filter.add_mime_type("image/png")
	filter.add_mime_type("image/jpeg")
	filter.add_mime_type("image/gif")
	filter.add_pattern("*.png")
	filter.add_pattern("*.jpg")
	filter.add_pattern("*.gif")
	filter.add_pattern("*.tif")
	filter.add_pattern("*.xpm")
	dialog.add_filter(filter)

	response = dialog.run()

	if response == gtk.ResponseType.OK:
		os.chdir(default_path)
		notify.Notification.new("<b>Notification</b>", 'Backup wird erstellt für ' + server + '', None).show()
		linux_cmd = ""
		if server == "survival":
			linux_cmd = 'rsync -r -v --progress robin@grapefruit.vingu.online:/srv/minecraft-surv ' + str(dialog.get_filename())

		if server == "pangea":
			linux_cmd = 'rsync -r -v --progress robin@grapefruit.vingu.online:/srv/minecraft-prod ' + str(dialog.get_filename())

		if server == "test":
			linux_cmd = 'rsync -r -v --progress robin@grapefruit.vingu.online:/srv/minecraft-test ' + str(dialog.get_filename())
		
		# Execute command to backup
		state = os.system("gnome-terminal -e '" + linux_cmd + "'")
		if state == 0:
			notify.Notification.new("<b>Notification</b>", 'Backup für ' + server + ' wurde erfolgreich erstellt.', None).show()
		else:
			notify.Notification.new("<b>Notification</b>", 'Backup für ' + server + ' konnte nicht erstellt werden.', None).show()

	elif response == gtk.ResponseType.CANCEL:
		os.chdir(default_path)
		notify.Notification.new("<b>Notification</b>", 'Backup für ' + server + ' wurde nicht erstellt.', None).show()


	dialog.destroy()

def quit(_):
	notify.Notification.new("<b>Notification</b>", 'mc-controller wird beendet.', None).show()
	notify.uninit()
	gtk.main_quit()


def get_status():
	global IP
	global SURVIVAL_PORT
	global PANGEA_PORT
	global TEST_PORT

	output = {}
	on_string = "» [on ]\t"
	off_string = "» [off]\t"
	if not os.system("nc " + IP + " " + PANGEA_PORT + " < /dev/null"):
		output["pangea"] = on_string
	else:
		output["pangea"] = off_string

	if not os.system("nc " + IP + " " + SURVIVAL_PORT + " < /dev/null"):
		output["survival"] = on_string
	else:
		output["survival"] = off_string

	if not os.system("nc " + IP + " " + TEST_PORT + " < /dev/null"):
		output["test"] = on_string
	else:
		output["test"] = off_string

	return output

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()