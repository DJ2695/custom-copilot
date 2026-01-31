# iOS Release Guide for Flutter

## Complete Release Workflow

### 1. Prepare Release

**Pre-release checklist:**
- [ ] All features complete and tested
- [ ] CI/CD passing
- [ ] No debug code or console logs
- [ ] Release notes written

**Update version in `pubspec.yaml`:**
```yaml
version: 1.2.3+46  # version+buildNumber
```

### 2. Build

**Flutter:**
```bash
flutter clean
flutter pub get
flutter build ipa --release
```

**Manual Xcode:**
1. Open `ios/Runner.xcworkspace`
2. Select "Any iOS Device (arm64)"
3. Product → Archive
4. Wait for archive to complete

### 3. Upload to TestFlight

**Option A: fastlane (Recommended)**
```bash
cd ios
fastlane beta
```

**Option B: Transporter App**
1. Find `.ipa` in `build/ios/ipa/`
2. Open Transporter app
3. Drag `.ipa` to Transporter
4. Wait for upload

**Option C: Xcode Organizer**
1. Window → Organizer
2. Select archive
3. Distribute App → App Store Connect
4. Follow prompts

### 4. TestFlight Testing

**Processing:** 5-30 minutes after upload

**Steps:**
1. [App Store Connect](https://appstoreconnect.apple.com/) → App → TestFlight
2. Select build
3. Add to testing group
4. Add internal testers
5. Notify testers

**Testing checklist:**
- [ ] App launches successfully
- [ ] Key user flows work
- [ ] No crashes on different devices
- [ ] Performance acceptable

### 5. Submit to App Store

1. App Store Connect → App Store tab
2. Create new version (if needed)
3. Select build from TestFlight
4. Fill release information:
   - What's new in this version
   - Screenshots (if changed)
   - App description (if changed)
5. Submit for review

**Review time:** Typically 24-48 hours

### 6. Release Options

- **Automatic:** Goes live immediately after approval
- **Manual:** Hold for manual release
- **Scheduled:** Release on specific date

## Troubleshooting

| Problem | Solution |
|---------|----------|
| Build fails | `flutter clean && cd ios && pod install` |
| Signing error | Check certificates in Xcode → Preferences → Accounts |
| Upload rejected | Check App Store Connect for rejection reason |
| Missing entitlements | Add to `Runner.entitlements` |
| Provisioning profile issue | Regenerate in Apple Developer portal |
| "Archive not valid" | Check bundle ID and provisioning profiles |

### Clean Build

```bash
flutter clean
rm -rf ios/Pods ios/Podfile.lock
cd ios && pod install
flutter build ipa --release
```

### Check Certificates

```bash
# List certificates
security find-identity -v -p codesigning

# Verify profile
cd ~/Library/MobileDevice/Provisioning\ Profiles/
ls -la
```

## Version Management

### Info.plist

Ensure version matches `pubspec.yaml` (handled automatically by Flutter):

```xml
<key>CFBundleShortVersionString</key>
<string>1.2.3</string>
<key>CFBundleVersion</key>
<string>46</string>
```

### Increment Build Number

```bash
cd ios
agvtool next-version -all
```

## Screenshots and Assets

### Required Screenshots

| Device | Size |
|--------|------|
| 6.7" Display | 1290 x 2796 |
| 6.5" Display | 1284 x 2778 |
| 5.5" Display | 1242 x 2208 |

**Tools:**
- [fastlane snapshot](https://docs.fastlane.tools/actions/snapshot/)
- [App Store Screenshot Generator](https://www.appstorescreenshot.com/)

### App Icon

- Required: 1024x1024 PNG (no alpha channel)
- Location: `ios/Runner/Assets.xcassets/AppIcon.appiconset/`

## Post-Release

- [ ] Monitor crash reports in App Store Connect
- [ ] Check user reviews
- [ ] Verify analytics show expected behavior
- [ ] Tag release in git: `git tag v1.2.3`

## fastlane Commands

```bash
cd ios

fastlane beta              # Upload to TestFlight
fastlane release           # Release to App Store
fastlane snapshot          # Generate screenshots
fastlane match development # Sync certificates
```
