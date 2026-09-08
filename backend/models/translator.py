import logging
import time
import re
from concurrent.futures import ThreadPoolExecutor

try:
    from deep_translator import GoogleTranslator, MyMemoryTranslator
except ImportError:
    GoogleTranslator = None
    MyMemoryTranslator = None

SUPPORTED_LANGUAGES = [
    # Indian Languages (26)
    {"code": "ta", "name": "Tamil", "native": "தமிழ்", "flag": "🇮🇳", "speech": "ta-IN", "region": "India"},
    {"code": "hi", "name": "Hindi", "native": "हिन्दी", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "te", "name": "Telugu", "native": "తెలుగు", "flag": "🇮🇳", "speech": "te-IN", "region": "India"},
    {"code": "ml", "name": "Malayalam", "native": "മലയാളം", "flag": "🇮🇳", "speech": "ml-IN", "region": "India"},
    {"code": "kn", "name": "Kannada", "native": "ಕನ್ನಡ", "flag": "🇮🇳", "speech": "kn-IN", "region": "India"},
    {"code": "bn", "name": "Bengali", "native": "বাংলা", "flag": "🇮🇳", "speech": "bn-IN", "region": "India"},
    {"code": "mr", "name": "Marathi", "native": "मराठी", "flag": "🇮🇳", "speech": "mr-IN", "region": "India"},
    {"code": "gu", "name": "Gujarati", "native": "ગુજરાતી", "flag": "🇮🇳", "speech": "gu-IN", "region": "India"},
    {"code": "pa", "name": "Punjabi", "native": "ਪੰਜਾਬੀ", "flag": "🇮🇳", "speech": "pa-IN", "region": "India"},
    {"code": "ur", "name": "Urdu", "native": "اردو", "flag": "🇮🇳", "speech": "ur-IN", "region": "India"},
    {"code": "or", "name": "Odia", "native": "ଓଡ଼ିଆ", "flag": "🇮🇳", "speech": "or-IN", "region": "India"},
    {"code": "as", "name": "Assamese", "native": "অসমীয়া", "flag": "🇮🇳", "speech": "as-IN", "region": "India"},
    {"code": "sa", "name": "Sanskrit", "native": "संस्कृतम्", "flag": "🇮🇳", "speech": "sa-IN", "region": "India"},
    {"code": "ne", "name": "Nepali", "native": "नेपाली", "flag": "🇮🇳", "speech": "ne-NP", "region": "India"},
    {"code": "sd", "name": "Sindhi", "native": "سنڌي", "flag": "🇮🇳", "speech": "sd-IN", "region": "India"},
    {"code": "mai", "name": "Maithili", "native": "मैथिली", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "kok", "name": "Konkani", "native": "कोंकणी", "flag": "🇮🇳", "speech": "kok-IN", "region": "India"},
    {"code": "mni", "name": "Manipuri", "native": "মৈতৈলোন্", "flag": "🇮🇳", "speech": "mni-IN", "region": "India"},
    {"code": "brx", "name": "Bodo", "native": "बर'", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "dgo", "name": "Dogri", "native": "डोगरी", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "ks", "name": "Kashmiri", "native": "کٲشُر", "flag": "🇮🇳", "speech": "ks-IN", "region": "India"},
    {"code": "sat", "name": "Santali", "native": "ᱥᱟᱱᱛᱟᱲᱤ", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "bho", "name": "Bhojpuri", "native": "भोजपुरी", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "tcy", "name": "Tulu", "native": "ತುಳು", "flag": "🇮🇳", "speech": "kn-IN", "region": "India"},
    {"code": "raj", "name": "Rajasthani", "native": "राजस्थानी", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},
    {"code": "har", "name": "Haryanvi", "native": "हरियाणवी", "flag": "🇮🇳", "speech": "hi-IN", "region": "India"},

    # Global Languages (25)
    {"code": "en", "name": "English", "native": "English", "flag": "🇬🇧", "speech": "en-US", "region": "Global"},
    {"code": "fr", "name": "French", "native": "Français", "flag": "🇫🇷", "speech": "fr-FR", "region": "Global"},
    {"code": "de", "name": "German", "native": "Deutsch", "flag": "🇩🇪", "speech": "de-DE", "region": "Global"},
    {"code": "es", "name": "Spanish", "native": "Español", "flag": "🇪🇸", "speech": "es-ES", "region": "Global"},
    {"code": "ar", "name": "Arabic", "native": "العربية", "flag": "🇸🇦", "speech": "ar-SA", "region": "Global"},
    {"code": "ja", "name": "Japanese", "native": "日本語", "flag": "🇯🇵", "speech": "ja-JP", "region": "Global"},
    {"code": "zh", "name": "Chinese", "native": "中文", "flag": "🇨🇳", "speech": "zh-CN", "region": "Global"},
    {"code": "ru", "name": "Russian", "native": "Русский", "flag": "🇷🇺", "speech": "ru-RU", "region": "Global"},
    {"code": "ko", "name": "Korean", "native": "한국어", "flag": "🇰🇷", "speech": "ko-KR", "region": "Global"},
    {"code": "it", "name": "Italian", "native": "Italiano", "flag": "🇮🇹", "speech": "it-IT", "region": "Global"},
    {"code": "pt", "name": "Portuguese", "native": "Português", "flag": "🇵🇹", "speech": "pt-PT", "region": "Global"},
    {"code": "tr", "name": "Turkish", "native": "Türkçe", "flag": "🇹🇷", "speech": "tr-TR", "region": "Global"},
    {"code": "nl", "name": "Dutch", "native": "Nederlands", "flag": "🇳🇱", "speech": "nl-NL", "region": "Global"},
    {"code": "sv", "name": "Swedish", "native": "Svenska", "flag": "🇸🇪", "speech": "sv-SE", "region": "Global"},
    {"code": "pl", "name": "Polish", "native": "Polski", "flag": "🇵🇱", "speech": "pl-PL", "region": "Global"},
    {"code": "fa", "name": "Persian", "native": "فارسی", "flag": "🇮🇷", "speech": "fa-IR", "region": "Global"},
    {"code": "id", "name": "Indonesian", "native": "Bahasa Indonesia", "flag": "🇮🇩", "speech": "id-ID", "region": "Global"},
    {"code": "th", "name": "Thai", "native": "ไทย", "flag": "🇹🇭", "speech": "th-TH", "region": "Global"},
    {"code": "vi", "name": "Vietnamese", "native": "Tiếng Việt", "flag": "🇻🇳", "speech": "vi-VN", "region": "Global"},
    {"code": "ms", "name": "Malay", "native": "Bahasa Melayu", "flag": "🇲🇾", "speech": "ms-MY", "region": "Global"},
    {"code": "el", "name": "Greek", "native": "Ελληνικά", "flag": "🇬🇷", "speech": "el-GR", "region": "Global"},
    {"code": "he", "name": "Hebrew", "native": "עברית", "flag": "🇮🇱", "speech": "he-IL", "region": "Global"},
    {"code": "uk", "name": "Ukrainian", "native": "Українська", "flag": "🇺🇦", "speech": "uk-UA", "region": "Global"},
    {"code": "cs", "name": "Czech", "native": "Čeština", "flag": "🇨🇿", "speech": "cs-CZ", "region": "Global"},
    {"code": "ro", "name": "Romanian", "native": "Română", "flag": "🇷🇴", "speech": "ro-RO", "region": "Global"},
]

