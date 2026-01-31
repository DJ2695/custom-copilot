# Fastlane Setup for Flutter

## Installation

```bash
# macOS
brew install fastlane

# Alternative (Ruby gem)
sudo gem install fastlane
```

## iOS Setup

### Initialize

```bash
cd ios
fastlane init
```

**Select option:** "Automate App Store distribution"

**Prompts:**
- Apple ID
- App Identifier (bundle ID)
- Team ID (optional, auto-detected)

### Configure Fastfile

**Location:** `ios/fastlane/Fastfile`

```ruby
default_platform(:ios)

platform :ios do
  desc "Push a new beta build to TestFlight"
  lane :beta do
    increment_build_number(xcodeproj: "Runner.xcodeproj")
    build_app(scheme: "Runner")
    upload_to_testflight(skip_waiting_for_build_processing: true)
  end

  desc "Push a new release to the App Store"
  lane :release do
    increment_build_number(xcodeproj: "Runner.xcodeproj")
    build_app(scheme: "Runner")
    upload_to_app_store(
      force: true,
      skip_metadata: false,
      skip_screenshots: false
    )
  end
  
  desc "Take screenshots"
  lane :screenshots do
    capture_screenshots
    upload_to_app_store(
      skip_binary_upload: true,
      skip_metadata: true
    )
  end
end
```

### App Store Connect API Key (Recommended)

**Setup:**
1. App Store Connect → Users and Access → Keys
2. Generate API Key
3. Download `.p8` file
4. Note Key ID and Issuer ID

**Configure:**
```ruby
# fastlane/Fastfile
app_store_connect_api_key(
  key_id: "ABC123",
  issuer_id: "12345678-1234-1234-1234-123456789012",
  key_filepath: "./AuthKey_ABC123.p8"
)
```

### Credentials

**Option A: Environment Variables**
```bash
export FASTLANE_USER="your@email.com"
export FASTLANE_PASSWORD="your-password"
export FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD="xxxx-xxxx-xxxx-xxxx"
```

**Option B: Fastlane Match** (team collaboration)
```bash
fastlane match init
fastlane match development
fastlane match appstore
```

## Android Setup

### Initialize

```bash
cd android
fastlane init
```

**Select:** "Upload to Play Store"

**Prompts:**
- Package name
- Path to service account JSON

### Service Account Setup

1. [Google Cloud Console](https://console.cloud.google.com/)
2. Enable Google Play Android Developer API
3. Create service account
4. Download JSON key
5. Grant access in Play Console:
   - Settings → API access
   - Link service account
   - Grant "Release manager" role

### Configure Fastfile

**Location:** `android/fastlane/Fastfile`

```ruby
default_platform(:android)

platform :android do
  desc "Upload to internal testing track"
  lane :internal do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(
      track: "internal",
      aab: "../app/build/outputs/bundle/release/app-release.aab",
      skip_upload_apk: true
    )
  end

  desc "Promote internal to production"
  lane :production do
    upload_to_play_store(
      track: "internal",
      track_promote_to: "production",
      rollout: "0.1",  # 10% staged rollout
      skip_upload_aab: true,
      skip_upload_apk: true,
      skip_upload_metadata: true,
      skip_upload_images: true,
      skip_upload_screenshots: true
    )
  end
  
  desc "Full release to production"
  lane :release do
    gradle(task: "bundle", build_type: "Release")
    upload_to_play_store(
      track: "production",
      aab: "../app/build/outputs/bundle/release/app-release.aab",
      rollout: "0.1"
    )
  end
end
```

### Credentials

**Location:** `android/fastlane/service_account.json`

```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "...",
  "client_email": "...",
  "client_id": "...",
  ...
}
```

**⚠️ Important:** Add to `.gitignore`

## Common Configuration

### Appfile

**iOS (`ios/fastlane/Appfile`):**
```ruby
app_identifier("com.example.myapp")
apple_id("your@email.com")
team_id("ABC123")
```

**Android (`android/fastlane/Appfile`):**
```ruby
json_key_file("service_account.json")
package_name("com.example.myapp")
```

### .env Files

**Structure:**
```
fastlane/
├── .env.default      # Default values
├── .env.development  # Dev environment
├── .env.staging      # Staging
└── .env.production   # Production
```

**Example `.env.production`:**
```bash
FASTLANE_USER="your@email.com"
FASTLANE_TEAM_ID="ABC123"
APP_IDENTIFIER="com.example.myapp"
```

**Use in Fastfile:**
```ruby
app_identifier(ENV["APP_IDENTIFIER"])
```

## Metadata Management

### iOS Metadata

```bash
cd ios
fastlane deliver init
```

**Structure:**
```
fastlane/metadata/
├── en-US/
│   ├── name.txt
│   ├── subtitle.txt
│   ├── description.txt
│   ├── keywords.txt
│   ├── release_notes.txt
│   └── privacy_url.txt
└── screenshots/
    └── en-US/
        ├── iPhone-6.5/
        └── iPhone-5.5/
```

### Android Metadata

```bash
cd android
fastlane supply init
```

**Structure:**
```
fastlane/metadata/android/
├── en-US/
│   ├── title.txt
│   ├── short_description.txt
│   ├── full_description.txt
│   └── changelogs/
│       └── 46.txt
└── images/
    ├── phoneScreenshots/
    └── featureGraphic.png
```

## Advanced Lanes

### Increment Version

```ruby
lane :bump_version do
  increment_version_number(
    bump_type: "patch"  # major, minor, or patch
  )
  increment_build_number
  commit_version_bump(
    message: "Bump version"
  )
end
```

### Tests Before Release

```ruby
lane :test_and_release do
  run_tests
  build_app
  upload_to_testflight
end
```

### Notifications

```ruby
lane :beta do
  build_app
  upload_to_testflight
  
  slack(
    message: "New TestFlight build uploaded!",
    channel: "#releases"
  )
end
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `fastlane` command not found | Add to PATH or use `bundle exec fastlane` |
| Authentication fails (iOS) | Generate app-specific password for 2FA |
| Service account error (Android) | Verify API enabled and permissions granted |
| Build not found | Check scheme/flavor names match |
| Upload timeout | Increase timeout: `ENV["FASTLANE_XCODEBUILD_SETTINGS_TIMEOUT"] = "120"` |

## Best Practices

✅ **DO:**
- Use App Store Connect API Key (iOS)
- Use service accounts (Android)
- Version control Fastfile and Appfile
- Use `.env` files for sensitive data
- Test lanes locally before CI/CD
- Document custom lanes

❌ **DON'T:**
- Commit API keys or service account JSON
- Hardcode credentials in Fastfiles
- Skip error handling in lanes
- Use personal accounts for automation

## CI/CD Integration

See [CI/CD Integration Guide](cicd-integration.md) for GitHub Actions setup.
