"""Saxlama qatı (Streamlit-dən asılı deyil).

LocalStore    : yerli fayllar, tək istifadəçi, giriş yoxdur (kompüterdə işləmə).
SupabaseStore : hər istifadəçinin datası Supabase-də, satır səviyyəli qoruma (RLS) ilə.
Giriş yalnız SUPABASE_URL və SUPABASE_ANON_KEY təyin olunanda aktivləşir.
"""
import os, re, json, uuid, datetime

try:
    from supabase import create_client
except ImportError:  # paket quraşdırılmayıb
    create_client = None

USERNAME_RE = re.compile(r"^[a-z0-9_]{3,20}$")
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
CHAT_ID_RE = re.compile(r"^[A-Za-z0-9_\-]+$")
RESERVED = {"admin", "administrator", "root", "support", "system", "moderator", "owner", "tutor", "null", "none"}


# ---------------------------- mesaj şifrələməsi ----------------------------
# Mesajlar bazaya AES-256-GCM ilə şifrələnmiş yazılır. Açar yalnız Streamlit Secrets / .env-dəki MSG_KEY-dir
# (Supabase-də yoxdur). Hər mesajın öz təsadüfi nonce-u var; açar hər söhbət üçün ayrıca törədilir və söhbət
# nömrəsi də doğrulanır (şifrəli mətni başqa söhbətə köçürmək olmur). MSG_KEY_PREV açarı dəyişəndə köhnə mesajları oxumaq üçündür.
try:
    from cryptography.hazmat.primitives.ciphers.aead import AESGCM
    from cryptography.hazmat.primitives.kdf.hkdf import HKDF
    from cryptography.hazmat.primitives import hashes as _hashes
except Exception:  # noqa
    AESGCM = None

import base64 as _b64


class MsgKeyMissing(Exception):
    pass


def _msg_master(name):
    raw = (os.getenv(name, "") or "").strip()
    return raw.encode("utf-8") if len(raw) >= 24 else None


def _msg_conv_key(master, conv):
    return HKDF(algorithm=_hashes.SHA256(), length=32, salt=b"tutor-msg-v1", info=str(conv).encode("utf-8")).derive(master)


def msg_key_ok():
    return AESGCM is not None and _msg_master("MSG_KEY") is not None


def msg_encrypt(conv, text):
    master = _msg_master("MSG_KEY")
    if AESGCM is None or master is None:
        raise MsgKeyMissing("MSG_KEY")
    nonce = os.urandom(12)
    ct = AESGCM(_msg_conv_key(master, conv)).encrypt(nonce, str(text).encode("utf-8"), str(conv).encode("utf-8"))
    return "v1:" + _b64.urlsafe_b64encode(nonce + ct).decode("ascii")


def msg_decrypt(conv, blob):
    """Şifrəli mətni açır. 'v1:' ilə başlamayan mətn (kimsə API-ni birbaşa çağırıbsa) olduğu kimi, amma təmiz mətn kimi qaytarılır."""
    blob = str(blob or "")
    if not blob.startswith("v1:"):
        return blob
    if AESGCM is None:
        return "[?]"
    try:
        raw = _b64.urlsafe_b64decode(blob[3:].encode("ascii"))
    except Exception:
        return "[?]"
    for name in ("MSG_KEY", "MSG_KEY_PREV"):
        master = _msg_master(name)
        if master is None:
            continue
        try:
            return AESGCM(_msg_conv_key(master, conv)).decrypt(raw[:12], raw[12:], str(conv).encode("utf-8")).decode("utf-8")
        except Exception:
            continue
    return "[?]"


class SessionExpired(Exception):
    """Giriş sessiyası bitib, yenidən daxil olmaq lazımdır."""


# ---------------------------- köməkçilər ----------------------------
def now_iso():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()


def baku_today():
    """Bakı vaxtı ilə bu günün tarixi (UTC+4)."""
    return (datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=4)).date().isoformat()


def valid_username(name):
    return bool(USERNAME_RE.match(name or "")) and name not in RESERVED


def valid_email(email):
    return bool(EMAIL_RE.match(email or "")) and len(email) <= 254


def email_domain_ok(email):
    """ALLOWED_EMAIL_DOMAINS (vergüllə) təyin olunubsa, yalnız həmin domenlərə icazə verir."""
    allowed = [d.strip().lower() for d in os.getenv("ALLOWED_EMAIL_DOMAINS", "").split(",") if d.strip()]
    if not allowed:
        return True
    return email.rsplit("@", 1)[-1].lower() in allowed


def password_problem(pw):
    """Problem varsa səbəbi, yoxdursa None qaytarır."""
    if len(pw or "") < 8:
        return "short"
    if len(pw) > 128:
        return "long"
    if not re.search(r"[A-Za-z]", pw) or not re.search(r"\d", pw):
        return "weak"
    return None


def auth_enabled():
    return create_client is not None and bool(os.getenv("SUPABASE_URL")) and bool(os.getenv("SUPABASE_ANON_KEY"))


def make_client():
    """Hər brauzer sessiyası üçün ayrı müştəri (paylaşılmır, çünki içində istifadəçinin sessiyası var)."""
    return create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_ANON_KEY"))


def invite_required():
    """Sahib Supabase-də dəvət kodu təyin edibsə True (qeydiyyat zamanı çağırılır, giriş tələb etmir)."""
    try:
        res = make_client().rpc("invite_required", {}).execute()
        return bool(res.data)
    except Exception:
        return False


def check_invite(code):
    """Supabase-dəki dəvət kodunu yoxlayır. Server 10 dəqiqədə həddindən çox cəhdi rədd edir."""
    try:
        res = make_client().rpc("check_invite", {"p_code": (code or "").strip()[:100]}).execute()
        return bool(res.data)
    except Exception:
        return False


