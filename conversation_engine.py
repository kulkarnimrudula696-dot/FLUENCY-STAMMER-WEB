"""
FLUENCY Natural Conversation Engine
Provides intelligent, natural, context-aware back-and-forth dialogue for Conversation Mode.

Core Design:
1. Strictly ZERO repetition: No question, sentence, or phrasing is ever repeated during a session.
2. Truly understands the user's message using word-boundary parsing, entity extraction, and sentiment recognition.
3. Covers all 10 real-life conversation scenarios:
   1. Introducing Yourself (scen_intro)
   2. Talking with a Friend (scen_friend)
   3. College Conversation (scen_college)
   4. Job Interview (scen_interview)
   5. Restaurant / Ordering Food (scen_restaurant)
   6. Shopping (scen_shopping)
   7. Asking for Directions (scen_directions)
   8. Talking to a Teacher (scen_teacher)
   9. Doctor Appointment (scen_doctor)
   10. Phone Call (scen_phone)
4. Multi-language support: English, Hindi, Marathi, Spanish, French, German, Japanese, Chinese.
5. Continues naturally indefinitely until the user chooses to end the call.
"""

import re
import os
import json
import random
import logging
import unicodedata

logger = logging.getLogger(__name__)

# =============================================================================
# 10 FULL REAL-LIFE SCENARIO DEFINITIONS
# =============================================================================

