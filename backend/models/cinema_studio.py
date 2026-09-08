"""
Vernacular AI - Cinema & English Film Vernacular Dubbing & Subtitle Studio
Enables non-English speakers to watch and enjoy English movies with synchronized
vernacular subtitles, AI audio dubbing, and cultural idiom explanations.
"""

from .translator import translate_text, get_language_code

# Curated Cinema Scenes for instant demonstration
CINEMA_SCENES = [
    {
        "id": "pursuit_of_happyness",
        "title": "The Pursuit of Happyness",
        "scene_name": "Protect Your Dream (Father-Son Speech)",
        "genre": "Inspirational / Drama",
        "speaker": "Chris Gardner (Will Smith)",
        "poster_emoji": "🏀",
        "bg_gradient": "linear-gradient(135deg, #1e3c72 0%, #2a5298 100%)",
        "description": "A struggling father teaches his young son never to let anyone stop him from achieving his dreams.",
        "cultural_notes": "English cinema uses phrases like 'Period' to mean 'Final Decision / End of discussion'. In Tamil: 'அவ்வளவுதான், இதற்கு மேல் மாற்றுப் பேச்சே இல்லை'.",
        "dialogues": [
            {
                "start": 0.0,
                "end": 4.5,
                "english": "Don't ever let somebody tell you... you can't do something.",
                "idiom": "Don't ever let somebody tell you",
                "idiom_explanation": "யாராவது நீ எதையும் செய்ய முடியாது என்று சொல்வதை ஒருபோதும் அனுமதிக்காதே."
            },
            {
                "start": 4.5,
                "end": 8.0,
                "english": "Not even me. All right?",
                "idiom": "Not even me",
                "idiom_explanation": "உன் சொந்த தந்தையான நானாக இருந்தாலும் கூட அதை ஒப்புக்கொள்ளாதே."
            },
            {
                "start": 8.0,
                "end": 12.0,
                "english": "You got a dream... you gotta protect it.",
                "idiom": "you gotta protect it",
                "idiom_explanation": "உனக்கென்று ஒரு லட்சியம் இருந்தால், அதை நீயே உயிராகக் காப்பாற்ற வேண்டும்."
            },
            {
                "start": 12.0,
                "end": 17.0,
                "english": "People can't do something themselves, they want to tell you you can't do it.",
                "idiom": "tell you you can't do it",
                "idiom_explanation": "மற்றவர்களால் முடியாததை, உன்னாலும் முடியாது என்று சொல்லி உன்னை முடக்க நினைப்பார்கள்."
            },
            {
                "start": 17.0,
                "end": 21.0,
                "english": "If you want something, go get it. Period.",
                "idiom": "Period",
                "idiom_explanation": "Period என்றால் 'அவ்வளவுதான், வேறு பேச்சே இல்லை (இறுதி முடிவு)' என்று பொருள்."
            }
        ]
    },
    {
        "id": "interstellar",
        "title": "Interstellar",
        "scene_name": "The Dimension of Love",
        "genre": "Sci-Fi / Space",
        "speaker": "Dr. Amelia Brand (Anne Hathaway)",
        "poster_emoji": "🪐",
        "bg_gradient": "linear-gradient(135deg, #09203f 0%, #537895 100%)",
        "description": "Astronauts debating love and physics across black holes and wormholes in outer space.",
        "cultural_notes": "Concepts of multi-dimensional space (பரிமாணங்கள்) simplified for non-English speakers.",
        "dialogues": [
            {
                "start": 0.0,
                "end": 4.5,
                "english": "Love isn't something we invented. It's observable, powerful.",
                "idiom": "observable, powerful",
                "idiom_explanation": "அன்பு என்பது மனிதர்கள் கண்டுபிடித்தது அல்ல; அது இயற்கையிலேயே உணரக்கூடிய மகத்தான சக்தி."
            },
            {
                "start": 4.5,
                "end": 9.0,
                "english": "It has to mean something.",
                "idiom": "mean something",
                "idiom_explanation": "இதற்குப் பின்னால் நிச்சயம் ஒரு ஆழ்ந்த அர்த்தம் இருக்க வேண்டும்."
            },
            {
                "start": 9.0,
                "end": 16.0,
                "english": "Love is the one thing we're capable of perceiving that transcends dimensions of time and space.",
                "idiom": "transcends dimensions",
                "idiom_explanation": "காலம், விண்வெளி தூரம் என்ற எந்த எல்லைகளையும் தாண்டிப் பாயும் ஒரே உணர்வு அன்பு மட்டுமே."
            },
            {
                "start": 16.0,
                "end": 21.0,
                "english": "Maybe we should trust that, even if we can't understand it yet.",
                "idiom": "trust that",
                "idiom_explanation": "அறிவியலால் முழுமையாக விளக்க முடியாவிட்டாலும், அன்பின் வழிகாட்டலை நாம் நம்ப வேண்டும்."
            }
        ]
    },
    {
        "id": "oppenheimer",
        "title": "Oppenheimer",
        "scene_name": "The Destroyer of Worlds",
        "genre": "Historical / Biography",
        "speaker": "J. Robert Oppenheimer (Cillian Murphy)",
        "poster_emoji": "⚛️",
        "bg_gradient": "linear-gradient(135deg, #2b0000 0%, #551414 100%)",
        "description": "The fateful moment the first atomic bomb test shakes the world.",
        "cultural_notes": "Oppenheimer quotes the Hindu sacred text Bhagavad Gita in Sanskrit ('कालोऽस्मि लोकक्षयकृत्प्रवृद्धो').",
        "dialogues": [
            {
                "start": 0.0,
                "end": 4.5,
                "english": "We knew the world would not be the same.",
                "idiom": "not be the same",
                "idiom_explanation": "இந்த வரலாற்று தருணத்திற்குப் பிறகு இந்த உலகம் பழைய நிலைக்குத் திரும்பப் போவதில்லை."
            },
            {
                "start": 4.5,
                "end": 9.5,
                "english": "A few people laughed, a few people cried, most people were silent.",
                "idiom": "most people were silent",
                "idiom_explanation": "அணுவின் பேரழிவை உணர்ந்து பெரும்பான்மையான மக்கள் அதிர்ச்சியில் உறைந்து மௌனமாயினர்."
            },
            {
                "start": 9.5,
                "end": 16.0,
                "english": "Now I am become Death, the destroyer of worlds.",
                "idiom": "destroyer of worlds",
                "idiom_explanation": "'இப்போது நான் உலகங்களை அழிக்கும் காலன் (மரண தேவன்) ஆகிவிட்டேன்' - பகவத் கீதையின் 11-வது அத்தியாய வாசகம்."
            }
        ]
    },
    {
        "id": "planet_earth",
        "title": "BBC Planet Earth",
        "scene_name": "The Living Web of Earth",
        "genre": "Nature / Wildlife Documentary",
        "speaker": "Sir David Attenborough",
        "poster_emoji": "🌿",
        "bg_gradient": "linear-gradient(135deg, #134e5e 0%, #71b280 100%)",
        "description": "A breathtaking cinematic exploration of the interconnected ecosystems of our living planet.",
        "cultural_notes": "Documentaries use high English vocabulary like 'fragile web' and 'paradise'.",
        "dialogues": [
            {
                "start": 0.0,
                "end": 4.5,
                "english": "Our planet is still full of wonders.",
                "idiom": "full of wonders",
                "idiom_explanation": "நம் பூமி இன்னும் எண்ணற்ற வியப்புகளும் அதிசயங்களும் நிறைந்தது."
            },
            {
                "start": 4.5,
                "end": 9.5,
                "english": "Every creature here is linked in a delicate web of life.",
                "idiom": "delicate web of life",
                "idiom_explanation": "பூமியில் உள்ள சிறு எறும்பு முதல் மனிதன் வரை அனைத்து உயிரினங்களும் ஒன்றோடொன்று பிணைக்கப்பட்ட உயிர்ச்சங்கிலி."
            },
            {
                "start": 9.5,
                "end": 16.0,
                "english": "Water and sunlight have crafted a paradise across billions of years.",
                "idiom": "crafted a paradise",
                "idiom_explanation": "கோடிக்கணக்கான ஆண்டுகளாக சூரிய ஒளியும் நீரும் இணைந்து இந்த பூமியை ஒரு சொர்க்கமாக மாற்றியுள்ளன."
            }
        ]
    }
]

