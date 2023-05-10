# infra_sprint1
## **Деплой проекта Kittygram на удалённый сервер**

Доменное имя
```
    kit.blinklab.com
```
### 1.	Клонируйте репозиторий infra_sprint1 с проектом Kittygram со своего аккаунта на GitHub на удалённый сервер.

```
    git clone 'git@github.com:Dnevvs/infra_sprint1.git'
```
### 2. Переходим в директорию проекта.

```
    cd infra_sprint1/
```
### 3. Создаём виртуальное окружение.
```
    python3 -m venv venv
```
### 4. Активируем виртуальное окружение.
```
    source venv/bin/activate
```
### 5. Устанавливаем зависимости.
```
    pip install -r requirements.txt
```
### 6. Переходим в директорию backend-приложения проекта.
```
	cd backend
```
### 7. Применяем миграции.
```
	python manage.py migrate
```
### 8.Создаём суперпользователя.
```
    python manage.py createsuperuser
```
### 9. Откройте файл settings.py в редакторе Nano:
```
    nano infra_sprint1/backend/kittigram_backend/settings.py 
```
Отредактируйте этот файл — в список ALLOWED_HOSTS добавьте:
```
	ALLOWED_HOSTS = ['130.193.53.253', '127.0.0.1', 'localhost', ‘kit.blinklab.com’]  
```
### 10. Перейдите в директорию infra_sprint1//frontend/ и выполните команду:
```
	npm i 
```
### 11.	Настройте WSGI-сервер Gunicorn для работы с бэкенд-приложением проекта Kittygram: 
Подключитесь к удалённому серверу, активируйте виртуальное окружение проекта и 
установите пакет gunicorn: 
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
    pip install gunicorn==20.1.0 
```
Для проверки перейдите в директорию проекта, в которой лежит файл manage.py, и запустите  Gunicorn
```
	cd infra_sprint1/backend
	gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi 
```
Остановите сервис Ctrl-C

Создайте ещё конфигурационный файл для демона WSGI-сервера Gunicorn. Назовите его gunicorn-kittygram. 
```
    sudo nano /etc/systemd/system/gunicorn-kittigram.service
```
Опишите в этом файле параметры запуска приложения через WSGI-сервер. 
```
[Unit]
Description=gunicorn daemon 

After=network.target 

[Service]
User=yc-user 

WorkingDirectory=/home/yc-user/infra_sprint1/backend/

ExecStart=/home/yc-user/infra_sprint1/venv/bin/gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi

[Install]
WantedBy=multi-user.target
```
Запустите процесс gunicorn-kittigram.service:
```
	sudo systemctl start gunicorn-kittigram 
```
Дополнительной командой добавьте процесс Gunicorn в список автозапуска  операционной системы на удалённом сервере:
```
	sudo systemctl enable gunicorn-kittigram
```
Чтобы проверить работоспособность запущенного демона, воспользуйтесь командой:
```
	sudo systemctl status gunicorn-kittigram
```
### 12.	Настраиваем веб-сервер Nginx
Перейдите в директорию 
```
    cd infra_sprint1/frontend/
```
и выполните команду:
```	
    npm run build 
```
скопируйте папку build в /var/www/
```
	sudo cp -r yc-user/infra_sprint1/frontend/build/. /var/www/infra_sprint1/
```
### 13.	Настройте веб-сервер Nginx для перенаправления запросов и работы со статикой проекта Kittygram: 
Опишите нужные настройки в существующем файле конфигурации, но в новом блоке server.
```
    sudo nano /etc/nginx/sites-enabled/default 
```
```
server {
    server_name 130.193.53.253 kit.blinklab.com;

    location /api/ {
        proxy_pass http://127.0.0.1:8080;
    }

    location /admin/ {
        proxy_pass http://127.0.0.1:8080;
    }

    location / {
        root   /var/www/infra_sprint1;
        index  index.html index.htm;
        try_files $uri /index.html;
    }

    location /sentry-debug/ {
        proxy_pass http://127.0.0.1:8080;
    }

}
```
### 14. Чтобы фотографии котиков отображались на сайте, создайте директорию media в директории /var/www/kittygram/. Django-приложение будет использовать эту директорию для хранения картинок.
В настройках бекенда для константы MEDIA_ROOT укажите путь до созданной директории media.
```
    /var/www/infra_sprint1/media
```
Назначьте текущего пользователя владельцем директории media чтобы Django-приложение могло сохранять картинки. Для этого используйте команду chown:
```
    sudo chown -R yc-user /var/www/infra_sprint1/media/
```  
Опишите в файле конфигурации блок с префиксом /media/, чтобы Nginx знал, из какой директории забирать фото котиков. Тут вам нужно немного поработать самостоятельно и разобраться с тем, как работать с директивой alias.
```
	location /media/ {
	  alias /var/www/infra_sprint1/media/;
	}
```    
Перезапустите сервер:
```    
    sudo nginx -t
    sudo systemctl reload nginx 
```    
### 15. Подготовить бэкенд-приложение для сбора статики.
Через редактор Nano откройте файл settings.py, укажите новое значение для константы STATIC_URL и создайте константу STATIC_ROOT:
```
    STATIC_URL = 'static_backend'
    STATIC_ROOT = BASE_DIR / 'static_backend' 
```
Теперь можно собрать статику бэкенд-приложения:
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
	cd infra_sprint1/backend
    python manage.py collectstatic 
```
В директории проекта backend/ будет создана директория static_backend/ со всей статикой бэкенд-приложения. 
Скопируйте директорию static_backend/ в директорию /var/www/Taski/:
```
sudo cp -r infra_sprint1/backend/static_backend/ /var/www/infra_sprint1/ 
```
### 16. Настройте шифрование запросов по протоколу HTTPS.
```
    sudo certbot --nginx 
    sudo systemctl reload nginx 
```
### 17. Перезагрузите сервер:
```
    sudo reboot
```
