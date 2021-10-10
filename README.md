## **Simple Keystore API**

Exposes following APIs:
1. getall
2. set 
3. get/\<key\>
4. search?prefix=\<pattern\> and search?suffix=\<pattern\>
5. del/\<key\>

**Examples:**

1. **get all**
```
→ curl -s --location --request GET 'http://simple-keystore.info/getall'|jq 
    {
    "abc-2": "abc-2",
    "key1": "value1",
    "key2": "value2",
    "key3": "value3",
    "xyz-1": "xyz-1",
    "xyz-2": "xyz-2"
    } 
```

2. **get/\<key\>**
```
→ curl -s --location --request GET 'http://simple-keystore.info/get/abc-1'|jq
"abc-1"
```

3. **set key** (sample payload)
```
→ curl -s --location --request POST 'http://simple-keystore.info/set' \
--header 'Content-Type: application/json' \
--data-raw '{
    "xyz-3": "xyz-3"
}' |jq
{
  "abc-1": "abc-1",
  "abc-2": "abc-2",
  "key1": "value1",
  "key2": "value2",
  "key3": "value3",
  "xyz-1": "xyz-1",
  "xyz-2": "xyz-2",
  "xyz-3": "xyz-3"
}
```

4. **search prefix**
```
→ curl -s --location --request GET 'http://simple-keystore.info/search?prefix=abc'|jq
[
  "abc-1",
  "abc-2"
]
```

5. **search suffix**
```
→ curl -s --location --request GET 'http://simple-keystore.info/search?suffix=-1'|jq
[
  "abc-1",
  "xyz-1"
]
```

## Includes a Dockerfile and k8s yaml plus steps to deploy the same in a local minikube kubernetes setup

1. clone this repository into your local
2. enable the ingress addon for minikue(it will deoloy the nginx-ingress controller)
```
minikube addons enable ingress
```

*minikube ip will act as the entry point for external traffic here(in case of cloud we will deploy a loadbalancer)*
3. create the keystore deployment
```
kubectl create -f k8s/deployment.yaml
```
4. expose the service
```
kubectl expose deployment keystore  --port=5000
```
5. create the ingress rule
```
kubectl create -f k8s/ingress.yaml
```

6. check if the keystore app pods are running
```
→ kubectl get pods
NAME                        READY   STATUS    RESTARTS   AGE
keystore-56ccbb9fb6-7f2gq   1/1     Running   0          32m
keystore-56ccbb9fb6-h7n4b   1/1     Running   0          32m
keystore-56ccbb9fb6-q29lw   1/1     Running   0          32m
```
7. create a local dns entry in the hosts file for the minikube ip.
```
echo "$(minikube ip) simple-keystore.info" | sudo tee -a /etc/hosts
```


## Test Coverage:
Validates 200 status code and respose body get/set/search api calls

```
root@keystore-7cc6c9659b-qd249:/app# python3 test_app.py
.['value1', 'value2', 'value3']
..
----------------------------------------------------------------------
Ran 3 tests in 0.010s

OK
```
