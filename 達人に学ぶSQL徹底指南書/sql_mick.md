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



