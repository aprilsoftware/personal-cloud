# Install [Kubernetes](https://kubernetes.io/)

**On each node**

```
apt install gnupg2 apt-transport-https curl iptables
```

```
cat <<EOF | sudo tee /etc/modules-load.d/k8s.conf 
overlay 
br_netfilter 
EOF
```

```
modprobe overlay
```

```
modprobe br_netfilter
```

```
cat <<EOF | sudo tee /etc/sysctl.d/k8s.conf 
net.ipv4.ip_forward = 1
net.bridge.bridge-nf-call-iptables = 1
net.bridge.bridge-nf-call-ip6tables = 1 
EOF
```

```
sysctl --system
```

## [cri-o](https://cri-o.io/)

```
OS=Debian_11
VERSION=1.27
```

```
echo "deb https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/ /" > /etc/apt/sources.list.d/devel-kubic-libcontainers-stable-$VERSION.list
```

```
echo "deb http://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/ /" > /etc/apt/sources.list.d/devel-kubic-libcontainers-stable-cri-o-$VERSION.list
```

```
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable:/cri-o:/$VERSION/$OS/Release.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/devel-kubic-libcontainers-$VERSION.gpg > /dev/null
```

```
curl -L https://download.opensuse.org/repositories/devel:/kubic:/libcontainers:/stable/$OS/Release.key | gpg --dearmor | tee /etc/apt/trusted.gpg.d/devel-kubic-libcontainers-cri-o-$VERSION.gpg > /dev/null
```

```
apt-get update
```

```
apt-get install cri-o cri-o-runc cri-tools
```

```
apt-mark hold cri-o cri-o-runc
```

```
systemctl enable crio
```

## K8s

```
curl -L https://packages.cloud.google.com/apt/doc/apt-key.gpg | gpg --dearmor | tee /etc/apt/trusted.gpg.d/kubernetes.gpg > /dev/null
```

```
echo "deb https://apt.kubernetes.io/ kubernetes-xenial main" | sudo tee /etc/apt/sources.list.d/kubernetes.list
```

```
apt update
```

```
apt-get install kubelet=1.27.2-00 kubeadm=1.27.2-00 kubectl=1.27.2-00
```

```
apt-mark hold kubelet kubeadm kubectl
```

```
service crio start
```

**On the master node**

```
kubeadm init --pod-network-cidr=10.86.0.0/16
```

```
To start using your cluster, you need to run the following as a regular user:

mkdir -p $HOME/.kube
sudo cp -i /etc/kubernetes/admin.conf $HOME/.kube/config
sudo chown $(id -u):$(id -g) $HOME/.kube/config

Alternatively, if you are the root user, you can run:

  export KUBECONFIG=/etc/kubernetes/admin.conf

You should now deploy a pod network to the cluster.
Run "kubectl apply -f [podnetwork].yaml" with one of the options listed at:
  https://kubernetes.io/docs/concepts/cluster-administration/addons/

Then you can join any number of worker nodes by running the following on each as root:

kubeadm join 192.168.7.117:6443 --token x36skg.hkyg3vqd8s3hbfoc \
	--discovery-token-ca-cert-hash sha256:d63dfb51ff1e98a55e7042844ffe7fa9df8f1b126f06156487e22c212dbf7084

```

**On the other nodes**

```
kubeadm join 192.168.7.117:6443 --token x36skg.hkyg3vqd8s3hbfoc \
	--discovery-token-ca-cert-hash sha256:d63dfb51ff1e98a55e7042844ffe7fa9df8f1b126f06156487e22c212dbf7084
```

**On the master node**

```
kubectl label node k8s1node1 node-role.kubernetes.io/worker=worker
kubectl label node k8s1node2 node-role.kubernetes.io/worker=worker
kubectl label node k8s1node3 node-role.kubernetes.io/worker=worker
kubectl label node k8s1node4 node-role.kubernetes.io/worker=worker
```

## [antrea](https://antrea.io/)
```
apt install openvswitch-switch
```

```
kubectl apply -f https://github.com/antrea-io/antrea/releases/download/v1.12.0/antrea.yml
```

