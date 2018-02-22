# Pi-Loc
## Auto Position Reporter Headless for Raspberry Pi

Basic requirements: python, gpsd, gpsd-clients, python-gps, python-pip, dnsutils, vim, supervisor, git

To install:
apt-get the above packages
configure gpsd (conf file in repo)
download code and put somewhere logical (/opt is usually a good choice)
configure supervisor (pi-loc.conf in repo)
update-rc.d supervisor defaults
Set it and forget it #ronco

## Configuring Logging
Pi-loc uses a s3 bucket for ease of log access.  To enable this logging you must have an AWS s3 bucket set up and the proper credentials need to be set within the code.

## Configuring Read-Only FS 
1. apt-get update / upgrade and reboot as needed
2. Remove unneeded packages: apt-get remove --purge wolfram-engine triggerhappy anacron logrotate dphys-swapfile xserver-common lightdm
3. Remove X11: insserv -r x11-common; apt-get autoremove --purge
4. Replace default log management with busybox: apt-get install busybox-syslogd; dpkg --purge rsyslog (This will put log into circular memory buffer, you will able to see log using
logread command)
5. Disable swap and filesystem check; set to readonly:
Edit /boot/cmdline.txt and add "fastboot noswap ro" to the end of the line
(e.g. dwc_otg.lpm_enable=0 console=serial0,115200 console=tty1 root=PARTUUID=7dedfa85-02 rootfstype=ext4 elevator=deadline fsck.repair=yes rootwait fastboot noswap ro)
6. Move stuff to the tmpfs filesystem:
rm -rf /var/lib/dhcp/ /var/run /var/spool /var/lock /etc/resolv.conf
ln -s /tmp /var/lib/dhcp
ln -s /tmp /var/run
ln -s /tmp /var/spool
ln -s /tmp /var/lock
touch /tmp/dhcpcd.resolv.conf; ln -s /tmp/dhcpcd.resolv.conf /etc/resolv.conf
7. Move lock / pid files to tmpfs:
Edit /etc/systemd/system/dhcpcd5 and change PIDFile=/var/run/dhcpcd.pid
8. Move random-seed:
rm /var/lib/systemd/random-seed
ln -s /tmp/random-seed /var/lib/systemd/random-seed
9. We need to create the target at boot-time so we use systemd in some trickery
Edit /lib/systemd/system/systemd-random-seed.service
Add this line in the [service] section: ExecStartPre=/bin/echo "" >/tmp/random-seed
10. Restart systemd:  systemctl daemon-reload
11. Make sure that your pi is using ntp (check with ntpq -p) and time zone is set (using raspi-config)
12. Edit /etc/cron.hourly/fake-hw-clock to properly handle RO FS:
if (command -v fake-hwclock >/dev/null 2>&1) ; then
mount -o remount,rw /
fake-hwclock save
mount -o remount,ro /
fi
13. Set ntp to put the drift file in tmpfs:
Edit /etc/ntp.conf
driftfile /var/tmp/ntp.drift
14. Remove unneeded startup scripts:
insserv -r bootlogs; insserv -r console-setup
15. Now we need to edit /etc/fstab to have the block devices marked as ro and create tmpfs mounts:
proc                  /proc           proc    defaults             0       0
PARTUUID=7dedfa85-01  /boot           vfat    defaults,ro          0       2
PARTUUID=7dedfa85-02  /               ext4    defaults,noatime,ro  0       1
tmpfs                 /tmp            tmpfs   nosuid,nodev         0       0
tmpfs                 /var/log        tmpfs   nosuid,nodev         0       0
tmpfs                 /var/tmp        tmpfs   nosuid,nodev         0       0
16. Edit supervisor config file (etc/supervisor/supervisor.conf):
logfile=/var/log/supervisord.log ; (main log file;default $CWD/supervisord.log)
childlogdir=/var/log/            ; ('AUTO' child log dir, default $TEMP)
17. Edit /usr/lib/systemd/system/systemd-hostnamed.service
PrivateTmp=no
18. Here goes nothing...time to reboot #crossfingers
19. Now check to make sure all is well:
run mount
/dev/mmcblk0p2 on / type ext4 (ro,noatime,data=ordered) <- note ro for /
/dev/mmcblk0p1 on /boot type vfat (ro,relatime,fmask=0022,dmask=0022,codepage=437,iocharset=ascii,shortname=mixed,errors=remount-ro) <- note ro for /boot
run service supervisor status to make sure supervisor is running
Check to make sure pi-loc is logging to /var/log

