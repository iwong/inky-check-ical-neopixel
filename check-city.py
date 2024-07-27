import requests
from icalendar import Calendar
from datetime import datetime, timedelta
import board
import neopixel

# Configuration
ICAL_URL = 'https://recollect.a.ssl.fastly.net/api/places/DD53433C-7EDC-11E8-B7D6-AA1A2925712F/services/218/events.en.ics?client_id=13B7C5A4-8F5C-11EC-A6BB-EF58BD83BBD5'  # Replace with your iCal URL
NUM_PIXELS = 1  # Number of NeoPixels
PIN = board.D18  # GPIO pin connected to NeoPixels (board.D18 for GPIO18)
ORDER = neopixel.GRB  # Pixel color order

# NeoPixel setup
strip = neopixel.NeoPixel(PIN, NUM_PIXELS, auto_write=False, pixel_order=ORDER, brightness=0.1)

def turn_on_neopixel(color):
    """Turn on the NeoPixel to the given color."""
    for i in range(NUM_PIXELS):
        strip[i] = color
    strip.show()

def get_tomorrow_events(ical_url):
    """Fetch iCal data and return events for tomorrow."""
    response = requests.get(ical_url)
    calendar = Calendar.from_ical(response.content)
        
    #now = datetime.now() + timedelta(days=10)
    now = datetime.now()
    today_start = datetime(now.year, now.month, now.day)
    tomorrow_start = today_start + timedelta(days=1)
    tomorrow_end = tomorrow_start + timedelta(days=1)

    events = []
    for component in calendar.walk():
        if component.name == "VEVENT":
            start = datetime.combine(component.get('dtstart').dt, datetime.min.time())
            
            if isinstance(start, datetime) and (today_start <= start < tomorrow_start or tomorrow_start <= start < tomorrow_end):
                summary = component.get('summary')
                if summary:
                    summary_lower = summary.lower()
                    if 'garbage' in summary_lower:
                        #print('garbage')
                        return (32, 16, 0)  # Brown
                    elif 'food and yard waste' in summary_lower:
                        #print('food and yard waste')
                        return (0, 32, 0)  # Green
                    elif 'recycling' in summary_lower:
                        #print('recycling')
                        return (0, 0, 32)  # Blue
    
    return (0, 0, 0)  # Turn off NeoPixel (off)

def main():
    color = get_tomorrow_events(ICAL_URL)
    if color != (0, 0, 0):
        print("Relevant event found for today or tomorrow. Turning on NeoPixel.")
    else:
        print("No relevant event found for today or tomorrow.")

if __name__ == '__main__':
    main()
