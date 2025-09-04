<?php
session_start();
$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);
?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Grandma's Notes</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    body { font-family: system-ui, sans-serif; margin: 2rem; max-width: 720px; }
    form { margin: 1rem 0; padding: 1rem; border: 1px solid #ddd; border-radius: 8px; }
    input, textarea { width: 100%; padding: .5rem; margin: .25rem 0 .75rem; }
    .flash { padding:.75rem; background:#f5faff; border:1px solid #bfe0ff; border-radius:8px; }
    .row { display:flex; gap:1rem; }
    .row > div { flex: 1; }
    a { text-decoration: none; }
    small { color:#666; }
  </style>
</head>
<body>
  <h1>Grandma's Notes</h1>
  <?php if ($flash): ?>
    <div class="flash"><?= htmlspecialchars($flash) ?></div>
  <?php endif; ?>

  <?php if (!empty($_SESSION['user'])): ?>
    <p>You are logged in as <strong><?= htmlspecialchars($_SESSION['user']['username']) ?></strong>. Go to <a href="dashboard.php">dashboard</a> or <a href="logout.php">logout</a>.</p>
  <?php else: ?>
    <div class="row">
      <div>
        <h2>Register</h2>
        <form method="post" action="register.php">
          <label>Username</label>
          <input name="username" maxlength="64" required>
          <label>Password (max 16 chars)</label>
          <input name="password" type="password" maxlength="16" required>
          <button type="submit">Create account</button>
        </form>
      </div>
      <div>
        <h2>Login</h2>
        <form method="post" action="login.php">
          <label>Username</label>
          <input name="username" required>
          <label>Password</label>
          <input name="password" type="password" required>
          <button type="submit">Sign in</button>
        </form>
      </div>
    </div>
  <?php endif; ?>
  <p>With <3 from @gehaxelt</p>
</body>
</html>
