#!/usr/bin/env bash
set -euo pipefail
php /var/www/html/init.php || true
exec apache2-foreground
