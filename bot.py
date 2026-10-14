import logging
import io
from contextlib import redirect_stdout
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder, ContextTypes, CommandHandler, MessageHandler, CallbackQueryHandler, filters
)
from apscheduler.schedulers.background import BackgroundScheduler

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

# ВСТАВТЕ СВІЙ ТОКЕН ТУТ
TOKEN = "8307859199:AAEg-U7bOuLdE3Hlk705kslm95MMmLByVys"

# Професійна програма: розділена на чисту теорію та окремі завдання
LESSONS = [
    {
        "title": "Модуль 1.1: Цілі числа (int) — Облік кишенькових грошей",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Уявіть, що ви збираєте гроші у скарбничку. Кількість монет або цілих гривень — це **цілі числа** (`int`). У них немає ніяких копійок чи дробів.\n\n"
            "💻 **Як це в коді:**\n"
            "Ми створюємо коробку (змінну) і кладемо туди число:\n"
            "```python\n"
            "pocket_money = 250\n"
            "my_savings = 1000\n"
            "total = pocket_money + my_savings\n"
            "print(total)  # Виведе 1250\n"
            "```\n"
            "Ділення націло (`//`) ідеально підходить, коли треба поділити гроші чи предмети порівну без залишку."
        ),
        "task": "Створіть дві цілочисельні змінні `x = 25` та `y = 4`. Збережіть результат цілочисельного ділення `x` на `y` у змінну `result` і виведіть її через `print()`.",
        "check": lambda lv: 'result' in lv and lv['result'] == 6,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\na = 17\nb = 3\nresult = a // b  # Отримаємо 5\nprint(result)\n```",
        "resources": "🔗 **Корисні матеріали до Уроку 1.1:**\n• [Офіційна документація Python про числа](https://docs.python.org/3/library/stdtypes.html#numeric-types-int-float-complex)\n• [Підручник Real Python — Numbers](https://realpython.com/python-numbers/)"
    },
    {
        "title": "Модуль 1.2: Дробові числа (float) — Розрахунок у магазині",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Коли ви купуєте продукти у супермаркеті, ціни рідко бувають цілими. Наприклад, пачка макаронів коштує `49.50` грн. Числа з десятковою крапкою у програмуванні називаються **float**.\n\n"
            "💻 **Як це в коді:**\n"
            "Пам'ятайте головне правило: замість коми ставиться **крапка** (`.`):\n"
            "```python\n"
            "apple_price = 12.75\n"
            "count = 3\n"
            "total_cost = apple_price * count\n"
            "print(total_cost)\n"
            "```"
        ),
        "task": "Створіть дробову змінну `item_price = 49.5` та цілу змінну `quantity = 3`. Обчисліть загальну вартість покупки (`item_price * quantity`) у змінній `total` і виведіть її.",
        "check": lambda lv: 'total' in lv and lv['total'] == 148.5,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nweight = 1.5\ncount = 4\ntotal = weight * count\nprint(total)\n```",
        "resources": "🔗 **Корисні матеріали до Уроку 1.2:**\n• [W3Schools Python Numbers](https://www.w3schools.com/python/python_numbers.asp)\n• [Programiz Float Numbers](https://www.programiz.com/python-programming/numbers)"
    },
    {
        "title": "Модуль 1.3: Рядки (str) — Анкетування та бейджики",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Будь-який текст — імена, адреси, повідомлення в месенджері — це **рядки** (`str`). На бейджику на конференції написано ваше ім'я, і комп'ютер сприймає його як текст у лапках.\n\n"
            "💻 **Як це в коді:**\n"
            "Сучасні розробники об'єднують текст і змінні за допомогою **f-рядків** (форматованих рядків):\n"
            "```python\n"
            "name = 'Ірина'\n"
            "role = 'розробниця'\n"
            "badge = f'Привіт, мене звати {name}, я {role}.'\n"
            "print(badge)\n"
            "```"
        ),
        "task": "Створіть змінні `city = 'Харків'` та `year = 2026`. За допомогою f-рядка сформуйте текст у змінній `info` та виведіть його.",
        "check": lambda lv: 'info' in lv and isinstance(lv.get('info'), str),
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nlang = 'Python'\nver = 3\nmsg = f'Мова {lang} версії {ver}'\nprint(msg)\n```",
        "resources": "🔗 **Корисні матеріали до Уроку 1.3:**\n• [Real Python — Python Strings](https://realpython.com/python-strings/)\n• [Guide to f-strings in Python](https://realpython.com/python-f-strings/)"
    },
    {
        "title": "Модуль 2.1: Функція input() — Онлайн-замовлення",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Коли ви замовляєте піцу в інтернеті, сайт запитує ваше ім'я чи кількість порцій через поле введення. У Python за це відповідає функція `input()`.\n\n"
            "💻 **Як це в коді:**\n"
            "```python\n"
            "user_age = int('16')\n"
            "double_age = user_age * 2\n"
            "print(double_age)\n"
            "```"
        ),
        "task": "Створіть змінну `double_val`, яка містить результат множення числа `50` на `2` (можете записати `double_val = 50 * 2`). Виведіть її.",
        "check": lambda lv: 'double_val' in lv and lv['double_val'] == 100,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nval = 20\nres = val * 5\nprint(res)\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 2.1:**\n• [Python Input/Output Tutorial](https://www.programiz.com/python-programming/input-output-import)\n• [Real Python — Input and Output](https://realpython.com/python-input-output/)"
    },
    {
        "title": "Модуль 2.2: Умови if-elif-else — Пропуск у кінотеатр",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "На вході в кінотеатр контролер перевіряє ваш вік: якщо вам більше 16 років — вас пускають на дорослий сеанс, інакше — ні. Це класична життєва **умова**.\n\n"
            "💻 **Як це в коді:**\n"
            "```python\n"
            "age = 17\n"
            "if age >= 16:\n"
            "    print('Доступ дозволено')\n"
            "else:\n"
            "    print('Доступ обмежено')\n"
            "```"
        ),
        "task": "Створіть змінну `points = 70`. Напишіть умову: якщо `points >= 80`, виведіть `'Високий'`, інакше виведіть `'Базовий'` через `print()`.",
        "check": lambda lv: 'points' in lv,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nage = 15\nif age >= 18:\n    print('Дорослий')\nelse:\n    print('Підліток')\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 2.2:**\n• [Python Conditional Statements (W3Schools)](https://www.w3schools.com/python/python_conditions.asp)\n• [Real Python — Conditional Statements](https://realpython.com/python-conditional-statements/)"
    },
    {
        "title": "Модуль 3.1: Цикли while — Таймер зворотного відліку",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Уявіть мікрохвильову піч, яка розігріває їжу: таймер показує 3 хвилини, потім 2, 1, і лунає дзвінок. Поки умова (час більше нуля) правдива — цикл працює.\n\n"
            "💻 **Як це в коді:**\n"
            "```python\n"
            "n = 3\n"
            "while n > 0:\n"
            "    print(n)\n"
            "    n -= 1\n"
            "```"
        ),
        "task": "Створіть цикл `while`, який зменшує змінну `n = 3` до нуля і виводить кожне значення через `print()`. Переконайтеся, що на кінці `n` дорівнює 0.",
        "check": lambda lv: 'n' in lv and lv['n'] == 0,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\ni = 2\nwhile i > 0:\n    print(i)\n    i -= 1\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 3.1:**\n• [Python While Loops (W3Schools)](https://www.w3schools.com/python/python_while_loops.asp)"
    },
    {
        "title": "Модуль 4.1: Списки (List) — Плейлист у плеєрі",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Ваш музичний плейлист у смартфоні містить кілька пісень поспіль. Ви можете додавати нові треки в кінець списку за допомогою кнопки «Додати».\n\n"
            "💻 **Як це в коді:**\n"
            "```python\n"
            "playlist = ['Трек 1', 'Трек 2']\n"
            "playlist.append('Трек 3')\n"
            "print(len(playlist))\n"
            "```"
        ),
        "task": "Створіть список `items = ['ручка', 'зошит']`. За допомогою методу `.append()` додайте `'олівець'` та виведіть довжину списку через `print(len(items))`.",
        "check": lambda lv: 'items' in lv and isinstance(lv.get('items'), list) and len(lv.get('items')) == 3,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nnums = [1, 2]\nnums.append(3)\nprint(len(nums))\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 4.1:**\n• [Python Lists (W3Schools)](https://www.w3schools.com/python/python_lists.asp)"
    },
    {
        "title": "Модуль 5.1: Функції — Калькулятор знижок",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Уявіть кавовий автомат: ви кидаєте монетку і натискаєте кнопку «Лате». Автомат виконує заздалегідь закладену інструкцію і видає каву. У програмуванні це **функція** з оператором `return`.\n\n"
            "💻 **Як це в коді:**\n"
            "```python\n"
            "def calculate_double(a, b):\n"
            "    return a * b\n"
            "```"
        ),
        "task": "Створіть функцію `multiply(a, b)`, яка повертає добуток двох чисел через `return`.",
        "check": lambda lv: 'multiply' in lv and callable(lv.get('multiply')),
        "analogy": "💡 *Зразок на схожу тему:*\n```python\ndef add(x, y):\n    return x + y\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 5.1:**\n• [Python Functions (W3Schools)](https://www.w3schools.com/python/python_functions.asp)"
    },
    {
        "title": "Модуль 6.1: Обробка винятків — Захист від збоїв каси",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Якщо касир у магазині випадково спробує виконати некоректну дію, каса не повинна зависати — вона має вивести попередження через блок `try-except`."
        ),
        "task": "Напишіть блок `try-except`, який намагається виконати `int('abc')` і перехоплює помилку `ValueError`.",
        "check": lambda lv: True,
        "analogy": "💡 *Зразок на схожу тему:*\n```python\ntry:\n    x = int('hello')\nexcept ValueError:\n    print('Помилка')\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 6.1:**\n• [Python Exceptions (W3Schools)](https://www.w3schools.com/python/python_try_except.asp)"
    },
    {
        "title": "Модуль 7.1: ООП та конструктор __init__ — Фабрика автомобілів",
        "theory": (
            "📌 **ЖИТТЄВИЙ ПРИКЛАД:**\n"
            "Уявіть завод, який випускає автомобілі за одним кресленням (класом). Для задання властивостей використовується конструктор `__init__`."
        ),
        "task": "Створіть клас `Book` з конструктором `__init__(self, title)`, який зберігає назву у `self.title`.",
        "check": lambda lv: 'Book' in lv and callable(lv.get('Book')),
        "analogy": "💡 *Зразок на схожу тему:*\n```python\nclass Dog:\n    def __init__(self, name):\n        self.name = name\n```",
        "resources": "🔗 **Корисні матеріали до Модуля 7.1:**\n• [Python Classes (W3Schools)](https://www.w3schools.com/python/python_classes.asp)"
    }
]

