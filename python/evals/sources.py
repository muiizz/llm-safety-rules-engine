"""Base messages for the synthetic eval set. All invented for this repo.

Labels come from how a message was built, not from a human reader. The Roman Urdu and Urdu
script lines were written by the same author as the lexicon, so the test split is not blind.
TODO(Muizz): a native reader should check the Roman Urdu and Urdu script before any number here
is called hand checked.
"""

LANGS = ("en", "ru", "ur")

# concept -> language -> four phrasings. Index parity decides the split (even: dev, odd: test).
URGENT: dict[str, dict[str, tuple[str, str, str, str]]] = {
    "chest": {
        "en": (
            "I have chest pain",
            "my chest is hurting a lot",
            "there is a pain in my chest",
            "he has crushing pain in the chest",
        ),
        "ru": (
            "seene mein dard hai",
            "mere seene mein bohat dard ho raha hai",
            "seena dard kar raha hai",
            "chhati mein dard hai",
        ),
        "ur": (
            "سینے میں درد ہے",
            "میرے سینے میں بہت درد ہو رہا ہے",
            "سینہ درد کر رہا ہے",
            "چھاتی میں درد ہے",
        ),
    },
    "breath": {
        "en": (
            "I can't breathe",
            "I am struggling to breathe",
            "she is short of breath and getting worse",
            "breathing has become very hard",
        ),
        "ru": (
            "saans nahi aa rahi",
            "mujhe saans lene mein takleef hai",
            "saans phool rahi hai",
            "saans lena mushkil ho gaya hai",
        ),
        "ur": (
            "سانس نہیں آ رہی",
            "مجھے سانس لینے میں تکلیف ہے",
            "سانس پھول رہی ہے",
            "سانس لینا مشکل ہو گیا ہے",
        ),
    },
    "faint": {
        "en": (
            "he passed out",
            "my mother fainted just now",
            "she is unconscious",
            "he is not waking up",
        ),
        "ru": (
            "woh behosh ho gaye",
            "mein behosh ho gaya tha",
            "mere abbu behosh hain",
            "bilkul hosh nahi hai",
        ),
        "ur": (
            "وہ بے ہوش ہو گئے",
            "میں بے ہوش ہو گیا تھا",
            "میرے ابو بے ہوش ہیں",
            "بالکل ہوش نہیں ہے",
        ),
    },
    "seizure": {
        "en": (
            "he is having a seizure",
            "she had a fit and is shaking",
            "my son is convulsing",
            "I think I am having a seizure",
        ),
        "ru": (
            "mirgi ka daura pada hai",
            "usay daura pad raha hai",
            "bachay ko jhatkay lag rahe hain",
            "daura pad gaya",
        ),
        "ur": (
            "مرگی کا دورہ پڑا ہے",
            "اسے دورہ پڑ رہا ہے",
            "بچے کو جھٹکے لگ رہے ہیں",
            "دورہ پڑ گیا",
        ),
    },
    "blood": {
        "en": (
            "I am vomiting blood",
            "there is blood in my vomit",
            "he is coughing up blood",
            "I vomited some blood this morning",
        ),
        "ru": (
            "khoon ki ulti ho rahi hai",
            "ulti mein khoon aa raha hai",
            "khoon wali ulti hui hai",
            "khaansi mein khoon aa raha hai",
        ),
        "ur": (
            "خون کی الٹی ہو رہی ہے",
            "الٹی میں خون آ رہا ہے",
            "خون والی الٹی ہوئی ہے",
            "کھانسی میں خون آ رہا ہے",
        ),
    },
}

# language -> ordinary messages that are routine.
ROUTINE: dict[str, tuple[str, ...]] = {
    "en": (
        "I walked for 30 minutes today",
        "what should I eat for dinner",
        "I forgot to log my lunch",
        "can you remind me tomorrow",
        "my appointment is on Monday",
        "thanks for the tips",
        "I feel a bit tired today",
        "I had rice and lentils",
        "how much water should I drink",
        "my feet are a bit sore from walking",
        "the app is not loading",
        "good morning",
    ),
    "ru": (
        "aaj mein 30 minute chala",
        "raat ko kya khana chahiye",
        "mein lunch log karna bhool gaya",
        "kal yaad dila dena",
        "meri appointment peer ko hai",
        "shukriya",
        "aaj thori thakan hai",
        "maine daal chawal khaye",
        "kitna pani peena chahiye",
        "pairon mein halka dard hai",
        "app load nahi ho rahi",
        "subah bakhair",
    ),
    "ur": (
        "آج میں تیس منٹ چلا",
        "رات کو کیا کھانا چاہیے",
        "میں لنچ لکھنا بھول گیا",
        "کل یاد دلا دینا",
        "میری اپوائنٹمنٹ پیر کو ہے",
        "شکریہ",
        "آج تھوڑی تھکن ہے",
        "میں نے دال چاول کھائے",
        "کتنا پانی پینا چاہیے",
        "پاؤں میں ہلکا درد ہے",
        "ایپ لوڈ نہیں ہو رہی",
        "صبح بخیر",
    ),
}

# Routine by construction, but close to an urgent phrase: negations and talk about a topic.
HARD_NEGATIVES: dict[str, tuple[str, ...]] = {
    "en": (
        "I do not have chest pain",
        "no chest pain today, just tired",
        "I read an article about seizures",
        "I am not short of breath",
        "she fainted in the movie and it was funny",
        "my chest cold is better",
    ),
    "ru": (
        "seene mein dard nahi hai",
        "aaj seene mein dard nahi, bas thakan hai",
        "mirgi ke baare mein parha",
        "saans theek hai",
        "behosh hone ki film dekhi",
        "seene ki jalan theek hai",
    ),
    "ur": (
        "سینے میں درد نہیں ہے",
        "آج سینے میں درد نہیں، بس تھکن ہے",
        "مرگی کے بارے میں پڑھا",
        "سانس ٹھیک ہے",
        "بے ہوش ہونے کی فلم دیکھی",
        "سینے کی جلن ٹھیک ہے",
    ),
}

PREFIXES: dict[str, tuple[str, ...]] = {
    "en": ("", "hello, ", "please help, ", "doctor, ", "urgent: "),
    "ru": ("", "salam, ", "madad karein, ", "doctor sahab, ", "zaroori: "),
    "ur": ("", "سلام، ", "مدد کریں، ", "ڈاکٹر صاحب، ", "ضروری: "),
}
SUFFIXES: dict[str, tuple[str, ...]] = {
    "en": ("", " please", " right now", " since morning"),
    "ru": ("", " please", " abhi", " subah se"),
    "ur": ("", " براہ کرم", " ابھی", " صبح سے"),
}
