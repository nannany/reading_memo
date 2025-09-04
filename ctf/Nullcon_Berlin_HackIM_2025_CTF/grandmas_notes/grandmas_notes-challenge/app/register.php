<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/config.php';

$username = trim($_POST['username'] ?? '');
$password = (string)($_POST['password'] ?? '');

if ($username === '' || $password === '') {
    $_SESSION['flash'] = "Missing username or password.";
    header('Location: index.php'); exit;
}

if (mb_strlen($password, 'UTF-8') > 16) {
    $_SESSION['flash'] = "Password must be at most 16 characters.";
    header('Location: index.php'); exit;
}

[$algo, $options] = hashing_algo_and_options();
$pwHash = password_hash($password, $algo, $options);

$pdo = db();
try {
    $pdo->beginTransaction();

    $stmt = $pdo->prepare("INSERT INTO users (username, password_hash, note) VALUES (?, ?, NULL)");
    $stmt->execute([$username, $pwHash]);
    $userId = (int)$pdo->lastInsertId();

    $ins = $pdo->prepare("INSERT INTO password_chars (user_id, position, char_hash) VALUES (?, ?, ?)");
    $chars = preg_split('//u', $password, -1, PREG_SPLIT_NO_EMPTY);
    foreach ($chars as $i => $ch) {
        $ins->execute([$userId, $i, sha256_hex($ch)]);
    }

    $pdo->commit();
    $_SESSION['flash'] = "Registered. You can now sign in.";
} catch (Throwable $e) {
    $pdo->rollBack();
    if (str_contains($e->getMessage(), 'Duplicate') || str_contains($e->getMessage(), 'UNIQUE')) {
        $_SESSION['flash'] = "Username already taken.";
    } else {
        $_SESSION['flash'] = "Registration failed.";
    }
}

header('Location: index.php');
