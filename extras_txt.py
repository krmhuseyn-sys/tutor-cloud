"""Yeni funksiyaların mətnləri: key -> (az, en, ru). app.py bunları CT və TXT-yə birləşdirir."""

_T = {
    # --- giriş / bloklama / çıxış
    "blocked": ("Bu hesaba giriş dayandırılıb. Səhv olduğunu düşünürsənsə, sahiblə əlaqə saxla.",
                "Access to this account has been suspended. If this is a mistake, contact the owner.",
                "Доступ к этому аккаунту приостановлен. Если это ошибка, свяжись с владельцем."),
    "x_all_title": ("Bütün cihazlardan çıx", "Sign out of all devices", "Выйти на всех устройствах"),
    "x_all_hint": ("Telefonda, kompüterdə və başqa brauzerdə açıq olan bütün sessiyalar bağlanır. Başqa cihazda açıq səhifə ən çox 1 saata qədər işləyə bilər, sonra məcburi çıxır.",
                   "Closes every open session on phone, computer and other browsers. A page already open elsewhere may keep working for up to 1 hour, then it is signed out.",
                   "Закрывает все открытые сессии на телефоне, компьютере и в других браузерах. Уже открытая страница может работать до 1 часа, затем выход."),
    "x_all_btn": ("Bütün cihazlardan çıx", "Sign out everywhere", "Выйти везде"),
    "x_all_yes": ("Bəli, hamısından çıx", "Yes, sign out everywhere", "Да, выйти везде"),
    "x_all_no": ("Ləğv et", "Cancel", "Отмена"),
    # --- sahib: giriş idarəsi
    "x_acc_title": ("🔐 Giriş idarəsi", "🔐 Access management", "🔐 Управление доступом"),
    "x_need_sql": ("Bu bölmə üçün extras.sql Supabase-də işlədilməlidir.",
                   "Run extras.sql in Supabase to enable this section.",
                   "Для этого раздела нужно выполнить extras.sql в Supabase."),
    "x_inv_on": ("Dəvət kodu aktivdir: yeni qeydiyyat üçün kod tələb olunur.",
                 "Invite code is active: new sign-ups need the code.",
                 "Код приглашения активен: для регистрации нужен код."),
    "x_inv_off": ("Bazada dəvət kodu yoxdur (env-dəki kod və ya sərbəst qeydiyyat qüvvədədir).",
                  "No invite code in the database (the env code or open sign-up applies).",
                  "В базе нет кода приглашения (действует код из env или свободная регистрация)."),
    "x_inv_new": ("Yeni dəvət kodu (ən azı 6 simvol)", "New invite code (at least 6 characters)", "Новый код приглашения (не менее 6 символов)"),
    "x_inv_set": ("Kodu dəyiş", "Set code", "Сменить код"),
    "x_inv_clear": ("Kodu sil", "Remove code", "Удалить код"),
    "x_inv_short": ("Kod ən azı 6 simvol olmalıdır.", "The code must be at least 6 characters.", "Код должен быть не короче 6 символов."),
    "x_inv_ok_set": ("Dəvət kodu dəyişdirildi (göstərilmir, yadda saxla).", "Invite code updated (it is never shown, remember it).", "Код обновлён (он не показывается, запомни его)."),
    "x_inv_ok_clr": ("Dəvət kodu silindi.", "Invite code removed.", "Код приглашения удалён."),
    "x_blk_title": ("İstifadəçini blokla", "Block a user", "Заблокировать пользователя"),
    "x_blk_user": ("İstifadəçi adı", "Username", "Имя пользователя"),
    "x_blk_do": ("Blokla", "Block", "Заблокировать"),
    "x_blk_undo": ("Blokdan çıxar", "Unblock", "Разблокировать"),
    "x_blk_ok_b": ("Bloklandı.", "Blocked.", "Заблокирован."),
    "x_blk_ok_u": ("Blokdan çıxarıldı.", "Unblocked.", "Разблокирован."),
    "x_blk_fail": ("Alınmadı: ad səhvdir və ya bu sahibdir.", "Failed: unknown name, or the user is an owner.", "Не удалось: неверное имя или это владелец."),
    "x_blk_list": ("Bloklananlar: ", "Blocked: ", "Заблокированы: "),
    "x_blk_note": ("Bloklanan istifadəçi ən gec ~5 dəqiqəyə sistemdən çıxarılır.", "A blocked user is signed out within about 5 minutes.", "Заблокированный пользователь выходит из системы примерно за 5 минут."),
}


