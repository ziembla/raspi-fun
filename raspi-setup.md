
# Setting up a new Raspberry Pi #

## Installing NOOBS ##

Note: Raspbian's changelog is in `os/Raspbian/release_notes.txt` in the `NOOBS-*.zip`

### Cleaning flash card ###

**VERIFY THAT YOU KNOW WHAT YOU'RE DOING BEFORE RUNNING COMMANDS GIVEN BELOW. THESE CAN DESTROY YOUR SYSTEM, NOT ONLY THE CARD!**

After preparing the card put contents of the unzipped NOOBS archive on it.

#### Windows ####

Run `cmd.exe` as Administrator, then `diskpart`:

```
list disk
select disk XXX
clean
create partition primary
format fs=fat32 quick
assign
```

#### Linux #####

Identify the device for your card with:

```
sudo parted --list
```

Unmount any of the partitions if auto-mounted by OS on card insert event!

Check the end of the usable space and proceed with cleaning:

```
DEVICE=/dev/sdXXX

sudo parted ${DEVICE} unit B print free

CARD_END=XXX
CARD_LABEL=RASPI

sudo dd if=/dev/zero of=${DEVICE} bs=10M count=2
sudo parted ${DEVICE} mklabel msdos unit b mkpart pri fat32 1048576 ${CARD_END}  
sudo mkfs.vfat -F 32 -n ${CARD_LABEL} ${DEVICE}1
```

### Getting this doc ###

<https://github.com/ziembla/raspi-fun/blob/master/raspi-setup.md>

Clone the doc?

```
cd
git clone https://github.com/ziembla/raspi-fun.git
cd raspi-fun
git config --local user.name XXXXX
git config --local user.email XXXXX
```

If from bare repo on USB use something like:

```
git clone /media/pi/PASPI_GIT/git-repos/raspi-fun
```

Checking git settings

```
for option in '--system' '--global' '--local' '' ; do echo ========== $option ; git config -l $option ; done
```

## Basic configuration

### raspi-config etc.

* check monitor modes available
~~~
tvservice -d /tmp/edid-dump
edidparser /tmp/edid-dump
~~~

Find the best mode, for FullHD there should be "DMT mode (82) 1920x1080p" listed

* reboot, go to NOOBS console
* "Edit config"
    * remove/comment any "overscan_" lines
    * set `hdmi_group=2` and `hdmi_mode=82` (as checked above, group 2 is for DMT)
    * "Exit" to reboot
* in terminal

~~~
sudo raspi-config
~~~

    * "Change user password"
    * "Boot options"/"Console"
    * "Internationalisation Options"
        * "Change locale"
            * clean existing "en_GB.UTF-8" or "en_US..." using **Space**
            * check "pl_PL.UTF-8"
        * "Change timezone"/"Europe"/"Warsaw"
        * "Change keyboard layout"/"104-key"/"Polish"/"default"/"no compose"/"yes"
    * "Advanced options"
        * "Hostname" (raspberrypi->XXXXX)
        * "Memory Split" 256
        * (leave SSH access enabled?!)
        * "Audio"/"Force 3.5mm jack"
        * "GL Driver"/"???" ("Disabled" by default and good for minecraft, "Enabled" needed for colobot)
    * "Finish" (**Tab** to exit menu)
    * reboot
* in terminal
~~~
sudo dpkg-reconfigure console-setup
~~~
    * "UTF-8"/"Latin2"/"Terminus" (or "Fixed")/"8x16" (or "8x14")

### some global setup

```
read -d '' SETTINGS << EOF

EDITOR="vi -e"
VISUAL=vi

HISTCONTROL=ignoreboth:erasedups
shopt -s histappend
shopt -s histverify
HISTSIZE=5000
HISTFILESIZE=8000
 #PROMPT_COMMAND="history -a; history -c; history -r"
PROMPT_COMMAND="history -w"

alias ll="ls -l"
alias mc=". /usr/lib/mc/mc-wrapper.sh"

EOF
FILES="/home/`id -un`/.bashrc /root/.bashrc /etc/skel/.bashrc"

echo "$SETTINGS" | sudo tee -a $FILES > /dev/null
```

Note, that `echo $SETTINGS` would glued all lines into one, quotations needed to keep the original form!

### nonstandard user setup

