import datetime
from geopy.geocoders import Nominatim
from state_territory_to_abbrev import au_state_territory_to_abbrev, us_state_to_abbrev, ca_state_territory_to_abbrev
from country_to_abbrev import country_to_abbrev

class Event():
  def __init__(self, name, location, date, url, virtual, organizerName, organizerUrl, duplicate=False) -> None:
    self.name = name
    self.location = location
    self.date = date
    self.url = url
    self.virtual = virtual
    self.organizerName = organizerName
    self.organizerUrl = organizerUrl
    self.duplicate = duplicate

  def to_markdown_string(self) -> str:
    if self.virtual:
      return f'* {self.date} | Virtual ({self.location}) | [{self.organizerName}]({self.organizerUrl})\n\t*[**{self.name}**]({self.url})'
    else:
      return f'* {self.date} | {self.location} | [{self.organizerName}]({self.organizerUrl})\n\t*[**{self.name}**]({self.url})'
    
  def format_date(self):
      # Formats datetime data into date.
      if isinstance(self.date, datetime.datetime):
        self.date = self.date.date()

  def format_location(self):
    # Formats location data into (city, +/-state, country).
    geocoder = Nominatim(user_agent="TWiR")
    locationData = str(geocoder.geocode(self.location, language="en")).split(",")
    print(locationData)

    if len(locationData) > 3:
      city, state, country = locationData[2].strip(), locationData[3].strip(), locationData[-1].strip()
      country = country_to_abbrev(country)
      if country in ["AU", "CA", "US"]:
        if country == "AU":
          state = au_state_territory_to_abbrev(state)
        elif country == "CA":
          state = ca_state_territory_to_abbrev(state)
        elif country == "US":
          state = us_state_to_abbrev(state)
        self.location = f'{city}, {state}, {country}'
      else:
        self.location = f'{city}, {country}'
