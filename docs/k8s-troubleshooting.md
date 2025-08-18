# Kubernetes Troubleshooting Guide

## Quick Debugging Commands
```bash
kubectl get events --sort-by=.metadata.creationTimestamp  # Recent cluster events
kubectl get pods -o wide                                  # Pods with node info
kubectl get all                                           # All resources overview
kubectl describe pod [pod-name]                           # Detailed pod info
kubectl logs [pod-name]                                   # Current pod logs
kubectl logs [pod-name] --previous                        # Previous container logs
kubectl logs [pod-name] -f                                # Follow logs in real-time
kubectl logs [pod-name] --tail=50                         # Last 50 log lines
```

## Interactive Debugging
```bash
kubectl exec -it [pod-name] -- /bin/bash     # Shell into pod
kubectl exec -it [pod-name] -- sh            # Shell (if bash not available)
kubectl port-forward [pod-name] 8080:80      # Forward local port to pod
kubectl proxy                                # Start kubectl proxy
```

## Common Pod Issues & Solutions

### 1. CrashLoopBackOff
**Symptoms:** Pod keeps restarting
```bash
# Investigate
kubectl describe pod [pod-name]
kubectl logs [pod-name] --previous
kubectl get events --field-selector involvedObject.name=[pod-name]

# Common causes:
# - Application exits immediately
# - Missing environment variables
# - Resource limits too low
# - Dependency not available
```

### 2. ImagePullBackOff
**Symptoms:** Cannot pull container image
```bash
# Investigate
kubectl describe pod [pod-name]
kubectl get events --field-selector involvedObject.name=[pod-name]

# Common causes:
# - Wrong image name/tag
# - Missing image pull secrets
# - Network connectivity issues
# - Private registry authentication
```

### 3. Pending Pods
**Symptoms:** Pod stuck in Pending state
```bash
# Investigate
kubectl describe pod [pod-name]
kubectl get nodes
kubectl describe node [node-name]

# Common causes:
# - Insufficient resources
# - Node selector doesn't match
# - Taints and tolerations mismatch
# - PVC not available
```

### 4. Service Connection Issues
**Symptoms:** Cannot reach service
```bash
# Debug service connectivity
kubectl get svc                              # List services
kubectl describe svc [service-name]          # Service details
kubectl get endpoints [service-name]         # Service endpoints
kubectl port-forward svc/[service-name] 8080:80  # Test service locally

# Check pod labels match service selector
kubectl get pods --show-labels
```

## Resource Investigation
```bash
# Pod resource usage
kubectl top pods --sort-by=cpu               # Sort by CPU usage
kubectl top pods --sort-by=memory            # Sort by memory usage

# Node resource usage
kubectl top nodes
kubectl describe node [node-name]            # Node capacity and usage

# Check resource quotas
kubectl get resourcequota
kubectl describe resourcequota [quota-name]
```

## Event Analysis
```bash
# Recent events (most useful for debugging)
kubectl get events --sort-by=.metadata.creationTimestamp --all-namespaces

# Events for specific resource
kubectl get events --field-selector involvedObject.name=[pod-name]

# Warning events only
kubectl get events --field-selector type=Warning
```

## Network Debugging
```bash
# DNS testing from within cluster
kubectl run -it --rm debug --image=busybox --restart=Never -- nslookup [service-name]

# Test connectivity between pods
kubectl exec [pod1] -- ping [pod2-ip]
kubectl exec [pod1] -- wget -qO- [service-name]:[port]

# Check network policies
kubectl get networkpolicies
kubectl describe networkpolicy [policy-name]
```

## Storage Issues
```bash
# Persistent Volume investigation
kubectl get pv                               # List persistent volumes
kubectl get pvc                              # List persistent volume claims
kubectl describe pv [pv-name]                # PV details
kubectl describe pvc [pvc-name]              # PVC details

# Check storage classes
kubectl get storageclass
kubectl describe storageclass [class-name]
```

## Configuration Debugging
```bash
# Check ConfigMap contents
kubectl get configmap [cm-name] -o yaml
kubectl describe configmap [cm-name]

# Check Secret contents (base64 encoded)
kubectl get secret [secret-name] -o yaml
kubectl get secret [secret-name] -o jsonpath='{.data}'

# Validate YAML before applying
kubectl apply --dry-run=client -f [file.yaml]
kubectl apply --validate=true -f [file.yaml]
```

## Cleanup Commands
```bash
# Remove failed/completed pods
kubectl delete pods --field-selector=status.phase=Failed
kubectl delete pods --field-selector=status.phase=Succeeded

# Force delete stuck resources
kubectl delete pod [pod-name] --force --grace-period=0

# Clean up evicted pods
kubectl get pods --all-namespaces --field-selector=status.phase=Failed -o json | kubectl delete -f -
```

## Troubleshooting Workflow
1. **Check pod status**: `kubectl get pods`
2. **Get pod details**: `kubectl describe pod [name]`
3. **Check recent events**: `kubectl get events --sort-by=.metadata.creationTimestamp`
4. **Examine logs**: `kubectl logs [pod-name]`
5. **Check resource usage**: `kubectl top pods`
6. **Verify configuration**: ConfigMaps, Secrets, Services
7. **Test connectivity**: Port forwarding, exec into pods

## Quick Health Check
```bash
# One-liner cluster health check
kubectl get nodes,pods --all-namespaces | grep -E "(NotReady|Error|CrashLoop|ImagePull)"
```