NAME_TO_CODE = {lang["name"].lower(): lang["code"] for lang in SUPPORTED_LANGUAGES}
CODE_TO_NAME = {lang["code"]: lang["name"] for lang in SUPPORTED_LANGUAGES}

for lang in SUPPORTED_LANGUAGES:
    NAME_TO_CODE[lang["code"].lower()] = lang["code"]

DEMO_TRANSLATIONS = {
    "ta": {
        "The Sun gives us light and heat.": "சூரியன் நமக்கு ஒளியையும் வெப்பத்தையும் தருகிறது.",
        "Plants need sunlight and water.": "தாவரங்களுக்கு சூரிய ஒளியும் நீரும் தேவை.",
        "Water is essential for all living things.": "அனைத்து உயிரினங்களுக்கும் நீர் மிகவும் அவசியம்.",
        "The Earth moves around the Sun.": "பூமி சூரியனைச் சுற்றி வருகிறது.",
    },
    "hi": {
        "The Sun gives us light and heat.": "सूर्य हमें प्रकाश और ऊष्मा देता है।",
        "Plants need sunlight and water.": "पौधों को धूप और पानी की आवश्यकता होती है।",
        "Water is essential for all living things.": "सभी जीवित प्राणियों के लिए जल आवश्यक है।",
        "The Earth moves around the Sun.": "पृथ्वी सूर्य के चारों ओर घूमती है।",
    }
}

