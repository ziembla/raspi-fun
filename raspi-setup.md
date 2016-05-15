
# Setting up a new Raspberry Pi #

## Installing NOOBS

Note: Raspbian's changelog is in `os/Raspbian/release_notes.txt` in the `NOOBS-*.zip`

### cleaning flash card

**VERIFY THAT YOU KNOW WHAT YOU'RE DOING BEFORE RUNNING COMMANDS GIVEN BELOW. THESE CAN DESTROY YOUR SYSTEM, NOT ONLY THE CARD!**

In Windows, run `cmd.exe` as Administrator, then `diskpart`:

```
list disk
select disk XXX
clean
create partition primary
format fs=fat32 quick
assign
```

Put contents of the unzipped NOOBS archive on the card.

### view this doc

<https://github.com/ziembla/raspi-fun/blob/master/raspi-setup.md>

or clone it
```
cd
git clone https://github.com/ziembla/raspi-fun.git
cd raspi-fun
git config --local user.name XXXXX
git config --local user.email XXXXX
```

checking git settings
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
        * "Change keyboard layout"/"104-key"/"Polish"/"default"/"no compose"/"no"
    * "Advanced options"
        * "Hostname" (raspberrypi->XXXXX)
        * "Memory Split" 256
        * (leave SSH access enabled?!)
        * "Audio"/"Force 3.5mm jack"
        * "GL Driver"/"Enable" (required by colobot only?!)
    * "Finish" (**Tab** to exit menu)
    * reboot
* in terminal
~~~
sudo dpkg-reconfigure console-setup
~~~
    * "UTF-8"/"Latin2"/"Terminus" (or "Fixed")/"8x16" (or "8x14")

### nonstandard user setup

* in terminal
~~~
sudo su -
adduser XXXXX --gecos ''
usermod -G `groups pi | awk '{ s = substr($0,2*length("pi")+5); gsub(/ /,",",s); print s}'` XXXXX
cat /etc/shadow | grep pi
usermod -L pi
cat grep pi /etc/shadow 
~~~
verify, that the `pi` user has `!` in front of the password hash to be locked from logging in  

    * unlock later with `usermod -U pi` when needed
    * remember, that `su pi` from `root`'s terminal is still possible (no password needed)
* append the following to `/etc/environment`
~~~
export EDITOR=vi
~~~
* append the following to `~/.bash_profile`
~~~
export HISTCONTROL=ignorespace:ignoredups:erasedups
shopt -s histappend
export PROMPT_COMMAND="${PROMPT_COMMAND:+$PROMPT_COMMAND;}history -a; history -c; history -r"
~~~
* append the following to `~/.bashrc` and `/root/.bashrc`
~~~
alias ll='ls -l'
~~~
* in terminal (optionally, for "NOPASSWD" sudo for new user)
~~~
sudo su -
visudo
~~~
add line based of the `pi` user
~~~
XXXXX ALL=(ALL) NOPASSWD: ALL
~~~

* to change font in terminal window (LXTerminal) just use "Edycja"/"Preferencje" to change "Monospace 10"->"DejaVu Sans Mono 9"

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
- **colobot** is a superb programming game, still at least the linux '0.1.3-alpha' version tends to hang my raspberry 2 (NOOBS+Raspbian 1.9.0). I have no idea whether it is the game's or experimental OpenGL's (see `raspi-config` above) fault...
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

### version checks

* linux kernel
~~~
uname -a
~~~
* g++
~~~
g++ --version
~~~
* mathematica
~~~
wolfram -run 'Print[$Version]; Quit[]'
~~~
* firmware
~~~
/opt/vc/bin/vcgencmd version
~~~

### screenshots
~~~
scrot -cd 5 -a PLIK.png
scrot -s
~~~
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