## Switching to/from Read-Only FS

To remount fs as read/write:
mount -o remount,rw /
To remount fs as read-only:
mount -o remount,ro /


## **DISCLAIMER OF LIABILITY NOTICE**:



> The United States Government shall not be liable or responsible for
> any maintenance, updating or for correction of any errors in the
> software. 
>
> THIS SOFTWARE IS PROVIDED "AS IS" WITHOUT ANY WARRANTY OF ANY KIND,
> EITHER EXPRESSED, IMPLIED, OR STATUTORY, INCLUDING, BUT NOT LIMITED
> TO, ANY WARRANTY THAT THE SOFTWARE WILL CONFORM TO SPECIFICATIONS, ANY
> IMPLIED WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR
> PURPOSE, OR FREEDOM FROM INFRINGEMENT, ANY WARRANTY THAT THE SOFTWARE
> WILL BE ERROR FREE, OR ANY WARRANTY THAT THE DOCUMENTATION, IF
> PROVIDED, WILL CONFORM TO THE SOFTWARE.  IN NO EVENT SHALL THE UNITED
> STATES GOVERNMENT OR ITS CONTRACTORS OR SUBCONTRACTORS BE LIABLE FOR
> ANY DAMAGES, INCLUDING, BUT NOT LIMITED TO, DIRECT, INDIRECT, SPECIAL
> OR CONSEQUENTIAL DAMAGES, ARISING OUT OF, RESULTING FROM, OR IN ANY
> WAY CONNECTED WITH THE SOFTWARE OR ANY OTHER PROVIDED DOCUMENTATION,
> WHETHER OR NOT BASED UPON WARRANTY, CONTRACT, TORT, OR OTHERWISE,
> WHETHER OR NOT INJURY WAS SUSTAINED BY PERSONS OR PROPERTY OR
> OTHERWISE, AND WHETHER OR NOT LOSS WAS SUSTAINED FROM, OR AROSE OUT OF
> THE RESULTS OF, OR USE OF, THE NICS SOFTWARE OR ANY PROVIDED
> DOCUMENTATION. THE UNITED STATES GOVERNMENT DISCLAIMS ALL WARRANTIES
> AND LIABILITIES REGARDING THIRD PARTY SOFTWARE, IF PRESENT IN THE
> SOFTWARE, AND DISTRIBUTES IT "AS IS."
>
>            
>
> LICENSEE AGREES TO WAIVE ANY AND ALL CLAIMS AGAINST THE U.S.
> GOVERNMENT AND THE UNITED STATES GOVERNMENT'S CONTRACTORS AND
> SUBCONTRACTORS, AND SHALL INDEMNIFY AND HOLD HARMLESS THE U.S.
> GOVERNMENT AND THE UNITED STATES GOVERNMENT'S CONTRACTORS AND
> SUBCONTRACTORS FOR ANY LIABILITIES, DEMANDS, DAMAGES, EXPENSES, OR
> LOSSES THAT MAY ARISE FROM RECIPIENT'S USE OF THE SOFTWARE OR PROVIDED
> DOCUMENTATION, INCLUDING ANY LIABILITIES OR DAMAGES FROM PRODUCTS
> BASED ON, OR RESULTING FROM, THE USE THEREOF.
>
> **[ACKNOWLEDGEMENT NOTICE]**:
>
> *This software was developed with funds from the Department of
> Homeland Security's Science and Technology Directorate.* 
>
> **[PROHIBITION ON USE OF DHS IDENTITIES NOTICE]**:
>
> A.  No user shall use the DHS or its component name, seal or other
> identity, or any variation or adaptation thereof, for an enhancement,
> improvement, modification or derivative work utilizing the software.
>
> B.  No user shall use the DHS or its component name, seal or other
> identity, or any variation or adaptation thereof for advertising its
> products or services, with the exception of using a factual statement
> such as included in the ACKNOWLEDGEMENT NOTICE indicating DHS funding
> of development of the software.           
>
> C.  No user shall make any trademark claim to the DHS or its component
> name, seal or other identity, or any other confusing similar identity,
> and no user shall seek registration of these identities at the U.S.
> Patent and Trademark Office.