Create a new user, assign to the `pi`'s groups an disable `pi`

Verify, that the `pi` user has `!` in front of the password hash to unable logging in  

    * unlock later with `usermod -U pi` when needed
    * note, that `su pi` from `root`'s terminal is still possible (no password needed!)

Note, that you need `sudo` without password prompt for your user, as some default applications assume that (running Scratch from a menu can hang your X-window session with the invisible sudo password prompt... learnt the hard way)

~~~

NEW_USER=XXXXX

sudo adduser ${NEW_USER} --gecos ''

sudo usermod -aG `groups pi | awk '{ s = substr($0,2*length("pi")+5); gsub(/ /,",",s); print s}'` ${NEW_USER}

grep pi /etc/shadow
sudo usermod -L pi
grep pi /etc/shadow

sudo visudo
~~~

add line based of the `pi` user (or just add your username after comma `pi,XXXXX`)

~~~
XXXXX ALL=(ALL) NOPASSWD: ALL
~~~



* to change font in terminal window (LXTerminal) just use "Edycja"/"Preferencje" to change "Monospace 10"->"DejaVu Sans Mono 9"





## Updating

```
sudo apt-get update
sudo apt-get dist-upgrade
```

`sudo rpi-update` not needed...?


Checking free space available might be useful before

```
df -h
du -sh /var/cache/apt/archives
du -hd1 /tmp
```

Downloaded packages can be deleted from `/var/cache/apt/archives` with `sudo apt-get clean`.

Unneeded orphaned packages can be deleted with `sudo apt-get autoremove`.

## Installing additional software ##

### Checking software versions

package         | command
---             | ---
linux distro    |lsb_release -a
linux kernel    |uname -a
raspi firmware  |vcgencmd version
raspi board     |cat /sys/firmware/devicetree/base/model
mathematica     |wolfram -run 'Print[$Version]; Quit[]'
g++             |g++ --version
python          |python -c "import sys; print sys.version #sys.version_info"