def get_cinema_scenes():
    """Returns metadata for all available curated movie scenes."""
    return [
        {
            "id": s["id"],
            "title": s["title"],
            "scene_name": s["scene_name"],
            "genre": s["genre"],
            "speaker": s["speaker"],
            "poster_emoji": s["poster_emoji"],
            "bg_gradient": s["bg_gradient"],
            "description": s["description"],
            "cultural_notes": s["cultural_notes"],
            "dialogue_count": len(s["dialogues"])
        }
        for s in CINEMA_SCENES
    ]

def translate_scene(scene_id, target="Tamil"):
    """
    Translates all dialogues of a movie scene into the chosen vernacular language
    and generates cultural & idiom breakdowns.
    """
    scene = next((s for s in CINEMA_SCENES if s["id"] == scene_id), None)
    if not scene:
        return None

    translated_dialogues = []

    for d in scene["dialogues"]:
        vernacular_text = translate_text(d["english"], source="English", target=target)
        translated_dialogues.append({
            "start": d["start"],
            "end": d["end"],
            "english": d["english"],
            "vernacular": vernacular_text,
            "idiom": d.get("idiom", ""),
            "idiom_explanation": d.get("idiom_explanation", "")
        })

    return {
        "scene_id": scene["id"],
        "title": scene["title"],
        "scene_name": scene["scene_name"],
        "speaker": scene["speaker"],
        "poster_emoji": scene["poster_emoji"],
        "target_language": target,
        "cultural_notes": scene["cultural_notes"],
        "dialogues": translated_dialogues
    }

def format_timestamp_srt(seconds):
    """Converts seconds float into standard SRT timestamp 00:00:00,000"""
    hrs = int(seconds // 3600)
    mins = int((seconds % 3600) // 60)
    secs = int(seconds % 60)
    millis = int(round((seconds - int(seconds)) * 1000))
    return f"{hrs:02d}:{mins:02d}:{secs:02d},{millis:03d}"

def generate_srt_file(scene_data, include_bilingual=True):
    """
    Generates standard .srt subtitle file content in vernacular language.
    """
    dialogues = scene_data.get("dialogues", [])
    srt_lines = []
    
    for i, d in enumerate(dialogues, 1):
        start_ts = format_timestamp_srt(d["start"])
        end_ts = format_timestamp_srt(d["end"])
        srt_lines.append(str(i))
        srt_lines.append(f"{start_ts} --> {end_ts}")
        if include_bilingual:
            srt_lines.append(d.get("vernacular", ""))
            srt_lines.append(f"({d.get('english', '')})")
        else:
            srt_lines.append(d.get("vernacular", ""))
        srt_lines.append("")  # Empty separator line

    return "\n".join(srt_lines)
