import logging
import random
from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.utils import is_request_type, is_intent_name
from ask_sdk_core.handler_input import HandlerInput
from ask_sdk_model.ui import SimpleCard
from ask_sdk_model import Response
#ask_sdk_core.attributes_manager.AbstractPersistenceAdapter
sb =SkillBuilder()

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

SKILL_NAME = "CricVerbal"

data_out = [
  'Bowled!','out!','L.B.W. !','Run Out!','It was a Catch!','You are Stumped!','Outzaatt!!!','Hit Wicket!',' ',]

data_six = [
  'Boundary!','What a shot!',' ',]

data_win = [
  'Congratulation!', 'Bravo!', 'Hurray!', 'Yippie!', ' ',]


#expressions for winning or losing
#six or four

@sb.request_handler(can_handle_func=is_request_type("LaunchRequest"))
def launch_request_handler(handler_input):
	"""Handler for Skill Launch."""
	# type: (HandlerInput) -> Response
	speech_text = "Welcome to Cricverbal. You can choose to Bat or Ball first"
	attr = handler_input.attributes_manager.session_attributes
	attr["user_choice"]=int(0)
	attr["user_score"]=int(0)
	attr["alexa_score"]=int(0)
	attr["user_state"]=0	# 0 for first bat, 1 for second bat
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("PlayCricverbalIntent"))
def play_request_handler(handler_input):
	"""Handler for Skill Launch."""
	# type: (HandlerInput) -> Response
	attr = handler_input.attributes_manager.session_attributes
	attr["user_choice"]=int(0)
	attr["user_score"]=int(0)
	attr["alexa_score"]=int(0)
	attr["user_state"]=0	# 0 for first bat, 1 for second bat
	speech_text = "Welcome to Cricverbal. You can choose to Bat or Ball first"
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("PlayAgainIntent"))
def play_again_request_handler(handler_input):
    """Handler for Skill Launch."""
    # type: (HandlerInput) -> Response
    attr = handler_input.attributes_manager.session_attributes
    attr["user_choice"]=int(0)
    attr["user_score"]=int(0)
    attr["alexa_score"]=int(0)
    attr["user_state"]=0	# 0 for first bat, 1 for second bat
    speech_text = "Great! You can again choose to Bat or Ball first"
    return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("BatIntent"))
def bat_response_handler(handler_input):
	"""Handler to start batting"""
	# type: (HandlerInput) -> Response
	attr = handler_input.attributes_manager.session_attributes
	attr["user_choice"]=int(1)
	speech_text = "Great Choice! You are batting now. Start saying a random number between 1 and 6"
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("BallIntent"))
def ball_response_handler(handler_input):
	"""Handler to start batting"""
	# type: (HandlerInput) -> Response
	attr = handler_input.attributes_manager.session_attributes
	attr["user_choice"]=int(0)
	speech_text = "Great Choice! You are balling now. Start saying a random number between 1 and 6"
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response

