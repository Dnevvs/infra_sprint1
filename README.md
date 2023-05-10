# infra_sprint1
## **��� ����Kittygram � ���� ���**

���� �
```
    kit.blinklab.com
```
### 1.	����� ������infra_sprint1 ����� Kittygram � ��� ���� � GitHub � ���� ���.

```
    git clone 'git@github.com:Dnevvs/infra_sprint1.git'
```
### 2. ����������� ����

```
    cd infra_sprint1/
```
### 3. ��� �����������
```
    python3 -m venv venv
```
### 4. ����� �����������
```
    source venv/bin/activate
```
### 5. �������������
```
    pip install -r requirements.txt
```
### 6. ����������� backend-����� ����
```
    cd backend
```
### 7. ���� ����.
```
    python manage.py migrate
```
### 8.��� ��������.
```
    python manage.py createsuperuser
```
### 9. ���� �� settings.py ������Nano:
```
    nano infra_sprint1/backend/kittigram_backend/settings.py 
```
������� �� ��  ���� ALLOWED_HOSTS ����:
```
    ALLOWED_HOSTS = ['130.193.53.253', '127.0.0.1', 'localhost', kit.blinklab.com]  
```
### 10. ����������� infra_sprint1//frontend/ ����������
```
    npm i 
```
### 11.	�����WSGI-��� Gunicorn � ��� ����-����������Kittygram: 
������ ���������� ����������������������
����� ���gunicorn: 
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
    pip install gunicorn==20.1.0 
```
� ���� ����������� ���� ���������� manage.py, ������ Gunicorn
```
    cd infra_sprint1/backend
    gunicorn --bind 0.0.0.0:8080 kittygram_backend.wsgi 
```
����� ��� Ctrl-C

���� � �������� �� � ��� WSGI-����Gunicorn. ���� ��gunicorn-kittygram. 
```
    sudo nano /etc/systemd/system/gunicorn-kittigram.service
```
������� ����������������� ���WSGI-���. 
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
���������gunicorn-kittigram.service:
```
    sudo systemctl start gunicorn-kittigram 
```
������� ���� ���� ����Gunicorn ���� ������ ������ ����� ���� ����
```
    sudo systemctl enable gunicorn-kittigram
```
��������������������������, ������� ����:
```
    sudo systemctl status gunicorn-kittigram
```
### 12.	����������� Nginx
����������� 
```
    cd infra_sprint1/frontend/
```
����������
```	
    npm run build 
```
����� ���build �/var/www/
```
    sudo cp -r yc-user/infra_sprint1/frontend/build/. /var/www/infra_sprint1/
```
### 13.	���������� Nginx � ������� ���� ���� � ���� ����Kittygram: 
������� ���������������������, � �������server.
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
### 14. �������� ���������� � ��� ���� ����� media ������ /var/www/kittygram/. Django-����� ��������� ������� � ���� ����.
������ ����� �����MEDIA_ROOT ������ � ���������� media.
```
    /var/www/infra_sprint1/media
```
��������� ������ ����� ����� media ���Django-����� ������� ����. � �������������chown:
```
    sudo chown -R yc-user /var/www/infra_sprint1/media/
```  
�������������� �� ������/media/, ���Nginx ��, � �������� ���� �� ���� ���������������� ������� ������ ��� ������ ������ alias.
```
    location /media/ {
      alias /var/www/infra_sprint1/media/;
    }
```    
����������:
```    
    sudo nginx -t
    sudo systemctl reload nginx 
```    
### 15. ���������-����� � �������
������� Nano ���� �� settings.py, ����������� � �����STATIC_URL ����� �����STATIC_ROOT:
```
    STATIC_URL = 'static_backend'
    STATIC_ROOT = BASE_DIR / 'static_backend' 
```
��� ��������������-�����:
```
    cd infra_sprint1/
    python3 -m venv venv
    source venv/bin/activate
    cd infra_sprint1/backend
    python manage.py collectstatic 
```
������ ����backend/ ������������ static_backend/ � �� ���� ���-�����. 
����� ����� static_backend/ ������ /var/www/Taski/:
```
sudo cp -r infra_sprint1/backend/static_backend/ /var/www/infra_sprint1/ 
```
### 16. ���������� ���� � �����HTTPS.
```
    sudo certbot --nginx 
    sudo systemctl reload nginx 
```
### 17. ����������:
```
    sudo reboot
```