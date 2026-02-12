---
name: Windows Development Platform Instructions
description: Platform-specific guidance for Windows application development
---

<!-- Catalog Metadata
id: INST-PLAT-002
version: 1.0.0
scope: platform
applies_to: windows
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Windows Development — Platform Instructions

## Scope
These instructions apply when building **Windows desktop applications**, services, and system tools.

## UI Frameworks

### WinUI 3 (Recommended for new Windows apps)
- Modern, native Windows UI framework
- Part of the Windows App SDK
- Fluent Design System support
- Supports packaged (MSIX) and unpackaged deployment
- Use for new Windows desktop applications targeting Windows 10 1809+

### WPF (Windows Presentation Foundation)
- Mature XAML-based framework with rich data binding
- Largest ecosystem of controls and libraries
- Use for enterprise line-of-business applications
- Consider for apps that need rich printing, complex data grids

### .NET MAUI
- Cross-platform (Windows, macOS, iOS, Android)
- Single codebase with platform-specific customization
- Use when targeting multiple platforms from a single project

### Win32 / C++
- Maximum performance and system access
- Use for system tools, drivers, performance-critical applications
- Consider when interfacing with existing native codebases

## Windows-Specific Considerations

### Deployment
- **MSIX**: Modern packaging, clean install/uninstall, auto-update support
- **ClickOnce**: Simple deployment for .NET apps, web-based install
- **MSI/WiX**: Traditional installer, complex but flexible
- **Microsoft Store**: Distribution channel, sandboxed, auto-updates
- **winget**: Command-line package manager integration

### Security
- Follow **Windows security best practices**: UAC integration, code signing
- Use **Windows Credential Manager** for storing user credentials
- Sign executables and installers with **Authenticode certificates**
- Implement **AppContainer** isolation where appropriate
- Use **Windows DPAPI** for local data encryption
- Request **minimum permissions** — don't require admin unless necessary

### Performance
- Use **async patterns** to keep the UI thread responsive
- Implement **virtualization** for large lists (VirtualizingStackPanel)
- Profile with **Windows Performance Toolkit** (WPT) and **PerfView**
- Minimize **startup time** — defer non-essential initialization
- Use **compiled bindings** (x:Bind in WinUI) for better performance

### Accessibility
- Support **Windows Narrator** and other screen readers
- Implement **UI Automation** patterns for custom controls
- Support **High Contrast** themes
- Support **keyboard navigation** for all interactive elements
- Follow **Fluent Design accessibility guidelines**

### Data and Storage
- Use **SQLite** for local structured data
- Use **ApplicationData** APIs for app-specific settings
- Support **roaming settings** for multi-device scenarios
- Handle **file system permissions** properly
- Support **OneDrive** integration for document-centric apps

## Common Patterns

### MVVM (Model-View-ViewModel)
- Standard architecture for XAML-based apps
- Use **CommunityToolkit.Mvvm** for boilerplate reduction
- Keep ViewModels testable — no UI framework dependencies
- Use **messaging** for cross-ViewModel communication

### Background Processing
- Use **BackgroundWorker** or **Task.Run** for CPU-bound work
- Use **Windows Services** for long-running background processes
- Consider **Windows Task Scheduler** for periodic tasks
- Use **AppService** for inter-process communication
