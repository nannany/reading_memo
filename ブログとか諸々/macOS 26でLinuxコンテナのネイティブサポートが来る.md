https://future-architect.github.io/articles/20250610a/

コンテナの仕組み上、カーネルはホストOSのものを共有して使う。
現在のアプリケーションコンテナは大抵linuxカーネルを使っている。
そのため、macOSにおいてはlinuxカーネルを動かす必要があり、docker desktopやcolimaを利用して軽量VMを立ち上げて、その中でdockerを動かしていた。

この度 [containerization](https://developer.apple.com/jp/videos/play/wwdc2025/346/)という仕組みができたことによって、仕組みが変わる。

https://github.com/apple/container
https://github.com/apple/containerization


具体的には、virtual frameworkという仕組みを使って、その上に軽量カーネルをコンテナごとに作るようになる。

mac純正の仕組みになるので、効率よくできるらしい？

networkとか諸々まだ問題はあるらしいが乞うご期待なフェーズ。