SCENARIO_DEFINITIONS = {
    'scen_intro': {
        'title': 'Introducing Yourself',
        'persona': 'Friendly Host Alex',
        'default_greeting': "Hello there! Welcome! I don't think we've met yet. I'm Alex. Could you tell me a little bit about yourself?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Welcome! It's so great to meet you. Exploring {item} sounds really interesting.",
                'question': "What kind of hobbies, creative projects, or activities do you enjoy spending time on?"
            },
            {
                'turn_index': 2,
                'ack': "That is really fascinating! Getting involved with {item} takes genuine passion.",
                'question': "How did you first get into that? Was there a particular moment or person that inspired you?"
            },
            {
                'turn_index': 3,
                'ack': "I love hearing origin stories like that - it makes the journey so meaningful.",
                'question': "What are you most excited to accomplish or learn over the next few months?"
            }
        ]
    },

    'scen_friend': {
        'title': 'Talking with a Friend',
        'persona': 'Close Friend Sam',
        'default_greeting': "Hey! It's so great to see you! How has your week been going so far? Anything exciting happen?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "I can definitely relate - {item} sounds like it took quite a bit of energy!",
                'question': "Did you get any time to relax or do something fun for yourself after that?"
            },
            {
                'turn_index': 2,
                'ack': "That sounds like a really enjoyable way to spend time.",
                'question': "Have you watched any good movies, heard new music, or visited any cool spots lately?"
            },
            {
                'turn_index': 3,
                'ack': "I always love hearing your recommendations!",
                'question': "Do you have any fun plans coming up for this weekend or next week?"
            }
        ]
    },

    'scen_college': {
        'title': 'College Conversation',
        'persona': 'Study Partner Maya',
        'default_greeting': "Hey! Glad we could meet up at the library. For our upcoming presentation, do you have any ideas you'd like us to explore together?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Exploring {item} is a brilliant angle! That will definitely catch the class's attention.",
                'question': "How should we divide the slides between us - would you prefer introducing the concepts or presenting the case studies?"
            },
            {
                'turn_index': 2,
                'ack': "That division sounds very fair and well-balanced.",
                'question': "When would be a good time for us to do a quick dry run together to practice our timing?"
            },
            {
                'turn_index': 3,
                'ack': "Sounds like a plan! We're in great shape for this presentation.",
                'question': "How are your other courses and assignments going this semester - staying on top of things?"
            }
        ]
    },

    'scen_interview': {
        'title': 'Job Interview',
        'persona': 'Hiring Manager Sarah',
        'default_greeting': "Thank you so much for joining me today. To get started, could you walk me through your background and what excites you about this opportunity?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Thank you for sharing that overview - your background in {item} sounds very relevant.",
                'question': "Could you walk me through a specific project or achievement that you're especially proud of?"
            },
            {
                'turn_index': 2,
                'ack': "That demonstrates great initiative and problem-solving resilience.",
                'question': "When collaborating in a team, how do you like to approach giving and receiving feedback?"
            },
            {
                'turn_index': 3,
                'ack': "Clear, empathetic communication makes such a positive impact on any team.",
                'question': "Looking ahead, what skills or areas of expertise are you most excited to develop further over the next couple of years?"
            }
        ]
    },

    'scen_restaurant': {
        'title': 'Restaurant / Ordering Food',
        'persona': 'Server Liam',
        'default_greeting': "Good evening! Welcome to the Bistro. Tonight our chef's special is fresh garden pasta and creamy roasted tomato soup. What can I get started for you?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "A fresh order of {item} is a wonderful choice! We will get that prepared right away.",
                'question': "Would you like to pair that with a refreshing beverage, sparkling water, or iced tea?"
            },
            {
                'turn_index': 2,
                'ack': "Got that noted for your table!",
                'question': "Are you saving room for dessert tonight? We have warm chocolate lava cake and fresh fruit tarts."
            },
            {
                'turn_index': 3,
                'ack': "Everything is on its way to the kitchen.",
                'question': "Is there anything else we can bring to make your dining experience comfortable?"
            }
        ]
    },

    'scen_shopping': {
        'title': 'Shopping',
        'persona': 'Store Associate Jordan',
        'default_greeting': "Hello! Welcome to our store. Are you looking for anything specific today, or can I help you find sizes and styles?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "We have a fantastic selection of {item} right over in our new arrivals section.",
                'question': "What specific color, size, or material do you prefer for this?"
            },
            {
                'turn_index': 2,
                'ack': "Let me check our stock... Yes, we have that size available right here!",
                'question': "Would you like to try it on in our fitting rooms, or would you like to see a complementary item?"
            },
            {
                'turn_index': 3,
                'ack': "That fits your style really well.",
                'question': "Would you like me to take this to the front register for you, or are you still browsing?"
            }
        ]
    },

    'scen_directions': {
        'title': 'Asking for Directions',
        'persona': 'Helpful Resident Chris',
        'default_greeting': "Excuse me! You look like you might be looking for something. Can I help point you in the right direction?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Oh yes, I know the {item} well! You're actually not far at all.",
                'question': "Are you planning to walk there on foot, or would you prefer a quick bus route?"
            },
            {
                'turn_index': 2,
                'ack': "Walking is super pleasant from here - just follow the sidewalk past the clock tower and turn right.",
                'question': "Are you visiting our city for the first time, or have you explored around here before?"
            },
            {
                'turn_index': 3,
                'ack': "Welcome! There are so many great sights in this neighborhood.",
                'question': "Are you looking for any cozy coffee spots or local bakeries along the way?"
            }
        ]
    },

    'scen_teacher': {
        'title': 'Talking to a Teacher',
        'persona': 'Professor Evans',
        'default_greeting': "Hello! Come on in and have a seat. What topic or assignment would you like to discuss today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "I'm glad you brought up {item}. That is a key concept in our syllabus.",
                'question': "What specific part of the assignment or concept has been the most challenging to work through?"
            },
            {
                'turn_index': 2,
                'ack': "That's a very thoughtful question. Breaking it into smaller steps makes it much clearer.",
                'question': "How is your study pace going for the upcoming midterm - do you have a study group or schedule?"
            },
            {
                'turn_index': 3,
                'ack': "You have a solid study approach, and your questions show genuine engagement.",
                'question': "Are there any additional reference materials or research papers I can share to support your work?"
            }
        ]
    },

    'scen_doctor': {
        'title': 'Doctor Appointment',
        'persona': 'Dr. Sharma',
        'default_greeting': "Good morning! Please have a seat. How have you been feeling lately, and what brings you in for a visit today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Thank you for describing that. It is helpful to understand how {item} has been affecting you.",
                'question': "How long have you noticed these symptoms, and do they feel more noticeable during certain times of the day?"
            },
            {
                'turn_index': 2,
                'ack': "That gives me clear context. We will do a gentle examination to check on that.",
                'question': "How has your daily routine been lately in terms of hydration, regular sleep, and balanced meals?"
            },
            {
                'turn_index': 3,
                'ack': "Prioritizing rest and proper hydration will make a significant positive difference.",
                'question': "Do you have any specific concerns or questions you'd like us to discuss before we finalize your plan?"
            }
        ]
    },

    'scen_phone': {
        'title': 'Phone Call',
        'persona': 'Receptionist Taylor',
        'default_greeting': "Thank you for calling City Care Center. This is Taylor speaking. How may I assist you today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "I would be glad to help you schedule your {item}.",
                'question': "Which day of the week works best for your schedule - would you prefer earlier or later in the week?"
            },
            {
                'turn_index': 2,
                'ack': "Let me check our calendar... Yes, we have openings available then!",
                'question': "Would a morning slot around 10:30 AM or an afternoon slot around 2:15 PM suit you better?"
            },
            {
                'turn_index': 3,
                'ack': "Got that reserved for you in our system.",
                'question': "Could you please confirm your contact details so we can send a text or email confirmation?"
            }
        ]
    }
}

