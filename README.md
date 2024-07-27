# inky-check-ical-neopixel
This script checks City of Regina iCal for 3 collection type events. If the event is today or tomorrow turn on the neopixel.

## Setup cronjob
Add to root, neopixel requires root.
```
sudo crontab -e
```

Run job every day at minute 0 past hour 0 and 12.
```
0 0,12 * * * root bash /home/pi/projects/inky-check-ical-neopixel/check-city.sh >/dev/null 2>&1
```

### pip notes
```
pip3 install pipreqs
python3 -m  pipreqs.pipreqs .
pip3 install -r requirements.txt
```