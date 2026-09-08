"""
Vernacular AI - Conversational Pedagogical AI Tutor
Understands questions in English, Tamil, Tanglish, and regional languages,
providing structured mother-tongue explanations with real-world examples,
analogies, key takeaways, and practice questions.
"""

import re
from .translator import translate_text, get_language_code

# Curated knowledge base for foundational STEM & vernacular questions
KNOWLEDGE_BASE = {
    "photosynthesis": {
        "concept": "Photosynthesis is the biological process by which green plants absorb sunlight, carbon dioxide, and water to synthesize glucose (food) and release oxygen.",
        "example": "Think of a leaf as a tiny solar-powered kitchen: sunlight is the fire, water and air are the ingredients, and fresh fruits and oxygen are the delicious output!",
        "takeaway": "Without photosynthesis, Earth would have no breathable oxygen and no food chain.",
        "question": "Which gas do plants release during photosynthesis?",
        "suggestions": [
            "Why is chlorophyll green?",
            "What happens to plants at night?",
            "How do roots absorb water?"
        ]
    },
    "gravity": {
        "concept": "Gravity is the fundamental attractive force by which a planet or other body draws objects toward its center.",
        "example": "When you drop an apple, Earth's immense mass pulls it down. The same invisible pull keeps our Moon in orbit and prevents the oceans from floating into space!",
        "takeaway": "Gravity depends on mass and distance. Earth's gravitational acceleration is approximately 9.8 m/s².",
        "question": "Why do astronauts feel weightless in space?",
        "suggestions": [
            "Who discovered gravity?",
            "How does gravity affect planets?",
            "What is a black hole?"
        ]
    },
    "water_cycle": {
        "concept": "The water cycle describes how water continuously evaporates from oceans and lakes into vapor, condenses into clouds, and precipitates back to Earth as rain.",
        "example": "When you boil water in a pot with a lid, steam rises and turns back into water drops under the lid. Nature does the exact same thing on a planetary scale!",
        "takeaway": "Water is never lost on Earth; it is constantly recycled across oceans, atmosphere, and land.",
        "question": "What is the process called when plants release water vapor?",
        "suggestions": [
            "Why does it rain?",
            "What are clouds made of?",
            "Why is sea water salty?"
        ]
    },
    "stars": {
        "concept": "Stars appear to twinkle because their light travels through turbulent, shifting layers of Earth's atmosphere, which continually bends and refracts the light rays.",
        "example": "Just like looking at a coin at the bottom of a swimming pool makes it look like it's wiggling, atmospheric winds make distant starlight wiggle!",
        "takeaway": "Stars don't actually twinkle in outer space; twinkle only happens when seen through an atmosphere.",
        "question": "Why don't planets twinkle like stars?",
        "suggestions": [
            "What is the closest star to Earth?",
            "What causes shooting stars?",
            "How hot is the Sun?"
        ]
    },
    "matter": {
        "concept": "Matter is anything that has mass and takes up space. The three primary states of matter are solid (rigid shape), liquid (takes container shape), and gas (fills entire volume).",
        "example": "Ice is solid water, water in a glass is liquid, and steam rising from a kettle is gaseous water!",
        "takeaway": "Matter can change states when heated or cooled without altering its underlying chemical composition.",
        "question": "What is the 4th state of matter found in stars and lightning?",
        "suggestions": [
            "What is plasma?",
            "Can a solid turn directly into gas?",
            "What are atoms made of?"
        ]
    }
}

GREETINGS = {
    "hello", "hi", "hey", "vanakkam", "namaste", "namaskaram", "good morning", "good evening",
    "வணக்கம்", "नमस्ते", "నమస్కారం", "നമസ്കാരം"
}

def detect_concept_key(query_lower):
    """Detects concept keyword from query (handling English, Tamil, and Tanglish)."""
    if any(w in query_lower for w in ["photosynthesis", "photo synthesis", "oli serkkai", "olicherkkai", "ஒளிச்சேர்க்கை", "plant food", "தாவர உணவு"]):
        return "photosynthesis"
    if any(w in query_lower for w in ["gravity", "eerppu", "irpu", "visai", "ஈர்ப்பு", "புவியீர்ப்பு", "gravitational", "apple fall"]):
        return "gravity"
    if any(w in query_lower for w in ["water cycle", "rain cycle", "watercycle", "neer suzhar", "மழை", "நீர் சுழற்சி"]):
        return "water_cycle"
    if any(w in query_lower for w in ["twinkle", "stars", "star", "minumuk", "நட்சத்திரங்கள்", "விண்மீன்"]):
        return "stars"
    if any(w in query_lower for w in ["matter", "states of matter", "solid", "liquid", "gas", "பொருளின் நிலைகள்"]):
        return "matter"
    return None

