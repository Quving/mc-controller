# This code is an example for a tutorial on Ubuntu Unity/Gnome AppIndicators:
# http://candidtim.github.io/appindicator/2014/09/13/ubuntu-appindicator-step-by-step.html

import os, signal 
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
	submenu = gtk.Menu()
	submenu.append(gtk.MenuItem('Bat'))
	item_submenu = gtk.MenuItem('item_submenu')
	item_submenu.set_submenu(submenu)
	menu.append(item_submenu)


	# Joke
	item_joke = gtk.MenuItem('Joke')
	item_joke.connect('activate', joke)
	menu.append(item_joke)

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
	os.system("gnome-terminal -e 'sleep 2'")


def quit(_):
	notify.uninit()
	gtk.main_quit()

if __name__ == "__main__":
	signal.signal(signal.SIGINT, signal.SIG_DFL)
	main()