import os, re, json, time, uuid, hmac, hashlib, sqlite3, subprocess, sys, tempfile, datetime
import pandas as pd
import streamlit as st
import chromadb
from google import genai
from google.genai import types

try:
    from openai import OpenAI  # Groq və Perplexity bu kitabxana ilə işləyir
except ImportError:
    OpenAI = None

# ======================= PROVAYDERLƏR =======================
# free=True olanlar "Avto" rejimdə işləyir. Pullu provayder (Perplexity) yalnız veb axtarışı,
# araşdırma sualları və sən seçəndə işləyir, hər gün üçün sorğu limiti var (kreditə qoruma).
PROVIDERS = {
    "gemini": dict(label="Gemini (Google)", kind="gemini", env="GEMINI_API_KEY", free=True,
                   model_env="GEMINI_MODEL", fallback="gemini-flash-latest"),
    "groq": dict(label="Groq (açıq modellər)", kind="openai", env="GROQ_API_KEY", free=True,
                 base="https://api.groq.com/openai/v1",
                 model_env="GROQ_MODEL", fallback="llama-3.3-70b-versatile"),
    "perplexity": dict(label="Perplexity (veb axtarışı)", kind="openai", env="PERPLEXITY_API_KEY", free=False,
                       base="https://api.perplexity.ai",
                       model_env="PERPLEXITY_MODEL", fallback="sonar", cap=30,
                       extra_body={"web_search_options": {"search_context_size": "low"}}),
}
AUTO_ORDER = [p.strip() for p in os.getenv("AUTO_ORDER", "gemini,groq").split(",") if p.strip()]

EMBED = "gemini-embedding-001"  # dəyişmə: dəyişsən materialları yenidən yükləmək lazım olar
GROQ_STT = os.getenv("GROQ_STT_MODEL", "whisper-large-v3-turbo")
AZ_VOICE = "az-AZ-BanuNeural"
EN_VOICE = "en-US-AriaNeural"

SUBJ = {
    "az": {
        "gen": "Ümumi köməkçi",
        "rtp": "Rəqəmsal texnologiya və proqramlaşdırma",
        "er": "İqtisadi təfəkkür (Economic reasoning)",
        "kom": "Azərbaycan dilində kommunikasiya",
        "rwct": "Reading, Writing and Critical Thinking",
        "lsct": "Listening, Speaking and Critical Thinking",
    },
    "en": {
        "gen": "General assistant",
        "rtp": "Digital technology and programming",
        "er": "Economic reasoning",
        "kom": "Communication skills (Azerbaijani)",
        "rwct": "Reading, Writing and Critical Thinking",
        "lsct": "Listening, Speaking and Critical Thinking",
    },
}
SUBJ_KEYS = list(SUBJ["az"])
EN_SUBJ = ("rwct", "lsct")
AZ_SUBJ = ("rtp", "er", "kom")

