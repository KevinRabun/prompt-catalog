---
name: Linux Development Platform Instructions
description: Platform-specific guidance for Linux application development
---

<!-- Catalog Metadata
id: INST-PLAT-003
version: 1.0.0
scope: platform
applies_to: linux
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Linux Development — Platform Instructions

## Scope
These instructions apply when building **Linux applications** — CLI tools, daemons/services, desktop apps, and embedded systems.

## Application Types

### CLI Tools
- Follow **Unix philosophy**: do one thing well, support piping, use exit codes
- Support **standard I/O** (stdin, stdout, stderr) conventions
- Parse arguments with established libraries (argparse, clap, cobra)
- Support **--help**, **--version**, and **long and short** option flags
- Return **meaningful exit codes** (0 = success, non-zero = failure)
- Support **configuration files** (XDG Base Directory spec), environment variables, and CLI flags
- Consider **man page** generation for discoverability

### Daemons / Services
- Use **systemd** unit files for service management
- Implement **graceful shutdown** on SIGTERM
- Support **log rotation** (via journald or logrotate)
- Handle **PID files** correctly if not using systemd
- Run as a **non-root user** with minimal privileges
- Support **configuration reloading** on SIGHUP
- Use **socket activation** where appropriate

### Desktop Applications
- **GTK**: GNOME ecosystem, C/Python/Rust bindings, Flatpak distribution
- **Qt**: Cross-platform, C++ with QML for modern UIs, feature-rich
- **Electron/Tauri**: Web technology-based, Tauri preferred for native performance
- Follow **freedesktop.org specifications** for integration

### Embedded / IoT
- Cross-compile with appropriate **toolchains**
- Minimize **dependencies** and **binary size**
- Handle **resource constraints** (memory, storage, CPU)
- Implement **watchdog timers** for reliability
- Consider **OTA update** mechanisms

## Linux-Specific Considerations

### File System
- Follow the **Filesystem Hierarchy Standard** (FHS)
- Respect **XDG Base Directory Specification** for user-specific files
  - Config: `$XDG_CONFIG_HOME` (~/.config/)
  - Data: `$XDG_DATA_HOME` (~/.local/share/)
  - Cache: `$XDG_CACHE_HOME` (~/.cache/)
  - Runtime: `$XDG_RUNTIME_DIR`
- Handle **permissions** correctly (umask, file ownership)
- Use **appropriate file locking** mechanisms

### Security
- Follow **principle of least privilege** — don't run as root
- Use **capabilities** instead of full root access when elevated privileges are needed
- Implement **SELinux/AppArmor** policies for services
- Use **seccomp** to restrict system calls
- Validate all **file paths** — prevent path traversal
- Use **/dev/urandom** for cryptographic randomness
- Support **encrypted storage** for sensitive data

### Packaging and Distribution
- **DEB** packages for Debian/Ubuntu ecosystems
- **RPM** packages for Red Hat/Fedora/SUSE ecosystems
- **Flatpak** or **Snap** for universal Linux desktop distribution
- **AppImage** for portable desktop applications
- **Container images** for server applications and microservices
- **Language package managers** (pip, npm, cargo, go modules) for libraries

### Process Management
- Handle **signals** properly (SIGTERM, SIGINT, SIGHUP, SIGUSR1/2)
- Use **systemd** for service lifecycle management
- Implement **proper forking** if daemonizing manually
- Use **cgroups** for resource control
- Implement **inter-process communication** via Unix sockets, D-Bus, or message queues

### Networking
- Support both **IPv4 and IPv6**
- Use **SO_REUSEADDR** and **SO_REUSEPORT** appropriately
- Handle **socket timeouts** and **connection pooling**
- Use **epoll/io_uring** for high-performance network I/O
- Follow **iptables/nftables** best practices for firewall rules
