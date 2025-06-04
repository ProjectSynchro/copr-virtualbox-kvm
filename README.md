Copr repository for VirtualBox, built with KVM support.

The packages in this repo should work on Fedora 41+.

## Installation 

Activate the repo with `sudo dnf copr enable jackgreiner/virtualbox-kvm` and then install the package with `sudo dnf install VirtualBox-kvm --refresh`.

To revert this, remove the copr repository with `sudo dnf copr remove jackgreiner/virtualbox-kvm` and then run `sudo dnf remove *VirtualBox-kvm*` to remove the virtualbox packages.


## Issues

Feel free to open issues when there are build issues I haven't fixed for a few days: https://github.com/ProjectSynchro/copr-virtualbox-kvm/issues

If you'd like me to attempt to package this for other RPM based distros like SUSE, open an issue and I'll see what I can do :)

## Known issues and limitations

* Currently, Intel x86_64 is the only supported host platform.
  * AMD will most likely work too but is considered experimental at the moment.
  * Processor support for the `XSAVE` instruction is required. This implies a
    2nd Gen Core processor or newer.
* Linux is required as a host operating system for building and running the KVM
  backend.
* Starting with Intel Tiger Lake (11th Gen Core processors) or newer, split lock
  detection must be turned off in the host system. This can be achieved using
  the Linux kernel command line parameter `split_lock_detect=off` or using the
  `split_lock_mitigate` sysctl.

## Networking

The new KVM backend utilizes the `--driverless` mode of VirtualBox. Some setups
that require kernel module support will not work in this mode and prevent the
VM from starting. Specifically, the Bridged adapter and "NAT Network" modes do
not work. Only regular NAT is easily supported. More complex setups will need
manual configuration, e.g., using `tun`/`tap` devices.


## Building Locally Using fedpkg

To build this package locally using `fedpkg`, follow these steps:

1. **Clone the Repository**:
    ```sh
    fedpkg clone -a https://github.com/ProjectSynchro/copr-virtualbox-kvm.git
    cd copr-virtualbox-kvm
    ```

2. **Install Dependencies**:
    ```sh
    sudo dnf install fedpkg
    sudo dnf builddep virtualbox-kvm.spec
    ```

3. **Build the Package**:
    ```sh
    spectool -g virtualbox-kvm.spec
    fedpkg local
    ```

This will create the RPM packages under a folder named by whatever arch you are building for in the current directory.

For more information on using `fedpkg`, refer to the [Fedora Packaging Guidelines](https://docs.fedoraproject.org/en-US/packaging-guidelines/).
