# Android Release Guide for Flutter

## Complete Release Workflow

### 1. Prepare Release

**Pre-release checklist:**
- [ ] All features complete and tested
- [ ] CI/CD passing
- [ ] Release notes written
- [ ] Signing configuration verified

**Update version in `pubspec.yaml`:**
```yaml
version: 1.2.3+46  # Build number must be higher than previous
```

### 2. Verify Signing

**Check `android/app/build.gradle`:**
```groovy
android {
    signingConfigs {
        release {
            storeFile file(MYAPP_RELEASE_STORE_FILE)
            storePassword MYAPP_RELEASE_STORE_PASSWORD
            keyAlias MYAPP_RELEASE_KEY_ALIAS
            keyPassword MYAPP_RELEASE_KEY_PASSWORD
        }
    }
    buildTypes {
        release {
            signingConfig signingConfigs.release
        }
    }
}
```

**Check `android/key.properties`:**
```properties
storeFile=release.keystore
storePassword=***
keyAlias=upload
keyPassword=***
```

### 3. Build

**Flutter:**
```bash
flutter clean
flutter pub get
flutter build appbundle --release
```

**Output location:**
- `build/app/outputs/bundle/release/app-release.aab`

### 4. Upload to Play Store

**Option A: fastlane (Recommended)**
```bash
cd android
fastlane internal  # Internal testing track
```

**Option B: Play Console**
1. [Google Play Console](https://play.google.com/console/)
2. Select app
3. Release → Testing → Internal testing
4. Create new release
5. Upload `.aab` file
6. Fill release notes
7. Review and roll out

### 5. Testing Tracks

| Track | Purpose | Audience |
|-------|---------|----------|
| Internal | Quick testing | Up to 100 testers |
| Closed | Larger group | Specified testers |
| Open | Public beta | Anyone with link |

**After upload:**
1. Add testers (email list or Google Group)
2. Share testing link
3. Monitor crash reports
4. Iterate if needed

### 6. Production Release

**Promote from testing:**
1. Play Console → Production
2. Create new release
3. Select build from testing track
4. Fill release notes
5. Choose rollout percentage

**Staged rollout strategy:**
- Day 1: 10% of users
- Day 2-3: Monitor, increase to 50% if stable
- Day 4-5: Monitor, increase to 100%

### 7. Monitor

- Check crash reports in Play Console
- Monitor ANRs (Application Not Responding)
- Watch user reviews
- Track analytics

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | `flutter clean && cd android && ./gradlew clean` |
| Signing error | Verify keystore path and passwords in `key.properties` |
| Upload rejected | Check Play Console for policy violations |
| Version code conflict | Increment build number in `pubspec.yaml` |
| Missing permissions | Add to `AndroidManifest.xml` |
| "Duplicate classes" error | Check for dependency conflicts |

### Clean Build

```bash
flutter clean
cd android
./gradlew clean
cd ..
flutter build appbundle --release
```

### Verify Signing

```bash
# Check signed bundle
jarsigner -verify -verbose build/app/outputs/bundle/release/app-release.aab

# View keystore info
keytool -list -v -keystore android/app/release.keystore
```

## Version Management

### build.gradle

Flutter automatically reads version from `pubspec.yaml`:

```groovy
// android/app/build.gradle
def flutterVersionCode = localProperties.getProperty('flutter.versionCode')
def flutterVersionName = localProperties.getProperty('flutter.versionName')

android {
    defaultConfig {
        versionCode flutterVersionCode.toInteger()
        versionName flutterVersionName
    }
}
```

## Screenshots and Listing

### Required Screenshots

| Type | Min | Max | Size |
|------|-----|-----|------|
| Phone | 2 | 8 | 16:9 or 9:16 |
| 7" Tablet | 0 | 8 | 16:9 or 9:16 |
| 10" Tablet | 0 | 8 | 16:9 or 9:16 |

**Dimensions:**
- Phone: 1080 x 1920 minimum
- Tablet 7": 1024 x 1768 minimum
- Tablet 10": 1200 x 1920 minimum

### Feature Graphic

- Size: 1024 x 500
- Format: PNG or JPEG
- Required for Play Store listing

## App Signing

### Play App Signing (Recommended)

Google manages your app signing key:

1. Enable in Play Console → Release → Setup → App signing
2. Upload upload certificate
3. Google signs releases with app signing key

**Benefits:**
- Lost key recovery
- Automatic APK optimization
- Universal APKs

### Generate Upload Keystore

```bash
keytool -genkeypair -v \
  -keystore upload.keystore \
  -alias upload \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000
```

## Staged Rollout

**Manage rollout:**
```bash
cd android
fastlane supply \
  --track production \
  --rollout 0.1  # 10%
```

**Increase percentage:**
1. Play Console → Production
2. Manage release
3. Update rollout percentage
4. Confirm

**Halt rollout:**
- Click "Pause rollout" to stop at current percentage
- Fix issues
- Resume when ready

## Post-Release

- [ ] Monitor crash rates (should be <0.5%)
- [ ] Check ANR rate (should be <0.5%)
- [ ] Respond to user reviews
- [ ] Track downloads and ratings
- [ ] Tag release: `git tag android-v1.2.3`

## fastlane Commands

```bash
cd android

fastlane internal      # Upload to internal track
fastlane production    # Release to production
fastlane supply        # Update metadata
fastlane screenshots   # Generate screenshots
```