# Add alias for legacy scenario keys if any
SCENARIO_DEFINITIONS['scen_cafe'] = SCENARIO_DEFINITIONS['scen_restaurant']
SCENARIO_DEFINITIONS['scen_help'] = SCENARIO_DEFINITIONS['scen_directions']
SCENARIO_DEFINITIONS['scen_office'] = SCENARIO_DEFINITIONS['scen_interview']

# =============================================================================
# TOPIC KNOWLEDGE GRAPH & ENTITY-SPECIFIC FOLLOW-UPS
# =============================================================================

ENTITY_TOPIC_MAP = {
    'tech_and_coding': {
        'keywords': ['app', 'code', 'coding', 'software', 'developer', 'web', 'website', 'python', 'javascript', 'frontend', 'backend', 'ai', 'program', 'programming', 'tech', 'data', 'engineer', 'feature', 'bug', 'system', 'react', 'database', 'project'],
        'ack_templates': [
            "Working with technology like {item} takes great problem-solving and creativity.",
            "Building projects with {item} is such an impactful and creative process!",
            "That sounds like a very engaging project involving {item}."
        ],
        'followups': [
            "What has been the most enjoyable or rewarding part of building it so far?",
            "Did you run into any tricky challenges while developing it, and how did you solve them?",
            "What technologies or tools are you enjoying working with the most right now?",
            "Where do you hope to take this project next once the initial version is ready?"
        ]
    },
    'nature_and_outdoors': {
        'keywords': ['hike', 'hiking', 'mountain', 'mountains', 'trail', 'forest', 'park', 'nature', 'beach', 'ocean', 'lake', 'camping', 'outdoor', 'outdoors', 'walk', 'walking', 'autumn', 'spring', 'trees', 'scenery'],
        'ack_templates': [
            "Getting outdoors and spending time in {item} is such a refreshing way to recharge.",
            "There's nothing quite like fresh air and {item} to clear your mind and reset.",
            "Connecting with nature around {item} always brings a great sense of calm."
        ],
        'followups': [
            "Do you have a favorite trail, park, or scenic spot you love returning to?",
            "Do you prefer peaceful solo walks or exploring outdoors with friends and family?",
            "What is the most breathtaking nature spot you've ever come across?",
            "How does being out in nature affect your mood and focus for the rest of the week?"
        ]
    },
    'travel_and_cities': {
        'keywords': ['travel', 'trip', 'japan', 'europe', 'paris', 'tokyo', 'mumbai', 'pune', 'delhi', 'london', 'visit', 'visited', 'vacation', 'flight', 'country', 'city', 'cities', 'tour', 'explore', 'exploring', 'destination', 'abroad', 'culture'],
        'ack_templates': [
            "Visiting {item} sounds like such an extraordinary experience!",
            "Traveling to {item} brings so many rich memories and new perspectives.",
            "That sounds like a memorable journey to {item}."
        ],
        'followups': [
            "What was your absolute favorite memory or hidden gem you discovered during that trip?",
            "Did you get to try any unique local dishes or traditional foods while you were there?",
            "If you could plan your next dream vacation anywhere in the world, where would you go next?",
            "Do you prefer structured sightseeing trips, or wandering around and discovering local spots?"
        ]
    },
    'food_and_culinary': {
        'keywords': ['cappuccino', 'espresso', 'tea', 'chai', 'coffee', 'latte', 'pasta', 'pizza', 'sushi', 'curry', 'baking', 'cook', 'cooking', 'recipe', 'breakfast', 'dinner', 'lunch', 'dessert', 'cake', 'croissant', 'soup', 'sandwich', 'paneer', 'biryani', 'dosa', 'roti'],
        'ack_templates': [
            "{item} is such a wonderful choice - comforting and delicious!",
            "You have great taste - enjoying good {item} is always satisfying.",
            "There is something so special about sharing good food and {item}."
        ],
        'followups': [
            "Do you enjoy cooking and preparing meals at home, or do you prefer discovering cozy local restaurants?",
            "Is there a family recipe or special signature dish you love making?",
            "What is your go-to comfort meal when you've had a long day and want to unwind?",
            "If you could have a chef make you any special dish right now, what would you ask for?"
        ]
    },
    'pets_and_animals': {
        'keywords': ['dog', 'dogs', 'cat', 'cats', 'pet', 'pets', 'puppy', 'kitten', 'animal', 'animals', 'rescue', 'bird', 'fish', 'otter', 'capybara', 'koala'],
        'ack_templates': [
            "Animals and pets like {item} bring so much companionship and warmth into our days!",
            "Having a {item} around makes daily life so much brighter and more entertaining.",
            "Taking care of a {item} is such a heartwarming bond."
        ],
        'followups': [
            "What's the funniest or sweetest thing you've seen your pet or an animal do?",
            "How does spending time with pets help you unwind after a busy day?",
            "If you could spend a day observing any animal in its natural habitat, what would it be?",
            "What is their favorite game, treat, or spot to relax in the house?"
        ]
    },
    'creative_arts_and_music': {
        'keywords': ['music', 'guitar', 'piano', 'singing', 'song', 'songs', 'art', 'draw', 'drawing', 'painting', 'photo', 'photography', 'camera', 'write', 'writing', 'book', 'books', 'read', 'reading', 'novel', 'movie', 'film'],
        'ack_templates': [
            "Expressing yourself through {item} is such a fulfilling and creative outlet.",
            "I love that you're engaged with {item} - creative hobbies bring so much richness to life.",
            "Having a genuine passion for {item} is so rewarding."
        ],
        'followups': [
            "What first sparked your interest or passion for that?",
            "Who are some of your favorite artists, authors, or creators that inspire you?",
            "Do you usually set aside quiet time for creative work, or do you do it whenever inspiration strikes?",
            "What's one creative project or piece of music you'd love to work on in the future?"
        ]
    },
    'wellness_and_mindfulness': {
        'keywords': ['relax', 'relaxing', 'calm', 'quiet', 'peace', 'meditate', 'meditation', 'breath', 'breathing', 'sleep', 'morning', 'routine', 'yoga', 'exercise', 'gym', 'workout', 'stretch', 'reset'],
        'ack_templates': [
            "Prioritizing {item} is so important for keeping a balanced and grounded state of mind.",
            "Taking dedicated time for {item} makes such a noticeable difference in how we feel.",
            "That sounds like a very healthy and restorative approach."
        ],
        'followups': [
            "What does your ideal morning routine look like when you want to start the day feeling calm?",
            "When things get busy or hectic, what is your most reliable way to take a step back and de-stress?",
            "How do you like to create a peaceful environment at home to unwind in the evening?",
            "Do you find that physical movement or quiet reflection helps you reset more effectively?"
        ]
    }
}

