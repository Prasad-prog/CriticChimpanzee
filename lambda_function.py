# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.



import logging
import ask_sdk_core.utils as ask_utils
import random
import os
from ask_sdk_s3.adapter import S3Adapter
s3_adapter=S3Adapter(bucket_name=os.environ['S3_PERSISTENCE_BUCKET'])

from ask_sdk_core.skill_builder import CustomSkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

data=[
    {'Question':"Douglas Engelbert who passed away in 2013, is credited as the inventor of which of these products? A. Mobile Phone, B. Computer Mouse, C. Bluetooth Mouse, D. Digital camera", 'Answer':'option b'},
    {'Question':"Which of these persons has not walked on the Moon? A. Charles Duke, B. James A Lovell, C.  Alan Bean, D. Pete Conrad", 'Answer':'option b'},
    {'Question':"In the Mughal era, which of these harbours was also known as 'Babul Mecca' and 'Meccaidwar'? A. Bharuch, B. Surat, C. Porbandar, D. Khambat", 'Answer':'option b'},
    {'Question':"From which country did India buy an aircraft carrier which was renamed as INS Vikramaditya? A. France, B. Germany, C. England, D. Russia", 'Answer':'option d'},
    {'Question':"Which of these festivals is also known as 'Khichdi Parv' in northern India? A. Makar Sankranti, B. Vaishakhi, C. Vasant Panchami, D. Narak Chaturdashi", 'Answer':'option a'},
    {"Question":"Who is the only Indian to have won a medal in Womens' Singles at the World Badminton Championship? A. Jwala Gupta, B. P V Sindhu, C. Saina Nehwal, D. Ashwini Ponnappa", "Answer":'option b'},
    {"Question":"The end of what service is referred to in this newspaper headline : 'Dot, dash, full stop service ends July 15 '? A. Trunk Call, B. Telegram, C. Post Card, D. Toy Train", "Answer":'option b'},
    {"Question":"Who is the first woman amputee in the world to summit Mount Everest? A. Tashi Malik, B. Raha Moharrak, C. Samina Baig, D. Arunima Sinha", "Answer":'option d'},
    {"Question":"Which of these is a piece of the game called as chess: A. Wazir, B. Nawab, C. Sarpanch, D. Patbari", "Answer":'option a'},
    {"Question":"After whom is the Centigrade system of tempreature measurement named? A. Anders Celsius, B. Daniel Fahrenheit, C. Lord Kelvin, D. Gabriele Centi", "Answer":'option a'},
    {"Question":"Arrange these official positions in India as per their increasing order of people that can occupy these positions at any give point of time. A.Rajya Sabha Member, B. Lok Sabha Member, C. Chief Minister, D.Prime Minister, Options are A. ABCD,B. BCDA, C. DCAB, D. CDAB", "Answer":'option c'},
    {"Question":"To reach which of these places do pilgrims start their journey on foot from Gauri Kund? A. Badrinath, B. Kedarnath, C. Vaishano Devi, D. Amarnath", "Answer":'option b'},
    {"Question":"What is the name of India's first ever indigenous aircraft carrier launched in August 2013? A. INS Viraat, B. INS Shaurya, C. INS chakra, D. INS Vikrant", "Answer":'option d'},
    {"Question":"What disease, ascribed to a deficiency of vitamin B1, gets its name from a Sinhalese word for 'weakness'? A. Anaemia, B. Riboflavin, C. Beriberi, D.Kala-azar", "Answer":'option c'},
    {"Question":"What was the code name of the operation by IPKF to take control of Jaffna from the LTTE in 1987? A. Operation Cyclone, B. Operation Meghdoot, C. Operation Cactus, D. Operation Pawan", "Answer":'option d'},
    {"Question":"Which of these cities is not named after its founder or a dynasty? A. Bikaner, B. Ludhiana, C. Khajuraho, D. Jodhpur", "Answer":'option c'},
    {"Question":"The tenth Edition of the bilateral exercise between the Indian Navy and Russian Federation Navy begins in? A. Visakhapatnam, B. Kolkata, C. Cochin, D. Chennai", "Answer":'option a'},
    {"Question":"Where will the Indian Army induct new artillery guns and equipment, including K9 Vajra and M777 howitzersW in Maharashtra? , A. Thane, B. Pune, C. Nagpur, D. Nashik", "Answer":'option d'},
    {"Question":"How many submarines will be contructed by DAC worth of Rs40000 cr? A. 5, B. 6, C. 8, D. 10", "Answer":'option b'},
    {"Question":"What was originally called the 'imitation game' by its creator? A. The Turing Test, B. LISP, C. The Logic Theorist, D. Cybernetics", "Answer":'option a'},
    {"Question":"Parallel Economy is also referred as ? A. Grey Market, B. Black Market , C. Black Economy, D. Grey Economoy", "Answer":'option c'},
    {"Question":"Which is a legal tender in modern economy amongst the following? A. Currency notes, B. Cheques, C. Bank Draft, D. Promissory notes", "Answer":'option a'},
    {"Question":"In which year did second phase of nationalization of banks took place? A. 1969, B. 1979, C. 1980, D. 1990", "Answer":'option c'},
    {"Question":"When more than one bank is allowing credit facilities to one party in coordination with each other under a formal arrangement, the arrangement is generally known as? A. Consortium, B. Syndication, C. Multiple Banking, D. Participation", "Answer":'option a'},
    {"Question":"The difference between exports and imports is called as? A. assets and liabilities, B. balance of payment, C. GDP, D. balance of trade", "Answer":'option d'},
    {"Question":"Which among the following was the capital of Shivaji? A. Poona, B. Raigad, C. Sinhagad, D. Panhala", "Answer":'option b'},
    {"Question":"Shivaji founded the Maratha kingdom by annexing the territories of ? A. Bijapur, B. Mughals, C. Both a and b, D. Bijapur, Golcunda and the Mughals", "Answer":'option c'},
    {"Question":"What was Chauth? A. A religious tax imposed by Aurangzeb, B. Toll tax imposed by Shivaji, C. Irrigation tax charged by Akbar Land tax levied by Shivaji on neighbouring, D. States", "Answer":'option d'},
    {"Question":"Who was the last Mughal emperor? A. Shah Alam-II, B. Akbar-II, C. Bahadur Shah-II, D. Ahmad Shah ", "Answer":'option c'},
    {"Question":"Which one is not situated at Fatehpur Sikri? A. The Panch Mahal, B. Moti Masjid, C. Tomb of Salim Chishti, D. The Moriam Palaoe", "Answer":'option b'},
    {"Question":"During the reign of which ruler use of Halo or Divine Lights were started in paintings? A. Iltutmish, B. Aurangazeb, C. Jahangir, D. Akbar", "Answer":'option c'},
    {"Question":"Who was the first Sultan of Delhi to issue regular currency and to declare Delhi as the capital of his empire? A. Balban, B. Aram Shah, C. Nasiruddin Mahmud, D. IIitutmish", "Answer":'option d'},
    {"Question":"Humayun restored his Indian kingdom with the help of which country ruler? A. Arabia, B. Kabul, C. Persia, D. Turkey", "Answer":'option d'},
    {"Question":"Tulsi Das composed his Ramacharitamanas during the reign of? A. Harsha, B. Alauddin Khalji, C. Akbar, D. Krishnadeva Raya", "Answer":'option c'},
    {"Question":"Humayun Nama was written by? A. Humayun, B. Mirza Kamran, C. Bairam Khan D. Gulbadan Begum", "Answer":'option d'},
    {"Question":"The first constitutional measure introduced by the British in India which worked till the framing of the Indian Constitution was? A. the Act of 1919, B. the Act of 1935, C. Indian Independence Bill, D. Cabinet Mission Plan", "Answer":'option b'},
    {"Question":"The British law which provoked Mahatma  Gandhi to crusade for the Asians in South Africa was called? A. Apartheid, B. Blacks' Registration, C. Asiatic Registration, D. Subcitizens' Licence", "Answer":'option c'},
    {"Question":"Who among the following was popularly known as the 'Frontier Gandhi'? A. Hasrat Mohani, B. Maulana Abul Kalam Azad, C. Khan Abdul Ghaffar Khan, D. Iqbal Khan", "Answer":'option c'},
    {"Question":"Individuals of one population can interbreed with individuals of another population if they have the same? A. Species, B. Genus, C. Family, D. Order ","Answer":"option a"},
    {"Question":"The Indian Botanical Garden is located at? A. Dehradun, B. Lucknow, C. Kolkata, D. Chennai","Answer":"option c"},
    {"Question":"The point of intersection of the altitudes of a triangle is called? A. Excentre, B. Orthocentre, C. Incentre, D. Centroid","Answer":"option b"},
    {"Question":"The Accounting Year of Reserve Bank of India runs from? A. April to March, B. July to June, C. January to December, D. August to July","Answer":"option b"},
    {"Question":"The Indian economy can be most appropriately described as? A. Capitalist economy, B. Socialist economy, C. Traditional economy, D. Mixed economy","Answer":"option d"},
    {"Question":"Which one of the following is NOT within the duties of the Planning Commission? A. To make an assessment of the material, capital and human resources of the country, B. To define the stage of growth and suggest allocation of resources, C. To determine the nature of machinery required for implementation of plan proposals, D. To prepare the annual central budget ","Answer":"option d"},
    {"Question":"All taxes come under? A. revenue receipts, B. capital receipts, C. public debt, D. public receipts","Answer":"option a"},
    {"Question":"Which of the following was not one of the techniques of 'Satyagraha' advocated by Mahatama Gandhi? A. Ahimsa, B. Fasting, C. Civil Disobedience, D. Non-Cooperation","Answer":"option a"},
    {"Question":"Which Party was established by Subhash Chandra Bose after he came out of Indian National Congress? A. Indian National Army, B. Republican party, C. Forward Bloc, D. Socialist Party","Answer":"option c"},
    {"Question":"The Indian Independence Act was passed in? A. 18th July 1947, B. 1st August 1947, C. 1st June 1947, D. 1st September 1947, ","Answer":"option a"},
    {"Question":"The British attitude towards granting India independence changed partly owing to the? A. Change in the government of the UK, B. Impact of World War II, C. Growing tide of Indian Nationalism, D. All of the above","Answer":"option d"},
    {"Question":"Who among the following revolutionaries was executed by the British ? A. Jitin Das, B. Chandrashekhar Azad, C. Rajguru, D. Kalpana - Dutt","Answer":"option c"},
    {"Question":"In the 18th Century the Royal prerogative in the affairs of the East India Company was controlled by? A. The Viceroy's Council, B. The Indian Legislature, C. The Parliament in England, D. The Secretary of State, ","Answer":"option c"},
    {"Question":"5th June is observed as ? A. World forest day, B. World environment day, C. World wildlife day, D. World population day","Answer":"option b"},
    {"Question":"Temperate forests in India occur in? A. Indo-gangetic plains, B. Himalayas, C. Eastern India, D. Southern peninsula","Answer":"option b"},
    {"Question":"In the stratosphere, what happens with the air temperature normally? A. Decreases with increasing height, B. Increases with increasing height, C. Increases and decreases depending on the season, D. Cannot be measured","Answer":"option b"},
    {"Question":"What is the man-made green house gas known as? A. Carbon dioxide, B. HFC, C. Ozone, D. Water Vapour","Answer":"option b"},
    {"Question":"The portion of the ocean floor closest to the land is known as? A. Continental Shelf, B. Ocean deep, C. Continental slope, D. Coastal Plain","Answer":"option a"},
    {"Question":"What is a light year? A. A unit of time which the earth takes to go round the sun, B. The distance travelled by the light in one year, C. It is a year in which the gravitational pull is less than the normal value of 'G', D. The distance travelled by the light in ten years","Answer":"option b"},
    {"Question":"High salinity in the sea results from? A. High temperature, B. Low temperature, C. Enclosed Seas, D. Humidity","Answer":"option c"},
    {"Question":"Where is the thermal equator located? A. In northern hemisphere, B. In southern hemisphere, C. In western hemisphere, D. In eastern hemisphere","Answer":"option a"},
    {"Question":"What does an approaching cyclone lead to? A. Drop in pressure, B. Rise in temperature, C. Both a and b, D. Rise in pressure","Answer":"option c"},
    {"Question":"How many ways are there to become a United States Citizen? A. 1, B. 2, C. 3, D. 4","Answer":"option b"},
    {"Question":"Career planning and development is an example of? A. human process intervention, B. techno structural interventions, C. strategic intervention, D.HRM interventions","Answer":"option d"},
    {"Question":"Which of the following is correct about sustainable development? A. It aims at continuous development, B. It deals with regular growth of social interest, C. It meets the needs of present without hurting future generations, D. It develops employees for growth of busines","Answer":"option c"},
    {"Question":"What is meant by the public sector? A. The goals of the society, B. Economic activities in which the government engages for the public good, C. Economic activities in which self interest makes for personal affluence, D. Economic activities open to the public ","Answer":"option b"},
    {"Question":"The frequency of which of the following is the highest? A. Gamma rays, B. Light waves, C. Micro waves, D. Radio waves","Answer":"option a"},
    {"Question":"The velocity of sound in air under normal condition in meters per second is? A. 30 mps, B. 320 mps, C. 343 mps, D. 320 mps","Answer":"option c"},
    {"Question":"The highest national award in India given for exceptional work for advancement of art, literature and science? A.Bharat Ratna, B. Padma Awards, C. Gallantry Awards, D. Padma Bhushan","Answer":"option a"},
    {"Question":"Which of the following acts as a channel of transmission of blood to the heart in the human body? A. Arteries, B. Muscle fibres, C. Nerves, D. Veins","Answer":"option d"},
    {"Question":"The Olympic Flame symbolises? A. unity among various nations of the world, B. speed, perfection and strength, C. sports as a means for securing harmony among nations, D. continuity between the ancient and modern games","Answer":"option d"},
    {"Question":"India's first atomic power station was set up at? A. Surat,Gujarat, B. Tarapur,Maharashtra, C. Trombay,Maharashtra, D. Solapur,Maharashtra","Answer":"option b"},
    {"Question":"Computer Assisted Instruction is based on which principle? A. Operant Conditioning, B. Classical Conditioning, C. Pavlovian Conditioning, D. Respondent Conditioning", "Answer":'option a'},
    {"Question":"Which of the following affects an individual's development at a given time? A. Their experiences, B. Inherited potentitalities, C. Interaction of nature and nurture, D. Social pressure on the individual", "Answer":'option c'},
    {"Question":"Which of the following items of information are important about students to motivate them for studies? A. Personality, B. Learning style, C. Socio-cultural background, D. All of the above", "Answer":'option d'},
    {"Question":"Which is the apex institution involved in the planned and coordinated development of the teacher education system in the country? A. UGC, B. NCTE, C. NCERT, D. None of these", "Answer":'option b'},
    {"Question":"Why is Environmental Awareness necessary at all stages of education? A. Important for human survival, B. Environment varies from region to region, C. Man must control and change environment, D. Man must adapt to the environment", "Answer":'option b'},
    {"Question":"The first Indian actress to have been nominated to the Rajya Sabha was? A. Nargis Dutt, B. Hema Malini, C. Jaya Prada, D. Raveena Tandon", "Answer":'option a'},
    {"Question":"India's first indigenously built submarine was? A. INS Savitri, B. INS Shalki, C. INS Delhi, D. INS Vibhuti", "Answer":'option b'},
    {"Question":"What is the role of World Trade Organisation? A. To settle trade disputes between nations, B. To widen the principal of free trade to sectors such as services and agriculture, C. To initiate trades, D. To handle trading policies", "Answer":'option b'},
    {"Question":"Excessive secretion from the pituitary gland in the children results in? A. increased height, B. retarded growth, C. weakening of bones, D. weakening of muscles", "Answer":'option a'},
    {"Question":"The SLV-3 project provided India with the expertise to lop a larger and more sophisticated launch vehicle? A. PSLV, B. ASLV, C. GSLV, D. SLV-S", "Answer":'option b'},
    {"Question":"The number of chromosomes in human body is? A. 42, B. 44, C. 46, D. 48", "Answer":'option c'},
    {"Question":"Lal Bahadur Shastri is also known as? A. Guruji, B. Man of Peace, C. Punjab Kesari, D. Mahamana", "Answer":'option b'},
    {"Question":"The first recipient of Bharat Ratna award in 1954 was? A. S. Radhakrishnan, B. C. Rajagopalachari, C. V. Raman, D. Jawaharlal Nehru", "Answer":'option b'},
    {"Question":"The ozone layer is being destroyed by chlorofluorocarbons. In this regard which do you consider as the most harmful? A. Carbon atom, B. Chlorine atom, C. Fluorine atom, D. The entire compound", "Answer":'option b'},
    {"Question":"When is the International Workers Day? A. 15th April, B. 12th December, C. 1st May, D. 1st August", "Answer":'option c'},
    {"Question":"Which launch vehicle is capable of placing around 1540 kg of INSAT class of satellites in geo-synchronous transfer orbit of earth? A. SLV-S, B. PSLV, C. ASLV, D. GSLV", "Answer":'option d'},
    {"Question":"P. T. Usha, who came close to bagging a bronze, finished fourth in which of the 1984 Olympics? A. 400 meters final, B. 800 meters final, C. 400 meters hurdle, D. the marathon", "Answer":'option c'},
    {"Question":"The term used when a member of a legislature leaves his party on whose ticket he was elected to join the ruling party or the opposition, is called? A. floor crossing, B. fourth estate, C. fifth column, D. free ports", "Answer":'option a'},
    {"Question":"What happens to resistance of a substance when related with Super conductivity? A. increases with temperature, B. decreases with temperature, C. does not change with temperature, D. becomes zero at very low temperature", "Answer":'option d'},
    {"Question":"The credit of inventing the television goes to? A. Faraday, B. Baird, C. Edison, D. Marconi", "Answer":'option b'},
    {"Question":"The playground of baseball is known as? A. court, B. diamond, C. ring, D. pitch", "Answer":'option b'},
    {"Question":"India has largest deposits of in the world. A. gold, B. copper, C. mica, D. silver", "Answer":'option c'},
    {"Question":"World War II was fought between? A. Axis Power Germany, Italy and Japan against the Allies Britain, USSR, USA, France, B. Austria, Hungary, Turkey against France, USA, Japan, C. Hungary, Turkey against France, Japan, D. Austria, France, Turkey against USA, Japan", "Answer":'option a'},
    {"Question":"Study of earthquakes is known as? A. ecology, B. seismology, C. numismatics, D. geology", "Answer":'option b'},
    {"Question":"Which of the following are the member countries of the commonwealth? A. Australia, Tonga, UK and Zimbabwe, B. Nigeria, Pakistan, India, Jamaica and Singapore, C. Mauritius, Maldives, Ghana, Bangladesh, D. All of the above", "Answer":'option d'},
    {"Question":"Coral reefs in India can be found in? A. the coast of Orissa, B. Waltair, C. Rameshwaram, D. Trivandrum", "Answer":'option c'},
    {"Question":"The main objective of which of the following UN agency is to help the underdeveloped countries in the task of raising their living standards? A. IMF, B. UNICEF, C. UNDP, D. IDA", "Answer":'option d'},
    {"Question":"Richter scale is used for measuring? A. density of liquid, B. intensity of earthquakes, C. velocity of wind, D. humidity of air", "Answer":'option d'},
    {"Question":"How many times has Brazil won the World Cup Football Championship? A. Four times, B. Twice, C. Five times, D. Once", "Answer":'option c'},
    {"Question":"National Anthem was first sung on ? A. December 27, 1911 during the Indian National Congress Session at Calcutta, B. January 24, 1950 by the Constituent Assembly of India, C. January 26, 1959 by the Government of India, D. December 12, 1913 during the Indian National Congress", "Answer":'option a'}
]


