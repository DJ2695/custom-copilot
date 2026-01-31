# CI/CD Integration for Flutter Releases

## Multi-Platform Release Workflow

**File:** `.github/workflows/flutter-release.yaml`

```yaml
name: Flutter Release

on:
  workflow_dispatch:
    inputs:
      platform:
        description: 'Platform to release'
        required: true
        type: choice
        options:
          - ios
          - android
          - web
          - all

jobs:
  release-ios:
    if: inputs.platform == 'ios' || inputs.platform == 'all'
    runs-on: macos-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
          cache: true
      - run: flutter pub get
      - run: flutter build ipa --release
      - run: cd ios && bundle install && bundle exec fastlane beta
        env:
          FASTLANE_USER: ${{ secrets.FASTLANE_USER }}
          FASTLANE_PASSWORD: ${{ secrets.FASTLANE_PASSWORD }}
          FASTLANE_APPLE_APPLICATION_SPECIFIC_PASSWORD: ${{ secrets.FASTLANE_ASP }}
  
  release-android:
    if: inputs.platform == 'android' || inputs.platform == 'all'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
          cache: true
      - run: flutter pub get
      - name: Setup signing
        run: |
          echo "${{ secrets.KEYSTORE_BASE64 }}" | base64 -d > android/app/release.keystore
          echo "storeFile=release.keystore" > android/key.properties
          echo "storePassword=${{ secrets.KEYSTORE_PASSWORD }}" >> android/key.properties
          echo "keyAlias=${{ secrets.KEY_ALIAS }}" >> android/key.properties
          echo "keyPassword=${{ secrets.KEY_PASSWORD }}" >> android/key.properties
      - run: flutter build appbundle --release
      - run: |
          echo '${{ secrets.PLAY_STORE_CONFIG_JSON }}' > android/fastlane/service_account.json
          cd android && bundle install && bundle exec fastlane internal
      - run: rm -f android/app/release.keystore android/key.properties android/fastlane/service_account.json
        if: always()
  
  release-web:
    if: inputs.platform == 'web' || inputs.platform == 'all'
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.x'
          cache: true
      - run: flutter pub get
      - run: flutter build web --release
      - uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: live
          projectId: your-project-id
```

## Platform-Specific Workflows

See templates for individual platform workflows:
- [iOS Release Workflow](../templates/ios-release.yaml)
- [Android Release Workflow](../templates/android-release.yaml)
- [Web Deploy Workflow](../templates/web-deploy.yaml)

## Required Secrets

### iOS
- `FASTLANE_USER` - Apple ID
- `FASTLANE_PASSWORD` - Apple ID password
- `FASTLANE_ASP` - App-specific password
- `MATCH_PASSWORD` - Fastlane match passphrase (optional)

### Android
- `KEYSTORE_BASE64` - Base64 encoded keystore
- `KEYSTORE_PASSWORD` - Keystore password
- `KEY_ALIAS` - Key alias
- `KEY_PASSWORD` - Key password
- `PLAY_STORE_CONFIG_JSON` - Service account JSON

### Web
- `FIREBASE_SERVICE_ACCOUNT` - Firebase service account JSON
- Or: `NETLIFY_AUTH_TOKEN` & `NETLIFY_SITE_ID`
- Or: `VERCEL_TOKEN` & `VERCEL_ORG_ID` & `VERCEL_PROJECT_ID`

## Automated Version Bumping

```yaml
name: Bump Version

on:
  workflow_dispatch:
    inputs:
      bump:
        type: choice
        options: [patch, minor, major]

jobs:
  bump:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub version ${{ inputs.bump }}
      - run: |
          git config user.name "GitHub Actions"
          git config user.email "actions@github.com"
          git add pubspec.yaml
          git commit -m "Bump version (${{ inputs.bump }})"
          git push
```

## Environment-Based Deployment

```yaml
name: Deploy by Environment

on:
  push:
    branches:
      - develop   # staging
      - main      # production

jobs:
  deploy-web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: subosito/flutter-action@v2
      - run: flutter pub get
      - name: Build for environment
        run: |
          if [[ "${{ github.ref }}" == "refs/heads/main" ]]; then
            flutter build web --release --dart-define=ENV=production
          else
            flutter build web --release --dart-define=ENV=staging
          fi
      - uses: FirebaseExtended/action-hosting-deploy@v0
        with:
          repoToken: '${{ secrets.GITHUB_TOKEN }}'
          firebaseServiceAccount: '${{ secrets.FIREBASE_SERVICE_ACCOUNT }}'
          channelId: ${{ github.ref == 'refs/heads/main' && 'live' || 'staging' }}
          projectId: your-project-id
```

## Best Practices

✅ **DO:**
- Use workflow_dispatch for manual control
- Store all credentials in secrets
- Clean up sensitive files after use
- Use caching for faster builds
- Add approval gates for production

❌ **DON'T:**
- Commit signing keys or credentials
- Echo secrets in logs
- Skip cleanup steps
- Deploy without testing

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Flutter version mismatch | Pin specific version in workflow |
| iOS build timeout | Use macos-latest-xlarge runner |
| Android signing fails | Verify base64 encoding is correct |
| Web deploy fails | Check Firebase project ID and permissions |
| Fastlane auth fails | Regenerate app-specific password |
