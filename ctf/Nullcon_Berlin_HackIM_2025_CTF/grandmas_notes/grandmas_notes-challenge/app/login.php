<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/config.php';

$username = trim($_POST['username'] ?? '');
$password = (string)($_POST['password'] ?? '');

$pdo = db();

$stmt = $pdo->prepare("SELECT id, username, password_hash FROM users WHERE username = ?");
$stmt->execute([$username]);
$user = $stmt->fetch();

if (!$user) {
    $_SESSION['flash'] = "Invalid username or password.";
    header('Location: index.php'); exit;
}

if (password_verify($password, $user['password_hash'])) {
    $_SESSION['user'] = ['id' => (int)$user['id'], 'username' => $user['username']];
    header('Location: dashboard.php'); exit;
}

$chars = preg_split('//u', $password, -1, PREG_SPLIT_NO_EMPTY);
$q = $pdo->prepare("SELECT position, char_hash FROM password_chars WHERE user_id = ? ORDER BY position ASC");
$q->execute([(int)$user['id']]);
$stored = $q->fetchAll();

$correct = 0;
$limit = min(count($chars), count($stored));
for ($i = 0; $i < $limit; $i++) {
    $enteredCharHash = sha256_hex($chars[$i]);
    if (hash_equals($stored[$i]['char_hash'], $enteredCharHash)) {
        $correct++;
    } else {
        break;
    }
}
$_SESSION['flash'] = "Invalid password, but you got {$correct} characters correct!";
header('Location: index.php');