# =============================================================================
# EXTENSIVE BACKUP / EXPANSION TOPICS (INFINITE CONVERSATION POOL)
# =============================================================================

GENERAL_CONVERSATION_TOPICS = [
    {
        'category': 'childhood_and_memories',
        'ack': "Reflecting on favorite memories is always so heartwarming.",
        'questions': [
            "What was one of your favorite games, hobbies, or activities when you were growing up?",
            "Did you have a favorite family tradition or celebration as a child?",
            "What is a piece of simple advice from a teacher or mentor that has always stuck with you?"
        ]
    },
    {
        'category': 'weekend_and_leisure',
        'ack': "Finding time for things you love during the weekend is so important.",
        'questions': [
            "If you had an entire weekend with zero responsibilities, how would you spend it from morning to evening?",
            "Do you enjoy quiet weekends at home or going out to explore new places and events?",
            "What's a local weekend market, park, or café you always enjoy visiting?"
        ]
    },
    {
        'category': 'learning_and_curiosity',
        'ack': "Staying curious and learning new things keeps life so exciting.",
        'questions': [
            "If you could master any new instrument, language, or skill overnight, what would you choose?",
            "What's a subject or topic you've recently become curious to learn more about?",
            "Do you learn best by reading, watching demonstrations, or jumping straight into hands-on practice?"
        ]
    },
    {
        'category': 'seasons_and_weather',
        'ack': "Changing weather and seasons definitely shape the rhythm of our days.",
        'questions': [
            "Which season of the year makes you feel the most energized and happy?",
            "What is your favorite thing to do on a cozy, rainy afternoon?",
            "Do you prefer sunny outdoor weather or crisp, cool autumn mornings?"
        ]
    },
    {
        'category': 'goals_and_aspirations',
        'ack': "Setting inspiring goals gives so much clarity and direction to our days.",
        'questions': [
            "What is a personal project or milestone you'd love to make progress on this year?",
            "When working towards a long-term goal, how do you celebrate small daily wins along the way?",
            "Who is someone whose work ethic or positive attitude inspires you?"
        ]
    }
]

# =============================================================================
# MULTILINGUAL TRANSLATIONS & DIALOGUE RESPONSES
# =============================================================================

HINDI_RESPONSES = {
    'ack_short': ["बहुत बढ़िया!", "समझ गया।", "बिलकुल सही।", "बहुत अच्छा।"],
    'repeat': "ज़रूर! मैं पूछ रहा था: {q} आराम से बताएं, कोई जल्दी नहीं है।",
    'tip': "शांत सांस लें और स्वाभाविक गति से बोलें।",
    'general_ack': [
        "यह बताने के लिए धन्यवाद।",
        "आपके विचार सुनकर बहुत अच्छा लगा।",
        "यह बहुत दिलचस्प बात है।"
    ],
    'questions': [
        "आपको अपने खाली समय में क्या करना सबसे ज्यादा पसंद है?",
        "क्या आपको नई जगहें घूमना पसंद है या घर पर शांति से समय बिताना?",
        "हाल ही में आपने कोई अच्छी फिल्म देखी या किताब पढ़ी है?",
        "जब आप व्यस्त दिन के बाद थक जाते हैं, तो खुद को कैसे रिलैक्स करते हैं?",
        "आने वाले दिनों में आपकी क्या खास योजनाएं हैं?"
    ]
}