@sb.request_handler(can_handle_func=is_intent_name("NumberIntent"))
def batting_handler(handler_input):
	"""Handler for batting or balling"""
	# type: (HandlerInput) -> Response
	random_out=random.choice(data_out)
	random_six=random.choice(data_six)
	random_win=random.choice(data_win)
	random_number=int(random.randint(1,6))
	attr = handler_input.attributes_manager.session_attributes
	slots = handler_input.request_envelope.request.intent.slots
	number_user = slots["number"].value
	attr["NUMBER"] = number_user
	bat_or_ball=attr.get("user_choice")
	if (int(number_user)<1 or int(number_user)>6):
		speech_text="You are supposed to choose number between 1 and 6"
	elif (bat_or_ball==1):
		if (random_number == int(number_user)):
			speech_text = random_out + " I also threw "+str(random_number) + ". You are out with score {} .".format(str(attr.get("user_score")))
			if (attr.get("user_state")==0): 
				attr["user_choice"]=int(0)
				speech_text+="Now its your turn to bowl. Start balling by saying random number between 1 and 6"
				attr["user_state"]=1
			else :
				if (attr.get("user_score")>attr.get("alexa_score")):
					speech_text+= random_win + " You won by "+ str(attr.get("user_score")-(attr.get("alexa_score")))+" runs."
				elif (attr.get("user_score")==attr.get("alexa_score")):
					speech_text+=" Its a draw!"
				else:
					speech_text+=" You lost by "+ str(-(attr.get("user_score"))+(attr.get("alexa_score")))+" runs."
				speech_text+=" Would you like to play again?"
				return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response
		else:
			if (int(number_user)==4 or int(number_user)==6):
				speech_text = random_six + ".I threw "+str(random_number)+". Continue Batting... " 
			else :
				speech_text = "I threw "+str(random_number)+". Continue Batting..."
			attr["user_score"]=int(attr.get("user_score"))+int(number_user)
			if (attr.get("user_state")==1 and attr.get("user_score")>attr.get("alexa_score")):
				speech_text="I threw "+str(random_number)+". " + random_win + " You won!"
				speech_text+=" Would you like to play again?" 

	elif(bat_or_ball==0):			
			if (random_number==int(number_user)):
				speech_text= "Oh no! I also threw "+str(random_number)+". I am out with score "+str(attr.get("alexa_score"))+" ."
				if (attr.get("user_state")==0): 
					attr["user_choice"]=int(1)
					speech_text+=" Now its your turn to bat. Start batting by saying a random number between 1 and 6."
					attr["user_state"]=1
				else :
					if (attr.get("user_score")>attr.get("alexa_score")):
						speech_text+= random_win+" You won by "+ str(attr.get("user_score")-(attr.get("alexa_score")))+" runs."
					elif (attr.get("user_score")==attr.get("alexa_score")):
						speech_text+=" Its a draw!"
					else:
						speech_text+="You lost by "+ str(-(attr.get("user_score"))+(attr.get("alexa_score")))+" runs."
					speech_text+=" Would you like to play again?"
					return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response
			else:
				speech_text="I scored " + str(random_number)+". Continue bowling..."
				attr["alexa_score"]=attr.get("alexa_score")+random_number
				if (attr.get("user_state")==1 and attr.get("user_score")<attr.get("alexa_score")):
					speech_text="I threw "+str(random_number)+". You lost!"
					speech_text+=" Would you like to play again?"
	
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(False).response
	
@sb.request_handler(can_handle_func=is_intent_name("DontPlayAgainIntent"))
def dontplayagain_handler(handler_input):
	"""Handler to not play again"""
	# type: (HandlerInput) -> Response
	speech_text="See you next time! Goodbye!"
	return handler_input.response_builder.speak(speech_text).set_card(SimpleCard(SKILL_NAME, speech_text)).set_should_end_session(True).response
	




#################################################################################
@sb.request_handler(can_handle_func=is_intent_name("AMAZON.HelpIntent"))
def help_intent_handler(handler_input):
    """Handler for Help Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "You can play cricket with me! The rules are simple....If you and I choose same number, the person batting is out! Otherwise, we will continue playing. Try saying play cricket."

    return handler_input.response_builder.speak(speech_text).ask(
        speech_text).set_card(SimpleCard(
            SKILL_NAME, speech_text)).response


@sb.request_handler(
    can_handle_func=lambda handler_input:
        is_intent_name("AMAZON.CancelIntent")(handler_input) or
        is_intent_name("AMAZON.StopIntent")(handler_input))
def cancel_and_stop_intent_handler(handler_input):
    """Single handler for Cancel and Stop Intent."""
    # type: (HandlerInput) -> Response
    speech_text = "Goodbye!"

    return handler_input.response_builder.speak(speech_text).set_card(
        SimpleCard(SKILL_NAME, speech_text)).response


@sb.request_handler(can_handle_func=is_intent_name("AMAZON.FallbackIntent"))
def fallback_handler(handler_input):
    """AMAZON.FallbackIntent is only available in en-US locale.
    This handler will not be triggered except in that locale,
    so it is safe to deploy on any locale.
    """
    # type: (HandlerInput) -> Response
    speech = (
        "The CricVerbal skill can't help you with that.  "
        "You can say say Bat or Ball")
    reprompt = "You can say Bat!!"
    handler_input.response_builder.speak(speech).ask(reprompt)
    return handler_input.response_builder.response


@sb.request_handler(can_handle_func=is_request_type("SessionEndedRequest"))
def session_ended_request_handler(handler_input):
    """Handler for Session End."""
    # type: (HandlerInput) -> Response
    return handler_input.response_builder.response


@sb.exception_handler(can_handle_func=lambda i, e: True)
def all_exception_handler(handler_input, exception):
    """Catch all exception handler, log exception and
    respond with custom message.
    """
    # type: (HandlerInput, Exception) -> Response
    logger.error(exception, exc_info=True)

    speech = "Sorry, there was some problem. Please try again!!"
    handler_input.response_builder.speak(speech).ask(speech)

    return handler_input.response_builder.response


lambda_handler = sb.lambda_handler()
