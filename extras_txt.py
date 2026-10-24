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
    "m_need_key": ("Mesajlaşma üçün şifrələmə açarı (MSG_KEY) təyin edilməyib. Sahib onu Secrets-ə əlavə etməlidir.",
                   "The encryption key (MSG_KEY) for messaging is not set. The owner must add it to Secrets.",
                   "Ключ шифрования (MSG_KEY) для сообщений не задан. Владельцу нужно добавить его в Secrets."),
    "m_e_no_key": ("Şifrələmə açarı yoxdur, mesaj göndərilmədi.", "No encryption key, message not sent.",
                   "Нет ключа шифрования, сообщение не отправлено."),
    "m_retry": ("Yenidən yoxla", "Check again", "Проверить снова"),
    "m_priv": ("Mesajları tətbiq sahibi görmür. Yalnız şikayət etdiyin yazışmanın son hissəsi ona çatır.",
               "The app owner cannot see messages. Only the last part of a conversation you report reaches them.",
               "Владелец приложения не видит сообщения. Ему попадает только последняя часть переписки, на которую пожаловались."),
    "m_scam": ("Heç kim (hətta müəllim və ya tətbiq sahibi adından) səndən parol, e-poçt kodu və ya Authenticator kodu istəməməlidir. Belə mesaj gəlsə, şikayət et və linkə basma.",
               "Nobody (not even in the name of a teacher or the app owner) should ask you for a password, email code or Authenticator code. If you get such a message, report it and do not click links.",
               "Никто (даже от имени преподавателя или владельца приложения) не должен просить у тебя пароль, код из почты или код Authenticator. Если пришло такое сообщение, пожалуйся и не нажимай на ссылки."),
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


_T.update({
    # --- Authenticator (TOTP) və təhlükəsizlik jurnalı
    "mfa_title": ("Authenticator ilə qorunma", "Authenticator protection", "Защита через Authenticator"),
    "mfa_hint": ("Google Authenticator, Microsoft Authenticator və ya Authy ilə hər girişdə 6 rəqəmli kod soruşulur. Parolun və e-poçtun ələ keçsə belə, hesaba girə bilməzlər.",
                 "With Google Authenticator, Microsoft Authenticator or Authy a 6-digit code is required at every sign-in. Even if your password and email are stolen, they cannot get into the account.",
                 "С Google Authenticator, Microsoft Authenticator или Authy при каждом входе нужен 6-значный код. Даже если пароль и почта украдены, в аккаунт не войти."),
    "mfa_on_btn": ("Authenticator qoş", "Set up Authenticator", "Подключить Authenticator"),
    "mfa_scan": ("QR kodu Authenticator tətbiqi ilə oxut, sonra göstərdiyi 6 rəqəmli kodu yaz.",
                 "Scan the QR code with your Authenticator app, then enter the 6-digit code it shows.",
                 "Отсканируй QR-код приложением Authenticator и введи показанный 6-значный код."),
    "mfa_manual": ("QR oxunmursa, bu açarı tətbiqə əl ilə yaz (heç kimə göndərmə):",
                   "If the QR does not scan, type this key into the app (never share it):",
                   "Если QR не читается, введи этот ключ в приложении вручную (никому не отправляй):"),
    "mfa_code": ("6 rəqəmli kod", "6-digit code", "6-значный код"),
    "mfa_confirm": ("Təsdiqlə və qoş", "Confirm and enable", "Подтвердить и включить"),
    "mfa_on": ("Authenticator qoşulub. Hər girişdə kod soruşulur.", "Authenticator is on. A code is asked at every sign-in.",
               "Authenticator включён. При каждом входе спрашивается код."),
    "mfa_off": ("Authenticator-u söndür", "Turn off Authenticator", "Отключить Authenticator"),
    "mfa_off_warn": ("Söndürsən, hesab yenə yalnız parol və e-poçt kodu ilə qorunacaq. Əminsən?",
                     "If you turn it off, the account is protected only by password and email code. Sure?",
                     "Если отключить, аккаунт будет защищён только паролем и кодом из почты. Уверен?"),
    "mfa_off_yes": ("Bəli, söndür", "Yes, turn off", "Да, отключить"),
    "mfa_fail": ("Alınmadı. Bir az sonra yenə yoxla.", "Did not work. Try again later.", "Не получилось. Попробуй позже."),
    "mfa_prompt": ("Authenticator tətbiqindəki 6 rəqəmli kodu yaz.", "Enter the 6-digit code from your Authenticator app.",
                   "Введи 6-значный код из приложения Authenticator."),
    "mfa_owner_warn": ("Sahib hesabında Authenticator qoşulmayıb. Ayarlar > Profil bölməsində qoş: bu, sahib panelinin ən güclü qorumasıdır.",
                       "Authenticator is not enabled on the owner account. Turn it on in Settings > Profile: it is the strongest protection for the owner panel.",
                       "На аккаунте владельца не включён Authenticator. Включи в Настройки > Профиль: это самая сильная защита панели владельца."),
    "sl_title": ("Təhlükəsizlik jurnalı", "Security log", "Журнал безопасности"),
    "sl_need_sql": ("Jurnal üçün security.sql işlədilməlidir.", "Run security.sql to see the log.", "Для журнала нужно выполнить security.sql."),
    "sl_none": ("Hələ qeyd yoxdur.", "No entries yet.", "Записей пока нет."),
    "sl_show": ("Son {n} hadisə", "Last {n} events", "Последние события: {n}"),
})