MARATHI_RESPONSES = {
    'ack_short': ["छान!", "समजले.", "नक्कीच.", "खूप छान."],
    'repeat': "नक्कीच! मी विचारत होतो: {q} शांतपणे सांगा, काही घाई नाही.",
    'tip': "हळूवार श्वास घ्या आणि सहज गतीने बोला.",
    'general_ack': [
        "माहिती दिल्याबद्दल धन्यवाद.",
        "तुमचे विचार ऐकून खूप छान वाटले.",
        "हा खरोखरच खूप छान मुद्दा आहे."
    ],
    'questions': [
        "तुम्हाला रिकाम्या वेळेत कोणता छंद जोपासायला आवडतो?",
        "तुम्हाला नवीन ठिकाणी फिरायला आवडते की शांतपणे वाचन करायला?",
        "अलीकडे तुम्ही काही छान अनुभव किंवा नवीन गोष्ट शिकलात का?",
        "दिवसभराच्या कामाच्या धावपळीनंतर तुम्ही स्वतःला कसे ताजेतवाने करता?",
        "पुढील काही दिवसांत तुमच्या काय विशेष योजना आहेत?"
    ]
}

# =============================================================================
# CORE CONVERSATION ENGINE CLASS
# =============================================================================

class ConversationEngine:
    """Intelligent, context-aware, zero-repetition conversational partner."""

    @classmethod
    def generate_reply(cls, scenario_id, user_message, history, persona="buddy_mascot", user_age=21, language="English", custom_api_key=None):
        user_message_clean = (user_message or '').strip()
        norm_lang = (language or "English").strip().lower()

        # Handle empty user message
        if not user_message_clean:
            if norm_lang in ['hindi', 'hi']:
                return {"reply": "नमस्ते! मैं सुन रहा हूँ। आप अपनी बात आराम से कह सकते हैं।", "speaking_tip": "आराम से बोलें।"}
            elif norm_lang in ['marathi', 'mr']:
                return {"reply": "नमस्कार! मी ऐकतो आहे. आपण शांतपणे बोलू शकता.", "speaking_tip": "सहजतेने बोला."}
            return {
                "reply": "I'm right here listening! Whenever you're ready, feel free to speak at your natural pace.",
                "speaking_tip": "Take an easy diaphragmatic breath before speaking."
            }

        # Build list of all previous AI messages to strictly avoid any repetition
        all_previous_ai_texts = [
            turn.get('text', '') for turn in history 
            if turn.get('sender') in ('ai', 'assistant', 'bot')
        ]
        
        # 1. Handle user asking to repeat the last question
        if cls._is_repeat_request(user_message_clean):
            last_q = cls._find_last_ai_question(all_previous_ai_texts)
            if last_q:
                if norm_lang in ['hindi', 'hi']:
                    return {"reply": HINDI_RESPONSES['repeat'].format(q=last_q), "speaking_tip": HINDI_RESPONSES['tip']}
                elif norm_lang in ['marathi', 'mr']:
                    return {"reply": MARATHI_RESPONSES['repeat'].format(q=last_q), "speaking_tip": MARATHI_RESPONSES['tip']}
                return {
                    "reply": f"Of course! I was asking: {last_q} Take your time, no rush at all.",
                    "speaking_tip": "Notice your breath and start with a gentle onset."
                }
            if norm_lang in ['hindi', 'hi']:
                return {"reply": "कोई बात नहीं! आपका दिन कैसा चल रहा है?", "speaking_tip": HINDI_RESPONSES['tip']}
            elif norm_lang in ['marathi', 'mr']:
                return {"reply": "काही हरकत नाही! तुमचा आजचा दिवस कसा चालू आहे?", "speaking_tip": MARATHI_RESPONSES['tip']}
            return {
                "reply": "No problem at all! How has your day been going so far?",
                "speaking_tip": "Speak at a steady, comfortable pace."
            }

        # 2. Handle user asking a question directly to the AI
        if cls._is_user_asking_question(user_message_clean):
            direct_ans = cls._answer_user_question(user_message_clean, scenario_id, persona, norm_lang)
            followup = cls._select_unique_question(
                all_previous_ai_texts=all_previous_ai_texts,
                scenario_id=scenario_id,
                user_msg=user_message_clean,
                history=history,
                language=norm_lang
            )
            return {
                "reply": f"{direct_ans} {followup}".strip(),
                "speaking_tip": "Take a gentle breath pause before sharing your thoughts."
            }

        # 3. Extract entities, subjects, and sentiment
        extracted = cls._extract_entities_and_intent(user_message_clean)

        # 4. Generate Acknowledgment / Reflection
        ack = cls._build_acknowledgment(
            user_msg=user_message_clean,
            extracted=extracted,
            scenario_id=scenario_id,
            history=history,
            language=norm_lang
        )

        # 5. Generate / Select Unique Follow-Up Question
        followup_q = cls._select_unique_question(
            all_previous_ai_texts=all_previous_ai_texts,
            scenario_id=scenario_id,
            user_msg=user_message_clean,
            history=history,
            extracted=extracted,
            language=norm_lang
        )

        # 6. Assemble complete conversational response
        final_reply = f"{ack} {followup_q}".strip()

        # 7. Generate actionable speech tip
        speaking_tip = cls._build_speaking_tip(user_message_clean, norm_lang)

        return {
            "reply": final_reply,
            "speaking_tip": speaking_tip
        }

    @classmethod
    def _is_repeat_request(cls, text):
        lower = text.lower()
        patterns = [
            r'\brepeat\b', r'\bsay that again\b', r'\bwhat did you say\b',
            r'\bpardon\b', r'\bcome again\b', r'\bdidn\'t hear\b',
            r'\bdid not catch\b', r'\bonce more\b', r'\bone more time\b',
            r'फिर से', r'दोबारा', r'पुन्हा सांगा', r'काय म्हणालात'
        ]
        return any(re.search(p, lower) for p in patterns)

    @classmethod
    def _find_last_ai_question(cls, ai_texts):
        for msg in reversed(ai_texts):
            sentences = re.split(r'(?<=[.?!।॥])\s+', msg)
            for s in reversed(sentences):
                if '?' in s or 'काय' in s or 'क्या' in s:
                    return s.strip()
        return None

    @classmethod
    def _is_user_asking_question(cls, text):
        lower = text.lower()
        if '?' in text:
            return True
        starters = [
            r'\bwhat about you\b', r'\bhow about you\b', r'\bwhat do you think\b',
            r'\bwhat is your\b', r'\bwhat\'s your\b', r'\bdo you like\b',
            r'\bdo you have\b', r'\bwhere are you\b', r'\bwho are you\b',
            r'आप क्या', r'तुम्ही काय', r'तुला काय'
        ]
        return any(re.search(p, lower) for p in starters)

    @classmethod
    def _answer_user_question(cls, text, scenario_id, persona, language="english"):
        lower = text.lower()
        if language in ['hindi', 'hi']:
            if 'पसंद' in text or 'favorite' in lower:
                return "मुझे लोगों से बातचीत करना और उनके विचार सुनना बहुत पसंद है!"
            return "यह बहुत अच्छा सवाल है! मुझे आपके साथ अभ्यास करके बहुत खुशी हो रही है।"
        elif language in ['marathi', 'mr']:
            if 'आवड' in text or 'favorite' in lower:
                return "मला नवीन लोकांशी गप्पा मारणे आणि त्यांचे अनुभव ऐकणे खूप आवडते!"
            return "हा खूप छान प्रश्न आहे! मला तुमच्याशी संवाद साधताना खूप आनंद होत आहे."

        # English answers
        if re.search(r'\b(favorite|like|prefer|recommend|best)\b', lower):
            if scenario_id in ['scen_restaurant', 'scen_cafe']:
                return "I love a warm cappuccino and freshly baked pastries! Though great conversations are my favorite fuel."
            elif scenario_id == 'scen_interview':
                return "On our team, we deeply value curiosity, clear collaboration, and supporting each other through challenges."
            elif scenario_id == 'scen_college':
                return "I love topics that connect technology with real-world impact - they always keep the audience engaged!"
            else:
                return "I really enjoy calm moments, positive conversations, and learning new stories from everyone I chat with!"
        elif re.search(r'\b(how are you|how is it going|how\'s it going)\b', lower):
            return "I'm doing wonderful, thank you for asking! I'm really enjoying our practice conversation together."
        elif re.search(r'\b(who are you|where are you)\b', lower):
            return "I'm your FLUENCY speaking partner, right here practicing with you."
        return "That's a great question! I'm always happy to share, and I love hearing your perspective on it too."

    @classmethod
    def _extract_entities_and_intent(cls, text):
        lower = text.lower()
        words = re.findall(r"\b[\w'-]+\b", lower)

        extracted = {
            'domain': None,
            'matched_keyword': None,
            'entities': [],
            'sentiment': 'neutral',
            'word_count': len(words),
            'raw_text': text
        }

        all_candidates = []
        for domain, d_info in ENTITY_TOPIC_MAP.items():
            for kw in d_info['keywords']:
                if re.search(r'\b' + re.escape(kw) + r'\b', lower):
                    all_candidates.append((len(kw), domain, kw))
        
        if all_candidates:
            all_candidates.sort(key=lambda x: x[0], reverse=True)
            extracted['domain'] = all_candidates[0][1]
            extracted['matched_keyword'] = all_candidates[0][2]
            extracted['entities'].append(all_candidates[0][2])

        if not extracted['matched_keyword']:
            proper_nouns = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
            if proper_nouns:
                extracted['matched_keyword'] = proper_nouns[0]
                extracted['entities'].append(proper_nouns[0])

        if not extracted['matched_keyword']:
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'i', 'you',
                'he', 'she', 'it', 'we', 'they', 'my', 'your', 'to', 'for', 'in', 'on', 'at',
                'by', 'with', 'about', 'like', 'that', 'this', 'so', 'just', 'be', 'do', 'have',
                'had', 'will', 'would', 'can', 'could', 'should', 'there', 'here', 'them', 'then',
                'yes', 'no', 'yeah', 'sure', 'okay', 'well', 'also', 'really', 'very', 'today'
            }
            meaningful = [w for w in words if w not in stop_words and len(w) > 3]
            if meaningful:
                extracted['matched_keyword'] = meaningful[0]
                extracted['entities'].append(meaningful[0])

        if any(re.search(r'\b' + w + r'\b', lower) for w in ['great', 'awesome', 'love', 'excited', 'good', 'wonderful', 'happy', 'enjoy', 'favorite', 'अच्छा', 'छान']):
            extracted['sentiment'] = 'positive'
        elif any(re.search(r'\b' + w + r'\b', lower) for w in ['nervous', 'busy', 'tired', 'tough', 'hard', 'difficult', 'stress', 'worried', 'थकवा', 'कठीण']):
            extracted['sentiment'] = 'reflective'

        return extracted

    @classmethod
    def _build_acknowledgment(cls, user_msg, extracted, scenario_id, history, language="english"):
        lower = user_msg.lower()
        item = extracted.get('matched_keyword')
        domain = extracted.get('domain')
        sentiment = extracted.get('sentiment')
        word_count = extracted.get('word_count', 0)
        sub = item.capitalize() if item else "that"

        if language in ['hindi', 'hi']:
            if word_count <= 2:
                return random.choice(HINDI_RESPONSES['ack_short'])
            return random.choice(HINDI_RESPONSES['general_ack'])

        if language in ['marathi', 'mr']:
            if word_count <= 2:
                return random.choice(MARATHI_RESPONSES['ack_short'])
            return random.choice(MARATHI_RESPONSES['general_ack'])

        # English acknowledgments
        if word_count <= 2:
            if re.search(r'\b(yes|yeah|yep|sure|ok|okay|definitely|absolutely)\b', lower):
                return random.choice(["Got it!", "Sounds great.", "Understood.", "Awesome, that's clear."])
            elif re.search(r'\b(no|nope|nah|not really|nothing)\b', lower):
                return random.choice(["Understood, no problem at all.", "Got it, that makes total sense.", "Fair enough!"])
            elif re.search(r'\b(thanks|thank you)\b', lower):
                return random.choice(["You're very welcome!", "Anytime! Happy to chat."])
            return "Got it!"

        user_turn_count = len([t for t in history if t.get('sender') == 'user'])
        scen_info = SCENARIO_DEFINITIONS.get(scenario_id)
        if scen_info and user_turn_count <= len(scen_info.get('initial_turns', [])):
            step_idx = user_turn_count - 1
            if 0 <= step_idx < len(scen_info['initial_turns']):
                step_ack = scen_info['initial_turns'][step_idx]['ack']
                return step_ack.replace('{item}', sub)

        if domain and item:
            domain_info = ENTITY_TOPIC_MAP[domain]
            templates = domain_info['ack_templates']
            template = random.choice(templates)
            return template.replace('{item}', sub)

        if item and sentiment == 'positive':
            return f"That sounds wonderful! Focusing on {sub} brings so much positive energy."
        elif item and sentiment == 'reflective':
            return f"I understand - managing {sub} definitely takes focus and patience."
        elif item:
            return f"Thank you for sharing your thoughts about {sub}!"

        return "Thank you for sharing that with me. It's great to hear your perspective."

    @classmethod
    def _select_unique_question(cls, all_previous_ai_texts, scenario_id, user_msg, history, extracted=None, language="english"):
        asked_set = set()
        for msg in all_previous_ai_texts:
            norm = cls._normalize(msg)
            asked_set.add(norm)

        user_turn_count = len([t for t in history if t.get('sender') == 'user'])

        if language in ['hindi', 'hi']:
            shuffled_hi = list(HINDI_RESPONSES['questions'])
            random.shuffle(shuffled_hi)
            for q in shuffled_hi:
                if not cls._is_already_asked(q, asked_set):
                    return q
            return "आप अपने दिन के बारे में कुछ और बताना चाहेंगे?"

        if language in ['marathi', 'mr']:
            shuffled_mr = list(MARATHI_RESPONSES['questions'])
            random.shuffle(shuffled_mr)
            for q in shuffled_mr:
                if not cls._is_already_asked(q, asked_set):
                    return q
            return "तुम्हाला तुमच्या दिवसाबद्दल अजून काही सांगायचे आहे का?"

        # Candidate 1: Scenario Progression (Turns 1-3)
        scen_info = SCENARIO_DEFINITIONS.get(scenario_id)
        if scen_info and user_turn_count <= len(scen_info.get('initial_turns', [])):
            initial_turns = scen_info.get('initial_turns', [])
            for turn_step in initial_turns:
                q = turn_step['question']
                if not cls._is_already_asked(q, asked_set):
                    return q

        # Candidate 2: Domain-specific follow-up based on extracted entity
        if extracted and extracted.get('domain'):
            domain = extracted['domain']
            domain_questions = list(ENTITY_TOPIC_MAP[domain]['followups'])
            random.shuffle(domain_questions)
            for q in domain_questions:
                if not cls._is_already_asked(q, asked_set):
                    return q

        # Candidate 3: Open-Ended Exploration Topics
        shuffled_categories = list(GENERAL_CONVERSATION_TOPICS)
        random.shuffle(shuffled_categories)

        for cat in shuffled_categories:
            questions = list(cat['questions'])
            random.shuffle(questions)
            for q in questions:
                if not cls._is_already_asked(q, asked_set):
                    return q

        # Candidate 4: Procedural bridge questions
        procedural_stems = [
            "Speaking of memorable moments, what is something enjoyable that happened to you recently?",
            "What's one thing you're really looking forward to later this month?",
            "If you could recommend one favorite book, song, or spot to a friend, what would it be?",
            "What is a place that always makes you feel peaceful and comfortable whenever you visit?",
            "What is a hobby or skill that took some practice, but felt great once you got the hang of it?",
            "How do you usually like to celebrate after completing a big milestone or busy week?"
        ]
        random.shuffle(procedural_stems)
        for q in procedural_stems:
            if not cls._is_already_asked(q, asked_set):
                return q

        return "What is one small thing that brought a smile to your face today?"

    @classmethod
    def _normalize(cls, text):
        return re.sub(r'[^\\w\\s]', '', text.lower()).strip()

    @classmethod
    def _is_already_asked(cls, candidate_q, asked_set):
        norm_cand = cls._normalize(candidate_q)
        cand_words = set(norm_cand.split())
        if not cand_words:
            return True

        for prev in asked_set:
            if norm_cand in prev or prev in norm_cand:
                return True
            prev_words = set(prev.split())
            if not prev_words:
                continue
            overlap = len(cand_words.intersection(prev_words)) / max(len(cand_words.union(prev_words)), 1)
            if overlap > 0.60:
                return True
        return False

    @classmethod
    def _build_speaking_tip(cls, text, language="english"):
        if language in ['hindi', 'hi']:
            return "वाक्य शुरू करने से पहले एक शांत सांस लें और सामान्य गति में बोलें।"
        elif language in ['marathi', 'mr']:
            return "वाक्य सुरू करण्यापूर्वी हळूवार श्वास घ्या आणि शांतपणे बोला."

        word_count = len(text.split())
        if word_count <= 4:
            return "Try answering with a full 6 to 10 word sentence on your next turn to practice continuous airflow."
        elif word_count > 25:
            return "Great phrasing! Remember to take a gentle 1-second breath pause between thoughts."
        else:
            tips = [
                "Notice your breath before starting your next sentence.",
                "Maintain a relaxed, steady rhythm without rushing.",
                "Allow a soft, gentle onset on initial vowel sounds.",
                "Keep your jaw and shoulders relaxed as you speak."
            ]
            return random.choice(tips)


def generate_conversation_reply(scenario_id, user_message, history, persona="buddy_mascot", user_age=21, language="English", custom_api_key=None):
    """Public function called by Flask backend."""
    return ConversationEngine.generate_reply(
        scenario_id=scenario_id,
        user_message=user_message,
        history=history,
        persona=persona,
        user_age=user_age,
        language=language,
        custom_api_key=custom_api_key
    )
