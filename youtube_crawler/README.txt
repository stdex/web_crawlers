1. Создать приложение для работы с API:
1) Создать приложение в Google Developers Console:
https://console.developers.google.com/project
2) Подключить YouTube Data API к приложению:
https://console.developers.google.com/apis/library
3) Настроить данные доступа:
https://console.developers.google.com/apis/credentials
OAuth client ID - Web application - Authorized redirect URIs (на корень сайта).
4) Получить client ID и client secret.

2. Настройка скрипта:
1) Загрузить файлы на сервер или локалхост.
2) Открыть index.php, заполнить перменные $OAUTH2_CLIENT_ID и $OAUTH2_CLIENT_SECRET
$OAUTH2_CLIENT_ID = '253367390360-0q720p00jjv8v1vs5e79lin5adpc87bg.apps.googleusercontent.com';
$OAUTH2_CLIENT_SECRET = '1UcUeReetq34ixK3BMsbLIha';
2) Настроить время выполнения скрипта (опционально).
Установить set_time_limit(0) внутри скрипта, либо значение директивы max_execution_time в php.ini (в зависимости от настроек сервера).

