# Flutter Web Deployment

## Build Configuration

### Build for Web

```bash
flutter build web --release

# Build output: build/web/
```

### Build Options

```bash
# With specific renderer
flutter build web --web-renderer canvaskit  # Better graphics
flutter build web --web-renderer html       # Smaller size

# With base href for subdirectory hosting
flutter build web --base-href /app/

# Development build
flutter build web --profile
```

## Deployment Platforms

### Firebase Hosting

**Setup:**
```bash
firebase login
firebase init hosting
```

**firebase.json:**
```json
{
  "hosting": {
    "public": "build/web",
    "ignore": ["firebase.json", "**/.*", "**/node_modules/**"],
    "rewrites": [
      {
        "source": "**",
        "destination": "/index.html"
      }
    ]
  }
}
```

**Deploy:**
```bash
flutter build web --release
firebase deploy --only hosting

# Preview before deploy
firebase hosting:channel:deploy preview
```

### Netlify

**netlify.toml:**
```toml
[build]
  command = "flutter build web --release"
  publish = "build/web"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
```

**Deploy:**
```bash
# Install CLI
npm install -g netlify-cli

# Deploy
flutter build web --release
netlify deploy --prod --dir=build/web
```

**Auto-deploy from Git:**
1. Connect repo in Netlify UI
2. Set build command: `flutter build web --release`
3. Set publish directory: `build/web`

### Vercel

**vercel.json:**
```json
{
  "buildCommand": "flutter build web --release",
  "outputDirectory": "build/web",
  "routes": [
    {
      "src": "/(.*)",
      "dest": "/index.html"
    }
  ]
}
```

**Deploy:**
```bash
# Install CLI
npm install -g vercel

# Deploy
flutter build web --release
vercel --prod
```

### GitHub Pages

**Deploy script:**
```bash
#!/bin/bash
flutter build web --release --base-href /repo-name/
cd build/web
git init
git add -A
git commit -m "Deploy"
git push -f git@github.com:username/repo-name.git master:gh-pages
```

**Or use GitHub Actions** (see CI/CD Integration)

### Docker + Nginx

**Dockerfile:**
```dockerfile
FROM nginx:alpine
COPY build/web /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Build and run:**
```bash
flutter build web --release
docker build -t flutter-web .
docker run -p 8080:80 flutter-web
```

## Environment Configuration

### Environment Variables

```bash
# Build with env variables
flutter build web --release --dart-define=API_URL=https://api.prod.com

# Multiple variables
flutter build web --release \
  --dart-define=API_URL=https://api.prod.com \
  --dart-define=ENV=production
```

**Access in code:**
```dart
const apiUrl = String.fromEnvironment('API_URL', defaultValue: 'http://localhost');
```

### Environment Files

**web/env.js:**
```javascript
window.ENV = {
  apiUrl: 'https://api.prod.com',
  environment: 'production'
};
```

**web/index.html:**
```html
<script src="env.js"></script>
```

**Access in Dart:**
```dart
import 'dart:html' as html;

String getApiUrl() {
  return html.window.localStorage['apiUrl'] ?? 'default-url';
}
```

## Performance Optimization

### Reduce Build Size

**pubspec.yaml:**
```yaml
flutter:
  uses-material-design: true
  # Only include needed fonts
  fonts:
    - family: Roboto
      fonts:
        - asset: fonts/Roboto-Regular.ttf
```

**Build with tree shaking:**
```bash
flutter build web --release --tree-shake-icons
```

### Caching Strategy

**web/index.html:**
```html
<script>
  if ('serviceWorker' in navigator) {
    window.addEventListener('flutter-first-frame', function () {
      navigator.serviceWorker.register('flutter_service_worker.js');
    });
  }
</script>
```

### CDN Integration

Use Firebase Hosting, Netlify, or Cloudflare for automatic CDN.

## Custom Domain

### Firebase Hosting

```bash
firebase hosting:sites:create my-site
firebase target:apply hosting prod my-site
firebase deploy --only hosting:prod
```

**Add custom domain:**
1. Firebase Console → Hosting
2. Add custom domain
3. Add DNS records

### Netlify

1. Netlify Dashboard → Domain settings
2. Add custom domain
3. Configure DNS

### DNS Records

**Typical setup:**
```
A     @       192.0.2.1
CNAME www     your-site.netlify.app
```

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Blank page after deploy | Check base-href matches hosting path |
| Assets not loading | Verify asset paths in pubspec.yaml |
| Routing breaks on refresh | Add rewrite rule for SPA |
| Large bundle size | Use `--web-renderer html` or optimize assets |
| CORS errors | Configure backend CORS headers |

### Debug Deployed Site

```bash
# Serve locally like production
flutter build web --release
cd build/web
python -m http.server 8000
```

## CI/CD Integration

See [CI/CD Integration](cicd-integration.md) for GitHub Actions workflows.

**Quick example:**
```yaml
- name: Build and deploy web
  run: |
    flutter build web --release
    firebase deploy --only hosting --token ${{ secrets.FIREBASE_TOKEN }}
```

## Best Practices

✅ **DO:**
- Use CDN for static assets
- Enable caching headers
- Minimize bundle size
- Test on multiple browsers
- Use environment variables for API URLs
- Set up staging environment

❌ **DON'T:**
- Hardcode API URLs
- Skip browser compatibility testing
- Deploy without testing build locally
- Forget base-href for subdirectory hosting
- Commit environment secrets
