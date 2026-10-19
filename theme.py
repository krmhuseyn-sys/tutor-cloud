"""Tutor Komandam: görünüş (temalar, animasiyalar).

Yalnız CSS və kiçik HTML parçaları yaradır. Streamlit-dən asılı deyil, ona görə ayrıca yoxlana bilər.
Heç bir məlumat toplamır, xarici skript işlətmir (yalnız Google Fonts şriftləri).
"""

DEFAULT_THEME = "teal"

# dark: tema tünddürsə True. Seçicilər və qaranlıq/işıqlı sistem rejimindən asılı olmayaraq rənglər tam təyin olunur.
THEMES = {
    "teal": dict(
        az="Akademik", en="Academic", dark=False,
        bg="#F6F3EA", bg2="#E6F0EC", surface="#FFFFFF", surface2="#F0EEE6",
        text="#16302B", muted="#566B66", accent="#0F766E", on_accent="#FFFFFF", accent2="#C9892B",
        border="rgba(22,48,43,0.16)", head="'Fraunces', Georgia, serif",
    ),
    "forest": dict(
        az="Meşə", en="Forest", dark=True,
        bg="#0C1A17", bg2="#10261F", surface="#14231F", surface2="#1A2E29",
        text="#E4EFEB", muted="#9DB5AE", accent="#34D3A0", on_accent="#05261C", accent2="#E9B44C",
        border="rgba(228,239,235,0.16)", head="'Fraunces', Georgia, serif",
    ),
    "midnight": dict(
        az="Gecə", en="Midnight", dark=True,
        bg="#0A0F1F", bg2="#14173A", surface="#121A33", surface2="#192244",
        text="#E7EBF8", muted="#9AA6C9", accent="#7C93FF", on_accent="#0A1030", accent2="#22D3EE",
        border="rgba(231,235,248,0.16)", head="'Space Grotesk', 'Inter', sans-serif",
    ),
    "paper": dict(
        az="Kağız", en="Paper", dark=False,
        bg="#FFFFFF", bg2="#F3F4F8", surface="#F6F6F8", surface2="#ECEDF2",
        text="#1B1C20", muted="#60636E", accent="#2F5BEA", on_accent="#FFFFFF", accent2="#E8590C",
        border="rgba(27,28,32,0.14)", head="'Inter', sans-serif",
    ),
    "sunset": dict(
        az="Gün batımı", en="Sunset", dark=False,
        bg="#FFF4EA", bg2="#FCE5F0", surface="#FFFFFF", surface2="#FFEDE0",
        text="#3A1F2B", muted="#7D5A68", accent="#D6336C", on_accent="#FFFFFF", accent2="#F08C00",
        border="rgba(58,31,43,0.16)", head="'Poppins', 'Inter', sans-serif",
    ),
}
ORDER = ["teal", "forest", "midnight", "paper", "sunset"]


def valid_theme(name):
    return name if name in THEMES else DEFAULT_THEME


def label(name, lang="az"):
    return THEMES[valid_theme(name)].get(lang, THEMES[valid_theme(name)]["en"])


def swatch(name):
    """Seçim üçün kiçik rəng önizləməsi (xarici resursu olmayan HTML)."""
    p = THEMES[valid_theme(name)]
    return (
        f'<div class="tk-swatch" style="background:linear-gradient(135deg,{p["bg"]},{p["bg2"]});'
        f'border-color:{p["border"]}"><span style="background:{p["accent"]}"></span>'
        f'<span style="background:{p["accent2"]}"></span>'
        f'<span style="background:{p["surface"]};border:1px solid {p["border"]}"></span></div>'
    )


def swatch_row(selected, lang="az"):
    """Qeydiyyatda bütün temaların önizləməsi (seçilmiş olan çərçivə ilə)."""
    cards = []
    for k in ORDER:
        p = THEMES[k]
        on = " on" if k == valid_theme(selected) else ""
        cards.append(
            f'<div class="tk-sw{on}"><div class="tk-swatch" style="background:linear-gradient(135deg,{p["bg"]},{p["bg2"]});'
            f'border-color:{p["border"]}"><span style="background:{p["accent"]}"></span>'
            f'<span style="background:{p["accent2"]}"></span>'
            f'<span style="background:{p["surface"]};border:1px solid {p["border"]}"></span></div>'
            f'<small>{label(k, lang)}</small></div>')
    return '<div class="tk-swrow">' + "".join(cards) + "</div>"


