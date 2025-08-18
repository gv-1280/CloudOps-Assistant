# Git & GitHub Troubleshooting Guide

## Quick Debugging Commands
```bash
git status                            # Check current repository state
git log --oneline -10                 # Recent commits
git reflog                            # Complete reference log
git remote -v                         # Check remote URLs
git config --list                     # View Git configuration
git diff HEAD~1                       # Compare with previous commit
```

## Common Git Issues

### 1. Authentication Problems
**Symptoms:** "Permission denied", "Authentication failed"

```bash
# Check current authentication
gh auth status
git config --list | grep user

# Re-authenticate
gh auth login                         # GitHub CLI authentication
git config --global credential.helper store  # Store credentials

# SSH key issues
ssh -T git@github.com                 # Test SSH connection
ssh-keygen -t ed25519 -C "your_email@example.com"  # Generate new SSH key
cat ~/.ssh/id_ed25519.pub             # Copy public key to GitHub
```

**Fix HTTPS → SSH:**
```bash
git remote set-url origin git@github.com:username/repo.git
```

### 2. Merge Conflicts
**Symptoms:** "Automatic merge failed; fix conflicts"

```bash
# Check conflict status
git status                            # Shows conflicted files
git diff                              # Shows conflict markers

# Resolve conflicts
# 1. Edit files to resolve <<<< ==== >>>> markers
# 2. Stage resolved files
git add <resolved_file>
git commit                            # Complete the merge

# Abort merge if needed
git merge --abort                     # Cancel ongoing merge
```

### 3. Detached HEAD State
**Symptoms:** "You are in 'detached HEAD' state"

```bash
# Check current state
git status
git log --oneline -5

# Fix: Create branch from current state
git checkout -b recovery-branch       # Create branch from current commit
git checkout main                     # Return to main branch
git merge recovery-branch             # Merge your changes if needed

# Or discard changes and return
git checkout main                     # Just go back to main
```

### 4. "Your branch is ahead/behind origin"
```bash
# Branch is ahead (you have local commits)
git push origin <branch>              # Push your commits

# Branch is behind (remote has new commits)
git pull origin <branch>              # Pull remote changes

# Branches have diverged
git pull --rebase origin <branch>     # Rebase your commits on top
# OR
git fetch origin
git merge origin/<branch>             # Merge remote changes
```

## Commit and History Issues

### 1. Fix Last Commit Message
```bash
git commit --amend -m "corrected message"     # Change last commit message
git commit --amend --no-edit                  # Add files to last commit
```

### 2. Undo Commits
```bash
# Undo last commit, keep changes
git reset --soft HEAD~1

# Undo last commit, discard changes
git reset --hard HEAD~1

# Undo specific commit (creates new commit)
git revert <commit_hash>

# Reset to specific commit
git reset --hard <commit_hash>
```

### 3. Lost Commits
```bash
# Find lost commits
git reflog                            # Shows all recent HEAD changes
git log --oneline --all --graph       # Visual history

# Recover lost commit
git checkout <commit_hash>            # Go to lost commit
git checkout -b recovery-branch       # Create branch to save it
```

## Branch Issues

### 1. Can't Switch Branches
**Error:** "Your local changes would be overwritten"

```bash
# Option 1: Stash changes
git stash                             # Save changes temporarily
git checkout <branch>                 # Switch branch
git stash pop                         # Restore changes

# Option 2: Commit changes
git add .
git commit -m "WIP: temporary commit"
git checkout <branch>

# Option 3: Force switch (lose changes)
git checkout -f <branch>              # DANGER: Discards changes
```

### 2. Remote Branch Tracking Issues
```bash
# Set upstream for current branch
git push -u origin <branch_name>

# Track existing remote branch
git checkout -b <local_branch> origin/<remote_branch>

# Fix broken tracking
git branch --set-upstream-to=origin/<branch> <local_branch>
```

## GitHub-Specific Issues

### 1. Large File Problems
**Error:** "File too large" or slow pushes

```bash
# Check repository size
git count-objects -vH

# Find large files
find . -size +50M -type f

# Use Git LFS for large files
git lfs install
git lfs track "*.zip"
git add .gitattributes
git add large_file.zip
git commit -m "Add large file with LFS"
```

### 2. Push Rejected
**Error:** "Updates were rejected because the tip of your current branch is behind"

