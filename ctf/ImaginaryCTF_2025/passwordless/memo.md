https://chatgpt.com/c/68bc4140-b1e0-8328-aab0-8e4335692c4e


u+AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA@gmail.com

今回のパスワード生成ロジックは登録メール+16文字のランダムな値、になり、それをbcryptでハッシュ化してdbに保存してる。

bcryptは72文字目以降を切り捨ててしまう性質を使って、上記のようなメールを登録すると、mail, pass両方を上記で打ち込めばログインできる。

ログインできたらflagが見れる。
