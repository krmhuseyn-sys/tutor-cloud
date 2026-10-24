"""Tətbiqi oyaq saxlayır: saytı gizli brauzerdə açır, yatıbsa "oyandır" düyməsinə basır,
tətbiq açılana qədər gözləyir. GitHub Actions hər 6 saatdan bir işlədir (.github/workflows/keepalive.yml).
Heç bir parol və ya açar istifadə etmir; giriş ekranından o tərəfə keçmir."""
import os
import re
import sys
import time

from playwright.sync_api import sync_playwright

URL = os.environ.get("APP_URL", "https://mytutor1.streamlit.app")
WAKE_RE = re.compile(r"get this app back up|wake.*up", re.I)
LOAD_TIMEOUT = 240  # saniyə: yatmış tətbiq 1-3 dəqiqəyə oyanır


def app_loaded(page):
    """Streamlit tətbiqi (bizim giriş ekranı daxil) hər hansı çərçivədə görünürmü?"""
    for fr in page.frames:
        try:
            if fr.locator('[data-testid="stApp"]').count() > 0:
                return True
        except Exception:
            pass
    return False


def click_wake(page):
    for fr in page.frames:
        try:
            btn = fr.get_by_role("button", name=WAKE_RE)
            if btn.count() > 0:
                btn.first.click()
                return True
        except Exception:
            pass
    return False


def main():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(URL, wait_until="domcontentloaded", timeout=90_000)
        woke = False
        deadline = time.time() + LOAD_TIMEOUT
        while time.time() < deadline:
            if app_loaded(page):
                break
            if not woke and click_wake(page):
                woke = True
                print("Tətbiq yatmışdı: oyandırma düyməsinə basıldı.")
            page.wait_for_timeout(3000)
        ok = app_loaded(page)
        if ok:
            page.wait_for_timeout(15_000)  # bir az açıq qalsın ki, ziyarət kimi sayılsın
        browser.close()
    if ok:
        print("Tətbiq oyaqdır" + (" (indi oyandırıldı)." if woke else "."))
        return 0
    print("XƏTA: tətbiq 4 dəqiqə ərzində açılmadı. Streamlit Cloud-da yoxla (Reboot app).")
    return 1


if __name__ == "__main__":
    sys.exit(main())