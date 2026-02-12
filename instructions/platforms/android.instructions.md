---
name: Android Development Platform Instructions
description: Platform-specific guidance for Android application development
---

<!-- Catalog Metadata
id: INST-PLAT-004
version: 1.0.0
scope: platform
applies_to: android
priority: high
author: community
last_reviewed: 2026-02-12
-->

# Android Development — Platform Instructions

## Scope
These instructions apply when building **Android applications** — native or cross-platform.

## Technology Choices

### Native Android (Recommended for Android-first apps)
- **Kotlin** — primary language, officially recommended by Google
- **Jetpack Compose** — modern declarative UI toolkit (preferred for new projects)
- **XML Layouts** — traditional imperative UI (still valid for existing projects)
- **Android Studio** — official IDE

### Cross-Platform
- **Flutter** (Dart) — high-performance, single codebase, custom rendering
- **React Native** (JavaScript/TypeScript) — web developer friendly, native bridge
- **.NET MAUI** (C#) — Microsoft ecosystem, single codebase for mobile + desktop
- **Kotlin Multiplatform** — shared business logic, native UI per platform

## Android-Specific Considerations

### Architecture
- Follow **Modern Android Architecture** (Google's recommended approach)
- Use **MVVM** with **ViewModel**, **LiveData**, or **StateFlow**
- Implement **Repository pattern** for data access
- Use **Hilt/Dagger** for dependency injection
- Separate **UI layer**, **domain layer**, and **data layer**
- Use **Navigation Component** for screen navigation
- Handle **configuration changes** properly (rotation, locale change)

### Lifecycle Management
- Respect **Activity/Fragment lifecycle** — release resources appropriately
- Use **ViewModel** for data that survives configuration changes
- Use **SavedStateHandle** for data that survives process death
- Handle **back stack** navigation correctly
- Support **multi-window** and **picture-in-picture** where appropriate

### Performance
- Keep **main thread** free — offload work with Coroutines or WorkManager
- Use **RecyclerView** with ViewHolder pattern (or LazyColumn in Compose)
- Optimize **startup time** — defer non-critical initialization
- Use **baseline profiles** for AOT compilation of hot paths
- Minimize **overdraw** in UI rendering
- Use **Android Profiler** for CPU, memory, and network analysis
- Implement **R8/ProGuard** for code shrinking and obfuscation

### Security
- Use **Android Keystore** for cryptographic key storage
- Implement **certificate pinning** for sensitive API communication
- Use **EncryptedSharedPreferences** for sensitive local data
- Follow **Android security best practices** from Google
- Implement **biometric authentication** for sensitive operations
- Apply **ProGuard/R8** rules to obfuscate code
- Never store **secrets in the APK** — they can be extracted
- Use **SafetyNet/Play Integrity API** for device attestation

### Permissions
- Request **only necessary permissions**
- Request permissions **at the point of use**, not on startup
- Handle **permission denial** gracefully — degrade functionality, don't crash
- Support **runtime permissions** (Android 6.0+)
- Respect **scoped storage** (Android 10+)

### Testing
- **Unit tests**: JUnit, Mockito/MockK for business logic
- **UI tests**: Espresso (View-based) or Compose testing APIs
- **Integration tests**: Robolectric for fast JVM-based Android tests
- **End-to-end**: UI Automator for cross-app scenarios
- Test on **multiple API levels** and **screen sizes**

### Distribution
- **Google Play Store** — primary distribution channel
- Support **App Bundles** (AAB) for optimized delivery
- Implement **in-app updates** for critical fixes
- Set appropriate **minSdk**, **targetSdk**, and **compileSdk**
- Follow **Google Play policies** for content and monetization