## [metallb](https://metallb.universe.tf/)
```
kubectl apply -f https://raw.githubusercontent.com/metallb/metallb/v0.13.10/config/manifests/metallb-native.yaml
```

```
vi metallb-pool.yaml
```

```
apiVersion: metallb.io/v1beta1
kind: IPAddressPool
metadata:
  name: default
  namespace: metallb-system
spec:
  addresses:
  - 192.168.7.50-192.168.7.59
```

```
kubectl apply -f metallb-pool.yaml
```

```
vi metallb-adv.yaml
```

```
apiVersion: metallb.io/v1beta1
kind: L2Advertisement
metadata:
  name: default
  namespace: metallb-system
```

```
kubectl apply -f metallb-adv.yaml
```

## [ingress-haproxy](https://haproxy-ingress.github.io/)
### Install helm as root
```
sudo -i
```

```
curl https://baltocdn.com/helm/signing.asc | gpg --dearmor | sudo tee /usr/share/keyrings/helm.gpg > /dev/null
```

```
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/helm.gpg] https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list
```

```
apt-get update
```

```
apt-get install helm
```

```
exit
```

### Install ingress-haproxy as a kubernetes user
```
helm repo add haproxy-ingress https://haproxy-ingress.github.io/charts
```

```
vi haproxy-ingress-values.yaml
```

```
controller:
  hostNetwork: true
```

```
helm install haproxy-ingress haproxy-ingress/haproxy-ingress\
  --create-namespace --namespace ingress-controller\
  --version 0.14.2\
  -f haproxy-ingress-values.yaml
```

## [Rook / Ceph](https://rook.io/)
**On each storage node**

```
apt install lvm2 ntp
```

**On the master node**
```
apt install git
```

```
git clone --single-branch --branch v1.11.4 https://github.com/rook/rook.git
```

```
cd rook/deploy/examples
```

```
cp operator.yaml ../../../init/
cp cluster.yaml ../../../init/
cp toolbox.yaml ../../../init/
cp crds.yaml ../../../init/
cp common.yaml ../../../init/
```

```
cd ../../../init
```

```
kubectl get nodes --show-labels
```

```
kubectl label node k8s1node1 storage-node=true
kubectl label node k8s1node2 storage-node=true
kubectl label node k8s1node3 storage-node=true
```

Modify operator.yaml and cluster.yaml

```
kubectl create -f crds.yaml -f common.yaml -f operator.yaml
```

Wait orchestrator running

```
kubectl create -f cluster.yaml
```

```
kubectl create -f toolbox.yaml
```

```
kubectl -n rook-ceph exec -it deploy/rook-ceph-tools -- bash
```

Check that Ceph status is OK

```
ceph status
```

```
ceph osd status
```

## [cert-manager](https://cert-manager.io/)
```
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.12.0/cert-manager.yaml
```

## PKI
```
apt install coreutils
```

```
cat intermediate_ca.crt root_ca.crt > bundle_ca.crt
```

```
cat bundle_ca.crt | base64 -w0
```

```
openssl ec -in intermediate_ca_key -out intermediate_ca.key
```

```
cat intermediate_ca.key | base64 -w0
```

```
kubectl create namespace cert-manager
```

```
vi intermediate-ca-key-pair.yaml
```

```
apiVersion: v1
kind: Secret
metadata:
  name: intermediate-ca-key-pair
  namespace: cert-manager
data:
  tls.crt: YOUR_CRT
  tls.key: YOUR_KEY
```

```
kubectl apply -f intermediate-ca-key-pair.yaml
```

```
vi intermediate-ca-issuer.yaml
```

```
apiVersion: cert-manager.io/v1
kind: ClusterIssuer
metadata:
  name: intermediate-ca-issuer
  namespace: cert-manager
spec:
  ca:
    secretName: intermediate-ca-key-pair
```

```
kubectl apply -f intermediate-ca-issuer.yaml
```

## Ceph objectstore
```
vi s3-cert.yaml
```

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: s3-cert
  namespace: rook-ceph
