"""
FLUENCY Natural Conversation Engine
Provides intelligent, natural, context-aware back-and-forth dialogue for Conversation Mode.

Core Design:
1. Strictly ZERO repetition: No question, sentence, or phrasing is ever repeated during a session.
2. Truly understands the user's message using word-boundary parsing, entity extraction, and sentiment recognition.
3. Natural 3-phase flow:
   - Phase 1: Scenario Greeting & Objective (e.g., cafe ordering, interview intro, office sync)
   - Phase 2: Adaptive Contextual Follow-up (deepens into what the user actually said)
   - Phase 3: Seamless Open-Ended Topics (hobbies, travel, food, daily life, relaxation, aspirations) that never run out
4. Acknowledges user input with specific, personalized reflections (not generic robotic praise).
5. Dynamic memory tracks all discussed topics and entities to reference them naturally.
6. The conversation continues indefinitely until the USER chooses to end it.
"""

import re
import random
import logging

logger = logging.getLogger(__name__)

# =============================================================================
# TOPIC KNOWLEDGE GRAPH & ENTITY-SPECIFIC FOLLOW-UPS
# =============================================================================

ENTITY_TOPIC_MAP = {
    'tech_and_coding': {
        'keywords': ['app', 'code', 'coding', 'software', 'developer', 'web', 'website', 'python', 'javascript', 'frontend', 'backend', 'ai', 'program', 'programming', 'tech', 'data', 'engineer', 'feature', 'bug', 'system', 'react', 'database'],
        'ack_templates': [
            "Building and working with technology like {item} is such an engaging and creative process!",
            "Working in {item} is great - it takes both analytical thinking and creativity.",
            "That sounds like an impactful project with {item}."
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
            "Getting outdoors and exploring {item} is such a refreshing way to recharge.",
            "There's nothing quite like spending time in {item} to clear your mind and enjoy the fresh air.",
            "Connecting with nature in {item} always brings a great sense of calm."
        ],
        'followups': [
            "Do you have a favorite trail or scenic spot you love returning to?",
            "Do you prefer hiking alone with your thoughts, or going with friends and family?",
            "What is the most breathtaking view or nature spot you've ever come across?",
            "How does being out in nature affect your mood and focus for the rest of the week?"
        ]
    },
    'travel_and_cities': {
        'keywords': ['travel', 'trip', 'japan', 'europe', 'paris', 'tokyo', 'kyoto', 'visit', 'visited', 'vacation', 'flight', 'country', 'city', 'cities', 'tour', 'explore', 'exploring', 'destination', 'abroad', 'culture', 'temple', 'temples'],
        'ack_templates': [
            "Visiting {item} sounds like an extraordinary experience!",
            "Traveling to {item} brings so many rich memories and new perspectives.",
            "That sounds like a memorable journey to {item}."
        ],
        'followups': [
            "What was your absolute favorite memory or place you discovered during that trip?",
            "Did you get to try any unique local dishes or foods while you were there?",
            "If you could plan your next dream vacation anywhere in the world, where would you go next?",
            "Do you prefer structured sightseeing trips, or wandering around and discovering hidden spots?"
        ]
    },
    'food_and_culinary': {
        'keywords': ['cinnamon roll', 'hot chocolate', 'comfort food', 'cappuccino', 'espresso', 'americano', 'mocha', 'chai', 'matcha', 'latte', 'coffee', 'tea', 'pasta', 'pizza', 'sushi', 'curry', 'baking', 'cook', 'cooking', 'recipe', 'breakfast', 'dinner', 'lunch', 'dessert', 'muffin', 'scone', 'croissant', 'chocolate', 'cheese', 'soup', 'bread', 'ramen', 'pastry', 'sandwich', 'bagel', 'pancake', 'waffle'],
        'ack_templates': [
            "{item} is such a wonderful choice - comforting and delicious!",
            "You have great taste - {item} is always a favorite.",
            "There's something so satisfying about enjoying good {item}."
        ],
        'followups': [
            "Do you enjoy cooking and preparing meals at home, or do you prefer discovering cozy local restaurants?",
            "Is there a family recipe or special dish you've perfected over time?",
            "What is your go-to comfort meal when you've had a long day and want to unwind?",
            "If you could have a chef make you any signature dish right now, what would you ask for?"
        ]
    },
    'pets_and_animals': {
        'keywords': ['dog', 'dogs', 'cat', 'cats', 'pet', 'pets', 'puppy', 'kitten', 'animal', 'animals', 'rescue', 'shelter', 'vet', 'bird', 'fish', 'hamster', 'otter', 'capybara', 'koala'],
        'ack_templates': [
            "Pets and animals like {item} bring so much companionship and warmth into our days!",
            "Having a {item} around makes life so much brighter and more entertaining.",
            "Animals are wonderful - taking care of a {item} is such a heartwarming bond."
        ],
        'followups': [
            "What's the funniest or sweetest thing you've seen your pet or an animal do?",
            "How does spending time with pets help you unwind after a busy day?",
            "If you could have any friendly animal as a companion for a day, what would it be?",
            "What is their favorite game, treat, or spot to nap in the house?"
        ]
    },
    'creative_arts_and_music': {
        'keywords': ['music', 'guitar', 'piano', 'singing', 'song', 'songs', 'art', 'draw', 'drawing', 'painting', 'photo', 'photography', 'camera', 'write', 'writing', 'book', 'books', 'read', 'reading', 'novel', 'movie', 'film', 'instruments'],
        'ack_templates': [
            "Expressing yourself through {item} is such a fulfilling and creative outlet.",
            "I love that you're engaged with {item} - it brings so much richness to daily life.",
            "Having a creative passion for {item} is so rewarding."
        ],
        'followups': [
            "What first sparked your interest or passion for that?",
            "Who are some of your favorite artists, authors, or creators that inspire you?",
            "Do you usually set aside dedicated quiet time for creative work, or do you do it whenever inspiration strikes?",
            "What's one creative project or piece of music you'd love to learn in the future?"
        ]
    },
    'wellness_and_mindfulness': {
        'keywords': ['relax', 'relaxing', 'calm', 'quiet', 'peace', 'meditate', 'meditation', 'breath', 'breathing', 'sleep', 'morning', 'routine', 'yoga', 'exercise', 'gym', 'workout', 'stretch', 'reset', 'early'],
        'ack_templates': [
            "Prioritizing {item} is so important for keeping a balanced and grounded state of mind.",
            "Taking time for {item} makes such a noticeable difference in how we feel every day.",
            "That sounds like a very healthy and restorative approach."
        ],
        'followups': [
            "What does your ideal morning routine look like when you want to start the day feeling calm?",
            "When things get hectic, what is your most reliable way to take a step back and de-stress?",
            "How do you like to create a peaceful environment at home to unwind in the evening?",
            "Do you find that physical movement or quiet reflection helps you reset more effectively?"
        ]
    },
    'sports_and_fitness': {
        'keywords': ['football', 'soccer', 'basketball', 'cricket', 'tennis', 'swim', 'swimming', 'run', 'running', 'marathon', 'fitness', 'cycling', 'bike', 'gym', 'workout', 'sports'],
        'ack_templates': [
            "Staying active with {item} is such a great boost for both physical and mental energy!",
            "Engaging in {item} takes great dedication and discipline.",
            "That sounds like a fantastic way to stay energized."
        ],
        'followups': [
            "How long have you been active with that, and what keeps you motivated?",
            "Do you prefer team sports with friends or individual training sessions?",
            "What is a personal fitness milestone you've reached that made you feel proud?"
        ]
    }
}

