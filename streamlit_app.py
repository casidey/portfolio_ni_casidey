"""Postcard from Cebu: a personal autobiography and portfolio app.

Run with:  streamlit run streamlit_app.py
Edit your details in content.py.
"""

import io
import json
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import altair as alt
import pandas as pd
import pydeck as pdk
import streamlit as st
from PIL import Image, ImageDraw, ImageFont, ImageOps

import content as c

APP_DIR = Path(__file__).parent
PHOTO_DIR = APP_DIR / "photos"

st.set_page_config(
    page_title=f"{c.NAME} · Postcard from Cebu",
    page_icon=":material/travel_explore:",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# --- Session state (one place) ------------------------------------------------
st.session_state.setdefault("featured_idx", 0)
st.session_state.setdefault("postcards", [])

TILE_COLORS = [
    ("#F7E7C6", "#6B5832"),
    ("#CDE7E4", "#134E4A"),
    ("#F9D9C8", "#7C2D12"),
    ("#E4E1F5", "#3730A3"),
]


# --- Helpers ---------------------------------------------------------------------
@st.cache_data(max_entries=64)
def placeholder_tile(label: str, palette_idx: int, size: tuple[int, int] = (900, 675)) -> bytes:
    """A soft colored tile shown when a photo file hasn't been added yet."""
    bg, fg = TILE_COLORS[palette_idx % len(TILE_COLORS)]
    img = Image.new("RGB", size, bg)
    draw = ImageDraw.Draw(img)
    try:
        font = ImageFont.load_default(size=34)
    except TypeError:  # older Pillow
        font = ImageFont.load_default()
    text = f"Add a photo: {label}"
    box = draw.textbbox((0, 0), text, font=font)
    x = (size[0] - (box[2] - box[0])) / 2
    y = (size[1] - (box[3] - box[1])) / 2
    draw.text((x, y), text, fill=fg, font=font)
    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()


@st.cache_data(max_entries=64)
def crop_photo(path: str, changed: float) -> bytes:
    """Crop a photo to 4:3 so every image on the page is the same size."""
    img = Image.open(path)
    img = ImageOps.exif_transpose(img)  # keeps phone photos the right way up
    img = img.convert("RGB")
    img = ImageOps.fit(img, (900, 675))  # 900 x 675 = 4:3, cropped from the center
    buf = io.BytesIO()
    img.save(buf, format="JPEG", quality=90)
    return buf.getvalue()


def photo(file_name: str, label: str, palette_idx: int = 0):
    """Return the cropped photo if it exists, otherwise a placeholder tile."""
    if file_name:
        path = PHOTO_DIR / file_name
        if path.exists():
            return crop_photo(str(path), path.stat().st_mtime)
    return placeholder_tile(label, palette_idx)


@st.cache_data(ttl=900, max_entries=4, show_spinner=False)
def current_weather(lat: float, lon: float) -> dict | None:
    """Live weather from Open-Meteo (free, no key). Returns None if offline."""
    url = (
        "https://api.open-meteo.com/v1/forecast"
        f"?latitude={lat}&longitude={lon}&current=temperature_2m,weather_code&timezone=auto"
    )
    try:
        with urllib.request.urlopen(url, timeout=3) as resp:
            data = json.load(resp)["current"]
    except Exception:
        return None
    code = data.get("weather_code", -1)
    if code == 0:
        sky = "Clear"
    elif code in (1, 2):
        sky = "Partly cloudy"
    elif code == 3:
        sky = "Cloudy"
    elif code in (45, 48):
        sky = "Foggy"
    elif 51 <= code <= 67 or 80 <= code <= 82:
        sky = "Rainy"
    elif code >= 95:
        sky = "Thunderstorms"
    else:
        sky = "—"
    return {"temp": data.get("temperature_2m"), "sky": sky}


def next_project(step: int, count: int) -> None:
    st.session_state.featured_idx = (st.session_state.featured_idx + step) % count


def send_postcard() -> None:
    name = st.session_state.pc_name.strip()
    message = st.session_state.pc_message.strip()
    if not name or not message:
        st.session_state.pc_error = True
        return
    st.session_state.pc_error = False
    st.session_state.postcards.append(
        {"name": name, "message": message, "mood": st.session_state.pc_mood}
    )
    st.session_state.pc_name = ""
    st.session_state.pc_message = ""
    st.session_state.pc_sent = True


# --- Hero: the map of where I live -------------------------------------------------
home = c.HOME
pin = pd.DataFrame([{"label": home["label"], "lat": home["lat"], "lon": home["lon"]}])
deck = pdk.Deck(
    map_style=None,  # Streamlit picks a Carto basemap that matches the theme
    initial_view_state=pdk.ViewState(
        latitude=home["lat"], longitude=home["lon"], zoom=8.6, pitch=35, bearing=-10
    ),
    layers=[
        pdk.Layer(  # soft halo
            "ScatterplotLayer",
            data=pin,
            get_position="[lon, lat]",
            get_radius=9000,
            get_fill_color=[194, 65, 12, 45],
            pickable=False,
        ),
        pdk.Layer(  # the pin
            "ScatterplotLayer",
            data=pin,
            get_position="[lon, lat]",
            get_radius=1800,
            get_fill_color=[194, 65, 12, 240],
            get_line_color=[255, 255, 255],
            line_width_min_pixels=3,
            stroked=True,
            pickable=True,
        ),
        pdk.Layer(
            "TextLayer",
            data=pin,
            get_position="[lon, lat]",
            get_text="label",
            get_size=18,
            get_color=[16, 48, 47],
            get_pixel_offset=[0, -28],
            font_weight=700,
        ),
    ],
    tooltip={"text": "{label}: this is where I live"},
)
st.pydeck_chart(deck, height=420, alt=f"Map of {home['region']} with a pin on {home['label']}, where I live")

# Greeting card
with st.container(border=True):
    st.caption(f":material/waving_hand: {c.GREETING}")
    st.title(f"I'm {c.NAME}.")
    st.markdown(c.TAGLINE)
    with st.container(horizontal=True, gap="small"):
        for badge in c.ROLE_BADGES:
            st.badge(badge, color="orange" if badge == c.ROLE_BADGES[0] else "gray")
    with st.container(horizontal=True, gap="small"):
        for label, link in c.LINKS.items():
            if link["url"]:
                st.link_button(label, link["url"], icon=link["icon"])
        resume = APP_DIR / c.RESUME_FILE
        if resume.exists():
            st.download_button(
                "Download résumé",
                data=resume.read_bytes(),
                file_name=c.RESUME_FILE,
                mime="application/pdf",
                icon=":material/download:",
                type="primary",
            )

# Quick numbers
with st.container(horizontal=True, gap="medium"):
    for stat in c.STATS:
        st.metric(stat["label"], stat["value"], help=stat["help"], border=True)

# Life in Cebu right now
st.subheader("Life in Cebu right now", icon=":material/location_on:")
local_now = datetime.now(timezone(timedelta(hours=home["utc_offset_hours"])))
weather = current_weather(home["lat"], home["lon"])
with st.container(horizontal=True, gap="medium"):
    st.metric("Local time", local_now.strftime("%I:%M %p").lstrip("0"), border=True)
    if weather and weather["temp"] is not None:
        st.metric("Weather now", f"{weather['temp']:.0f}°C", weather["sky"], delta_color="off", border=True)
    else:
        st.metric("Weather now", "—", "offline", delta_color="off", border=True)
    for label, value in c.LOCAL_FAVORITES.items():
        st.metric(label, value, border=True)

# --- My story, in chapters ------------------------------------------------------------
st.header("My story, in chapters", icon=":material/auto_stories:")
chapter_titles = [ch["title"] for ch in c.CHAPTERS]
chapter_icons = {ch["title"]: ch["icon"] for ch in c.CHAPTERS}
picked = st.segmented_control(
    "Chapter",
    chapter_titles,
    default=chapter_titles[0],
    required=True,
    format_func=lambda t: f"{chapter_icons[t]} {t}",
    label_visibility="collapsed",
    key="chapter",
)
chapter_idx = chapter_titles.index(picked)
chapter = c.CHAPTERS[chapter_idx]

photo_col, text_col = st.columns([1, 1], gap="large", vertical_alignment="center")
with photo_col:
    st.image(
        photo(chapter["photo"], chapter["title"], chapter_idx),
        width="stretch",
        alt=f"Photo from the {chapter['title']} chapter of my life",
    )
with text_col:
    st.subheader(f"Chapter {chapter_idx + 1} · {chapter['title']}")
    st.caption(chapter["when"])
    for paragraph in chapter["paragraphs"]:
        st.markdown(paragraph)
    with st.container(horizontal=True, gap="small"):
        for tag in chapter["tags"]:
            st.badge(tag, color="blue")
    st.progress(
        (chapter_idx + 1) / len(c.CHAPTERS),
        text=f"Chapter {chapter_idx + 1} of {len(c.CHAPTERS)}",
    )

# Journey timeline (appears once every chapter has start and end years)
if all(isinstance(ch["start"], int) and isinstance(ch["end"], int) for ch in c.CHAPTERS):
    journey = pd.DataFrame(
        [{"Chapter": ch["title"], "Start": ch["start"], "End": ch["end"]} for ch in c.CHAPTERS]
    )
    journey_chart = (
        alt.Chart(journey)
        .mark_bar(cornerRadius=8, height=22)
        .encode(
            x=alt.X("Start:Q", title=None, axis=alt.Axis(format="d")),
            x2="End:Q",
            y=alt.Y("Chapter:N", sort=chapter_titles, title=None),
            color=alt.Color("Chapter:N", legend=None, sort=chapter_titles),
            tooltip=["Chapter", "Start", "End"],
        )
    )
    st.altair_chart(journey_chart, alt="Timeline of the chapters of my life by year")
else:
    st.caption(
        ":material/timeline: Add start and end years to each chapter in content.py to see your journey timeline here."
    )

# --- Things I love ------------------------------------------------------------------
st.header("Things I love", icon=":material/favorite:")
love_cols = st.columns(len(c.LOVES), gap="medium")
for i, (col, love) in enumerate(zip(love_cols, c.LOVES)):
    with col:
        st.image(
            photo(love["photo"], love["caption"], i),
            caption=love["caption"],
            width="stretch",
            alt=love["caption"],
        )

# --- Things I've built --------------------------------------------------------------
st.header("Things I've built", icon=":material/construction:")
categories = sorted({p["category"] for p in c.PROJECTS})
chosen = st.pills(
    "Filter by type",
    categories,
    selection_mode="multi",
    key="project_filter",
)
projects = [p for p in c.PROJECTS if not chosen or p["category"] in chosen]

featured = [p for p in projects if p["featured"]]
if featured:
    idx = st.session_state.featured_idx % len(featured)
    project = featured[idx]
    with st.container(border=True):
        img_col, info_col = st.columns([1, 1], gap="large", vertical_alignment="center")
        with img_col:
            st.image(
                photo(project["photo"], project["name"], idx + 1),
                width="stretch",
                alt=f"Screenshot of {project['name']}",
            )
        with info_col:
            year = project["year"] or "[year]"
            st.caption(f"Featured · {project['category']} · {year}")
            st.subheader(project["name"])
            st.markdown(project["summary"])
            with st.container(horizontal=True, gap="small"):
                for tech in project["stack"]:
                    st.badge(tech, color="gray")

    with st.container(horizontal=True, horizontal_alignment="distribute", vertical_alignment="center"):
        st.button(
            "Previous",
            icon=":material/chevron_left:",
            on_click=next_project,
            args=(-1, len(featured)),
            key="prev_project",
        )
        st.caption(f"{idx + 1} of {len(featured)} featured")
        st.button(
            "Next",
            icon=":material/chevron_right:",
            on_click=next_project,
            args=(1, len(featured)),
            key="next_project",
        )
else:
    st.caption("No featured projects match that filter.")

all_tab, skills_tab = st.tabs([":material/table_rows: All projects", ":material/bar_chart: Skills"])
with all_tab:
    table = pd.DataFrame(
        [
            {
                "Project": p["name"],
                "Type": p["category"],
                "Year": p["year"],
                "Stack": p["stack"],
                "Status": p["status"],

            }
            for p in projects
        ]
    )
    st.dataframe(
        table,
        hide_index=True,
        column_config={
            "Year": st.column_config.NumberColumn(format="%d"),
            "Stack": st.column_config.ListColumn(),
            "Status": st.column_config.SelectboxColumn(options=["Live", "In progress", "Archived"]),

        },
        alt="Table of all my projects with type, year, tech stack, status and links",
    )
with skills_tab:
    skills = pd.DataFrame({"Skill": list(c.SKILLS), "Level": list(c.SKILLS.values())})
    skills_chart = (
        alt.Chart(skills)
        .mark_bar(cornerRadiusEnd=8, height=24)
        .encode(
            x=alt.X("Level:Q", scale=alt.Scale(domain=[0, 100]), title="Comfort level"),
            y=alt.Y("Skill:N", sort="-x", title=None),
            tooltip=["Skill", "Level"],
        )
    )
    st.altair_chart(skills_chart, alt="Bar chart of how comfortable I am with each skill")

# --- Fun facts + postcard -------------------------------------------------------------
facts_col, form_col = st.columns([1, 1], gap="large")
with facts_col:
    st.header("Fun facts", icon=":material/lightbulb:")
    for i, fact in enumerate(c.FUN_FACTS):
        with st.expander(fact["q"], icon=fact["icon"], expanded=i == 0):
            st.markdown(fact["a"])

    st.subheader("Enjoying the visit?")
    rating = st.feedback("faces", key="visit_rating")
    if rating is not None:
        st.caption("Salamat! Thanks for letting me know. :material/favorite:")

with form_col:
    st.header("Send me a postcard", icon=":material/mail:")
    with st.form("postcard", border=True):
        st.text_input("Your name", key="pc_name", max_chars=60)
        st.text_area("Message", key="pc_message", max_chars=500, height=120)
        st.select_slider(
            "How's your day going?",
            options=["Rough", "Okay", "Good", "Great", "Amazing"],
            value="Good",
            key="pc_mood",
        )
        st.form_submit_button(
            "Send it", icon=":material/send:", type="primary", width="stretch", on_click=send_postcard
        )

    if st.session_state.pop("pc_error", False):
        st.warning("Please add your name and a message before sending.", icon=":material/edit:")
    if st.session_state.pop("pc_sent", False):
        st.toast("Postcard sent. Salamat!", icon=":material/mark_email_read:")
        st.balloons()

    if st.session_state.postcards:
        st.caption("Postcards from this visit")
        for card in reversed(st.session_state.postcards):
            with st.chat_message("user", avatar=":material/mail:"):
                st.markdown(f"**{card['name']}** · feeling {card['mood'].lower()}")
                st.markdown(card["message"])
    st.caption(
        "Postcards are kept only while this page is open. "
        "Hook the form up to email or a Google Sheet to actually receive them."
    )

st.space("large")
st.caption(f"Made with Streamlit in {home['label']} · © {local_now.year} {c.FULL_NAME}", text_alignment="center")