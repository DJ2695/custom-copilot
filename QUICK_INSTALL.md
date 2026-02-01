# Quick Installation Reference

## TL;DR - Installation Commands

### Public Repository
```bash
pip install git+https://github.com/DJ2695/custom-copilot.git
```

### Private Repository - SSH
```bash
pip install git+ssh://git@github.com/DJ2695/custom-copilot.git
```

### Private Repository - Personal Access Token
```bash
# Option 1: Direct (less secure, token visible in history)
pip install git+https://YOUR_TOKEN@github.com/DJ2695/custom-copilot.git

# Option 2: Environment variable (recommended)
export GITHUB_TOKEN=your_token_here
pip install git+https://${GITHUB_TOKEN}@github.com/DJ2695/custom-copilot.git
```

### Local Development
```bash
git clone https://github.com/DJ2695/custom-copilot.git
cd custom-copilot
pip install -e .
```

## Verify Installation
```bash
cc help
```

## Making the Repository Public

To make this repository public while restricting contributions:

1. **On GitHub:**
   - Go to Repository Settings
   - Scroll to "Danger Zone"
   - Click "Change visibility"
   - Select "Make public"
   - Confirm the action

2. **Contribution Restrictions Already in Place:**
   - ✅ CONTRIBUTING.md restricts external contributions
   - ✅ Pull request template warns contributors
   - ✅ Issue templates disabled for external users
   - ✅ README clearly states contribution policy

3. **GitHub Repository Settings (Optional but Recommended):**
   - Settings → General → Features:
     - ✅ Keep Wikis disabled
     - ✅ Keep Projects disabled  
     - ✅ Keep Discussions disabled (unless you want them)
   
   - Settings → Branches:
     - Add branch protection rules for `main`:
       - ✅ Require pull request reviews before merging
       - ✅ Require status checks to pass
       - ✅ Include administrators (so only you can push)
   
   - Settings → Moderation:
     - Set interaction limits if needed

4. **After Making Public:**
   Users can install with:
   ```bash
   pip install git+https://github.com/DJ2695/custom-copilot.git
   ```

## License

The MIT License allows others to:
- ✅ Use the software commercially
- ✅ Modify the software
- ✅ Distribute the software
- ✅ Use the software privately
- ✅ Fork and create their own versions

But they must:
- Include the original license and copyright notice
- Not hold you liable

This means users can fork and modify the code for their own needs, but cannot contribute back to your repository due to the contribution policy.
