# EJB(Enterprise JavaBeans)
* セッションビーン
 * Stateless
 * Stateful
 * Singleton
* StatefulとSingletonは使われずに一定時間たつと、磁気記憶装置に対比されるので、Serializableを実装する必要がある。
* @Schedule でスケジューリング処理を実施することができる。
 * 毎秒事にログを出力するなど
* @Asynchronous で非同期処理を実装できる。
