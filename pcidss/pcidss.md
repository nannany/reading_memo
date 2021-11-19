- 原本
    - https://ja.pcisecuritystandards.org/_onelink_/pcisecurity/en2ja/minisite/en/docs/PCI_DSS_v3_2_1_JA-JP.pdf
- 説明資料
    - https://www.icms.co.jp/downloaddata/PCIDSS_DL_20210413_2.pdf


# 用語
https://ja.pcisecuritystandards.org/_onelink_/pcisecurity/en2ja/minisite/en/docs/PCI_DSS_v3_Glossary_JA-JP.pdf

- PCI DSS(Payment Card Industry Data Security Standard):カード会員データのセキュリティを強化し、均一なデータセキュリティ評価基準の採用をグローバルに推進するために策定された基準
- CDE : カード会員データ環境  
- CHD(CardHolder Data):カード会員データ
  - PAN(Primary Account Number)
  - カード会員名
  - 有効期限
  - サービスコード
- SAD(Sensitive Authentication Data): 機密認証データ
  - フルトラックデータ
  - CAV2/CVC2/CVV2/CID
  - PIN
- PA DSS(Payment Application Data Security Standard): ペイメントアプリケーションデータセキュリティ基準

# PCI DSS 適用性情報

CHDは保存可能。ただし、PANは制限あり。
SADは保存不可。

## PCI DSS と PA-DSS との関係

https://atmarkit.itmedia.co.jp/fsecurity/rensai/pcidss09/pcidss01.html
https://ja.pcisecuritystandards.org/_onelink_/pcisecurity/en2ja/minisite/en/docs/PA-DSS_v3-2.pdf

PCI DSSの中にPA DSSが含まれるイメージ。

## PCI DSS 要件の適用範囲

事業体はPCI DSSの範囲がどのように決められたかを示す文書を保持する。

### ネットワークセグメンテーション

ネットワークセグメンテーション（カード会員データ環境の隔離）はPCI DSS要件ではないが、PCI DSS評価対象範囲を絞るといった点で有効。

付録Dに色々これにまつわることが書いてあるっぽい

### ワイヤレス

line-busting?

### 第三者サービスプロバイダ/アウトソーシングの使用

AOC:「準拠証明書」の頭字語です。AOCは、コンプライアンスに関する自己問診または報告書に記録されている通り、加盟店およびサービスプロバイダがPCI DSS評価結果を証明するための文書です。
ROC:「Report on Compliance（準拠レポート）」の頭字語です。事業体の PCI DSS評価からの詳細結果を文書化したレポート

## PCI DSSを日常業務のプロセスに導入するベストプラクティス

BAU:「通常通りのビジネス」の頭字語 BAU は会社の通常通りの日常ビジネス業務です。

## 評価期間: ビジネス設備とシステムコンポーネントのサンプリング

全量は見れないのでサンプリングする。

## 代替コントロール

付録BとC

## 準拠に関するレポートの指示と内容


## PCI DSS評価プロセス


## PCI DSSバージョン

## PCI DSS要件およびセキュリティ評価手順の詳細


- PCI DSS 要件 
  - この列では、データセキュリティ基準要件を定義します。これらの要件に照合して PCI DSS 準拠が検証されます。
- テスト手順
  - この列には、PCI DSS 要件に「対応」していることを検証するために、評価担当者が行うプロセスが表示されています。
- ガイダンス
  - この列には、各 PCI DSS 要件の意図とセキュリティ目標が表示されています。この列には、ガイダンスのみ表示され、各要件の意図
を理解しやすくすることを目的としています。この列のガイダンスは、PCI DSS 要件およびテスト手順を置き換えたり拡張するものではありませ
ん。

-----

## 要件 6: 安全性の高いシステムとアプリケーションを開発し、保守する

セキュリティパッチをちゃんと当てろというないように見える。概要を見ると。

### 6.1

常に脆弱性に関する情報をキャッチアップできる仕組みが整っているかを確かめるような要件になっている。
