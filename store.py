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


# ---------------------------- yerli saxlama ----------------------------
class LocalStore:
    kind = "local"
    email = "local"
    username = "local"
    user_id = "local"

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

    # ---- hesabı silmək (bütün data cascade ilə silinir)
    def delete_account(self):
        self._db().rpc("delete_my_account", {}).execute()