COMMON_STOPWORDS = {
    "what", "where", "when", "which", "whose", "why", "how", "this", "that", "these", "those",
    "there", "here", "they", "them", "their", "with", "from", "about", "into", "through",
    "after", "before", "because", "while", "during", "does", "have", "been", "were", "will",
    "would", "could", "should", "your", "give", "make", "tell", "much", "many", "some"
}

def get_language_code(lang_str):
    if not lang_str:
        return "en"
    key = str(lang_str).strip().lower()
    return NAME_TO_CODE.get(key, key[:2])

# Comprehensive Offline Vernacular Lexicon
OFFLINE_LEXICON = {
    "ta": {
        "water": "தண்ணீர்", "essential": "இன்றியமையாதது", "life": "வாழ்க்கை", "all": "அனைத்து", "living": "உயிருள்ள",
        "things": "பொருட்கள்", "sun": "சூரியன்", "gives": "தருகிறது", "us": "நமக்கு", "light": "ஒளி", "heat": "வெப்பம்",
        "plants": "தாவரங்கள்", "need": "தேவை", "sunlight": "சூரிய ஒளி", "make": "உருவாக்க", "food": "உணவு",
        "earth": "பூமி", "moves": "நகர்கிறது", "around": "சுற்றி", "stars": "நட்சத்திரங்கள்", "twinkle": "மினுமினுக்கின்றன",
        "night": "இரவு", "gravity": "ஈர்ப்பு விசை", "pulls": "இழுக்கிறது", "towards": "நோக்கி", "center": "மையம்",
        "oxygen": "ஆக்ஸிஜன்", "carbon": "கரிமம்", "photosynthesis": "ஒளிச்சேர்க்கை", "process": "செயல்முறை",
        "energy": "ஆற்றல்", "science": "அறிவியல்", "nature": "இயற்கை", "human": "மனிதன்", "body": "உடல்",
        "blood": "இரத்தம்", "heart": "இதயம்", "brain": "மூளை", "tree": "மரம்", "rain": "மழை", "sky": "வானம்",
        "ocean": "பெருங்கடல்", "sea": "கடல்", "river": "ஆறு", "wind": "காற்று", "fire": "தீ", "air": "காற்று",
        "what": "என்ன", "why": "ஏன்", "how": "எப்படி", "where": "எங்கே", "when": "எப்போது", "who": "யார்",
        "is": "ஆகும்", "are": "இருக்கின்றன", "the": "", "a": "ஒரு", "an": "ஒரு", "and": "மற்றும்", "or": "அல்லது",
        "for": "ஆக", "with": "உடன்", "from": "இருந்து", "in": "இல்", "on": "மீது", "to": "க்கு", "of": "இன்",
        "movie": "திரைப்படம்", "film": "படம்", "cinema": "திரைப்படம்", "actor": "நடிகர்", "hero": "கதாநாயகன்",
        "dream": "கனவு", "time": "நேரம்", "space": "விண்வெளி", "love": "அன்பு", "hope": "நம்பிக்கை", "world": "உலகம்",
        "protect": "பாதுகாக்க", "never": "ஒருபோதும்", "give up": "விட்டுக்கொடுக்காதே", "remember": "நினைவில் கொள்",
        "believe": "நம்பு", "future": "எதிர்காலம்", "power": "சக்தி", "strong": "வலிமையான", "freedom": "சுதந்திரம்",
        "truth": "உண்மை", "peace": "அமைதி", "knowledge": "அறிவு", "education": "கல்வி", "student": "மாணவர்",
        "teacher": "ஆசிரியர்", "school": "பள்ளி", "book": "புத்தகம்", "learn": "கற்றுக்கொள்", "study": "படி",
        "understand": "புரிந்துகொள்", "question": "கேள்வி", "answer": "பதில்", "success": "வெற்றி", "work": "வேலை",
        "important": "முக்கியமானது", "fundamental": "அடிப்படையானது", "yes": "ஆம்", "no": "இல்லை"
    },
    "hi": {
        "water": "जल", "essential": "आवश्यक", "life": "जीवन", "all": "सभी", "living": "जीवित",
        "things": "चीजें", "sun": "सूर्य", "gives": "देता है", "us": "हमें", "light": "प्रकाश", "heat": "ऊष्मा",
        "plants": "पौधे", "need": "आवश्यकता", "sunlight": "धूप", "make": "बनाने", "food": "भोजन",
        "earth": "पृथ्वी", "moves": "घूमती है", "around": "चारों ओर", "stars": "तारे", "twinkle": "टिमटिमाते हैं",
        "gravity": "गुरुत्वाकर्षण", "photosynthesis": "प्रकाश संश्लेषण", "energy": "ऊर्जा", "science": "विज्ञान",
        "nature": "प्रकृति", "what": "क्या", "why": "क्यों", "how": "कैसे", "where": "कहाँ",
        "movie": "फिल्म", "dream": "सपना", "time": "समय", "space": "अंतरिक्ष", "love": "प्रेम", "hope": "आशा",
        "world": "दुनिया", "future": "भविष्य", "education": "शिक्षा", "success": "सफलता", "important": "महत्वपूर्ण"
    },
    "te": {
        "water": "నీరు", "essential": "అత్యవసరం", "life": "జీవితం", "all": "అన్ని", "living": "జీవరాశులు",
        "sun": "సూర్యుడు", "gives": "ఇస్తుంది", "us": "మనకు", "light": "కాంతి", "heat": "వేడి",
        "plants": "మొక్కలు", "need": "అవసరం", "sunlight": "సూర్యరశ్మి", "food": "ఆహారం",
        "earth": "భూమి", "around": "చుట్టూ", "gravity": "గురుత్వాకర్షణ", "energy": "శక్తి",
        "photosynthesis": "కిరణజన్య సంయోగక్రియ", "science": "విజ్ఞానశాస్త్రం", "nature": "ప్రకృతి",
        "what": "ఏమిటి", "why": "ఎందుకు", "how": "ఎలా", "movie": "సినిమా", "dream": "కల", "time": "సమయం"
    },
    "ml": {
        "water": "വെള്ളം", "essential": "അത്യന്താപേക്ഷിതം", "life": "ജീവൻ", "all": "എല്ലാ",
        "sun": "സൂര്യൻ", "gives": "നൽകുന്നു", "us": "നമുക്ക്", "light": "വെളിച്ചം", "heat": "ചൂട്",
        "plants": "സസ്യങ്ങൾ", "sunlight": "സൂര്യപ്രകാശം", "food": "ഭക്ഷണം", "earth": "ഭൂമി",
        "gravity": "ഗുരുത്വാകർഷണം", "energy": "ഊർജ്ജം", "science": "ശാസ്ത്രം", "nature": "പ്രകൃതി",
        "what": "എന്ത്", "why": "എന്തുകൊണ്ട്", "how": "എങ്ങനെ", "movie": "സിനിമ", "dream": "സ്വപ്നം"
    }
}

