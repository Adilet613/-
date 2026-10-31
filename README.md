# 🎮 Grand Mobile · Qazaq Loc QA

> **Decentrathon 6.0 | Кейс 02: Grand Mobile**  
> Автономный инструмент аудита, детекции ошибок и контроля качества казахской локализации для Flutter ARB-файлов.

---

## 👥 Команда «Amigos» (ID: 352482)

* 👑 **Эльмар Сейнлхан** — Team Lead / Solution Architecture
* 🇰🇿 **Adilet Sungatuly** — QA Lead & Native Qazaq Reviewer
* 💻 **Аймұхаммед Жанаберген** — CLI Core & Algorithm Engineer
* 📱 **Shadibay Kenzhebek** — Flutter & Localization Specialist

---

## 📊 Ключевые результаты аудита

* **5 479 строк** проверено в боевом контракте.
* **145 дефектов** выявлено по 11 типам ошибок.
* **144 строки исправлено** и **100% подтверждено носителем** (`reviewed_by_human: true`).
* **87 терминов** утверждено в глоссарии сленга («варн», «мут», «ГК», «отбасы», «фракция»).
* **89 из 89 тестов пройдены** (100% coverage).
* **Flutter gen-l10n**: полная валидность ICU и плейсхолдеров.

---

## 🚀 Запуск утилиты
```bash
cd grand_mobile_locqa_final_submission/cli
python -m pip install -e .
locqa check --source intl_ru.arb --target intl_kk.arb --glossary glossary.csv --out report.json
