
# Setting up a new Raspberry Pi #

## Installing NOOBS

Raspbian's changelog is in `os/Raspbian/release_notes.txt` in the `NOOBS-*.zip`

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

### get this doc

```
cd
git clone https://github.com/ziembla/raspi-fun.git
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
            * clean existing "en_GB..." or "en_US..." using **Space**
            * check "pl_PL.UTF-8"
        * "Change timezone"/"Europe"/"Warsaw"
        * "Change keyboard layout"/"104-key"/"Polish"/"default"/"no compose"/"no"
    * "Advanced options"
        * "Hostname" (raspberrypi->*raspi-tata*)
        * "Memory Split" 256
        * (leave SSH access enabled????)
        * "Audio"/"Force 3.5mm jack"
    * "Finish" (**Tab** to exit menu)
    * reboot
* in terminal
~~~
sudo dpkg-reconfigure console-setup
~~~
    * "UTF-8"/"Latin2"/"Terminus" (or "Fixed")/"8x16" (or "8x14")
* to change font in terminal window (LXTerminal) just use "Edycja"/"Preferencje" to change "Monospace 10"->"DejaVu Sans Mono 9"

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
(unlock with `usermod -U pi` when needed) 


* append the following to `.bashrc` files in both `/home/XXXXX` and `/root` directories 
~~~
alias ll='ls -l'
export EDITOR=vi
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

### nonstandard user setup

### wifi

* disable history...
~~~
export HISTFILE=
wpa_passphrase SSID PASSWORD
vi /etc/wpa_supplicant/wpa_supplicant.conf
~~~

### packages



## Operations

### switch user (`-l`!)
~~~
su -          # same as 'su -l root'
su - user     # same as 'su -l user'
~~~


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





### monitoring
~~~
dmesg -H
htop
~~~




~~~
visudo     # edit /etc/sudoers
vipw [-s]  # edit /etc/passwd (/etc/shadow)
vigr [-s]  # edit /etc/group (/etc/gshadow)

usermod -L pi
usermod -U pi

ifconfig
ifconfig wlan0 down
ifconfig wlan0 up
~~~
