# kubectl Essentials - Daily Commands

## Cluster Information
```bash
kubectl version                   # Display Kubernetes client and server version
kubectl version --short           # Concise version information
kubectl cluster-info              # Display cluster information
kubectl get namespaces            # List all namespaces
```

## Basic Resource Operations
```bash
# Get resources
kubectl get [resource]            # List resources
kubectl get pods                  # List pods in current namespace
kubectl get deployments          # List all deployments
kubectl get services              # List all services
kubectl get configmaps           # List all ConfigMaps
kubectl get secrets              # List all secrets

# Detailed information
kubectl describe [resource] [name]   # Show detailed resource info
kubectl describe pod [pod-name]      # Detailed pod information
```

## Creating and Managing Resources
```bash
# Create resources
kubectl create -f [file]              # Create resource from file
kubectl apply -f [file]               # Apply configuration from file
kubectl run nginx --image=nginx       # Create pod with nginx image
kubectl create deployment nginx --image=nginx  # Create deployment

# Delete resources
kubectl delete [resource] [name]      # Delete resource by name
kubectl delete pod [pod-name]         # Delete specific pod
kubectl delete -f [file]              # Delete resources defined in file
```

## Working with Pods
```bash
kubectl get pods                      # List pods in current namespace
kubectl get pods --namespace [ns]     # List pods in specific namespace
kubectl get pods -o wide             # List pods with more details
kubectl get pods --selector app=myapp # List pods with specific label
kubectl logs [pod-name]              # View pod logs
kubectl exec [pod-name] -- [command] # Execute command in pod
```

## Deployments
```bash
kubectl get deployments                           # List deployments
kubectl create deployment [name] --image=[image]  # Create deployment
kubectl scale deployment [name] --replicas=3      # Scale deployment
kubectl rollout status deployment [name]          # Check rollout status
kubectl rollout undo deployment [name]            # Rollback deployment
```

## Services & Networking
```bash
kubectl get services                              # List services
kubectl expose deployment [name] --port=80       # Expose deployment
kubectl expose deployment [name] --type=NodePort --port=80  # Expose with NodePort
```

## ConfigMaps & Secrets
```bash
# ConfigMaps
kubectl create configmap [name] --from-literal=key=value  # Create ConfigMap
kubectl get configmaps                                    # List ConfigMaps

# Secrets
kubectl create secret generic [name] --from-literal=key=value  # Create secret
kubectl get secrets                                            # List secrets
```

## Namespace Management
```bash
kubectl get namespaces               # List namespaces
kubectl create namespace [name]      # Create namespace
kubectl delete namespace [name]      # Delete namespace
kubectl config set-context --current --namespace=[name]  # Switch namespace
```

## Resource Monitoring
```bash
kubectl top nodes                    # Node resource usage
kubectl top pods                     # Pod resource usage
kubectl top pods --namespace [ns]    # Pod usage in specific namespace
```

## Common Resource Types
- **pods** (po)
- **services** (svc)
- **deployments** (deploy)
- **configmaps** (cm)
- **secrets**
- **nodes** (no)
- **namespaces** (ns)
- **persistentvolumes** (pv)
- **persistentvolumeclaims** (pvc)