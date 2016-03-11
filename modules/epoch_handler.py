import sys
import time
from sets import Set
from slackutil.slackbot_handler import slackbot_handler

class epoch_handler(slackbot_handler):
    def __init__(self, config):
        super(epoch_handler, self).__init__(config)
        self._additional_location = self._config.get('Epoch', 'additional_location')

    def get_handler_name(self):
        return 'Epoch'

    def get_commands_and_examples(self):
        return (['slacker can also do epoch-to-time conversions.'], ['slacker 1456184562'])

    def can_handle(self, fulltext, tokens, edited):
        possible_epoch_list = fulltext.split(' ', 1)
        epoch_string = possible_epoch_list[1].strip()
        self._epoch = None
        if not set(epoch_string).issubset(set('0123456789')):
            epoch_string = None
        if epoch_string:
            epoch = int(epoch_string)
            if 1000000000 <= epoch <= 3000000000:
                self._epoch = epoch
        return self._epoch

    def handle(self, fulltext, tokens, slackclient, channel, user):
        slackclient.post_message(channel, 'UTC: `' + time.strftime('%Y/%m/%d-%H:%M:%S', time.gmtime(self._epoch)) + '`')
        if self._additional_location and 'modules.google_tz_handler' in sys.modules:
            handler_module = sys.modules['modules.google_tz_handler']
            handler_class = getattr(handler_module, 'google_tz_handler')
            handler_instance = handler_class(self._config)
            slackclient.post_message(channel, self._additional_location + ': `' + time.strftime('%Y/%m/%d-%H:%M:%S', time.gmtime(handler_instance.get_raw_local_time(handler_instance.get_cities(self._additional_location.replace(' ', '+'))[0], self._epoch))) + '`')
