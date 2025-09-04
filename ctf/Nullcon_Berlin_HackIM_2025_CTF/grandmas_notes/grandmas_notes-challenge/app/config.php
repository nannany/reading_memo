<?php
declare(strict_types=1);

$DB_HOST = getenv('DB_HOST') ?: 'db';
$DB_NAME = getenv('DB_NAME') ?: 'ctf';
$DB_USER = getenv('DB_USER') ?: 'ctfuser';
$DB_PASS = getenv('DB_PASS') ?: 'ctfpass';

function db(): PDO {
    static $pdo = null;
    global $DB_HOST, $DB_NAME, $DB_USER, $DB_PASS;
    if ($pdo === null) {
        $dsn = "mysql:host={$DB_HOST};dbname={$DB_NAME};charset=utf8mb4";
        $pdo = new PDO($dsn, $DB_USER, $DB_PASS, [
            PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
            PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
        ]);
    }
    return $pdo;
}

function sha256_hex(string $s): string {
    return hash('sha256', $s);
}

function hashing_algo_and_options(): array {
    $algoEnv = strtolower((string)(getenv('HASH_ALGO') ?: 'bcrypt'));
    if ($algoEnv === 'argon2id' && defined('PASSWORD_ARGON2ID')) {
        $options = [
            'memory_cost' => (int)(getenv('ARGON2_MEMORY_KB') ?: 65536),
            'time_cost'   => (int)(getenv('ARGON2_TIME_COST') ?: 1),
            'threads'     => (int)(getenv('ARGON2_THREADS') ?: 1),
        ];
        return [PASSWORD_ARGON2ID, $options];
    }
    $cost = (int)(getenv('BCRYPT_COST') ?: 8);
    return [PASSWORD_BCRYPT, ['cost' => $cost]];
}

function create_schema(): void {
    $pdo = db();
    $pdo->exec("
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(64) NOT NULL UNIQUE,
            password_hash VARCHAR(255) NOT NULL,
            note TEXT NULL
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ");

    $pdo->exec("
        CREATE TABLE IF NOT EXISTS password_chars (
            id INT AUTO_INCREMENT PRIMARY KEY,
            user_id INT NOT NULL,
            position INT NOT NULL, 
            char_hash CHAR(64) NOT NULL, 
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
            UNIQUE KEY uniq_user_pos (user_id, position)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    ");
}

function upsert_admin(): void {
    $pdo = db();
    $adminUser = getenv('ADMIN_USERNAME') ?: 'admin';
    $adminPass = getenv('ADMIN_PASSWORD') ?: 'changeme_admin';
    $adminNote = getenv('ADMIN_NOTE') ?: 'FAKEFLAG';

    [$algo, $options] = hashing_algo_and_options();
    $pwHash = password_hash($adminPass, $algo, $options);

    $pdo->beginTransaction();
    try {
        $stmt = $pdo->prepare("SELECT id FROM users WHERE username = ?");
        $stmt->execute([$adminUser]);
        $user = $stmt->fetch();

        if ($user) {
            $userId = (int)$user['id'];
            $stmt = $pdo->prepare("UPDATE users SET password_hash=?, note=? WHERE id=?");
            $stmt->execute([$pwHash, $adminNote, $userId]);

            $pdo->prepare("DELETE FROM password_chars WHERE user_id=?")->execute([$userId]);
        } else {
            $stmt = $pdo->prepare("INSERT INTO users (username, password_hash, note) VALUES (?, ?, ?)");
            $stmt->execute([$adminUser, $pwHash, $adminNote]);
            $userId = (int)$pdo->lastInsertId();
        }

        // Store per-character SHA-256 hashes for the hint mechanic
        $ins = $pdo->prepare("INSERT INTO password_chars (user_id, position, char_hash) VALUES (?, ?, ?)");
        $chars = preg_split('//u', $adminPass, -1, PREG_SPLIT_NO_EMPTY);
        foreach ($chars as $i => $ch) {
            $ins->execute([$userId, $i, sha256_hex($ch)]);
        }

        $pdo->commit();
    } catch (Throwable $e) {
        $pdo->rollBack();
        throw $e;
    }
}
