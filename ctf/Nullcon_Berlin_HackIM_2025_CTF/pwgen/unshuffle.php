<?php
/*
  Usage:
    php unshuffle.php 1 "7F6_23Ha8:5E4N3_/e27833D4S5cNaT_1i_O46STLf3r-4AH6133bdTO5p419U0n53Rdc80F4_Lb6_65BSeWb38f86{dGTf4}eE8__SW4Dp86_4f1VNH8H_C10e7L62154"

  仕組み:
    - srand(0x1337) で初期化
    - (N-1) 回ぶん、長さ L の「rand(0, i) を用いたシャッフル」を“消費”して前進
    - N 回目の置換 perm を作る（orig_idx -> new_idx）
    - 逆置換 inv を作り、観測文字列の各 new_idx から元の orig_idx へ戻す
*/

if ($argc < 3) {
    fwrite(STDERR, "Usage: php {$argv[0]} <N> <observed_string>\n");
    exit(1);
}
$N = intval($argv[1]);
$observed = $argv[2];
$L = strlen($observed);

if ($N < 1) {
    fwrite(STDERR, "N must be >= 1\n");
    exit(1);
}

srand(0x1337);

/* (N-1)回ぶんのシャッフルを“消費” */
for ($k = 0; $k < $N - 1; $k++) {
    for ($i = $L - 1; $i > 0; $i--) {
        /* 置換は作らず、rand を同じ回数だけ消費 */
        rand(0, $i);
    }
}

/* N回目の置換を作る（Fisher–Yates） */
// 注意: この perm は「new -> orig」の写像になる
$perm = range(0, $L - 1);
for ($i = $L - 1; $i > 0; $i--) {
    $j = rand(0, $i);
    // swap perm[i], perm[j]
    $tmp = $perm[$i];
    $perm[$i] = $perm[$j];
    $perm[$j] = $tmp;
}

/* 観測文字列に new->orig を適用して元順序へ戻す */
$chars = str_split($observed);
$orig_chars = array_fill(0, $L, '');
for ($new = 0; $new < $L; $new++) {
    $orig = $perm[$new]; // new -> orig
    $orig_chars[$orig] = $chars[$new];
}
echo implode('', $orig_chars), PHP_EOL;
