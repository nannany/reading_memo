# 第一部 魔法のSQL

## 1. CASE式のススメ

WHERE句で条件分岐させるのは素人のやること。プロはSELECT句で分岐させる

HAVING句で条件分岐させるのは素人のやること。プロはSELECT句で分岐させる

* GROUP BY句でCASE式を使うことで、集約単位となるコードや階級を柔軟に設定できる。これは非定型的な集約に大きな威力を発揮する。
* 集約関数の中に使うことで、行持ちから列持ちへの水平展開も自由自在
* 反対に集約関数を条件式に組み込むことでHAVING句を使わずにクエリをまとめられる
*　実装依存の関数より表現力が非常に強力なうえ、汎用性も高まって一石二鳥
* そうした利点があるのも、CASE式が「文」ではなく「式」であるからこそ
* CASE式を駆使することで複数のSQL文を１つにまとめられ、可読性もパフォーマンスも向上していいことづくし

```sql
CREATE TABLE Greatests
(key CHAR(1) PRIMARY KEY,
 x   INTEGER NOT NULL,
 y   INTEGER NOT NULL,
 z   INTEGER NOT NULL);

INSERT INTO Greatests VALUES('A', 1, 2, 3);
INSERT INTO Greatests VALUES('B', 5, 5, 2);
INSERT INTO Greatests VALUES('C', 4, 7, 1);
INSERT INTO Greatests VALUES('D', 3, 3, 8);
```

```sql
select key,
       case when x < y then y else x end as greatest
from Greatests;

select key,
        case when x < y
            then case when y < z
                then z else y end
        when y <= x
            then case when x < z
                then z else x end
        end
from Greatests;
```

演習２

```sql
CREATE TABLE PopTbl2
(pref_name VARCHAR(32),
 sex CHAR(1) NOT NULL,
 population INTEGER NOT NULL,
    PRIMARY KEY(pref_name, sex));

INSERT INTO PopTbl2 VALUES('徳島', '1',	60 );
INSERT INTO PopTbl2 VALUES('徳島', '2',	40 );
INSERT INTO PopTbl2 VALUES('香川', '1',	100);
INSERT INTO PopTbl2 VALUES('香川', '2',	100);
INSERT INTO PopTbl2 VALUES('愛媛', '1',	100);
INSERT INTO PopTbl2 VALUES('愛媛', '2',	50 );
INSERT INTO PopTbl2 VALUES('高知', '1',	100);
INSERT INTO PopTbl2 VALUES('高知', '2',	100);
INSERT INTO PopTbl2 VALUES('福岡', '1',	100);
INSERT INTO PopTbl2 VALUES('福岡', '2',	200);
INSERT INTO PopTbl2 VALUES('佐賀', '1',	20 );
INSERT INTO PopTbl2 VALUES('佐賀', '2',	80 );
INSERT INTO PopTbl2 VALUES('長崎', '1',	125);
INSERT INTO PopTbl2 VALUES('長崎', '2',	125);
INSERT INTO PopTbl2 VALUES('東京', '1',	250);
INSERT INTO PopTbl2 VALUES('東京', '2',	150);
```

```sql
select
    case when sex = '1' then '男' else '女' end as sex1,
    sum(PopTbl2.population) as zenkoku,
    sum(case when pref_name = '徳島' then population else 0 end) as tokushima,
    sum(case when pref_name = '高知' then population else 0 end) as tokushima,
    sum(case when pref_name = '香川' then population else 0 end) as tokushima,
    sum(case when pref_name = '愛媛' then population else 0 end) as ehime,
    sum(case when pref_name in ('愛媛','高知','香川','徳島') then population else 0 end) as shikoku
from PopTbl2
group by sex1
```

演習3

```sql
select
    key
from Greatests
order by case key
    when 'B' then 1
    when 'A' then 2
    when 'D' then 3
    when 'C' then 4
    end;
``` 



# 2. 必ずわかるウィンドウ関数

* ウィンドウ関数の「ウィンドウ」とは、（原則として順序を持つ）「範囲」という意味。
* ウィンドウ関数の構文上では、PARTITION BY句とORDER BY句で特徴づけられたレコードの集合を意味するが、一般的に簡略形の構文が使われるため、かえってウィンドウの存在を意識しにくい
* PARTITION BY句はGROUP BY句から集約の機能を引いて、カットの機能だけを残し、ORDER BY句はレコードの順序を付ける。
* フレーム句はカーソルの機能をSQLの構文に持ち込むことで、「カレントレコード」を中心にしたレコード集合の範囲を定義することができる
* フレーム句を使うことで、異なる行のデータを1つの行に持ってくることができるようになり、行間比較が簡単に行えるようになった。
* ウィンドウ関数の内部動作としては、現在のところ、レコードのソートが行われている。将来的にハッシュが採用される可能性もゼロではない。

## 演習2.1

予想：全レコードの合計loadが算出されるのでは ⇒ あたり

