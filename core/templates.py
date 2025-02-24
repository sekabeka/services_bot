
HELP_TEMPLATE = """
<i>Часто задаваемые вопросы:</i>

<b>Это конечная версия бота?</b>
<i>Нет</i>, бот активно развивается.

<b>Как я могу связаться с разработчиком?</b>
Связаться можно через <a href="https://t.me/devarsb">телеграмм</a>.

<b>Сколько стоит подключить подобного бота?</b>
Уточняйте у разработчика.

<b>Бот нацелен на работу с одним мастером?</b>
<i>Да</i>, текущая реализация подразумевает наличие одного мастера.

<b>Какие дальнейшие планы?</b>
Интеграция с CRM-системами, расширение количества мастеров, подключение медиафайлов.

<b>Для чего этот бот?</b>
Из личного опыта, мне показалось, что мастера тратят немало времени на то, чтобы записать клиента на услугу. Этот бот попытка в решении данного вопроса.
"""

START_TEMPLATE = """
<i>Привет 👀</i>

Я помощник салона красоты <b>BreStyle</b>!
Кратко о салоне:
- <i>5000+</i> довольных клиентов 🤝
- более 250 клиентов ежедневно 🌅
- выезд за город всем коллективом ежемесячно 🫂
- корпоративные подарки 🎁

И этого всего за полгода 🤯
Наши мастера каждые 6 месяцев проходят переквалификацию и повышают уровень своих знаний 👩‍💻

Я могу помочь тебе записаться на услугу и посмотреть свои бронирования 📒
Ниже отображаются кнопки с <b>доступными</b> действиями 🛠
"""

NOTIFY_TEMPLATE_FOR_EMPLOYEE = """
<b>Новое бронирование №{id}</b> 🚀

Услуга: <i>{title}</i> 🌅
Дата: {date} 📆
"""

NOTIFY_TEMPLATE_FOR_EMPLOYEE_MORNING = """
<b>Бронирования на сегодня 🚀</b>

{% for booking in bookings %}
- {{booking.date.time()}}
{% endfor %}
"""

NOTIFY_TEMPLATE_FOR_USER = """
<b>Напоминание о предстоящей записи №{id}</b> 🚀

Вы записаны на услугу <i>{title}</i> 📝
Дата бронирования: {date} 🕐
"""

BOOKINGS_TEMPLATE = """
Бронирование <b>№{{item.id}}</b>

Название услуги: <i>{{item.service.title}}</i> 🚀
Дата бронирования: <i>{{item.date}}</i> 📅

{% if item.user.tg_id != item.employee.tg_id %}
Мастер: <i>{{item.employee.firstname}} {{item.employee.lastname}}</i> 🙎‍♂️
{% endif %}
"""

NO_BOOKINGS_TEMPLATE = """
На данный момент у Вас нет активных бронирований 🌉

Вы можете записаться на услуги через меню 🙌
"""

SERVICE_TEMPLATE_LIST = """
<b>Услуга</b> <i>{{item.title}}</i> 🎈
<b>Услуга длится</b> <i>{{item.duration}} минут</i> ⏳
{% if item.description %}

<b>Описание</b> 💬
<i>{{item.description}}</i>
{% endif %}

Нажмите на кнопку \"К мастерам\", чтобы посмотреть цены и мастеров 
"""

SERVICE_EMPLOYEE_TEMPLATE_LIST = """
<b>Мастер</b> <i>{{item.lastname}} {{item.firstname}}</i> 🙎‍♂️
<b>Цена</b> {{item.price}} рублей 💰
{% if item.description %}

<b>Описание</b> 💬
<i>{{item.description}}</i>
{% endif %}

Нажмите на кнопку \"Записаться\" чтобы посмотреть список свободных дат и времени
"""

SERVICE_TEMPLATE_DATE = """
Вы выбрали услугу <b>{{dialog_data.service.title}}</b> 🎈
Вы выбрали мастера <b>{{dialog_data.employee.firstname}}</b> 🙎‍♂️

Укажите удобную для Вас дату 📅
"""

SERVICE_TEMPLATE_TIME = """
Вы выбрали услугу <b>{{dialog_data.service.title}}</b> 🎈
Вы выбрали мастера <b>{{dialog_data.employee.firstname}}</b> 🙎‍♂️
Вы выбрали дату <b>{{dialog_data.selected_date}}</b> 📅

Укажите удобное для Вас время 🕔
"""

SERVICE_TEMPLATE_CONFIRM = """
Проверьте информацию ❗️

<b>Услуга</b> {{dialog_data.service.title}} 🎈
<b>Дата бронирования</b> {{dialog_data.selected_date}} 📅
<b>Время бронирования</b> {{dialog_data.selected_time}} 🕔
<b>Мастер</b> <i>{{dialog_data.employee.firstname}} {{dialog_data.employee.lastname}}</i> 🙎‍♂️

Если все верно, нажмите на кнопку <b>\"Подтвердить\"</b> 🆗
Если допущена ошибка, вернитесь назад ↩️
"""

SERVICE_TEMPLATE_COMPLETE = """
<b>Бронирование №{{dialog_data.booking_id}}</b> 🌅

Вы записались на <b>{{dialog_data.service.title}}</b> <i>{{dialog_data.selected_datetime}}</i> 🎉
Мастер: <i>{{dialog_data.employee.firstname}} {{dialog_data.employee.lastname}}</i> 🌝

Вы получите напоминание о предстоящей записи 📩
"""
