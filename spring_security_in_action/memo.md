# FilterChainProxyについて

https://www.fatalerrors.org/a/1dxx2A.html

FilterChainProxyを、WebServer(tomcatとか？)がもっている仕組みであるFilterに入れ込む。
FilterChainProxyの中に、複数のChain群があり、リクエストのパスに応じてどのFilterを通過させるかがきまる。
