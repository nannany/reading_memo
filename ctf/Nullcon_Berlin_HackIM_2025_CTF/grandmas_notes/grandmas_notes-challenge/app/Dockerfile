FROM php:8.3-apache

# Install PDO MySQL and Argon2 dependencies
RUN apt-get update && apt-get install -y libargon2-dev             && docker-php-ext-install pdo pdo_mysql             && rm -rf /var/lib/apt/lists/*

COPY . /var/www/html

RUN chmod +x /var/www/html/entrypoint.sh
ENTRYPOINT ["/var/www/html/entrypoint.sh"]
