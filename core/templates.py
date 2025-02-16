
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
<i>Привет!👀</i>

Я могу помочь тебе записаться на услугу и посмотреть свои бронирования!📒
Ниже отображаются кнопки с <b>доступными</b> действиями🛠.

Бо&#769;льшую часть текста можно редактировать и настраивать под себя.
"""

NOTIFY_TEMPLATE_FOR_OWNER = """
<b>Новое бронирование №{id}</b>

Услуга: <i>{title}</i>
Дата: {date}
"""

NOTIFY_TEMPLATE_FOR_USER = """
<b>Напоминание о предстоящей записи №{id}</b>

Вы записаны на услугу <i>{title}</i>
Время бронирования: {date}
"""

BOOKINGS_TEMPLATE = """
Бронирование <b>№{{item.id}}</b>

Оказываемая услуга: {{item.service.title}}
Дата бронирования: {{item.date}}

"""

NO_BOOKINGS_TEMPLATE = """
На данный момент у Вас нет активных бронирований!
"""

SERVICE_TEMPLATE_LIST = """
Название услуги: <b>{{item.title}}</b>
Цена услуги: <i>{{item.price}}</i> рублей
Длительность услуги: {{item.duration}} минут
"""

SERVICE_TEMPLATE_DATE = """
Вы выбрали услугу <b>{{dialog_data.service.title}}</b>
Укажите удобную для Вас дату.
"""

SERVICE_TEMPLATE_TIME = """
Вы выбрали дату <b>{{dialog_data.selected_date}}</b>
Укажите удобное для Вас время.
"""

SERVICE_TEMPLATE_CONFIRM = """
Проверьте информацию:

<b>Услуга</b>
{{dialog_data.service.title}}
<b>Дата бронирования</b>
{{dialog_data.selected_date}}
<b>Время бронирования</b>
{{dialog_data.selected_time}}

Если все верно, нажмите на кнопку <b>\"Подтвердить\"</b>.
Если допущена ошибка, вернитесь назад.
"""

SERVICE_TEMPLATE_COMPLETE = """
<b>Бронирование №{{dialog_data.record.id}}</b>

Вы записались на <b>{{dialog_data.record.service.title}}</b> <i>{{dialog_data.record.date}}</i>

Вы получите напоминание о предстоящей записи!
"""