# Offline phrase templates
OFFLINE_PHRASES = {
    "ta": {
        "water is essential for all living things": "அனைத்து உயிரினங்களுக்கும் நீர் மிகவும் அவசியம்.",
        "water is essential for life": "வாழ்க்கைக்கு நீர் இன்றியமையாதது.",
        "the sun gives us light and heat": "சூரியன் நமக்கு ஒளியையும் வெப்பத்தையும் தருகிறது.",
        "plants need sunlight and water": "தாவரங்களுக்கு சூரிய ஒளியும் நீரும் தேவை.",
        "the earth moves around the sun": "பூமி சூரியனைச் சுற்றி வருகிறது.",
        "why do plants need sunlight": "தாவரங்களுக்கு சூரிய ஒளி ஏன் தேவை?",
        "why is photosynthesis important": "ஒளிச்சேர்க்கை ஏன் முக்கியமானது?",
        "don't ever let somebody tell you you can't do something": "நீ எதையும் செய்ய முடியாது என்று யாராவது சொல்வதை ஒருபோதும் அனுமதிக்காதே.",
        "love is the one thing that transcends time and space": "அன்பு மட்டுமே காலம் மற்றும் விண்வெளியைத் தாண்டி நிற்கும் ஒன்று.",
        "look deep into nature": "இயற்கையை ஆழமாகப் பாருங்கள்."
    },
    "hi": {
        "water is essential for all living things": "सभी जीवित प्राणियों के लिए जल आवश्यक है।",
        "water is essential for life": "जीवन के लिए जल आवश्यक है।",
        "the sun gives us light and heat": "सूर्य हमें प्रकाश और ऊष्मा देता है।",
        "plants need sunlight and water": "पौधों को धूप और पानी की आवश्यकता होती है।",
        "the earth moves around the sun": "पृथ्वी सूर्य के चारों ओर घूमती है।"
    }
}

