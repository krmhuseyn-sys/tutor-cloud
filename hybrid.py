"""Hibrid axtarış: açar söz (BM25) + vektor axtarışı, nəticələr RRF ilə birləşdirilir.

Vektor axtarışı mənanı tutur, amma dəqiq söz, termin, qısaltma və rəqəmləri (məsələn "SWOT", "HTTP",
"Fisher tənliyi") bəzən qaçırır. BM25 məhz bunları tapır. Hər ikisinin nəticəsi birləşdirilir.

Heç bir xarici paket lazım deyil. Həm tətbiq (app.py), həm də eval.py bunu işlədir.
"""
import math
import re

# Azərbaycan hərflərini sadələşdir: istifadəçi "ə" əvəzinə "e" yazsa da tapılsın
_FOLD = str.maketrans({
    "ə": "e", "Ə": "e", "ı": "i", "I": "i", "İ": "i", "ö": "o", "Ö": "o", "ü": "u", "Ü": "u",
    "ç": "c", "Ç": "c", "ş": "s", "Ş": "s", "ğ": "g", "Ğ": "g",
    "ә": "e", "Ә": "e", "­": "",  # OCR-dan gələn oxşar simvollar
})
_WORD = re.compile(r"\w+", re.UNICODE)
STEM = 5  # uzun sözlərin ilk 5 hərfi: "kapitalın", "kapitalda" -> "kapit" (ağlabatan şəkilçi həlli)


def fold(text):
    """Kiçik hərf + Azərbaycan hərflərinin sadələşdirilməsi (axtarış üçün)."""
    return (text or "").translate(_FOLD).lower()


def tokenize(text):
    out = []
    for w in _WORD.findall((text or "").translate(_FOLD).lower()):
        if len(w) < 2 and not w.isdigit():
            continue
        out.append(w[:STEM] if len(w) > STEM and not w.isdigit() else w)
    return out


class BM25:
    def __init__(self, ids, docs, metas, k1=1.5, b=0.75):
        self.ids, self.docs, self.metas = list(ids), list(docs), list(metas)
        self.pos = {cid: i for i, cid in enumerate(self.ids)}
        self.k1, self.b = k1, b
        self.inv = {}      # söz -> [(sənəd indeksi, tezlik)]
        self.len = []
        for i, d in enumerate(self.docs):
            toks = tokenize(d)
            self.len.append(len(toks))
            tf = {}
            for w in toks:
                tf[w] = tf.get(w, 0) + 1
            for w, c in tf.items():
                self.inv.setdefault(w, []).append((i, c))
        self.n = len(self.docs)
        self.avg = (sum(self.len) / self.n) if self.n else 1.0

    def top(self, query, k=20):
        """Ən uyğun k sənədin id-ləri (xalı olanlar), ən yaxşıdan başlayaraq."""
        scores = {}
        for w in set(tokenize(query)):
            plist = self.inv.get(w)
            if not plist:
                continue
            idf = math.log(1 + (self.n - len(plist) + 0.5) / (len(plist) + 0.5))
            for i, c in plist:
                denom = c + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg)
                scores[i] = scores.get(i, 0.0) + idf * c * (self.k1 + 1) / denom
        best = sorted(scores.items(), key=lambda x: -x[1])[:k]
        return [self.ids[i] for i, _ in best]

    def get(self, cid):
        i = self.pos.get(cid)
        return (self.docs[i], self.metas[i]) if i is not None else None


def rrf(lists, k=60, weights=None):
    """Reciprocal Rank Fusion: bir neçə sıralı siyahını birləşdirir. Qaytarır: id-lər, ən yaxşıdan."""
    weights = weights or [1.0] * len(lists)
    score = {}
    for lst, w in zip(lists, weights):
        for rank, cid in enumerate(lst, 1):
            score[cid] = score.get(cid, 0.0) + w / (k + rank)
    return [cid for cid, _ in sorted(score.items(), key=lambda x: -x[1])]


def fuse(vec_ids, bm, query, n=8, pool=20):
    """Vektor id siyahısı (ən yaxşıdan) + BM25 -> birləşmiş n id."""
    kw = bm.top(query, pool) if bm else []
    return rrf([vec_ids[:pool], kw])[:n]