def hero(title, subtitle=""):
    sub = f'<p class="tk-sub">{subtitle}</p>' if subtitle else ""
    return f'<div class="tk-hero"><div class="tk-logo">🎓</div><h1 class="tk-title">{title}</h1>{sub}</div>'


FONTS = (
    "@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,500;9..144,700"
    "&family=Inter:wght@400;500;600&family=Poppins:wght@500;600&family=Space+Grotesk:wght@500;700&display=swap');"
)


def css(name, force_motion=False):
    p = THEMES[valid_theme(name)]
    scheme = "dark" if p["dark"] else "light"
    shadow = "0 8px 30px rgba(0,0,0,0.35)" if p["dark"] else "0 8px 28px rgba(20,30,40,0.10)"
    glow = "0 0 0 3px color-mix(in srgb, var(--tk-accent) 28%, transparent)"
    line = f"color-mix(in srgb, {p['accent']} 62%, #000)" if not p["dark"] else f"color-mix(in srgb, {p['accent']} 78%, {p['bg']})"
    reduce_block = "" if force_motion else """
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after { animation:none !important; transition:none !important; }
}"""
    return f"""
<style>
{FONTS}
:root {{
  --tk-bg:{p["bg"]}; --tk-bg2:{p["bg2"]}; --tk-surface:{p["surface"]}; --tk-surface2:{p["surface2"]};
  --tk-text:{p["text"]}; --tk-muted:{p["muted"]}; --tk-accent:{p["accent"]}; --tk-on:{p["on_accent"]};
  --tk-accent2:{p["accent2"]}; --tk-border:{p["border"]}; --tk-head:{p["head"]};
  --tk-shadow:{shadow}; --tk-radius:14px; --tk-line:{line};
  color-scheme:{scheme};
  accent-color:{p["accent"]};
}}

/* ---------- ümumi fon və mətn ---------- */
html, body {{ background:var(--tk-bg) !important; }}
html, body, .stApp {{
  color:var(--tk-text) !important;
  font-family:'Inter', system-ui, -apple-system, 'Segoe UI', sans-serif !important;
}}
[data-testid="stAppViewContainer"], [data-testid="stMain"], [data-testid="stMainBlockContainer"],
section.main, .main, [data-testid="stApp"] > div {{ background:transparent !important; }}
.stApp {{
  isolation:isolate;
  background:
    radial-gradient(1200px 600px at 12% -10%, color-mix(in srgb, var(--tk-accent) 14%, transparent), transparent 60%),
    radial-gradient(900px 500px at 100% 0%, color-mix(in srgb, var(--tk-accent2) 12%, transparent), transparent 55%),
    linear-gradient(180deg, var(--tk-bg), var(--tk-bg2)) !important;
  background-attachment:fixed !important;
}}
[data-testid="stHeader"] {{ background:transparent !important; }}
[data-testid="stBottom"], [data-testid="stBottom"] > div, [data-testid="stBottomBlockContainer"] {{
  background:transparent !important;
}}
.stApp p, .stApp li, .stApp label, .stApp span, .stApp summary,
.stApp [data-testid="stMarkdownContainer"], .stApp [data-testid="stWidgetLabel"] * {{
  color:var(--tk-text);
}}
.stApp h1, .stApp h2, .stApp h3, .stApp h4 {{
  font-family:var(--tk-head) !important; color:var(--tk-text) !important; letter-spacing:-0.01em;
}}
.stApp [data-testid="stCaptionContainer"], .stApp [data-testid="stCaptionContainer"] * ,
.stApp small {{ color:var(--tk-muted) !important; }}
.stApp a {{ color:var(--tk-accent) !important; }}
.stApp hr {{ border-color:var(--tk-border) !important; }}
.stApp code {{ background:var(--tk-surface2) !important; color:var(--tk-text) !important; border-radius:6px; }}

/* ---------- yan panel ---------- */
[data-testid="stSidebar"] {{
  background:color-mix(in srgb, var(--tk-surface) 92%, transparent) !important;
  border-right:1px solid var(--tk-border);
  backdrop-filter:blur(8px);
}}
[data-testid="stSidebar"] [data-testid="stSidebarContent"] {{ background:transparent !important; }}

/* ---------- düymələr ---------- */
.stApp button[data-testid^="stBaseButton"] {{
  background:var(--tk-surface) !important; color:var(--tk-text) !important;
  border:1px solid var(--tk-border) !important; border-radius:12px !important;
  transition:transform .18s ease, box-shadow .18s ease, border-color .18s ease, background .18s ease;
}}
.stApp button[data-testid^="stBaseButton"] * {{ color:inherit !important; }}
.stApp button[data-testid^="stBaseButton"]:hover {{
  transform:translateY(-1px); border-color:var(--tk-accent) !important; box-shadow:var(--tk-shadow);
}}
.stApp button[data-testid^="stBaseButton"]:active {{ transform:translateY(0) scale(.98); }}
.stApp button[data-testid="stBaseButton-primary"],
.stApp button[data-testid="stBaseButton-primaryFormSubmit"],
.stApp button[data-testid="stBaseButton-secondaryFormSubmit"] {{
  background:var(--tk-accent) !important; color:var(--tk-on) !important; border-color:transparent !important;
  font-weight:600;
}}
.stApp button[data-testid="stBaseButton-primary"] *,
.stApp button[data-testid="stBaseButton-primaryFormSubmit"] *,
.stApp button[data-testid="stBaseButton-secondaryFormSubmit"] * {{ color:var(--tk-on) !important; }}

/* ---------- daxiletmə sahələri ----------
   Fon və çərçivə yalnız xarici qatda; daxili qatların hamısı şəffaf (Streamlit onlara ayrıca açıq fon verir). */
.stApp div[data-baseweb="input"], .stApp div[data-baseweb="textarea"], .stApp div[data-baseweb="select"] {{
  background:var(--tk-surface) !important; border:2px solid var(--tk-line) !important;
  border-radius:12px !important; transition:box-shadow .18s ease, border-color .18s ease;
}}
.stApp div[data-baseweb="input"] *, .stApp div[data-baseweb="textarea"] *, .stApp div[data-baseweb="select"] *,
.stApp div[data-baseweb="input"], .stApp div[data-baseweb="select"] > div {{
  background-color:transparent !important; border-color:transparent !important; box-shadow:none !important;
}}
.stApp div[data-baseweb="input"], .stApp div[data-baseweb="textarea"], .stApp div[data-baseweb="select"] {{
  background-color:var(--tk-surface) !important; border-color:var(--tk-line) !important;
}}
.stApp input, .stApp textarea, .stApp div[data-baseweb="select"] * {{
  color:var(--tk-text) !important; -webkit-text-fill-color:var(--tk-text) !important;
}}
.stApp input::placeholder, .stApp textarea::placeholder {{ color:var(--tk-muted) !important; -webkit-text-fill-color:var(--tk-muted) !important; opacity:.8; }}
.stApp div[data-baseweb="input"]:focus-within, .stApp div[data-baseweb="textarea"]:focus-within,
.stApp div[data-baseweb="select"]:focus-within {{
  border-color:var(--tk-accent) !important; box-shadow:{glow} !important;
}}
.stApp [data-baseweb="select"] svg, .stApp [data-baseweb="input"] svg {{ fill:var(--tk-muted) !important; color:var(--tk-muted) !important; }}
/* ---------- Streamlit-in yeni quruluşu (data-baseweb atributları yoxdur) ----------
   Xana = mətn sahəsinin/inputun kök elementi və ya seçimin içində birbaşa <input> olan div. */
.stApp [data-testid="stTextAreaRootElement"], .stApp [data-testid="stTextInputRootElement"],
.stApp [data-testid="stNumberInputContainer"], .stApp [data-testid="stDateInputRootElement"],
.stApp [data-testid="stSelectbox"] div:has(> input), .stApp [data-testid="stMultiSelect"] div:has(> input) {{
  background:var(--tk-surface) !important; background-color:var(--tk-surface) !important;
  border:2px solid var(--tk-line) !important; border-radius:12px !important;
  transition:box-shadow .18s ease, border-color .18s ease;
}}
.stApp [data-testid="stTextAreaRootElement"] *, .stApp [data-testid="stTextInputRootElement"] *,
.stApp [data-testid="stNumberInputContainer"] *, .stApp [data-testid="stDateInputRootElement"] *,
.stApp [data-testid="stSelectbox"] div, .stApp [data-testid="stMultiSelect"] div {{
  background:transparent !important; background-color:transparent !important; box-shadow:none !important;
}}
.stApp [data-testid="stSelectbox"] div, .stApp [data-testid="stMultiSelect"] div,
.stApp [data-testid="stTextAreaRootElement"] *, .stApp [data-testid="stTextInputRootElement"] * {{
  color:var(--tk-text) !important; -webkit-text-fill-color:var(--tk-text) !important;
}}
.stApp [data-testid="stTextAreaRootElement"]:focus-within, .stApp [data-testid="stTextInputRootElement"]:focus-within,
.stApp [data-testid="stNumberInputContainer"]:focus-within,
.stApp [data-testid="stSelectbox"] div:has(> input):focus-within,
.stApp [data-testid="stMultiSelect"] div:has(> input):focus-within {{
  border-color:var(--tk-accent) !important; box-shadow:{glow} !important;
}}
.stApp [data-testid="stSelectbox"] svg, .stApp [data-testid="stMultiSelect"] svg,
.stApp [data-testid="stTextInputRootElement"] svg {{ fill:var(--tk-muted) !important; color:var(--tk-muted) !important; }}
.stApp [data-testid="stSelectbox"] button, .stApp [data-testid="stMultiSelect"] button {{
  background:transparent !important; border:0 !important;
}}
/* tarix sahəsi: quruluşdan asılı olmayaraq oxunaqlı (açıq fonda açıq mətn olmasın) */
.stApp [data-testid="stDateInput"] input, .stApp [data-testid="stDateInput"] span,
.stApp [data-testid="stDateInput"] div {{
  background:transparent !important; background-color:transparent !important;
  color:var(--tk-text) !important; -webkit-text-fill-color:var(--tk-text) !important; box-shadow:none !important;
}}
.stApp [data-testid="stDateInput"] > div:not([data-testid="stWidgetLabel"]) {{
  background:var(--tk-surface) !important; border:2px solid var(--tk-line) !important; border-radius:12px !important;
}}
.stApp [data-testid="stDateInput"] > div:not([data-testid="stWidgetLabel"]):focus-within {{
  border-color:var(--tk-accent) !important; box-shadow:{glow} !important;
}}
.stApp [data-testid="stDateInput"] svg {{ fill:var(--tk-muted) !important; color:var(--tk-muted) !important; }}

/* açılan siyahı: BaseWeb olmasa da role="listbox" ilə tapılır */
[role="listbox"], [data-testid="stSelectboxVirtualDropdown"],
div:has(> [role="listbox"]), div:has(> div > [role="listbox"]) {{
  background:var(--tk-surface) !important; color:var(--tk-text) !important;
}}
[role="listbox"] [role="option"], [role="listbox"] li, [role="listbox"] * {{
  background:transparent !important; color:var(--tk-text) !important;
}}
[role="listbox"] [role="option"]:hover, [role="listbox"] [aria-selected="true"], [role="listbox"] li:hover {{
  background:color-mix(in srgb, var(--tk-accent) 14%, transparent) !important;
}}

/* açılan siyahılar (portal içində) */
[data-baseweb="popover"] > div, [data-baseweb="popover"] [data-baseweb="menu"], [data-baseweb="popover"] ul {{
  background:var(--tk-surface) !important; color:var(--tk-text) !important;
  border:1px solid var(--tk-border); border-radius:12px !important; box-shadow:var(--tk-shadow);
}}
[data-baseweb="popover"] li, [data-baseweb="popover"] li * {{ color:var(--tk-text) !important; }}
[data-baseweb="popover"] li:hover, [data-baseweb="popover"] [aria-selected="true"] {{
  background:var(--tk-surface2) !important;
}}

/* ---------- söhbət ---------- */
[data-testid="stChatMessage"] {{
  background:var(--tk-surface) !important; border:1px solid var(--tk-border);
  border-radius:18px !important; padding:14px 16px !important; margin-bottom:10px;
  box-shadow:0 1px 0 rgba(0,0,0,0.02);
  animation:tk-rise .45s cubic-bezier(.2,.7,.2,1) both;
}}
[data-testid="stChatMessage"]:has([data-testid="stChatMessageAvatarUser"]) {{
  background:color-mix(in srgb, var(--tk-accent) 9%, var(--tk-surface)) !important;
}}
.stApp div[data-testid="stChatInput"] {{
  background:var(--tk-surface) !important; border:2px solid var(--tk-line) !important;
  border-radius:20px !important; box-shadow:var(--tk-shadow); transition:box-shadow .2s, border-color .2s;
}}
.stApp div[data-testid="stChatInput"]:focus-within {{ border-color:var(--tk-accent) !important; box-shadow:{glow}, var(--tk-shadow); }}
.stApp [data-testid="stChatInput"] div, .stApp [data-testid="stChatInput"] textarea,
.stApp [data-testid="stChatInput"] [data-baseweb] {{
  background:transparent !important; background-color:transparent !important; border-color:transparent !important;
  box-shadow:none !important; color:var(--tk-text) !important; -webkit-text-fill-color:var(--tk-text) !important;
}}
.stApp [data-testid="stChatInput"] textarea::placeholder {{ color:var(--tk-muted) !important; -webkit-text-fill-color:var(--tk-muted) !important; }}
.stApp [data-testid="stChatInput"] button {{ background:var(--tk-accent) !important; border-radius:12px !important; }}
.stApp [data-testid="stChatInput"] button svg {{ fill:var(--tk-on) !important; color:var(--tk-on) !important; }}

/* ---------- panellər, sekmələr, forma ---------- */
[data-testid="stExpander"] details, [data-testid="stForm"] {{
  background:var(--tk-surface) !important; border:1px solid var(--tk-border) !important;
  border-radius:var(--tk-radius) !important;
}}
.stApp [data-testid="stExpander"] summary, .stApp [data-testid="stExpander"] details[open] > summary,
.stApp [data-testid="stExpander"] summary:hover, .stApp [data-testid="stExpander"] summary:focus,
.stApp [data-testid="stExpanderDetails"] {{
  background:transparent !important; color:var(--tk-text) !important;
}}
.stApp [data-testid="stExpander"] summary * {{ color:var(--tk-text) !important; }}
.stApp [data-testid="stExpander"] summary svg {{ fill:var(--tk-muted) !important; color:var(--tk-muted) !important; }}
.stApp [data-testid="stExpander"] summary:hover {{ background:color-mix(in srgb, var(--tk-accent) 8%, transparent) !important; }}
.stApp [data-baseweb="tab"] {{ color:var(--tk-muted) !important; font-weight:500; }}
.stApp [data-baseweb="tab"][aria-selected="true"] {{ color:var(--tk-accent) !important; }}
.stApp [data-baseweb="tab-highlight"] {{ background:var(--tk-accent) !important; height:3px !important; border-radius:3px; }}
.stApp [data-baseweb="tab-border"] {{ background:var(--tk-border) !important; }}
[data-testid="stAlert"] {{ border-radius:var(--tk-radius) !important; }}
.stApp [data-testid="stRadio"] [role="radiogroup"] label {{ transition:transform .15s ease; }}
.stApp [data-testid="stRadio"] [role="radiogroup"] label:hover {{ transform:translateX(2px); }}
/* radio dairələri: seçilməyən = boş halqa, seçilən = tema rəngində dolu + içində nöqtə */
.stApp [data-testid="stRadio"] label > div:first-of-type {{
  background:transparent !important; background-color:transparent !important;
  border:2px solid var(--tk-muted) !important; border-radius:50% !important; box-sizing:border-box !important;
}}
.stApp [data-testid="stRadio"] label:has(input:checked) > div:first-of-type {{
  background:var(--tk-accent) !important; background-color:var(--tk-accent) !important; border-color:var(--tk-accent) !important;
}}
.stApp [data-testid="stRadio"] label:has(input:checked) > div:first-of-type > div {{
  background:var(--tk-on) !important; background-color:var(--tk-on) !important;
}}
.stApp [data-testid="stRadio"] label:hover > div:first-of-type {{ border-color:var(--tk-accent) !important; }}

/* ---------- giriş / açılış səhifəsi ---------- */
.tk-hero {{ text-align:center; padding:28px 0 10px; animation:tk-rise .6s cubic-bezier(.2,.7,.2,1) both; }}
.tk-logo {{
  font-size:46px; line-height:1; display:inline-block; animation:tk-float 5s ease-in-out infinite;
  filter:drop-shadow(0 8px 14px color-mix(in srgb, var(--tk-accent) 40%, transparent));
}}
.stApp h1.tk-title {{
  margin:10px 0 4px; font-size:clamp(28px, 6vw, 44px); font-weight:700; padding:0;
  background:linear-gradient(100deg, var(--tk-text) 0%, var(--tk-accent) 45%, var(--tk-accent2) 75%, var(--tk-text) 100%);
  background-size:220% 100%; -webkit-background-clip:text; background-clip:text;
  color:transparent !important; -webkit-text-fill-color:transparent;
  animation:tk-shine 9s ease-in-out infinite;
}}
.tk-sub {{ color:var(--tk-muted) !important; margin:0 0 6px; font-size:15px; }}

/* tema seçimi önizləməsi */
.tk-swatch {{
  display:flex; gap:6px; align-items:center; padding:10px; border-radius:14px; border:1px solid;
  height:46px; margin:2px 0 8px; animation:tk-rise .4s ease both;
}}
.tk-swatch span {{ width:22px; height:22px; border-radius:50%; display:inline-block; }}

.tk-swrow {{ display:flex; flex-wrap:wrap; gap:10px; margin:4px 0 6px; }}
.tk-sw {{ text-align:center; flex:1 1 90px; max-width:130px; }}
.tk-sw small {{ display:block; color:var(--tk-muted) !important; font-size:12px; margin-top:-2px; }}
.tk-sw.on .tk-swatch {{ outline:2px solid var(--tk-accent); outline-offset:2px; transform:translateY(-2px); }}
.tk-sw .tk-swatch {{ transition:transform .2s ease, outline-color .2s ease; justify-content:center; }}

/* bildiriş, kod və JSON blokları: tünd temada da oxunsun */
[data-testid="stToast"], [data-testid="stToast"] > div, [data-testid="stTooltipContent"] {{
  background:var(--tk-surface) !important; color:var(--tk-text) !important; border:1px solid var(--tk-border);
  border-radius:12px !important;
}}
.stApp pre, .stApp [data-testid="stCode"], .stApp [data-testid="stJson"], .stApp [data-testid="stText"] {{
  background:var(--tk-surface2) !important; color:var(--tk-text) !important; border-radius:12px;
}}
.stApp [data-testid="stCode"] * , .stApp [data-testid="stJson"] * {{ color:var(--tk-text); }}

/* yumşaq fon hərəkəti: iki rəngli ləkə (yüngül, GPU ilə) */
.stApp::before, .stApp::after {{
  content:""; position:fixed; z-index:-1; pointer-events:none; border-radius:50%;
  width:52vmax; height:52vmax; opacity:.9; will-change:transform;
}}
.stApp::before {{
  top:-18vmax; left:-14vmax;
  background:radial-gradient(circle, color-mix(in srgb, var(--tk-accent) 50%, transparent), transparent 66%);
  animation:tk-drift-a 11s ease-in-out infinite alternate;
}}
.stApp::after {{
  bottom:-22vmax; right:-16vmax;
  background:radial-gradient(circle, color-mix(in srgb, var(--tk-accent2) 48%, transparent), transparent 66%);
  animation:tk-drift-b 14s ease-in-out infinite alternate;
}}

@keyframes tk-rise {{ from {{ opacity:0; transform:translateY(10px); }} to {{ opacity:1; transform:none; }} }}
@keyframes tk-float {{ 0%,100% {{ transform:translateY(0) rotate(-3deg); }} 50% {{ transform:translateY(-7px) rotate(3deg); }} }}
@keyframes tk-shine {{ 0%,100% {{ background-position:0% 50%; }} 50% {{ background-position:100% 50%; }} }}
@keyframes tk-drift-a {{ from {{ transform:translate(0,0) scale(1); }} to {{ transform:translate(34vmax,24vmax) scale(1.35); }} }}
@keyframes tk-drift-b {{ from {{ transform:translate(0,0) scale(1); }} to {{ transform:translate(-32vmax,-22vmax) scale(1.4); }} }}

/* üzən işıq nöqtələri: yuxarı qalxan hissəciklər */
[data-testid="stAppViewContainer"]::before {{
  content:""; position:fixed; inset:0; z-index:0; pointer-events:none; opacity:.85;
  background-image:
    radial-gradient(circle, var(--tk-accent) 0 3px, transparent 4px),
    radial-gradient(circle, var(--tk-accent2) 0 4px, transparent 5px),
    radial-gradient(circle, var(--tk-accent) 0 2px, transparent 3px);
  background-size:230px 230px, 340px 340px, 150px 150px;
  background-position:20px 40px, 130px 200px, 70px 90px;
  animation:tk-particles 28s linear infinite;
  -webkit-mask-image:linear-gradient(180deg, transparent 0, #000 25%, #000 75%, transparent 100%);
  mask-image:linear-gradient(180deg, transparent 0, #000 25%, #000 75%, transparent 100%);
  opacity:.35;
}}
@keyframes tk-particles {{
  from {{ background-position:20px 40px, 130px 200px, 70px 90px; }}
  to   {{ background-position:60px -190px, 90px -140px, 110px -60px; }}
}}

/* düymələr: qalxma + parıltı */
.stApp .stButton > button, .stApp .stDownloadButton > button, .stApp [data-testid="stFormSubmitButton"] > button {{
  transition:transform .18s ease, box-shadow .18s ease, filter .18s ease; position:relative; overflow:hidden;
}}
.stApp .stButton > button:hover, .stApp .stDownloadButton > button:hover, .stApp [data-testid="stFormSubmitButton"] > button:hover {{
  transform:translateY(-3px) scale(1.02); box-shadow:0 10px 24px color-mix(in srgb, var(--tk-accent) 38%, transparent); filter:brightness(1.06);
}}
.stApp .stButton > button:active {{ transform:translateY(0) scale(.98); }}
.stApp .stButton > button[kind="primary"], .stApp [data-testid="stFormSubmitButton"] > button[kind="primaryFormSubmit"] {{
  background:linear-gradient(100deg, var(--tk-accent), var(--tk-accent2), var(--tk-accent)) !important;
  background-size:220% 100% !important; animation:tk-shine 6s ease-in-out infinite;
}}

/* mesajlar: yumşaq sıçrayış, loqo parıltısı */
[data-testid="stChatMessage"] {{ animation:tk-pop .55s cubic-bezier(.2,.9,.25,1.15) both !important; }}
@keyframes tk-pop {{ 0% {{ opacity:0; transform:translateY(18px) scale(.97); }} 100% {{ opacity:1; transform:none; }} }}
.tk-logo {{ animation:tk-float 4s ease-in-out infinite, tk-pulse 3s ease-in-out infinite !important; }}
@keyframes tk-pulse {{ 0%,100% {{ filter:drop-shadow(0 6px 10px color-mix(in srgb, var(--tk-accent) 30%, transparent)); }}
  50% {{ filter:drop-shadow(0 12px 26px color-mix(in srgb, var(--tk-accent) 75%, transparent)); }} }}
[data-testid="stSidebar"] .stSelectbox, [data-testid="stSidebar"] [data-testid="stExpander"] {{ transition:transform .2s ease; }}
[data-testid="stSidebar"] [data-testid="stExpander"]:hover {{ transform:translateX(3px); }}
[data-testid="stChatMessage"]:hover {{ box-shadow:0 8px 22px color-mix(in srgb, var(--tk-accent) 18%, transparent); transition:box-shadow .25s; }}

/* söhbət xanası: ətrafında axan işıq */
@property --tk-ang {{ syntax:"<angle>"; initial-value:0deg; inherits:false; }}
.stApp div[data-testid="stChatInput"] {{
  border:2.5px solid transparent !important;
  background:
    linear-gradient(var(--tk-surface), var(--tk-surface)) padding-box,
    conic-gradient(from var(--tk-ang), transparent 0deg, var(--tk-accent) 50deg, var(--tk-accent2) 110deg, transparent 170deg,
      transparent 190deg, var(--tk-accent2) 240deg, var(--tk-accent) 300deg, transparent 360deg) border-box !important;
  animation:tk-spin 4.5s linear infinite;
  box-shadow:0 0 18px color-mix(in srgb, var(--tk-accent) 35%, transparent), var(--tk-shadow) !important;
}}
.stApp div[data-testid="stChatInput"]:focus-within {{
  animation-duration:2.2s;
  box-shadow:0 0 30px color-mix(in srgb, var(--tk-accent) 60%, transparent), var(--tk-shadow) !important;
}}
@keyframes tk-spin {{ to {{ --tk-ang:360deg; }} }}

/* + əlavə düyməsi: sual xanasının içində, ən solda, yumru, temanın rəngində */
[data-testid="stBottom"] [data-testid="stHorizontalBlock"] {{ position:relative; flex-wrap:nowrap !important; }}
[data-testid="stBottom"] [data-testid="stColumn"]:first-child, [data-testid="stBottom"] [data-testid="column"]:first-child {{
  position:absolute !important; left:9px; bottom:7px; width:42px !important; min-width:42px !important;
  flex:none !important; z-index:20;
}}
[data-testid="stBottom"] [data-testid="stColumn"]:nth-child(2), [data-testid="stBottom"] [data-testid="column"]:nth-child(2) {{
  flex:1 1 100% !important; width:100% !important; min-width:0 !important;
}}
[data-testid="stBottom"] [data-testid="stChatInput"] textarea {{ padding-left:54px !important; }}
[data-testid="stBottom"] [data-testid="stColumn"]:first-child button, [data-testid="stBottom"] [data-testid="column"]:first-child button {{
  width:42px !important; min-width:42px !important; height:42px !important; min-height:42px !important; padding:0 !important;
  border-radius:50% !important; border:none !important;
  background:linear-gradient(135deg, var(--tk-accent), var(--tk-accent2)) !important;
  color:var(--tk-on) !important; font-size:26px !important; font-weight:600 !important; line-height:1 !important;
  box-shadow:0 0 14px color-mix(in srgb, var(--tk-accent) 45%, transparent);
  transition:transform .25s ease, box-shadow .2s ease;
}}
[data-testid="stBottom"] [data-testid="stColumn"]:first-child button *, [data-testid="stBottom"] [data-testid="column"]:first-child button * {{
  color:var(--tk-on) !important; font-size:26px !important; line-height:1 !important; margin:0 !important;
}}
[data-testid="stBottom"] [data-testid="stColumn"]:first-child button svg, [data-testid="stBottom"] [data-testid="column"]:first-child button svg {{ display:none !important; }}
[data-testid="stBottom"] [data-testid="stColumn"]:first-child button:hover, [data-testid="stBottom"] [data-testid="column"]:first-child button:hover {{
  transform:rotate(90deg) scale(1.06); box-shadow:0 0 24px color-mix(in srgb, var(--tk-accent) 70%, transparent);
}}
[data-testid="stPopoverBody"] {{
  background:var(--tk-surface) !important; color:var(--tk-text) !important;
  border:1px solid var(--tk-border) !important; border-radius:16px !important; box-shadow:var(--tk-shadow);
}}
[data-testid="stPopoverBody"] * {{ color:var(--tk-text); }}
[data-testid="stFileUploaderDropzone"] {{
  background:var(--tk-surface2) !important; border:2px dashed var(--tk-line) !important; border-radius:14px !important;
}}
[data-testid="stFileUploaderDropzone"] * {{ color:var(--tk-text) !important; }}
[data-testid="stFileUploaderDropzone"] button {{ background:var(--tk-accent) !important; color:var(--tk-on) !important; border:none !important; }}
[data-testid="stFileUploaderDropzone"] button * {{ color:var(--tk-on) !important; }}
[data-testid="stCameraInput"] {{ border-radius:14px; overflow:hidden; border:2px solid var(--tk-line); }}
[data-testid="stCameraInput"] button {{ background:var(--tk-accent) !important; color:var(--tk-on) !important; border:none !important; }}
[data-testid="stCameraInput"] button * {{ color:var(--tk-on) !important; }}

{reduce_block}
@media (max-width: 640px) {{
  .stApp::before, .stApp::after {{ opacity:.7; }}
  [data-testid="stChatMessage"] {{ border-radius:16px !important; padding:12px 13px !important; }}
}}
</style>
"""