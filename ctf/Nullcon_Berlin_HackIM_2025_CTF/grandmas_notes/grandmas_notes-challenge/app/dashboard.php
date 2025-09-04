<?php
declare(strict_types=1);
session_start();
require __DIR__ . '/config.php';

if (empty($_SESSION['user'])) {
    header('Location: index.php'); exit;
}

$pdo = db();
$stmt = $pdo->prepare("SELECT note FROM users WHERE id = ?");
$stmt->execute([$_SESSION['user']['id']]);
$row = $stmt->fetch();
$note = $row ? ($row['note'] ?? '') : '';
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Dashboard — CTF Notes</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 720px; }
    textarea { width: 100%; height: 200px; }
    .top { display:flex; justify-content: space-between; align-items:center; }
  </style>
</head>
<body>
  <div class="top">
    <h1>Dashboard</h1>
    <div>Logged in as <strong><?= htmlspecialchars($_SESSION['user']['username']) ?></strong> — <a href="logout.php">Logout</a></div>
  </div>

  <form method="post" action="save_note.php">
    <label>Your note</label>
    <textarea name="note"><?= htmlspecialchars($note) ?></textarea>
    <br><button type="submit">Save</button>
  </form>
</body>
</html>
