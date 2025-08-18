# Git & GitHub Essentials - Daily Commands

## Git Configuration
```bash
# Initial setup
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
git config --list                     # View current configuration
git config --global init.defaultBranch main  # Set default branch to main
```

## Repository Management
```bash
# Initialize and clone
git init                              # Initialize new repository
git clone <repository_url>            # Clone remote repository
git clone <url> <directory_name>      # Clone to specific directory
git remote -v                         # View remote repositories
git remote add origin <url>           # Add remote repository
git remote set-url origin <new_url>   # Change remote URL
```

## Basic Workflow
```bash
# Check status and changes
git status                            # Show working directory status
git diff                              # Show unstaged changes
git diff --staged                     # Show staged changes
git diff HEAD~1                       # Compare with previous commit

# Stage and commit
git add <file>                        # Stage specific file
git add .                             # Stage all changes
git add -A                            # Stage all changes including deletions
git commit -m "commit message"        # Commit staged changes
git commit -am "message"              # Stage and commit modified files
```

## Branch Management
```bash
# Working with branches
git branch                            # List local branches
git branch -a                         # List all branches (local and remote)
git branch <branch_name>              # Create new branch
git checkout <branch_name>            # Switch to branch
git checkout -b <branch_name>         # Create and switch to new branch
git switch <branch_name>              # Modern way to switch branches
git switch -c <branch_name>           # Create and switch (modern syntax)

# Branch operations
git merge <branch_name>               # Merge branch into current branch
git branch -d <branch_name>           # Delete local branch
git branch -D <branch_name>           # Force delete local branch
git push origin --delete <branch>     # Delete remote branch
```

## Remote Operations
```bash
# Synchronizing with remote
git fetch                             # Download changes from remote
git pull                              # Fetch and merge changes
git pull origin <branch>              # Pull specific branch
git push                              # Push commits to remote
git push origin <branch>              # Push specific branch
git push -u origin <branch>           # Push and set upstream
git push --force-with-lease           # Safer force push
```

## Viewing History
```bash
# Log and history
git log                               # View commit history
git log --oneline                     # Compact log view
git log --graph                       # Visual branch representation
git log --author="name"               # Filter by author
git log --since="2 weeks ago"         # Filter by date
git show <commit_hash>                # Show specific commit details
git reflog                            # Show reference log
```

## Undoing Changes
```bash
# Unstage and reset
git reset <file>                      # Unstage file
git reset --soft HEAD~1               # Undo last commit, keep changes staged
git reset --hard HEAD~1               # Undo last commit, discard changes
git checkout -- <file>                # Discard changes to file
git restore <file>                    # Modern way to discard changes
git restore --staged <file>           # Unstage file (modern syntax)
```

## Stashing
```bash
# Temporary storage
git stash                             # Stash current changes
git stash push -m "message"           # Stash with message
git stash list                        # List all stashes
git stash pop                         # Apply and remove most recent stash
git stash apply stash@{0}             # Apply specific stash
git stash drop stash@{0}              # Delete specific stash
git stash clear                       # Delete all stashes
```

## GitHub-Specific Operations
```bash
# GitHub CLI (gh) commands
gh auth login                         # Authenticate with GitHub
gh repo create <name>                 # Create new repository
gh repo clone <user>/<repo>           # Clone repository
gh pr create                          # Create pull request
gh pr list                            # List pull requests
gh pr checkout <number>               # Checkout PR locally
gh issue create                       # Create new issue
gh issue list                         # List issues
```

## Working with Forks
```bash
# Fork workflow
gh repo fork <user>/<repo>            # Fork repository
git remote add upstream <original_repo_url>  # Add upstream remote
git fetch upstream                    # Fetch upstream changes
git checkout main
git merge upstream/main               # Sync with upstream
```

## Tags and Releases
```bash
# Tagging
git tag                               # List tags
git tag <tag_name>                    # Create lightweight tag
git tag -a <tag_name> -m "message"    # Create annotated tag
git push origin <tag_name>            # Push specific tag
git push origin --tags               # Push all tags
git tag -d <tag_name>                # Delete local tag
git push origin --delete <tag_name>  # Delete remote tag
```

## File Operations
```bash
# File management
git mv <old_name> <new_name>          # Rename file
git rm <file>                         # Remove file from Git
git rm --cached <file>                # Remove from Git but keep locally
git clean -f                          # Remove untracked files
git clean -fd                         # Remove untracked files and directories
```

## .gitignore Management
```bash
# Common .gitignore patterns
echo "node_modules/" >> .gitignore    # Ignore Node.js dependencies
echo "*.log" >> .gitignore            # Ignore log files
echo ".env" >> .gitignore             # Ignore environment files
echo "dist/" >> .gitignore            # Ignore build directories

# Apply .gitignore to already tracked files
git rm -r --cached .
git add .
git commit -m "Apply .gitignore"
```

## Collaboration Workflow
```bash
# Typical GitHub workflow
git checkout main                     # Switch to main branch
git pull origin main                  # Get latest changes
git checkout -b feature/new-feature   # Create feature branch
# ... make changes ...
git add .
git commit -m "Add new feature"
git push origin feature/new-feature   # Push feature branch
# Create PR on GitHub
# After PR merge:
git checkout main
git pull origin main
git branch -d feature/new-feature     # Clean up local branch
```

## Useful Git Aliases
Add these to your `~/.gitconfig`:
```bash
[alias]
    st = status
    co = checkout
    br = branch
    ci = commit
    unstage = reset HEAD --
    last = log -1 HEAD
    visual = !gitk
    lg = log --oneline --graph --decorate --all
```