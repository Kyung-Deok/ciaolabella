#첫 빌드시 : docker-compose up --build
#이후 : docker-compose up
# 방화벽 설정으로 실행 안될때 iptables 초기화 
# sudo iptables -t filter -F && sudo iptables -t filter -X && sudo systemctl restart docker
version: "3"
services:
    nginx:
        image: nginx:1.14.0
        container_name : nginx_ciao
        volumes: 
            - /home/ubuntu/nginx/nginx.conf:/etc/nginx/nginx.conf
            - /home/ubuntu/ciaolabella:/home/ubuntu/ciaolabella
            - /etc/letsencrypt/:/etc/letsencrypt/
            - /var/www/certbot/:/var/www/letsencrypt/
        ports:
            - "80:80"
            - "443:443"
        depends_on : 
            - ciao1
            - ciao2
            - ciao3
        tty: true
        stdin_open: true

    ciao1:
        build : ./ciaolabella
        container_name : ciao1
        # volumes: 
            # - /home/ubuntu/ciaolabella:/home/ubuntu/ciaolabella
            # - ./config/gunicorn:/etc/systemd/system
        command: bash -c "python3 manage.py makemigrations ciaoadmin
            && python3 manage.py makemigrations lesswasteapp
            && python3 manage.py makemigrations member
            && python3 manage.py makemigrations nolabelapp
            && python3 manage.py migrate   
            && python3 manage.py collectstatic --noinput
            && gunicorn ciaolabella.wsgi -b 0.0.0.0:8990"
        ports: 
            - "8990:80"
        expose: 
            - "8990"
        tty: true
        stdin_open: true

    ciao1:
        build : ./ciaolabella
        container_name : ciao1
        # volumes: 
            # - /home/ubuntu/ciaolabella:/home/ubuntu/ciaolabella
            # - ./config/gunicorn:/etc/systemd/system
        command: bash -c "python3 manage.py makemigrations ciaoadmin
            && python3 manage.py makemigrations lesswasteapp
            && python3 manage.py makemigrations member
            && python3 manage.py makemigrations nolabelapp
            && python3 manage.py migrate   
            && python3 manage.py collectstatic --noinput
            && gunicorn ciaolabella.wsgi -b 0.0.0.0:8991"
        ports: 
            - "8991:80"
        expose: 
            - "8991"
        tty: true
        stdin_open: true

    ciao1:
        build : ./ciaolabella
        container_name : ciao1
        # volumes: 
            # - /home/ubuntu/ciaolabella:/home/ubuntu/ciaolabella
            # - ./config/gunicorn:/etc/systemd/system
        command: bash -c "python3 manage.py makemigrations ciaoadmin
            && python3 manage.py makemigrations lesswasteapp
            && python3 manage.py makemigrations member
            && python3 manage.py makemigrations nolabelapp
            && python3 manage.py migrate   
            && python3 manage.py collectstatic --noinput
            && gunicorn ciaolabella.wsgi -b 0.0.0.0:8992"
        ports: 
            - "8992:80"
        expose: 
            - "8992"
        tty: true
        stdin_open: true