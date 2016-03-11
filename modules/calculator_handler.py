from slackutil.slackbot_handler import slackbot_handler

class calculator_handler(slackbot_handler):
    def __init__(self, config):
        super(calculator_handler, self).__init__(config)

    def get_handler_name(self):
        return 'Calculator'

    def get_commands_and_examples(self):
        return (['<mathematical expression>'], ['slacker (75.0 - 32) * 5/9'])

    def can_handle(self, fulltext, tokens, edited):
        possible_calc_list = fulltext.split(' ', 1)
        self._calc_string = possible_calc_list[1].strip()
        if not set(self._calc_string).issubset(set(' 0123456789().+-*/')):
            self._calc_string = None
        return self._calc_string

    def handle(self, fulltext, tokens, slackclient, channel, user):
        try:
            expression = eval(self._calc_string, {"__builtins__":None})
            slackclient.post_message(channel, str(expression))
        except SyntaxError as e:
            slackclient.post_message(channel, 'Syntax error: ' + self._calc_string)
        except ZeroDivisionError as e:
            nice_try = ''
            if '/0' in text:
                nice_try = 'nice try, result: '
            slackclient.post_message(channel, nice_try + 'undefined')
