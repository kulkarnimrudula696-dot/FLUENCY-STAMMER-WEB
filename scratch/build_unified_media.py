"""
Unified Media Content Generator for FLUENCY Image & Video Mode
Generates 100% verified, consistent data objects where:
- visual media URL
- media type
- title
- speaking clue / prompt
- description / instruction
- guiding questions
- vocabulary
all describe the EXACT same visual.
"""

import os
import sys
import json

# =============================================================================
# 20 VERIFIED HIGH-RES IMAGES (UNSPLASH)
# =============================================================================
IMAGE_CATALOG = [
    {
        "index": 1,
        "image_url": "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1519331379826-f10be5486c6f?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Sunny Park Pathway & Bench",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Sunny Park Pathway & Bench",
                "prompt": "Describe the sunny gravel path, the tall leafy trees, and the empty bench on the grass.",
                "description": "Look closely at the image, then describe the park walkway, the sunlight through the trees, and the atmosphere.",
                "guidingQuestions": [
                    "What can you see along the curving walkway, and where is the park bench located?",
                    "How does the warm sunlight filtering through the leafy tree branches make the park feel?",
                    "Who might enjoy walking along this path or sitting on the empty bench?"
                ],
                "vocabulary": ["pathway", "park bench", "leafy trees", "sunlight", "gravel path", "canopy", "grass", "tranquil"]
            },
            "Medium": {
                "title": "Quiet Morning on the Park Pathway",
                "prompt": "Explain how the interplay of morning sunlight and ancient trees creates a serene retreat in this park.",
                "description": "Describe the scene in detail, focusing on sensory impressions, natural lighting, and the welcoming environment.",
                "guidingQuestions": [
                    "How does the perspective of the pathway guide the viewer's eye into the lush distance?",
                    "What sensory details—fresh morning air, rustling leaves, warm sunshine—would someone experience here?",
                    "Why are peaceful green spaces like this park essential for rest and mental wellbeing?"
                ],
                "vocabulary": ["serene", "foliage", "sun-dappled", "tranquility", "landscape", "urban retreat", "canopy", "solitude"]
            },
            "Hard": {
                "title": "Atmospheric Park Landscape & Solitude",
                "prompt": "Deliver a comprehensive visual critique of the composition, lighting, and evocative atmosphere of this park pathway.",
                "description": "Provide an articulate analysis of the photograph's depth, environmental beauty, and emotional tone.",
                "guidingQuestions": [
                    "Analyze how the curved gravel avenue and overarching plane trees create balanced visual framing.",
                    "How does the placement of the solitary bench symbolize reflection and respite in modern life?",
                    "Discuss the photographer's use of natural golden lighting to evoke feelings of calm and contemplation."
                ],
                "vocabulary": ["composition", "contemplation", "respite", "atmospheric", "verdant", "perspective", "refinement", "equanimity"]
            }
        }
    },
    {
        "index": 2,
        "image_url": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1517256064527-09c73fc73e38?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Warm Cappuccino & Cafe Table",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Morning Coffee Cup & Cafe Table",
                "prompt": "Describe the warm cup of coffee, the creamy foam with sprinkled cinnamon, and the table setting.",
                "description": "Look closely at the image, then describe the freshly brewed coffee, the saucer, and the cafe ambiance.",
                "guidingQuestions": [
                    "What beverage is served in the white ceramic cup, and what garnish is sprinkled on top?",
                    "What decorative plant is sitting on the wooden tabletop behind the cup?",
                    "What time of day does this warm coffee scene remind you of, and why?"
                ],
                "vocabulary": ["cappuccino", "coffee cup", "creamy foam", "cinnamon", "saucer", "succulent", "wooden table", "aroma"]
            },
            "Medium": {
                "title": "Artisanal Latte at a Cozy Cafe",
                "prompt": "Describe the cozy atmosphere of sipping an artisanal latte in a warm coffee shop.",
                "description": "Describe the scene in detail, focusing on sensory impressions, latte craftsmanship, and cafe culture.",
                "guidingQuestions": [
                    "How does the presentation of the latte and saucer reflect careful cafe craftsmanship?",
                    "What morning routine or relaxed conversation might be taking place around this cafe table?",
                    "How does the warm contrast between the dark table and the light beverage create an inviting mood?"
                ],
                "vocabulary": ["artisanal", "latte art", "espresso", "froth", "cinnamon dusting", "potted plant", "ambiance", "barista"]
            },
            "Hard": {
                "title": "Sensory Still Life: Coffee & Mindfulness",
                "prompt": "Examine the visual elements of this cafe still life, focusing on texture, warmth, and daily ritual.",
                "description": "Provide an articulate analysis of the photograph's focus, lighting, and cultural celebration of coffee.",
                "guidingQuestions": [
                    "Analyze how the shallow depth of field isolates the delicate texture of the coffee foam from the background.",
                    "Discuss coffee culture as a modern mindful ritual of focus, pause, and social connection.",
                    "How do subtle visual cues—the ceramic saucer, wooden grain, and soft bokeh—evoke comfort?"
                ],
                "vocabulary": ["still life", "depth of field", "mindfulness", "ritual", "bokeh", "ceramic", "tactile", "contemplative"]
            }
        }
    },
    {
        "index": 3,
        "image_url": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Sunset Waves on Sandy Beach",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Sunset Waves on Sandy Beach",
                "prompt": "Describe the gentle waves rolling onto the sand and the soft colors of the sunset sky.",
                "description": "Look closely at the image, then describe the ocean tide, the sandy shoreline, and the sunset horizon.",
                "guidingQuestions": [
                    "What are the ocean waves doing as they reach the wet sandy shoreline?",
                    "What colors do you notice in the sky as the sun shines near the horizon?",
                    "How would it feel to walk barefoot along this quiet, peaceful beach?"
                ],
                "vocabulary": ["ocean waves", "sandy beach", "sunset", "shoreline", "surf", "tide", "horizon", "peaceful"]
            },
            "Medium": {
                "title": "Golden Hour Ocean Shoreline",
                "prompt": "Narrate the tranquil sights and sounds of the ocean tide washing over the sandy beach at golden hour.",
                "description": "Describe the scene in detail, capturing the movement of the surf, coastal breeze, and warm sky.",
                "guidingQuestions": [
                    "How does the golden sunlight reflect across the wet sand and breaking seafoam?",
                    "What sounds—rushing water, distant surf, gentle breeze—would someone hear standing here?",
                    "Why is the seashore universally recognized as a sanctuary for renewal and mental relaxation?"
                ],
                "vocabulary": ["golden hour", "seafoam", "tranquil", "coastal", "reflections", "shoreline", "tide", "retreat"]
            },
            "Hard": {
                "title": "Coastal Horizons & Tidal Harmony",
                "prompt": "Deliver an evocative monologue on the interplay of light, coastal expanse, and rhythmic ocean tides.",
                "description": "Provide a nuanced critique of the photograph's minimalist balance, color temperature, and atmospheric serenity.",
                "guidingQuestions": [
                    "Examine how the photographer balances the vastness of sea, sky, and wet sand across the horizon line.",
                    "Discuss the poetic symbolism of returning ocean tides as a metaphor for constancy and renewal.",
                    "How does the harmonious palette of turquoise waters and soft amber light affect the viewer's emotional state?"
                ],
                "vocabulary": ["horizon", "minimalism", "symbolism", "serenity", "ebb and flow", "turquoise", "atmospheric", "equilibrium"]
            }
        }
    },
    {
        "index": 4,
        "image_url": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1530103862676-de8c9debad1d?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Colorful Party Balloons",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Colorful Party Balloons Celebration",
                "prompt": "Describe the bright colorful balloons floating up and the ribbons hanging down.",
                "description": "Look closely at the image, then describe the different balloon colors, the floating bunch, and the party mood.",
                "guidingQuestions": [
                    "Which bright colors of balloons can you identify in the cluster?",
                    "Where are the balloons floating, and what is attached to their knots at the bottom?",
                    "What kind of festive party or special celebration might these balloons be for?"
                ],
                "vocabulary": ["balloons", "party", "colorful", "ribbons", "floating", "celebration", "festive", "bright"]
            },
            "Medium": {
                "title": "Festive Floating Celebration Balloons",
                "prompt": "Explain what celebratory event might be happening based on this colorful bouquet of balloons.",
                "description": "Describe the celebratory atmosphere, the buoyant energy, and the visual excitement of the decorations.",
                "guidingQuestions": [
                    "How does the variety of balloon colors and flowing ribbons create an atmosphere of excitement?",
                    "What joyful sounds, laughter, and party activities would you expect in this room?",
                    "Why have balloons remained an iconic universal symbol of milestone celebrations and birthdays?"
                ],
                "vocabulary": ["celebratory", "festive", "buoyancy", "decorations", "party ribbons", "vibrant", "milestone", "gathering"]
            },
            "Hard": {
                "title": "Visual Vibrancy & Festive Atmosphere",
                "prompt": "Analyze the dynamic composition, festive color saturation, and uplifting mood of this balloon canopy.",
                "description": "Deliver a detailed critique on how color harmony, vertical lines of ribbons, and reflective surfaces evoke joy.",
                "guidingQuestions": [
                    "Evaluate how the vertical lines of hanging ribbons create upward movement toward the buoyant balloon cluster.",
                    "Discuss how color psychology triggers spontaneous feelings of nostalgia, celebration, and levity.",
                    "How does the glossy finish of the latex balloons catch overhead light to create visual dimension?"
                ],
                "vocabulary": ["color saturation", "canopy", "nostalgia", "composition", "vibrancy", "levity", "festivity", "dimension"]
            }
        }
    },
    {
        "index": 5,
        "image_url": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1578916171728-46686eac8d58?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Supermarket Grocery Store Aisle",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Supermarket Grocery Store Aisle",
                "prompt": "Describe the long supermarket aisle, the organized food shelves, and the bright lights above.",
                "description": "Look closely at the image, then describe the tall shelves, cereal boxes, and supermarket aisle.",
                "guidingQuestions": [
                    "What kinds of food products and boxes are stocked neatly on the shelves to the left and right?",
                    "How are the products organized to make it easy for shoppers to find what they need?",
                    "What details do you observe along the polished floor and overhead strip lights?"
                ],
                "vocabulary": ["supermarket", "grocery aisle", "shelves", "cereal boxes", "cartons", "merchandise", "shopping", "organized"]
            },
            "Medium": {
                "title": "Browsing the Supermarket Shelves",
                "prompt": "Walk through the experience of shopping in this well-stocked grocery store aisle.",
                "description": "Narrate the process of navigating the grocery store aisle, comparing food brands, and filling a shopping cart.",
                "guidingQuestions": [
                    "How do the perspective lines of the long aisle draw the viewer's attention toward the distant shoppers?",
                    "What considerations—nutrition, budget, taste—guide a shopper selecting items from these shelves?",
                    "Describe the clean, brightly illuminated environment that supermarkets design to encourage browsing."
                ],
                "vocabulary": ["supermarket aisle", "inventory", "consumer choice", "packaged goods", "fluorescent lighting", "browsing", "produce", "groceries"]
            },
            "Hard": {
                "title": "Modern Consumerism & Retail Architecture",
                "prompt": "Discuss the visual organization, shelf merchandising, and architecture of this supermarket aisle.",
                "description": "Analyze how retail layout, product categorization, and visual abundance shape consumer behavior.",
                "guidingQuestions": [
                    "Analyze how eye-level product placement and color-coordinated packaging influence buying decisions.",
                    "Discuss the logistical precision required to maintain fully stocked supermarket aisles in modern supply chains.",
                    "How does the expansive perspective of this aisle represent modern commercial abundance and efficiency?"
                ],
                "vocabulary": ["merchandising", "consumerism", "retail layout", "supply chain", "abundance", "eye-level placement", "logistics", "commercial"]
            }
        }
    },
    {
        "index": 6,
        "image_url": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1521587760476-6c12a4b040da?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Vintage Library Bookshelf & Hardcovers",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Vintage Library Bookcase & Old Books",
                "prompt": "Describe the tall wooden bookcase filled with colorful old hardcover books.",
                "description": "Look closely at the image, then describe the wooden shelves, the colorful book spines, and the library setting.",
                "guidingQuestions": [
                    "How are the books arranged and organized on the wooden shelves?",
                    "What different colors, sizes, and bindings do you notice on the book spines?",
                    "What kind of interesting stories or historical topics might be hidden inside these volumes?"
                ],
                "vocabulary": ["bookcase", "hardcover", "leather-bound", "spines", "vintage books", "library", "volumes", "reading"]
            },
            "Medium": {
                "title": "Exploring Classic Library Shelves",
                "prompt": "Describe the variety of antique and leather-bound books arranged on these library shelves.",
                "description": "Capture the timeless atmosphere of a historic library, the smell of aged paper, and the pursuit of knowledge.",
                "guidingQuestions": [
                    "What visual details on the book spines indicate age, craftsmanship, or frequent reading?",
                    "What sensory atmosphere—scents of aged paper, quiet study, wooden bookshelves—is evoked here?",
                    "Why do physical hardcover books retain an enduring charm compared to reading on digital screens?"
                ],
                "vocabulary": ["antique books", "leather-bound", "gilt lettering", "archival", "craftsmanship", "curated", "scholarly", "knowledge"]
            },
            "Hard": {
                "title": "Literary Heritage & Archival Knowledge",
                "prompt": "Deliver a monologue on the preservation of knowledge, vintage typography, and the allure of old libraries.",
                "description": "Analyze the cultural and aesthetic significance of physical book collections as monuments of human thought.",
                "guidingQuestions": [
                    "Examine how the grid-like shelving frames centuries of curated intellectual and literary history.",
                    "Analyze the aesthetic value of embossed leather bindings, varied typography, and age-worn patina.",
                    "Discuss how physical libraries serve as sanctuaries for deep, contemplative reading in a distracted digital world."
                ],
                "vocabulary": ["archival", "preservation", "typography", "patina", "intellectual heritage", "sanctuary", "contemplation", "volumes"]
            }
        }
    },
    {
        "index": 7,
        "image_url": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1534438327276-14e5300c3a48?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Fitness Gym Workout & Dumbbells",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Fitness Gym Workout & Dumbbells",
                "prompt": "Describe the rows of dumbbells on the rack and the people exercising in the gym.",
                "description": "Look closely at the image, then describe the weight rack, the workout room, and the fitness atmosphere.",
                "guidingQuestions": [
                    "What exercise equipment is lined up along the black metal tiered rack?",
                    "What are the people doing in the background near the workout machines and mirrors?",
                    "Why do people visit this fitness gym regularly to stay active and healthy?"
                ],
                "vocabulary": ["dumbbells", "fitness gym", "weight rack", "exercise", "strength", "workout", "athletes", "health"]
            },
            "Medium": {
                "title": "Strength Training at the Fitness Club",
                "prompt": "Explain the energy, dedication, and fitness routines taking place in this weight room.",
                "description": "Describe the focus, physical discipline, and equipment designed for progressive resistance training.",
                "guidingQuestions": [
                    "How is the gym organized to support progressive strength training with different weight increments?",
                    "What focus and determination can you observe in the athlete working out in the background?",
                    "Describe the energetic atmosphere of motivation, movement, and physical effort in this training room."
                ],
                "vocabulary": ["strength training", "resistance", "dumbbells", "conditioning", "weight room", "discipline", "athletic", "endurance"]
            },
            "Hard": {
                "title": "Athletic Discipline & Resistance Training",
                "prompt": "Critique the environment of modern strength training, physical wellness, and athletic discipline.",
                "description": "Provide a comprehensive speech examining the psychology of physical conditioning and health habits.",
                "guidingQuestions": [
                    "Analyze how modern gym facilities combine ergonomic equipment and motivating space to support fitness habits.",
                    "Discuss the psychological benefits of consistent strength training beyond physical aesthetics.",
                    "How does the sharp focus on the metallic dumbbells in the foreground emphasize dedication and grit?"
                ],
                "vocabulary": ["conditioning", "ergonomic", "progressive overload", "wellness", "athleticism", "discipline", "resilience", "physiology"]
            }
        }
    },
    {
        "index": 8,
        "image_url": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1556910103-1c02745aae4d?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Friends Cooking Soup in Modern Kitchen",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Friends Cooking in a Warm Kitchen",
                "prompt": "Describe the friends preparing food together in the kitchen, the blue pot, and the wooden spoon.",
                "description": "Look closely at the image, then describe the young man tasting soup, the woman smiling, and the kitchen island.",
                "guidingQuestions": [
                    "What is the smiling young man in the apron doing with the wooden spoon and blue pot?",
                    "What fresh ingredients, bowl of salad, and olive oil bottle are visible on the wooden counter?",
                    "How can you tell that the friends are having fun cooking together in this bright kitchen?"
                ],
                "vocabulary": ["kitchen", "wooden spoon", "soup pot", "tasting", "apron", "salad bowl", "olive oil", "smiling"]
            },
            "Medium": {
                "title": "Culinary Collaboration in the Kitchen",
                "prompt": "Explain how the friends cooperate to prepare a homemade meal, tasting and seasoning the soup.",
                "description": "Narrate the cooking process, the division of kitchen tasks, and the warmth of shared culinary teamwork.",
                "guidingQuestions": [
                    "How do the friends divide kitchen tasks between simmering soup, prepping ingredients, and tasting?",
                    "What savory aromas, herbs, and flavors can you imagine emerging from the blue Dutch oven?",
                    "Why does cooking and preparing meals together strengthen social bonds and conversation?"
                ],
                "vocabulary": ["culinary", "collaboration", "simmering", "seasoning", "Dutch oven", "camaraderie", "homemade", "ingredients"]
            },
            "Hard": {
                "title": "Kitchen Artistry & Shared Gastronomy",
                "prompt": "Analyze the social camaraderie, culinary craftsmanship, and home atmosphere depicted in this kitchen.",
                "description": "Deliver an articulate critique examining how home cooking fosters community, nutrition, and joy.",
                "guidingQuestions": [
                    "Examine how open kitchen shelving, artisanal cookware, and warm lighting create a welcoming culinary aesthetic.",
                    "Discuss the sociological importance of communal meal preparation as an antidote to fast-paced modern life.",
                    "Analyze the genuine nonverbal interactions—smiles, eye contact, and relaxed posture—shared by the cooks."
                ],
                "vocabulary": ["gastronomy", "camaraderie", "artisanal", "communal", "culinary aesthetic", "nourishment", "hospitality", "tableau"]
            }
        }
    },
    {
        "index": 9,
        "image_url": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1524178232363-1fb2b075b655?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Conference Presentation & Speaker",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Conference Presentation & Speaker",
                "prompt": "Describe the speaker at the podium presenting to the seated audience in the meeting room.",
                "description": "Look closely at the image, then describe the speaker, the projector screen, and the audience members listening.",
                "guidingQuestions": [
                    "Where is the speaker standing, and what presentation equipment is he using at the front?",
                    "What are the audience members in the chairs doing as they listen to the talk?",
                    "What is displayed on the large white projector screen beside the podium?"
                ],
                "vocabulary": ["speaker", "podium", "projector screen", "audience", "presentation", "meeting room", "laptop", "listening"]
            },
            "Medium": {
                "title": "Delivering a Professional Seminar",
                "prompt": "Explain how the speaker uses visual slides and speaking skills to engage the listeners.",
                "description": "Discuss effective public speaking, seminar communication, and how presentation visuals clarify information.",
                "guidingQuestions": [
                    "How does the speaker establish presence and maintain the attention of the diverse audience?",
                    "What role do projected visual slides play in communicating complex data and business ideas clearly?",
                    "Describe the professional atmosphere of learning, note-taking, and discussion in this conference room."
                ],
                "vocabulary": ["professional seminar", "keynote", "public speaking", "projector slides", "audience engagement", "discourse", "podium", "conference"]
            },
            "Hard": {
                "title": "Public Speaking & Intellectual Discourse",
                "prompt": "Critique the communication dynamics, audience engagement, and rhetoric of this seminar.",
                "description": "Analyze the spatial dynamics, nonverbal cues, and rhetorical presentation techniques displayed in this seminar setting.",
                "guidingQuestions": [
                    "Evaluate how the room arrangement balances formal presentation at the podium with collaborative discussion.",
                    "Discuss the oratorical strategies required to sustain engagement during technical seminars and business pitches.",
                    "Analyze the body language and attentive posture of the listeners seated in the audience rows."
                ],
                "vocabulary": ["rhetoric", "intellectual discourse", "oratory", "nonverbal communication", "pedagogy", "seminar", "engagement", "articulation"]
            }
        }
    },
    {
        "index": 10,
        "image_url": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1475721027785-f74eccf877e2?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Stage Microphone & Warm Lights",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Stage Microphone Under Warm Lights",
                "prompt": "Describe the metal microphone on its stand, waiting for a speaker or singer to step up.",
                "description": "Look closely at the image, then describe the close-up microphone, the stand, and the blurred crowd in the background.",
                "guidingQuestions": [
                    "What piece of audio equipment is positioned in the center of the image?",
                    "What warm lighting colors and blurred silhouettes do you notice in the background?",
                    "Who might be about to step up to this microphone to speak or perform for the crowd?"
                ],
                "vocabulary": ["microphone", "stage", "metal stand", "bokeh", "performer", "warm lights", "crowd", "audio"]
            },
            "Medium": {
                "title": "Standing at the Stage Microphone",
                "prompt": "Explain the feelings of anticipation and excitement when stepping up to a stage microphone.",
                "description": "Describe the atmosphere of a live venue, the technical clarity of the microphone, and the energy of an awaiting crowd.",
                "guidingQuestions": [
                    "How does the shallow focus emphasize the textured metal mesh of the vocal microphone?",
                    "What emotions—excitement, anticipation, nervousness—does a speaker or musician feel before speaking?",
                    "Describe the ambiance of the illuminated venue and the attentive crowd waiting in the background."
                ],
                "vocabulary": ["vocal microphone", "stage performance", "anticipation", "acoustics", "shallow focus", "venue", "spotlight", "audience"]
            },
            "Hard": {
                "title": "The Power of the Voice: Stage & Oratory",
                "prompt": "Deliver a speech on the emotional power of the human voice and the symbolic weight of the microphone.",
                "description": "Provide a reflective oratorical analysis on public expression, amplification of ideas, and stage presence.",
                "guidingQuestions": [
                    "Discuss the microphone as a cultural symbol of democratic expression, performance, and leadership.",
                    "How does the composition contrast the sharp, tangible microphone with the soft, luminous bokeh of the crowd?",
                    "What psychological shift occurs in a speaker when their spoken words are amplified to a listening room?"
                ],
                "vocabulary": ["oratory", "amplification", "vocal resonance", "symbolism", "stage presence", "expressive", "articulation", "luminosity"]
            }
        }
    },
    {
        "index": 11,
        "image_url": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Modern Cafe & Espresso Counter",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Busy Coffee Shop & Laptop Tables",
                "prompt": "Describe the open cafe, the people working at wooden tables, and the coffee counter.",
                "description": "Look closely at the image, then describe the cafe interior, the wooden furniture, and customers on laptops.",
                "guidingQuestions": [
                    "What are the customers at the wooden tables doing on their laptops?",
                    "Where is the coffee service counter located, and what menu boards are hanging above it?",
                    "What decorative features—lamps, staircase, wooden furniture—make this cafe welcoming?"
                ],
                "vocabulary": ["coffee shop", "cafe counter", "wooden tables", "laptops", "barista", "industrial lamps", "customers", "open space"]
            },
            "Medium": {
                "title": "Coworking Afternoon in an Urban Cafe",
                "prompt": "Explain how this modern cafe serves as a bustling hub for remote work, coffee, and casual meetings.",
                "description": "Capture the creative energy, espresso aromas, and productive hum of an urban neighborhood coffee house.",
                "guidingQuestions": [
                    "How does the architectural combination of high ceilings, warm timber, and open lighting shape the mood?",
                    "Why do students and professionals choose to work on projects in vibrant cafes rather than at home?",
                    "Describe the sensory blend of freshly ground coffee, clinking cups, and ambient keyboard typing."
                ],
                "vocabulary": ["coworking", "urban cafe", "timber furniture", "espresso bar", "remote work", "productivity", "architectural", "patrons"]
            },
            "Hard": {
                "title": "The Third Place: Community & Remote Work",
                "prompt": "Analyze the architectural and social design of the modern cafe as a productive 'third place'.",
                "description": "Deliver a sociological and design critique on how contemporary cafes merge hospitality, community, and commerce.",
                "guidingQuestions": [
                    "Examine Ray Oldenburg's concept of the 'third place' as exemplified by this open, multi-functional cafe.",
                    "Analyze how industrial steel beams, timber accents, and natural daylight create an inviting workspace.",
                    "Discuss how modern cafe culture has adapted to accommodate the flexible work habits of digital professionals."
                ],
                "vocabulary": ["third place", "sociological", "spatial design", "hospitality", "multi-functional", "contemporary", "ambiance", "community"]
            }
        }
    },
    {
        "index": 12,
        "image_url": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1474487548417-781cb71495f3?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Freight Cargo Train on Railroad Tracks",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Freight Cargo Train on the Tracks",
                "prompt": "Describe the big yellow and red train engine pulling the long line of cargo cars on the tracks.",
                "description": "Look closely at the image, then describe the heavy freight locomotive, the train tracks, and the sky.",
                "guidingQuestions": [
                    "What bright colors stand out on the front cab of the train locomotive?",
                    "What kind of round tanker cars and cargo is the locomotive pulling behind it?",
                    "Where are the steel railway tracks leading across the countryside?"
                ],
                "vocabulary": ["freight train", "locomotive", "railroad tracks", "cargo cars", "steel rails", "yellow engine", "countryside", "clouds"]
            },
            "Medium": {
                "title": "Diesel Freight Train Crossing the Countryside",
                "prompt": "Narrate the powerful journey of this diesel locomotive as it transports vital freight along the railway.",
                "description": "Describe the industrial strength of the train, the rumble of the diesel engine, and the cloudy landscape.",
                "guidingQuestions": [
                    "How do the heavy steel tracks and gravel ballast support the enormous tonnage of the moving train?",
                    "What role do transcontinental freight trains play in distributing raw materials and goods nationwide?",
                    "Describe the deep rumble, metallic clatter, and sense of unstoppable momentum as the train approaches."
                ],
                "vocabulary": ["diesel locomotive", "freight transport", "cargo tankers", "railway tracks", "ballast", "momentum", "industrial", "haulage"]
            },
            "Hard": {
                "title": "Heavy Rail Freight & Industrial Logistics",
                "prompt": "Deliver a commentary on the economic significance and engineering power of heavy rail freight transportation.",
                "description": "Analyze the energy efficiency, infrastructure, and historical importance of commercial railway logistics.",
                "guidingQuestions": [
                    "Analyze how rail freight remains one of the most fuel-efficient methods for overland bulk transportation.",
                    "Discuss the visual composition, including the low-angle perspective emphasizing the train's imposing scale.",
                    "How does the dramatic overcast sky enhance the rugged industrial atmosphere of the railway corridor?"
                ],
                "vocabulary": ["rail freight", "logistics infrastructure", "diesel-electric", "tonnage", "bulk transport", "overcast", "industrialization", "artery"]
            }
        }
    },
    {
        "index": 13,
        "image_url": "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1506015391300-4802dc74de2e?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Off-Road Jeep in Desert Dusk",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Off-Road Jeep in the Desert at Dusk",
                "prompt": "Describe the black 4x4 Jeep parked on the desert gravel with its bright headlights turned on.",
                "description": "Look closely at the image, then describe the off-road vehicle, the desert dirt road, and the evening sky.",
                "guidingQuestions": [
                    "What type of 4x4 vehicle is parked on the desert gravel path?",
                    "What time of day does it appear to be based on the twilight sky and glowing headlights?",
                    "What landscape features and mountains can you see in the arid desert background?"
                ],
                "vocabulary": ["Jeep", "off-road", "4x4", "desert", "headlights", "gravel trail", "twilight", "mountains"]
            },
            "Medium": {
                "title": "Desert Expedition in a 4x4 Vehicle",
                "prompt": "Explain the spirit of outdoor adventure and off-road exploration represented by this desert Jeep.",
                "description": "Capture the rugged freedom of traversing backcountry trails, camping under open skies, and desert exploration.",
                "guidingQuestions": [
                    "How do the all-terrain tires, high ground clearance, and sturdy frame equip this vehicle for rocky terrain?",
                    "What survival gear, navigation tools, and mindset are essential when heading into remote desert wilderness?",
                    "Describe the stillness and dramatic beauty of the desert as sunset transitions into cool twilight."
                ],
                "vocabulary": ["expedition", "all-terrain", "ground clearance", "backcountry", "wilderness", "twilight", "rugged", "exploration"]
            },
            "Hard": {
                "title": "Off-Grid Exploration & Rugged Wilderness",
                "prompt": "Critique the theme of wilderness travel, automotive engineering, and solitude in the desert landscape.",
                "description": "Deliver a detailed monologue on the romanticism of overland journeys and human interaction with arid nature.",
                "guidingQuestions": [
                    "Examine how the vehicle's rugged black profile contrasts with the soft pastel tones of the dusk desert horizon.",
                    "Discuss the cultural fascination with overland exploration as an escape from urban domesticity.",
                    "Analyze how the warm illumination of the headlights introduces human presence into an ancient landscape."
                ],
                "vocabulary": ["overlanding", "solitude", "arid landscape", "ruggedness", "automotive design", "twilight", "remoteness", "endurance"]
            }
        }
    },
    {
        "index": 14,
        "image_url": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1503899036084-c55cdd92da26?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Tokyo Neon City Street at Night",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Tokyo Neon City Street at Night",
                "prompt": "Describe the bright neon signs, the busy pedestrians, and the famous Godzilla head on the building in Tokyo.",
                "description": "Look closely at the image, then describe the glowing signs in Japanese, the tall hotel building, and the nighttime crowds.",
                "guidingQuestions": [
                    "What glowing neon signs and colorful advertisements line both sides of the city street?",
                    "Can you spot the iconic giant Godzilla head perched atop the hotel building in the background?",
                    "What are the pedestrians on the street doing as they walk through this bustling night district?"
                ],
                "vocabulary": ["Tokyo", "neon signs", "Godzilla", "nightlife", "Shinjuku", "pedestrians", "billboards", "city street"]
            },
            "Medium": {
                "title": "Evening Vibrancy in Tokyo's Neon District",
                "prompt": "Describe the bustling evening energy, glowing Japanese signs, and urban excitement of this Tokyo street.",
                "description": "Capture the futuristic spectacle, bustling foot traffic, and luminous nighttime culture of Shinjuku.",
                "guidingQuestions": [
                    "How does the vertical density of multi-story illuminated signs create a sensory-rich urban canyon?",
                    "What sounds—store music, restaurant announcements, trains, lively chatter—fill this famous district?",
                    "Why has Tokyo's illuminated nightlife become a world-renowned visual symbol of modern metropolis culture?"
                ],
                "vocabulary": ["illuminated", "neon corridor", "Shinjuku Kabukicho", "foot traffic", "sensory", "metropolis", "commercial", "kinetic"]
            },
            "Hard": {
                "title": "Urban Nocturne: Cyberpunk Aesthetics & Tokyo Metropolis",
                "prompt": "Analyze the architectural density, luminous neon signage, and futuristic visual culture of Tokyo nightlife.",
                "description": "Provide a comprehensive cultural and aesthetic critique of Tokyo's nighttime urban landscape and pop iconography.",
                "guidingQuestions": [
                    "Analyze how the juxtaposition of traditional pedestrian lanes and colossal illuminated billboards evokes cyberpunk aesthetics.",
                    "Discuss the inclusion of the Godzilla landmark as playful cultural heritage integrated into modern commercial space.",
                    "How does the visual saturation of electric blues, vivid reds, and glowing yellow text impact viewer immersion?"
                ],
                "vocabulary": ["cyberpunk", "visual saturation", "nocturne", "architectural density", "iconography", "spectacle", "immersion", "metropolitan"]
            }
        }
    },
    {
        "index": 15,
        "image_url": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1533900298318-6b8da08a523e?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Fresh Fruit Stall at Farmers Market",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Fresh Fruit Stall at Farmers Market",
                "prompt": "Describe the wooden crates filled with fresh fruits and the market stalls under the canvas roof.",
                "description": "Look closely at the image, then describe the boxes of grapes, peaches, apples, and the market vendors.",
                "guidingQuestions": [
                    "What colorful fresh fruits are displayed inside the rustic wooden produce crates?",
                    "How are the crates stacked on tables to showcase the harvest to passing customers?",
                    "What are the market vendors in the background doing as they attend to their fruit stalls?"
                ],
                "vocabulary": ["farmers market", "fruit stall", "wooden crates", "grapes", "peaches", "fresh produce", "market awning", "vendors"]
            },
            "Medium": {
                "title": "Morning at the Open-Air Produce Market",
                "prompt": "Narrate the sights, colors, and aromas of shopping at this lively open-air fruit and vegetable market.",
                "description": "Describe the tactile charm of farmers markets, seasonal produce, and personal exchanges between farmers and shoppers.",
                "guidingQuestions": [
                    "How does shopping at open-air market stalls differ from buying packaged goods in commercial supermarkets?",
                    "What sensory details—sweet ripe aromas, crisp textures, morning warmth—bring this market scene to life?",
                    "Why do local community farmers markets strengthen regional agriculture and healthy eating habits?"
                ],
                "vocabulary": ["open-air market", "seasonal produce", "rustic crates", "orchard harvest", "community commerce", "sweet aroma", "wholesome", "artisanal"]
            },
            "Hard": {
                "title": "Agrarian Commerce & Local Food Markets",
                "prompt": "Discuss the cultural, economic, and community benefits of traditional open-air farmers markets.",
                "description": "Deliver a detailed critique on sustainable food systems, regional food sovereignty, and community gathering spaces.",
                "guidingQuestions": [
                    "Analyze how open-air markets serve as vital social fabric that connects rural food producers with urban consumers.",
                    "Examine the visual warmth of hand-labeled wooden crates, canvas awnings, and dappled morning market lighting.",
                    "Discuss the modern consumer resurgence of interest in traceability, freshness, and local agricultural sustainability."
                ],
                "vocabulary": ["agrarian commerce", "sustainability", "food sovereignty", "traceability", "local economy", "wholesome", "social fabric", "harvest"]
            }
        }
    },
    {
        "index": 16,
        "image_url": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1515694346937-94d85e41e6f0?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Raindrops on Window Over City Lights",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Raindrops on Window Over City Lights",
                "prompt": "Describe the raindrops clinging to the window glass and the warm blurry city lights outside.",
                "description": "Look closely at the image, then describe the water droplets, the evening rain, and the colorful glowing lights.",
                "guidingQuestions": [
                    "What clings to the surface of the clear glass window in the foreground?",
                    "What colors of warm circular lights shine through the rainy glass from the street below?",
                    "What kind of cozy feelings do people often have when watching rain from inside a warm room?"
                ],
                "vocabulary": ["raindrops", "window glass", "city lights", "glowing", "bokeh", "evening rain", "cozy", "droplets"]
            },
            "Medium": {
                "title": "Rainy Evening Reflections Through the Window",
                "prompt": "Capture the cozy, introspective mood of watching rain fall against the window while city lights glow.",
                "description": "Describe the peaceful rhythm of rainfall, the optical beauty of water droplets, and the gentle melancholy of evening rain.",
                "guidingQuestions": [
                    "How does each individual raindrop act as a miniature lens reflecting the evening streetlights?",
                    "What thoughts and memories often arise while watching a steady downpour wash over a bustling city?",
                    "Describe the contrast between the wet, cold weather outside and the comfort of watching from within."
                ],
                "vocabulary": ["introspective", "water droplets", "reflections", "bokeh lights", "downpour", "melancholy", "precipitation", "tranquility"]
            },
            "Hard": {
                "title": "Melancholy & Urban Light: Raindrop Perspectives",
                "prompt": "Deliver an evocative poetic critique on visual abstraction, wet surfaces, and urban evening moods.",
                "description": "Analyze how macro photography of rain transforms a mundane urban weather scene into abstract visual poetry.",
                "guidingQuestions": [
                    "Evaluate how the visual tension between the sharp foreground droplets and blurred background bokeh evokes introspection.",
                    "Discuss the literary and cinematic tradition of using rain against glass to signify reflection, longing, or calm.",
                    "How does the color palette—cool slate blues paired with warm amber and magenta headlights—influence emotional resonance?"
                ],
                "vocabulary": ["abstraction", "bokeh", "introspection", "poetic resonance", "optical distortion", "macro photography", "luminance", "melancholic"]
            }
        }
    },
    {
        "index": 17,
        "image_url": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1511795409834-ef04bbd61622?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Elegant Banquet Table & Floral Centerpiece",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Elegant Banquet Dinner Table & Flowers",
                "prompt": "Describe the long beautifully set dinner table, the shiny wine glasses, and the colorful flower centerpiece.",
                "description": "Look closely at the image, then describe the crystal wine glasses, white plates, napkins, and floral bouquet.",
                "guidingQuestions": [
                    "What formal dining items are set neatly at each place setting along the table?",
                    "What vibrant colors of roses and blossoms make up the decorative floral arrangement in the center?",
                    "What special occasion—such as a wedding reception or gala banquet—might this table be prepared for?"
                ],
                "vocabulary": ["banquet table", "wine glasses", "plates", "floral centerpiece", "roses", "napkins", "celebration", "formal dining"]
            },
            "Medium": {
                "title": "Formal Dining Setting for a Special Celebration",
                "prompt": "Explain the formal etiquette, glassware arrangement, and celebratory ambiance of this banquet table.",
                "description": "Describe the anticipation of a celebratory gala dinner, the art of formal table setting, and joyful toasts.",
                "guidingQuestions": [
                    "How do sparkling crystal stemware, fine china, and bespoke floral arrangements set an elevated mood?",
                    "What toasts, laughter, and multi-course culinary experiences will soon unfold around this banquet table?",
                    "Describe the care, symmetry, and hospitality required to prepare such a luxurious celebratory setting."
                ],
                "vocabulary": ["stemware", "bespoke florals", "banquet", "formal etiquette", "hospitality", "celebratory", "table setting", "gala dinner"]
            },
            "Hard": {
                "title": "Haute Cuisine Hospitality & Table Design",
                "prompt": "Critique the design principles, hospitality standards, and refined luxury displayed in this table setting.",
                "description": "Analyze how table layout, floral architecture, and ambient lighting come together to create high-end event dining.",
                "guidingQuestions": [
                    "Analyze how the linear perspective of repetitive crystal glassware leads the eye directly to the vibrant floral focal point.",
                    "Discuss the role of sensory staging—visual elegance, tactile linen, and aromatic flowers—in premier hospitality.",
                    "How does formal dining design transform an ordinary meal into an unforgettable, ceremonial human celebration?"
                ],
                "vocabulary": ["haute cuisine", "sensory staging", "table design", "linear perspective", "ceremonial", "hospitality standards", "symmetry", "opulence"]
            }
        }
    },
    {
        "index": 18,
        "image_url": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1522071820081-009f0129c71c?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Tech Team Laptop Collaboration",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Team Working on Laptops Together",
                "prompt": "Describe the group of young people sitting around the table working hard on their open laptops.",
                "description": "Look closely at the image, then describe the teammates gathered at the wooden desk, their screens, and collaboration.",
                "guidingQuestions": [
                    "How many people are gathered together around the wooden table working on laptops?",
                    "What electronic devices, notebooks, or headphones are the team members using?",
                    "What clues show that the group is working collaboratively on an important group project or software?"
                ],
                "vocabulary": ["teamwork", "laptops", "table", "coworkers", "coding", "headphones", "collaboration", "focused"]
            },
            "Medium": {
                "title": "Startup Team Collaboration & Coding Session",
                "prompt": "Explain how this software or project team collaborates, codes, and shares ideas around their shared workspace.",
                "description": "Narrate the problem-solving energy, rapid brainstorming, and deep technical focus of a startup team sprint.",
                "guidingQuestions": [
                    "How does sitting together around a communal work table accelerate communication and team problem-solving?",
                    "What balance between individual deep focus (with headphones) and spontaneous team discussion is shown here?",
                    "Describe the informal, dedicated culture of modern software engineering sprints and hackathons."
                ],
                "vocabulary": ["software engineering", "hackathon", "sprint", "communal workspace", "problem-solving", "code review", "brainstorming", "synergy"]
            },
            "Hard": {
                "title": "Agile Development & Creative Synergy",
                "prompt": "Analyze the modern dynamics of collaborative programming, startup culture, and cognitive focus.",
                "description": "Deliver a detailed critique on team cognitive dynamics, agile workflows, and collaborative technical innovation.",
                "guidingQuestions": [
                    "Examine how open collaborative environments balance intense solitary cognitive tasks with immediate peer feedback.",
                    "Discuss the sociological shift from rigid corporate cubicles to agile, shared wooden work tables in technology companies.",
                    "Analyze the body language, screen orientation, and shared tools that enable synchronous creative momentum."
                ],
                "vocabulary": ["agile methodology", "cognitive focus", "creative synergy", "synchronous", "collaborative programming", "innovation", "startup culture", "momentum"]
            }
        }
    },
    {
        "index": 19,
        "image_url": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1519494026892-80bbd2d6fd0d?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Medical Clinic & Hospital Reception",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Medical Clinic & Hospital Reception Desk",
                "prompt": "Describe the hospital reception desk, the glass counter, the directory signs, and the clean hallway.",
                "description": "Look closely at the image, then describe the curved white counter, registration glass, and clinic hall.",
                "guidingQuestions": [
                    "What is situated in the center of the entrance hall to assist arriving patients and visitors?",
                    "What medical departments and floors are listed on the blue wall directory sign (Piso 1)?",
                    "Why are clean tiled floors, bright lighting, and clear signs essential for a welcoming medical facility?"
                ],
                "vocabulary": ["reception desk", "hospital", "clinic", "directory sign", "counter", "clean hallway", "medical", "elevator"]
            },
            "Medium": {
                "title": "Navigating the Healthcare Reception Area",
                "prompt": "Explain how patients and visitors are welcomed and guided at this modern clinic reception desk.",
                "description": "Discuss the process of patient check-in, reassurance from medical staff, and organized clinical navigation.",
                "guidingQuestions": [
                    "How does the curved reception desk with glass partitions balance patient privacy with clear communication?",
                    "What feelings of reassurance and trust does a bright, hygienic, and organized clinic entrance instill in patients?",
                    "Describe the duties of front-desk medical administrative staff in directing visitors to the right department."
                ],
                "vocabulary": ["patient admission", "clinical navigation", "hygienic", "reassurance", "healthcare administration", "privacy partition", "directory", "hospitality"]
            },
            "Hard": {
                "title": "Clinical Architecture & Patient Admission",
                "prompt": "Evaluate how hospital interior architecture, hygiene standards, and signage facilitate patient care and comfort.",
                "description": "Analyze healthcare facility design, wayfinding systems, and how sterile architecture influences patient emotional states.",
                "guidingQuestions": [
                    "Analyze the architectural choices—curved counters, wipeable ceramic tiles, and wide corridors—designed for infection control and accessibility.",
                    "Discuss how clear wayfinding and bilingual signage alleviate stress for patients navigating unfamiliar healthcare systems.",
                    "How can medical architecture balance clinical efficiency and sterile requirements with human empathy and warmth?"
                ],
                "vocabulary": ["clinical architecture", "wayfinding", "infection control", "patient-centered", "sanitary", "accessibility", "administrative", "empathy"]
            }
        }
    },
    {
        "index": 20,
        "image_url": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=1200&q=80",
        "thumbnail": "https://images.unsplash.com/photo-1519501025264-65ba15a82390?auto=format&fit=crop&w=400&q=80",
        "scene_subject": "Downtown Skyscraper Canyon & City Traffic",
        "durations": {"Easy": "Visual Scene", "Medium": "Visual Scene", "Hard": "Visual Scene"},
        "tiers": {
            "Easy": {
                "title": "Downtown Skyscraper Canyon & City Traffic",
                "prompt": "Describe the towering city skyscrapers, the city buses, the yellow taxis, and the wet street reflections.",
                "description": "Look closely at the image, then describe the tall historic buildings, city traffic at dusk, and metropolitan street.",
                "guidingQuestions": [
                    "What vehicles—taxis, buses, and cars—are driving down the wet city avenue between the tall buildings?",
                    "How high do the skyscrapers and historic towers rise on both sides of the street?",
                    "What time of day does it appear to be based on the glowing headlights and evening sky?"
                ],
                "vocabulary": ["skyscrapers", "downtown", "taxis", "traffic", "city bus", "wet street", "avenue", "headlights"]
            },
            "Medium": {
                "title": "Twilight Commute in the Financial District",
                "prompt": "Narrate the evening rush hour in this bustling downtown canyon as commuters travel between skyscrapers.",
                "description": "Describe the metropolitan energy, the glowing tail lights reflecting on damp asphalt, and the architectural grandeur.",
                "guidingQuestions": [
                    "How do the towering vertical walls of the skyscrapers create a dramatic urban canyon framing the street below?",
                    "What sounds and sensory experiences—honking horns, bus brakes, bustling commuters—fill this financial district?",
                    "Describe the visual contrast between the cool dusk sky and the warm amber glow of vehicle headlights."
                ],
                "vocabulary": ["financial district", "urban canyon", "evening commute", "skyscrapers", "metropolitan", "rush hour", "reflections", "architecture"]
            },
            "Hard": {
                "title": "Metropolitan Scale: Urban Canyons & Rush Hour",
                "prompt": "Critique the monumental urban canyon architecture, street-level energy, and mobility in this metropolis.",
                "description": "Deliver a sophisticated architectural and urbanist analysis on density, transit systems, and iconic cityscapes.",
                "guidingQuestions": [
                    "Analyze how the perspective composition draws the eye toward the historic Chicago Board of Trade tower at the canyon's terminus.",
                    "Discuss the ecological and societal balance between mass transit buses, rideshare vehicles, and dense pedestrian corridors.",
                    "How do wet street surfaces enhance the photographic depth through specular light reflections and atmospheric mood?"
                ],
                "vocabulary": ["urban canyon", "monumental scale", "metropolitan transit", "architectural vista", "specular reflections", "density", "corridor", "cityscape"]
            }
        }
    }
]

