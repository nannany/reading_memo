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



-----

## 要件 6: 安全性の高いシステムとアプリケーションを開発し、保守する