TXT = {
    "az": {
        "page_tutor": "💬 Tutor", "page_lab": "🧪 Kod laboratoriyası",
        "subject": "Fənn", "mode": "Rejim",
        "m_learn": "📖 İzah", "m_practice": "🏋️ Praktika", "m_exam": "📝 İmtahan",
        "provider": "Model mənbəyi",
        "p_auto": "Avto (yalnız pulsuzlar)", "p_smart": "Ağıllı seçim (araşdırma sualları Perplexity-yə)",
        "free": "pulsuz", "paid": "pullu",
        "web": "🔎 Veb axtarışı",
        "verify": "Dəqiqlik rejimi (2 sorğu)",
        "speak": "🔊 Tutor səslə cavab versin",
        "voice": "🎤 Mikrofonla danışım",
        "chats": "🗂 Söhbətlər", "new_chat": "➕ Yeni söhbət", "no_chats": "Bu fənndə hələ söhbət yoxdur.",
        "delete": "Söhbəti sil",
        "ask_ph": "Sualını yaz...", "sources": "📚 Mənbələr", "web_sources": "🌐 Veb mənbələr",
        "page_word": "səhifə",
        "save_mem": "💾 Yaddaşa yaz", "mem_ok": "Yaddaşa yazıldı", "my_mem": "🧠 Yaddaşım",
        "mic": "🎤 Danış", "mic_hint": "Danış, sonra dayandır",
        "transcribing": "Səsin yazıya çevrilir...", "mic_empty": "Səs başa düşülmədi, yenidən cəhd et.",
        "read": "Səslə oxu",
        "verifying": "Cavab hazırlanır və yoxlanılır...",
        "answered": "Cavabı verdi",
        "usage": "Bu gün sorğu sayı",
        "voice_test": "🔊 Səsi yoxla", "voice_test_text": "Salam, mən sənin tutorunam.",
        "tts_missing": "Səs üçün terminalda bunu yaz: pip install edge-tts",
        "tts_err": "Səs alınmadı. Terminalda bunu yaz: pip install -U edge-tts. Xəta: ",
        "busy": "Model hazırda yüklüdür və ya limit dolub. 1-2 dəqiqə sonra yenidən yaz.",
        "empty": "Model boş cavab qaytardı. Sualı bir az fərqli yaz.",
        "no_provider": "Heç bir model qoşulmayıb. Açarları yoxla.",
        "cap": "Perplexity günlük limitinə çatdı (kreditə qoruma). Sabah davam et və ya PERPLEXITY_DAILY_CAP ilə limiti artır.",
        "err": "Xəta: ",
        "providers": "🔌 Provayderlər", "key_missing": "açar yoxdur", "pkg_missing": "paket yoxdur",
        "lab_title": "🧪 Kod laboratoriyası", "lab_lang": "Dil",
        "py_code": "Python kodu", "sql_setup": "Cədvəl və data (setup)", "sql_query": "SQL sorğusu",
        "run": "▶️ İşə sal", "feedback": "🧑‍🏫 Tutordan rəy al",
        "theme_note": "Tema: yuxarı sağdakı ⋮ → Settings → Theme.",
    },
    "en": {
        "page_tutor": "💬 Tutor", "page_lab": "🧪 Code lab",
        "subject": "Subject", "mode": "Mode",
        "m_learn": "📖 Learn", "m_practice": "🏋️ Practice", "m_exam": "📝 Exam",
        "provider": "Model source",
        "p_auto": "Auto (free ones only)", "p_smart": "Smart pick (research questions go to Perplexity)",
        "free": "free", "paid": "paid",
        "web": "🔎 Web search",
        "verify": "Accuracy mode (2 requests)",
        "speak": "🔊 Tutor answers aloud",
        "voice": "🎤 Talk with microphone",
        "chats": "🗂 Chats", "new_chat": "➕ New chat", "no_chats": "No chats in this subject yet.",
        "delete": "Delete chat",
        "ask_ph": "Type your question...", "sources": "📚 Sources", "web_sources": "🌐 Web sources",
        "page_word": "page",
        "save_mem": "💾 Save to memory", "mem_ok": "Saved to memory", "my_mem": "🧠 My memory",
        "mic": "🎤 Speak", "mic_hint": "Speak, then stop",
        "transcribing": "Turning your voice into text...", "mic_empty": "I could not understand the audio. Try again.",
        "read": "Read aloud",
        "verifying": "Preparing and checking the answer...",
        "answered": "Answered by",
        "usage": "Requests today",
        "voice_test": "🔊 Test voice", "voice_test_text": "Hello, I am your tutor.",
        "tts_missing": "For voice, run this in the terminal: pip install edge-tts",
        "tts_err": "No audio. Run this in the terminal: pip install -U edge-tts. Error: ",
        "busy": "The model is busy or the limit is reached. Try again in 1-2 minutes.",
        "empty": "The model returned an empty answer. Rephrase the question a little.",
        "no_provider": "No model is connected. Check your keys.",
        "cap": "Perplexity reached its daily cap (credit protection). Continue tomorrow or raise PERPLEXITY_DAILY_CAP.",
        "err": "Error: ",
        "providers": "🔌 Providers", "key_missing": "no key", "pkg_missing": "package missing",
        "lab_title": "🧪 Code lab", "lab_lang": "Language",
        "py_code": "Python code", "sql_setup": "Tables and data (setup)", "sql_query": "SQL query",
        "run": "▶️ Run", "feedback": "🧑‍🏫 Get tutor feedback",
        "theme_note": "Theme: top-right ⋮ → Settings → Theme.",
    },
}

MODES = {
    "learn": "",
    "practice": (
        "ACTIVE MODE: PRACTICE. Give one task at a time with rising difficulty. "
        "Wait for the student's attempt, then give feedback and the next task."
    ),
    "exam": (
        "ACTIVE MODE: EXAM. Ask exactly 5 questions in the exam format from COURSE INFO "
        "(if absent, use a sensible university format). Ask them ONE BY ONE, check each answer, "
        "and at the end give a score out of 100 and list weak topics."
    ),
}

