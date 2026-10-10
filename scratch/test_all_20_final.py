import urllib.request
import json

videos_to_test = [
    {
        "id": "therapy_vid_1",
        "title": "The ABCs of Stuttering",
        "category": "Kids & Schools",
        "category_key": "kids",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "69Q_3VQ07vA",
        "thumbnail": "https://img.youtube.com/vi/69Q_3VQ07vA/hqdefault.jpg",
        "duration": "10 min",
        "target_audience": "Students, Parents & Teachers",
        "description": "Students who stutter talk openly about classroom experiences, answering questions and sharing what helps them feel confident participating in class.",
        "key_takeaways": [
            "Classroom strategies for students and educators",
            "Addressing teasing and speaking pressure constructively",
            "Creating a supportive, open environment for talking"
        ]
    },
    {
        "id": "therapy_vid_2",
        "title": "Stuttering: For Kids, By Kids",
        "category": "Kids & Teens",
        "category_key": "kids",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "Po-WMo8vXRY",
        "thumbnail": "https://img.youtube.com/vi/Po-WMo8vXRY/hqdefault.jpg",
        "duration": "12 min",
        "target_audience": "Children & Young Students",
        "description": "Real children who stutter share their thoughts, feelings, and strategies for overcoming fears and speaking openly with friends and teachers.",
        "key_takeaways": [
            "Normalizing disfluency among peers and classmates",
            "Expressing thoughts openly without fear or shame",
            "Practical speech tips directly from children who stutter"
        ]
    },
    {
        "id": "therapy_vid_3",
        "title": "Stuttering: For Kids, By Kids 2.0",
        "category": "Kids & Teens",
        "category_key": "kids",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "Mn2iAfkqews",
        "thumbnail": "https://img.youtube.com/vi/Mn2iAfkqews/hqdefault.jpg",
        "duration": "14 min",
        "target_audience": "Elementary & Middle Schoolers",
        "description": "A modern, updated look at stuttering through the eyes of diverse children, discussing school presentations, friendships, and self-advocacy.",
        "key_takeaways": [
            "Building proactive self-advocacy in school settings",
            "Handling classroom presentations and reading aloud",
            "Embracing communication diversity and personal strengths"
        ]
    },
    {
        "id": "therapy_vid_4",
        "title": "Stuttering: Straight Talk for Teens",
        "category": "Teens & Young Adults",
        "category_key": "teens",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "7SUcxAjG2GI",
        "thumbnail": "https://img.youtube.com/vi/7SUcxAjG2GI/hqdefault.jpg",
        "duration": "30 min",
        "target_audience": "Teenagers & High Schoolers",
        "description": "Teenagers speak candidly about dating, high school life, job interviews, and how speech therapy techniques empowered their daily communication.",
        "key_takeaways": [
            "Navigating social relationships, dating, and peer dynamics",
            "Job interview and college presentation preparation",
            "Evidence-based therapy techniques for daily speech freedom"
        ]
    },
    {
        "id": "therapy_vid_5",
        "title": "Stuttering: Straight Talk for Teachers",
        "category": "Schools & Educators",
        "category_key": "kids",
        "source": "The Stuttering Foundation & ASHA",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "ix65403ruKI",
        "thumbnail": "https://img.youtube.com/vi/ix65403ruKI/hqdefault.jpg",
        "duration": "18 min",
        "target_audience": "Teachers & School Pathologists",
        "description": "Expert guidance for educators on creating an inclusive classroom, handling reading aloud, preventing bullying, and supporting fluent turn-taking.",
        "key_takeaways": [
            "Best practices for oral reading and presentations in class",
            "Fostering psychological safety and patience in the classroom",
            "Effective collaboration with Speech-Language Pathologists"
        ]
    },
    {
        "id": "therapy_vid_6",
        "title": "7 Tips for Talking with the Child Who Stutters",
        "category": "Parents & Families",
        "category_key": "parents",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "wTpckAufNDE",
        "thumbnail": "https://img.youtube.com/vi/wTpckAufNDE/hqdefault.jpg",
        "duration": "8 min",
        "target_audience": "Parents & Caregivers",
        "description": "Practical, everyday conversational tips for parents and caregivers to reduce time pressure and create relaxed speaking environments.",
        "key_takeaways": [
            "Unrushed conversational pacing and natural pauses",
            "Listening attentively to what is said rather than how it is said",
            "Reducing conversational competition and time pressure at home"
        ]
    },
    {
        "id": "therapy_vid_7",
        "title": "Stuttering and Your Child: Help for Parents",
        "category": "Parents & Families",
        "category_key": "parents",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "u2_mgt87g1Y",
        "thumbnail": "https://img.youtube.com/vi/u2_mgt87g1Y/hqdefault.jpg",
        "duration": "30 min",
        "target_audience": "Parents & Family Members",
        "description": "Clinical experts and parents explore early childhood disfluency, when to seek speech-language therapy, and how home routines make a difference.",
        "key_takeaways": [
            "Distinguishing developmental disfluency from persistent stuttering",
            "When and how to seek early professional intervention",
            "Creating speech-friendly routines and supportive home dialogue"
        ]
    },
    {
        "id": "therapy_vid_8",
        "title": "Kids Who Stutter: Parents Speak",
        "category": "Parents & Families",
        "category_key": "parents",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "03yQQo_LUf0",
        "thumbnail": "https://img.youtube.com/vi/03yQQo_LUf0/hqdefault.jpg",
        "duration": "16 min",
        "target_audience": "Parents & Families",
        "description": "Honest discussions from parents about their emotional journeys, finding the right speech-language pathologist, and nurturing their child's voice.",
        "key_takeaways": [
            "Navigating parental worry and letting go of guilt",
            "Partnering effectively with speech therapy professionals",
            "Nurturing confidence, communication courage, and emotional health"
        ]
    },
    {
        "id": "therapy_vid_9",
        "title": "Back to the Basics: Advice for Adults Who Stutter",
        "category": "Foundations & Awareness",
        "category_key": "teens",
        "source": "The Stuttering Foundation",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "_tE_Smzf_xU",
        "thumbnail": "https://img.youtube.com/vi/_tE_Smzf_xU/hqdefault.jpg",
        "duration": "15 min",
        "target_audience": "Adults & Self-Advocates",
        "description": "A comprehensive overview breaking down core speech motor principles, self-advocacy, and emotional resilience for adults who stutter.",
        "key_takeaways": [
            "Affective dimension: addressing fear, tension, and emotional weight",
            "Behavioral dimension: understanding core repetitions and blocks",
            "Cognitive dimension: reshaping beliefs about speech capability"
        ]
    },
    {
        "id": "therapy_vid_10",
        "title": "Stuttering 101",
        "category": "Foundations & Awareness",
        "category_key": "techniques",
        "source": "The Stuttering Foundation & Dr. Barry Guitar",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "MXh9OWIIU5g",
        "thumbnail": "https://img.youtube.com/vi/MXh9OWIIU5g/hqdefault.jpg",
        "duration": "12 min",
        "target_audience": "General Public & Beginners",
        "description": "An accessible introduction explaining neurogenic foundations, common misconceptions, secondary behaviors, and evidence-based treatment pathways.",
        "key_takeaways": [
            "Debunking pervasive myths and societal stereotypes",
            "Neurobiology of speech motor planning and timing",
            "Comprehensive, evidence-based therapy pathways"
        ]
    },
    {
        "id": "therapy_vid_11",
        "title": "Stuttering Well: Self-Management & Spontaneity",
        "category": "Self-Management & Fluency",
        "category_key": "techniques",
        "source": "AIS & Dr. Christopher Constantino",
        "source_url": "https://stutteringtreatment.org",
        "youtube_id": "jaAfq8Gvmy4",
        "thumbnail": "https://img.youtube.com/vi/jaAfq8Gvmy4/hqdefault.jpg",
        "duration": "22 min",
        "target_audience": "Adults & Self-Advocates",
        "description": "Moving from struggle and tension to ease, spontaneity, and joyful communication through self-compassion and speech agency.",
        "key_takeaways": [
            "Redefining speaking success beyond zero disfluency",
            "Communicating with physical ease and spontaneous joy",
            "Cultivating agency, ease, and authenticity in conversation"
        ]
    },
    {
        "id": "therapy_vid_12",
        "title": "Dealing Effectively with Attitudes and Emotions",
        "category": "Emotional Well-being",
        "category_key": "emotions",
        "source": "The Stuttering Foundation & Vivian Sisskin, M.S.",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "-R85B1lij2A",
        "thumbnail": "https://img.youtube.com/vi/-R85B1lij2A/hqdefault.jpg",
        "duration": "25 min",
        "target_audience": "Teens, Adults & Clinicians",
        "description": "Clinically proven strategies to unravel fear, anticipation, and negative self-talk associated with speaking blocks and social situations.",
        "key_takeaways": [
            "Cognitive reframing for anticipatory speech anxiety",
            "Untangling emotional reactivity from physical speech blocks",
            "Developing lasting resilience in challenging social situations"
        ]
    },
    {
        "id": "therapy_vid_13",
        "title": "Helping Children Who Stutter Overcome Bullying",
        "category": "Emotional Well-being",
        "category_key": "emotions",
        "source": "MedBridge & William Murphy, M.A.",
        "source_url": "https://www.medbridge.com",
        "youtube_id": "OJ2o3OF_XP0",
        "thumbnail": "https://img.youtube.com/vi/OJ2o3OF_XP0/hqdefault.jpg",
        "duration": "28 min",
        "target_audience": "Adults, Families & Therapists",
        "description": "A compassionate deep dive into unburdening the shame cycle, handling teasing constructively, and building communicative confidence.",
        "key_takeaways": [
            "Deconstructing internalized shame, secrecy, and avoidance",
            "The therapeutic benefit of self-disclosure in reducing fear",
            "Reclaiming self-worth, communicative dignity, and vocal pride"
        ]
    },
    {
        "id": "therapy_vid_14",
        "title": "Building Confidence and Resilience in Children Who Stutter",
        "category": "Confidence & Resilience",
        "category_key": "emotions",
        "source": "SAY: The Stuttering Association for the Young",
        "source_url": "https://www.say.org",
        "youtube_id": "QmepajAKavs",
        "thumbnail": "https://img.youtube.com/vi/QmepajAKavs/hqdefault.jpg",
        "duration": "18 min",
        "target_audience": "Children, Teens & Parents",
        "description": "Evidence-informed approaches to helping young people build emotional fortitude, self-worth, and communicative pride beyond fluency.",
        "key_takeaways": [
            "Strength-based and solution-focused empowerment methodologies",
            "Building communicative courage and self-belief in social arenas",
            "Empowering young people to express every thought freely"
        ]
    },
    {
        "id": "therapy_vid_15",
        "title": "Empowering Authenticity: Moving from Pressure to Presence",
        "category": "Confidence & Resilience",
        "category_key": "emotions",
        "source": "National Stuttering Association",
        "source_url": "https://westutter.org",
        "youtube_id": "KxgFAaxZAzI",
        "thumbnail": "https://img.youtube.com/vi/KxgFAaxZAzI/hqdefault.jpg",
        "duration": "24 min",
        "target_audience": "Adults, Teens & Clinicians",
        "description": "Practical therapeutic frameworks for clinicians and families to foster resilience, shift from pressure to presence, and communicate with ease.",
        "key_takeaways": [
            "Resilience-building frameworks in daily communication",
            "Preventing speech avoidance and apprehension from taking root",
            "Fostering positive communicative curiosity and authentic connection"
        ]
    },
    {
        "id": "therapy_vid_16",
        "title": "The Role of Acceptance, Commitment and Mindfulness in Stuttering Therapy",
        "category": "Mindfulness & ACT",
        "category_key": "emotions",
        "source": "The Stuttering Foundation & Clinical Specialists",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "9LP54UCtrrc",
        "thumbnail": "https://img.youtube.com/vi/9LP54UCtrrc/hqdefault.jpg",
        "duration": "32 min",
        "target_audience": "Adults & Clinical Pathologists",
        "description": "How Acceptance and Commitment Therapy (ACT) and mindful breath awareness help individuals detach from speech anxiety and live meaningfully.",
        "key_takeaways": [
            "Mindfulness exercises to soften physical tension and panic",
            "Defusion techniques to distance from unhelpful internal critic",
            "Aligning daily communication goals with core personal values"
        ]
    },
    {
        "id": "therapy_vid_17",
        "title": "Using Voluntary Stuttering to Empower Children Who Stutter",
        "category": "Clinical Techniques",
        "category_key": "techniques",
        "source": "The Stuttering Foundation & Dr. Joseph Donaher",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "JDcpe4lOWD8",
        "thumbnail": "https://img.youtube.com/vi/JDcpe4lOWD8/hqdefault.jpg",
        "duration": "20 min",
        "target_audience": "Children, Teens & Clinicians",
        "description": "Understanding the therapeutic power of stuttering on purpose to desensitize fear, release physical tension, and regain vocal control.",
        "key_takeaways": [
            "Demystifying speech blocks through intentional, easy disfluency",
            "Desensitizing fear and eradicating anticipatory panic",
            "Gaining mastery and conscious control over vocal articulators"
        ]
    },
    {
        "id": "therapy_vid_18",
        "title": "Co-existing ADHD and Childhood Stuttering",
        "category": "Clinical Techniques",
        "category_key": "techniques",
        "source": "The Stuttering Foundation & Dr. Joseph Donaher",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "DJxkoYWWX_o",
        "thumbnail": "https://img.youtube.com/vi/DJxkoYWWX_o/hqdefault.jpg",
        "duration": "16 min",
        "target_audience": "Educators, Parents & Therapists",
        "description": "Step-by-step techniques and therapeutic considerations for children managing both attention differences and speech disfluency.",
        "key_takeaways": [
            "Understanding the neurological overlap between ADHD and speech motor planning",
            "Pacing and focus strategies for calm speech production",
            "Structured turn-taking routines for home and classroom"
        ]
    },
    {
        "id": "therapy_vid_19",
        "title": "Confident Presentations and Communication for People Who Stutter",
        "category": "Teens & Young Adults",
        "category_key": "teens",
        "source": "National Stuttering Association",
        "source_url": "https://westutter.org",
        "youtube_id": "vMFsdiO6yHI",
        "thumbnail": "https://img.youtube.com/vi/vMFsdiO6yHI/hqdefault.jpg",
        "duration": "26 min",
        "target_audience": "Adolescents, Adults & Professionals",
        "description": "Specialized communication strategies targeting school and workplace presentations, peer support, and personal empowerment.",
        "key_takeaways": [
            "Addressing adolescent social dynamics, peer groups, and school pressure",
            "Developing presentation skills and public speaking readiness",
            "Integrating speech modification tools seamlessly into daily life"
        ]
    },
    {
        "id": "therapy_vid_20",
        "title": "Avoidance Reduction Therapy & Stuttering Modification in Action",
        "category": "Clinical Techniques",
        "category_key": "techniques",
        "source": "The Stuttering Foundation & Vivian Sisskin, M.S.",
        "source_url": "https://www.stutteringhelp.org",
        "youtube_id": "OjuD8RBNDz4",
        "thumbnail": "https://img.youtube.com/vi/OjuD8RBNDz4/hqdefault.jpg",
        "duration": "28 min",
        "target_audience": "Adults, Teens & Clinicians",
        "description": "Masterclass on Avoidance Reduction Therapy (ARTS®) and speech modification: reducing struggle, easing fear, and speaking with open spontaneity.",
        "key_takeaways": [
            "Avoidance reduction: dismantling covert habits and fear of stuttering",
            "Shifting out of hard struggle blocks into easy, open phonation",
            "Fostering comfort, communicative freedom, and authentic expression"
        ]
    }
]

print(f"Testing all {len(videos_to_test)} videos...")
passed = 0
for idx, v in enumerate(videos_to_test):
    vid_id = v["youtube_id"]
    oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={vid_id}&format=json"
    thumb_url = v["thumbnail"]
    try:
        # 1. Check YouTube validity
        req = urllib.request.Request(oembed_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=5) as resp:
            data = json.loads(resp.read().decode('utf-8'))
            yt_title = data.get('title')
        
        # 2. Check thumbnail image validity
        req_thumb = urllib.request.Request(thumb_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req_thumb, timeout=5) as resp_thumb:
            thumb_status = resp_thumb.status

        print(f"[{idx+1}/20 PASS] {v['id']} ({v['title']}) -> YouTube Title: '{yt_title}' | Thumb Status: {thumb_status}")
        passed += 1
    except Exception as e:
        print(f"[{idx+1}/20 FAIL] {v['id']} ({v['title']}) -> Error: {e}")

print(f"\nALL TESTED: {passed} / {len(videos_to_test)} PASSED")