_T.update({
    # --- cavabın altında sürətli düymələr
    "qf_simple": ("Sadə izah et", "Simpler", "Проще"),
    "qf_example": ("Misal ver", "Example", "Пример"),
    "qf_quiz": ("Məni yoxla", "Quiz me", "Проверь меня"),
    "qf_simple_q": ("Bunu daha sadə izah et, gündəlik həyatdan bir misalla.",
                    "Explain that more simply, with an everyday example.",
                    "Объясни это проще, на примере из жизни."),
    "qf_example_q": ("Buna aid bir konkret misal ver və addım-addım izah et.",
                     "Give me one concrete example of this and walk me through it step by step.",
                     "Приведи конкретный пример и разбери его по шагам."),
    "qf_quiz_q": ("Bu mövzu üzrə məni yoxla: mənə bir sual ver və cavabımı gözlə.",
                  "Quiz me on this: ask me one question and wait for my answer.",
                  "Проверь меня по этой теме: задай один вопрос и дождись моего ответа."),
})



_T.update({
    # --- dəftər (saxlanmış cavablar)
    "view_notebook": ("Dəftər", "Notebook", "Тетрадь"),
    "nb_title": ("Dəftər", "Notebook", "Тетрадь"),
    "nb_star": ("Dəftər", "Notebook", "Тетрадь"),
    "nb_star_on": ("Dəftərdə", "In notebook", "В тетради"),
    "nb_star_help": ("Bu cavabı fənnin dəftərinə saxla (yenidən bassan, çıxarılır)",
                     "Save this answer to the subject notebook (press again to remove)",
                     "Сохранить ответ в тетрадь предмета (повторное нажатие убирает)"),
    "nb_added": ("Dəftərə əlavə olundu.", "Saved to the notebook.", "Добавлено в тетрадь."),
    "nb_removed": ("Dəftərdən çıxarıldı.", "Removed from the notebook.", "Убрано из тетради."),
    "nb_limit": ("Dəftər doludur (500 cavab). Köhnələrdən bir neçəsini sil.",
                 "The notebook is full (500 answers). Delete some old ones.",
                 "Тетрадь заполнена (500 ответов). Удали несколько старых."),
    "nb_need_sql": ("Dəftər və sınaq imtahanı üçün study.sql Supabase-də işlədilməlidir.",
                    "Run study.sql in Supabase to use the notebook and practice exams.",
                    "Для тетради и пробного экзамена нужно выполнить study.sql в Supabase."),
    "nb_empty": ("Dəftər hələ boşdur. Söhbətdə bəyəndiyin cavabın altındakı \"Dəftər\" düyməsini bas, burada toplanacaq.",
                 "The notebook is empty. Press \"Notebook\" under an answer you like in the chat and it will appear here.",
                 "Тетрадь пока пуста. Нажми \"Тетрадь\" под понравившимся ответом в чате, и он появится здесь."),
    "nb_count": ("Bu fəndə {n} saxlanmış cavab var.", "{n} saved answers in this subject.",
                 "Сохранённых ответов по предмету: {n}."),
    "nb_search": ("Dəftərdə axtar", "Search the notebook", "Поиск в тетради"),
    "nb_search_ph": ("söz və ya ifadə", "word or phrase", "слово или фраза"),
    "nb_found": ("Tapıldı: {n}", "Found: {n}", "Найдено: {n}"),
    "nb_md": ("Markdown yüklə", "Download Markdown", "Скачать Markdown"),
    "nb_pdf": ("PDF hazırla", "Make PDF", "Сделать PDF"),
    "nb_pdf_dl": ("PDF-i yüklə", "Download PDF", "Скачать PDF"),
    "nb_pdf_fail": ("PDF hazırlanmadı. Markdown kimi yüklə.", "Could not make the PDF. Download Markdown instead.",
                    "PDF не получился. Скачай Markdown."),
    "nb_sum": ("Konspekt hazırla", "Make a revision sheet", "Сделать конспект"),
    "nb_sum_help": ("Tutor bütün saxlanmış cavablardan bir səhifəlik imtahan konspekti hazırlayır (1 sual sayılır)",
                    "The tutor turns all saved answers into a one-page revision sheet (counts as 1 question)",
                    "Тьютор делает из сохранённых ответов конспект на одну страницу (1 вопрос)"),
    "nb_sum_spin": ("Konspekt hazırlanır...", "Making the revision sheet...", "Готовлю конспект..."),
    "nb_sum_title": ("İmtahan konspekti", "Revision sheet", "Конспект к экзамену"),
    "nb_sum_save": ("Konspekti dəftərə saxla", "Save the sheet to the notebook", "Сохранить конспект в тетрадь"),
    "nb_mock": ("Dəftərdən sınaq", "Practice exam from it", "Пробный экзамен"),
    "nb_mock_help": ("Sınaq imtahanını bu dəftərdəki cavablar əsasında hazırla",
                     "Build a practice exam from the answers in this notebook",
                     "Составить пробный экзамен по ответам из тетради"),
    "nb_note": ("Qeydim", "My note", "Моя заметка"),
    "nb_note_ph": ("Öz sözlərinlə qısa qeyd (istəyə bağlı)", "A short note in your own words (optional)",
                   "Короткая заметка своими словами (необязательно)"),
    "nb_note_save": ("Qeydi saxla", "Save note", "Сохранить"),
    "nb_note_ok": ("Qeyd saxlanıldı.", "Note saved.", "Заметка сохранена."),
    "nb_ask": ("Söhbətdə davam et", "Continue in chat", "Продолжить в чате"),
    "nb_ask_q": ("Bu mövzunu daha ətraflı izah et: {q}", "Explain this topic in more depth: {q}",
                 "Объясни эту тему подробнее: {q}"),
    "nb_del": ("Sil", "Delete", "Удалить"),
    "nb_saved_at": ("Saxlanıb", "Saved", "Сохранено"),

    # --- sınaq imtahanı
    "mk_tab": ("Sınaq imtahanı", "Practice exam", "Пробный экзамен"),
    "mk_title": ("Sınaq imtahanı", "Practice exam", "Пробный экзамен"),
    "mk_intro": ("Müəllimin keçmiş imtahanlarını və ya nümunə suallarını yüklə. Tutor eyni formatda və çətinlikdə YENİ suallar yaradır, sonra cavablarını yoxlayır.",
                 "Upload your teacher's past exams or sample questions. The tutor writes NEW questions in the same format and difficulty, then checks your answers.",
                 "Загрузи прошлые экзамены преподавателя или примеры вопросов. Тьютор составит НОВЫЕ вопросы в том же формате и сложности и проверит ответы."),
    "mk_no_book": ("Bu hesabda kurs kitabı bağlıdır: suallar nümunələrə, şəxsi qeydlərinə və ümumi biliklərə əsaslanır.",
                   "Course books are not available on this account: questions are based on the samples, your notes and general knowledge.",
                   "Учебники недоступны на этом аккаунте: вопросы основаны на примерах, твоих заметках и общих знаниях."),
    "mk_need_sql": ("Sınaq imtahanı üçün study.sql Supabase-də işlədilməlidir.",
                    "Run study.sql in Supabase to use practice exams.",
                    "Для пробного экзамена нужно выполнить study.sql в Supabase."),
    "mk_samples": ("Keçmiş imtahan nümunələri ({n})", "Past exam samples ({n})", "Примеры прошлых экзаменов ({n})"),
    "mk_samples_hint": ("PDF, şəkil (telefonla çəkilmiş imtahan vərəqi) və ya mətn. Fayllar yalnız sənə görünür. Tutor köhnə sualları köçürmür, yalnız üslubu götürür. Hər fənn üçün 8 nümunəyə qədər.",
                        "PDF, a photo of an exam paper, or text. Files are visible only to you. The tutor does not copy old questions, it only learns the style. Up to 8 samples per subject.",
                        "PDF, фото экзаменационного листа или текст. Файлы видишь только ты. Тьютор не копирует старые вопросы, только перенимает стиль. До 8 примеров на предмет."),
    "mk_upload": ("Fayl seç", "Choose a file", "Выбери файл"),
    "mk_save_sample": ("Nümunəni saxla", "Save sample", "Сохранить пример"),
    "mk_reading": ("Fayl oxunur...", "Reading the file...", "Читаю файл..."),
    "mk_paste_name": ("Ad (məsələn: Midterm 2025)", "Name (e.g. Midterm 2025)", "Название (например: Midterm 2025)"),
    "mk_paste": ("və ya sualları buraya yapışdır", "or paste the questions here", "или вставь вопросы сюда"),
    "mk_sample_word": ("Nümunə", "Sample", "Пример"),
    "mk_saved": ("Saxlanıldı: {name}", "Saved: {name}", "Сохранено: {name}"),
    "mk_chars": ("simvol", "characters", "символов"),
    "mk_limit": ("Bu fənn üçün 8 nümunə limitinə çatdın. Birini sil.", "You reached 8 samples for this subject. Delete one.",
                 "Достигнут лимит в 8 примеров для предмета. Удали один."),
    "mk_err_type": ("Bu fayl növü dəstəklənmir (PDF, şəkil, txt, md).", "This file type is not supported (PDF, image, txt, md).",
                    "Этот тип файла не поддерживается (PDF, изображение, txt, md)."),
    "mk_err_big": ("Fayl çox böyükdür (10 MB-a qədər).", "The file is too large (up to 10 MB).", "Файл слишком большой (до 10 МБ)."),
    "mk_err_empty": ("Faylda və ya mətndə oxunacaq sual tapılmadı.", "No readable questions were found.",
                     "Не найдено читаемых вопросов."),
    "mk_err_ocr": ("Şəkil və skan PDF-ləri oxumaq üçün Gemini lazımdır. Mətni yapışdır.",
                   "Reading images and scanned PDFs needs Gemini. Paste the text instead.",
                   "Для фото и сканов нужен Gemini. Вставь текст вручную."),
    "mk_err_quota": ("Bugünkü sual limiti bitib: şəkli sabah oxuya bilərsən və ya mətni yapışdır.",
                     "Today's question limit is used up: read the image tomorrow or paste the text.",
                     "Дневной лимит исчерпан: прочитай фото завтра или вставь текст."),
    "mk_err_fail": ("Fayl oxunmadı. Bir az sonra yenə yoxla və ya mətni yapışdır.",
                    "Could not read the file. Try again later or paste the text.",
                    "Не удалось прочитать файл. Попробуй позже или вставь текст."),
    "mk_history": ("Son nəticələrin", "Your recent results", "Последние результаты"),
    "mk_make": ("Yeni sınaq", "New practice exam", "Новый пробный экзамен"),
    "mk_topic": ("Plandakı mövzu", "Topic from your plan", "Тема из плана"),
    "mk_all_topics": ("Bütün mövzular", "All topics", "Все темы"),
    "mk_topic_own": ("və ya mövzunu özün yaz", "or type a topic", "или впиши тему"),
    "mk_topic_ph": ("məsələn: Mövzu 2, məhdudluq və seçim", "e.g. Topic 2, scarcity and choice", "например: Тема 2, ограниченность"),
    "mk_n": ("Sual sayı", "Number of questions", "Количество вопросов"),
    "mk_timed": ("Vaxtla", "Timed", "На время"),
    "mk_harder": ("Bir az daha çətin", "A bit harder", "Чуть сложнее"),
    "mk_use_nb": ("Dəftərimdəki cavabları da istifadə et", "Also use my notebook", "Использовать и тетрадь"),
    "mk_use_nb_help": ("Suallar dəftərdə saxladığın cavablara da əsaslansın",
                       "Questions will also be based on the answers saved in your notebook",
                       "Вопросы будут опираться и на сохранённые ответы"),
    "mk_no_samples": ("Nümunə yoxdur: tutor standart midterm formatında sınaq hazırlayacaq.",
                      "No samples: the tutor will use a standard midterm format.",
                      "Примеров нет: тьютор использует стандартный формат промежуточного экзамена."),
    "mk_go": ("Sınağı hazırla", "Create the exam", "Составить экзамен"),
    "mk_spin": ("Suallar hazırlanır... (15-40 saniyə)", "Writing the questions... (15-40 seconds)",
                "Составляю вопросы... (15-40 секунд)"),
    "mk_gen_fail": ("Suallar hazırlanmadı. Bir az sonra yenə yoxla.", "Could not create the questions. Try again shortly.",
                    "Не удалось составить вопросы. Попробуй чуть позже."),
    "mk_style": ("Tanınan üslub", "Detected style", "Распознанный стиль"),
    "mk_paper_info": ("{n} sual, cəmi {p} bal.", "{n} questions, {p} points in total.", "{n} вопросов, всего {p} баллов."),
    "mk_pts": ("bal", "pts", "балл."),
    "mk_pdf_blank": ("Çap üçün PDF (cavabsız)", "PDF to print (no answers)", "PDF для печати (без ответов)"),
    "mk_pdf_key": ("Cavablarla PDF", "PDF with answers", "PDF с ответами"),
    "mk_q_word": ("Sual", "Question", "Вопрос"),
    "mk_key_word": ("Cavab", "Answer", "Ответ"),
    "mk_answer_ph": ("Cavabını yaz...", "Write your answer...", "Напиши ответ..."),
    "mk_submit": ("Təhvil ver və yoxla", "Submit and check", "Сдать и проверить"),
    "mk_grading": ("Cavablar yoxlanılır...", "Checking your answers...", "Проверяю ответы..."),
    "mk_cancel": ("İmtina et", "Cancel", "Отменить"),
    "mk_score": ("Bal", "Score", "Баллы"),
    "mk_mcq_ok": ("Test: düz", "Multiple choice correct", "Тест: верно"),
    "mk_open_ungraded": ("Açıq suallar yoxlanmadı (limit və ya bağlantı problemi). Nümunə cavabla özün müqayisə et.",
                         "Open questions were not graded (limit or connection problem). Compare with the model answer yourself.",
                         "Открытые вопросы не проверены (лимит или связь). Сравни с образцом сам."),
    "mk_cards": ("Səhvlərdən kart", "Cards from mistakes", "Карточки из ошибок"),
    "mk_cards_help": ("Səhv cavabladığın suallar düzgün cavabı ilə kartlara çevrilir (AI işlətmir)",
                      "Questions you got wrong become flashcards with the correct answer (no AI used)",
                      "Вопросы с ошибками станут карточками с правильным ответом (без ИИ)"),
    "mk_no_wrong": ("Səhv yoxdur, kart lazım deyil.", "No mistakes, no cards needed.", "Ошибок нет, карточки не нужны."),
    "mk_retry": ("Eyni sınağı yenidən", "Retry the same exam", "Пройти заново"),
    "mk_new": ("Yeni sınaq", "New exam", "Новый экзамен"),
    "mk_your": ("Sənin cavabın", "Your answer", "Твой ответ"),
    "mk_blank": ("(boş)", "(blank)", "(пусто)"),
    "mk_missing": ("Çatışmayan", "Missing", "Не хватает"),
    "mk_model": ("Nümunə cavab", "Model answer", "Образец ответа"),
    "mk_save_q": ("Dəftərə saxla", "Save to notebook", "В тетрадь"),
})