DEFAULT_GEN = (
    "You are a friendly, honest study assistant for a first-year university student in Azerbaijan. "
    "Reply in the language the student writes in (Azerbaijani or English). "
    "Explain simply, use everyday examples, and ask at most one short question per reply. "
    "If you are not sure, say so instead of inventing facts. "
    "Do not do graded homework for the student; give hints and plans instead."
)

RULES = (
    "RULES FOR ALL REPLIES:\n"
    "- If you use the MATERIALS, cite [file, page]. Never invent citations.\n"
    "- Do not mention the student's major, field or future career (for example finance or fintech) "
    "unless the student brings it up. Use neutral everyday examples.\n"
    "- Keep replies focused and not too long."
)

VERIFY_SYS = (
    "You are a strict reviewer. You get MATERIALS, the student's question and a DRAFT tutor reply. "
    "Fix factual errors, invented citations, and violations of the tutor rules (for example giving a full "
    "answer to graded work, or more than one question per reply). Keep the same language, tone and length. "
    "Output ONLY the final reply and never mention the review."
)

for d in ("memory", "chats", "profiles"):
    os.makedirs(d, exist_ok=True)

client = genai.Client()
db = chromadb.PersistentClient("db")
USAGE = "usage.json"

st.set_page_config(page_title="Tutor Komandam", page_icon="🎓", layout="wide")
st.session_state.setdefault("ui", "az")
st.session_state.setdefault("cid", None)
st.session_state.setdefault("mic_n", 0)
st.session_state.setdefault("used", "gemini")
st.session_state.setdefault("web_sources", [])
# ---- PIN qoruması (APP_PIN təyin olunubsa; təyin olunmayıbsa yerli işləmədə heç nə soruşmur) ----
_PIN = os.getenv("APP_PIN", "")
if _PIN and not st.session_state.get("authed"):
    st.title("🔒 Tutor Komandam")
    _tries = st.session_state.get("pin_tries", 0)
    if _tries >= 5:
        st.error("Çox səhv cəhd. Səhifəni bağlayıb sonra yenidən cəhd et.")
        st.stop()
    _pin = st.text_input("PIN", type="password")
    if _pin:
        if hmac.compare_digest(_pin.encode(), _PIN.encode()):
            st.session_state["authed"] = True
            st.rerun()
        st.session_state["pin_tries"] = _tries + 1
        st.error("PIN səhvdir.")
    st.stop()

def t(k):
    return TXT[st.session_state.get("ui", "az")][k]


def subj_name(k):
    return SUBJ[st.session_state.get("ui", "az")][k]


def wide(fn, *args, **kwargs):
    """Streamlit versiyalarına görə 'width' və ya 'use_container_width' işlədir."""
    try:
        return fn(*args, width="stretch", **kwargs)
    except TypeError:
        return fn(*args, use_container_width=True, **kwargs)


def read_json(path, default):
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return default


def write_json(path, data):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
    except Exception:
        pass


# ======================= SAYĞAC VƏ KREDİT QORUMASI =======================
def _usage():
    d = read_json(USAGE, {})
    today = datetime.date.today().isoformat()
    if d.get("date") != today:
        d = {"date": today}
    return d


def count_call(pid):
    d = _usage()
    d[pid] = d.get(pid, 0) + 1
    write_json(USAGE, d)


def daily_cap(pid):
    cfg = PROVIDERS[pid]
    if cfg["free"]:
        return None
    try:
        return int(os.getenv(f"{pid.upper()}_DAILY_CAP", cfg.get("cap", 30)))
    except ValueError:
        return cfg.get("cap", 30)


def over_cap(pid):
    cap = daily_cap(pid)
    return cap is not None and _usage().get(pid, 0) >= cap


# ======================= XƏTALAR =======================
def is_busy(e):
    s = str(e)
    return any(w in s for w in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE",
                                "overloaded", "rate_limit", "Rate limit", "529"))


def friendly(e):
    s = str(e)
    if s == "EMPTY":
        return t("empty")
    if s == "NOPROVIDER":
        return t("no_provider")
    if s == "CAP":
        return t("cap")
    if is_busy(e):
        return t("busy")
    return t("err") + s[:300]


# ======================= PROVAYDER QATI =======================
def available(pid):
    cfg = PROVIDERS[pid]
    if not os.getenv(cfg["env"]):
        return False
    if cfg["kind"] == "openai" and OpenAI is None:
        return False
    return True


def openai_client(pid):
    cfg = PROVIDERS[pid]
    if OpenAI is None or not os.getenv(cfg["env"]):
        return None
    return OpenAI(api_key=os.getenv(cfg["env"]), base_url=cfg["base"])


