# .zshrc
# From : https://github.com/NicolasCARPi/.dotfiles

# History
HISTFILE=~/.histfile
HISTSIZE=100000
SAVEHIST=100000

# autocompletion
autoload -Uz compinit && compinit
# load colors
[[ -r ${HOME}/.zsh/colors.zsh ]] && source ${HOME}/.zsh/colors.zsh
# For autocompletion with an arrow-key driven interface
zstyle ':completion:*' menu select
# import new commands from the history file also in other zsh-session
setopt SHARE_HISTORY
# save each command's beginning timestamp and the duration to the history file
setopt EXTENDED_HISTORY
# If a new command line being added to the history list duplicates an older
# one, the older command is removed from the list
setopt HIST_IGNORE_ALL_DUPS
# remove command lines from the history list when the first character on the
# line is a space
setopt HIST_IGNORE_SPACE
# remove blanks
setopt HIST_REDUCE_BLANKS
# suggest correction
setopt CORRECT
# * shouldn't match dotfiles. ever.
setopt noglobdots

# edit command line in $EDITOR with ^f
autoload -U edit-command-line
zle -N edit-command-line
bindkey '^f' edit-command-line

# vim <3... but later
export EDITOR="nano"

## PROMPT appearance
#┌─[user@machine:~]-[16:26:07]
#└─>
if [ $UID -eq 0 ];then
    export PROMPT="%{$fg[red]%}┌─[%{$fg[green]%}%n%{$fg[cyan]%}@%{$fg[green]%}%m%{$fg[red]%}:%{$fg[yellow]%}%~%{$fg[red]%}]%{$fg[yellow]%}-%{$fg[red]%}[%{$fg[cyan]%}%*%{$fg[red]%}]%{$reset_color%}%{$reset_color%}"$'\n'"%{$fg[red]%}└─>%{$reset_color%} "
else
    export PROMPT="%{$fg[white]%}┌─[%{$fg[green]%}%n%{$fg[cyan]%}@%{$fg[green]%}%m%{$fg[white]%}:%{$fg[cyan]%}%~%{$fg[white]%}]%{$fg[yellow]%}-%{$fg[white]%}[%{$fg[cyan]%}%*%{$fg[white]%}]%{$reset_color%}%{$reset_color%}"$'\n'"%{$fg[white]%}└─>%{$reset_color%} "
fi

PATH=~/.bin:/srv/http/go/bin:~/.gem/ruby/2.4.0/bin:~/.gem/ruby/2.3.0/bin:$PATH
export PATH
export PATH=/usr/local/bin:/usr/local/sbin:$PATH
export PATH=/usr/local/share/python:$PATH

if [ -d "$HOME/bin" ] ; then
  PATH="$PATH:$HOME/bin"
fi


# to have nice colors in ls
export LS_OPTIONS='-G'
LSCOLORS='Exfxcxdxbxegedabagacad'
export LSCOLORS
CLICOLOR=1
export CLICOLOR
#zstyle ':completion:*' list-colors ${(s.:.)LS_COLORS}

# completion in the middle of a line
bindkey '^i' expand-or-complete-prefix

# pretty man pages
export LESS_TERMCAP_mb=$'\E[01;31m'
export LESS_TERMCAP_md=$'\E[01;31m'
export LESS_TERMCAP_me=$'\E[0m'
export LESS_TERMCAP_se=$'\E[0m'
export LESS_TERMCAP_so=$'\E[01;44;33m'
export LESS_TERMCAP_ue=$'\E[0m'
export LESS_TERMCAP_us=$'\E[01;32m'


source  /opt/intel/mkl/bin/mklvars.sh intel64

# autocomplete
# https://github.com/tarruda/zsh-autosuggestions
source ~/.zsh/zsh-autosuggestions.zsh



# change color of autocomplete
export ZSH_AUTOSUGGEST_HIGHLIGHT_STYLE='fg=7'

## ls after cd
function chpwd() {
    emulate -LR zsh
    ls -G
}

# extract command
function e () {
    if [ -f $1 ] ; then
        case $1 in
        *.tar.bz2) tar xvjf $1 ;;
        *.tar.gz) tar xvzf $1 ;;
        *.bz2) bunzip2 $1 ;;
        *.rar) unrar x $1 ;;
        *.gz) gunzip $1 ;;
        *.tar) tar xvf $1 ;;
        *.tbz2) tar xvjf $1 ;;
        *.tgz) tar xvzf $1 ;;
        *.zip) unzip $1 ;;
        *.Z) uncompress $1 ;;
        *.7z) 7z x $1 ;;
        *.tar.xz) tar xvJf $1 ;;
        *.xz) unlzma $1 ;;
        *) echo "wtf is that shit ?? '$1'...";;

        esac
    else
        echo "'$1' is not a fucking file !"
    fi
}

# local configuration
# if file is here and is readable, load it
[[ -r ${HOME}/.zshrc.local ]] && source ${HOME}/.zshrc.local
[[ -r ${HOME}/.zsh_alias ]] && source ${HOME}/.zsh_alias
