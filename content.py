
NAME = "Casidey"
FULL_NAME = "Casidey Kirzteen A. Quibuyen"
GREETING = "Maayong adlaw"
TAGLINE = "A student who loves to go with the flow"
ROLE_BADGES = ["Soon to be a full stack developer",]

LINKS = {
    "GitHub": {"url": "", "icon": "https://github.com/casidey"},
    "Email me": {"url": "", "icon": "casidey.kirzteen.quibuyen@gmail.com"},
}

RESUME_FILE = "https://docs.google.com/document/d/1bS3Kjwr5RDoYfaTLv5DOSUHDzyeAjuFzdaA9n4mLubw/edit?usp=sharing"

HOME = {
    "label": "Cebu City",
    "region": "Cebu, Philippines",
    "lat": 10.3157,
    "lon": 123.8854,
    "utc_offset_hours": 8,
}

LOCAL_FAVORITES = {
    "Favorite spot": "SRP seawall",
    "Must-eat": "Angel's Pizza mac n' cheese",
}

STATS = [
    {"label": "Projects built", "value": "4", "help": "Apps, sites and experiments"},
    {"label": "Years coding", "value": "3", "help": "Since my first line of code"},
    {"label": "Languages I code in", "value": "1", "help": None},
    {"label": "Cups of coffee / week", "value": "2", "help": None},
]

# --- Your story, in chapters ---------------------------------------------------
# start/end are years (numbers). Fill them in to unlock the journey timeline chart.
CHAPTERS = [
    {
        "title": "Roots",
        "icon": ":material/home:",
        "start": 2005,
        "end": 2015,
        "when": "[birth year] – [year]",
        "paragraphs": [
            "I was born and raised right here in Cebu City.",
            "Growing up, my lola, who I call Nanay, took care of me all the way until high school. "
            "She's like a second mother to me, and a lot of who I am today comes from her.",
        ],
        "tags": ["Cebu City", "Nanay"],
        "photo": "me.png",
    },
    {
        "title": "School",
        "icon": ":material/school:",
        "start": None,
        "end": None,
        "when": "[year] – [year]",
        "paragraphs": [
            "I went to the University of Cebu for high school, then moved to CIT for college "
            "to take up Computer Science.",
            "The person who got me into coding was Sir Amparo. He's really good at teaching, he knows "
            "how to vibe with his students, and he always helped us debug. That's when coding started "
            "to click for me.",
        ],
        "tags": ["University of Cebu", "CIT", "Computer Science"],
        "photo": "uc_graduate.png",
    },
    {
        "title": "Today",
        "icon": ":material/today:",
        "start": 2025,
        "end": None,
        "when": "[year] – now",
        "paragraphs": [
            "My weeks look a lot different now than before. Things can get tiring, so I've been "
            "putting my energy into sharpening my skills and preparing for the future.",
            "I am trying to learn machine learning as of the moment.",
        ],
        "tags": ["2026", "Leveling up"],
        "photo": "today.png",
    },
    {
        "title": "What's next",
        "icon": ":material/flag:",
        "start": None,
        "end": None,
        "when": "Next",
        "paragraphs": [
            "I dream of being somewhere new, where no one knows me yet, doing the things I've always dreamed of.",
            "My goal is a comfortable life where I can support my parents and be happy. I've seen how hard "
            "life gets when money isn't enough, and that's what keeps me working hard now.",
        ],
        "tags": ["Support my parents", "A comfortable, happy life"],
        "photo": "family.png",
    },
]

LOVES = [
    {"caption": "[Favorite beach or spot]", "photo": "seawall.png"},
    {"caption": "[Favorite food]", "photo": "macNcheese.png"},
    {"caption": "[Hobby]", "photo": "netflix.png"},
    {"caption": "[People / pets]", "photo": "pet.png"},
]

PROJECTS = [
    {
        "name": "DormWise",
        "category": "Web",
        "year": 2026,
        "stack": ["python", "supabase"],
        "status": "archived",
        "summary": "[What DormWise does, e.g. helps students find, compare or manage dorms.]",
        "photo": "dormwise.png",
        "featured": True,
    },
    {
        "name": "Tindahan Ledger",
        "category": "Web",
        "year": 2026,
        "stack": ["python", "supabase"],
        "status": "archived",
        "summary": "A pricing helper for sari-sari store owners. It works out a selling price for each "
                   "product that still makes a profit after costs like electricity, so small stores "
                   "don't end up selling at a loss.",
        "photo": "sarisari.png",
        "featured": True,
    },
    {
        "name": "Kalsada Watch",
        "category": "web",
        "year": 2026,
        "stack": ["C# (Blazor)"],
        "status": "archived",
        "summary": "[What Kalsada Watch does, e.g. lets people report road problems like potholes or flooding.]",
        "photo": "kalsada_watch.png",
        "featured": True,
    },
]

SKILLS = {
    "Python": 80,
    "Java": 30,
    "Kotlin": 40,
    "JavaScript": 30,
}


FUN_FACTS = [
    {"q": "Comfort food?", "a": "Mac n' cheese from Angel's Pizza, every time.", "icon": ":material/restaurant:"},
    {"q": "Where do you go to unwind?", "a": "The seawall sidewalk near SRP.", "icon": ":material/waves:"},
    {"q": "Who got you into coding?", "a": "My father always convinces me to try coding when I was still a kid.", "icon": ":material/school:"},
    {"q": "Song on repeat", "a": "kalapastangan and dandelions", "icon": ":material/music_note:"},
    {"q": "If you weren't coding, you'd be…", "a": "Policeman", "icon": ":material/explore:"},
]