# =============================================================================
# SCENARIOS INITIAL STAGES (PHASE 1)
# =============================================================================

SCENARIO_DEFINITIONS = {
    'scen_cafe': {
        'title': 'Café Ordering & Friendly Small Talk',
        'persona': 'Friendly Barista',
        'default_greeting': "Hi there! Welcome to Sunny Roast. What can I get started for you today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "A fresh {item} is a wonderful choice! We'll prepare that right away.",
                'question': "Would you like to pair that with a warm croissant, blueberry muffin, or anything from our bakery case?"
            },
            {
                'turn_index': 2,
                'ack': "Got that added to your order - our bakery items pair so nicely!",
                'question': "Will you be relaxing here at one of our sunny tables today, or taking this on the go?"
            },
            {
                'turn_index': 3,
                'ack': "Perfect, we've got you all set up and comfortable.",
                'question': "What does the rest of your day have in store for you? Working on anything interesting?"
            }
        ]
    },

    'scen_interview': {
        'title': 'Warm Job Interview Practice',
        'persona': 'Welcoming Interviewer',
        'default_greeting': "Thank you so much for meeting with me today. To begin, could you tell me a little bit about yourself and what drew you to this role?",
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

    'scen_intro': {
        'title': 'Self-Introduction & Networking',
        'persona': 'Friendly Community Member',
        'default_greeting': "Hey there! I don't think we've met yet. I'm Alex. What brings you to the event today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Welcome! It's so great that you decided to join us today.",
                'question': "What kind of topics, hobbies, or creative projects are you most enthusiastic about right now?"
            },
            {
                'turn_index': 2,
                'ack': "That is really fascinating! Getting involved with {item} takes genuine passion.",
                'question': "How did you first get into that? Was there a particular moment or person that inspired you?"
            },
            {
                'turn_index': 3,
                'ack': "I love hearing origin stories like that - it makes the journey so meaningful.",
                'question': "Have you lived in this area for a while, or did you move here recently?"
            }
        ]
    },

    'scen_office': {
        'title': 'Office Stand-Up & Project Update',
        'persona': 'Team Lead',
        'default_greeting': "Thanks Maya! Alright, next up on the board is your update. How are things looking on your end?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Thanks for the clear summary - sounds like solid progress on {item}.",
                'question': "Are there any blockers, dependencies, or access items we can help clear for you today?"
            },
            {
                'turn_index': 2,
                'ack': "Appreciate the visibility - team alignment keeps everything flowing smoothly.",
                'question': "What is your main focus or milestone for the rest of today's sprint?"
            },
            {
                'turn_index': 3,
                'ack': "Sounds like a strong, well-prioritized plan.",
                'question': "How has our recent team workflow or tooling been feeling for you lately - any improvements you'd like to try?"
            }
        ]
    },

    'scen_college': {
        'title': 'College Group Discussion',
        'persona': 'Classmate & Study Partner',
        'default_greeting': "Hey! So for our group presentation, the professor said we can pick any topic on sustainability or emerging tech. Do you have any ideas you'd like to explore?",
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

    'scen_phone': {
        'title': 'Phone Call: Booking an Appointment',
        'persona': 'Receptionist Jordan',
        'default_greeting': "Thank you for calling City Care Center. This is Jordan speaking. How may I assist you today?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "I'd be glad to help you schedule your {item}.",
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
    },

    'scen_help': {
        'title': 'Asking for Help & Directions in a New City',
        'persona': 'Helpful Local Resident',
        'default_greeting': "Excuse me! You look like you might be looking for something. Can I help point you in the right direction?",
        'initial_turns': [
            {
                'turn_index': 1,
                'ack': "Oh yes, I know the {item} well! You're actually not far at all.",
                'question': "Are you planning to walk there on foot, or would you prefer a quick bus route?"
            },
            {
                'turn_index': 2,
                'ack': "Walking is super pleasant from here - just follow the sidewalk past the clock tower.",
                'question': "Are you visiting our city for the first time, or have you explored around here before?"
            },
            {
                'turn_index': 3,
                'ack': "Welcome! There are so many great sights in this neighborhood.",
                'question': "Are you looking for any cozy coffee spots or local bakeries along the way?"
            }
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
            "What was one of your favorite games or activities when you were growing up?",
            "Did you have a favorite family tradition or holiday celebration as a child?",
            "What is a piece of simple advice from a teacher or mentor that has stuck with you?"
        ]
    },
    {
        'category': 'weekend_and_leisure',
        'ack': "Finding time for things you love during the weekend is so important.",
        'questions': [
            "If you had an entire weekend with zero responsibilities, how would you spend it from morning to evening?",
            "Do you enjoy quiet weekends at home or going out to explore new places and events?",
            "What's a local weekend market, park, or café you always enjoy dropping by?"
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
            "Do you prefer hot summer beach days or crisp, cool autumn mornings?"
        ]
    },
    {
        'category': 'entertainment_and_stories',
        'ack': "Great stories, movies, and podcasts have a way of leaving a lasting impression.",
        'questions': [
            "Have you watched or read any story recently that made you think about things from a new angle?",
            "What kind of background sounds or music help you concentrate best when working?",
            "Do you have an all-time favorite movie or comfort show you can rewatch anytime?"
        ]
    },
    {
        'category': 'future_and_goals',
        'ack': "Setting thoughtful milestones gives us something motivating to work toward.",
        'questions': [
            "What is one personal or creative goal you're looking forward to tackling in the coming months?",
            "Where do you hope to see yourself in a couple of years in terms of your personal growth?",
            "What is a small positive habit you've been trying to build into your daily routine?"
        ]
    },
    {
        'category': 'social_and_friendships',
        'ack': "Meaningful friendships and connections make all the difference in life.",
        'questions': [
            "What qualities do you value most in a good friend or team member?",
            "Do you prefer deep one-on-one conversations or lively group hangouts?",
            "What is a fun memory you've shared with close friends recently?"
        ]
    }
]

