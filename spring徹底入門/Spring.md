# Spring Frameworkとは

## 1.1 Spring Frameworkの概要

めっちゃ流行っている。

## 1.2 Spring Frameworkの歴史

## 1.3 Springの各種プロジェクトについて

### 1.3.1 Spring MVC

Webアプリをつくるためのやつ。アクションベースFW

### 1.3.2 Spring Security

### 1.3.3 Spring Data

さまざまなサブプロジェクトを含む。まぁDB系のあれこれ

### 1.3.4 Spring Batch

### 1.3.5 Spring Integration

エンドポイント間のやり取りをうまいことやる

### 1.3.6 Spring Cloud

サブプロジェクトが多数。Cloud Nativeなものつくるのに使う

### 1.3.7 Spring Tool Suite

### 1.3.8 Spring IO Platform

### 1.3.9 Spring Boot

## 1.4 Java EEとの関係

# 2 Spring Core（DI×AOP）

## 2.1 SpringによるDI

* DIの仕組みで、クラス間の結合度を下げることができる。
* DIの仕組みで、使用するDBドライバ、ミドルウェアの決定判断を遅らせることができる

## 2.1.1 DI（依存性の注入）とは

* 制御の反転
* インスタンス取得はDIコンテナに任せる

## 2.1.2 ApplicationContextとBean定義

* ApplicationContextがDIコンテナの役割を担う
* DIコンテナに登録するコンポーネント→Bean
* Configuration→Bean定義
* DI定義からBeanを取得→ルックアップ
* 代表的なBean定義方法→JavaベースConfiguration、XMLベース、アノテーションベース

## 2.1.3 Configuration方法


## 2.1.4 インジェクションの種類

* セッターインジェクション
* コンストラクタインジェクション
* フィールドインジェクション

## 2.1.5 オートワイヤリング

## 2.1.6 コンポーネントスキャン

* @Controller、@Service、@Repository、@Componentの違い