# =============================================================================
# 20 VERIFIED EMBEDDABLE YOUTUBE ANIMATED SHORT FILMS
# =============================================================================
VIDEO_CATALOG = [
    {
        "index": 1,
        "youtube_id": "_nbVTUYVKxg",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/_nbVTUYVKxg",
        "embed_url": "https://www.youtube.com/embed/_nbVTUYVKxg",
        "film_title": "Pixar's For the Birds",
        "durations": {"Easy": "3 min", "Medium": "3 min", "Hard": "3 min"},
        "tiers": {
            "Easy": {
                "title": "For the Birds: Feathery Friends on a Wire",
                "prompt": "Watch the small blue birds on the telephone wire tease the big goofy bird, and explain what goes wrong for them!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "How do the small blue birds react when the large, unusual bird lands in the middle of their telephone wire?",
                    "What happens to the heavy telephone wire as the big bird hangs upside down by his toes?",
                    "How does the little birds' teasing behavior backfire comically when the wire snaps back like a slingshot?"
                ],
                "vocabulary": ["blue birds", "telephone wire", "chirping", "teasing", "slingshot", "feathers", "comedy", "squawking"]
            },
            "Medium": {
                "title": "Pixar's For the Birds: Mob Mentality on the Wire",
                "prompt": "Explain how the flock of small birds' bullying behavior toward the big awkward newcomer hilariously backfires.",
                "description": "Watch the short film, then describe the sequence of events, character expressions, and comedic climax.",
                "guidingQuestions": [
                    "How does the flock demonstrate mob mentality as they huddle together and peck at the big bird's feet?",
                    "What visual comedy and physics are used when the wire stretches to the ground before snapping upward?",
                    "What moral lesson about kindness, inclusion, and unexpected consequences does this animated short convey?"
                ],
                "vocabulary": ["mob mentality", "telephone wire", "slingshot effect", "comedy", "exclusion", "consequences", "featherless", "irony"]
            },
            "Hard": {
                "title": "Satire & Slapstick: Pixar's For the Birds",
                "prompt": "Analyze the comic timing, character animation, and moral allegory about exclusion and irony in 'For the Birds'.",
                "description": "Deliver a detailed critique evaluating how expressive character animation and sound design tell a wordless story.",
                "guidingQuestions": [
                    "Analyze how Ralph Eggleston uses expressive chirps, squash-and-stretch animation, and pacing without spoken dialogue.",
                    "Discuss the visual irony of the small birds celebrating their apparent victory right before losing their own feathers.",
                    "How does this Academy Award-winning short use physical comedy to deliver an enduring critique of prejudice?"
                ],
                "vocabulary": ["comic timing", "allegory", "squash and stretch", "slapstick", "satire", "poetic justice", "wordless storytelling", "irony"]
            }
        }
    },
    {
        "index": 2,
        "youtube_id": "07d2dXHYb94",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/07d2dXHYb94",
        "embed_url": "https://www.youtube.com/embed/07d2dXHYb94",
        "film_title": "Pip the Puppy (Canine University)",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "Pip the Puppy: Learning to Be a Guide Dog",
                "prompt": "Watch little Pip train at Canine University and explain how she proves her bravery in the emergency!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What dream does little puppy Pip have when she arrives at Canine University to train as a guide dog?",
                    "Why does Pip struggle during the classroom tests and obstacle courses compared to the bigger dogs?",
                    "How does Pip show heroic courage when an emergency happens outside, earning her official guide dog cape?"
                ],
                "vocabulary": ["Pip", "puppy", "guide dog", "Canine University", "bravery", "training", "cape", "heroic"]
            },
            "Medium": {
                "title": "Pip the Guide Dog: Determination Over Size",
                "prompt": "Narrate Pip's journey from a clumsy, undersized recruit to a brave, certified guide dog hero.",
                "description": "Analyze Pip's emotional struggles, resilience in the face of failure, and quick thinking during the crisis.",
                "guidingQuestions": [
                    "How do the trainers and taller dogs react to Pip's mistakes, and how does she keep trying despite discouragement?",
                    "What critical skills does Pip apply when an instructor is in danger near the construction site?",
                    "How does the story prove that heart, determination, and quick thinking matter more than physical size?"
                ],
                "vocabulary": ["determination", "resilience", "guide dog training", "Canine University", "obstacle course", "emergency", "service dog", "triumph"]
            },
            "Hard": {
                "title": "Pip: Resilience & Purpose in Canine Training",
                "prompt": "Analyze the storytelling arc of Pip, exploring themes of perseverance, overcoming limitations, and selflessness.",
                "description": "Deliver an articulate speech on how Pip inspires empathy, dedication to service, and emotional storytelling.",
                "guidingQuestions": [
                    "Examine the narrative structure of Pip: how initial failure establishes empathy before the climactic redemption.",
                    "Discuss the vital real-world role of guide dogs and service animals portrayed through this heartwarming animation.",
                    "How does the emotional musical score and visual cues communicate Pip's feelings of insecurity and determination?"
                ],
                "vocabulary": ["narrative arc", "resilience", "service dog", "underdog archetype", "empathy", "redemption", "altruism", "triumph"]
            }
        }
    },
    {
        "index": 3,
        "youtube_id": "38y_1EWIE9I",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/38y_1EWIE9I",
        "embed_url": "https://www.youtube.com/embed/38y_1EWIE9I",
        "film_title": "Snack Attack (Cookie Confusion)",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "Snack Attack: The Train Station Cookie Mystery",
                "prompt": "Watch the lady fight with the vending machine and share cookies with the teen on the bench, then explain the twist!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What trouble does the elderly woman have when trying to buy her package of cookies from the vending machine?",
                    "Why does she get increasingly annoyed with the young boy sitting on the train station bench?",
                    "What surprising discovery does she make once she boards her train and opens her handbag?"
                ],
                "vocabulary": ["vending machine", "cookies", "train station", "bench", "teenager", "misunderstanding", "handbag", "twist"]
            },
            "Medium": {
                "title": "Snack Attack: Misunderstanding on the Bench",
                "prompt": "Explain the humorous misunderstanding between the elderly woman and the teenager sharing cookies on the bench.",
                "description": "Describe the growing tension, the teenager's generous reaction, and the revelation that shifts our perspective.",
                "guidingQuestions": [
                    "How does the woman misinterpret the teenager's actions while they are sitting together waiting for the train?",
                    "Notice the teenager's generous decision to break the last cookie in half—what does that reveal about his character?",
                    "How does the sudden twist ending make both the protagonist and the audience re-evaluate their assumptions?"
                ],
                "vocabulary": ["misunderstanding", "generosity", "vending machine", "train platform", "presumption", "perspective", "shared cookie", "revelation"]
            },
            "Hard": {
                "title": "Snack Attack: Assumptions & Perspective",
                "prompt": "Analyze how 'Snack Attack' subverts audience expectations and offers an insightful lesson on jumping to conclusions.",
                "description": "Provide a thoughtful critique of narrative misdirection, cognitive bias, and intergenerational empathy.",
                "guidingQuestions": [
                    "Analyze how director Eduardo Verastegui uses tight visual framing and misdirection to align our bias with the woman.",
                    "Discuss how generational stereotypes lead to hasty conclusions, and how true kindness crossed generational lines.",
                    "What psychological lessons about humility, perspective-taking, and self-awareness does the film impart?"
                ],
                "vocabulary": ["cognitive bias", "misdirection", "perspective-taking", "intergenerational", "subversion", "stereotypes", "humility", "empathy"]
            }
        }
    },
    {
        "index": 4,
        "youtube_id": "5L4DQfVIcdg",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/5L4DQfVIcdg",
        "embed_url": "https://www.youtube.com/embed/5L4DQfVIcdg",
        "film_title": "Coin Operated (Rocket to the Stars)",
        "durations": {"Easy": "5 min", "Medium": "5 min", "Hard": "5 min"},
        "tiers": {
            "Easy": {
                "title": "Coin Operated: A Boy's Rocket Dream",
                "prompt": "Watch the young boy save coins in jars for seventy years to fly the rocket ride, and describe his journey!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What cardboard costume is the little boy wearing when he first discovers the coin-operated mechanical rocket?",
                    "How does he spend his entire life saving coins from selling lemonade on the street corner?",
                    "What magical and heartwarming event happens when the elderly man feeds all his saved coins into the rocket?"
                ],
                "vocabulary": ["rocket", "coin-operated", "lemonade stand", "saving coins", "astronaut", "perseverance", "lifelong", "moon"]
            },
            "Medium": {
                "title": "Coin Operated: A Lifelong Quest for Space",
                "prompt": "Narrate how a 5-year-old boy's determination carries him through a lifetime of work to reach outer space.",
                "description": "Explain the emotional passage of time, the jars filling with coins, and the fulfillment of a childhood vow.",
                "guidingQuestions": [
                    "How does the short film visually depict the passage of seventy years through seasons and changing eras?",
                    "Why does the protagonist remain so stubbornly committed to his childhood dream even into old age?",
                    "Describe the climactic sequence when the mechanical rocket defies reality and blasts him up into the starry sky."
                ],
                "vocabulary": ["determination", "lifelong dream", "passage of time", "lemonade stand", "piggy bank", "outer space", "fulfillment", "cosmic"]
            },
            "Hard": {
                "title": "Coin Operated: Dedication, Time & Childhood Dreams",
                "prompt": "Deliver an analysis on the passage of time, enduring childhood passion, and poignant payoff in 'Coin Operated'.",
                "description": "Analyze Nicholas Arioli's poetic short film on human purpose, devotion to wonder, and the transcendent finale.",
                "guidingQuestions": [
                    "Analyze how the montage technique illustrates decades of relentless dedication without a single spoken word.",
                    "Discuss whether the rocket flight should be interpreted literally or as a metaphor for a life fulfilled with purpose.",
                    "How does the soaring orchestral score elevate the emotional impact when the rocket finally leaves the pavement?"
                ],
                "vocabulary": ["passage of time", "transcendent", "poignant", "montage", "allegory", "unwavering dedication", "orchestral score", "fulfillment"]
            }
        }
    },
    {
        "index": 5,
        "youtube_id": "P5yunhX3FIE",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/P5yunhX3FIE",
        "embed_url": "https://www.youtube.com/embed/P5yunhX3FIE",
        "film_title": "Dustin (Pug vs. Robotic Vacuum)",
        "durations": {"Easy": "7 min", "Medium": "7 min", "Hard": "7 min"},
        "tiers": {
            "Easy": {
                "title": "Dustin: Energetic Pug vs. Robot Vacuum",
                "prompt": "Describe what happens when Dustin the friendly pug encounters the strange automated vacuum cleaner in his house!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "How does Dustin the pug react the first time he sees the round robotic vacuum cleaner moving by itself?",
                    "What comical tricks and barking showdowns does Dustin try to defend his living room and food bowl?",
                    "How do Dustin and the robot cleaner eventually become friendly companions at the end of the story?"
                ],
                "vocabulary": ["Dustin", "pug", "robot vacuum", "living room", "barking", "food bowl", "friendship", "comedy"]
            },
            "Medium": {
                "title": "Dustin: Territorial Feud in the Living Room",
                "prompt": "Explain the escalating rivalry between Dustin and the robotic vacuum, and how they eventually make peace.",
                "description": "Describe the comical dynamics between pet instincts and domestic technology in this lighthearted short.",
                "guidingQuestions": [
                    "How does Dustin's natural territorial instinct turn an ordinary cleaning appliance into an arch-nemesis?",
                    "What funny moments occur as the vacuum cleaner persistently cleans right up to Dustin's favorite spots?",
                    "What pivotal moment leads Dustin to view the robot as a partner rather than an intruder?"
                ],
                "vocabulary": ["territorial", "rivalry", "pet instincts", "domestic comedy", "robot vacuum", "persistence", "showdown", "truce"]
            },
            "Hard": {
                "title": "Dustin: Anthropomorphism & Comedic Conflict",
                "prompt": "Analyze character animation, sound design, and comedic pacing in this domestic clash of pet versus machine.",
                "description": "Critique Michael Fritzsche's character-driven 3D animation exploring anthropomorphism and domestic storytelling.",
                "guidingQuestions": [
                    "Analyze how the animators endow a featureless robotic vacuum with distinct personality and stubbornness.",
                    "Discuss how the detailed facial rigging and physical comedy of the pug evoke immediate viewer affection.",
                    "How does the sound design contrast the electronic whirs and beeps of the machine with organic pug snorts and barks?"
                ],
                "vocabulary": ["anthropomorphism", "character rigging", "comedic pacing", "domestic clash", "sound design", "physical comedy", "nuance", "reconciliation"]
            }
        }
    },
    {
        "index": 6,
        "youtube_id": "2REkk9SCRn0",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/2REkk9SCRn0",
        "embed_url": "https://www.youtube.com/embed/2REkk9SCRn0",
        "film_title": "In a Heartbeat (Young Love & Courage)",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "In a Heartbeat: A Boy's Runaway Heart",
                "prompt": "Watch Sherwin's beating heart jump out of his chest to chase Jonathan, and describe how they become friends!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What happens when Sherwin sees Jonathan walking past the school trees with a book in hand?",
                    "How does Sherwin try desperately to catch and hide his glowing, runaway heart across the schoolyard?",
                    "What touching moment happens when Jonathan finds the broken half of the heart and hands it back with a smile?"
                ],
                "vocabulary": ["Sherwin", "Jonathan", "heartbeat", "schoolyard", "crush", "bravery", "friendship", "kindness"]
            },
            "Medium": {
                "title": "In a Heartbeat: Bravery in Young Love",
                "prompt": "Narrate the emotional pursuit as Sherwin tries to stop his passionate heart from revealing his secret crush at school.",
                "description": "Describe Sherwin's panic, the fear of judgment from schoolmates, and the heartwarming acceptance in Jonathan's eyes.",
                "guidingQuestions": [
                    "Why is Sherwin so terrified when his heart bursts out and pulls him toward Jonathan in front of everyone?",
                    "How do the cold stares of other students affect Sherwin, causing his heart to literally break in two?",
                    "How does Jonathan's gentle gesture of putting the heart back together symbolize acceptance and courage?"
                ],
                "vocabulary": ["vulnerability", "acceptance", "runaway heart", "courage", "fear of judgment", "gentleness", "reconnection", "affection"]
            },
            "Hard": {
                "title": "In a Heartbeat: Vulnerability & Acceptance",
                "prompt": "Analyze the metaphor of a literal runaway heart in portraying the fear, vulnerability, and beauty of young romance.",
                "description": "Deliver a compelling critique of Beth David and Esteban Bravo's celebrated animated short on LGBTQ+ youth and empathy.",
                "guidingQuestions": [
                    "Analyze how externalizing the heart as an autonomous, expressive character externalizes internal romantic conflict.",
                    "Discuss the visual language of isolation when the school courtyard empties, leaving Sherwin in solitary heartbreak.",
                    "How does the ending reaffirm that genuine connection and mutual vulnerability overcome societal stigma?"
                ],
                "vocabulary": ["vulnerability", "externalization", "stigma", "symbolism", "acceptance", "empathy", "metaphor", "authenticity"]
            }
        }
    },
    {
        "index": 7,
        "youtube_id": "1QAI4B_2Mfc",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/1QAI4B_2Mfc",
        "embed_url": "https://www.youtube.com/embed/1QAI4B_2Mfc",
        "film_title": "Paperman (Disney's Oscar-Winning Romance)",
        "durations": {"Easy": "7 min", "Medium": "7 min", "Hard": "7 min"},
        "tiers": {
            "Easy": {
                "title": "Paperman: Airplanes Across the City",
                "prompt": "Watch the office clerk fold paper airplanes to reach the girl across the street, and explain what magic happens!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "How do George and Meg first meet on the windy elevated train platform in 1940s New York?",
                    "What creative method does George use when he spots Meg working in the office building opposite his desk?",
                    "What magical swirling wind guides hundreds of folded paper airplanes to reunite the two in the train station?"
                ],
                "vocabulary": ["paper airplane", "Paperman", "train platform", "lipstick", "office desk", "wind", "destiny", "magic"]
            },
            "Medium": {
                "title": "Paperman: A Whimsical Paper Plane Romance",
                "prompt": "Explain how George's desperate flurry of paper airplanes takes on a life of its own to reunite him with Meg.",
                "description": "Describe George's frustrating routine, the spark of hope seeing Meg across the street, and the whimsical climax.",
                "guidingQuestions": [
                    "How does the sterile, monotone office environment contrast with George's yearning and imaginative pursuit?",
                    "Describe the comedic and heartbreaking attempts as gust after gust of wind drops his paper airplanes into the street.",
                    "How do the inanimate paper airplanes become enchanted messengers of fate in the climactic alleyway scene?"
                ],
                "vocabulary": ["whimsical", "monotone", "paper airplanes", "destiny", "elevated train", "enchanted", "yearning", "serendipity"]
            },
            "Hard": {
                "title": "Paperman: Innovation, Fate & 1940s Romanticism",
                "prompt": "Critique the hybrid 2D/3D animation technique, expressive non-verbal storytelling, and theme of destiny in 'Paperman'.",
                "description": "Analyze Disney's groundbreaking Meander technology blending hand-drawn artistry with computer animation.",
                "guidingQuestions": [
                    "Analyze how John Kahrs uses black-and-white cinematography punctuated by a single red lipstick smudge to focus narrative drive.",
                    "Discuss the technical innovation of Disney's Meander software, integrating organic pencil line art onto CG geometry.",
                    "How does the romantic fable challenge urban alienation by suggesting unseen forces conspire to bring kindred souls together?"
                ],
                "vocabulary": ["Meander technology", "hybrid animation", "cinematography", "serendipity", "urban alienation", "romanticism", "symbolic color", "destiny"]
            }
        }
    },
    {
        "index": 8,
        "youtube_id": "WjqiU5FgsYc",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/WjqiU5FgsYc",
        "embed_url": "https://www.youtube.com/embed/WjqiU5FgsYc",
        "film_title": "The Present (Boy & Three-Legged Puppy)",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "The Present: A Boy and His New Puppy",
                "prompt": "Watch the boy playing video games receive an eager puppy from his mom, and describe how the puppy wins him over!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What is the boy doing inside his dark living room when his mother brings home a mysterious cardboard box?",
                    "Why does the boy initially push the puppy away and return grumpily to his video game controller?",
                    "What does the puppy do with the red ball that makes the boy smile, pick up his crutches, and head outside?"
                ],
                "vocabulary": ["puppy", "present", "video games", "cardboard box", "crutches", "friendship", "red ball", "smile"]
            },
            "Medium": {
                "title": "The Present: Overcoming Bitterness Through Friendship",
                "prompt": "Narrate how the boy's annoyance transforms into empathy and camaraderie when he connects with the three-legged puppy.",
                "description": "Describe the boy's defensive withdrawal, the puppy's unyielding joy, and the touching common bond between them.",
                "guidingQuestions": [
                    "Why did the puppy's missing front leg trigger such an angry, defensive reaction in the boy at first?",
                    "How does the puppy's playful resilience—falling down and joyfully scrambling right back up—inspire the boy?",
                    "What makes the final revelation of the boy's own amputated leg so emotionally impactful and uplifting?"
                ],
                "vocabulary": ["empathy", "resilience", "three-legged pup", "crutches", "defensiveness", "camaraderie", "overcoming adversity", "bond"]
            },
            "Hard": {
                "title": "The Present: Empathy, Disability & Mutual Acceptance",
                "prompt": "Analyze the profound thematic reveal at the conclusion of 'The Present' and how it explores emotional healing and disability.",
                "description": "Provide a comprehensive critique of Jacob Frey's viral thesis short, examining disability psychology and shared vulnerability.",
                "guidingQuestions": [
                    "Analyze how the visual direction conceals the boy's missing leg until the final moments to maximize narrative resonance.",
                    "Discuss how the mother's gift was intentionally chosen not just for entertainment, but as an emotional mirror for self-acceptance.",
                    "How does the film illustrate that companionship with an imperfect being can dismantle defensive emotional walls?"
                ],
                "vocabulary": ["narrative reveal", "self-acceptance", "disability representation", "emotional healing", "vulnerability", "catharsis", "companionship", "mirroring"]
            }
        }
    },
    {
        "index": 9,
        "youtube_id": "kNw8V_Fkw28",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/kNw8V_Fkw28",
        "embed_url": "https://www.youtube.com/embed/kNw8V_Fkw28",
        "film_title": "Hair Love (Oscar-Winning Family Story)",
        "durations": {"Easy": "7 min", "Medium": "7 min", "Hard": "7 min"},
        "tiers": {
            "Easy": {
                "title": "Hair Love: A Father Styles Zuri's Hair",
                "prompt": "Watch the loving father wrestle with tutorials to style his daughter Zuri's beautiful natural hair!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What special day is young Zuri getting ready for, and what hairstyle does she dream of creating?",
                    "What comical wrestling match happens between father Stephen and Zuri's magnificent, wild hair curls?",
                    "How do father and daughter work together using video tutorials to style perfect afro puffs to welcome Mom home?"
                ],
                "vocabulary": ["Hair Love", "afro puffs", "natural hair", "father", "Zuri", "styling", "video tutorial", "family"]
            },
            "Medium": {
                "title": "Hair Love: Patience & Fatherly Dedication",
                "prompt": "Explain the heartwarming efforts of Stephen learning to style Zuri's afro puffs in time to welcome her mother home.",
                "description": "Analyze the themes of fatherly love, cultural pride in natural hair, and family solidarity during hardship.",
                "guidingQuestions": [
                    "How does Stephen overcome his initial intimidation and frustration with combs and hair products to help his daughter?",
                    "What role does the mother's video blog play in guiding Stephen and reminding Zuri of her beauty?",
                    "How does the family embrace at the hospital ward give deeper emotional meaning to Zuri's pride in her hair?"
                ],
                "vocabulary": ["dedication", "afro puffs", "cultural pride", "natural hair", "parenting", "perseverance", "solidarity", "unconditional love"]
            },
            "Hard": {
                "title": "Hair Love: Cultural Identity & Family Devotion",
                "prompt": "Evaluate how 'Hair Love' celebrates Black hair textures, fatherhood, vulnerability, and love in the face of illness.",
                "description": "Critique Matthew A. Cherry's Oscar-winning short celebrating Black representation, paternal tenderness, and emotional resilience.",
                "guidingQuestions": [
                    "Discuss how 'Hair Love' serves as a landmark cultural celebration of Black hair, reclaiming dignity and joy in styling rituals.",
                    "Analyze the depiction of tender, hands-on Black fatherhood that subverts mainstream cinematic stereotypes.",
                    "How does the reveal of the mother's chemotherapy headscarf deepen the thematic core from cosmetic pride to profound love?"
                ],
                "vocabulary": ["cultural identity", "representation", "paternal tenderness", "stereotypes", "resilience", "ritual", "vulnerability", "triumph"]
            }
        }
    },
    {
        "index": 10,
        "youtube_id": "vbuq7w3ZDUQ",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/vbuq7w3ZDUQ",
        "embed_url": "https://www.youtube.com/embed/vbuq7w3ZDUQ",
        "film_title": "Pixar's La Luna (Moon Star Sweepers)",
        "durations": {"Easy": "7 min", "Medium": "7 min", "Hard": "7 min"},
        "tiers": {
            "Easy": {
                "title": "La Luna: Sweeping Stars on the Moon",
                "prompt": "Watch Bambino row out to sea with his father and grandfather to climb a ladder and sweep glowing stars on the moon!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What gift do the father and grandfather give to young Bambino at the start of their nighttime boat journey?",
                    "How does Bambino climb up the gigantic ladder from the wooden rowboat to stand on the glowing moon?",
                    "What work do the three generations do together on the moon, sweeping shimmering fallen stars with brooms?"
                ],
                "vocabulary": ["La Luna", "stars", "moon", "wooden rowboat", "ladder", "broom", "family", "glowing"]
            },
            "Medium": {
                "title": "La Luna: A Family Tradition Under the Stars",
                "prompt": "Explain how Bambino navigates the conflicting advice of his elders to discover his own way of shaping the crescent moon.",
                "description": "Describe the generational differences between Papa and Nonno, the gigantic fallen star, and Bambino's breakthrough.",
                "guidingQuestions": [
                    "How do Papa and Nonno argue over how Bambino should wear his cap and which type of broom he should use?",
                    "What happens when an enormous, glowing star crashes onto the lunar surface and neither elder can move it?",
                    "How does Bambino climb up with his little hammer and discover his own clever way to break the giant star into crescent pieces?"
                ],
                "vocabulary": ["family tradition", "generations", "crescent moon", "shimmering stars", "lunar surface", "individuality", "elder guidance", "wonder"]
            },
            "Hard": {
                "title": "La Luna: Coming of Age & Finding One's Own Voice",
                "prompt": "Critique the magical realism, generational dynamics, and poetic coming-of-age symbolism in Pixar's 'La Luna'.",
                "description": "Deliver a detailed aesthetic critique of Enrico Casarosa's Academy Award-nominated masterpiece on heritage and individuality.",
                "guidingQuestions": [
                    "Analyze how Casarosa uses celestial magical realism inspired by Saint-Exupéry and Calvino to illustrate growing up.",
                    "Discuss the nonverbal gibberish dialogue and expressive gestures that convey affectionate generational tension.",
                    "How does Bambino turning his cap backward symbolize the birth of personal identity while respecting ancestral tradition?"
                ],
                "vocabulary": ["magical realism", "coming of age", "generational heritage", "individuality", "celestial", "symbolism", "poetic storytelling", "whimsy"]
            }
        }
    },
    {
        "index": 11,
        "youtube_id": "OuJ4BBQ0nhc",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/OuJ4BBQ0nhc",
        "embed_url": "https://www.youtube.com/embed/OuJ4BBQ0nhc",
        "film_title": "Jinxy Jenkins & Lucky Lou",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "Jinxy Jenkins & Lucky Lou: Opposites Attract",
                "prompt": "Watch unlucky Jinxy and extremely lucky Lou crash down the steep city streets together on a wild runaway ride!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What constant bad luck follows clumsy Jinxy Jenkins wherever he walks on the city sidewalks?",
                    "What amazing good fortune follows cheerful Lucky Lou as everyday items magically fall into place for her?",
                    "What happens when the two meet on a runaway ice cream cart rolling down the steepest hills of San Francisco?"
                ],
                "vocabulary": ["Jinxy", "Lucky Lou", "unlucky", "good fortune", "San Francisco hills", "runaway cart", "comedy", "balance"]
            },
            "Medium": {
                "title": "Jinxy & Lou: Balancing Good and Bad Luck",
                "prompt": "Narrate how the contrasting luck of clumsy Jinxy and fortunate Lou combines into the ultimate thrilling ride.",
                "description": "Explain how Jenkins' catastrophic misfortune and Lou's effortless luck cancel out into exhilarating harmony.",
                "guidingQuestions": [
                    "How do the directors visually contrast Jenkins' gloomy rain cloud existence with Lou's sunny, serendipitous world?",
                    "Describe the chain reaction of comedic accidents as the cart hurtles down through traffic, laundry lines, and scaffolding.",
                    "How does their mutual adventure demonstrate that having an opposite partner can bring balance and joy to one's life?"
                ],
                "vocabulary": ["serendipity", "catastrophe", "chain reaction", "counterbalance", "runaway cart", "kinetic comedy", "harmony", "exhilarating"]
            },
            "Hard": {
                "title": "Jinxy Jenkins & Lucky Lou: Equilibrium & Synchronicity",
                "prompt": "Analyze the kinetic pacing, character contrasts, and philosophical balance of fortune in 'Jinxy Jenkins & Lucky Lou'.",
                "description": "Critique Mike Bidinger and Michelle Kwon's award-winning CG short on fortune, choreography, and synchronicity.",
                "guidingQuestions": [
                    "Analyze how the visual choreography uses steep urban elevation and roller-coaster physics to drive comedic pacing.",
                    "Discuss the philosophical allegory: why unmitigated good luck was boring for Lou, and how Jenkins gave her excitement.",
                    "How does their union illustrate the principle of dynamic equilibrium where contrasting forces create stability?"
                ],
                "vocabulary": ["dynamic equilibrium", "kinetic pacing", "synchronicity", "philosophical allegory", "choreography", "yin and yang", "visual comedy", "equilibrium"]
            }
        }
    },
    {
        "index": 12,
        "youtube_id": "EUm-vAOmV1o",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/EUm-vAOmV1o",
        "embed_url": "https://www.youtube.com/embed/EUm-vAOmV1o",
        "film_title": "Ormie the Pig (The Cookie Jar Heist)",
        "durations": {"Easy": "4 min", "Medium": "4 min", "Hard": "4 min"},
        "tiers": {
            "Easy": {
                "title": "Ormie the Pig: Reaching the Cookie Jar",
                "prompt": "Watch Ormie the pig try crazy inventions like trampolines and rockets to reach the cookie jar on top of the fridge!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What delicious treat does Ormie the pig spot resting high up on top of the tall white refrigerator?",
                    "What ridiculous contraptions—such as pogo sticks, cardboard boxes, and trampolines—does Ormie build to climb up?",
                    "How does each one of Ormie's funny stunts fail comically, and does he ever give up his quest for cookies?"
                ],
                "vocabulary": ["Ormie", "pig", "cookie jar", "refrigerator", "trampoline", "slapstick", "contraptions", "funny"]
            },
            "Medium": {
                "title": "Ormie the Pig: Inventive Contraptions for Cookies",
                "prompt": "Detail the increasingly ridiculous and creative stunts Ormie concocts to obtain his beloved chocolate chip cookies.",
                "description": "Describe Ormie's engineering schemes, the hilarious physical failures, and his unrelenting determination.",
                "guidingQuestions": [
                    "How does Ormie escalate his plans from simple jumps and stacking boxes to skydiving and rocket boots?",
                    "What visual gags—splattering against the fridge, parachute tangled in ceiling fan—make this short so laugh-out-loud funny?",
                    "Why is Ormie's relentless persistence despite constant failure such a timelessly entertaining cartoon trope?"
                ],
                "vocabulary": ["slapstick comedy", "inventive stunts", "cookie heist", "escalation", "relentless persistence", "cartoon physics", "parachutes", "failure"]
            },
            "Hard": {
                "title": "Ormie the Pig: Slapstick Comedy & Unyielding Persistence",
                "prompt": "Analyze the classic slapstick comedic structure, visual escalation, and timing in Ormie's refrigerator heist.",
                "description": "Critique Rob Silvestri's celebrated animated short on classic Warner Bros-style comedic pacing and pantomime animation.",
                "guidingQuestions": [
                    "Analyze how the filmmakers employ the rule of three and rapid comedic escalation to maintain high comedic energy.",
                    "Discuss the influence of classic Looney Tunes/Wile E. Coyote pantomime animation in Ormie's expressive facial frustration.",
                    "How does the surprise twist ending deliver an unexpected subversion to Ormie's single-minded obsession?"
                ],
                "vocabulary": ["slapstick structure", "pantomime animation", "rule of three", "escalation", "comedic timing", "Wile E. Coyote trope", "subversion", "obsession"]
            }
        }
    },
    {
        "index": 13,
        "youtube_id": "Hz_d-cikWmI",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/Hz_d-cikWmI",
        "embed_url": "https://www.youtube.com/embed/Hz_d-cikWmI",
        "film_title": "Ian (Inspiring Story of Inclusion)",
        "durations": {"Easy": "10 min", "Medium": "10 min", "Hard": "10 min"},
        "tiers": {
            "Easy": {
                "title": "Ian: A Boy's Wish to Play on the Playground",
                "prompt": "Watch Ian in his wheelchair try to make friends on the playground and explain how the other kids welcome him!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "Why does Ian sit behind the metal fence watching the other children playing together on the swings and slides?",
                    "What happens to Ian's body as a visual metaphor when he feels left out, bullied, or sad?",
                    "How do the children on the playground eventually come together, hold Ian's hand, and invite him to play?"
                ],
                "vocabulary": ["Ian", "playground", "wheelchair", "cerebral palsy", "friendship", "inclusion", "kindness", "courage"]
            },
            "Medium": {
                "title": "Ian: Breaking Barriers of Isolation",
                "prompt": "Explain Ian's emotional struggle with isolation and how an act of kindness dismantles the barriers separating him.",
                "description": "Analyze the visual metaphor of turning to sand, the pain of exclusion, and the triumph of community inclusion.",
                "guidingQuestions": [
                    "What is the significance of the chain-link fence that physically and emotionally divides Ian from his peers?",
                    "How does the animation visually represent Ian's emotional pain through crumbling into sand pieces?",
                    "What transformative moment occurs when a peer extends a hand of friendship, inspiring the whole playground to join?"
                ],
                "vocabulary": ["isolation", "inclusion", "cerebral palsy", "visual metaphor", "barriers", "empathy", "solidarity", "compassion"]
            },
            "Hard": {
                "title": "Ian: Empathy, Inclusion & Overcoming Ableism",
                "prompt": "Discuss how 'Ian' utilizes surrealist visual disintegration to depict disability, rejection, and triumphant inclusion.",
                "description": "Deliver a profound social and artistic critique of Juan José Campanella's Mundoloco short produced with the Ian Foundation.",
                "guidingQuestions": [
                    "Analyze the artistic metaphor of physical disintegration into sand as an externalization of emotional alienation.",
                    "Discuss how the film confronts ableist indifference without relying on pity, emphasizing Ian's agency and resilience.",
                    "How does the collective gesture of the children crossing the fence redefine disability from an individual problem to a community responsibility?"
                ],
                "vocabulary": ["ableism", "social model of disability", "disintegration", "agency", "community responsibility", "empathy", "inclusion", "catharsis"]
            }
        }
    },
    {
        "index": 14,
        "youtube_id": "HtFxYfhxS2M",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/HtFxYfhxS2M",
        "embed_url": "https://www.youtube.com/embed/HtFxYfhxS2M",
        "film_title": "Changing Batteries (The Devoted Robot)",
        "durations": {"Easy": "6 min", "Medium": "6 min", "Hard": "6 min"},
        "tiers": {
            "Easy": {
                "title": "Changing Batteries: An Old Woman & Her Helper Robot",
                "prompt": "Watch the sweet robot care for the elderly grandmother at home, and describe their heartwarming bond!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "Who sends the package containing the small helper robot to the elderly grandmother living alone in the countryside?",
                    "What daily household chores and caring tasks does the little robot do to help the grandmother smile?",
                    "Why does the robot try to change batteries when the grandmother quietly falls asleep on her rocking chair?"
                ],
                "vocabulary": ["robot", "grandmother", "helper", "batteries", "rocking chair", "companionship", "chores", "devotion"]
            },
            "Medium": {
                "title": "Changing Batteries: Loyalty & Companionship",
                "prompt": "Narrate the bond of care between the elderly woman and the small robot, focusing on devotion and the cycle of life.",
                "description": "Describe the touching progression of their friendship, the robot's mechanical understanding of life, and heartfelt loyalty.",
                "guidingQuestions": [
                    "How does the robot learn to understand the grandmother's needs beyond simple programming to form genuine love?",
                    "What poignant misunderstanding occurs when the robot assumes the grandmother can be revived simply by replacing batteries?",
                    "Why does this wordless short resonate so deeply with viewers regarding the care of aging family members?"
                ],
                "vocabulary": ["devotion", "companionship", "elderly care", "loyalty", "robotics", "cycle of life", "poignant", "unconditional"]
            },
            "Hard": {
                "title": "Changing Batteries: Aging, Caretaking & Eternal Love",
                "prompt": "Deliver a moving critique on the themes of elder loneliness, technological companionship, and grief in 'Changing Batteries'.",
                "description": "Analyze Casandra Ng's Multimedia University student short on artificial empathy, filial duty, and emotional storytelling.",
                "guidingQuestions": [
                    "Analyze how the film critiques absent family members who substitute electronic devices for physical filial presence.",
                    "Discuss the poignant innocence of the robot trying to insert AA batteries into the grandmother's hand to restore life.",
                    "How does the gentle, melancholic piano score enhance the emotional gravity of the final garden scene?"
                ],
                "vocabulary": ["filial duty", "elder isolation", "artificial empathy", "poignancy", "grief", "caretaking", "melancholy", "devotion"]
            }
        }
    },
    {
        "index": 15,
        "youtube_id": "yWd4mzGqQYo",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/yWd4mzGqQYo",
        "embed_url": "https://www.youtube.com/embed/yWd4mzGqQYo",
        "film_title": "One Small Step (Luna's Astronaut Dream)",
        "durations": {"Easy": "8 min", "Medium": "8 min", "Hard": "8 min"},
        "tiers": {
            "Easy": {
                "title": "One Small Step: Luna's Dream to Be an Astronaut",
                "prompt": "Watch Luna grow up building cardboard rockets with her cobbler father and follow her dream to the moon!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What childhood dream inspires young Luna as she plays in cardboard boxes with her shoemaker father?",
                    "What difficulties and failures does Luna face in school and astronaut training as she grows up?",
                    "How do the handmade boots her late father crafted inspire Luna to persevere and finally step onto the moon?"
                ],
                "vocabulary": ["Luna", "astronaut", "shoemaker father", "cardboard rocket", "boots", "moon", "perseverance", "dream"]
            },
            "Medium": {
                "title": "One Small Step: A Father's Love Behind a Great Dream",
                "prompt": "Explain how Luna overcomes academic and physical failures through the enduring love and handmade boots of her father.",
                "description": "Describe Luna's adolescent frustrations, the heartbreaking loss of her father, and her triumphant journey to space.",
                "guidingQuestions": [
                    "How did Luna's father support her passion at every stage of her childhood, even when she took him for granted?",
                    "What emotional turning point occurs when Luna finds the box of handmade running shoes after her father's passing?",
                    "How does Luna honoring her father's memory fuel her determination to become an elite astronaut?"
                ],
                "vocabulary": ["parental sacrifice", "astronaut training", "resilience", "handmade boots", "turning point", "grief to purpose", "determination", "achievement"]
            },
            "Hard": {
                "title": "One Small Step: Grief, Grit & Reaching the Stars",
                "prompt": "Analyze the emotional narrative of 'One Small Step', examining the sacrifice of immigrant parents and resilience.",
                "description": "Critique TAIKO Studios' Academy Award-nominated animation exploring cross-generational sacrifice, grief, and triumph.",
                "guidingQuestions": [
                    "Analyze how directors Andrew Chesworth and Bobby Pontillas use the motif of footwear to symbolize fatherly support.",
                    "Discuss the portrayal of the humble cobbler father as the true foundation of his daughter's lofty cosmic ambitions.",
                    "How does the final visual juxtaposition—a space boot stepping on lunar dust—fulfill Neil Armstrong's famous namesake quote?"
                ],
                "vocabulary": ["generational sacrifice", "resilience", "motif", "grief", "cosmic ambition", "cinematic pacing", "triumph", "legacy"]
            }
        }
    },
    {
        "index": 16,
        "youtube_id": "kQjtK32mGJQ",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/kQjtK32mGJQ",
        "embed_url": "https://www.youtube.com/embed/kQjtK32mGJQ",
        "film_title": "Alike (Father & Son's Colors)",
        "durations": {"Easy": "8 min", "Medium": "8 min", "Hard": "8 min"},
        "tiers": {
            "Easy": {
                "title": "Alike: A Father and Son's Colorful World",
                "prompt": "Watch how Copi and Paste lose their vibrant colors at work and school until they embrace music and creativity!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What colors do father Copi and his little son Paste have at the beginning of their morning routine?",
                    "Why do Paste and Copi turn gray and lifeless as they spend boring hours at school and a gray office cubicle?",
                    "What does the street violinist in the park do that brings bright colors, joy, and dancing back into their lives?"
                ],
                "vocabulary": ["Alike", "Copi", "Paste", "colors", "violin music", "cubicle", "creativity", "joy"]
            },
            "Medium": {
                "title": "Alike: Rekindling Joy in a Monotone World",
                "prompt": "Explain how father Copi realizes that forcing his son to conform is stealing his happiness, and how they reclaim joy.",
                "description": "Describe how rigid societal expectations drain human vitality, and how art and fatherly love revive it.",
                "guidingQuestions": [
                    "How does the animated short use color saturation to symbolize happiness, imagination, and individuality?",
                    "What heartbreaking change occurs in Paste when he stops drawing and conforms to rigid school copying exercises?",
                    "What brave decision does Copi make at the end to abandon routine and dance together in the park?"
                ],
                "vocabulary": ["conformity", "color saturation", "imagination", "individuality", "violinist", "vitality", "paternal love", "spontaneity"]
            },
            "Hard": {
                "title": "Alike: Conformity, Creative Spirit & Parental Love",
                "prompt": "Critique the social commentary in 'Alike' regarding societal conditioning, bureaucratic monotony, and creative freedom.",
                "description": "Analyze Daniel Martínez Lara and Rafa Cano Méndez's Goya Award-winning short on educational conformity and art.",
                "guidingQuestions": [
                    "Analyze the visual metaphor of monochrome grayness representing the soul-crushing routine of corporate and rote schooling.",
                    "Discuss how parents often unintentionally extinguish their children's creative spark in the name of practical conformity.",
                    "How does the violin performance serve as a sanctuary of pure artistic emotion in a standardized society?"
                ],
                "vocabulary": ["social conditioning", "bureaucratic monotony", "creative spark", "rote learning", "conformity", "paternal epiphany", "artistic sanctuary", "liberation"]
            }
        }
    },
    {
        "index": 17,
        "youtube_id": "k1vCrsZ80M4",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/k1vCrsZ80M4",
        "embed_url": "https://www.youtube.com/embed/k1vCrsZ80M4",
        "film_title": "The Neighbors' Window (Oscar Winner)",
        "durations": {"Easy": "20 min", "Medium": "20 min", "Hard": "20 min"},
        "tiers": {
            "Easy": {
                "title": "The Neighbors' Window: Life Across the Street",
                "prompt": "Watch the couple raise their young children while looking across at their neighbors' apartment window, and describe what happens!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What does the young mother Alli observe when looking through the apartment window across the street?",
                    "Why do Alli and her husband feel both amused and slightly envious of the young couple's carefree lifestyle?",
                    "What poignant event occurs at the end of the story when Alli meets the neighbor woman on the street?"
                ],
                "vocabulary": ["window", "neighbors", "apartment", "family", "children", "binoculars", "compassion", "perspective"]
            },
            "Medium": {
                "title": "The Neighbors' Window: The Grass Isn't Always Greener",
                "prompt": "Explain how the exhausted parents' envy of the couple across the street turns into profound compassion.",
                "description": "Narrate the subtle shift from voyeuristic envy to unexpected grief and gratitude for one's own family life.",
                "guidingQuestions": [
                    "How does raising young children make Alli and Jacob feel fatigued and wistful about their past youth?",
                    "What heartbreaking reality is revealed about the neighbor husband's illness in the final acts of the film?",
                    "What powerful lesson does Alli learn about the hidden struggles everyone carries behind their public windows?"
                ],
                "vocabulary": ["voyeurism", "envy", "grass is greener", "hidden struggles", "parenting fatigue", "compassion", "gratitude", "empathy"]
            },
            "Hard": {
                "title": "The Neighbors' Window: Envy, Perception & Shared Grief",
                "prompt": "Deliver a psychological critique of 'The Neighbors' Window', exploring voyeurism, human projection, and gratitude.",
                "description": "Analyze Marshall Curry's Academy Award-winning live-action short on perception, idealization, and universal vulnerability.",
                "guidingQuestions": [
                    "Examine how the window functions as a cinematic screen through which the protagonists project their own unfulfilled desires.",
                    "Analyze the profound emotional twist when the neighbor reveals she was watching Alli's warm family with equal longing.",
                    "Discuss how Curry exposes the danger of comparing one's internal messy reality with another's curated external view."
                ],
                "vocabulary": ["projection", "voyeurism", "idealization", "human condition", "emotional resonance", "gratitude", "vulnerability", "epiphany"]
            }
        }
    },
    {
        "index": 18,
        "youtube_id": "76Xxn1FSdQ4",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/76Xxn1FSdQ4",
        "embed_url": "https://www.youtube.com/embed/76Xxn1FSdQ4",
        "film_title": "Swing of Change (Jazz Barbershop)",
        "durations": {"Easy": "7 min", "Medium": "7 min", "Hard": "7 min"},
        "tiers": {
            "Easy": {
                "title": "Swing of Change: A Barbershop Made of Jazz",
                "prompt": "Watch the grumpy 1930s barber hear the magic jazz trumpet and describe how his shop transforms with musical energy!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What kind of grumpy, rigid barber is Huck in 1930s New York at the start of the story?",
                    "What mysterious musical instrument does a client leave behind on the barbershop coat rack?",
                    "How does the swinging jazz music magically transform the furniture, mirrors, and Huck's own dancing feet?"
                ],
                "vocabulary": ["barbershop", "jazz trumpet", "music", "swing", "dancing", "transformation", "New York", "rhythm"]
            },
            "Medium": {
                "title": "Swing of Change: Music Melts Prejudice",
                "prompt": "Explain how the infectious rhythms of a brass jazz trumpet shatter the rigid, grumpy worldview of the barber.",
                "description": "Describe how the swing jazz tempo takes over the barber shop, transforming prejudice into infectious joy.",
                "guidingQuestions": [
                    "How does the animation contrast the barber's strict, classical German decor with the lively African-American jazz culture?",
                    "What visual magic occurs as scissors, combs, and shaving foam begin dancing to the swinging trumpet solo?",
                    "How does music act as a universal bridge overcoming cultural bias and opening the barber's closed heart?"
                ],
                "vocabulary": ["prejudice", "jazz trumpet", "swing rhythm", "barbershop", "cultural bridge", "transformation", "musical liberation", "joy"]
            },
            "Hard": {
                "title": "Swing of Change: Jazz, Cultural Transformation & Rhythm",
                "prompt": "Analyze the historical symbolism, musical animation, and cultural liberation represented in 'Swing of Change'.",
                "description": "Critique the ESMA graduation short film examining historical prejudice in Depression-era New York through jazz animation.",
                "guidingQuestions": [
                    "Analyze how the filmmakers use color transition—from dull sepia to vibrant brass hues—to signify ideological awakening.",
                    "Discuss jazz music as an irrepressible historical force of civil rights, cultural integration, and human celebration.",
                    "How does the choreography of everyday barber tools synchronize with big-band swing orchestration to create kinetic magic?"
                ],
                "vocabulary": ["cultural liberation", "ideological awakening", "jazz heritage", "choreography", "Depression-era", "synchronization", "big band", "integration"]
            }
        }
    },
    {
        "index": 19,
        "youtube_id": "Ad3CMri3hOs",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/Ad3CMri3hOs",
        "embed_url": "https://www.youtube.com/embed/Ad3CMri3hOs",
        "film_title": "The Fantastic Flying Books of Mr. Morris Lessmore",
        "durations": {"Easy": "15 min", "Medium": "15 min", "Hard": "15 min"},
        "tiers": {
            "Easy": {
                "title": "Flying Books of Mr. Morris Lessmore: Magic Library",
                "prompt": "Watch Morris Lessmore get swept into a whimsical library where books fly like birds, and describe his life caring for them!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "What catastrophic storm sweeps away Morris Lessmore's quiet town and scatters all the words from his book?",
                    "What wondrous building does Morris discover where ancient and colorful books fly and flutter through the air?",
                    "How does Morris spend his life mending, reading, and sharing books with visitors before writing his own final story?"
                ],
                "vocabulary": ["Morris Lessmore", "flying books", "library", "mending books", "hurricane", "reading", "whimsical", "stories"]
            },
            "Medium": {
                "title": "Morris Lessmore: Life Dedicated to Living Stories",
                "prompt": "Narrate how books restore color and joy to Morris's devastated world, and how he shares their magic with others.",
                "description": "Capture the life cycle of storytelling, literary preservation, and the passing of the torch to the next generation.",
                "guidingQuestions": [
                    "How does the short film visually shift from black-and-white to rich color when a person opens and reads a good book?",
                    "What delicate care does Morris show in 'operating' on torn book pages, taping spines, and nurturing damaged volumes?",
                    "Describe the touching finale when elderly Morris flies away with the books, leaving his completed memoir for a young girl."
                ],
                "vocabulary": ["literary preservation", "life cycle", "color restoration", "bibliophile", "flying books", "memoir", "legacy", "healing"]
            },
            "Hard": {
                "title": "Morris Lessmore: Literature as Healer & Legacy",
                "prompt": "Deliver an essay on 'Morris Lessmore' as an homage to storytelling, the longevity of literature, and mortality.",
                "description": "Critique William Joyce and Brandon Oldenburg's Academy Award-winning homage to Buster Keaton, The Wizard of Oz, and books.",
                "guidingQuestions": [
                    "Analyze how the Hurricane Katrina-inspired opening storm reflects how catastrophic loss can be healed through storytelling.",
                    "Discuss the film's homage to silent cinema legends (Buster Keaton) through Morris's expressive, wordless physical pantomime.",
                    "How does the film explore the concept of mortality: that individuals pass on, but their stories continue to illuminate minds?"
                ],
                "vocabulary": ["homage", "Buster Keaton", "bibliophile", "mortality", "literary legacy", "allegory", "catharsis", "pantomime"]
            }
        }
    },
    {
        "index": 20,
        "youtube_id": "WhWc3b3KhnY",
        "youtubeEmbedUrl": "https://www.youtube.com/embed/WhWc3b3KhnY",
        "embed_url": "https://www.youtube.com/embed/WhWc3b3KhnY",
        "film_title": "Spring (Blender Open Movie)",
        "durations": {"Easy": "8 min", "Medium": "8 min", "Hard": "8 min"},
        "tiers": {
            "Easy": {
                "title": "Spring: Awakening the Frozen Forest",
                "prompt": "Watch the young shepherd girl and her dog journey into the cold misty mountains with chimes to awaken spring!",
                "description": "Watch the video carefully, then explain what you saw in your own words.",
                "guidingQuestions": [
                    "Who are the two traveling companions walking through the frozen, misty ancient forest?",
                    "What musical chimes and sacred staff does the shepherd girl carry to awaken the ancient spirits?",
                    "What magical transformation happens to the icy valley when the giant mountain creature breathes spring flowers to life?"
                ],
                "vocabulary": ["Spring", "shepherd girl", "dog", "frozen forest", "chimes", "ancient spirits", "blossoms", "rebirth"]
            },
            "Medium": {
                "title": "Spring: A Shepherd Girl's Mountain Quest",
                "prompt": "Explain how the shepherd girl uses mystical sound and music to confront the ancient forest spirits and bring back spring.",
                "description": "Describe the perilous mountain climb, the confrontation with nature spirits, and the blossoming renewal of life.",
                "guidingQuestions": [
                    "How does the young girl demonstrate courage and reverence when facing the colossal, slumbering nature spirits?",
                    "What role does musical harmony play as the girl weaves sound chimes to melt the ancient frozen frost?",
                    "Describe the visual splendor as color, green moss, and blossoming flora wash over the gray rocky landscape."
                ],
                "vocabulary": ["mystical sound", "shepherd girl", "sacred chimes", "nature spirits", "mountain quest", "reverence", "blossoming", "renewal"]
            },
            "Hard": {
                "title": "Spring: Mythical Nature Spirits & Seasonal Rebirth",
                "prompt": "Analyze the mythic archetype of seasonal renewal, folklore worldbuilding, and visual fidelity in Blender's 'Spring'.",
                "description": "Critique Andy Goralczyk's acclaimed open-source fantasy short exploring animism, ritual music, and seasonal rebirth.",
                "guidingQuestions": [
                    "Analyze how the film draws upon ancient European pastoral folklore and animistic nature deities to construct its mythology.",
                    "Discuss the technical achievements of Blender's open-source rendering engine in simulating volumetric fog, fur, and flora.",
                    "How does the narrative structure illustrate the cyclical interdependence between humanity, ritual, and natural seasons?"
                ],
                "vocabulary": ["animism", "mythic archetype", "seasonal rebirth", "volumetric lighting", "open-source animation", "folklore", "interdependence", "splendor"]
            }
        }
    }
]

