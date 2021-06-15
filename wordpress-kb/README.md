# WordPress - Knowledge Base

The example provided uses the following as defaults, and should be updated according to your specifications.

- port 8080 for http
- port 8443 for https
- `./wordpress` volume mount for wordpress files
- `./dbdata` volume mount for mysql files

## Configure

### .env

Create a file named `.env` and update to your specification

```
cp env.template .env
```

Example `.env`:

```env
MYSQL_ROOT_PASSWORD=rootpassword123!
MYSQL_USER=wordpress
MYSQL_PASSWORD=userpassword123!
```

### docker-compose.yml

Update `services:`

- `db:volumes:` mysql volume mount
- `wordpress:volumes:` wordpress volume mount
- `webserver:ports:` http port (maps to 80 of container)
- `webserver:ports:` https port (maps to 443 of container)
- `webserver:wordpress:` wordpress volume mount
- `webserver:ssl:` trusted SSL certificate location

Example `docker-compose.yml`:

```yaml
version: '3.8'
services:

  db:
    image: mysql:8.0
    container_name: db-kb
    restart: unless-stopped
    command: '--default-authentication-plugin=mysql_native_password'
    env_file: .env
    environment:
      - MYSQL_DATABASE=wordpress
    volumes:
      - ./dbdata:/var/lib/mysql

  wordpress:
    image: wordpress:5-fpm
    depends_on:
      - db
    container_name: wordpress-kb
    restart: unless-stopped
    volumes:
      - ./wordpress:/var/www/html
      # - /path/to/repo/myTheme/:/var/www/html/wp-content/themes/myTheme
    env_file: .env
    environment:
      - WORDPRESS_DB_HOST=db:3306
      - WORDPRESS_DB_USER=$MYSQL_USER
      - WORDPRESS_DB_PASSWORD=$MYSQL_PASSWORD
      - WORDPRESS_DB_NAME=wordpress

  webserver:
    depends_on:
      - wordpress
    image: nginx:1.15.12-alpine
    container_name: nginx-kb
    restart: unless-stopped
    ports:
      - "8080:80"
      - "8443:443"
    volumes:
      - ./wordpress:/var/www/html
      - ./nginx/default.conf:/etc/nginx/conf.d/default.conf
      - ./ssl:/etc/ssl:ro
```

### nginx/default.conf

Update:

- server location port 80 rewrite statement (update https port)

Example `default.conf`:

```nginx
# default.conf
# redirect to HTTPS
server {
    listen 80;
    listen [::]:80;
    server_name $host;
    location / {
        # update port as needed for host mapped https
        rewrite ^ https://$host:8443$request_uri? permanent;
    }
}

server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;
    server_name $host;
    index index.php index.html index.htm;
    root /var/www/html;
    server_tokens off;
    # update ssl files as required by your deployment
    ssl_certificate /etc/ssl/fullchain.pem;
    ssl_certificate_key /etc/ssl/privkey.pem;
    # some security headers ( optional )
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header Referrer-Policy "no-referrer-when-downgrade" always;
    add_header Content-Security-Policy "default-src * data: 'unsafe-eval' 'unsafe-inline'" always;
    location / {
        try_files $uri $uri/ /index.php$is_args$args;
    }
    location ~ \.php$ {
        try_files $uri = 404;
        fastcgi_split_path_info ^(.+\.php)(/.+)$;
        fastcgi_pass wordpress:9000;
        fastcgi_index index.php;
        include fastcgi_params;
        fastcgi_param SCRIPT_FILENAME $document_root$fastcgi_script_name;
        fastcgi_param PATH_INFO $fastcgi_path_info;
    }
    location ~ /\.ht {
        deny all;
    }
    location = /favicon.ico {
        log_not_found off; access_log off;
    }
    location = /favicon.svg {
        log_not_found off; access_log off;
    }
    location = /robots.txt {
        log_not_found off; access_log off; allow all;
    }
    location ~* \.(css|gif|ico|jpeg|jpg|js|png)$ {
        expires max;
        log_not_found off;
    }
}

```

## Deploy

```
docker-compose pull
docker-compose up -d
```

Once deployed you should see three running containers with only the http and https ports exposed to the outside world.

```console
$ docker-compose ps
    Name                  Command               State                                      Ports
------------------------------------------------------------------------------------------------------------------------------------
db-kb          docker-entrypoint.sh --def ...   Up      3306/tcp, 33060/tcp
nginx-kb       nginx -g daemon off;             Up      0.0.0.0:8443->443/tcp,:::8443->443/tcp, 0.0.0.0:8080->80/tcp,:::8080->80/tcp
wordpress-kb   docker-entrypoint.sh php-fpm     Up      9000/tcp
```

Verify that your new site is running and immediately follow the on-screen prompts to create an Adminstrative user