_T.update({
    # --- ilk giriş turu
    "tour_again": ("Tanıtım turunu yenidən göstər", "Show the welcome tour again", "Показать обзор снова"),
    "tour_step": ("Addım {i}/{n}", "Step {i}/{n}", "Шаг {i}/{n}"),
    "tour_back": ("Geri", "Back", "Назад"),
    "tour_skip": ("Keç", "Skip", "Пропустить"),
    "tour_next": ("İrəli", "Next", "Далее"),
    "tour_done": ("Başlayaq", "Let's start", "Начнём"),
    "tour1_t": ("Xoş gəldin!", "Welcome!", "Добро пожаловать!"),
    "tour1_b": ("Bu, kurs fənlərin üçün şəxsi tutorundur.\n\n"
                "- **Sol paneldə fənni seç:** 5 kurs fənni və ümumi köməkçi var.\n"
                "- Sual yaz, şəkil və ya PDF əlavə et, tutor addım-addım izah etsin.\n"
                "- Gündə **40 sual** limiti var ki, tətbiq hamı üçün pulsuz qalsın.",
                "This is your personal tutor for your courses.\n\n"
                "- **Pick a subject in the left panel:** 5 courses and a general assistant.\n"
                "- Ask a question, attach a photo or a PDF, and the tutor explains step by step.\n"
                "- There is a limit of **40 questions a day** so the app stays free for everyone.",
                "Это твой личный тьютор по предметам.\n\n"
                "- **Выбери предмет слева:** 5 курсов и общий помощник.\n"
                "- Задай вопрос, прикрепи фото или PDF, и тьютор объяснит по шагам.\n"
                "- Лимит **40 вопросов в день**, чтобы приложение оставалось бесплатным."),
    "tour2_t": ("Dörd rejim", "Four modes", "Четыре режима"),
    "tour2_b": ("Sol paneldə rejimi seç:\n\n"
                "- **İzah:** mövzunu sadə dillə öyrədir.\n"
                "- **Praktika:** tapşırıq verir, cavabını yoxlayır.\n"
                "- **İmtahan:** imtahan kimi sual verir, ipucu vermir.\n"
                "- **Feynman:** sən izah edirsən, tutor boşluqları tapır. Ən güclü öyrənmə üsuludur.",
                "Choose a mode in the left panel:\n\n"
                "- **Learn:** explains the topic in plain words.\n"
                "- **Practice:** gives exercises and checks your answer.\n"
                "- **Exam:** asks exam-style questions without hints.\n"
                "- **Feynman:** you explain, the tutor finds the gaps. The strongest way to learn.",
                "Выбери режим слева:\n\n"
                "- **Объяснение:** простыми словами о теме.\n"
                "- **Практика:** задания и проверка ответа.\n"
                "- **Экзамен:** вопросы как на экзамене, без подсказок.\n"
                "- **Фейнман:** объясняешь ты, тьютор находит пробелы. Самый сильный способ учиться."),
    "tour3_t": ("Cavabın altındakı düymələr", "Buttons under each answer", "Кнопки под ответом"),
    "tour3_b": ("- **Sadə izah et / Misal ver / Məni yoxla:** bir kliklə növbəti sual.\n"
                "- **Dəftər:** yaxşı cavabı saxla. Dəftərdən imtahan konspekti də hazırlamaq olar.\n"
                "- **Kart:** cavabdan təkrar kartları yaradır.\n"
                "- **Oxu:** cavabı səslə dinlə.",
                "- **Simpler / Example / Quiz me:** the next question in one click.\n"
                "- **Notebook:** save a good answer. The notebook can also make a revision sheet.\n"
                "- **Card:** turns the answer into flashcards.\n"
                "- **Read:** listen to the answer.",
                "- **Проще / Пример / Проверь меня:** следующий вопрос в один клик.\n"
                "- **Тетрадь:** сохрани хороший ответ. Из тетради можно сделать конспект.\n"
                "- **Карточка:** превращает ответ в карточки.\n"
                "- **Озвучить:** послушай ответ."),
    "tour4_t": ("İmtahana hazırlıq", "Exam preparation", "Подготовка к экзамену"),
    "tour4_b": ("- **Kartlar:** gündəlik təkrar, test və vaxtlı imtahan.\n"
                "- **Plan:** imtahan tarixini yaz, tutor mövzuları günlərə bölür. Xülasə və mövzu xəritəsi də burdadır.\n"
                "- **Sınaq imtahanı:** müəllimin keçmiş imtahanını yüklə, tutor eyni üslubda yeni suallar hazırlayıb yoxlasın.\n"
                "- **Panel:** seriyan və irəliləyişin.",
                "- **Cards:** daily review, quizzes and timed exams.\n"
                "- **Plan:** set your exam date and the tutor spreads the topics over the days. Summaries and mind maps live here too.\n"
                "- **Practice exam:** upload your teacher's past exam and get new questions in the same style, graded.\n"
                "- **Stats:** your streak and progress.",
                "- **Карточки:** ежедневное повторение, тесты и экзамен на время.\n"
                "- **План:** укажи дату экзамена, и тьютор распределит темы по дням. Конспекты и карты тем тоже здесь.\n"
                "- **Пробный экзамен:** загрузи прошлый экзамен преподавателя и получи новые вопросы в том же стиле с проверкой.\n"
                "- **Статистика:** серия дней и прогресс."),
    "tour5_t": ("Sinif yoldaşları və təhlükəsizlik", "Classmates and safety", "Одногруппники и безопасность"),
    "tour5_b": ("- **Mesajlar:** qrup yarat (məsələn fin26), kodla qoşul, dostlarınla yaz. Pis davranışı şikayət et.\n"
                "- **Heç kim** (müəllim və ya tətbiq sahibi adından belə) səndən parol və ya kod istəməməlidir.\n"
                "- Hesabını daha güclü qorumaq üçün: **Ayarlar > Profil > Authenticator**.\n"
                "- Bu turu istənilən vaxt **Ayarlar > İnterfeys**-dən yenidən aça bilərsən.",
                "- **Messages:** create a group (e.g. fin26), join with a code, chat with friends. Report bad behaviour.\n"
                "- **Nobody** (not even in the name of a teacher or the app owner) should ask for your password or codes.\n"
                "- For stronger protection: **Settings > Profile > Authenticator**.\n"
                "- You can open this tour again any time in **Settings > Interface**.",
                "- **Сообщения:** создай группу (например fin26), вступай по коду, пиши друзьям. Жалуйся на плохое поведение.\n"
                "- **Никто** (даже от имени преподавателя или владельца) не должен просить пароль или коды.\n"
                "- Для сильной защиты: **Настройки > Профиль > Authenticator**.\n"
                "- Этот обзор можно открыть снова в **Настройки > Интерфейс**."),
})


