cd $(dirname $0)

# MSYS_NO_PATHCONVを設定しておき、勝手にパス変換させないようにする
export MSYS_NO_PATHCONV=1
export HOGE=FOOBAR

envsubst < env.template > /tmp/env

echo $(cat /tmp/env-sample)

unset MSYS_NO_PATHCONV
kubectl create secret generic my.secret --from-file=/tmp/env