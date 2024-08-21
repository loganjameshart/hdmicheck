import subprocess
from getpass import getuser
import time

USER = getuser()
DISPLAY_LOG = f"/home/{USER}/xchange.log"

# get on startup
def startup_display_detection():
	proc = subprocess.run(["xrandr", "--listactivemonitors"], text=True, stdout=subprocess.PIPE)
	with open(f"/home/{USER}/xchange.log", "w") as display_logfile:
		display_logfile.write(proc.stdout)


def update_config():
	with open(f"/home/{USER}/.config/display.conf", "w") as display_config:
		display_config.write("x=480\ny=720")


def display_daemon(logfile_path):
	with open(logfile_path) as logfile:
		current_display_status = logfile.read()
	while True:
		proc = subprocess.run(["xrandr", "--listactivemonitors"], text=True, stdout=subprocess.PIPE)
		if proc.stdout != current_display_status:
			update_config()
			print("Updated config.")
		time.sleep(2)


if __name__ == "__main__":
	startup_display_detection()
	display_daemon(DISPLAY_LOG)