def resolve_model(pid):
    cfg = PROVIDERS[pid]
    return os.getenv(cfg["model_env"]) or cfg["fallback"]


def gemini_stream(system, msgs, temp, web):
    contents = [
        types.Content(role="model" if m["role"] == "assistant" else "user",
                      parts=[types.Part.from_text(text=m["content"])])
        for m in msgs
    ]
    kwargs = dict(system_instruction=system, temperature=temp)
    if web:
        kwargs["tools"] = [types.Tool(google_search=types.GoogleSearch())]
    cfg = types.GenerateContentConfig(**kwargs)
    model = resolve_model("gemini")
    last = None
    for attempt in range(2):
        started = False
        try:
            count_call("gemini")
            for ch in client.models.generate_content_stream(model=model, contents=contents, config=cfg):
                if ch.text:
                    started = True
                    yield ch.text
            return
        except Exception as e:
            if started or not is_busy(e):
                raise
            last = e
            time.sleep(4)
    if last:
        raise last


def openai_stream(pid, system, msgs, temp):
    g = openai_client(pid)
    if g is None:
        raise RuntimeError(f"{pid} is not configured")
    model = resolve_model(pid)
    messages = [{"role": "system", "content": system}] + msgs
    extras = PROVIDERS[pid].get("extra_body")
    count_call(pid)

    # əvvəl bütün parametrlərlə, uyğun gəlməsə sadələşdirilmiş variantlarla cəhd edir
    attempts = [(True, True), (True, False), (False, False)] if extras else [(True, False), (False, False)]
    stream, last = None, None
    for use_temp, use_extra in attempts:
        kw = dict(model=model, messages=messages, stream=True)
        if use_temp:
            kw["temperature"] = temp
        if use_extra:
            kw["extra_body"] = extras
        try:
            stream = g.chat.completions.create(**kw)
            break
        except Exception as e:
            s = str(e)
            if is_busy(e) or any(c in s for c in ("401", "402", "403")):
                raise
            last = e
    if stream is None:
        raise last

    for ch in stream:
        if pid == "perplexity":
            c = getattr(ch, "citations", None)
            if not c:
                c = (getattr(ch, "model_extra", None) or {}).get("citations")
            if c:
                st.session_state["web_sources"] = [str(x) for x in list(c)[:8]]
        if ch.choices and ch.choices[0].delta and ch.choices[0].delta.content:
            yield ch.choices[0].delta.content


def stream_one(pid, system, msgs, temp, web):
    if PROVIDERS[pid]["kind"] == "gemini":
        return gemini_stream(system, msgs, temp, web)
    return openai_stream(pid, system, msgs, temp)


def stream_answer(system, msgs, plan, temp=0.3):
    """plan: [(provayder, veb_axtarışı)] ardıcıllığı. Birincisi alınmasa növbətisinə keçir."""
    st.session_state["web_sources"] = []
    last, tried, capped = None, False, False
    for pid, web in plan:
        if not available(pid):
            continue
        if over_cap(pid):
            capped = True
            continue
        tried = True
        got = False
        try:
            for tok in stream_one(pid, system, msgs, temp, web):
                got = True
                yield tok
            if got:
                st.session_state["used"] = pid + ("+web" if web else "")
                return
        except Exception as e:
            if got:
                raise
            last = e
    if last:
        raise last
    raise RuntimeError("EMPTY" if tried else ("CAP" if capped else "NOPROVIDER"))


def ask_msgs(system, msgs, plan, temp=0.2):
    return "".join(stream_answer(system, msgs, plan, temp))


def free_plan():
    return [(p, False) for p in AUTO_ORDER if p in PROVIDERS and PROVIDERS[p]["free"] and available(p)]


def is_research(q):
    ql = q.lower()
    return any(w in ql for w in ("araşdır", "son xəbər", "bu gün", "cari", "qiymət", "məzənnə", "news",
                                 "latest", "today", "current", "price", "2026"))


def choose_plan(choice, q, web):
    if web:
        plan = [("perplexity", False)] if available("perplexity") else []
        plan.append(("gemini", True))
        return plan
    if choice == "smart":
        pre = [("perplexity", False)] if is_research(q) and available("perplexity") else []
        return pre + free_plan()
    if choice == "auto":
        return free_plan()
    return [(choice, False)]


def provider_label(pid):
    cfg = PROVIDERS[pid]
    return f"{cfg['label']} · {t('free') if cfg['free'] else t('paid')}"


