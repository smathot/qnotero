Qnotero v1.0.0~pre1


*Copyright 2011-2014 Sebastiaan Mathôt*

## Overview


- [What is Qnotero?](#what-is-qnotero)
- [Download and installation](#download-and-installation)
	- [Windows](#windows)
	- [Debian/ Ubuntu/ Linux Mint](#debian-ubuntu-linux-mint)
- [Mac OS](#mac-os)
- [Other operating systems](#other-operating-systems)
- [Gnote integration (Linux only)](#gnote-integration-linux-only)
- [Install Zotero standalone on Linux](#install-zotero-standalone-on-linux)
	- [Automated Zotero standalone installer script](#automated-zotero-standalone-installer-script)
	- [Zotero standalone PPA for Ubuntu/ Linux Mint](#zotero-standalone-ppa-for-ubuntu-linux-mint)
- [Support](#support)



## What is Qnotero?

Qnotero provides lightning quick access to your Zotero references. Zotero is an excellent open source reference manager, but it lacks a simple and direct way to access your references at the click of a button. That is why I created this simple program, which lives in the system tray and allows you to search through your references by Author and/ or Year of Publication. If a PDF file is attached to a reference you can open it directly from within Qnotero.

Freely available under the [GNU GPL 3](http://www.gnu.org/copyleft/gpl.html).

## Download and installation

### Windows

Windows binaries can be downloaded from GitHub:

- <https://github.com/smathot/qnotero/releases>

### Debian/ Ubuntu/ Linux Mint

Ubuntu/ Linux Mint users can install Qnotero through the [Cogsci.nl PPA]:

	sudo add-apt-repository ppa:smathot/cogscinl
	sudo apt-get update
	sudo apt-get install qnotero

## Mac OS

There is no Qnotero package available for Mac OS. It should be possible to run Qnotero from source, if you have all the dependencies installed (notably Python and PyQt4). Please let me know of any experiences running Qnotero on Mac OS (good or bad).

## Other operating systems

For other operating systems, you can (try to) run Qnotero from source. Source code for stable releases can be downloaded from GitHub:

- <- <https://github.com/smathot/qnotero/releases>>

## Gnote integration (Linux only)

If you have Gnote installed (a note-taking program for Linux), Qnotero automatically searches Gnote for a (section in a) note belonging to a specific article. Qnotero expects each note to be preceded by a bold line containing at least the name of the first author and the year of publication within parentheses, like so:

    Duhamel et al. (1992) Science 255

## Install Zotero standalone on Linux

### Automated Zotero standalone installer script

Linux users need to install Zotero standalone manually from a .tar.gz archive. This is a little inconvenient, which is why I created a simple installation script. This script downloads the latest version of Zotero standalone and creates a menu entry. If you use Ubuntu or Linux Mint, you can also use the PPA (see below).

To run the automated installer, type (or copy-paste) the following in a terminal:

    wget https://raw.github.com/smathot/zotero_installer/master/zotero_installer.sh \
        -O /tmp/zotero_installer.sh
    chmod +x /tmp/zotero_installer.sh
    /tmp/zotero_installer.sh

### Zotero standalone PPA for Ubuntu/ Linux Mint

Ubuntu/ Linux Mint users can install Zotero standalone from the [Cogsci.nl PPA]. Note that this method of installation is essentially a wrapper around the installation script (see above) and will therefore provide some unusual terminal output.

    sudo add-apt-repository ppa:smathot/cogscinl
    sudo apt-get update
    sudo apt-get install zotero-standalone

If you have previously installed Zotero standalone using the installer script above, you will need to remove the installed files before re-installing from the PPA. For a local installation, these are:

    /home/[user]/zotero
    /home/[user]/.local/share/applications/zotero.desktop

For a global installation, these are:

    /opt/zotero
    /usr/local/applications/zotero.desktop

## Support

There are a number of channels through which you can ask questions:

-   The comment section below is a good place for brief comments/ simple questions.
-   For (potentially) lengthy discussions, please use the [forum].

[cogsci.nl ppa]: https://launchpad.net/~smathot/+archive/ubuntu/cogscinl
[forum]: http://forum.cogsci.nl/

[Overview]: #overview
[What is Qnotero?]: #what-is-qnotero
[Download and installation]: #download-and-installation
[Windows]: #windows
[Debian/ Ubuntu/ Linux Mint]: #debian-ubuntu-linux-mint
[Mac OS]: #mac-os
[Other operating systems]: #other-operating-systems
[Gnote integration (Linux only)]: #gnote-integration-linux-only
[Install Zotero standalone on Linux]: #install-zotero-standalone-on-linux
[Automated Zotero standalone installer script]: #automated-zotero-standalone-installer-script
[Zotero standalone PPA for Ubuntu/ Linux Mint]: #zotero-standalone-ppa-for-ubuntu-linux-mint
[Support]: #support