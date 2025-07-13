# Telepresence vs mirrord

## Overview

| Feature           | Telepresence                                              | mirrord                                                   |
|-------------------|-----------------------------------------------------------|------------------------------------------------------------|
| **Purpose**        | Run local code as if it’s part of the remote cluster     | Mirror a remote pod’s environment to a local process       |
| **Primary Use**    | Replace a pod or intercept traffic for development/debug | Run/debug local apps using remote cluster context          |
| **Core Approach**  | Pod swap or traffic proxying                             | LD_PRELOAD-based mirroring, environment injection          |
| **Target Users**   | App developers, platform engineers                       | Developers needing fast local iteration/testing            |

---

## Conceptual Differences

### Telepresence
- Connects your local machine to a Kubernetes cluster via a **traffic proxy**.
- Offers **swap deployment** mode: replaces a pod in the cluster with your local code.
- Makes it easy to test services locally that rely on complex remote dependencies.
- Traffic between your local app and other cluster services behaves as if your app were deployed remotely.

### mirrord
- **Mirrors the environment** (e.g., env vars, volumes, network) of a remote pod to your local process.
- Lets you **run or debug a local app** in the context of a remote Kubernetes pod without redeploying.
- Doesn’t replace pods — instead, it hooks into network traffic and environment variables using system-level tools.
- Typically requires fewer cluster privileges than Telepresence.

---

## Use Cases

| Use Case                        | Telepresence                         | mirrord                             |
|----------------------------------|--------------------------------------|--------------------------------------|
| Debug a microservice locally      | ✅ Yes                                | ✅ Yes                                |
| Replace a live pod                | ✅ Yes (swap deployment)              | ❌ No                                 |
| Run a local CLI tool in cluster context | ✅ With setup                  | ✅ Easily, just run via mirrord       |
| Use with IDE debugger             | ✅ Good support                       | ✅ Good support (via extension)       |
| Complex network dependency tests | ✅ Robust                            | ⚠️ May need config for advanced cases |

---

## Pros and Cons

### Telepresence

**Pros:**
- Well-suited for complex Kubernetes apps
- Supports full traffic routing
- Good for service-to-service testing

**Cons:**
- Heavier setup and dependencies
- Requires elevated permissions
- Sometimes intrusive (e.g., swap deployment)

---

### mirrord

**Pros:**
- Lightweight and easy to install
- Fast local iteration
- Works well with simple setups

**Cons:**
- Limited pod interaction (no pod replacement)
- May struggle with complex network edge cases
- Still maturing (some features in beta)

---

## Conclusion

- Use **Telepresence** if you need to replace a live service, handle complex network dependencies, or work with service meshes.
- Use **mirrord** if you want a lightweight, fast way to test and debug local code in the context of a Kubernetes pod with minimal setup.