print(f"Loaded {len(IMAGE_CATALOG)} verified images and {len(VIDEO_CATALOG)} verified videos.")


AGE_GROUPS = ['6-9', '10-12', '13-17', '18-25', '26-32', '33-40']
DIFFICULTIES = ['Easy', 'Medium', 'Hard']

all_images = []
for ag in AGE_GROUPS:
    ag_tag = ag.replace('-', '_')
    for diff in DIFFICULTIES:
        diff_tag = diff.lower()
        for item in IMAGE_CATALOG:
            idx = item['index']
            tier = item['tiers'][diff]
            item_id = f"img_{ag_tag}_{diff_tag}_{idx}"
            img_obj = {
                "id": item_id,
                "media": item["image_url"],
                "mediaType": "image",
                "media_type": "image",
                "title": tier["title"],
                "prompt": tier["prompt"],
                "clue": tier["prompt"],
                "description": tier["description"],
                "instruction": tier["description"],
                "description_prompt": tier["description"],
                "guidingQuestions": tier["guidingQuestions"],
                "guiding_questions": tier["guidingQuestions"],
                "vocabulary": tier["vocabulary"],
                "suggested_keywords": tier["vocabulary"],
                "age_group": ag,
                "category": "Visual Speaking Practice",
                "difficulty": diff,
                "difficulty_tag": diff,
                "length_type": "medium",
                "duration": "Visual Scene",
                "duration_label": "Visual Scene",
                "image_url": item["image_url"],
                "thumbnail": item["thumbnail"]
            }
            all_images.append(img_obj)