def used_label(used):
    pid = used.replace("+web", "")
    if pid not in PROVIDERS:
        return used
    extra = " + 🔎" if used.endswith("+web") else ""
    return f"{PROVIDERS[pid]['label']} · {resolve_model(pid)}{extra}"


# ======================= MATERIAL AXTARIŞI =======================
@st.cache_data(show_spinner=False)
def embed_cached(text):
    count_call("gemini")
    r = client.models.embed_content(model=EMBED, contents=text)
    return list(r.embeddings[0].values)


def retrieve(key, q, n=8):
    if key == "gen":
        return "", []
    try:
        col = db.get_collection("c_" + key)
        total = col.count()
        if total == 0:
            return "", []
        vec = embed_cached(q[:1000])
        r = col.query(query_embeddings=[vec], n_results=min(n, total))
        parts, srcs = [], []
        for d, m in zip(r["documents"][0], r["metadatas"][0]):
            parts.append(f"[{m['src']}, p.{m['page']}]\n{d}")
            srcs.append({"src": m["src"], "page": m["page"], "text": d[:300]})
        return "\n\n".join(parts), srcs
    except Exception as e:
        st.toast("Material search failed, answering without materials." if is_busy(e)
                 else f"Search error: {str(e)[:100]}")
        return "", []


# ======================= PROFİL VƏ YADDAŞ =======================
def load_text(path, default=""):
    try:
        with open(path, encoding="utf-8") as f:
            return f.read()
    except Exception:
        return default


def load_mem(key):
    return load_text(f"memory/{key}.json", "No notes yet.")


def build_system(key, mode):
    base = load_text(f"profiles/{key}.md", DEFAULT_GEN if key == "gen" else "You are a helpful tutor.")
    return (f"{base}\n\n{MODES.get(mode, '')}\n\n{RULES}\n\n"
            f"STUDENT MEMORY:\n{load_mem(key)}")


def build_msgs(hist, q, ctx):
    msgs = [{"role": m["role"], "content": m["content"]} for m in hist[-10:]]
    while msgs and msgs[0]["role"] != "user":
        msgs = msgs[1:]
    msgs.append({"role": "user", "content": f"MATERIALS:\n{ctx or '(none)'}\n\nSTUDENT: {q}"})
    return msgs


# ======================= SÖHBƏTLƏR (fayllarda) =======================
def chat_dir(key):
    p = os.path.join("chats", key)
    os.makedirs(p, exist_ok=True)
    return p


def new_chat_id():
    return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:4]


def chat_path(key, cid):
    return os.path.join(chat_dir(key), cid + ".json")


def load_chat(key, cid):
    return read_json(chat_path(key, cid), None)


def save_chat(key, chat):
    chat["updated"] = time.time()
    path = chat_path(key, chat["id"])
    tmp = path + ".tmp"
    try:
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(chat, f, ensure_ascii=False)
        os.replace(tmp, path)
    except Exception as e:
        st.toast(f"Save error: {e}")


def list_chats(key):
    out = []
    for fn in os.listdir(chat_dir(key)):
        if not fn.endswith(".json"):
            continue
        c = load_chat(key, fn[:-5])
        if c:
            out.append({"id": c["id"], "title": c.get("title") or "...", "updated": c.get("updated", 0)})
    return sorted(out, key=lambda x: x["updated"], reverse=True)


def cb_open(cid):
    st.session_state.cid = cid


def cb_new():
    st.session_state.cid = None


def cb_delete(key, cid):
    try:
        os.remove(chat_path(key, cid))
    except Exception:
        pass
    if st.session_state.cid == cid:
        st.session_state.cid = None


def show_web_sources(urls):
    if urls:
        with st.expander(t("web_sources")):
            st.markdown("\n".join(f"- {u}" for u in urls))


# ======================= SƏS =======================
def pick_voice(text, key):
    if key in EN_SUBJ:
        return EN_VOICE
    if key in AZ_SUBJ:
        return AZ_VOICE
    return AZ_VOICE if re.search(r"[əğıöüçşƏĞİÖÜÇŞ]", text) else EN_VOICE