spec:
  commonName: s3-cert
  secretName: s3-secret
  dnsNames:
  - rook-ceph-rgw-s3-object-store.rook-ceph.svc
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: intermediate-ca-issuer
    kind: ClusterIssuer
    group: cert-manager.io
```

```
kubectl apply -f s3-cert.yaml
```

```
vi s3-object-store.yaml
```

```
apiVersion: ceph.rook.io/v1
kind: CephObjectStore
metadata:
  name: s3-object-store
  namespace: rook-ceph
spec:
  metadataPool:
    failureDomain: host
    replicated:
      size: 3
      requireSafeReplicaSize: true
    parameters:
      compression_mode: none
  dataPool:
    failureDomain: host
    replicated:
      size: 3
      requireSafeReplicaSize: true
    parameters:
      compression_mode: none
  preservePoolsOnDelete: false
  gateway:
    sslCertificateRef: s3-secret
    securePort: 443
    instances: 1
  healthCheck:
    startupProbe:
      disabled: false
    readinessProbe:
      disabled: false
```

```
kubectl apply -f s3-object-store.yaml
```

```
vi s3-storageclass.yaml
```

```
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
   name: s3-bucket
   namespace: rook-ceph
provisioner: rook-ceph.ceph.rook.io/bucket
reclaimPolicy: Delete
parameters:
  objectStoreName: s3-object-store
  objectStoreNamespace: rook-ceph
```

```
kubectl create -f s3-storageclass.yaml
```

```
vi s3-bucket-claim.yaml
```

```
apiVersion: objectbucket.io/v1alpha1
kind: ObjectBucketClaim
metadata:
  name: s3-bucket
  namespace: rook-ceph
spec:
  generateBucketName: s3-bucket
  storageClassName: s3-bucket
```

```
kubectl create -f s3-bucket-claim.yaml
```

## Ingress
```
vi s3-example-com-cert.yaml
```

```
apiVersion: cert-manager.io/v1
kind: Certificate
metadata:
  name: s3-example-com-cert
  namespace: rook-ceph
spec:
  commonName: s3-example-com-cert
  secretName: s3-example-com-secret
  dnsNames:
  - s3.example.com
  privateKey:
    algorithm: ECDSA
    size: 256
  issuerRef:
    name: intermediate-ca-issuer
    kind: ClusterIssuer
    group: cert-manager.io
```

```
kubectl apply -f s3-example-com-cert.yaml
```

```
vi s3-ingress.yaml
```

```
apiVersion: networking.k8s.io/v1
kind: Ingress
metadata:
  name: s3-ingress
  namespace: rook-ceph
  annotations:
    kubernetes.io/ingress.class: haproxy
    ingress.kubernetes.io/secure-backends: "true"
    ingress.kubernetes.io/backend-protocol: "HTTPS"
spec:
  rules:
  - host: s3.example.com
    http:
      paths:
      - path: /
        pathType: Prefix
        backend:
          service:
            name: rook-ceph-rgw-s3-object-store
            port:
              number: 443
  tls:
  -
    secretName: s3-example-com-secret
    hosts:
    - s3.example.com
```

```
kubectl create -f s3-ingress.yaml
```

# S3 client
```
echo $(kubectl -n default get secret s3-bucket -n rook-ceph -o jsonpath='{.data.AWS_ACCESS_KEY_ID}' | base64 --decode)
```

```
echo $(kubectl -n default get cm s3-bucket -n rook-ceph -o jsonpath='{.data.BUCKET_NAME}')
```

```
echo $(kubectl -n default get secret s3-bucket -n rook-ceph -o jsonpath='{.data.AWS_SECRET_ACCESS_KEY}' | base64 --decode)
```

# s3cmd
```
sudo apt install s3cmd
```

```
s3cmd --configure
```

### .s3cfg
```
host_base = s3.example.com
host_bucket = s3://s3-bucket-xxxxxxxx-xxxx-xxx-xxxx-xxxxxxxxxxxx
```

### Create S3 user
```
apiVersion: ceph.rook.io/v1
kind: CephObjectStoreUser
metadata:
  name: my-user
  namespace: rook-ceph
spec:
  store: my-store
  displayName: "my display name"
```