_T.update({
    # --- paylaşılan kart dəstləri
    "dk_title": ("Kart dəstləri", "Card decks", "Наборы карточек"),
    "dk_need_sql": ("Kart dəstləri üçün study.sql Supabase-də işlədilməlidir.", "Run study.sql in Supabase to share card decks.",
                    "Для наборов карточек нужно выполнить study.sql в Supabase."),
    "dk_none": ("Hələ paylaşılan dəst yoxdur.", "No decks shared yet.", "Наборов пока нет."),
    "dk_cards": ("kart", "cards", "карточек"),
    "dk_add": ("Kartlarıma əlavə et", "Add to my cards", "Добавить себе"),
    "dk_add_help": ("Dəstdəki kartlar sənin kartlarına əlavə olunur (artıq olanlar təkrarlanmır)",
                    "The cards are added to yours (duplicates are skipped)",
                    "Карточки добавятся к твоим (повторы пропускаются)"),
    "dk_added": ("{n} kart \"{s}\" fənninə əlavə olundu. Kartlar bölməsində təkrar et.",
                 "{n} cards added to \"{s}\". Review them in Cards.",
                 "{n} карточек добавлено в \"{s}\". Повтори их в Карточках."),
    "dk_added0": ("Bu kartların hamısı səndə artıq var.", "You already have all these cards.", "Все эти карточки у тебя уже есть."),
    "dk_bad": ("Dəst açılmadı.", "Could not open the deck.", "Не удалось открыть набор."),
    "dk_share": ("Öz kartlarını paylaş", "Share your cards", "Поделиться карточками"),
    "dk_filter": ("Yalnız bu sözü olan kartlar (istəyə bağlı)", "Only cards containing (optional)",
                  "Только карточки со словом (необязательно)"),
    "dk_filter_ph": ("məsələn: fürsət xərci", "e.g. opportunity cost", "например: альтернативная стоимость"),
    "dk_n": ("Ən çox neçə kart", "Max number of cards", "Сколько карточек максимум"),
    "dk_name": ("Dəstin adı", "Deck name", "Название набора"),
    "dk_name_ph": ("{s} kartları", "{s} cards", "Карточки: {s}"),
    "dk_send": ("Dəsti paylaş", "Share the deck", "Поделиться набором"),
    "dk_empty": ("Bu fənndə uyğun kart yoxdur.", "No matching cards in this subject.", "В этом предмете нет подходящих карточек."),
    "dk_sent": ("{n} kartlıq dəst paylaşıldı.", "Shared a deck of {n} cards.", "Набор из {n} карточек отправлен."),
    "dk_msg": ("[Kart dəsti] {t}: {n} kart. Aşağıdakı \"Kart dəstləri\" bölməsindən əlavə et.",
               "[Card deck] {t}: {n} cards. Add it from \"Card decks\" below.",
               "[Набор карточек] {t}: {n} шт. Добавь его в разделе \"Наборы карточек\" ниже."),
})