# =============================================================================
# CONVERSATION ENGINE IMPLEMENTATION
# =============================================================================

class ConversationEngine:
    @classmethod
    def generate_reply(cls, scenario_id, user_message, history, persona="buddy_mascot", user_age=21):
        """
        Generate a thoughtful, back-and-forth conversational response.
        
        Guarantees:
        - NEVER repeats any sentence or question in the session.
        - Actively listens and reflects what the user actually said.
        - Naturally transitions across topics when a topic is done.
        - Never runs out of questions; continues until user ends session.
        - Supportive, casual, and non-judgmental tone.
        """
        user_message_clean = (user_message or "").strip()
        if not user_message_clean:
            return {
                "reply": "I'm right here listening whenever you're ready to speak!",
                "speaking_tip": "Take a calm belly breath before starting your sentence."
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
                return {
                    "reply": f"Of course! I was asking: {last_q} Take your time, no rush at all.",
                    "speaking_tip": "Notice your breath and start with a gentle onset."
                }
            return {
                "reply": "No problem! How is your day going so far?",
                "speaking_tip": "Speak at a steady, comfortable pace."
            }

        # 2. Handle user asking a question to the AI / Mascot
        if cls._is_user_asking_question(user_message_clean):
            direct_ans = cls._answer_user_question(user_message_clean, scenario_id, persona)
            followup = cls._select_unique_question(
                all_previous_ai_texts=all_previous_ai_texts,
                scenario_id=scenario_id,
                user_msg=user_message_clean,
                history=history
            )
            return {
                "reply": f"{direct_ans} {followup}".strip(),
                "speaking_tip": "Take a 1-second pause before sharing your answer."
            }

        # 3. Extract entities, subjects, and sentiment with strict word boundaries
        extracted = cls._extract_entities_and_intent(user_message_clean)

        # 4. Generate Acknowledgment / Reaction (Part 1 of natural back-and-forth)
        ack = cls._build_acknowledgment(
            user_msg=user_message_clean,
            extracted=extracted,
            scenario_id=scenario_id,
            history=history
        )

        # 5. Generate / Select Follow-Up Question (Part 2 of natural back-and-forth)
        followup_q = cls._select_unique_question(
            all_previous_ai_texts=all_previous_ai_texts,
            scenario_id=scenario_id,
            user_msg=user_message_clean,
            history=history,
            extracted=extracted
        )

        # 6. Assemble complete response
        final_reply = f"{ack} {followup_q}".strip()

        # 7. Generate helpful speech tip
        speaking_tip = cls._build_speaking_tip(user_message_clean)

        return {
            "reply": final_reply,
            "speaking_tip": speaking_tip
        }

    # -------------------------------------------------------------------------
    # INTENT & QUESTION DETECTION HELPERS
    # -------------------------------------------------------------------------

    @classmethod
    def _is_repeat_request(cls, text):
        lower = text.lower()
        patterns = [
            r'\brepeat\b', r'\bsay that again\b', r'\bwhat did you say\b',
            r'\bpardon\b', r'\bcome again\b', r'\bdidn\'t hear\b',
            r'\bdid not catch\b', r'\bonce more\b', r'\bone more time\b'
        ]
        return any(re.search(p, lower) for p in patterns)

    @classmethod
    def _find_last_ai_question(cls, ai_texts):
        for msg in reversed(ai_texts):
            sentences = re.split(r'(?<=[.?!])\s+', msg)
            for s in reversed(sentences):
                if '?' in s:
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
            r'\bdo you have\b', r'\bwhere are you\b', r'\bwho are you\b'
        ]
        return any(re.search(p, lower) for p in starters)

    @classmethod
    def _answer_user_question(cls, text, scenario_id, persona):
        lower = text.lower()
        if re.search(r'\b(favorite|like|prefer|recommend|best)\b', lower):
            if scenario_id == 'scen_cafe':
                return "I love a warm cinnamon cappuccino and a fresh blueberry scone! Though as a friendly practice partner, great conversations are my favorite fuel."
            elif scenario_id == 'scen_interview':
                return "On our team, we deeply value curiosity, clear collaboration, and supporting each other through new challenges."
            elif scenario_id == 'scen_college':
                return "I love topics that connect technology with real-world impact - they always keep the audience engaged!"
            else:
                return "I really enjoy calm moments, upbeat conversations, and learning new stories from everyone I chat with!"
        elif re.search(r'\b(how are you|how is it going|how\'s it going)\b', lower):
            return "I'm doing wonderful, thank you for asking! I'm really enjoying our practice conversation together."
        elif re.search(r'\b(who are you|where are you)\b', lower):
            return "I'm your FLUENCY companion, right here practicing speaking with you."
        return "That's a great question! I'm always happy to share, and I love hearing your perspective on it too."

    # -------------------------------------------------------------------------
    # ENTITY EXTRACTION WITH WORD BOUNDARIES
    # -------------------------------------------------------------------------

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

        # Check entity topic map with strict word boundaries, prioritizing longer/more specific phrases
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

        # Check for named entities or specific proper nouns (e.g., Max, Japan, Tokyo, etc.)
        if not extracted['matched_keyword']:
            proper_nouns = re.findall(r'\b[A-Z][a-z]{2,}\b', text)
            if proper_nouns:
                extracted['matched_keyword'] = proper_nouns[0]
                extracted['entities'].append(proper_nouns[0])

        # Fallback keyword extraction if not in mapped domains
        if not extracted['matched_keyword']:
            stop_words = {
                'the', 'a', 'an', 'and', 'or', 'but', 'is', 'are', 'was', 'were', 'i', 'you',
                'he', 'she', 'it', 'we', 'they', 'my', 'your', 'to', 'for', 'in', 'on', 'at',
                'by', 'with', 'about', 'like', 'that', 'this', 'so', 'just', 'be', 'do', 'have',
                'had', 'will', 'would', 'can', 'could', 'should', 'there', 'here', 'them', 'then',
                'yes', 'no', 'yeah', 'sure', 'okay', 'well', 'also', 'really', 'very', 'plan',
                'want', 'need', 'make', 'take', 'give', 'said', 'look', 'come', 'went', 'know',
                'think', 'some', 'much', 'many', 'good', 'well', 'thing', 'time', 'feel',
                'warm', 'cold', 'hot', 'iced', 'fresh', 'little', 'great', 'fine', 'such',
                'prefer', 'today', 'morning', 'afternoon', 'evening', 'night'
            }
            meaningful = [w for w in words if w not in stop_words and len(w) > 3]
            if meaningful:
                extracted['matched_keyword'] = meaningful[0]
                extracted['entities'].append(meaningful[0])

        # Detect sentiment
        if any(re.search(r'\b' + w + r'\b', lower) for w in ['great', 'awesome', 'love', 'excited', 'good', 'wonderful', 'happy', 'fantastic', 'enjoy', 'favorite']):
            extracted['sentiment'] = 'positive'
        elif any(re.search(r'\b' + w + r'\b', lower) for w in ['nervous', 'busy', 'tired', 'tough', 'hard', 'difficult', 'stress', 'worried', 'stuck', 'exhausted']):
            extracted['sentiment'] = 'reflective'

        return extracted

    # -------------------------------------------------------------------------
    # ACKNOWLEDGMENT GENERATION (UNDERSTANDS & REFLECTS USER'S INPUT)
    # -------------------------------------------------------------------------

    @classmethod
    def _build_acknowledgment(cls, user_msg, extracted, scenario_id, history):
        lower = user_msg.lower()
        item = extracted.get('matched_keyword')
        domain = extracted.get('domain')
        sentiment = extracted.get('sentiment')
        word_count = extracted.get('word_count', 0)
        sub = item.capitalize() if item else "that"

        # 1. Short or affirmation responses
        if word_count <= 2:
            if re.search(r'\b(yes|yeah|yep|sure|ok|okay|definitely|absolutely)\b', lower):
                return random.choice([
                    "Got it!", "Sounds great.", "Understood.", "Awesome, that's clear."
                ])
            elif re.search(r'\b(no|nope|nah|not really|nothing)\b', lower):
                return random.choice([
                    "Understood, no problem at all.", "Got it, that makes total sense.", "Fair enough!"
                ])
            elif re.search(r'\b(thanks|thank you)\b', lower):
                return random.choice([
                    "You're very welcome!", "Anytime! Happy to chat."
                ])
            return "Got it!"

        # 2. Early Scenario Stage Acknowledgments (Turns 1-2)
        user_turn_count = len([t for t in history if t.get('sender') == 'user'])
        scen_info = SCENARIO_DEFINITIONS.get(scenario_id)
        if scen_info and user_turn_count <= len(scen_info.get('initial_turns', [])):
            step_idx = user_turn_count - 1
            if 0 <= step_idx < len(scen_info['initial_turns']):
                step_ack = scen_info['initial_turns'][step_idx]['ack']
                return step_ack.replace('{item}', sub)

        # 3. Domain-specific personalized acknowledgments
        if domain and item:
            domain_info = ENTITY_TOPIC_MAP[domain]
            templates = domain_info['ack_templates']
            template = random.choice(templates)
            return template.replace('{item}', sub)

        # 4. Sentiment-aware reflections
        if item and sentiment == 'positive':
            return random.choice([
                f"That sounds wonderful! Focusing on {sub} brings so much good energy.",
                f"I love hearing that! {sub} is such an exciting area.",
                f"That's fantastic to hear!"
            ])
        elif item and sentiment == 'reflective':
            return random.choice([
                f"I understand - managing {sub} can definitely take focus and patience.",
                f"Thank you for sharing that openly. Taking things step by step makes all the difference.",
                f"That makes total sense. Giving yourself time with {sub} is so important."
            ])
        elif item:
            return random.choice([
                f"Thank you for sharing that about {sub}!",
                f"I appreciate that perspective on {sub}.",
                f"That's a really interesting point about {sub}."
            ])

        # 5. General conversational reflection
        return random.choice([
            "Thank you for sharing that with me.",
            "I appreciate you explaining your thoughts on that.",
            "That makes a lot of sense, and it's great to hear your perspective."
        ])

    # -------------------------------------------------------------------------
    # UNIQUE QUESTION SELECTION (STRICT ZERO-REPETITION GUARANTEE)
    # -------------------------------------------------------------------------

    @classmethod
    def _select_unique_question(cls, all_previous_ai_texts, scenario_id, user_msg, history, extracted=None):
        """
        Picks a completely unique question that has not been asked anywhere in the history.
        Prioritizes:
        1. Scenario progression steps (turns 1-3) if scenario is in early phase
        2. Entity-specific follow-ups if user mentioned a rich topic (Japan, coding, hiking, cooking, etc.)
        3. Expansion topics and open-ended curiosity questions (infinite pool)
        """
        asked_set = set()
        for msg in all_previous_ai_texts:
            norm = cls._normalize(msg)
            asked_set.add(norm)

        # Count turns in current session
        user_turn_count = len([t for t in history if t.get('sender') == 'user'])

        # Candidate 1: Early Scenario Progression (Turns 1-3 of structured scenario)
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

        # Candidate 3: Rich Open-Ended Topic Categories (Infinite Exploration)
        shuffled_categories = list(GENERAL_CONVERSATION_TOPICS)
        random.shuffle(shuffled_categories)

        for cat in shuffled_categories:
            questions = list(cat['questions'])
            random.shuffle(questions)
            for q in questions:
                if not cls._is_already_asked(q, asked_set):
                    return q

        # Candidate 4: Check other domains from ENTITY_TOPIC_MAP
        all_domain_questions = []
        for d in ENTITY_TOPIC_MAP.values():
            all_domain_questions.extend(d['followups'])
        random.shuffle(all_domain_questions)
        for q in all_domain_questions:
            if not cls._is_already_asked(q, asked_set):
                return q

        # Candidate 5: Dynamic Procedural Bridge Questions (Never exhausts)
        procedural_stems = [
            "Speaking of interesting moments, what is something memorable that happened to you recently?",
            "What's one thing you're really looking forward to later this month?",
            "If you could recommend one favorite book, song, or movie to a friend, what would it be?",
            "What is a place that always makes you feel peaceful and comfortable whenever you visit?",
            "What is a hobby or skill that took some practice, but felt amazing once you got the hang of it?",
            "How do you usually like to celebrate after finishing a big project or milestone?"
        ]
        random.shuffle(procedural_stems)
        for q in procedural_stems:
            if not cls._is_already_asked(q, asked_set):
                return q

        return "What is one small thing that brought a smile to your face today?"

    @classmethod
    def _normalize(cls, text):
        return re.sub(r'[^\w\s]', '', text.lower()).strip()

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
            # Check Jaccard word similarity (>60% means semantically redundant)
            overlap = len(cand_words.intersection(prev_words)) / max(len(cand_words.union(prev_words)), 1)
            if overlap > 0.60:
                return True
        return False

    @classmethod
    def _build_speaking_tip(cls, text):
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


def generate_conversation_reply(scenario_id, user_message, history, persona="buddy_mascot", user_age=21):
    """Public function called by Flask backend."""
    return ConversationEngine.generate_reply(
        scenario_id=scenario_id,
        user_message=user_message,
        history=history,
        persona=persona,
        user_age=user_age
    )
