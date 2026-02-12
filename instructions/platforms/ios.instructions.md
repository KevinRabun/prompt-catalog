---
name: iOS Development Platform Instructions
description: Platform-specific guidance for iOS/iPadOS application development
---

<!-- Catalog Metadata
id: INST-PLAT-005
version: 1.0.0
scope: platform
applies_to: ios
priority: high
author: community
last_reviewed: 2026-02-12
-->

# iOS Development — Platform Instructions

## Scope
These instructions apply when building **iOS and iPadOS applications** — native or cross-platform.

## Technology Choices

### Native iOS (Recommended for iOS-first apps)
- **Swift** — primary language, officially recommended by Apple
- **SwiftUI** — modern declarative UI framework (preferred for new projects)
- **UIKit** — imperative UI framework (still important for complex/existing apps)
- **Xcode** — required IDE for iOS development and submission

### Cross-Platform
- **Flutter** (Dart) — custom rendering engine, high-performance
- **React Native** (JavaScript/TypeScript) — web developer friendly
- **.NET MAUI** (C#) — Microsoft ecosystem
- **Kotlin Multiplatform** — share business logic with Android

## iOS-Specific Considerations

### Architecture
- Use **MVVM** or **TCA (The Composable Architecture)** for SwiftUI
- Use **MVC** or **MVVM-C** for UIKit-based apps
- Implement **protocol-oriented programming** where appropriate
- Use **Swift Concurrency** (async/await, actors) for concurrent code
- Separate concerns with **Swift packages** for modular architecture
- Use **dependency injection** — protocols and constructor injection

### SwiftUI Best Practices
- Keep **views small** and composable
- Use **@StateObject** for owned state, **@ObservedObject** for passed state
- Implement **@EnvironmentObject** for dependency injection of shared state
- Use **preview providers** for rapid iteration
- Support **Dynamic Type** and **Dark Mode** from the start
- Handle **Safe Area** insets properly

### UIKit Best Practices
- Use **Auto Layout** with constraints (avoid frame-based layout)
- Implement **coordinator pattern** for navigation
- Use **diffable data sources** for table and collection views
- Implement **proper cell reuse** in table and collection views

### Performance
- Profile with **Instruments** (Time Profiler, Allocations, Leaks)
- Use **lazy loading** for expensive resources
- Implement **image caching** and proper memory management
- Optimize **app launch time** — defer non-essential work
- Use **background fetch** and **BGTaskScheduler** for background work
- Minimize **main thread work** — UI must remain responsive
- Keep **app size** manageable (App Thinning, on-demand resources)

### Security
- Use **Keychain Services** for storing credentials and tokens
- Implement **App Transport Security** (ATS) — HTTPS required by default
- Use **certificate pinning** for sensitive API communication
- Implement **biometric authentication** (Face ID / Touch ID) via the LocalAuthentication framework
- Enable **Data Protection** for file encryption
- Never store **secrets in the app bundle** — they can be extracted
- Use **App Attest** for server-side device verification

### Privacy
- Implement **App Tracking Transparency** (ATT) for tracking
- Complete the **Privacy Nutrition Label** accurately in App Store Connect
- Handle **location, camera, microphone, photos** permissions properly
- Request permissions **in context** with clear usage descriptions
- Support **Sign in with Apple** if offering third-party sign-in

### Testing
- **Unit tests**: XCTest framework for business logic
- **UI tests**: XCUITest for automated UI testing
- **Snapshot tests**: For visual regression testing
- **Performance tests**: XCTest measure blocks
- Test on **multiple device sizes** (iPhone SE, iPhone 15, iPad)
- Test with **accessibility features** enabled (VoiceOver, Dynamic Type)

### Distribution
- **App Store** — primary distribution channel
- **TestFlight** — beta testing distribution
- **Enterprise distribution** — for internal corporate apps
- Follow **App Store Review Guidelines** carefully
- Support required **device capabilities** and **minimum iOS version**
- Comply with **Apple's Human Interface Guidelines**