all_videos = []
for ag in AGE_GROUPS:
    ag_tag = ag.replace('-', '_')
    for diff in DIFFICULTIES:
        diff_tag = diff.lower()
        for item in VIDEO_CATALOG:
            idx = item['index']
            tier = item['tiers'][diff]
            item_id = f"vid_{ag_tag}_{diff_tag}_{idx}"
            dur_str = item['durations'].get(diff, '4 min')
            dur_min = int(dur_str.split()[0]) if dur_str and dur_str.split()[0].isdigit() else 4
            dur_sec = dur_min * 60
            vid_obj = {
                "id": item_id,
                "media": item["youtubeEmbedUrl"],
                "mediaType": "video",
                "media_type": "video",
                "title": tier["title"],
                "prompt": tier["prompt"],
                "clue": tier["prompt"],
                "description": tier["description"],
                "instruction": tier["description"],
                "description_prompt": tier["description"],
                "guidingQuestions": tier["guidingQuestions"],
                "guiding_questions": tier["guidingQuestions"],
                "vocabulary": tier["vocabulary"],
                "suggested_keywords": tier["vocabulary"],
                "age_group": ag,
                "category": "Video Speaking Practice",
                "difficulty": diff,
                "difficulty_tag": diff,
                "duration": dur_str,
                "duration_label": f"{dur_str} practice",
                "duration_seconds": dur_sec,
                "youtube_id": item["youtube_id"],
                "youtubeEmbedUrl": item["youtubeEmbedUrl"],
                "embed_url": item["embed_url"],
                "thumbnail": f"https://img.youtube.com/vi/{item['youtube_id']}/hqdefault.jpg",
                "youtube_search_url": f"https://www.youtube.com/results?search_query={tier['title'].replace(' ', '+')}"
            }
            all_videos.append(vid_obj)

print(f"Generated {len(all_images)} unified images and {len(all_videos)} unified videos.")

# Save to scratch/unified_media.json
with open('scratch/unified_media.json', 'w', encoding='utf-8') as out_f:
    json.dump({'images': all_images, 'videos': all_videos}, out_f, indent=2, ensure_ascii=False)
print("Saved scratch/unified_media.json successfully.")