FULL_PROGRAM_TEXT = (
    "📚 **ПРОФЕСІЙНА ПРОГРАМА НАВЧАННЯ PYTHON:**\n\n"
    "• **Модуль 1:** Базові типи даних на життєвих прикладах (цілі числа, дроби, текст).\n"
    "• **Модуль 2:** Інтерактивність (`input`) та логічні розгалуження (`if-else`).\n"
    "• **Модуль 3:** Циклічні алгоритми (`while`).\n"
    "• **Модуль 4:** Колекції та списки даних.\n"
    "• **Модуль 5:** Функції та повернення результатів (`return`).\n"
    "• **Модуль 6:** Безпека та обробка винятків (`try-except`).\n"
    "• **Модуль 7:** Архітектура ООП — класи та конструктор `__init__`.\n\n"
    "Натисніть кнопку нижче, щоб повернутися до уроків:"
)

user_progress = {}
user_passed_lessons = {}
bot_application = None

def get_user_progress(user_id):
    if user_id not in user_progress:
        user_progress[user_id] = 0
    return user_progress[user_id]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_progress[user_id] = 0
    user_passed_lessons[user_id] = []
    
    keyboard = [
        [InlineKeyboardButton("📖 Переглянути всю програму курсу", callback_data="show_program")],
        [InlineKeyboardButton("👉 Перейти до першого уроку", callback_data="show_current_lesson")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_text = (
        "Вітаємо.\n\n"
        "Раді, що ви зацікавились навчанням Python.\n\n"
        "Виберіть потрібну дію за допомогою кнопок нижче:"
    )
    
    await update.message.reply_text(welcome_text, parse_mode='Markdown', reply_markup=reply_markup)

async def send_lesson_theory(target_message, user_id):
    idx = get_user_progress(user_id)
    
    if idx >= len(LESSONS):
        await target_message.reply_text("🎉 Вітаю! Ви успішно пройшли всі уроки цього професійного курсу!")
        return

    lesson = LESSONS[idx]
    
    # Тільки теорія та дві кнопки відповідно до запиту
    keyboard = [
        [InlineKeyboardButton("📝 Подивитися практичне завдання", callback_data=f"show_task_{idx}")],
        [InlineKeyboardButton("🔗 Корисні матеріали", callback_data=f"show_resources_{idx}")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    text = (
        f"📘 *Урок {idx + 1} з {len(LESSONS)}: {lesson['title']}*\n\n"
        f"{lesson['theory']}\n\n"
        f"Ознайомтеся з теорією та натисніть відповідну кнопку нижче:"
    )
    
    await target_message.reply_text(text, parse_mode='Markdown', reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    
    if query.data == "show_program":
        keyboard = [[InlineKeyboardButton("👉 Повернутися до уроків", callback_data="show_current_lesson")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.message.reply_text(FULL_PROGRAM_TEXT, parse_mode='Markdown', reply_markup=reply_markup)
        
    elif query.data == "show_current_lesson":
        await send_lesson_theory(query.message, user_id)
        
    elif query.data.startswith("show_task_"):
        idx = int(query.data.split("_")[2])
        lesson = LESSONS[idx]
        task_text = (
            f"🎯 *Практичне завдання до уроку {idx + 1}:*\n\n"
            f"{lesson['task']}\n\n"
            f"✍️ Надішліть свій код сюди у чат для перевірки."
        )
        await query.message.reply_text(task_text, parse_mode='Markdown')
        
    elif query.data.startswith("show_resources_"):
        idx = int(query.data.split("_")[2])
        lesson = LESSONS[idx]
        await query.message.reply_text(lesson['resources'], parse_mode='Markdown')

async def handle_code(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    idx = get_user_progress(user_id)

    if idx >= len(LESSONS):
        await update.message.reply_text("Ви вже завершили курс! Напишіть /start, щоб почати спочатку.")
        return

    user_code = update.message.text
    local_vars = {}
    f_out = io.StringIO()
    output_str = ""
    success = False
    error_msg = ""

    try:
        with redirect_stdout(f_out):
            exec(user_code, {}, local_vars)
        output_str = f_out.getvalue()

        lesson = LESSONS[idx]
        if lesson["check"](local_vars):
            success = True
        else:
            error_msg = "Код виконано без синтаксичних помилок, але умова завдання ще не повністю виконана."
    except Exception as e:
        error_msg = f"Помилка виконання: {e}"

    response = ""
    if output_str:
        response += f"Вивід програми (print):\n{output_str}\n"

    if success:
        response += "\n✅ ВІТАЮ! Завдання виконано успішно!"
        
        if user_id not in user_passed_lessons:
            user_passed_lessons[user_id] = []
        user_passed_lessons[user_id].append(LESSONS[idx])

        user_progress[user_id] += 1
        await update.message.reply_text(response)
        
        if user_progress[user_id] < len(LESSONS):
            keyboard = [[InlineKeyboardButton("➡️ Перейти до наступного уроку", callback_data="show_current_lesson")]]
            reply_markup = InlineKeyboardMarkup(keyboard)
            await update.message.reply_text("Натисніть кнопку нижче, щоб продовжити навчання:", reply_markup=reply_markup)
        else:
            await update.message.reply_text("🏆 Неймовірно! Ви пройшли повний професійний курс Python!")
    else:
        lesson = LESSONS[idx]
        response += f"\n❌ ПОМИЛКА:\n{error_msg}\n\n{lesson['analogy']}\n\nПроаналізуйте зразок вище, виправте код і надішліть його знову."
        await update.message.reply_text(response, parse_mode='Markdown')

def main():
    app = ApplicationBuilder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_code))
    
    print("🤖 Бот із розділеною теорією та кнопками успішно запущено!")
    app.run_polling()

if __name__ == '__main__':
    main()