_T.update({
    # --- ulduz və qovluqlar
    "f_all": ("Bütün söhbətlər", "All chats", "Все чаты"),
    "f_star": ("⭐ Seçilmişlər", "⭐ Starred", "⭐ Избранные"),
    "f_manage": ("📁 Qovluqlar", "📁 Folders", "📁 Папки"),
    "f_move": ("Bu söhbət hansı qovluqda?", "Folder for this chat", "Папка для этого чата"),
    "f_none": ("Qovluqsuz", "No folder", "Без папки"),
    "f_new": ("Yeni qovluq adı", "New folder name", "Название новой папки"),
    "f_add": ("Qovluq yarat", "Create folder", "Создать папку"),
    "f_del": ("Qovluğu sil", "Delete folder", "Удалить папку"),
    "f_limit": ("Qovluq limiti dolub (12).", "Folder limit reached (12).", "Достигнут лимит папок (12)."),
    "f_pin": ("Ulduzla", "Star", "В избранное"),
    "f_unpin": ("Ulduzu götür", "Unstar", "Убрать из избранного"),
    # --- fəaliyyət xəritəsi
    "d_heat": ("Fəaliyyət xəritəsi (son 13 həftə)", "Activity map (last 13 weeks)", "Карта активности (13 недель)"),
    "d_longest": ("Ən uzun seriya: {n} gün", "Longest streak: {n} days", "Самая длинная серия: {n} дн."),
})


_T.update({
    # --- PDF və LaTeX
    "pdf_prep": ("📄 PDF hazırla", "📄 Prepare PDF", "📄 Подготовить PDF"),
    "pdf_dl": ("⬇️ PDF yüklə", "⬇️ Download PDF", "⬇️ Скачать PDF"),
    "pdf_fail": ("PDF hazırlanmadı (reportlab lazımdır).", "Could not build the PDF (reportlab is required).", "Не удалось создать PDF (нужен reportlab)."),
    "tex_title": ("∑ LaTeX düsturlar ({n})", "∑ LaTeX formulas ({n})", "∑ Формулы LaTeX ({n})"),
    "tex_hint": ("Hər düsturun küncündəki düymə ilə kopyala, Word və ya Overleaf-ə yapışdır.",
                 "Use the copy button on each formula, then paste into Word or Overleaf.",
                 "Скопируй формулу кнопкой в углу и вставь в Word или Overleaf."),
})


_T.update({
    "vchat": ("Səsli söhbət rejimi", "Voice chat mode", "Режим голосового чата"),
    "vchat_help": ("Mikrofonu açır, cavabı səslə oxuyur və cavabları qısa saxlayır.",
                   "Turns on the mic, reads answers aloud and keeps answers short.",
                   "Включает микрофон, озвучивает ответы и делает их короткими."),
})


_T.update({
    "perf_line": ("⚡ Sürət (son {n} cavab, median): axtarış {a} s · ilk söz {b} s · cəmi {c} s",
                  "⚡ Speed (last {n} answers, median): search {a}s · first word {b}s · total {c}s",
                  "⚡ Скорость (последние {n} ответов, медиана): поиск {a} с · первое слово {b} с · всего {c} с"),
    "perf_none": ("⚡ Sürət ölçüsü: hələ cavab yoxdur.", "⚡ Speed: no answers measured yet.", "⚡ Скорость: ответов пока нет."),
})