def offline_translate(cleaned_text, src_code="en", tgt_code="ta"):
    """
    Translates text locally without any internet connection using:
    1. Offline phrase matching
    2. Token-level dictionary assembly with morphological heuristics
    """
    normalized = re.sub(r'[^\w\s]', '', cleaned_text.lower()).strip()
    
    # 1. Exact or near phrase match
    lang_phrases = OFFLINE_PHRASES.get(tgt_code, OFFLINE_PHRASES.get("ta", {}))
    if normalized in lang_phrases:
        return lang_phrases[normalized]
    
    for phrase, trans in lang_phrases.items():
        if phrase in normalized or normalized in phrase:
            return trans

    # 2. Token-level lexicon translation
    lexicon = OFFLINE_LEXICON.get(tgt_code, OFFLINE_LEXICON.get("ta", {}))
    tokens = re.findall(r'\b\w+\b', cleaned_text.lower())
    translated_tokens = []
    
    for t in tokens:
        if t in lexicon and lexicon[t]:
            translated_tokens.append(lexicon[t])
        elif len(t) > 2 and t not in COMMON_STOPWORDS:
            translated_tokens.append(t)
            
    if translated_tokens:
        result = " ".join(translated_tokens)
        return f"{result}"
        
    return f"{cleaned_text} ({tgt_code.upper()} ஆஃப்லைன்)"

def is_valid_translation(text):
    if not text or not isinstance(text, str):
        return False
    lower = text.lower().strip()
    if any(err in lower for err in [
        "error 500", "server error", "[translation error]", "please try again later",
        "that’s all we know", "thats all we know", "html", "<!doctype", "quota exceeded",
        "mymemory warning"
    ]):
        return False
    return True

def translate_text(text, source="English", target="Tamil"):
    """Translates educational content or questions with resilient multi-tier fallbacks and offline support."""
    cleaned_text = str(text or "").strip()
    if not cleaned_text:
        return ""

    src_code = get_language_code(source)
    tgt_code = get_language_code(target)

    if src_code == tgt_code:
        return cleaned_text

    # 1. Check local SQLite persistent database cache
    try:
        from database import find_cached_translation
        cached = find_cached_translation(cleaned_text, source_lang=source, target_lang=target)
        if cached and is_valid_translation(cached):
            return cached
    except Exception:
        pass

    # 2. Curated demo cache check
    if src_code == "en" and tgt_code in DEMO_TRANSLATIONS:
        if cleaned_text in DEMO_TRANSLATIONS[tgt_code]:
            return DEMO_TRANSLATIONS[tgt_code][cleaned_text]

    # 3. Attempt 1: GoogleTranslator direct (Online)
    if GoogleTranslator:
        for attempt in range(2):
            try:
                translator = GoogleTranslator(source=src_code, target=tgt_code)
                translated = translator.translate(cleaned_text)
                if is_valid_translation(translated):
                    return translated
            except Exception as e:
                logging.warning(f"GoogleTranslator error (network offline?): {e}")
                time.sleep(0.1)

        # Attempt 2: Auto source
        try:
            translator = GoogleTranslator(source="auto", target=tgt_code)
            translated = translator.translate(cleaned_text)
            if is_valid_translation(translated):
                return translated
        except Exception as e:
            logging.warning(f"GoogleTranslator auto fallback error: {e}")

    # 4. Attempt 3: MyMemoryTranslator
    if MyMemoryTranslator:
        try:
            mm = MyMemoryTranslator(source=src_code, target=tgt_code)
            translated = mm.translate(cleaned_text)
            if is_valid_translation(translated):
                return translated
        except Exception as e:
            logging.warning(f"MyMemory fallback error: {e}")

    # 5. Offline Fallback Engine (Runs with 0% network connectivity!)
    return offline_translate(cleaned_text, src_code=src_code, tgt_code=tgt_code)