def speak(text, key):
    """(audio_bytes, error) qaytarır."""
    try:
        import asyncio
        import edge_tts
    except ImportError:
        return None, "MISSING"
    clean = re.sub(r"```.*?```", " ", text, flags=re.S)
    clean = re.sub(r"[*#`_>|\[\]]", "", clean)[:1500]
    if not clean.strip():
        return None, "empty text"
    voice = pick_voice(clean, key)

    async def go():
        buf = b""
        async for ch in edge_tts.Communicate(clean, voice).stream():
            if ch["type"] == "audio":
                buf += ch["data"]
        return buf

    try:
        data = asyncio.run(asyncio.wait_for(go(), timeout=40))
        return (data, None) if data else (None, "no audio received")
    except Exception as e:
        return None, str(e)[:200]


def show_audio(data, err, autoplay=True, where=st):
    if data:
        where.audio(data, format="audio/mp3", autoplay=autoplay)
    elif err == "MISSING":
        where.warning(t("tts_missing"))
    else:
        where.warning(t("tts_err") + str(err))


def transcribe(audio_bytes, key):
    lang = "en" if key in EN_SUBJ else ("az" if key in AZ_SUBJ else None)
    g = openai_client("groq")
    if g is not None:
        try:
            count_call("groq")
            kw = dict(file=("speech.wav", audio_bytes), model=GROQ_STT, response_format="text")
            if lang:
                kw["language"] = lang
            r = g.audio.transcriptions.create(**kw)
            text = r if isinstance(r, str) else getattr(r, "text", "")
            if text and text.strip():
                return text.strip()
        except Exception:
            pass  # Gemini ilə yenidən cəhd edirik
    lang_name = {"en": "English", "az": "Azerbaijani"}.get(lang, "the spoken language")
    last = None
    for attempt in range(2):
        try:
            count_call("gemini")
            r = client.models.generate_content(
                model=resolve_model("gemini"),
                contents=[types.Part.from_bytes(data=audio_bytes, mime_type="audio/wav"),
                          f"Transcribe this speech exactly. Language: {lang_name}. Output only the transcript."])
            return (r.text or "").strip()
        except Exception as e:
            last = e
            if not is_busy(e):
                break
            time.sleep(4)
    if last:
        raise last
    return ""


# ======================= KOD LABORATORİYASI =======================
def run_python(code):
    env = {k: v for k, v in os.environ.items()
           if not any(w in k.upper() for w in ("KEY", "TOKEN", "SECRET"))}
    env["PYTHONIOENCODING"] = "utf-8"
    with tempfile.TemporaryDirectory() as d:
        try:
            p = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True,
                               encoding="utf-8", errors="replace", timeout=15, cwd=d, env=env)
            return p.stdout, p.stderr
        except subprocess.TimeoutExpired:
            return "", "Timeout: more than 15 seconds."


def run_sql(setup, query):
    con = sqlite3.connect(":memory:")
    try:
        if setup.strip():
            con.executescript(setup)
        return pd.read_sql_query(query, con), None
    except Exception as e:
        return None, str(e)
    finally:
        con.close()


PY_DEFAULT = '''# Kvadratlar cədvəli
for n in range(1, 6):
    print(n, "->", n * n)
'''
SQL_SETUP = '''CREATE TABLE students(id INTEGER PRIMARY KEY, name TEXT, course TEXT, score INTEGER);
INSERT INTO students(name, course, score) VALUES
 ('Aysel', 'Math', 91), ('Elvin', 'Math', 78),
 ('Aysel', 'English', 85), ('Elvin', 'English', 88);
'''
SQL_QUERY = "SELECT name, AVG(score) AS avg_score\nFROM students GROUP BY name;"


# ======================= YAN PANEL =======================
st.sidebar.title("🎓 Tutor Komandam")
st.sidebar.radio(
    "🌐", ["az", "en"], key="ui", horizontal=True,
    format_func=lambda x: {"az": "Azərbaycanca", "en": "English"}[x])
page = st.sidebar.radio(
    "page", ["tutor", "lab"], label_visibility="collapsed",
    format_func=lambda k: t("page_" + k))

avail_ids = [p for p in PROVIDERS if available(p)]
choice = st.sidebar.selectbox(
    t("provider"), ["auto", "smart"] + avail_ids,
    format_func=lambda k: t("p_auto") if k == "auto" else (t("p_smart") if k == "smart" else provider_label(k)))
web_on = st.sidebar.toggle(t("web"), value=False)

if page == "tutor":
    key = st.sidebar.selectbox(t("subject"), SUBJ_KEYS, format_func=subj_name)
    mode = st.sidebar.radio(t("mode"), ["learn", "practice", "exam"], format_func=lambda k: t("m_" + k))
    verify = st.sidebar.toggle(t("verify"), value=False)
    speak_on = st.sidebar.toggle(t("speak"), value=False)
    voice_in = st.sidebar.toggle(t("voice"), value=False)
    if st.sidebar.button(t("voice_test")):
        d_, e_ = speak(t("voice_test_text"), key)
        show_audio(d_, e_, True, st.sidebar)
    list_box = st.sidebar.container()