class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        score_attributes={'correct':0, 'totalq':0, 'playedtimes':0}
        handler_input.attributes_manager.persistent_attributes=score_attributes
        handler_input.attributes_manager.save_persistent_attributes()
        speak_output="Welcome to K. B. C. Quiz. Would you like to know the rules? You can say Yes or No. "
        reprompt_text="Would you like to know the rules?. You can say Yes or No. "
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class HasPlayedLaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        attr=handler_input.attributes_manager.persistent_attributes
        attributes_are_present=("correct" in attr and "totalq" in attr and "playedtimes" in attr)
        if attributes_are_present:
            if attr["totalq"]==0:
                attributes_are_present=False
        return attributes_are_present and ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr=handler_input.attributes_manager.persistent_attributes
        speak_output="Welcome back!! You have answered {c} out of {t} Questions correctly till now. Let's continue!!! ".format(c=attr['correct'],t=attr["totalq"])
        record=random.choice(data)
        session_attr=handler_input.attributes_manager.session_attributes
        session_attr["record"]=record
        session_attr['qnum']=1
        session_attr['correct']=0
        session_attr['score-booster']=2
        speak_output+="Your first question is, {} ".format(record["Question"])
        reprompt_text="Your question is {} ".format(record["Question"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class AnswerIntentHandler(AbstractRequestHandler):
    """Handler for Answer Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AnswerIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots=handler_input.request_envelope.request.intent.slots
        userchoice=slots["choice"].value
        session_attr=handler_input.attributes_manager.session_attributes
        attr=handler_input.attributes_manager.persistent_attributes
        #playedtimes=int(attr["playedtimes"])
        record=session_attr["record"]
        q=int(session_attr["qnum"])
        if userchoice==record["Answer"]:
            speak_output = "Well done, Your answer is correct!!! "
            session_attr["correct"]+=1
        else:
            speak_output = "Wrong choice! The correct answer is {}. ".format(record["Answer"])
        if (q+1)<=10:
            record=random.choice(data)
            session_attr["record"]=record
            session_attr["qnum"]=q+1
            speak_output+="Question number {num} is, {q}  ".format(num=q+1,q=record["Question"])
            reprompt_text="Your question is {}  ".format(record["Question"])
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
            )
        else:
            score_attributes={'correct':(attr['correct']+session_attr['correct']), 'totalq':(attr['totalq']+session_attr['qnum']), 'playedtimes':(attr['playedtimes']+1)}
            handler_input.attributes_manager.persistent_attributes=score_attributes
            handler_input.attributes_manager.save_persistent_attributes()
            speak_output+="You have answered {c} out of {t} questions correctly. Thank you for playing. Come again! ".format(c=score_attributes['correct'],t=score_attributes['totalq'])
            return (
            handler_input.response_builder
                .speak(speak_output)
                .response
            )
            
        
class YesIntentHandler(AbstractRequestHandler):
    """Handler for Yes Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.YesIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        record=random.choice(data)
        session_attr=handler_input.attributes_manager.session_attributes
        session_attr["record"]=record
        session_attr['qnum']=1
        session_attr['correct']=0
        session_attr['score-booster']=2
        speak_output="You will be asked 10 questions and given 2 score-boosters. The score-boosters will reveal the correct answer. You can reply to the question like, 'Answer is option B'. Say 'repeat' to repeat question.  Say 'score' to know your game score. Say 'score-booster' to use score-booster. Let's get started. "
        speak_output+="Your first question is, {} ".format(record["Question"])
        reprompt_text="Your question is {} ".format(record["Question"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class NoIntentHandler(AbstractRequestHandler):
    """Handler for No Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.NoIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        record=random.choice(data)
        session_attr=handler_input.attributes_manager.session_attributes
        session_attr["record"]=record
        session_attr['qnum']=1
        session_attr['correct']=0
        session_attr['score-booster']=2
        speak_output=" Say 'repeat' to repeat question. Say 'score' to know your game score. Say 'score-booster' to use score-booster. Let's get started. "
        speak_output+="Your first question is, {} ".format(record["Question"])
        reprompt_text="Your question is {} ".format(record["Question"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class ScoreBoosterIntentHandler(AbstractRequestHandler):
    """Handler for ScoreBoosterIntent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("ScoreBoosterIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr=handler_input.attributes_manager.session_attributes
        attr=handler_input.attributes_manager.persistent_attributes
        record=session_attr["record"]
        q=session_attr['qnum']
        if q<10:
            if session_attr["score-booster"]==0:
                speak_output="You have no score-boosters left. "
                speak_output+="Your question is, {} ".format(record["Question"])
            else:
                if session_attr["score-booster"]==1:
                    speak_output="The correct answer is {}. You now have 0 score-boosters left. ".format(record["Answer"])
                else:
                    speak_output="The correct answer is {}. You now have 1 score-booster left. ".format(record["Answer"])
                session_attr["correct"]+=1
                record=random.choice(data)
                session_attr["record"]=record
                session_attr['qnum']=q+1
                session_attr['score-booster']-=1
                speak_output+="Question number {num} is, {qu} ".format(num=q+1,qu=record["Question"])
            reprompt_text="Your question is {} ".format(record["Question"])
            return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
            )
        else:
            if session_attr["score-booster"]==0:
                speak_output="You have no score-boosters left. "
                speak_output+="Your question is, {} ".format(record["Question"])
                reprompt_text="Your question is {} ".format(record["Question"])
                return (
                handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
            )
            else:
                speak_output="The correct answer is {}. ".format(record['Answer'])
                session_attr["correct"]+=1
                score_attributes={'correct':(attr['correct']+session_attr['correct']), 'totalq':(attr['totalq']+session_attr['qnum']), 'playedtimes':(attr['playedtimes']+1)}
                handler_input.attributes_manager.persistent_attributes=score_attributes
                handler_input.attributes_manager.save_persistent_attributes()
                speak_output+="You have answered {c} out of {t} questions correctly. Thank you for playing. Come again! ".format(c=score_attributes['correct'],t=score_attributes['totalq'])
                return (
                handler_input.response_builder
                .speak(speak_output)
                .response
            )

class RepeatIntentHandler(AbstractRequestHandler):
    """Handler for Repeat Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("RepeatIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr=handler_input.attributes_manager.session_attributes
        record=session_attr["record"]
        speak_output="Your question is, {} ".format(record["Question"])
        reprompt_text="Your question is {}  ".format(record["Question"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class TellScoreIntentHandler(AbstractRequestHandler):
    """Handler for TellScore Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("TellScoreIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        session_attr=handler_input.attributes_manager.session_attributes
        record=session_attr["record"]
        speak_output = "Your answer is correct for {c} out of {t} questions currently. ".format(c=session_attr["correct"],t=(session_attr["qnum"]-1))
        speak_output+="Your question is, {} ".format(record["Question"])
        reprompt_text="Your question is {}  ".format(record["Question"])
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )

class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

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
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        attr=handler_input.attributes_manager.persistent_attributes
        session_attr=handler_input.attributes_manager.session_attributes
        if session_attr['qnum']>1:
            score_attributes={'correct':(attr['correct']+session_attr['correct']), 'totalq':(attr['totalq']+session_attr['qnum']-1), 'playedtimes':(attr['playedtimes']+1)}
            handler_input.attributes_manager.persistent_attributes=score_attributes
            handler_input.attributes_manager.save_persistent_attributes()
            speak_output="You have answered {c} out of {t} questions correctly till now. Thank you for playing. Come again! ".format(c=score_attributes['correct'],t=score_attributes['totalq'])
        else:
            speak_output="Come again to play!"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.
        attr=handler_input.attributes_manager.persistent_attributes
        session_attr=handler_input.attributes_manager.session_attributes
        if session_attr['qnum']>1:
            score_attributes={'correct':(attr['correct']+session_attr['correct']), 'totalq':(attr['totalq']+session_attr['qnum']-1), 'playedtimes':attr['playedtimes']+1}
            handler_input.attributes_manager.persistent_attributes=score_attributes
            handler_input.attributes_manager.save_persistent_attributes()
        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

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


sb = CustomSkillBuilder(persistence_adapter=s3_adapter)

sb.add_request_handler(HasPlayedLaunchRequestHandler())
sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(AnswerIntentHandler())
sb.add_request_handler(RepeatIntentHandler())
sb.add_request_handler(ScoreBoosterIntentHandler())
sb.add_request_handler(TellScoreIntentHandler())
sb.add_request_handler(YesIntentHandler())
sb.add_request_handler(NoIntentHandler())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()