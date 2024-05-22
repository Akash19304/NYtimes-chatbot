# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

import requests, json

from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionHelloWorld(Action):

    def name(self) -> Text:
        return "action_hello_world"   #action_action_name

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        print("I have got a request from nlu")

        dispatcher.utter_message(text="Hello World!")

        return []
    

class NYTimesAction(Action):

    def name(self) -> Text:
        return "action_get_news"   

    def run(self, 
            dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        category = tracker.get_slot('news_category')
        print(f"Identified News category is {category}")
        
        url = 'https://api.nytimes.com/svc/news/v3/content/all/{category}.json'.format(category=category)
        params = {'api-key': "QR1WpjPRM49jBYGvL2603z8nMlC9awIj", 'limit': 5}

        response = requests.get(url, params=params).text

        json_data = json.loads(response)["results"]

        counter = 0
        for each_news in json_data:
            counter += 1
            output_msg = f"{str(counter)}. {each_news['title']} -- under the section {each_news['section']} -- published on {each_news['published_date']}"

            dispatcher.utter_message(text=output_msg)

        return []
