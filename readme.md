# Тестовое задание на _Python_-программиста


# Обязательный уровень
  1. Запустить проект и ознакомиться с его документацией на странице `http://127.0.0.1:8000/redoc/`
     или `http://127.0.0.1:8000/docs/` 
     и выполнить каждый из запросов
  2. Изменить код проекта для получения дополнительных возможностей:
     - Добавить поиск городов аргументом `q` в запросе `/get-cities/`
     - Добавить возможность фильтрации пользователей по возрасту(минимальный/максимальный) в запросе `users-list`
     - Поправить ошибку в запросе `picnic-add`
     - Добавить метод регистрации на пикник `picnic-register`
  3. Высказать идеи рефакторинга файла `external_requests.py`
  4. Описать возможные проблемы при масштабировании проекта


     
## Продвинутый уровень
  1. Привести к нормальному виду:
     - Методы обращения к эндпойнтам
     - Названия эндпойнтов
     - Архитектуру и пути обращения к эндпойнтам
  2. Расписать все входные/выходные поля в документации (`/redoc/` или `/docs/`), описав их классами
  3. Оптимизировать работу с базой данных в запросе `/all-picnics/`
  4. Сменить базу данных с SQLite на PostgreSQL
  5. Отрефакторить файл `external_requests.py`
  6. Написать тесты


## Дополнительные задания
  - Сделать логирование в файл, который не будет очищаться после перезапуска в докере
  - Описать правильную архитектуру для проекта