```bash
# Safe approach
git fetch origin
git rebase origin/main               # Rebase your commits
git push origin <branch>

# Alternative: merge approach
git pull origin main                 # Pull and merge
git push origin <branch>

# Force push (DANGER - only on feature branches)
git push --force-with-lease origin <branch>
```

### 3. GitHub Actions Failures
```bash
# Check workflow status
gh run list                          # List recent workflow runs
gh run view <run_id>                 # View specific run details
gh run logs <run_id>                 # Download run logs

# Re-run failed workflows
gh run rerun <run_id>                # Re-run specific workflow
```

## Repository Issues

### 1. Repository Too Large
```bash
# Check repository size
git count-objects -vH
du -sh .git

# Clean up history
git filter-branch --tree-filter 'rm -rf <large_directory>' HEAD  # Remove directory from history
git gc --prune=now --aggressive      # Garbage collect

# Alternative: BFG Repo-Cleaner (recommended)
# Download BFG and run:
java -jar bfg.jar --delete-files "*.zip" .
git reflog expire --expire=now --all && git gc --prune=now --aggressive
```

### 2. Accidentally Committed Secrets
```bash
# Remove from last commit
git rm --cached <sensitive_file>
git commit --amend -m "Remove sensitive file"
git push --force-with-lease

# Remove from history (use BFG)
java -jar bfg.jar --replace-text passwords.txt .
git reflog expire --expire=now --all && git gc --prune=now --aggressive
git push --force
```

### 3. Corrupted Repository
```bash
# Check repository integrity
git fsck --full

# Recover from backup
git clone <remote_url> <new_directory>  # Fresh clone
# Copy your uncommitted work manually

# Repair corrupted objects
git gc --prune=now
git repack -Ad
```

## Network and Connectivity Issues

### 1. Slow Git Operations
```bash
# Use shallow clone
git clone --depth 1 <repository_url>  # Clone only latest commit

# Configure Git for better performance
git config --global core.preloadindex true
git config --global core.fscache true
git config --global gc.auto 256

# Use different protocol
git remote set-url origin git@github.com:user/repo.git  # Switch to SSH
```

### 2. Proxy Issues
```bash
# Configure Git for corporate proxy
git config --global http.proxy http://proxy.company.com:8080
git config --global https.proxy https://proxy.company.com:8080

# Remove proxy settings
git config --global --unset http.proxy
git config --global --unset https.proxy
```

## Collaboration Issues

### 1. Merge Conflicts in Pull Requests
```bash
# Sync with upstream
git fetch upstream
git checkout main
git merge upstream/main
git push origin main

# Update feature branch
git checkout feature-branch
git rebase main                       # Rebase on updated main
# Resolve conflicts if any
git add .
git rebase --continue
git push --force-with-lease origin feature-branch
```

### 2. Synchronizing Forks
```bash
# Add upstream remote (original repository)
git remote add upstream <original_repo_url>
git fetch upstream

# Update main branch
git checkout main
git merge upstream/main
git push origin main

# Update feature branch
git checkout feature-branch
git rebase upstream/main
```

## File and Directory Issues

### 1. Case Sensitivity Problems
```bash
# Fix case sensitivity issues
git config core.ignorecase false     # Make Git case-sensitive
git mv <Filename> <temp_name>
git mv <temp_name> <filename>         # Fix case through temp rename
```

### 2. Line Ending Issues
```bash
# Configure line endings
git config --global core.autocrlf true    # Windows
git config --global core.autocrlf input   # macOS/Linux

# Fix existing repository
git rm --cached -r .
git reset --hard
```

## Emergency Recovery
```bash
# Nuclear option: start fresh but keep work
cp -r <project_directory> <backup_directory>  # Backup your work
rm -rf .git                           # Remove Git history
git init                              # Start fresh
git remote add origin <remote_url>
git add .
git commit -m "Fresh start"
git push -u origin main
```

## Debugging Workflow
1. **Check status**: `git status`
2. **Review recent activity**: `git reflog`
3. **Check remote connectivity**: `git remote -v` and `git fetch`
4. **Examine specific issues**: Use targeted commands based on error
5. **Test with clean clone**: If all else fails, clone fresh and copy work

## Useful Git Troubleshooting Flags
```bash
--verbose                             # More detailed output
--dry-run                            # Show what would happen
--force-with-lease                   # Safer force operations
--no-verify                          # Skip pre-commit hooks
--allow-empty                        # Allow empty commits
```