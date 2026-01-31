---
name: flutter-app-release
description: 'Release Flutter apps to iOS (TestFlight/App Store), Android (Play Store), and Web (Firebase Hosting). Use when: (1) Building and releasing Flutter apps, (2) Managing app versioning, (3) Deploying to app stores or web hosting, (4) Setting up CI/CD for Flutter releases. Keywords: flutter, ios, android, web, release, testflight, play store, firebase hosting, app deployment.'
---

# Flutter App Release

Release Flutter apps to iOS App Store, Android Play Store, and web hosting platforms.

## When to Use

- Building Flutter releases for iOS, Android, or web
- Publishing to TestFlight, App Store, or Play Store
- Deploying Flutter web apps
- Managing versions and build numbers
- Setting up automated releases

## Versioning

**pubspec.yaml:** `version: 1.2.3+45` (semantic version + build number)

```bash
flutter pub version patch  # 1.2.3 → 1.2.4
flutter pub version minor  # 1.2.x → 1.3.0
flutter pub version major  # 1.x.x → 2.0.0
```

**Rule:** Increment build number (+45 → +46) for every release

## Quick Release

### iOS
```bash
flutter build ipa --release
cd ios && fastlane beta  # TestFlight
```

### Android
```bash
flutter build appbundle --release
cd android && fastlane internal  # Internal testing
```

### Web
```bash
flutter build web --release
firebase deploy --only hosting  # Firebase
# or: netlify deploy --prod
```

## Platform Setup

### iOS
```bash
brew install fastlane
cd ios && fastlane init
# Requires: Xcode, Apple Developer account
```

### Android
```bash
cd android && fastlane init
# Requires: Keystore, Play Console service account
```

### Web
```bash
firebase init hosting
# or setup: Netlify, Vercel, GitHub Pages
```

## References

- **[iOS Release](references/ios-release.md)** - TestFlight and App Store workflow
- **[Android Release](references/android-release.md)** - Play Store deployment
- **[Web Deployment](references/web-deployment.md)** - Firebase, Netlify, Vercel
- **[Fastlane Setup](references/fastlane-setup.md)** - iOS/Android automation
- **[CI/CD](references/cicd-integration.md)** - GitHub Actions workflows

## Templates

- **[iOS Fastfile](templates/ios-fastfile.rb)**
- **[Android Fastfile](templates/android-fastfile.rb)**
- **[iOS Workflow](templates/ios-release.yaml)**
- **[Android Workflow](templates/android-release.yaml)**
- **[Web Workflow](templates/web-deploy.yaml)**

## Best Practices

✅ Test on TestFlight/internal before production, use staged rollouts, increment versions
❌ Don't commit signing keys, skip testing, or release to 100% immediately

## Quick Commands

```bash
# Clean build
flutter clean && flutter pub get

# Build
flutter build ipa --release          # iOS
flutter build appbundle --release    # Android
flutter build web --release          # Web

# Release
cd ios && fastlane beta             # TestFlight
cd android && fastlane production   # Play Store
firebase deploy --only hosting      # Web
```

## Resources

- [Flutter Deployment Docs](https://docs.flutter.dev/deployment)
- [App Store Guidelines](https://developer.apple.com/app-store/review/guidelines/)
- [Play Console Help](https://support.google.com/googleplay/android-developer)
