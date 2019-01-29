クラスタ作成コマンド
aws eks create-cluster --name sample-eks-cluster --role-arn arn:aws:iam::948494934800:role/eksServiceRole --resources-vpc-config subnetIds=subnet-0034eb6881013ea26,subnet-0b1c4a71ae5814e61,subnet-0e9cd1acd39fbdd41,securityGroupIds=sg-042cfed69978ff6b8


```
# aws cli setting
export AWS_DEFAULT_REGION=us-west-2

# worker setting
export EKS_WORKER_INSTANCE_TYPE=t2.small
export EKS_WORKER_AMI=ami-02415125ccd555295

# aws resource name
export EKS_WORKER_STACK_NAME=eks-worker-stack
export EKS_CLUSTER_NAME=eks-cluster
export EKS_VPC_STACK_NAME=eks-vpc-stack
export EKS_ROLE_NAME=eks-role

# local directories and files
export EKS_KUBE_CONFIG_FILE=~/.kube/config-$EKS_CLUSTER_NAME

# kubectl configuration
export KUBECONFIG=$KUBECONFIG:$EKS_KUBE_CONFIG_FILE
```
