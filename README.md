# infra_sprint1
## **Дпо покаKittygram н уаны сре**

Дмно и
```
    kit.blinklab.com
```
### 1.	Коиут рпзтрйinfra_sprint1 споко Kittygram с сог акут н GitHub н уаны сре.

```
    git clone 'git@github.com:Dnevvs/infra_sprint1.git'
```
### 2. Прхдмвдркои пока

```
    cd infra_sprint1/
```
### 3. Сзаё врулнеоржне
```
    python3 -m venv venv
```
### 4. Атвре врулнеоржне
```
    source venv/bin/activate
```
### 5. Утнвиамзвсмси
```
    pip install -r requirements.txt
```
### 6. Прхдмвдркои backend-пиоеи пока
```
    cd backend
```
### 7. Пиее мгаи.
```
    python manage.py migrate
```
### 8.Сзаё спроьоае.
```
    python manage.py createsuperuser
```
### 9. Окот фй settings.py врдкоеNano:
```
    nano infra_sprint1/backend/kittigram_backend/settings.py 
```
Ордкиут эо фй  всио ALLOWED_HOSTS дбвт:
```
    ALLOWED_HOSTS = ['130.193.53.253', '127.0.0.1', 'localhost', kit.blinklab.com]  
```
### 10. Прйиевдркои infra_sprint1//frontend/ ивплиекмну
```
    npm i 
```
### 11.	НсрйеWSGI-сре Gunicorn д рбт сбкн-пиоеимпокаKittygram: 
Пдлчтс куаноусреу атврйеврулнеоржнепокаи
утнвт пктgunicorn: 
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
    pip install gunicorn==20.1.0 
```
Д поек прйиевдркои пока вктрйлжтфй manage.py, изпсие Gunicorn
```
    cd infra_sprint1/backend
    gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi 
```
Отнвт сри Ctrl-C

Сзат е книуаины фй д дмн WSGI-среаGunicorn. Нзвт еоgunicorn-kittygram. 
```
    sudo nano /etc/systemd/system/gunicorn-kittigram.service
```
Оииевэо фйепрмтызпсапиоеи чрзWSGI-сре. 
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
Зпсиепоесgunicorn-kittigram.service:
```
    sudo systemctl start gunicorn-kittigram 
```
Дплиеьо кмно дбвт поесGunicorn всио атзпса оеаино ссеын уано срее
```
    sudo systemctl enable gunicorn-kittigram
```
Чоыпоеиьрбтсоонсьзпщноодмн, всоьутс кмно:
```
    sudo systemctl status gunicorn-kittigram
```
### 12.	Нсриамвбсре Nginx
Прйиевдркои 
```
    cd infra_sprint1/frontend/
```
ивплиекмну
```	
    npm run build 
```
соиут ппуbuild в/var/www/
```
    sudo cp -r yc-user/infra_sprint1/frontend/build/. /var/www/infra_sprint1/
```
### 13.	Нсрйевбсре Nginx д прнпалн зпоо ирбт с саио покаKittygram: 
Оииенжы нсрйивсщсвщмфйекниуаи, н внвмбоеserver.
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
### 14. Чоыфтгаи ктквооржлс н сйе сзат дркои media вдркои /var/www/kittygram/. Django-пиоеи бдтиплзвт эудркои д хаеи крио.
Внсрйа бкнад кнтныMEDIA_ROOT уаиепт д сзанйдркои media.
```
    /var/www/infra_sprint1/media
```
Нзаьеткщг плзвтл ваеье дркои media чоыDjango-пиоеи мгосхат крик. Д эооиплзйекмнуchown:
```
    sudo chown -R yc-user /var/www/infra_sprint1/media/
```  
Оииевфйекниуаи бо спеисм/media/, чоыNginx за, и ккйдркои збрт фт кткв Ттвмнжонмоопрбтт смсотлн ирзбаь стм ккрбтт сдркио alias.
```
    location /media/ {
      alias /var/www/infra_sprint1/media/;
    }
```    
Прзпсиесре:
```    
    sudo nginx -t
    sudo systemctl reload nginx 
```    
### 15. Пдооиьбкн-пиоеи д соасаии
Чрзрдко Nano окот фй settings.py, уаиенвезаеи д кнтныSTATIC_URL исзат кнтнуSTATIC_ROOT:
```
    STATIC_URL = 'static_backend'
    STATIC_ROOT = BASE_DIR / 'static_backend' 
```
Тпр мжосбаьсаиубкн-пиоеи:
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
    cd infra_sprint1/backend
    python manage.py collectstatic 
```
Вдркои покаbackend/ бдтсзаадркои static_backend/ с ве саио бкн-пиоеи. 
Соиут дркои static_backend/ вдркои /var/www/Taski/:
```
sudo cp -r infra_sprint1/backend/static_backend/ /var/www/infra_sprint1/ 
```
### 16. Нсрйешфоаи зпоо п поооуHTTPS.
```
    sudo certbot --nginx 
    sudo systemctl reload nginx 
```
### 17. Прзгуиесре:
```
    sudo reboot
```