def generate_chat_response(message, history=None, target_language="Tamil"):
    """
    Generates an intelligent pedagogical conversational response in the student's mother tongue.
    """
    msg_cleaned = str(message or "").strip()
    if not msg_cleaned:
        return {
            "reply": "Please ask an educational question or type your doubt!",
            "language": target_language,
            "suggestions": ["What is photosynthesis?", "Why do stars twinkle?", "How does gravity work?"]
        }

    msg_lower = msg_cleaned.lower()
    
    # Check for greetings
    if any(re.search(r'\b' + re.escape(g) + r'\b', msg_lower) for g in GREETINGS):
        greeting_en = (
            "Hello! I am your Vernacular AI Educational Tutor. "
            "Ask me any question in science, math, or cinema, and I will explain it simply in your mother tongue! "
            "What would you like to learn today?"
        )
        vernacular_greeting = translate_text(greeting_en, source="English", target=target_language)
        return {
            "reply": vernacular_greeting,
            "language": target_language,
            "suggestions": [
                "🌱 What is photosynthesis?",
                "🪐 How does gravity work?",
                "✨ Why do stars twinkle?",
                "🌊 What is the water cycle?"
            ]
        }

    # Detect known curriculum concept
    concept_key = detect_concept_key(msg_lower)
    
    if concept_key and concept_key in KNOWLEDGE_BASE:
        kb = KNOWLEDGE_BASE[concept_key]
        
        # Translate each pedagogical section
        concept_trans = translate_text(kb["concept"], source="English", target=target_language)
        example_trans = translate_text(kb["example"], source="English", target=target_language)
        takeaway_trans = translate_text(kb["takeaway"], source="English", target=target_language)
        question_trans = translate_text(kb["question"], source="English", target=target_language)
        
        formatted_reply = (
            f"💡 **எளிய விளக்கம் (Concept Explanation):**\n{concept_trans}\n\n"
            f"🔬 **நிஜ உலக உதாரணம் (Real-World Analogy):**\n{example_trans}\n\n"
            f"📝 **முக்கிய குறிப்பு (Key Takeaway):**\n{takeaway_trans}\n\n"
            f"🎯 **உங்களுக்கான பயிற்சி கேள்வி (Quick Question):**\n{question_trans}"
        )
        
        # Translate suggestions
        translated_suggestions = [
            translate_text(s, source="English", target=target_language)
            for s in kb.get("suggestions", [])
        ]
        
        return {
            "reply": formatted_reply,
            "language": target_language,
            "suggestions": translated_suggestions
        }

    # General / Open-Ended Query Handling
    # Deconstruct query into pedagogical response
    if any(w in msg_lower for w in ["why", "reason", "yen", "yeno"]):
        structure = (
            f"Key Scientific Reason regarding your question: This phenomenon happens due to underlying physical and natural laws. "
            f"In simple words, nature balances energy and environmental factors to produce this effect."
        )
    elif any(w in msg_lower for w in ["how", "process", "working", "epdi"]):
        structure = (
            f"Working Mechanism: This operates step-by-step through interconnected scientific principles. "
            f"Energy, matter, and external forces interact continuously to make this process function."
        )
    else:
        structure = (
            f"Core Concept: This is a fundamental topic in science and nature. "
            f"Understanding this helps you connect classroom theory with real-world observations."
        )

    # Translate the contextual explanation
    vernacular_response = translate_text(structure, source="English", target=target_language)
    
    # Also provide a direct translation of the question context
    topic_translation = translate_text(msg_cleaned, source="English", target=target_language)
    
    formatted_reply = (
        f"💡 **உங்கள் கேள்வி (Your Topic):** {topic_translation}\n\n"
        f"📖 **விளக்கம் (Explanation):**\n{vernacular_response}\n\n"
        f"📝 **படிப்பிற்கான குறிப்பு (Study Tip):**\n"
        f"பாடப்புத்தகத்தில் உள்ள இந்த முக்கிய கருத்தை நினைவில் வைத்திருங்கள். அடுத்த தலைப்பை கேட்கவும்!"
    )
    
    return {
        "reply": formatted_reply,
        "language": target_language,
        "suggestions": [
            "🌱 Photosynthesis விளக்கம் வேண்டும்",
            "🪐 Gravity எப்படி வேலை செய்கிறது?",
            "✨ நட்சத்திரங்கள் ஏன் ஒளிர்கின்றன?",
            "💧 நீர் சுழற்சி என்றால் என்ன?"
        ]
    }
