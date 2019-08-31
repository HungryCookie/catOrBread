# Бот для определения кота

Имплементация Python Rest API бота.

Использовано: 
- `Python 3.6.8`
- `flask 1.1.1` - веб фреймворк был выбран, 
так как он легкий и удобный
- `sqlite3` - простая и эффективная (для данной задачи) база


## Как запускать

Просто запустить python файл:
__app.py__

Для обращения к боту:
В __post__ запросе в боди передается `user_id` и `answer`
в __json__ (__content_type__="application/json"), пример:
`{'user_id': #somenumber, 'answer': 'sth here'}`
