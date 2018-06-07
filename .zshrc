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
  PYTHONPATH="$PYTHONPATH:$HOME/bin"
fi


# to have nice colors in ls
 LS_COLORS='no=00:fi=00:di=34:ow=34;40:ln=35:pi=30;44:so=35;44:do=35;44:bd=33;44:cd=37;44:or=05;37;41:mi=05;37;41:ex=01;31:*.cmd=01;31:*.exe=01;31:*.com=01;31:*.bat=01;31:*.reg=01;31:*.app=01;31:*.txt=32:*.org=32:*.md=32:*.mkd=32:*.h=32:*.c=32:*.C=32:*.cc=32:*.cpp=32:*.cxx=32:*.objc=32:*.sh=32:*.csh=32:*.zsh=32:*.el=32:*.vim=32:*.java=32:*.pl=32:*.pm=32:*.py=32:*.rb=32:*.hs=32:*.php=32:*.htm=32:*.html=32:*.shtml=32:*.erb=32:*.haml=32:*.xml=32:*.rdf=32:*.css=32:*.sass=32:*.scss=32:*.less=32:*.js=32:*.coffee=32:*.man=32:*.0=32:*.1=32:*.2=32:*.3=32:*.4=32:*.5=32:*.6=32:*.7=32:*.8=32:*.9=32:*.l=32:*.n=32:*.p=32:*.pod=32:*.tex=32:*.go=32:*.bmp=33:*.cgm=33:*.dl=33:*.dvi=33:*.emf=33:*.eps=33:*.gif=33:*.jpeg=33:*.jpg=33:*.JPG=33:*.mng=33:*.pbm=33:*.pcx=33:*.pdf=33:*.pgm=33:*.png=33:*.PNG=33:*.ppm=33:*.pps=33:*.ppsx=33:*.ps=33:*.svg=33:*.svgz=33:*.tga=33:*.tif=33:*.tiff=33:*.xbm=33:*.xcf=33:*.xpm=33:*.xwd=33:*.xwd=33:*.yuv=33:*.aac=33:*.au=33:*.flac=33:*.m4a=33:*.mid=33:*.midi=33:*.mka=33:*.mp3=33:*.mpa=33:*.mpeg=33:*.mpg=33:*.ogg=33:*.ra=33:*.wav=33:*.anx=33:*.asf=33:*.avi=33:*.axv=33:*.flc=33:*.fli=33:*.flv=33:*.gl=33:*.m2v=33:*.m4v=33:*.mkv=33:*.mov=33:*.MOV=33:*.mp4=33:*.mp4v=33:*.mpeg=33:*.mpg=33:*.nuv=33:*.ogm=33:*.ogv=33:*.ogx=33:*.qt=33:*.rm=33:*.rmvb=33:*.swf=33:*.vob=33:*.webm=33:*.wmv=33:*.doc=31:*.docx=31:*.rtf=31:*.dot=31:*.dotx=31:*.xls=31:*.xlsx=31:*.ppt=31:*.pptx=31:*.fla=31:*.psd=31:*.7z=1;35:*.apk=1;35:*.arj=1;35:*.bin=1;35:*.bz=1;35:*.bz2=1;35:*.cab=1;35:*.deb=1;35:*.dmg=1;35:*.gem=1;35:*.gz=1;35:*.iso=1;35:*.jar=1;35:*.msi=1;35:*.rar=1;35:*.rpm=1;35:*.tar=1;35:*.tbz=1;35:*.tbz2=1;35:*.tgz=1;35:*.tx=1;35:*.war=1;35:*.xpi=1;35:*.xz=1;35:*.z=1;35:*.Z=1;35:*.zip=1;35:*.ANSI-30-black=30:*.ANSI-01;30-brblack=01;30:*.ANSI-31-red=31:*.ANSI-01;31-brred=01;31:*.ANSI-32-green=32:*.ANSI-01;32-brgreen=01;32:*.ANSI-33-yellow=33:*.ANSI-01;33-bryellow=01;33:*.ANSI-34-blue=34:*.ANSI-01;34-brblue=01;34:*.ANSI-35-magenta=35:*.ANSI-01;35-brmagenta=01;35:*.ANSI-36-cyan=36:*.ANSI-01;36-brcyan=01;36:*.ANSI-37-white=37:*.ANSI-01;37-brwhite=01;37:*.log=01;32:*~=01;32:*#=01;32:*.bak=01;33:*.BAK=01;33:*.old=01;33:*.OLD=01;33:*.org_archive=01;33:*.off=01;33:*.OFF=01;33:*.dist=01;33:*.DIST=01;33:*.orig=01;33:*.ORIG=01;33:*.swp=01;33:*.swo=01;33:*,v=01;33:*.gpg=34:*.gpg=34:*.pgp=34:*.asc=34:*.3des=34:*.aes=34:*.enc=34:*.sqlite=34:'


export LS_COLORS


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
    ls --color=auto
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
