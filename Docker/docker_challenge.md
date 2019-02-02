# やること

Dockerについて理解するために、非常に簡易なアプリケーションを動かしてみる。  
具体的には、"Hello world!" を1秒に1回出すようなアプリケーションをDockerを使って動かしてみる。
ビルド〜実行まですべてコンテナ上で行うことを目指す。
  
Javaのソースコードは以下のよう。
https://github.com/nannany/very-simple-application

# 環境

動作させた環境は
Windows10

# Dockerfile



まずはベースイメージを選ぶために、`FROM`を記述する。  
ここでは、`ubuntu:disco`を選択する。  

