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
    # --- istifadəçi adını dəyişmək
    "un_title": ("İstifadəçi adı", "Username", "Имя пользователя"),
    "un_hint": ("3-20 simvol: a-z, rəqəmlər və _. Adı 72 saatda yalnız 1 dəfə dəyişmək olar.",
                "3-20 characters: a-z, digits and _. You can change it only once every 72 hours.",
                "3-20 символов: a-z, цифры и _. Менять имя можно только раз в 72 часа."),
    "un_new": ("Yeni ad", "New username", "Новое имя"),
    "un_btn": ("Adı dəyiş", "Change username", "Сменить имя"),
    "un_ok": ("Ad dəyişdirildi.", "Username changed.", "Имя изменено."),
    "un_taken": ("Bu ad artıq götürülüb.", "This name is already taken.", "Это имя уже занято."),
    "un_invalid": ("Ad qaydaya uyğun deyil.", "The name does not match the rules.", "Имя не соответствует правилам."),
    "un_same": ("Bu sənin cari adındır.", "This is already your username.", "Это уже твоё имя."),
    "un_wait": ("Növbəti dəyişiklik {t} sonra mümkün olacaq.", "You can change it again in {t}.",
                "Сменить имя снова можно через {t}."),
    "un_units": ("gün|saat|dəq", "d|h|min", "д|ч|мин"),
    "un_need_sql": ("Bu funksiya üçün username_change.sql Supabase-də işlədilməlidir.",
                    "Run username_change.sql in Supabase to enable this.",
                    "Для этой функции нужно выполнить username_change.sql в Supabase."),
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
    "exp_title": ("Yüklə", "Export", "Экспорт"),
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


_T.update({
    "empty_hello": ("Nə öyrənmək istəyirsən?", "What would you like to learn?", "Что хочешь выучить?"),
    "fc_q": ("Sual", "Question", "Вопрос"),
    "fc_a": ("Cavab", "Answer", "Ответ"),
})