_T.update({
    # --- səsli söhbət düyməsi
    "vc_short": ("Səs", "Voice", "Голос"),
    "vc_on_help": ("Səsli söhbəti aç: danış, tutor səslə və qısa cavab versin",
                   "Turn on voice chat: speak and the tutor answers aloud, briefly",
                   "Включить голосовой чат: говори, тьютор ответит голосом и кратко"),
    "vc_off_help": ("Səsli söhbəti bağla", "Turn off voice chat", "Выключить голосовой чат"),
    "vc_hint": ("Səsli söhbət açıqdır: mikrofona bas, danış, sonra dayandır. Tutor cavabı səslə oxuyacaq. Hər dəfə mikrofona yenidən bas (brauzer təhlükəsizlik üçün mikrofonu özü açmağa icazə vermir).",
                "Voice chat is on: tap the mic, speak, then stop. The tutor will read the answer aloud. Tap the mic again each time (browsers do not let pages start the mic by themselves).",
                "Голосовой чат включён: нажми на микрофон, говори, затем останови. Тьютор прочитает ответ вслух. Каждый раз нажимай на микрофон снова (браузер не даёт странице включать его самой)."),
})


def add(d):
    _T.update(d)


def get(lang):
    i = {"az": 0, "en": 1, "ru": 2}.get(lang, 0)
    return {k: v[i] for k, v in _T.items()}