(raspi firmware versions look cryptic but they're just git commit ids, see <https://github.com/raspberrypi/firmware/commits/master>

NOT TRUE !!! NOT TRUE !!! NOT TRUE !!! NOT TRUE !!! NOT TRUE !!! NOT TRUE !!! 

### Installing

```
PACKAGES=
PACKAGES="$PACKAGES htop tree"
PACKAGES="$PACKAGES git-cola gitk"
PACKAGES="$PACKAGES kdiff3"
PACKAGES="$PACKAGES retext markdown"
PACKAGES="$PACKAGES dolphin"
PACKAGES="$PACKAGES kate"
PACKAGES="$PACKAGES pinta"
PACKAGES="$PACKAGES anki"
PACKAGES="$PACKAGES graphviz"
PACKAGES="$PACKAGES imagemagick"
PACKAGES="$PACKAGES tidy"
PACKAGES="$PACKAGES mc screen lsof"
PACKAGES="$PACKAGES freeplane"

 #PACKAGES="$PACKAGES emacs24 org-mode emacs-goodies-el"
 #PACKAGES="$PACKAGES openjdk-8-jdk"
 #PACKAGES="$PACKAGES vlc"
 #PACKAGES="$PACKAGES meld"

PACKAGES=
sudo apt-get install $PACKAGES

```

### (ubuntu-only packages, not for raspi) ###

```
PACKAGES="$PACKAGES indicator-multiload"
PACKAGES="$PACKAGES meld"

```

### Searching for packages ###

Non-installed

```
apt-cache search --names-only emacs
apt-cache search --names-only openjdk
apt-cache show emacs24


```

Installed
```
dpkg -l
dpkg -l '*-dev'
```

---


### other settings

monospace font: Droid Sans Mono (ew. DejaVu Sans Mono), size 9


* geany
    - set monospaced font for output
* retext
    - set `Roboto 10` as default rendering font
    - `printf '\n[General]\neditorFont=Droid Sans Mono\neditorFontSize=9\n' >> ~/.config/ReText\ project/ReText.conf`
    - use `^l` for live preview

### wifi

disable history, use PSK to avoid keeping plaintext password in config (is it really such a great idea?!)
~~~
unset HISTFILE
wpa_passphrase SSID PASSWORD
vi /etc/wpa_supplicant/wpa_supplicant.conf
~~~

copy output, skipping password, add `scan_ssid=1` if the network is hidden

### wifi TL-WN725N

<http://botland.com.pl/content/70-konfiguracja-wifi>
<https://github.com/lwfinger/rtl8188eu/>

```
sudo wget https://github.com/lwfinger/rtl8188eu/raw/c83976d1dfb4793893158461430261562b3a5bf0/rtl8188eufw.bin -O /lib/firmware/rtlwifi/rtl8188eufw.bin
```
or
```
sudo install -p -m 644 8188eu.ko /lib/modules/`uname -r`/kernel/drivers/net/wireless 
sudo depmod -a
sudo modprobe 8188eu
```

`TL-WN725N/install.sh`

### packages

```
sudo apt-get update
sudo apt-get upgrade
sudo apt-get install \
    kate \
    retext \
    geany \
    vlc \
    okular \
    iceweasel \
    git-cola gitk \
    python-nltk \
    python-reportlab \
    colobot \
 
```

* scala
```
sudo su -

v=2.11.8
cd /tmp
wget http://downloads.lightbend.com/scala/$v/scala-$v.tgz
cd /opt
tar zxvf /tmp/scala-$v.tgz
mv scala-$v scala
printf 'export PATH=$PATH:/opt/scala/bin\n' > /etc/profile.d/scala.sh
```

* maven
```
sudo su -

v=3.3.9
cd /tmp
wget ftp://ftp.task.gda.pl/pub/www/apache/dist/maven/maven-3/$v/binaries/apache-maven-$v-bin.tar.gz
cd /opt
tar zxvf /tmp/apache-maven-$v-bin.tar.gz
mv apache-maven-$v apache-maven
printf 'export M2_HOME=/opt/apache-maven\nexport PATH=$PATH:$M2_HOME/bin\n' > /etc/profile.d/maven.sh
```


Warnings
- **colobot** is a superb programming game "for children", still at least the linux '0.1.3-alpha' version tends to hang my raspberry 2 (NOOBS+Raspbian 1.9.0). I have no idea whether it is the game's or experimental OpenGL's (see `raspi-config` above) fault...
- don't try to install "all" in `sudo python -c "import nltk; nltk.download()"` (too big)


## Scratch

<http://download.scratch.mit.edu/ScratchReferenceGuide14.pdf>


## Backup

colobot
```
cd
tar -czvf backup-colobot-$(date '+%Y%m%d-%H%M%S').tgz .config/colobot.ini .local/share/colobot/*
```

restore
```
cd
tar -xzvf backup-XXXXX.tgz
```



## Operations

### switch user (`-l`!)
~~~
su -          # same as 'su -l root'
su - user     # same as 'su -l user'
~~~

other admin stuff
```
lsmod
lsusb

visudo     # edit /etc/sudoers
vipw [-s]  # edit /etc/passwd (/etc/shadow)
vigr [-s]  # edit /etc/group (/etc/gshadow)

usermod -L pi
usermod -U pi
```


### screenshots
```
scrot -cd 5 -a PLIK.png
scrot -s
```

`-d` delay (`-c` countwdown)  
`-u` active window  
`-s` selected area

### ssh
listing server public keys
~~~
for file in /etc/ssh/*_key.pub do ; echo $file ; ssh-keygen -lf $file ; echo ; done
~~~
connecting to server
~~~
ssh USER@HOST
~~~

### packages

* list files coming with PACKAGE
```
dpkg-query -L PACKAGE
```
* find package that brought FILE (Note: for `java` there is a sequence of links with /etc/alternalives etc.)
```
dpkg-query -S FILE
dpkg-query -S $(readlink -e $(which java))
```

### finding

files under home, matching pattern, changed last 24h
```
find ~ -type f -regex '.*pattern.*' -mtime -1 -ls
```

### monitoring
~~~
dmesg -H
htop

free -oh

pgrep PROCESS_NAME
pgrep -l PROCESS_NAME

~~~

~~~
ifconfig
ifconfig wlan0 
ifconfig wlan0 down
ifdown wlan0
ifup wlan0
~~~

### other
```
wget -O XXXXX https://xxxxx
hexdump -Cn 512 XXXXX
```

- after X-window hang: keep `<Alt>+<PrtScr>` pressed and type (slowly, wait for any response after each key): `reisub`



(just a test)