else:
    key = "rtp"
    mode = "learn"
    list_box = None

# ======================= TUTOR SƏHİFƏSİ =======================
if page == "tutor":
    if st.session_state.get("cur_key") != key:
        st.session_state.cur_key = key
        st.session_state.cid = None

    chat = load_chat(key, st.session_state.cid) if st.session_state.cid else None
    if chat is None:
        st.session_state.cid = None
        chat = {"id": new_chat_id(), "title": "", "updated": 0, "messages": []}

    st.title(subj_name(key))

    for i, m in enumerate(chat["messages"]):
        with st.chat_message(m["role"]):
            st.markdown(m["content"])
            if m.get("by"):
                st.caption(f"🤖 {m['by']}")
            if m.get("sources"):
                with st.expander(t("sources")):
                    for s in m["sources"]:
                        st.caption(f"**{s['src']}**, {t('page_word')} {s['page']}")
                        st.text(s["text"])
            show_web_sources(m.get("web"))
            if m["role"] == "assistant":
                if st.button("🔊", key=f"spk_{chat['id']}_{i}", help=t("read")):
                    d_, e_ = speak(m["content"], key)
                    show_audio(d_, e_, True)

    q = st.chat_input(t("ask_ph"))

    if voice_in:
        with st.expander(t("mic"), expanded=True):
            audio = st.audio_input(t("mic_hint"), key=f"mic_{st.session_state.mic_n}")
        if audio is not None:
            raw = audio.getvalue()
            h = hashlib.md5(raw).hexdigest()
            if h != st.session_state.get("last_audio"):
                st.session_state.last_audio = h
                try:
                    with st.spinner(t("transcribing")):
                        spoken = transcribe(raw, key)
                    if spoken:
                        q = q or spoken
                    else:
                        st.warning(t("mic_empty"))
                except Exception as e:
                    st.error(friendly(e))
                st.session_state.mic_n += 1

    if q:
        ctx, srcs = retrieve(key, q)
        system = build_system(key, mode)
        msgs = build_msgs(chat["messages"], q, ctx)
        plan = choose_plan(choice, q, web_on)
        with st.chat_message("user"):
            st.markdown(q)
        answer = None
        by = ""
        web_urls = []
        with st.chat_message("assistant"):
            try:
                if verify:
                    with st.spinner(t("verifying")):
                        draft = ask_msgs(system, msgs, plan, 0.3)
                    vmsgs = [{"role": "user",
                              "content": f"MATERIALS:\n{ctx}\n\nQUESTION: {q}\n\nDRAFT:\n{draft}"}]
                    answer = st.write_stream(
                        stream_answer(VERIFY_SYS + "\n\nTUTOR RULES:\n" + system, vmsgs,
                                      free_plan() or plan, 0.1))
                else:
                    answer = st.write_stream(stream_answer(system, msgs, plan, 0.3))
            except Exception as e:
                st.error(friendly(e))
            if answer:
                by = used_label(st.session_state.get("used", ""))
                st.caption(f"🤖 {t('answered')}: {by}")
                web_urls = list(st.session_state.get("web_sources", []))
                show_web_sources(web_urls)
                if srcs:
                    with st.expander(t("sources")):
                        for s in srcs:
                            st.caption(f"**{s['src']}**, {t('page_word')} {s['page']}")
                            st.text(s["text"])
                if speak_on:
                    d_, e_ = speak(answer, key)
                    show_audio(d_, e_, True)
        if answer:
            if not chat["title"]:
                chat["title"] = re.sub(r"\s+", " ", q).strip()[:40]
            chat["messages"].append({"role": "user", "content": q})
            chat["messages"].append({"role": "assistant", "content": answer, "sources": srcs,
                                     "web": web_urls, "by": f"{t('answered')}: {by}"})
            save_chat(key, chat)
            st.session_state.cid = chat["id"]

    # ---- yan paneldə söhbət siyahısı və yaddaş (cavabdan sonra çəkilir ki, yeni söhbət dərhal görünsün)
    with list_box:
        st.subheader(t("chats"))
        wide(st.button, t("new_chat"), key="new_chat_btn", on_click=cb_new)
        chats = list_chats(key)
        if not chats:
            st.caption(t("no_chats"))
        for c in chats[:40]:
            c1, c2 = st.columns([5, 1])
            label = ("● " if c["id"] == st.session_state.cid else "") + c["title"]
            with c1:
                wide(st.button, label, key=f"open_{c['id']}", on_click=cb_open, args=(c["id"],))
            with c2:
                st.button("🗑", key=f"del_{c['id']}", help=t("delete"), on_click=cb_delete, args=(key, c["id"]))

        st.divider()
        if st.button(t("save_mem")) and chat["messages"]:
            convo = "\n".join(f"{m['role']}: {m['content']}" for m in chat["messages"][-30:])
            try:
                raw = ask_msgs(
                    "Return ONLY valid JSON with keys: weak_topics (list), common_mistakes (list), "
                    "strengths (list), next_steps (list), last_session_summary (string). Merge the OLD "
                    "memory with this conversation, keep it concise, write values in Azerbaijani.",
                    [{"role": "user", "content": f"OLD:\n{load_mem(key)}\n\nCONVERSATION:\n{convo}"}],
                    free_plan(), 0.0)
                mt = re.search(r"\{.*\}", raw, flags=re.S)
                try:
                    data = json.loads(mt.group(0)) if mt else {"notes": raw}
                except Exception:
                    data = {"notes": raw}
                with open(f"memory/{key}.json", "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                st.success(t("mem_ok"))
            except Exception as e:
                st.error(friendly(e))
        with st.expander(t("my_mem")):
            raw_mem = load_mem(key)
            try:
                st.json(json.loads(raw_mem))
            except Exception:
                st.text(raw_mem)

# ======================= KOD LABORATORİYASI SƏHİFƏSİ =======================
else:
    st.title(t("lab_title"))
    lang = st.radio(t("lab_lang"), ["Python", "SQL"], horizontal=True)

    if lang == "Python":
        code = st.text_area(t("py_code"), PY_DEFAULT, height=280, key="py_code")
        if st.button(t("run")):
            out, err = run_python(code)
            st.session_state.lab = {"lang": "Python", "code": code, "out": out, "err": err, "df": None}
    else:
        setup = st.text_area(t("sql_setup"), SQL_SETUP, height=160, key="sql_setup")
        query = st.text_area(t("sql_query"), SQL_QUERY, height=120, key="sql_query")
        if st.button(t("run")):
            df, err = run_sql(setup, query)
            st.session_state.lab = {"lang": "SQL", "code": f"{setup}\n\n{query}",
                                    "df": df, "err": err, "out": ""}

    lab = st.session_state.get("lab")
    if lab and lab["lang"] == lang:
        if lab.get("err"):
            st.error(lab["err"])
        if lab.get("out"):
            st.code(lab["out"])
        if lab.get("df") is not None:
            wide(st.dataframe, lab["df"])
            result_text = lab["df"].head(20).to_string()
        else:
            result_text = lab.get("out", "")

        if st.button(t("feedback")):
            prompt = (f"The student ran this {lab['lang']} code.\n\nCODE:\n{lab['code']}\n\n"
                      f"OUTPUT:\n{result_text}\n\nERROR:\n{lab.get('err') or '(none)'}\n\n"
                      "Follow the tutor rules: first explain what happened. If there is an error, give a HINT "
                      "(help level 1-2), not the full fix. If the code works, suggest one improvement and ask "
                      "one question about it. Answer in Azerbaijani.")
            try:
                st.write_stream(stream_answer(build_system("rtp", "learn"),
                                              [{"role": "user", "content": prompt}],
                                              free_plan() or choose_plan(choice, prompt, False), 0.3))
            except Exception as e:
                st.error(friendly(e))

# ======================= YAN PANELİN ALTI =======================
st.sidebar.divider()
with st.sidebar.expander(t("providers")):
    u_now = _usage()
    for pid, cfg in PROVIDERS.items():
        if not os.getenv(cfg["env"]):
            st.caption(f"❌ {cfg['label']} ({t('key_missing')}: {cfg['env']})")
        elif not available(pid):
            st.caption(f"⚠️ {cfg['label']} ({t('pkg_missing')})")
        else:
            cap = daily_cap(pid)
            extra = f" ({u_now.get(pid, 0)}/{cap})" if cap is not None else ""
            st.caption(f"✅ {provider_label(pid)} → {resolve_model(pid)}{extra}")
u = _usage()
st.sidebar.caption(t("usage") + ": " + ", ".join(f"{k} {v}" for k, v in u.items() if k != "date"))
st.sidebar.caption(t("theme_note"))