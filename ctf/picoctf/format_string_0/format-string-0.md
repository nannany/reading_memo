segmentation faultが起きればflagが出力される。

printfにおいて、%114dとするとそれは114文字分の数字が出力される。(どんな数字になるんだ？)

また、printf("%s")みたいな感じにすると、%sはスタック上の値をポインタとして扱い、無効なメモリアドレスにアクセスしようとしてsegmentation faultが起きる。

