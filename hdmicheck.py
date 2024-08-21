#!/usr/bin/env python3

import subprocess
from getpass import getuser
import time

USER = getuser()
DISPLAY_LOG = f"/home/{USER}/xchange.log"
CONFIG_PATH = f"/home/{USER}/.config/display.conf"
CONFIG_PARAMETERS = "x=480\ny=720"


def startup_display_detection() -> None:
	"""Gets status of current displays."""
	proc = subprocess.run(["xrandr", "--listactivemonitors"], text=True, stdout=subprocess.PIPE)
	with open(f"/home/{USER}/xchange.log", "w") as display_logfile:
		display_logfile.write(proc.stdout)


def update_config(config_path: str, config_parameters: str) -> None:
	"""Updates target config file with chosen instructions."""
	with open(CONFIG_PATH, "w") as display_config:
		display_config.write(CONFIG_PARAMETERS)


def display_daemon(logfile_path: str) -> None:
	"""Checks for changes to original display logfile, and makes config file update if need be."""
	while True:
		with open(logfile_path) as logfile:
			current_display_status = logfile.read()

		proc = subprocess.run(["xrandr", "--listactivemonitors"], text=True, stdout=subprocess.PIPE)
		if proc.stdout != current_display_status:
			update_config()
			print("Updated config.")
			with open(f"/home/{USER}/xchange.log", "w") as display_logfile: # update the file with the new status
				display_logfile.write(proc.stdout)
		
		time.sleep(2)


if __name__ == "__main__":
	startup_display_detection()
	display_daemon(DISPLAY_LOG)