_T.update({
    "sc_notes": ("📝 Qeydlərim", "📝 My notes", "📝 Мои заметки"),
    "sc_notes_h": ("Öz fayllarını yüklə · Yalnız sənə görünür", "Upload your own files · Only visible to you", "Свои файлы · Видны только тебе"),
    "set_g_notes": ("Şəxsi qeydlər", "Personal notes", "Личные заметки"),
    "notes_hint": ("Öz konspektini (txt, md, pdf) yüklə. Tutor sualına uyğun parçaları tapıb cavabda istifadə edir və 📝 ilə göstərir. Fayllar yalnız sənin hesabına bağlıdır.",
                   "Upload your own notes (txt, md, pdf). The tutor finds the matching parts, uses them in answers and marks them 📝. Files belong to your account only.",
                   "Загрузи свой конспект (txt, md, pdf). Тьютор находит подходящие части, использует их в ответах и помечает 📝. Файлы привязаны только к твоему аккаунту."),
    "notes_use": ("Cavablarda qeydlərimi istifadə et", "Use my notes in answers", "Использовать мои заметки в ответах"),
    "notes_subj": ("Fənn", "Subject", "Предмет"),
    "notes_up": ("Fayl seç (txt, md, pdf; 5 MB-a qədər)", "Choose a file (txt, md, pdf; up to 5 MB)", "Выбери файл (txt, md, pdf; до 5 МБ)"),
    "notes_save": ("Qeydi saxla", "Save note", "Сохранить заметку"),
    "notes_ok": ("Saxlandı: {n} parça.", "Saved: {n} parts.", "Сохранено: {n} частей."),
    "notes_none": ("Bu fənn üçün qeyd yoxdur.", "No notes for this subject.", "Для этого предмета заметок нет."),
    "notes_limit": ("Limit doldu (12 fayl və ya 800 parça). Əvvəlcə birini sil.", "Limit reached (12 files or 800 parts). Delete one first.", "Лимит исчерпан (12 файлов или 800 частей). Сначала удали один."),
    "notes_need_sql": ("Qeydlər üçün extras.sql Supabase-də işlədilməlidir.", "Run extras.sql in Supabase to enable notes.", "Для заметок нужно выполнить extras.sql в Supabase."),
    "notes_fail": ("Silinmədi, bir az sonra yenidən cəhd et.", "Could not delete, try again shortly.", "Не удалось удалить, попробуй позже."),
    "notes_part": ("hissə", "part", "часть"),
    "notes_err_big": ("Fayl 5 MB-dan böyükdür.", "File is larger than 5 MB.", "Файл больше 5 МБ."),
    "notes_err_type": ("Fayl növü uyğun deyil (yalnız txt, md, pdf).", "Unsupported file type (txt, md, pdf only).", "Неподдерживаемый тип (только txt, md, pdf)."),
    "notes_err_empty": ("Fayldan mətn çıxmadı (skan edilmiş PDF ola bilər).", "No text found in the file (maybe a scanned PDF).", "Текст не найден (возможно, скан PDF)."),
})


_T.update({
    "act_read": ("Oxu", "Read", "Озвучить"),
    "act_card": ("Kart", "Card", "Карточка"),
    "act_up": ("Faydalı", "Helpful", "Полезно"),
    "act_dn": ("Faydasız", "Not helpful", "Не полезно"),
    "act_dl": ("Yüklə", "Save", "Скачать"),
})


_T.update({
    # emoji silindikdən sonra mənasını itirən sətirlər
    "o_fb_title": ("Cavablara rəylər", "Answer feedback", "Отзывы об ответах"),
    "o_fb_votes": ("Faydalı: {u} · Faydasız: {d}", "Helpful: {u} · Not helpful: {d}", "Полезно: {u} · Не полезно: {d}"),
})


def add(d):
    _T.update(d)


def get(lang):
    i = {"az": 0, "en": 1, "ru": 2}.get(lang, 0)
    return {k: v[i] for k, v in _T.items()}