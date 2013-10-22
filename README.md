# Updating using cron
Add a line like

	0 21 * * * /home/ckuijjer/src/starred_tweets/update_starred_tweets.sh

to cron using e.g. crontab -e to auto update the starred tweets every day at 21