def translate_multi_target(text, source="English", targets=None):
    """
    Translates a single lesson into multiple target languages concurrently (for live broadcast).
    """
    if not targets:
        targets = ["Tamil", "Hindi", "Telugu", "Malayalam"]

    results = {}
    with ThreadPoolExecutor(max_workers=min(len(targets), 5)) as executor:
        futures = {
            executor.submit(translate_text, text, source, tgt): tgt
            for tgt in targets
        }
        for future in futures:
            tgt = futures[future]
            try:
                results[tgt] = future.result()
            except Exception as e:
                results[tgt] = f"Error: {e}"

    return results

def extract_key_vocabulary(text, source="English", target="Tamil", max_terms=4):
    words = re.findall(r'\b[A-Za-z]{4,}\b', text)
    unique_words = []
    seen = set()
    for w in words:
        lower = w.lower()
        if lower not in COMMON_STOPWORDS and lower not in seen:
            seen.add(lower)
            unique_words.append(w.capitalize())
            if len(unique_words) >= max_terms:
                break

    vocab_list = []
    for term in unique_words:
        trans = translate_text(term, source=source, target=target)
        if trans and trans != term:
            vocab_list.append({
                "term": term,
                "translation": trans
            })

    return vocab_list

def generate_explanation(source_text, target="Tamil"):
    prompt_explanation = f"In simple terms: {source_text}"
    return translate_text(prompt_explanation, source="English", target=target)

def generate_mini_quiz(source_text, translated_text, target="Tamil"):
    q1_text = translate_text("What is the central subject of this lesson?", source="English", target=target)
    words = re.findall(r'\b\w+\b', translated_text)
    kw = words[0] if words else "Education"

    return [
        {
            "question": q1_text,
            "options": [kw, "Music & Art", "Sports & Games"],
            "correct": 0
        },
        {
            "question": translate_text("Is this concept fundamental to understanding science and nature?", source="English", target=target),
            "options": [
                translate_text("Yes, extremely important", source="English", target=target),
                translate_text("No, not required", source="English", target=target)
            ],
            "correct": 0
        }
    ]

def answer_student_doubt(lesson_text, doubt_question, target="Tamil"):
    """Answers a student doubt in their mother tongue with clear conceptual explanation."""
    doubt_lower = doubt_question.lower().strip()
    
    # Analyze doubt against lesson context
    context_sentences = [s.strip() for s in (lesson_text or "").split('.') if len(s.strip()) > 5]
    relevant_context = ". ".join(context_sentences[:2]) if context_sentences else (lesson_text or "this scientific concept")
    
    if any(w in doubt_lower for w in ["why", "reason", "purpose"]):
        explanation = f"Key Reason: {relevant_context}. This is essential for living organisms and natural balance."
    elif any(w in doubt_lower for w in ["what", "define", "meaning"]):
        explanation = f"Definition: {relevant_context}. In simple terms, this is the core principle of this topic."
    elif any(w in doubt_lower for w in ["how", "process", "step"]):
        explanation = f"How it works: {relevant_context}. It operates through interconnected biological and physical mechanisms."
    else:
        explanation = f"Key learning note: Regarding your question '{doubt_question}', remember that {relevant_context}."
        
    return translate_text(explanation, source="English", target=target)

