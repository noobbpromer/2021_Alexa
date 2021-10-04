# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import json
import random
import os
import re
import sys
# import pandas
# import ask_sdk_core.utils as ask_utils

from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.skill_builder import SkillBuilder
# from ask_sdk_core.dispatch_components import AbstractRequestHandler
# from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.dispatch_components import (AbstractRequestHandler, AbstractExceptionHandler, AbstractRequestInterceptor, AbstractResponseInterceptor)
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# question_data = json.loads(open('question_data.json').read())
accident_data = json.loads(open('car_accident.json').read())
greet_data = json.loads(open('greet.json').read())
injuries_data=json.loads(open('injuries.json').read())
counter=222

def listToString(s):  
    
    # initialize an empty string 
    str1 = ""  
    
    # traverse in the string   
    for ele in s:  
        str1 += ele 
    
    # return string   
    return str1 

def check_phase(from_user, in_json):
    str_value=""
    list_value=[]
    # 先后顺序
    for item in in_json:
        if re.search(r"\b{}\b".format(item), from_user.strip()):
            str_value=str_value+" "+item
            
    
    return str_value



class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        session_attributes["if_enter"] = 0
        
        for greet  in greet_data['GREETING']:
            
            speak_output=(greet['greet'])
            

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class LocationIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        
        return is_intent_name("LocationIntent")(handler_input) 

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        # quiz_started = session_attributes["quiz_started"]
        slots = handler_input.request_envelope.request.intent.slots
        
        location = slots["location"].value
        prepositions=slots["prepositions"].value
        someone=slots["someone"].value
        # s1=slots["someone"].confirmationStatus
        verb=slots["verb"].value
        incident=slots["incident"].value
        
        # the user not give alexa location
        if (location ==None) :
            current_question_index = 0
            session_attributes["if_enter"] = 1
            
            question = accident_data[current_question_index]["q"]
            speak_output = ("{}").format(question)
            
            if (someone ==None) or (verb ==None) or (incident ==None):
                
                for reply in greet_data['NOT_FULL_SENTENCE']:
                    
                    speak_output= (reply['reply'])
                    
                # speak_output = ("I'm sorry, I didn't get that. if you have emergency, Could you please tell me what the incident was again?")
        
        counter = session_attributes["if_enter"]
        
        if (location !=None) :
            current_question_index = 1
            
            question = accident_data[current_question_index]["q"]
            speak_output = ("{prepositions} {location} ? {}").format(question,prepositions=prepositions,location=location)
            

            if ((someone ==None) or (verb ==None) or (incident ==None)) :
                
                current_question_index = 2
                question = accident_data[current_question_index]["q"]
                speak_output = ("{prepositions} {location} ? {}").format(question,prepositions=prepositions,location=location)
                
                if(counter==0):
                    for reply in greet_data['FIRST_ENTER_ERROR']:
                        
                        speak_output=(reply['reply'])
                    

        session_attributes["current_question_index"] = current_question_index
        session_attributes["question"] = question
        
        quiz_started=True
        
        return (
            
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
                
                
        )

# class AnswerIntentHandler(AbstractRequestHandler):
#     """Handler for Help Intent."""
#     def can_handle(self, handler_input):
#         # type: (HandlerInput) -> bool
#         return is_intent_name("AnswerIntent")(handler_input)

#     def handle(self, handler_input):
#         # type: (HandlerInput) -> Response
#         session_attributes = handler_input.attributes_manager.session_attributes
#         slots = handler_input.request_envelope.request.intent.slots
#         # answer = slots["answer"].value 
#         current_question_index = session_attributes["current_question_index"] + 2
#         if current_question_index < 5:
#             question = accident_data[current_question_index]["q"]
#             speak_output = (" {}").format(question)
#             session_attributes["current_question_index"] = current_question_index
#             session_attributes["question"] = question 
    
#         return (
#             handler_input.response_builder
#                 .speak(speak_output)
#                 .ask(speak_output)
#                 .response
#         )

class InjuriesIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("InjuriesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attributes = handler_input.attributes_manager.session_attributes
        slots = handler_input.request_envelope.request.intent.slots
        
        # situation=slots["situation"].value
        word_list=[]
        subject_list=[]
        what_happen=slots["what_happen"].value
        str_what_happen=listToString(what_happen)
        
        
            
        subject_list=injuries_data["subject"]
        verb_list=injuries_data["verb"]
        status_list=injuries_data["status"]
        
        str_subject=listToString(subject_list)
        
        subject=check_phase(what_happen,subject_list)
        verb=check_phase(what_happen,verb_list)
        status=check_phase(what_happen,status_list) 
        
        # subject= list(subject.split(" "))
        # verb= list(verb.split(" "))
        # status=list(status.split(" "))
        
        to_speak=subject+verb+status
        
        
        speak_output=("{subject},{verb},{status}").format(subject=subject,verb=verb,status=status)
        
        # speak_output=("{subject} ").format(subject=subject)
        



            
        # speak_output=("{str_what_happen} {subject_list}").format(str_what_happen=str_what_happen,subject_list=subject_list)
            
        # speak_output = ("{word_list}").format(word_list=word_list)
            

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class OutlookIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("OutlookIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        
        session_attributes = handler_input.attributes_manager.session_attributes
        # quiz_started = session_attributes["quiz_started"]
        slots = handler_input.request_envelope.request.intent.slots
        car_color = slots["car_color"].value
        car_type = slots["car_type"].value
        speak_output = ("OK, {car_color} {car_type}").format(car_color=car_color, car_type=car_type)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )
    
class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )




class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (is_intent_name("AMAZON.CancelIntent")(handler_input) or
                is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.




sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
# sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(OutlookIntentHandler())
sb.add_request_handler(InjuriesIntentHandler())
sb.add_request_handler(LocationIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())
lambda_handler = sb.lambda_handler()