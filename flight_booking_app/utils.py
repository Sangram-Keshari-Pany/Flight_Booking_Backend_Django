from datetime import datetime
from datetime import timedelta

# THIS FUNCTION IS USED TO GET THE UPCOMMING DATE OF THE PARTICULAR DAY
def GETDATE(DAY):
  days_of_week = {'monday': 0, 'tuesday': 1, 'wednesday': 2, 'thursday': 3, 'friday': 4, 'saturday': 5, 'sunday': 6}
  today = datetime.now()
  today_weekday = today.weekday()

  target_weekday=days_of_week[DAY.lower()]
   
  if target_weekday==today_weekday:
    return today.strftime('%Y-%m-%d')
  else:
    days_until_target = (target_weekday - today_weekday + 7) % 7
    upcoming_date = today + timedelta(days=days_until_target)
    return upcoming_date.strftime('%Y-%m-%d')