NOTE_CHUNK, NOTE_MAX_CHUNKS, NOTE_MAX_FILES = 800, 800, 12


def note_chunks_from_text(text, size=NOTE_CHUNK, overlap=100):
    """Mətni üst-üstə düşən parçalara bölür (şəxsi qeydlər üçün)."""
    text = re.sub(r"[ \t]+", " ", (text or "").replace("\r", "")).strip()
    out, i = [], 0
    while i < len(text):
        piece = text[i:i + size].strip()
        if len(piece) > 30:
            out.append(piece)
        i += size - overlap
    return out


def owner_emails():
    return {e.strip().lower() for e in os.getenv("OWNER_EMAILS", "").split(",") if e.strip()}


# ---------------------------- kartlar: aralıq təkrar ----------------------------
CARD_FRONT_MAX, CARD_BACK_MAX, CARD_LIMIT = 500, 1500, 1500


def add_days(iso_day, n):
    return (datetime.date.fromisoformat(iso_day) + datetime.timedelta(days=int(n))).isoformat()


def norm_front(text):
    return re.sub(r"\s+", " ", (text or "").strip().lower())


def clean_card(c):
    """Kartı yoxlayır və təmizləyir; yararsızdırsa None."""
    front = str(c.get("front", "")).strip()[:CARD_FRONT_MAX]
    back = str(c.get("back", "")).strip()[:CARD_BACK_MAX]
    if len(front) < 3 or len(back) < 2:
        return None
    try:
        page = int(c["page"]) if c.get("page") is not None else None
    except Exception:
        page = None
    return {"front": front, "back": back, "src": str(c.get("src") or "")[:200], "page": page}


DEFAULT_GOAL = 10  # gündəlik hədəf: kart təkrarı sayı (0 = söndürülü)


def find_in_chat(title, messages, query):
    """Söhbətdə sorğunu axtarır (hərf böyüklüyünə və ə/e kimi fərqlərə həssas deyil). Tapılsa qısa kontekst qaytarır."""
    import hybrid
    q = hybrid.fold(query).strip()
    if not q:
        return None
    if q in hybrid.fold(title):
        return title or ""
    for m in messages or []:
        txt = (m.get("content") if isinstance(m, dict) else str(m)) or ""
        i = hybrid.fold(txt).find(q)
        if i >= 0:
            a = max(0, i - 30)
            return ("…" if a else "") + txt[a:i + len(q) + 70].replace("\n", " ")
    return None


def schedule(card, grade, today=None):
    """SM-2 tipli sadə cədvəl. grade: 0 Yenidən, 1 Çətin, 2 Yaxşı, 3 Asan. Yenilənən sahələri qaytarır."""
    today = today or baku_today()
    ease = float(card.get("ease") or 2.5)
    interval = int(card.get("interval_days") or 0)
    reps = int(card.get("reps") or 0)
    lapses = int(card.get("lapses") or 0)
    if grade <= 0:
        lapses += 1
        reps = 0
        interval = 0
        ease = max(1.3, ease - 0.2)
        due = today
    else:
        if grade == 1:
            interval = max(1, round(interval * 1.2)) if reps else 1
            ease = max(1.3, ease - 0.15)
        elif grade == 2:
            interval = 1 if reps == 0 else (3 if reps == 1 else max(interval + 1, round(interval * ease)))
        else:
            interval = 3 if reps == 0 else max(interval + 2, round(max(interval, 1) * ease * 1.3))
            ease = min(3.0, ease + 0.15)
        reps += 1
        interval = min(interval, 365)
        due = add_days(today, interval)
    return {"ease": round(ease, 2), "interval_days": interval, "reps": reps, "lapses": lapses, "due": due}


def streak(activity, today=None):
    """Ardıcıl aktiv gün sayı. activity: {gün: {"reviews": n, "questions": m}}.
    Bu gün hələ aktivlik yoxdursa, seriya dünən başlayır (seriya bu gün itmir)."""
    today = today or baku_today()
    def active(day):
        a = activity.get(day) or {}
        return (a.get("reviews", 0) + a.get("questions", 0)) > 0
    day = today if active(today) else add_days(today, -1)
    n = 0
    while active(day) and n < 400:
        n += 1
        day = add_days(day, -1)
    return n


def longest_streak(activity):
    """Bütün tarixçədə ən uzun ardıcıl aktiv gün sayı."""
    days = sorted(d for d, a in activity.items() if (a.get("reviews", 0) + a.get("questions", 0)) > 0)
    best = run = 0
    prev = None
    for d in days:
        run = run + 1 if prev is not None and add_days(prev, 1) == d else 1
        best = max(best, run)
        prev = d
    return best


# ---------------------------- dəftər / sınaq imtahanı ----------------------------
SAVED_MAX = 500          # dəftərdə ən çox cavab (bütün fənlər)
SAMPLES_MAX = 8          # hər fənn üçün ən çox imtahan nümunəsi
SAMPLE_MAX_CHARS = 30000


def _clean_sources(sources):
    """Mənbələrdən yalnız lazım olan sahələr (ölçü kiçik qalsın)."""
    out = []
    for x in list(sources or [])[:12]:
        if isinstance(x, dict):
            out.append({"src": str(x.get("src", ""))[:120], "page": x.get("page"),
                        "text": str(x.get("text", ""))[:300], "note": bool(x.get("note"))})
    return out


def _local_subjects(base, folder):
    d = os.path.join(base, folder)
    try:
        return [f[:-5] for f in os.listdir(d) if f.endswith(".json")]
    except Exception:
        return []


