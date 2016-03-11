import time
import unicodedata
from slackutil.slackbot_handler import slackbot_handler

class google_tz_handler(slackbot_handler):
    def __init__(self, config):
        super(google_tz_handler, self).__init__(config)
        self._google_token = config.get('Google', 'google_token')

    def get_handler_name(self):
        return 'Google Time Zone'

    def get_commands_and_examples(self):
        return (['Obtains current time in specified places or time zones.'], ['sm tz San Jose, CA'])

    def can_handle(self, fulltext, tokens, edited):
        return tokens[1] == 'tz'

    def handle(self, fulltext, tokens, slackclient, channel, user):
        del tokens[0]
        del tokens[0]
        if tokens:
            cities = self.get_cities('+'.join(tokens))
            if (cities):
                if len(cities) == 0:
                    slackclient.post_message(channel, 'No such place found')
                else:
                    output = ''
                    for city in cities:
                        city_string = unicodedata.normalize('NFKD', city['address']).encode('ascii','ignore')
                        output += 'Local time at *' + city_string + '* is `' + self.get_local_time(city) + '`\n'
                    slackclient.post_message(channel, output)
            else:
                slackclient.post_message(channel, 'No such place found')
        else:
            slackclient.post_message(channel, 'Missing place name')

    def get_cities(self, city):
        try:
            response = self._get_json_data_through_rest_get('https://maps.googleapis.com/maps/api/geocode/json?address=' + city + '&key=' + self._google_token)
            if response and response['status'] == 'OK':
                ret = []
                for result in response['results']:
                    new_city = {}
                    new_city['address'] = result['formatted_address']
                    new_city['latitude'] = result['geometry']['location']['lat']
                    new_city['longitude'] = result['geometry']['location']['lng']
                    ret.append(new_city)
                return ret
            else:
                return None
        except Exception as e:
            return None

    def get_raw_local_time(self, city, t):
        try:
            response = self._get_json_data_through_rest_get('https://maps.googleapis.com/maps/api/timezone/json?location=' + str(city['latitude']) + ',' + str(city['longitude']) + '&timestamp=' + str(t) + '&key=' + self._google_token)
            if response and response['status'] == 'OK':
                local_time = t + response['dstOffset'] + response['rawOffset']
                return local_time
            else:
                return None
        except Exception as e:
            return None

    def get_local_time(self, city, t = int(time.time())):
        return time.asctime(time.gmtime(self.get_raw_local_time(city, t))) 