```sql
CREATE TABLE ServerLoadSample
(server       CHAR(4) NOT NULL,
 sample_date  DATE    NOT NULL,
 load_val      INTEGER NOT NULL,
    PRIMARY KEY (server, sample_date));

INSERT INTO ServerLoadSample VALUES('A' , '2018-02-01',  1024);
INSERT INTO ServerLoadSample VALUES('A' , '2018-02-02',  2366);
INSERT INTO ServerLoadSample VALUES('A' , '2018-02-05',  2366);
INSERT INTO ServerLoadSample VALUES('A' , '2018-02-07',   985);
INSERT INTO ServerLoadSample VALUES('A' , '2018-02-08',   780);
INSERT INTO ServerLoadSample VALUES('A' , '2018-02-12',  1000);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-01',    54);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-02', 39008);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-03',  2900);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-04',   556);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-05', 12600);
INSERT INTO ServerLoadSample VALUES('B' , '2018-02-06',  7309);
INSERT INTO ServerLoadSample VALUES('C' , '2018-02-01',  1000);
INSERT INTO ServerLoadSample VALUES('C' , '2018-02-07',  2000);
INSERT INTO ServerLoadSample VALUES('C' , '2018-02-16',   500);
```

```sql
SELECT server, sample_date,
       SUM(load_val) OVER () AS sum_load
  FROM ServerLoadSample;
```

## 演習2.2 

サーバごとの合計値が取れる

# 3 自己結合の使い方

自己結合のコツは、同じテーブルが本当に2つあるかのように扱うこと

順列、組み合わせを得るときに役立つ方法が書いてある！

* 自己結合は非等値結合と組み合わせて使うのが基本
* GROUP BYと組み合わせると、再帰的集合を作ることができる
* 本当に異なるテーブルを結合していると考えると理解しやすい
* 物理ではなく論理の世界で考える

rank, dense_rank

## 演習3.1 重複組み合わせ

```sql
CREATE TABLE Products
(name VARCHAR(16) PRIMARY KEY,
 price INTEGER NOT NULL);

--重複順列・順列・組み合わせ
DELETE FROM Products;
INSERT INTO Products VALUES('りんご',	100);
INSERT INTO Products VALUES('みかん',	50);
INSERT INTO Products VALUES('バナナ',	80);
```

```sql
select p1.name , p2.name
from Products p1 cross join Products p2
where p1.name <=p2.name;
```

## 演習3.2 ウィンドウ関数で重複削除

```sql
DROP TABLE Products;
CREATE TABLE Products
(name VARCHAR(16) NOT NULL,
 price INTEGER NOT NULL);

--重複するレコード
INSERT INTO Products VALUES('りんご',	50);
INSERT INTO Products VALUES('みかん',	100);
INSERT INTO Products VALUES('みかん',	100);
INSERT INTO Products VALUES('みかん',	100);
INSERT INTO Products VALUES('バナナ',	80);
```

```sql
CREATE TABLE Products_NoRedundant
AS
SELECT ROW_NUMBER()
         OVER(PARTITION BY name, price
                  ORDER BY name) AS row_num,
       name, price
  FROM Products;


-- 連番が1以外のレコードを削除
DELETE FROM Products_NoRedundant
  WHERE row_num > 1;
```

# 4. 3値論理とNULL

null は値でも変数でもない

排中律 ⇒ 白黒はっきり命題の真偽が定まる

IN と EXISTSは同値変換が可能だが、NOT INとNOT EXISTSは同値でない

* NULLは値ではない
*　値ではないので、述語もまともに適用できない
* 無理やり適用するとunknownが生じる
* unknownが論理演算に紛れ込むと、SQLが直感に反する動作をする
* これに対処するには、段階的なステップに分けてSQLの動作を追うことが有効

## 演習４．１

postgresにおけるorder by のソート順。nullについて。
⇒
nulls first , nulls last でNULLを最初に持ってくるか、最後に持ってくるか決められる。
デフォルトでは、大きな値として扱われる。つまり、descだと最初に来る。

## 演習4.2

nullと文字連結
https://www.postgresql.jp/document/9.3/html/functions-string.html

## 演習4.3 

coalesce は左から順に、nullでないのを見つけたらそれを返す感じ  
↓は'ddd'返す。
```sql
select coalesce('ddd','abc' , null);
```

nullif は引数に与えられた2値が等しければnull返す。

下のはnull返す。
```sql
select nullif('dddd', 'dddd')
```


# 19. 手続き型から宣言型・集合指向へ　頭を切り替える7か条

* IF文やCASE文は、CASE式で置き換える。SQLはむしろ関数型言語と考え方が近い
* ループはGROUP BY句とウィンドウ関数で置き換える
* テーブルの行に順序はない
  * あえてアナロジーを挙げるとすれば、ファイルではなくバッグに詰め込まれたもの。(setみたいな)
* テーブルを集合とみなそう
* EXISTS述語と「量化」の概念を理解しよう
* HAVING句の真価をまなぶ
* 四角を描くな、円を描け