# ---------------------------- yerli saxlama ----------------------------
class LocalStore:
    kind = "local"
    email = "local"
    username = "local"
    user_id = "local"
    msg_enabled = False  # mesajlaşma yalnız Supabase ilə (hesablar lazımdır)

    def __init__(self, base="."):
        self.base = base

    def _chat_dir(self, key):
        p = os.path.join(self.base, "chats", key)
        os.makedirs(p, exist_ok=True)
        return p

    def new_chat_id(self):
        return datetime.datetime.now().strftime("%Y%m%d%H%M%S") + "_" + uuid.uuid4().hex[:4]

    def _chat_path(self, key, cid):
        return os.path.join(self._chat_dir(key), cid + ".json")

    def load_chat(self, key, cid):
        if not cid or not CHAT_ID_RE.match(cid):
            return None
        try:
            with open(self._chat_path(key, cid), encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            return None

    def save_chat(self, key, chat):
        chat["updated"] = datetime.datetime.now().timestamp()
        path = self._chat_path(key, chat["id"])
        tmp = path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(chat, f, ensure_ascii=False)
        os.replace(tmp, path)

    def list_chats(self, key):
        out = []
        for fn in os.listdir(self._chat_dir(key)):
            if not fn.endswith(".json"):
                continue
            c = self.load_chat(key, fn[:-5])
            if c:
                out.append({"id": c["id"], "title": c.get("title") or "...", "updated": c.get("updated", 0)})
        return sorted(out, key=lambda x: x["updated"], reverse=True)[:40]

    def search_chats(self, key, query, limit=15):
        out = []
        for c in self.list_chats_full(key):
            snip = find_in_chat(c.get("title"), c.get("messages"), query)
            if snip is not None:
                out.append({"id": c["id"], "title": c.get("title") or "...", "snippet": snip})
            if len(out) >= limit:
                break
        return out

    def list_chats_full(self, key):
        rows = []
        for fn in os.listdir(self._chat_dir(key)):
            if fn.endswith(".json"):
                c = self.load_chat(key, fn[:-5])
                if c:
                    rows.append(c)
        return sorted(rows, key=lambda x: x.get("updated", 0), reverse=True)

    def delete_chat(self, key, cid):
        if cid and CHAT_ID_RE.match(cid):
            try:
                os.remove(self._chat_path(key, cid))
            except Exception:
                pass

    def load_mem(self, key):
        try:
            with open(os.path.join(self.base, "memory", f"{key}.json"), encoding="utf-8") as f:
                return f.read()
        except Exception:
            return "No notes yet."

    def save_mem(self, key, data):
        os.makedirs(os.path.join(self.base, "memory"), exist_ok=True)
        with open(os.path.join(self.base, "memory", f"{key}.json"), "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def get_about(self):
        return ""

    def usage_today(self):
        return {}

    def bump(self, provider):
        return None

    # ---- kartlar
    def _cards_path(self, key):
        os.makedirs(os.path.join(self.base, "cards"), exist_ok=True)
        return os.path.join(self.base, "cards", f"{key}.json")

    def _cards_load(self, key):
        try:
            with open(self._cards_path(key), encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, list) else []
        except Exception:
            return []

    def _cards_save(self, key, rows):
        path = self._cards_path(key)
        with open(path + ".tmp", "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        os.replace(path + ".tmp", path)

    def add_cards(self, key, cards):
        rows = self._cards_load(key)
        seen = {norm_front(r.get("front")) for r in rows}
        added = 0
        for c in cards or []:
            c = clean_card(c)
            if not c or norm_front(c["front"]) in seen or len(rows) >= CARD_LIMIT:
                continue
            seen.add(norm_front(c["front"]))
            rows.append({**c, "id": uuid.uuid4().hex, "ease": 2.5, "interval_days": 0, "reps": 0,
                         "lapses": 0, "due": baku_today(), "created": now_iso()})
            added += 1
        if added:
            self._cards_save(key, rows)
        return added

    def card_counts(self, key):
        rows, today = self._cards_load(key), baku_today()
        return {"total": len(rows), "due": sum(1 for r in rows if r.get("due", today) <= today)}

    def due_cards(self, key, limit=20):
        today = baku_today()
        rows = [r for r in self._cards_load(key) if r.get("due", today) <= today]
        return sorted(rows, key=lambda r: r.get("due", ""))[:limit]

    def list_cards(self, key, limit=100):
        return sorted(self._cards_load(key), key=lambda r: r.get("created", ""), reverse=True)[:limit]

    def review_card(self, key, card, grade):
        rows, new = self._cards_load(key), schedule(card, grade)
        for r in rows:
            if r.get("id") == card.get("id"):
                r.update(new)
        self._cards_save(key, rows)
        return new

    def delete_card(self, key, card_id):
        rows = [r for r in self._cards_load(key) if r.get("id") != card_id]
        self._cards_save(key, rows)

    # ---- panel (yerli)
    def _log_path(self):
        os.makedirs(os.path.join(self.base, "cards"), exist_ok=True)
        return os.path.join(self.base, "cards", "_log.json")

    def bump_review(self, subject):
        try:
            with open(self._log_path(), encoding="utf-8") as f:
                log = json.load(f)
        except Exception:
            log = {}
        day = log.setdefault(baku_today(), {})
        day[subject] = day.get(subject, 0) + 1
        with open(self._log_path(), "w", encoding="utf-8") as f:
            json.dump(log, f)

    def card_stats(self):
        rows = []
        folder = os.path.join(self.base, "cards")
        if not os.path.isdir(folder):
            return rows
        for fn in os.listdir(folder):
            if fn.endswith(".json") and not fn.startswith("_"):
                for r in self._cards_load(fn[:-5]):
                    rows.append({**{k: r.get(k) for k in ("interval_days", "reps", "lapses", "ease", "due", "front")},
                                 "subject": fn[:-5]})
        return rows

    def activity(self, days=14):
        try:
            with open(self._log_path(), encoding="utf-8") as f:
                log = json.load(f)
        except Exception:
            log = {}
        return {d: {"reviews": sum(v.values()), "questions": 0} for d, v in log.items()}

    def _prefs_path(self):
        os.makedirs(os.path.join(self.base, "cards"), exist_ok=True)
        return os.path.join(self.base, "cards", "_prefs.json")

    def get_prefs(self):
        try:
            with open(self._prefs_path(), encoding="utf-8") as f:
                p = json.load(f)
            return p if isinstance(p, dict) else {}
        except Exception:
            return {}

    def set_prefs(self, prefs):
        try:
            if len(json.dumps(prefs, ensure_ascii=False)) > 60000:
                return False
            with open(self._prefs_path(), "w", encoding="utf-8") as f:
                json.dump(prefs, f, ensure_ascii=False)
            return True
        except Exception:
            return False

    def _goal_path(self):
        os.makedirs(os.path.join(self.base, "cards"), exist_ok=True)
        return os.path.join(self.base, "cards", "_goal.json")

    def get_goal(self):
        try:
            with open(self._goal_path(), encoding="utf-8") as f:
                return max(0, min(200, int(json.load(f).get("goal", DEFAULT_GOAL))))
        except Exception:
            return DEFAULT_GOAL

    def set_goal(self, n):
        try:
            with open(self._goal_path(), "w", encoding="utf-8") as f:
                json.dump({"goal": max(0, min(200, int(n)))}, f)
            return True
        except Exception:
            return False

    # ---- 👍/👎 rəy (yerli: cards/_feedback.json)
    def _fb_path(self):
        os.makedirs(os.path.join(self.base, "cards"), exist_ok=True)
        return os.path.join(self.base, "cards", "_feedback.json")

    def _fb_load(self):
        try:
            with open(self._fb_path(), encoding="utf-8") as f:
                rows = json.load(f)
            return rows if isinstance(rows, list) else []
        except Exception:
            return []

    def get_feedback(self, key, cid):
        return {r["idx"]: r["rating"] for r in self._fb_load()
                if r.get("subject") == key and r.get("chat_id") == cid and r.get("rating") in (1, -1)}

    def set_feedback(self, key, cid, idx, rating, question="", answer=""):
        rows = [r for r in self._fb_load()
                if not (r.get("subject") == key and r.get("chat_id") == cid and r.get("idx") == idx)]
        if rating in (1, -1):
            rows.append({"subject": key, "chat_id": cid, "idx": idx, "rating": rating,
                         "question": (question or "")[:200], "answer": (answer or "")[:400], "created": now_iso()})
        try:
            with open(self._fb_path(), "w", encoding="utf-8") as f:
                json.dump(rows[-500:], f, ensure_ascii=False)
            return True
        except Exception:
            return False

    def owner_feedback(self, limit=20):
        rows = self._fb_load()
        down = [r for r in rows if r.get("rating") == -1][-limit:][::-1]
        return {"up": sum(1 for r in rows if r.get("rating") == 1), "down": sum(1 for r in rows if r.get("rating") == -1),
                "recent": [{"subject": r.get("subject"), "question": r.get("question"), "answer": r.get("answer"),
                            "created_at": r.get("created")} for r in down]}

    def owner_overview(self, days=7):
        return None

    # ---- şəxsi qeydlər (yerli: notes/<fənn>.json)
    def _notes_path(self, key):
        os.makedirs(os.path.join(self.base, "notes"), exist_ok=True)
        return os.path.join(self.base, "notes", f"{key}.json")

    def _notes_load(self, key):
        try:
            with open(self._notes_path(key), encoding="utf-8") as f:
                rows = json.load(f)
            return rows if isinstance(rows, list) else []
        except Exception:
            return []

    def add_notes(self, key, name, chunks):
        """Eyni adlı faylı əvəz edir. Qaytarır: yazılan parça sayı (limit aşılırsa -1)."""
        name = str(name)[:120]
        rows = [r for r in self._notes_load(key) if r.get("name") != name]
        if len({r.get("name") for r in rows}) >= NOTE_MAX_FILES:
            return -1
        room = NOTE_MAX_CHUNKS - len(rows)
        if room <= 0:
            return -1
        chunks = list(chunks)[:room]
        rows += [{"name": name, "idx": i, "text": c} for i, c in enumerate(chunks)]
        with open(self._notes_path(key), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        return len(chunks)

    def list_note_files(self, key):
        out = {}
        for r in self._notes_load(key):
            out[r["name"]] = out.get(r["name"], 0) + 1
        return [{"name": k, "chunks": v} for k, v in out.items()]

    def note_chunks(self, key):
        return self._notes_load(key)

    def delete_note_file(self, key, name):
        rows = [r for r in self._notes_load(key) if r.get("name") != name]
        with open(self._notes_path(key), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)

    # ---- dəftər (saxlanmış cavablar) və sınaq imtahanı nümunələri
    def _json_path(self, folder, key):
        os.makedirs(os.path.join(self.base, folder), exist_ok=True)
        return os.path.join(self.base, folder, f"{key}.json")

    def _json_load(self, folder, key):
        try:
            with open(self._json_path(folder, key), encoding="utf-8") as f:
                rows = json.load(f)
            return rows if isinstance(rows, list) else []
        except Exception:
            return []

    def _json_save(self, folder, key, rows):
        with open(self._json_path(folder, key), "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)

    def saved_list(self, key):
        return sorted(self._json_load("saved", key), key=lambda r: r.get("created_at", ""), reverse=True)

    def saved_add(self, key, chat_id, idx, question, answer, sources=None):
        rows = self._json_load("saved", key)
        if any(r.get("chat_id") == chat_id and r.get("idx") == idx for r in rows):
            return "dup"
        total = sum(len(self._json_load("saved", k)) for k in _local_subjects(self.base, "saved"))
        if total >= SAVED_MAX:
            return -1
        row = {"id": uuid.uuid4().hex, "subject": key, "chat_id": str(chat_id)[:80], "idx": int(idx),
               "question": str(question or "")[:2000], "answer": str(answer)[:20000],
               "sources": _clean_sources(sources), "note": "",
               "created_at": datetime.datetime.now(datetime.timezone.utc).isoformat()}
        rows.append(row)
        self._json_save("saved", key, rows)
        return row["id"]

    def saved_delete(self, key, item_id):
        self._json_save("saved", key, [r for r in self._json_load("saved", key) if r.get("id") != item_id])

    def saved_delete_at(self, key, chat_id, idx):
        self._json_save("saved", key, [r for r in self._json_load("saved", key)
                                       if not (r.get("chat_id") == chat_id and r.get("idx") == idx)])

    def saved_note(self, key, item_id, note):
        rows = self._json_load("saved", key)
        for r in rows:
            if r.get("id") == item_id:
                r["note"] = str(note or "")[:1000]
        self._json_save("saved", key, rows)

    def samples_list(self, key):
        return self._json_load("samples", key)

    def sample_add(self, key, name, text):
        name = str(name)[:120] or "sample"
        rows = [r for r in self._json_load("samples", key) if r.get("name") != name]
        if len(rows) >= SAMPLES_MAX:
            return -1
        rows.append({"name": name, "text": str(text)[:SAMPLE_MAX_CHARS]})
        self._json_save("samples", key, rows)
        return 1

    def sample_delete(self, key, name):
        self._json_save("samples", key, [r for r in self._json_load("samples", key) if r.get("name") != name])

    # ---- bloklama / dəvət kodu: yalnız Supabase rejimində mənalıdır
    def is_blocked(self):
        return False

    def chat_counts(self):
        out = {}
        base = os.path.join(self.base, "chats")
        if os.path.isdir(base):
            for k in os.listdir(base):
                p_ = os.path.join(base, k)
                if os.path.isdir(p_):
                    out[k] = len([f for f in os.listdir(p_) if f.endswith(".json")])
        return out


# ---------------------------- Supabase saxlama ----------------------------
class SupabaseStore:
    kind = "supabase"

    def __init__(self, sb, user_id, email):
        self.sb = sb
        self.user_id = user_id
        self.email = (email or "").lower()
        self.username = None

    def _db(self):
        sess = self.sb.auth.get_session()  # vaxtı keçibsə özü yeniləyir
        if sess is None:
            raise SessionExpired("login required")
        self.sb.postgrest.auth(sess.access_token)
        return self.sb

    def new_chat_id(self):
        return str(uuid.uuid4())

    @staticmethod
    def _is_uuid(value):
        try:
            uuid.UUID(str(value))
            return True
        except Exception:
            return False

    # ---- söhbətlər
    def list_chats(self, key):
        rows = (self._db().table("chats").select("id,title,updated_at").eq("subject", key)
                .order("updated_at", desc=True).limit(40).execute().data) or []
        return [{"id": r["id"], "title": r.get("title") or "...", "updated": r.get("updated_at", "")} for r in rows]

    def load_chat(self, key, cid):
        if not self._is_uuid(cid):
            return None
        rows = (self._db().table("chats").select("id,title,messages").eq("id", cid).eq("subject", key)
                .limit(1).execute().data) or []
        if not rows:
            return None
        r = rows[0]
        return {"id": r["id"], "title": r.get("title") or "", "updated": 0, "messages": r.get("messages") or []}

    def save_chat(self, key, chat):
        self._db().table("chats").upsert({
            "id": chat["id"], "user_id": self.user_id, "subject": key,
            "title": (chat.get("title") or "")[:80],
            "messages": chat["messages"][-200:],
            "updated_at": now_iso(),
        }).execute()

    def search_chats(self, key, query, limit=15):
        rows = (self._db().table("chats").select("id,title,messages").eq("subject", key)
                .order("updated_at", desc=True).limit(150).execute().data) or []
        out = []
        for r in rows:
            snip = find_in_chat(r.get("title"), r.get("messages"), query)
            if snip is not None:
                out.append({"id": r["id"], "title": r.get("title") or "...", "snippet": snip})
            if len(out) >= limit:
                break
        return out

    def delete_chat(self, key, cid):
        if self._is_uuid(cid):
            self._db().table("chats").delete().eq("id", cid).execute()

    # ---- yaddaş
    def load_mem(self, key):
        rows = (self._db().table("memory").select("data").eq("subject", key).limit(1).execute().data) or []
        return json.dumps(rows[0]["data"], ensure_ascii=False) if rows else "No notes yet."

    def save_mem(self, key, data):
        self._db().table("memory").upsert(
            {"user_id": self.user_id, "subject": key, "data": data, "updated_at": now_iso()},
            on_conflict="user_id,subject").execute()

    # ---- profil
    def get_profile(self):
        try:
            rows = (self._db().table("profiles").select("username,about,theme").eq("id", self.user_id)
                    .limit(1).execute().data) or []
        except SessionExpired:
            raise
        except Exception:  # tema sütunu hələ yaradılmayıb: köhnə sxemlə işləməyə davam et
            rows = (self._db().table("profiles").select("username,about").eq("id", self.user_id)
                    .limit(1).execute().data) or []
        return rows[0] if rows else None

    def username_available(self, name):
        res = self._db().rpc("username_available", {"p_name": name}).execute()
        return bool(res.data)

    def change_username(self, name):
        """72 saatda bir dəfə ad dəyişmə (qayda bazada yoxlanılır). Qaytarır: {'ok': bool, 'error'?, 'retry_at'?, 'next_at'?}."""
        res = self._db().rpc("change_username", {"p_name": (name or "").strip().lower()[:20]}).execute()
        return res.data if isinstance(res.data, dict) else {"ok": False, "error": "unknown"}

    def username_next_change(self):
        """Növbəti ad dəyişməsinin mümkün olduğu vaxt (ISO) və ya None."""
        res = self._db().rpc("username_next_change").execute()
        return res.data or None

    # ---- mesajlaşma (messaging.sql lazımdır; bütün qaydalar bazadakı funksiyalarda yoxlanılır)
    msg_enabled = True

    def _msg(self, fn, args=None):
        return self._db().rpc(fn, args or {}).execute().data

    def msg_ready(self):
        """messaging.sql işlədilibmi? (funksiya yoxdursa False)"""
        try:
            self._msg("msg_friends_list")
            return True
        except SessionExpired:
            raise
        except Exception:
            return False

    def msg_conversations(self):
        return self._msg("msg_conversations_list") or []

    def msg_key_ok(self):
        return msg_key_ok()

    def msg_fetch(self, conv, after=0):
        rows = self._msg("msg_fetch", {"p_conv": conv, "p_after": int(after or 0)}) or []
        for m in rows:
            m["body"] = msg_decrypt(conv, m.get("body"))
        return rows

    def msg_send(self, conv, body):
        try:
            blob = msg_encrypt(conv, (body or "")[:1000])
        except MsgKeyMissing:
            return {"ok": False, "error": "no_key"}
        r = self._msg("msg_send", {"p_conv": conv, "p_body": blob})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def msg_delete(self, mid):
        self._msg("msg_delete_message", {"p_id": int(mid)})

    def msg_create_group(self, name):
        r = self._msg("msg_create_group", {"p_name": (name or "").strip()[:30]})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def msg_join_group(self, code):
        r = self._msg("msg_join_group", {"p_code": (code or "").strip()[:20]})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def msg_leave_group(self, conv):
        self._msg("msg_leave_group", {"p_conv": conv})

    def msg_delete_group(self, conv):
        self._msg("msg_delete_group", {"p_conv": conv})

    def msg_group_remove(self, conv, username):
        self._msg("msg_group_remove", {"p_conv": conv, "p_username": (username or "").strip()[:20]})

    def msg_members(self, conv):
        return self._msg("msg_members_list", {"p_conv": conv}) or []

    def msg_friends(self):
        r = self._msg("msg_friends_list")
        return r if isinstance(r, dict) else {"friends": [], "incoming": [], "outgoing": [], "blocked": []}

    def msg_friend_request(self, username):
        r = self._msg("msg_friend_request", {"p_username": (username or "").strip().lower()[:20]})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def msg_friend_respond(self, username, accept):
        r = self._msg("msg_friend_respond", {"p_username": (username or "").strip().lower()[:20],
                                             "p_accept": bool(accept)})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def msg_friend_remove(self, username):
        self._msg("msg_friend_remove", {"p_username": (username or "").strip().lower()[:20]})

    def msg_block(self, username, flag=True):
        self._msg("msg_set_block", {"p_username": (username or "").strip().lower()[:20], "p_flag": bool(flag)})

    def msg_report(self, mid, reason=""):
        r = self._msg("msg_report", {"p_message_id": int(mid), "p_reason": (reason or "")[:300]})
        return r if isinstance(r, dict) else {"ok": False, "error": "unknown"}

    def owner_msg_reports(self):
        reps = self._msg("owner_msg_reports") or []
        for r in reps:
            for x in r.get("snapshot") or []:
                x["body"] = msg_decrypt(r.get("conversation_id"), x.get("body"))
        return reps

    def owner_security_log(self, limit=40):
        return self._msg("owner_security_log", {"p_limit": int(limit)}) or []

    def owner_msg_resolve(self, rid, action):
        r = self._msg("owner_msg_resolve", {"p_id": int(rid), "p_action": "block" if action == "block" else "dismiss"})
        return r if isinstance(r, dict) else {"ok": False}

    def create_profile(self, username, theme="teal"):
        row = {"id": self.user_id, "username": username, "theme": theme}
        try:
            self._db().table("profiles").insert(row).execute()
        except SessionExpired:
            raise
        except Exception as e:
            if "theme" not in str(e).lower():
                raise
            row.pop("theme")  # tema sütunu yoxdur: yalnız adı yaz
            self._db().table("profiles").insert(row).execute()

    def set_theme(self, theme):
        self._db().table("profiles").update({"theme": theme}).eq("id", self.user_id).execute()

    def set_about(self, text):
        self._db().table("profiles").update({"about": (text or "")[:600]}).eq("id", self.user_id).execute()

    def get_prefs(self):
        try:
            rows = (self._db().table("profiles").select("prefs").eq("id", self.user_id)
                    .limit(1).execute().data) or []
            p = rows[0].get("prefs") if rows else None
            return p if isinstance(p, dict) else {}
        except SessionExpired:
            raise
        except Exception:  # prefs sütunu hələ yaradılmayıb
            return {}

    def set_prefs(self, prefs):
        try:
            if len(json.dumps(prefs, ensure_ascii=False)) > 60000:
                return False
            self._db().table("profiles").update({"prefs": prefs}).eq("id", self.user_id).execute()
            return True
        except SessionExpired:
            raise
        except Exception:
            return False

    def get_goal(self):
        try:
            rows = (self._db().table("profiles").select("goal").eq("id", self.user_id)
                    .limit(1).execute().data) or []
            g = rows[0].get("goal") if rows else None
            return DEFAULT_GOAL if g is None else max(0, min(200, int(g)))
        except SessionExpired:
            raise
        except Exception:  # goal sütunu hələ yaradılmayıb
            return DEFAULT_GOAL

    def set_goal(self, n):
        try:
            self._db().table("profiles").update({"goal": max(0, min(200, int(n)))}).eq("id", self.user_id).execute()
            return True
        except SessionExpired:
            raise
        except Exception:
            return False

    # ---- istifadə sayğacı
    def usage_today(self):
        rows = (self._db().table("usage").select("provider,count").eq("day", baku_today()).execute().data) or []
        return {r["provider"]: r["count"] for r in rows}

    def bump(self, provider):
        self._db().rpc("bump_usage", {"p_provider": provider}).execute()


    # ---- kartlar
    def add_cards(self, key, cards):
        db = self._db()
        old = (db.table("cards").select("front").eq("subject", key).limit(2000).execute().data) or []
        if len(old) >= CARD_LIMIT:
            return 0
        seen = {norm_front(r["front"]) for r in old}
        rows = []
        for c in cards or []:
            c = clean_card(c)
            if not c or norm_front(c["front"]) in seen or len(old) + len(rows) >= CARD_LIMIT:
                continue
            seen.add(norm_front(c["front"]))
            rows.append({**c, "user_id": self.user_id, "subject": key})
        if rows:
            db.table("cards").insert(rows).execute()
        return len(rows)

    def card_counts(self, key):
        db, today = self._db(), baku_today()
        total = db.table("cards").select("id", count="exact").eq("subject", key).limit(1).execute().count or 0
        due = (db.table("cards").select("id", count="exact").eq("subject", key).lte("due", today)
               .limit(1).execute().count or 0)
        return {"total": total, "due": due}

    def due_cards(self, key, limit=20):
        return ((self._db().table("cards").select("*").eq("subject", key).lte("due", baku_today())
                 .order("due").limit(limit).execute().data) or [])

    def list_cards(self, key, limit=100):
        return ((self._db().table("cards").select("*").eq("subject", key)
                 .order("created_at", desc=True).limit(limit).execute().data) or [])

    def review_card(self, key, card, grade):
        new = schedule(card, grade)
        self._db().table("cards").update(new).eq("id", card["id"]).execute()
        return new

    def delete_card(self, key, card_id):
        if self._is_uuid(card_id):
            self._db().table("cards").delete().eq("id", card_id).execute()


    # ---- panel
    def bump_review(self, subject):
        try:
            self._db().rpc("bump_review", {"p_subject": subject}).execute()
        except SessionExpired:
            raise
        except Exception:
            pass  # jurnal cədvəli hələ yaradılmayıb: təkrarı pozma

    def card_stats(self):
        return ((self._db().table("cards").select("subject,interval_days,reps,lapses,ease,due,front")
                 .limit(3000).execute().data) or [])

    def activity(self, days=14):
        db = self._db()
        since = add_days(baku_today(), -(days - 1))
        out = {}
        try:
            for r in (db.table("review_log").select("day,count").gte("day", since).execute().data) or []:
                d = out.setdefault(r["day"], {"reviews": 0, "questions": 0})
                d["reviews"] += r["count"]
        except SessionExpired:
            raise
        except Exception:
            pass
        for r in (db.table("usage").select("day,count").eq("provider", "question").gte("day", since)
                  .execute().data) or []:
            d = out.setdefault(r["day"], {"reviews": 0, "questions": 0})
            d["questions"] += r["count"]
        return out

    # ---- 👍/👎 rəy (feedback cədvəli; feedback.sql işlədilməyibsə səssizcə işləmir)
    def get_feedback(self, key, cid):
        try:
            rows = (self._db().table("feedback").select("msg_idx,rating").eq("subject", key).eq("chat_id", str(cid))
                    .limit(500).execute().data) or []
            return {r["msg_idx"]: r["rating"] for r in rows}
        except SessionExpired:
            raise
        except Exception:
            return {}

    def set_feedback(self, key, cid, idx, rating, question="", answer=""):
        try:
            db = self._db()
            if rating in (1, -1):
                db.table("feedback").upsert(
                    {"user_id": self.user_id, "subject": key, "chat_id": str(cid), "msg_idx": int(idx),
                     "rating": int(rating), "question": (question or "")[:200], "answer": (answer or "")[:400]},
                    on_conflict="user_id,chat_id,msg_idx").execute()
            else:
                db.table("feedback").delete().eq("chat_id", str(cid)).eq("msg_idx", int(idx)).execute()
            return True
        except SessionExpired:
            raise
        except Exception:
            return False

    def owner_feedback(self, limit=20):
        """Yalnız sahib üçün (Supabase funksiyası özü yoxlayır)."""
        res = self._db().rpc("owner_feedback", {"p_limit": int(limit)}).execute()
        return res.data

    def owner_overview(self, days=7):
        """Yalnız sahib üçün (Supabase funksiyası özü yoxlayır). days: 1, 7, 28; 0 = bütün zaman."""
        res = self._db().rpc("owner_overview", {"p_days": int(days)}).execute()
        return res.data

    # ---- şəxsi qeydlər (notes cədvəli; yalnız sahibinə görünür; extras.sql lazımdır)
    def add_notes(self, key, name, chunks):
        db = self._db()
        name = str(name)[:120]
        old = (db.table("notes").select("name,idx").eq("subject", key).limit(2000).execute().data) or []
        others = [r for r in old if r.get("name") != name]
        if len({r["name"] for r in others}) >= NOTE_MAX_FILES:
            return -1
        room = NOTE_MAX_CHUNKS - len(others)
        if room <= 0:
            return -1
        chunks = list(chunks)[:room]
        db.table("notes").delete().eq("subject", key).eq("name", name).execute()
        rows = [{"user_id": self.user_id, "subject": key, "name": name, "idx": i, "text": c}
                for i, c in enumerate(chunks)]
        for i in range(0, len(rows), 100):
            db.table("notes").insert(rows[i:i + 100]).execute()
        return len(chunks)

    def list_note_files(self, key):
        rows = (self._db().table("notes").select("name").eq("subject", key).limit(2000).execute().data) or []
        out = {}
        for r in rows:
            out[r["name"]] = out.get(r["name"], 0) + 1
        return [{"name": k, "chunks": v} for k, v in out.items()]

    def note_chunks(self, key):
        return ((self._db().table("notes").select("name,idx,text").eq("subject", key)
                 .order("name").order("idx").limit(NOTE_MAX_CHUNKS).execute().data) or [])

    def delete_note_file(self, key, name):
        self._db().table("notes").delete().eq("subject", key).eq("name", str(name)).execute()

    # ---- dəftər və sınaq imtahanı nümunələri (study.sql lazımdır)
    def saved_list(self, key):
        return ((self._db().table("saved_answers").select("id,chat_id,idx,question,answer,sources,note,created_at")
                 .eq("subject", key).order("created_at", desc=True).limit(SAVED_MAX).execute().data) or [])

    def saved_add(self, key, chat_id, idx, question, answer, sources=None):
        row = {"user_id": self.user_id, "subject": key, "chat_id": str(chat_id)[:80], "idx": int(idx),
               "question": str(question or "")[:2000], "answer": str(answer)[:20000],
               "sources": _clean_sources(sources)}
        try:
            res = self._db().table("saved_answers").insert(row).execute()
        except SessionExpired:
            raise
        except Exception as e:
            low = str(e).lower()
            if "limit: saved_answers" in low:
                return -1
            if "duplicate" in low or "23505" in low or "saved_answers_one" in low:
                return "dup"
            raise
        data = res.data or []
        return data[0].get("id") if data else "ok"

    def saved_delete(self, key, item_id):
        self._db().table("saved_answers").delete().eq("id", str(item_id)).execute()

    def saved_delete_at(self, key, chat_id, idx):
        (self._db().table("saved_answers").delete().eq("subject", key).eq("chat_id", str(chat_id))
         .eq("idx", int(idx)).execute())

    def saved_note(self, key, item_id, note):
        self._db().table("saved_answers").update({"note": str(note or "")[:1000]}).eq("id", str(item_id)).execute()

    def samples_list(self, key):
        return ((self._db().table("exam_samples").select("name,text").eq("subject", key)
                 .order("created_at").limit(SAMPLES_MAX).execute().data) or [])

    def sample_add(self, key, name, text):
        name = str(name)[:120] or "sample"
        db = self._db()
        db.table("exam_samples").delete().eq("subject", key).eq("name", name).execute()
        try:
            db.table("exam_samples").insert({"user_id": self.user_id, "subject": key, "name": name,
                                             "text": str(text)[:SAMPLE_MAX_CHARS]}).execute()
        except SessionExpired:
            raise
        except Exception as e:
            if "limit: exam_samples" in str(e).lower():
                return -1
            raise
        return 1

    def sample_delete(self, key, name):
        self._db().table("exam_samples").delete().eq("subject", key).eq("name", str(name)).execute()

    # ---- bloklama (blocked_users cədvəli: istifadəçi yalnız öz sətrini oxuya bilər, yaza bilməz)
    def is_blocked(self):
        try:
            rows = (self._db().table("blocked_users").select("user_id").eq("user_id", self.user_id)
                    .limit(1).execute().data) or []
            return bool(rows)
        except SessionExpired:
            raise
        except Exception:
            return False  # cədvəl hələ yaradılmayıb

    # ---- sahib: dəvət kodu və bloklama (Supabase funksiyaları sahibliyi özü yoxlayır)
    def owner_invite_status(self):
        return bool(self._db().rpc("owner_invite_status", {}).execute().data)

    def owner_set_invite(self, code):
        """Boş mətn kodu silir (qeydiyyat sərbəst olur / env-dəki kod qüvvədədir)."""
        self._db().rpc("owner_set_invite", {"p_code": (code or "").strip()[:100]}).execute()

    def owner_set_blocked(self, username, flag):
        return self._db().rpc("owner_set_blocked", {"p_username": (username or "").strip().lower()[:20],
                                                    "p_blocked": bool(flag)}).execute().data

    def owner_blocked_list(self):
        return self._db().rpc("owner_blocked_list", {}).execute().data or []

    def chat_counts(self):
        rows = (self._db().table("chats").select("subject").limit(3000).execute().data) or []
        out = {}
        for r in rows:
            out[r["subject"]] = out.get(r["subject"], 0) + 1
        return out

    # ---- hesabı silmək (bütün data cascade ilə silinir)
    def delete_account(self):
        self._db().rpc("delete_my_account", {}).execute()