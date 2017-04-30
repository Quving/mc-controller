# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os, signal, gi

gi.require_version('Gtk', '3.0')
gi.require_version('Notify', '0.7')
gi.require_version('AppIndicator3', '0.1')

import json

from urllib2 import Request, urlopen, URLError

from gi.repository import Gtk as gtk
from gi.repository import AppIndicator3 as appindicator
from gi.repository import Notify as notify


APPINDICATOR_ID = 'McController'

def main():
	indicator = appindicator.Indicator.new(APPINDICATOR_ID, 
		os.path.abspath('../icon/minecraft.png'), 
		appindicator.IndicatorCategory.SYSTEM_SERVICES)

	indicator.set_status(appindicator.IndicatorStatus.ACTIVE)
	indicator.set_menu(build_menu())
	notify.init(APPINDICATOR_ID)
	gtk.main()

def build_menu():
	menu = gtk.Menu()

	##########################################################
	# Survival
	submenu_survival = gtk.Menu()
	item_start_survival = gtk.MenuItem('Start!')
	item_start_survival.connect('activate', start_survival)

	item_stop_survival = gtk.MenuItem('Stop!')
	item_stop_survival.connect('activate', stop_survival)


	submenu_survival.append(item_start_survival)
	submenu_survival.append(item_stop_survival)
	item_survival = gtk.MenuItem('Survival-Server')
	item_survival.set_submenu(submenu_survival)
	menu.append(item_survival)

	##########################################################
	# PANGEA
	submenu_pangea = gtk.Menu()
	item_start_pangea = gtk.MenuItem('Start!')
	item_start_pangea.connect('activate', start_pangea)

	item_stop_pangea = gtk.MenuItem('Stop!')
	item_stop_pangea.connect('activate', stop_pangea)

	submenu_pangea.append(item_start_pangea)
	submenu_pangea.append(item_stop_pangea)
	item_pangea = gtk.MenuItem('Pangea-Server')
	item_pangea.set_submenu(submenu_pangea)
	menu.append(item_pangea)

	##########################################################
	# Test

	submenu_test = gtk.Menu()
	item_start_test = gtk.MenuItem('Start!')
	item_start_test.connect('activate', start_test)

	item_stop_test = gtk.MenuItem('Stop!')
	item_stop_test.connect('activate', stop_test)

	submenu_test.append(item_start_test)
	submenu_test.append(item_stop_test)
	item_test = gtk.MenuItem('Test-Server')
	item_test.set_submenu(submenu_test)
	menu.append(item_test)


	# Joke
	item_joke = gtk.MenuItem('Joke')
	item_joke.connect('activate', joke)
	menu.append(item_joke)

	# Update
	item_update = gtk.MenuItem('Update')
	item_update.connect('activate', update)
	menu.append(item_update)

	# Quit
	item_quit = gtk.MenuItem('Quit')
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
	
def start_survival(_):
	notify.Notification.new("<b>Notication</b>", 'Server Survival wird gestartet.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make start_survival'")

def stop_survival(_):
	notify.Notification.new("<b>Notication</b>", 'Server Survival wird gestoppt.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make stop_survival'")

def start_pangea(_):
	notify.Notification.new("<b>Notication</b>", 'Server Pangea wird gestartet.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make start_pangea'")

def stop_pangea(_):
	notify.Notification.new("<b>Notication</b>", 'Server Pangea wird gestoppt.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make stop_pangea'")

def start_test(_):
	notify.Notification.new("<b>Notication</b>", 'Server Test wird gestartet.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make start_test'")

def stop_test(_):
	notify.Notification.new("<b>Notication</b>", 'Server Test wird gestoppt.', None).show()
	os.system("gnome-terminal -e 'ssh robin@grapefruit.vingu.online make stop_test'")

def update(_):
	notify.Notification.new("<b>Notication</b>", 'Aktualisiere...', None).show()
	default_path = os.getcwd()
	process_id = os.getpid()
	os.chdir(default_path + "/../")
	os.system("gnome-terminal -e " + 'pwd && git pull origin master && cd src/ && python mc-controller.py &')
	os.system("kill " + str(process_id))
	os.chdir(default_path)



def quit(_):
	notify.uninit()
	gtk.main_quit()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()