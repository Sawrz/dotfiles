source /etc/profile

# TheFuck initialisation
eval "$(thefuck --alias)"

# Changing "ls" to "exa"
alias ls='exa --color=always --group-directories-first' # my preferred listing

# bare Git repository for dot files (see here https://www.atlassian.com/git/tutorials/dotfiles)
#alias config='/usr/bin/git --git-dir=/home/sandro/.cfg/ --work-tree=/home/sandro'

# Add local bin to PATH (e.g. for streamdeck-ui)
PATH=$PATH:$HOME/.local/bin

# Init SSH-Keys
if [ -n "$DESKTOP_SESSION" ];then
    eval $(gnome-keyring-daemon --start)
    export SSH_AUTH_SOCK
fi

# Edit chrontab
alias scron="su -c $(printf "%q " "crontab -e")"

# Use nvim instead of vim
alias vim="nvim"

# Add auto completion and keybindings
#source /usr/share/fzf/completion.bash
#source /usr/share/fzf/key-bindings.bash
