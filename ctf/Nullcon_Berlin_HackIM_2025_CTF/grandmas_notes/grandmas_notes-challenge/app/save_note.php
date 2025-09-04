<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/config.php';

if (empty($_SESSION['user']) || $_SESSION['user']['username'] == (getenv('ADMIN_USERNAME') ?: 'admin')) {
    header('Location: index.php'); exit;
}

$note = (string)($_POST['note'] ?? '');
$pdo = db();
$stmt = $pdo->prepare("UPDATE users SET note = ? WHERE id = ?");
$stmt->execute([$note, $_SESSION['user']['id']]);

$_SESSION['flash'] = "Note saved.";
header('Location: dashboard.php');
