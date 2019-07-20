cd $(dirname $0)

export HOGE=FOOBAR

envsubst < env.template > /tmp/env-sample

echo $(cat /tmp/env-sample)

kubectl create secret generic --from-file=/tmp/env-sample