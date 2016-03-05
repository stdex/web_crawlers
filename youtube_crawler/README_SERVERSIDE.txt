1. Создать приложение для работы с API:
1) Создать приложение в Google Developers Console:
https://console.developers.google.com/project
2) Подключить YouTube Data API к приложению:
https://console.developers.google.com/apis/library
3) Настроить данные доступа:
https://console.developers.google.com/apis/credentials
Create credentials -> API key - Server key - Create.
4) Получить Key.

2. Настройка скрипта:
1) Загрузить файлы на сервер или локалхост.
2) Открыть youtube_crawler.php, заполнить перменные $apiKey, $channelId 
$apiKey = 'AIzaSyC9qkuVGtbLoMWRBTXm23L0_N8OKpcF9rQ';
$channelId = 'UCnv6T5lLfRxvbUk-lzGC4XQ';
2) Настроить запуск по cron по типу:
0 */2 * * * /home/www/path_dir/youtube_crawler.php


