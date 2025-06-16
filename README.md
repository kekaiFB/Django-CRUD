## Быстрый запуск

В корне проекта расположен скрипт `setup.sh`. Он автоматически
создаёт виртуальное окружение, устанавливает зависимости из
`requirements.txt`, пытается создать базу данных `diagnosisDB` (если
на системе установлен PostgreSQL) и применяет миграции.

```bash
bash setup.sh
```

После выполнения скрипта активируйте окружение и запустите сервер:

```bash
source env/bin/activate
cd src
python manage.py runserver
```

---


юзлес каждый раз(потом поймешь):
env\scripts\activate
cd src
python manage.py runserver



если будут ошибки(что скорее всего) и что то не установлено(устанавливается) пиши GPT постепенно решишь



клонируешь проект к себе на копмьютер
заходишь в папку проекта например в VS среде разработке

делаешь там такие команды 
C:\Users\rusla\OneDrive\Desktop\disser>cd Django-Ajax-CRUD 
C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD>virtualenv env
C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD>env\scripts\activate

после этого путь будет таким
(env) C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD>

Далее
(env) C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD>
pip install Django==3.2.7
pip install django-cors-headers==3.9.0
pip install djangorestframework==3.12.4
pip install psycopg2==2.9.1
pip install pytz==2021.1
pip install sqlparse==0.4.2 
pip install setuptools
pip install psycopg2-binary


открываешь редактор в ктором можешь создать БД на потсрегс, у меня это pgadmin4

и создаем БД с названием formulesDB




в файле settings.py ставишь свои данные учетки от постргес


именно юзер и пароль(скорее всего только пароль поменяй на свой)


дале заносим миграции из нашего джанго приложения в БД


(env) C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD\src>python manage.py makemigrations

(env) C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD\src>python manage.py migrate

  

ЗАПУСКАЕМ ПРОЕКТ(ЭТУ КОМНАДУ ВЫПОЛНЯТЬ ВСЕГДА КОГДА ХОЧЕШЬ ЗАПУСТИТЬ ПРОЕКТ) ВЫПОЛНЯТЬ ЕЕ СТРОГО ИЗ ПАПКИ SRC

(env) C:\Users\rusla\OneDrive\Desktop\disser\Django-Ajax-CRUD\src>python manage.py runserver

после открываем в браузере такой url http://127.0.0.1:8000/

По умолчанию создается суперпользователь с логином **admin** и паролем **admin**.
Войти можно по адресу http://127.0.0.1:8000/login/.

Новые зарегистрированные пользователи автоматически получают роль *Patient*.
Администратор может назначать пользователю роль *Doctor* через панель `/admin/`.


