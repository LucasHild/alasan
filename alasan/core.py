from .event import Event
from .errors import IntentNotFound


class Alasan:
    def __init__(self):
        self.launch_function = lambda x: {}
        self.intent_functions = {}
        self.on_session_ended_function = lambda x: {}

    def __call__(self, event_dict, context):
        print("IN:", event_dict)

        event = Event(event_dict)

        if event.request.type == "LaunchRequest":
            response = self.launch_function(event)

        elif event.request.type == "IntentRequest":
            if event.request.intent.name not in self.intent_functions.keys():
                raise IntentNotFound

            response = self.intent_functions[event.request.intent.name](event)

        elif event.request.type == "SessionEndedRequest":
            response = self.on_session_ended_function(event)

        print("OUT:", response)
        return response

    def launch(self):
        def wrap(f):
            self.launch_function = f
            return f

        return wrap

    def intent(self, intent_name):
        def wrap(f):
            self.intent_functions[intent_name] = f
            return f

        return wrap

    def on_session_ended(self):
        def wrap(f):
            self.on_session_ended_function = f
            return f

        return wrap