_T.update({
    # --- mesajlaşma
    "view_msgs": ("Mesajlar", "Messages", "Сообщения"),
    "m_title": ("Mesajlar", "Messages", "Сообщения"),
    "m_local": ("Mesajlaşma hesablarla işləyir və yerli rejimdə mövcud deyil.",
                "Messaging needs accounts and is not available in local mode.",
                "Сообщения работают через аккаунты и недоступны в локальном режиме."),
    "m_need_sql": ("Mesajlaşma hələ qurulmayıb. Sahib messaging.sql faylını Supabase-də işlətməlidir.",
                   "Messaging is not set up yet. The owner needs to run messaging.sql in Supabase.",
                   "Сообщения ещё не настроены. Владельцу нужно выполнить messaging.sql в Supabase."),
    "m_retry": ("Yenidən yoxla", "Check again", "Проверить снова"),
    "m_priv": ("Mesajları tətbiq sahibi görmür. Yalnız şikayət etdiyin yazışmanın son hissəsi ona çatır.",
               "The app owner cannot see messages. Only the last part of a conversation you report reaches them.",
               "Владелец приложения не видит сообщения. Ему попадает только последняя часть переписки, на которую пожаловались."),
    "m_tab_chats": ("Söhbətlər", "Chats", "Чаты"),
    "m_tab_friends": ("Dostlar", "Friends", "Друзья"),
    "m_new_group": ("Yeni qrup", "New group", "Новая группа"),
    "m_group_name": ("Qrupun adı (məsələn fin26)", "Group name (for example fin26)", "Название группы (например fin26)"),
    "m_create": ("Yarat", "Create", "Создать"),
    "m_created": ("Qrup yaradıldı. Bu kodu yoldaşlarına göndər: {code}",
                  "Group created. Send this code to your classmates: {code}",
                  "Группа создана. Отправь этот код одногруппникам: {code}"),
    "m_join_title": ("Qrupa qoşul", "Join a group", "Вступить в группу"),
    "m_code": ("Qrup kodu", "Group code", "Код группы"),
    "m_join": ("Qoşul", "Join", "Вступить"),
    "m_none": ("Hələ söhbət yoxdur. Qrup yarat, kodla qrupa qoşul və ya dost əlavə et.",
               "No chats yet. Create a group, join one with a code, or add a friend.",
               "Чатов пока нет. Создай группу, вступи по коду или добавь друга."),
    "m_back": ("Geri", "Back", "Назад"),
    "m_invite": ("Qrup kodu (yalnız qrup sahibi görür)", "Group code (only the group owner sees it)",
                 "Код группы (виден только владельцу группы)"),
    "m_input": ("Mesaj yaz...", "Write a message...", "Напиши сообщение..."),
    "m_empty": ("Hələ mesaj yoxdur. İlk sən yaz.", "No messages yet. Be the first to write.",
                "Сообщений пока нет. Напиши первым."),
    "m_offline": ("Bağlantı yoxdur, yenidən cəhd olunur.", "No connection, retrying.", "Нет связи, повторяю попытку."),
    "m_live": ("Mesajlar bir neçə saniyədən bir yenilənir. Ən yenisi yuxarıdadır.",
               "Messages refresh every few seconds. The newest is at the top.",
               "Сообщения обновляются каждые несколько секунд. Новые сверху."),
    "m_more": ("Şikayət, bloklama, silmə", "Report, block, delete", "Жалоба, блокировка, удаление"),
    "m_pick": ("Başqasının mesajı", "Someone else's message", "Сообщение другого человека"),
    "m_pick_mine": ("Mənim mesajım", "My message", "Моё сообщение"),
    "m_reason": ("Səbəb (istəyə bağlı)", "Reason (optional)", "Причина (необязательно)"),
    "m_report": ("Şikayət et", "Report", "Пожаловаться"),
    "m_reported": ("Şikayət göndərildi.", "Report sent.", "Жалоба отправлена."),
    "m_block_author": ("Müəllifi blokla", "Block the author", "Заблокировать автора"),
    "m_del_mine": ("Mesajı sil", "Delete message", "Удалить сообщение"),
    "m_members": ("Üzvlər", "Members", "Участники"),
    "m_kick": ("Üzvü çıxar", "Remove a member", "Удалить участника"),
    "m_kick_btn": ("Çıxar", "Remove", "Удалить"),
    "m_leave": ("Qrupdan çıx", "Leave group", "Выйти из группы"),
    "m_leave_ask": ("Qrupdan çıxmaq istəyirsən?", "Leave this group?", "Выйти из группы?"),
    "m_delete_ask": ("Çıxsan, sahiblik başqasına keçəcək. İstəsən qrupu tamamilə silə bilərsən.",
                     "If you leave, ownership passes to someone else. You can also delete the group completely.",
                     "Если выйдешь, владение перейдёт другому. Можно также удалить группу полностью."),
    "m_delete_group": ("Qrupu sil", "Delete group", "Удалить группу"),
    "m_yes": ("Bəli, çıx", "Yes, leave", "Да, выйти"),
    "m_no": ("Ləğv et", "Cancel", "Отмена"),
    "m_block": ("Blokla", "Block", "Заблокировать"),
    "m_unblock": ("Blokdan çıxar", "Unblock", "Разблокировать"),
    "m_blocked": ("Bloklananlar", "Blocked", "Заблокированные"),
    "m_f_add": ("Dost əlavə et", "Add a friend", "Добавить друга"),
    "m_f_user": ("İstifadəçi adı (tam yaz)", "Username (type it exactly)", "Имя пользователя (точно)"),
    "m_f_send": ("İstək göndər", "Send request", "Отправить запрос"),
    "m_f_sent": ("Dostluq istəyi göndərildi.", "Friend request sent.", "Запрос в друзья отправлен."),
    "m_f_acc_done": ("Dost oldunuz.", "You are now friends.", "Вы теперь друзья."),
    "m_f_in": ("Gələn istəklər", "Incoming requests", "Входящие запросы"),
    "m_f_out": ("Göndərilən istəklər", "Sent requests", "Отправленные запросы"),
    "m_f_list": ("Dostlar", "Friends", "Друзья"),
    "m_f_none": ("Hələ dostun yoxdur.", "No friends yet.", "Друзей пока нет."),
    "m_accept": ("Qəbul et", "Accept", "Принять"),
    "m_decline": ("Rədd et", "Decline", "Отклонить"),
    "m_cancel_req": ("Geri çək", "Cancel", "Отменить"),
    "m_write": ("Yaz", "Message", "Написать"),
    "m_remove": ("Sil", "Remove", "Удалить"),
    "m_e_invalid": ("Ad 3-30 simvol olmalıdır (hərf, rəqəm, boşluq, _ . -).",
                    "The name must be 3-30 characters (letters, digits, space, _ . -).",
                    "Название: 3-30 символов (буквы, цифры, пробел, _ . -)."),
    "m_e_too_many": ("Limitə çatdın.", "You reached the limit.", "Достигнут лимит."),
    "m_e_bad_code": ("Belə kod tapılmadı.", "No group with this code.", "Группы с таким кодом нет."),
    "m_e_throttled": ("Çox cəhd oldu. Bir neçə dəqiqə sonra yenə yoxla.",
                      "Too many attempts. Try again in a few minutes.",
                      "Слишком много попыток. Попробуй через несколько минут."),
    "m_e_full": ("Qrup doludur (50 nəfər).", "The group is full (50 people).", "Группа заполнена (50 человек)."),
    "m_e_slow_down": ("Çox sürətli yazırsan. Bir az gözlə.", "You are writing too fast. Wait a moment.",
                      "Слишком быстро. Подожди немного."),
    "m_e_not_allowed": ("Bu söhbətə yazmaq olmur.", "You cannot write in this chat.", "В этот чат писать нельзя."),
    "m_e_length": ("Mesaj 1-1000 simvol olmalıdır.", "A message must be 1-1000 characters.",
                   "Сообщение: от 1 до 1000 символов."),
    "m_e_not_found": ("Belə istifadəçi tapılmadı.", "User not found.", "Пользователь не найден."),
    "m_e_you_blocked": ("Bu istifadəçini bloklamısan.", "You blocked this user.", "Ты заблокировал этого пользователя."),
    "m_e_already": ("Artıq dostsunuz.", "You are already friends.", "Вы уже друзья."),
    "m_e_pending": ("İstək artıq göndərilib.", "The request is already sent.", "Запрос уже отправлен."),
    "m_e_own": ("Öz mesajını şikayət etmək olmur.", "You cannot report your own message.",
                "Нельзя жаловаться на своё сообщение."),
    "m_e_unknown": ("Alınmadı. Bir az sonra yenə yoxla.", "Did not work. Try again later.",
                    "Не получилось. Попробуй позже."),
    "m_o_title": ("Mesaj şikayətləri", "Message reports", "Жалобы на сообщения"),
    "m_o_none": ("Açıq şikayət yoxdur.", "No open reports.", "Открытых жалоб нет."),
    "m_o_need_sql": ("Şikayətlər üçün messaging.sql işlədilməlidir.", "Run messaging.sql to see reports.",
                     "Для жалоб нужно выполнить messaging.sql."),
    "m_o_dismiss": ("Rədd et", "Dismiss", "Отклонить"),
    "m_o_block": ("İstifadəçini blokla", "Block the user", "Заблокировать пользователя"),
})


def add(d):
    _T.update(d)


def get(lang):
    i = {"az": 0, "en": 1, "ru": 2}.get(lang, 0)
    return {k: v[i] for k, v in _T.items()}