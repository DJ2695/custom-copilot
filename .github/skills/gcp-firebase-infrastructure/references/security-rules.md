# Security Rules Reference

## Firestore Rules

### Basic User Data Protection

```javascript
rules_version = '2';
service cloud.firestore {
  match /databases/{database}/documents {
    // User can only access their own data
    match /users/{userId} {
      allow read, write: if request.auth.uid == userId;
    }
    
    // Public read, authenticated write
    match /public/{document} {
      allow read: if true;
      allow write: if request.auth != null;
    }
    
    // Role-based access
    match /admin/{document} {
      allow read, write: if request.auth.token.admin == true;
    }
  }
}
```

### Complex Validation Rules

```javascript
match /posts/{postId} {
  allow create: if request.auth != null
    && request.resource.data.title is string
    && request.resource.data.title.size() > 0
    && request.resource.data.title.size() <= 100;
  
  allow update: if request.auth.uid == resource.data.authorId
    && request.resource.data.title == resource.data.title; // Title cannot be changed
  
  allow delete: if request.auth.uid == resource.data.authorId;
}
```

## Cloud Storage Rules

### User-Specific Uploads

```javascript
rules_version = '2';
service firebase.storage {
  match /b/{bucket}/o {
    match /user-uploads/{userId}/{allPaths=**} {
      allow read, write: if request.auth.uid == userId;
    }
    
    match /public/{allPaths=**} {
      allow read: if true;
      allow write: if request.auth != null;
    }
  }
}
```

### File Type and Size Restrictions

```javascript
match /images/{imageId} {
  allow write: if request.auth != null
    && request.resource.contentType.matches('image/.*')
    && request.resource.size < 5 * 1024 * 1024; // 5MB max
}
```

## Testing Rules Locally

```bash
# Start emulator
firebase emulators:start --only firestore

# In another terminal, run tests
firebase emulators:exec --only firestore "npm test"
```

## Deploying Rules

```bash
# Deploy Firestore rules
firebase deploy --only firestore:rules --project <project-id>

# Deploy Storage rules
firebase deploy --only storage:rules --project <project-id>

# Deploy both
firebase deploy --only firestore:rules,storage:rules --project <project-id>
```
