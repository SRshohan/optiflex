# VPS Management

## User Management

### Switch from root to user1
```bash
su - user1
```

## Tmux Management

### Check list of tmux sessions
```bash
tmux list-sessions
# or shorter version
tmux ls
```

### Attach to existing tmux session
```bash
tmux attach-session -t session_name
# or shorter version
tmux a -t session_name
```

### Create new tmux session
```bash
tmux new-session -s session_name
# or shorter version
tmux new -s session_name
```

### Switch between tmux sessions
```bash
# List sessions and select one
tmux choose-session

# Switch to next session
Ctrl+b n

# Switch to previous session  
Ctrl+b p

# Switch to specific session by number
Ctrl+b s
```

### Basic tmux shortcuts
- `Ctrl+b d` - Detach from session
- `Ctrl+b c` - Create new window
- `Ctrl+b n` - Next window
- `Ctrl+b p` - Previous window
- `Ctrl+b %` - Split pane vertically
- `Ctrl+b "` - Split pane horizontally
