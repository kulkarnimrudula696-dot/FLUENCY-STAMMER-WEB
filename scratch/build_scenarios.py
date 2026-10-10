import json

CONVERSATION_SCENARIOS = [
    {
        "id": "scen_intro",
        "title": "Introducing Yourself",
        "icon": "👋",
        "category": "Social & Confidence",
        "age_min": 6,
        "difficulty": "Easy & Friendly",
        "context": "You are meeting someone new at a community gathering, club, or social event. Practice introducing your name, background, hobbies, and interests with a calm, friendly tone.",
        "ai_initial_message": "Hello there! Welcome! I don't think we've met yet. I'm Alex. Could you tell me a little bit about yourself?",
        "suggested_user_openings": [
            "Hi Alex! Nice to meet you. My name is...",
            "Hello! I recently joined and wanted to connect with people here...",
            "Hi there! I'm really excited to be here. A little about me is..."
        ],
        "translations": {
            "Hindi": {
                "title": "अपना परिचय देना (Introducing Yourself)",
                "context": "आप किसी नए कार्यक्रम या सभा में किसी नए व्यक्ति से मिल रहे हैं। अपने नाम, रुचियों और पृष्ठभूमि के बारे में शांति से बताएं।",
                "ai_initial_message": "नमस्ते! स्वागत है आपका! मुझे लगता है हम पहले नहीं मिले हैं। मैं एलेक्स हूँ। क्या आप मुझे अपने बारे में कुछ बता सकते हैं?",
                "suggested_user_openings": [
                    "नमस्ते एलेक्स! आपसे मिलकर खुशी हुई। मेरा नाम...",
                    "नमस्ते! मैं यहाँ नया हूँ और नए लोगों से जुड़ना चाहता हूँ...",
                    "हेलो! मैं यहाँ आकर बहुत खुश हूँ। मेरे बारे में कुछ बातें..."
                ]
            },
            "Marathi": {
                "title": "स्वतःची ओळख करून देणे (Introducing Yourself)",
                "context": "तुम्ही एका सामाजिक कार्यक्रमात किंवा मित्रांच्या मेळाव्यात नवीन व्यक्तीला भेटत आहात. तुमचे नाव, छंद आणि आवडीनिवडी शांतपणे सांगा.",
                "ai_initial_message": "नमस्कार! तुमचे स्वागत आहे! मला वाटते आपण आधी भेटलो नाही. मी ॲलेक्स. तुम्ही मला तुमच्याबद्दल थोडे सांगू शकता का?",
                "suggested_user_openings": [
                    "नमस्कार ॲलेक्स! तुम्हाला भेटून आनंद झाला. माझे नाव...",
                    "हॅलो! मी येथे नवीन आलो आहे आणि नवीन मित्रांशी संवाद साधू इच्छितो...",
                    "नमस्कार! मला येथे येऊन खूप आनंद झाला. माझ्याबद्दल सांगायचे तर..."
                ]
            },
            "Spanish": {
                "title": "Presentarse (Introducing Yourself)",
                "context": "Estás conociendo a alguien nuevo en un evento social. Practica presentarte con calma y confianza.",
                "ai_initial_message": "¡Hola! ¡Bienvenido! Creo que aún no nos conocemos. Soy Alex. ¿Podrías contarme un poco sobre ti?",
                "suggested_user_openings": [
                    "¡Hola Alex! Encantado de conocerte. Mi nombre es...",
                    "¡Hola! Hace poco me uní y quería conocer a gente nueva...",
                    "¡Buenas! Estoy muy emocionado de estar aquí..."
                ]
            },
            "French": {
                "title": "Se présenter (Introducing Yourself)",
                "context": "Vous rencontrez quelqu'un lors d'un événement social. Présentez-vous avec calme et clarté.",
                "ai_initial_message": "Bonjour et bienvenue ! Je ne crois pas que nous nous soyons déjà rencontrés. Je m'appelle Alex. Peux-tu me parler un peu de toi ?",
                "suggested_user_openings": [
                    "Bonjour Alex ! Ravi de faire ta connaissance. Je m'appelle...",
                    "Salut ! Je viens d'arriver et je voulais faire de nouvelles rencontres...",
                    "Bonjour ! Je suis ravi d'être ici aujourd'hui..."
                ]
            },
            "German": {
                "title": "Sich vorstellen (Introducing Yourself)",
                "context": "Du triffst jemanden auf einer Veranstaltung. Stelle dich ruhig und freundlich vor.",
                "ai_initial_message": "Hallo und herzlich willkommen! Ich glaube, wir kennen uns noch nicht. Ich bin Alex. Magst du mir ein wenig über dich erzählen?",
                "suggested_user_openings": [
                    "Hallo Alex! Schön, dich kennenzulernen. Mein Name ist...",
                    "Hallo! Ich bin neu hier und wollte mich vernetzen...",
                    "Hi! Ich freue mich sehr, heute hier zu sein..."
                ]
            }
        }
    },
    {
        "id": "scen_friend",
        "title": "Talking with a Friend",
        "icon": "☕",
        "category": "Casual & Social",
        "age_min": 6,
        "difficulty": "Easy & Relaxed",
        "context": "You meet a good friend at a cozy coffee shop to catch up on each other's week, share weekend plans, and talk about what is new in your lives.",
        "ai_initial_message": "Hey! It's so great to see you! How has your week been going so far? Anything exciting happen?",
        "suggested_user_openings": [
            "Hey! It's great to see you too. My week has been pretty busy with...",
            "Hi! I'm so glad we caught up. Honestly, I had a really fun weekend...",
            "Hey! Things have been going well. I've been working on a few new projects..."
        ],
        "translations": {
            "Hindi": {
                "title": "दोस्त से बातचीत (Talking with a Friend)",
                "context": "आप एक कैफ़े में अपने दोस्त से मिल रहे हैं। अपने सप्ताह की बातें, योजनाएँ और अनुभव साझा करें।",
                "ai_initial_message": "अरे! तुम्हें देखकर बहुत अच्छा लगा! तुम्हारा सप्ताह कैसा रहा? कुछ नया या दिलचस्प हुआ?",
                "suggested_user_openings": [
                    "अरे! तुमसे मिलकर बहुत खुशी हुई। मेरा हफ्ता काफी व्यस्त रहा...",
                    "नमस्ते दोस्त! अच्छा हुआ हम मिले। पिछले कुछ दिनों में...",
                    "सब बढ़िया चल रहा है! मैं कुछ नई चीज़ों पर काम कर रहा हूँ..."
                ]
            },
            "Marathi": {
                "title": "मित्राशी गप्पा मारणे (Talking with a Friend)",
                "context": "तुम्ही तुमच्या जवळच्या मित्राला भेटत आहात. आठवड्यातील घडामोडी, अनुभव आणि भविष्यातील योजनांवर गप्पा मारा.",
                "ai_initial_message": "अरे मित्रा! तुला भेटून खूप छान वाटले! तुझा हा आठवडा कसा गेला? काही विशेष घडले का?",
                "suggested_user_openings": [
                    "अरे! तुलाही भेटून आनंद झाला. हा आठवडा बराच धावपळीचा होता...",
                    "हॅलो! छान झाले आपण भेटलो. मला तुला काही सांगायचे होते...",
                    "सर्व काही छान चालू आहे. मी सध्या काही नवीन गोष्टी शिकत आहे..."
                ]
            }
        }
    },
    {
        "id": "scen_college",
        "title": "College Conversation",
        "icon": "🎓",
        "category": "Academic & Campus",
        "age_min": 6,
        "difficulty": "Casual & Discussion",
        "context": "You and your classmate are in the campus library discussing an upcoming presentation, coursework, and study schedules.",
        "ai_initial_message": "Hey! Glad we could meet up at the library. For our upcoming presentation, do you have any ideas you'd like us to explore together?",
        "suggested_user_openings": [
            "I was thinking we could present on renewable energy and smart technology...",
            "What if we compared artificial intelligence applications in daily life?",
            "I'd love to focus on practical case studies that keep the audience engaged..."
        ],
        "translations": {
            "Hindi": {
                "title": "कॉलेज में सहपाठी से बातचीत (College Conversation)",
                "context": "आप लाइब्रेरी में अपने सहपाठी के साथ प्रोजेक्ट और असाइनमेंट पर चर्चा कर रहे हैं।",
                "ai_initial_message": "अरे! अच्छा हुआ हम लाइब्रेरी में मिल गए। हमारे प्रेजेंटेशन के लिए तुम्हारे पास क्या विचार हैं?",
                "suggested_user_openings": [
                    "मैं सोच रहा था कि हम पर्यावरण और नई तकनीक पर बात कर सकते हैं...",
                    "क्या हम आर्टिफिशियल इंटेलिजेंस के दैनिक उपयोग पर प्रोजेक्ट बना सकते हैं?",
                    "मुझे लगता है कि हमें कुछ वास्तविक उदाहरणों पर ध्यान देना चाहिए..."
                ]
            },
            "Marathi": {
                "title": "कॉलेजमधील सहकाऱ्याशी चर्चा (College Conversation)",
                "context": "तुम्ही कॉलेजच्या ग्रंथालयात सहकाऱ्यासोबत प्रेझेंटेशन आणि अभ्यासावर चर्चा करत आहात.",
                "ai_initial_message": "हॅलो! छान झाले आपण लायब्ररीत भेटलो. आपल्या आगामी प्रेझेंटेशनसाठी तुझ्या डोक्यात काही छान कल्पना आहेत का?",
                "suggested_user_openings": [
                    "मी विचार करत होतो की आपण नवीन तंत्रज्ञानावर सादरीकरण करू शकतो...",
                    "आपण प्रत्यक्ष उदाहरणे देऊन प्रेझेंटेशन अधिक प्रभावी करू शकतो का?",
                    "मला वाटते आपण विषयाची विभागणी करून घेऊया..."
                ]
            }
        }
    },
    {
        "id": "scen_interview",
        "title": "Job Interview",
        "icon": "💼",
        "category": "Career & Professional",
        "age_min": 6,
        "difficulty": "Medium & Professional",
        "context": "You are interviewing with a welcoming hiring manager who wants to understand your background, key strengths, and problem-solving approach.",
        "ai_initial_message": "Thank you so much for joining me today. To get started, could you walk me through your background and what excites you about this opportunity?",
        "suggested_user_openings": [
            "Thank you for having me. Over the past few years, I have focused on...",
            "Good morning. I have a strong passion for problem solving and collaborative teamwork...",
            "I'm excited to be here. My background combines strong analytical skills with creative execution..."
        ],
        "translations": {
            "Hindi": {
                "title": "नौकरी का साक्षात्कार (Job Interview)",
                "context": "आप एक इंटरव्यू में हैं जहाँ साक्षात्कारकर्ता आपकी पृष्ठभूमि, शक्तियों और कार्यशैली को समझना चाहते हैं।",
                "ai_initial_message": "आज हमारे साथ जुड़ने के लिए बहुत धन्यवाद। शुरुआत करने के लिए, क्या आप मुझे अपनी पृष्ठभूमि और इस पद के प्रति अपनी रुचि के बारे में बता सकते हैं?",
                "suggested_user_openings": [
                    "मुझे यह अवसर देने के लिए धन्यवाद। पिछले कुछ वर्षों में मैंने...",
                    "नमस्ते। मुझे नई चुनौतियों को हल करने और टीम में काम करने में गहरी रुचि है...",
                    "मैं यहाँ उपस्थित होकर बहुत उत्साहित हूँ। मेरी पृष्ठभूमि में..."
                ]
            },
            "Marathi": {
                "title": "नोकरीची मुलाखत (Job Interview)",
                "context": "तुम्ही नोकरीच्या मुलाखतीत आहात. तुमची शैक्षणिक पार्श्वभूमी, कौशल्ये आणि अनुभव स्पष्टपणे सांगा.",
                "ai_initial_message": "आज मुलाखतीस उपस्थित राहिल्याबद्दल धन्यवाद. सुरुवातीला, तुम्ही मला तुमची पार्श्वभूमी आणि या संधीबद्दल काय वाटते ते सांगू शकाल का?",
                "suggested_user_openings": [
                    "मला ही संधी दिल्याबद्दल धन्यवाद. मागील काही वर्षांत मी...",
                    "नमस्कार. मला नवीन समस्यांचे निराकरण करणे आणि सांघिक कार्य करणे आवडते...",
                    "मी येथे येऊन खूप उत्सुक आहे. माझ्या कौशल्यांमध्ये..."
                ]
            }
        }
    },
    {
        "id": "scen_restaurant",
        "title": "Restaurant / Ordering Food",
        "icon": "🍽️",
        "category": "Everyday Situations",
        "age_min": 6,
        "difficulty": "Easy & Practical",
        "context": "You are dining at a nice restaurant. The server greets you, introduces the daily specials, and asks for your food and drink orders.",
        "ai_initial_message": "Good evening! Welcome to the Bistro. Tonight our chef's special is fresh garden pasta and creamy roasted tomato soup. What can I get started for you?",
        "suggested_user_openings": [
            "Good evening! Could I please start with a sparkling water and a side salad?",
            "Hi! Everything smells amazing. Could you tell me more about the chef's special pasta?",
            "Hello! I'd like to order the grilled vegetable sandwich and a warm soup, please."
        ],
        "translations": {
            "Hindi": {
                "title": "रेस्टोरेंट में खाना ऑर्डर करना (Restaurant / Ordering Food)",
                "context": "आप एक अच्छे रेस्टोरेंट में हैं। वेटर आपका स्वागत करता है और आपसे ऑर्डर मांगता है।",
                "ai_initial_message": "शुभ संध्या! बिस्ट्रो में आपका स्वागत है। आज हमारे शेफ की विशेष डिश पास्ता और टोमैटो सूप है। आप क्या लेना पसंद करेंगे?",
                "suggested_user_openings": [
                    "नमस्ते! क्या मुझे पहले पानी और एक ताज़ा सलाद मिल सकता है?",
                    "नमस्ते! क्या आप मुझे आज के विशेष व्यंजन के बारे में बता सकते हैं?",
                    "हेलो! मैं एक वेज सैंडविच और गर्म सूप ऑर्डर करना चाहता हूँ।"
                ]
            },
            "Marathi": {
                "title": "रेस्टॉरंटमध्ये जेवण ऑर्डर करणे (Restaurant / Ordering Food)",
                "context": "तुम्ही रेस्टॉरंटमध्ये जेवायला गेला आहात. वेटरशी संवाद साधून तुमच्या आवडीचे जेवण ऑर्डर करा.",
                "ai_initial_message": "शुभ संध्याकाळ! आमच्या रेस्टॉरंटमध्ये आपले स्वागत आहे. आजचा आमचा स्पेशल मेनू पास्ता आणि गरम सूप आहे. आपण काय ऑर्डर करू इच्छिता?",
                "suggested_user_openings": [
                    "नमस्कार! मला सुरुवातीला पाणी आणि एक सॅलड हवे आहे...",
                    "हॅलो! आजच्या स्पेशल डिशबद्दल अधिक माहिती सांगू शकाल का?",
                    "नमस्कार! मला एक व्हेज सँडविच आणि गरम टोमॅटो सूप हवे आहे."
                ]
            }
        }
    },
    {
        "id": "scen_shopping",
        "title": "Shopping",
        "icon": "🛍️",
        "category": "Retail & Everyday",
        "age_min": 6,
        "difficulty": "Easy & Interactive",
        "context": "You are shopping in a department or electronics store looking for a particular product, checking sizes, features, prices, and discounts.",
        "ai_initial_message": "Hello! Welcome to our store. Are you looking for anything specific today, or can I help you find sizes and styles?",
        "suggested_user_openings": [
            "Hi! I'm looking for a comfortable jacket for cool weather. Where might I find those?",
            "Hello! Do you have this shirt in a medium size and different colors?",
            "Hi there! I was looking for wireless headphones with good battery life..."
        ],
        "translations": {
            "Hindi": {
                "title": "दुकान में खरीदारी (Shopping)",
                "context": "आप एक स्टोर में कपड़े या इलेक्ट्रॉनिक सामान देख रहे हैं और सेल्स पर्सन से सहायता ले रहे हैं।",
                "ai_initial_message": "नमस्ते! हमारी दुकान में आपका स्वागत है। क्या आप आज कुछ खास ढूंढ रहे हैं, या मैं आपकी कोई मदद कर सकता हूँ?",
                "suggested_user_openings": [
                    "नमस्ते! मैं हल्के मौसम के लिए एक अच्छी जैकेट ढूंढ रहा हूँ...",
                    "हेलो! क्या यह शर्ट मीडियम साइज और दूसरे रंगों में उपलब्ध है?",
                    "नमस्ते! मुझे अच्छी बैटरी वाले हेडफोन देखने हैं..."
                ]
            },
            "Marathi": {
                "title": "दुकानात खरेदी करणे (Shopping)",
                "context": "तुम्ही दुकानात कपडे किंवा इतर वस्तू खरेदी करत आहात. दुकानदाराशी संवाद साधून योग्य वस्तू निवडा.",
                "ai_initial_message": "नमस्कार! आमच्या दुकानात आपले स्वागत आहे. आपण आज काही खास शोधत आहात का, मी आपल्याला मदत करू का?",
                "suggested_user_openings": [
                    "नमस्कार! मला थंडीच्या दिवसांसाठी एक छान जॅकेट पाहायचे आहे...",
                    "हॅलो! हा शर्ट मिडीयम साईझ आणि इतर रंगांमध्ये मिळेल का?",
                    "नमस्कार! मला चांगल्या दर्जाचे हेडफोन्स पाहायचे आहेत..."
                ]
            }
        }
    },
    {
        "id": "scen_directions",
        "title": "Asking for Directions",
        "icon": "🗺️",
        "category": "Travel & Navigation",
        "age_min": 6,
        "difficulty": "Easy & Helpful",
        "context": "You are walking in a new neighborhood or town and need assistance finding the central train station, city park, or local landmark.",
        "ai_initial_message": "Excuse me! You look like you might be looking for something. Can I help point you in the right direction?",
        "suggested_user_openings": [
            "Hi! Yes, please. Could you tell me the best way to walk to the central train station?",
            "Hello! I'm trying to find the city art museum. Is it within walking distance from here?",
            "Excuse me, do you know if there is a metro station or bus stop nearby?"
        ],
        "translations": {
            "Hindi": {
                "title": "रास्ता पूछना (Asking for Directions)",
                "context": "आप एक नए शहर में हैं और किसी स्थानीय व्यक्ति से रेलवे स्टेशन या मुख्य चौराहे का रास्ता पूछ रहे हैं।",
                "ai_initial_message": "नमस्ते! ऐसा लगता है कि आप रास्ता ढूंढ रहे हैं। क्या मैं आपको सही दिशा बता सकता हूँ?",
                "suggested_user_openings": [
                    "नमस्ते! क्या आप मुझे सेंट्रल रेलवे स्टेशन जाने का रास्ता बता सकते हैं?",
                    "हेलो! मुझे सिटी म्यूजियम जाना है, क्या वह यहाँ से पैदल दूरी पर है?",
                    "माफ़ कीजियेगा, क्या यहाँ पास में कोई मेट्रो स्टेशन या बस स्टॉप है?"
                ]
            },
            "Marathi": {
                "title": "रस्ता विचारणे (Asking for Directions)",
                "context": "तुम्ही नवीन शहरात फिरत आहात आणि रेल्वे स्टेशन किंवा मुख्य उद्यानाचा रस्ता विचारत आहात.",
                "ai_initial_message": "नमस्कार! असे वाटते की आपण पत्ता शोधत आहात. मी आपल्याला योग्य रस्ता दाखवू का?",
                "suggested_user_openings": [
                    "नमस्कार! कृपया मला मुख्य रेल्वे स्टेशनकडे जाण्याचा मार्ग सांगाल का?",
                    "हॅलो! मला सार्वजनिक वाचनालय शोधायचे आहे, ते इथून जवळ आहे का?",
                    "माफ करा, जवळच काही बस स्टॉप किंवा मेट्रो स्टेशन आहे का?"
                ]
            }
        }
    },
    {
        "id": "scen_teacher",
        "title": "Talking to a Teacher",
        "icon": "📚",
        "category": "Education & Mentorship",
        "age_min": 6,
        "difficulty": "Respectful & Clear",
        "context": "You visit your teacher or professor during office hours to ask for guidance on an assignment, clarify a challenging concept, or seek project advice.",
        "ai_initial_message": "Hello! Come on in and have a seat. What topic or assignment would you like to discuss today?",
        "suggested_user_openings": [
            "Hello Professor! I wanted to get your feedback on my initial essay outline...",
            "Good morning! I had a few questions about the problem set we covered in yesterday's lecture...",
            "Hi! I'm preparing for the upcoming exam and wanted to clarify a few key concepts..."
        ],
        "translations": {
            "Hindi": {
                "title": "शिक्षक से बातचीत (Talking to a Teacher)",
                "context": "आप अपने शिक्षक से मिलकर किसी विषय, असाइनमेंट या मार्गदर्शन पर चर्चा कर रहे हैं।",
                "ai_initial_message": "नमस्ते! अंदर आइए और बैठिए। आज आप किस विषय या असाइनमेंट पर चर्चा करना चाहते हैं?",
                "suggested_user_openings": [
                    "नमस्ते सर! मैं अपने प्रोजेक्ट की रूपरेखा पर आपकी राय जानना चाहता था...",
                    "शुभ प्रभात! कल की कक्षा के कुछ सवालों को लेकर मेरे मन में कुछ शंकाएं थीं...",
                    "नमस्ते! परीक्षा की तैयारी के लिए मुझे कुछ बिंदुओं को स्पष्ट करना था..."
                ]
            },
            "Marathi": {
                "title": "शिक्षकांशी संवाद (Talking to a Teacher)",
                "context": "तुम्ही शिक्षकांशी किंवा प्राध्यापकांशी अभ्यासाबद्दल आणि प्रोजेक्टबद्दल मार्गदर्शन घेत आहात.",
                "ai_initial_message": "नमस्कार! या, बसा. आज तुम्हाला कोणत्या विषयावर किंवा अभ्यासावर चर्चा करायची आहे?",
                "suggested_user_openings": [
                    "नमस्कार सर! मला माझ्या प्रोजेक्टच्या विषयाबद्दल आपले मार्गदर्शन हवे होते...",
                    "शुभ सकाळ! काल शिकवलेल्या धड्यातील काही मुद्दे मला पुन्हा समजून घ्यायचे आहेत...",
                    "नमस्कार! आगामी परीक्षेच्या तयारीबद्दल मला काही शंका विचारायच्या आहेत..."
                ]
            }
        }
    },
    {
        "id": "scen_doctor",
        "title": "Doctor Appointment",
        "icon": "🩺",
        "category": "Health & Wellness",
        "age_min": 6,
        "difficulty": "Calm & Descriptive",
        "context": "You are at a routine health checkup or clinic consultation. The doctor gently asks how you have been feeling, your symptoms, and daily wellness habits.",
        "ai_initial_message": "Good morning! Please have a seat. How have you been feeling lately, and what brings you in for a visit today?",
        "suggested_user_openings": [
            "Good morning Doctor. I came in for a routine annual checkup and wellness review...",
            "Hello Doctor. I've been feeling a bit tired lately and wanted to check if everything is in order...",
            "Hi Doctor. I had a slight cough and seasonal allergies and wanted some advice..."
        ],
        "translations": {
            "Hindi": {
                "title": "डॉक्टर से परामर्श (Doctor Appointment)",
                "context": "आप क्लिनिक में डॉक्टर से अपनी सेहत, दिनचर्या और स्वास्थ्य संबंधी परामर्श ले रहे हैं।",
                "ai_initial_message": "शुभ प्रभात! कृपया बैठिए। आप हाल ही में कैसा महसूस कर रहे हैं, और आज आने का क्या कारण है?",
                "suggested_user_openings": [
                    "नमस्ते डॉक्टर। मैं नियमित स्वास्थ्य जांच के लिए आया हूँ...",
                    "नमस्ते डॉक्टर। मुझे पिछले कुछ दिनों से थोड़ी थकान महसूस हो रही है...",
                    "हेलो डॉक्टर। मौसम बदलने की वजह से मुझे हल्की खाँसी और एलर्जी है..."
                ]
            },
            "Marathi": {
                "title": "डॉक्टरांचा सल्ला (Doctor Appointment)",
                "context": "तुम्ही क्लिनिकमध्ये डॉक्टरांना भेटत आहात आणि तुमच्या आरोग्याबद्दल माहिती देत आहात.",
                "ai_initial_message": "शुभ सकाळ! कृपया बसा. अलीकडे तुमची तब्येत कशी आहे आणि आज येण्याचे कारण काय?",
                "suggested_user_openings": [
                    "नमस्कार डॉक्टर. मी नियमित आरोग्य तपासणीसाठी आलो आहे...",
                    "हॅलो डॉक्टर. मला काही दिवसांपासून थोडा थकवा जाणवत आहे...",
                    "नमस्कार डॉक्टर. हवामानातील बदलामुळे मला सर्दी आणि खोकल्याचा त्रास होतो आहे..."
                ]
            }
        }
    },
    {
        "id": "scen_phone",
        "title": "Phone Call",
        "icon": "📞",
        "category": "Practical Life",
        "age_min": 6,
        "difficulty": "Practical & Structured",
        "context": "You are making a phone call to a customer support desk or clinic reception to book an appointment, check timings, and ask questions over the phone.",
        "ai_initial_message": "Thank you for calling City Care Center. This is Taylor speaking. How may I assist you today?",
        "suggested_user_openings": [
            "Hello Taylor! I would like to schedule an appointment for next Tuesday afternoon, please...",
            "Hi! I'm calling to check your available consultation slots for this Thursday...",
            "Good morning! I wanted to confirm the timings and details for my upcoming visit..."
        ],
        "translations": {
            "Hindi": {
                "title": "फ़ोन कॉल पर बातचीत (Phone Call)",
                "context": "आप किसी सर्विस सेंटर या क्लिनिक में फ़ोन करके अपॉइंटमेंट बुक कर रहे हैं या जानकारी ले रहे हैं।",
                "ai_initial_message": "सिटी केयर सेंटर में कॉल करने के लिए धन्यवाद। मैं टेलर बोल रहा हूँ। आज मैं आपकी क्या सहायता कर सकता हूँ?",
                "suggested_user_openings": [
                    "नमस्ते! मैं अगले मंगलवार के लिए एक अपॉइंटमेंट बुक करना चाहता हूँ...",
                    "हेलो! मैं इस गुरुवार के समय और स्लॉट की जानकारी लेने के लिए कॉल कर रहा हूँ...",
                    "शुभ प्रभात! मुझे अपनी आगामी मुलाकात के समय की पुष्टि करनी थी..."
                ]
            },
            "Marathi": {
                "title": "फोनवर संभाषण (Phone Call)",
                "context": "तुम्ही सेवा केंद्रात किंवा क्लिनिकमध्ये फोन करून अपॉइंटमेंट बुक करत आहात.",
                "ai_initial_message": "सिटी केअर सेंटरमध्ये कॉल केल्याबद्दल धन्यवाद. मी टेलर बोलत आहे. मी आज आपली काय मदत करू शकतो?",
                "suggested_user_openings": [
                    "नमस्कार! मला पुढील मंगळवारसाठी अपॉइंटमेंट घ्यायची होती...",
                    "हॅलो! मी या आठवड्यातील उपलब्ध वेळेची माहिती घेण्यासाठी फोन केला आहे...",
                    "शुभ सकाळ! मला माझ्या भेटीची वेळ निश्चित करायची होती..."
                ]
            }
        }
    }
]

print(f"Generated {len(CONVERSATION_SCENARIOS)} scenarios.")
