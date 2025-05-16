# Standard compiler flags, without:
# -Wall        -- VirtualBox takes care of reasonable warnings very well
# -m32, -m64   -- 32bit code is built besides 64bit on x86_64
# -fexceptions -- R0 code doesn't link against C++ library, no __gxx_personality_v0
#global optflags %%(rpm --eval %%optflags |sed 's/-Wall//;s/-m[0-9][0-9]//;s/-fexceptions//')
# fix for error: code model kernel does not support PIC mode
#global optflags %%(echo %%{optflags} -fno-pic)
#global optflags %%(echo %%{optflags} | sed 's/-specs=.*cc1 //')

# In prerelease builds (such as betas), this package has the same
# major version number, while the kernel module abi is not guaranteed
# to be stable. This is so that we force the module update in sync with
# userspace.
#global prerel RC1
%global prereltag %{?prerel:_%(awk 'BEGIN {print toupper("%{prerel}")}')}

%global kvmpatch_ver 20250207

# Missing build-id in /builddir/build/BUILDROOT/VirtualBox-7.1.6-3.el9.x86_64/usr/lib64/virtualbox/iPxeBaseBin
%undefine _missing_build_ids_terminate_build

#%%if 0%%{?fedora} > 35
    #%%bcond_with webservice
#%%else
%bcond_without webservice
#%%endif
# Now we use upstream pdf
%bcond_with docs
%bcond_without vnc

%if 0%{?fedora} > 27 || 0%{?rhel} > 8
    %bcond_with guest_additions
%else
    %bcond_without guest_additions
%endif

%if 0%{?fedora}
    %bcond_without system_libtpms
%else
    %bcond_with system_libtpms
%endif

%if 0%{?fedora} || 0%{?rhel} > 8
    %bcond_without dxvk_native
%else
    %bcond_with dxvk_native
%endif

%if 0%{?fedora} > 40
# Python is not detected, yet
%bcond_with python3
%else
%bcond_without python3
%endif

Name:       VirtualBox-kvm
Version:    7.1.8
Release:    1.%{kvmpatch_ver}%{?dist}
Summary:    A general-purpose full virtualizer for PC hardware
Conflicts:  VirtualBox

License:    GPL-3.0-only AND (GPL-3.0-only OR CDDL-1.0)
URL:        https://www.virtualbox.org/wiki/VirtualBox

ExclusiveArch:  x86_64

Requires:   %{name}-server%{?isa} = %{version}

Source0:    https://download.virtualbox.org/virtualbox/%{version}%{?prereltag}/VirtualBox-%{version}%{?prereltag}.tar.bz2
Source1:    https://download.virtualbox.org/virtualbox/%{version}%{?prereltag}/UserManual.pdf
Source2:    VirtualBox.appdata.xml
Source3:    VirtualBox-60-vboxusb.rules
Source5:    VirtualBox-60-vboxguest.rules
Source6:    vboxclient.service
Source7:    vboxservice.service
Source8:    96-vboxguest.preset
Source10:   vboxweb.service
Source20:   os_mageia.png
Source21:   os_mageia_64.png
Source22:   os_mageia_x2.png
Source23:   os_mageia_64_x2.png
Source24:   os_mageia_x3.png
Source25:   os_mageia_64_x3.png
Source26:   os_mageia_x4.png
Source27:   os_mageia_64_x4.png

Patch1:     VirtualBox-7.0.2-noupdate.patch
Patch2:     VirtualBox-6.1.0-strings.patch
Patch3:     VirtualBox-7.1.0-default-to-Fedora.patch
Patch4:     VirtualBox-5.1.0-lib64-VBox.sh.patch
Patch5:     VirtualBox-python3.13.patch
Patch6:     0001-NEM-Implement-KVM-backend.patch

# from Mageia
Patch50:    VirtualBox-7.0.18-update-Mageia-support.patch
# from Fedora
Patch60:    VirtualBox-7.0.2-xclient-cleanups.patch
# from Arch
Patch70:    009-properly-handle-i3wm.patch
#from Gentoo
Patch80:    029_virtualbox-7.1.4_C23.patch


BuildRequires:  gcc-c++
BuildRequires:  kBuild >= 0.1.9998.r3093
BuildRequires:  openssl-devel
BuildRequires:  libcurl-devel
BuildRequires:  iasl
BuildRequires:  libxslt-devel
BuildRequires:  libIDL-devel
BuildRequires:  yasm
BuildRequires:  alsa-lib-devel
#BuildRequires:  opus-devel
BuildRequires:  pulseaudio-libs-devel
%if %{with python3}
BuildRequires:  python-rpm-macros
BuildRequires:  python%{python3_pkgversion}-devel
BuildRequires:  python%{python3_pkgversion}-setuptools
%endif
BuildRequires:  desktop-file-utils
BuildRequires:  libcap-devel
BuildRequires:  pkgconfig(Qt6Core)
BuildRequires:  pkgconfig(Qt6Help)
BuildRequires:  pkgconfig(Qt6Scxml)
BuildRequires:  xz-devel

%if %{with webservice}
BuildRequires:  gsoap-devel
%endif
BuildRequires:  pam-devel
BuildRequires:  genisoimage
#BuildRequires:  java-devel
%if %{with docs}
BuildRequires:  /usr/bin/pdflatex
BuildRequires:  docbook-dtds
BuildRequires:  docbook-style-xsl
BuildRequires:  doxygen-latex
BuildRequires:  texlive-collection-fontsrecommended
BuildRequires:  texlive-ec
BuildRequires:  texlive-ucs
BuildRequires:  texlive-tabulary
BuildRequires:  texlive-fancybox
%endif
BuildRequires:  boost-devel
BuildRequires:  liblzf-devel
BuildRequires:  libxml2-devel
BuildRequires:  libpng-devel
BuildRequires:  zlib-devel
BuildRequires:  device-mapper-devel
BuildRequires:  libvpx-devel
BuildRequires:  makeself
#For fixrom.pl
BuildRequires:  perl(FindBin)
BuildRequires:  perl(lib)

# for 32bit on 64
%ifarch x86_64
BuildRequires:  glibc-devel(x86-32)
BuildRequires:  libgcc(x86-32)
BuildRequires:  libstdc++-static(x86-32)
BuildRequires:  libstdc++-static(x86-64)
%else
BuildRequires:  libstdc++-static
%endif

# For the X11 module
BuildRequires:  libdrm-devel
BuildRequires:  xorg-x11-proto-devel
BuildRequires:  libXcomposite-devel
BuildRequires:  libXcursor-devel
BuildRequires:  libXdamage-devel
BuildRequires:  libXinerama-devel
BuildRequires:  libXmu-devel
BuildRequires:  libXrandr-devel
BuildRequires:  libXt-devel
BuildRequires:  mesa-libEGL-devel
BuildRequires:  mesa-libGL-devel
BuildRequires:  mesa-libGLU-devel
%if %{with vnc}
BuildRequires:  libvncserver-devel
%endif
%if %{with system_libtpms}
BuildRequires:	pkgconfig(libtpms)
%endif
BuildRequires:	pkgconfig(ogg)
BuildRequires:	pkgconfig(vorbis)
%if %{with dxvk_native}
BuildRequires:	glslang
# build fails with system dxvk_native
#BuildRequires:  dxvk-native-devel
%endif

%{?systemd_requires}
BuildRequires: systemd

%description
VirtualBox is a powerful x86 and AMD64/Intel64 virtualization product for
enterprise as well as home use. Not only is VirtualBox an extremely feature
rich, high performance product for enterprise customers, it is also the only
professional solution that is freely available as Open Source Software under
the terms of the GNU General Public License (GPL) version 2.

Presently, VirtualBox runs on Windows, Linux, Macintosh, and Solaris hosts and
supports a large number of guest operating systems including but not limited to
Windows (NT 4.0, 2000, XP, Server 2003, Vista, Windows 7, Windows 8, Windows
10), DOS/Windows 3.x, Linux (2.4, 2.6, 3.x and 4.x), Solaris and OpenSolaris,
OS/2, and OpenBSD.


%package server
Summary:    Core part (host server) for %{name}
Group:      Development/Tools
Requires:   hicolor-icon-theme
Conflicts:  VirtualBox-server
%if ! %{with python3}
Obsoletes:   python%{python3_pkgversion}-%{name}%{?isa} < %{version}-%{release}
%endif

%description server
%{name} without Qt GUI part.


%package webservice
Summary:        WebService GUI part for %{name}
Group:          System/Emulators/PC
Requires:       %{name}-server%{?isa} = %{version}
Conflicts:      VirtualBox-webservice

%description webservice
webservice GUI part for %{name}.

%package vnc
Summary:        VNC desktop sharing
Group:          System/Emulators/PC
Requires:       %{name} = %{version}
Conflicts:      VirtualBox-vnc
%description vnc
Virtual Network Computing (VNC) is a graphical desktop sharing system that uses the Remote Frame Buffer
protocol (RFB) to remotely control another computer. When this optional feature is desired, it is installed
as an "extpack" for VirtualBox. The implementation is licensed under GPL.

%package devel
Summary:    %{name} SDK
Group:      Development/Libraries
Requires:   %{name}-server%{?isa} = %{version}-%{release}
Conflicts:  VirtualBox-devel
%if %{with python3}
Requires:   python%{python3_pkgversion}-%{name}%{?isa} = %{version}-%{release}
%endif

%description devel
%{name} Software Development Kit.


%package -n python%{python3_pkgversion}-%{name}
Summary:    Python3 bindings for %{name}
Group:      Development/Libraries
Requires:   %{name}-server%{?_isa} = %{version}-%{release}
Conflicts:  VirtualBox-guest
%py_provides python%{python3_pkgversion}-%{name}

%description -n python%{python3_pkgversion}-%{name}
Python3 XPCOM bindings to %{name}.

%package guest-additions
Summary:    %{name} Guest Additions
Group:      System Environment/Base
Requires:   xorg-x11-server-Xorg
Requires:   xorg-x11-xinit
Provides:   %{name}-guest = %{version}-%{release}
Obsoletes:  %{name}-guest < %{version}-%{release}
Conflicts:  VirtualBox-guest
%if "%(xserver-sdk-abi-requires 2>/dev/null)"
Requires:   %(xserver-sdk-abi-requires ansic)
Requires:   %(xserver-sdk-abi-requires videodrv)
Requires:   %(xserver-sdk-abi-requires xinput)
%endif


%description guest-additions
This package replaces the application of Virtualbox's own methodology to
install Guest Additions (in menu: Devices | Insert Guest Additions CD-image file).
This subpackage provides tools that use kernel modules which support better
integration of VirtualBox guests with the Host, including file sharing, clipboard sharing,
video and mouse driver, USB and webcam proxy and Seamless mode.

%prep
%setup -q -n VirtualBox-%{version}%{?prereltag}
# add Mageia images
cp -a %{SOURCE20} %{SOURCE21} src/VBox/Frontends/VirtualBox/images/
cp -a %{SOURCE22} %{SOURCE23} src/VBox/Frontends/VirtualBox/images/x2/
cp -a %{SOURCE24} %{SOURCE25} src/VBox/Frontends/VirtualBox/images/x3/
cp -a %{SOURCE26} %{SOURCE27} src/VBox/Frontends/VirtualBox/images/x4/

# Remove prebuilt binary tools
find -name '*.py[co]' -delete
rm -r src/VBox/Additions/WINNT
rm -r src/VBox/Additions/os2
rm -r kBuild/
rm -r tools/
# Remove bundle X11 sources and some lib sources, before patching.
rm -r src/VBox/Additions/x11/x11include/
rm -r src/VBox/Additions/3D/mesa/mesa-21.3.8/
# wglext.h has typedefs for Windows-specific extensions
#rm include/VBox/HostServices/wglext.h
# src/VBox/GuestHost/OpenGL/include/GL/glext.h have VBOX definitions
#rm -r src/VBox/GuestHost/OpenGL/include/GL
rm -r src/VBox/Runtime/r3/darwin
rm -r src/VBox/Runtime/r0drv/darwin
rm -r src/VBox/Runtime/darwin

rm -r src/libs/liblzf-3.*/
rm -r src/libs/libpng-1.6.*/
rm -r src/libs/libxml2-2.*/
rm -r src/libs/openssl-3.*/
rm -r src/libs/zlib-1.3.*/
rm -r src/libs/curl-8.*/
rm -r src/libs/libvorbis-1.3.*/
rm -r src/libs/libogg-1.3.*/
rm -r src/libs/liblzma-5.*/
#rm -r src/libs/libslirp-4.*/
%if %{with system_libtpms}
rm -r src/libs/libtpms-0.9.*/
%endif
%if %{with dxvk_native}
#rm -r src/libs/dxvk-2.*/
%endif
#rm -r src/libs/softfloat-3e/

%patch -P 1 -p1 -b .noupdates
%patch -P 2 -p1 -b .strings
%patch -P 3 -p1 -b .default_os_fedora
%patch -P 4 -p1 -b .lib64-VBox.sh
%patch -P 5 -p1 -b .py3.13
%patch -P 6 -p1 -b .kvm

%patch -P 50 -p1 -b .mageia-support
%patch -P 60 -p1 -b .xclient
%patch -P 70 -p1 -b .i3wm
%patch -P 80 -p1 -b .c23


%build
./configure --disable-kmods \
  --with-kvm \
%if %{with webservice}
  --enable-webservice \
%endif
%if %{with vnc}
  --enable-vnc \
%endif
%if !%{with docs}
  --disable-docs \
%endif
%if !%{with python3}
  --disable-python \
%endif
  --disable-java \
  --disable-sdl

%if !%{with docs}
cp %{SOURCE1} UserManual.pdf
%endif

#--enable-libogg --enable-libvorbis
#--enable-vde
#--build-headless --build-libxml2
#--disable-xpcom
. ./env.sh
umask 0022

# The function VBoxExtPackIsValidEditionString only allows uppercase characters (A-Z) in the suffix.
%if "%{vendor}" == "RPM Fusion"
%global publisher _RPMFUSION
%else
%global publisher _%{?vendor:%(echo "%{vendor}" | \
    sed -e 's/[^[:alnum:]]//g; s/FedoraCopruser//' | cut -c -9 | tr '[:lower:]' '[:upper:]')}%{?!vendor:CUSTOM}
%endif

# VirtualBox build system installs and builds in the same step,
# not always looking for the installed files in places they have
# really been installed to. Therefore we do not override any of
# the installation paths
kmk %{_smp_mflags}                                             \
    KBUILD_VERBOSE=2                                           \
    TOOL_YASM_AS=yasm                                          \
    VBOX_PATH_APP_PRIVATE=%{_libdir}/virtualbox \
    VBOX_PATH_APP_PRIVATE_ARCH=%{_libdir}/virtualbox    \
    VBOX_PATH_APP_DOCS=%{_docdir}/VirtualBox    \
    VBOX_WITH_ORIGIN=                                   \
    VBOX_WITH_RUNPATH=%{_libdir}/virtualbox             \
    VBOX_GUI_WITH_SHARED_LIBRARY=1                      \
    VBOX_PATH_SHARED_LIBS=%{_libdir}/virtualbox         \
    VBOX_WITH_VBOX_IMG=1 \
    VBOX_WITH_VBOXIMGMOUNT=1 \
    VBOX_WITH_UNATTENDED=1  \
    VBOX_USE_SYSTEM_XORG_HEADERS=1                             \
    VBOX_USE_SYSTEM_GL_HEADERS=1                               \
    VBOX_NO_LEGACY_XORG_X11=1                                  \
    SDK_VBoxLibPng_INCS=/usr/include/libpng16                 \
    SDK_VBoxLibXml2_INCS=/usr/include/libxml2                 \
    SDK_VBoxLzf_LIBS="lzf"                                    \
    SDK_VBoxLzf_INCS="/usr/include/liblzf"                    \
    SDK_VBoxOpenSslStatic_INCS="/usr/include/openssl"                                   \
    SDK_VBoxOpenSslStatic_LIBS="ssl crypto"                         \
    SDK_VBoxZlib_INCS=""                                      \
%{?with_system_libtpms:   SDK_VBOX_LIBTPMS_INCS="/usr/include/libtpms"}  \
    SDK_VBoxLibVorbis_INCS="/usr/include/vorbis"                 \
    SDK_VBoxLibOgg_INCS="/usr/include/ogg"                       \
%{!?with_dxvk_native: VBOX_WITH_DXVK= }             \
%{?with_docs:   VBOX_WITH_DOCS=1 }                             \
    VBOX_JAVA_HOME=%{_prefix}/lib/jvm/java  \
    VBOX_WITH_REGISTRATION_REQUEST=         \
    VBOX_WITH_UPDATE_REQUEST=               \
    VBOX_WITH_TESTCASES=                    \
    VBOX_BUILD_PUBLISHER=%{publisher}

%if %{with vnc}
echo "build VNC extension pack"
# tar must use GNU, not POSIX, format here
# sed -i 's/tar /tar --format=gnu /' src/VBox/ExtPacks/VNC/Makefile.kmk
kmk -C src/VBox/ExtPacks/VNC packing KBUILD_VERBOSE=2
%endif

#    VBOX_GCC_WERR= \
#    TOOL_GCC3_CFLAGS="%{optflags}"   \
#    TOOL_GCC3_CXXFLAGS="%{optflags}" \
#    VBOX_GCC_OPT="%{optflags}" \
#    VBOX_WITH_CLOUD_NET:=
#    VBOX_WITH_VBOXSDL=1     \
#    VBoxSDL_INCS += \
#    VBoxSDL_LIBS
#    VBOX_WITH_SYSFS_BY_DEFAULT=1 \
#    VBOX_WITHOUT_PRECOMPILED_HEADERS=1      \
#    VBOX_XCURSOR_LIBS="Xcursor Xext X11 GL"             \
#    VBOX_DOCBOOK_WITH_LATEX    := 1
#    VBOX_WITH_EXTPACK_VBOXDTRACE=           \
#    VBOX_WITH_VBOXBFE :=
#    VBOX_PATH_DOCBOOK_DTD := /usr/share/xml/docbook/schema/dtd/4/


# doc/manual/fr_FR/ missing man_VBoxManage-debugvm.xml and man_VBoxManage-extpack.xml
#    VBOX_WITH_DOCS_TRANSLATIONS=1 \
# we can't build CHM DOCS we need hhc.exe which is not in source and we need
# also install wine:
# wine: cannot find
# '/builddir/build/BUILD/VirtualBox-5.1.6/tools/win.x86/HTML_Help_Workshop/v1.3//hhc.exe'
#    VBOX_WITH_DOCS_CHM=1 \
#    VBOX_WITH_ADDITION_DRIVERS = \
#    VBOX_WITH_INSTALLER = 1 \
#    VBOX_WITH_LINUX_ADDITIONS = 1 \
#    VBOX_WITH_X11_ADDITIONS = 1 \
#VBOX_WITH_LIGHTDM_GREETER=1 \


%install
# The directory layout created below attempts to mimic the one of
# the commercially supported version to minimize confusion

# Directory structure
install -d %{buildroot}%{_bindir}
install -d %{buildroot}%{_sbindir}
install -d %{buildroot}%{_libdir}
install -d %{buildroot}%{_libdir}/virtualbox
install -d %{buildroot}%{_libdir}/virtualbox/components
install -d %{buildroot}%{_libdir}/virtualbox/UnattendedTemplates
install -d %{buildroot}%{_libdir}/virtualbox/nls
install -d %{buildroot}%{_libdir}/virtualbox/ExtensionPacks
install -d %{buildroot}%{_libdir}/virtualbox/sdk
install -d %{buildroot}%{_datadir}/pixmaps
install -d %{buildroot}%{_metainfodir}
install -d %{buildroot}%{_datadir}/mime/packages
install -d %{buildroot}%{_datadir}/icons

# Libs
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/*.so

install -p -m 0644 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/VBoxEFI*.fd \
    out/linux.*/release/bin/*.r0

# Binaries
install -p -m 0755 out/linux.*/release/bin/VBox.sh %{buildroot}%{_bindir}/VBox

# Executables
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox \
    out/linux.*/release/bin/VirtualBox  \
    out/linux.*/release/bin/VBoxHeadless    \
    out/linux.*/release/bin/VBoxNetDHCP \
    out/linux.*/release/bin/VBoxNetNAT \
    out/linux.*/release/bin/VBoxNetAdpCtl   \
    out/linux.*/release/bin/VBoxVolInfo \
    out/linux.*/release/bin/SUPInstall \
    out/linux.*/release/bin/SUPLoggerCtl \
    out/linux.*/release/bin/SUPUninstall \
    out/linux.*/release/bin/VBoxAutostart \
    out/linux.*/release/bin/VBoxBalloonCtrl \
    out/linux.*/release/bin/VBoxExtPackHelperApp \
    out/linux.*/release/bin/VBoxManage  \
    out/linux.*/release/bin/VBoxSVC     \
    out/linux.*/release/bin/VBoxVMMPreload \
    out/linux.*/release/bin/VBoxSysInfo.sh  \
    out/linux.*/release/bin/vboxweb-service.sh \
%if %{with python3}
    out/linux.*/release/bin/vboxshell.py    \
%endif
    out/linux.*/release/bin/vbox-img    \
    out/linux.*/release/bin/vboximg-mount   \
    out/linux.*/release/bin/VBoxDTrace    \
    out/linux.*/release/bin/VBoxBugReport \
    out/linux.*/release/bin/VirtualBoxVM    \
    out/linux.*/release/bin/bldRTLdrCheckImports  \
    out/linux.*/release/bin/iPxeBaseBin         \
    out/linux.*/release/bin/VBoxCpuReport       \
    out/linux.*/release/bin/VBoxAudioTest       \
%if %{with webservice}
    out/linux.*/release/bin/vboxwebsrv  \
    out/linux.*/release/bin/webtest     \
%endif

#    out/linux.*/release/bin/VBoxSDL   \

# Wrapper with Launchers
ln -s VBox %{buildroot}%{_bindir}/VirtualBox
ln -s VBox %{buildroot}%{_bindir}/virtualbox
ln -s VBox %{buildroot}%{_bindir}/VBoxManage
ln -s VBox %{buildroot}%{_bindir}/vboxmanage
#ln -s VBox %{buildroot}%{_bindir}/VBoxSDL
#ln -s VBox %{buildroot}%{_bindir}/vboxsdl
ln -s VBox %{buildroot}%{_bindir}/VBoxVRDP
ln -s VBox %{buildroot}%{_bindir}/VBoxHeadless
ln -s VBox %{buildroot}%{_bindir}/vboxheadless
ln -s VBox %{buildroot}%{_bindir}/VBoxDTrace
ln -s VBox %{buildroot}%{_bindir}/vboxdtrace
ln -s VBox %{buildroot}%{_bindir}/VBoxBugReport
ln -s VBox %{buildroot}%{_bindir}/vboxbugreport
ln -s VBox %{buildroot}%{_bindir}/VBoxBalloonCtrl
ln -s VBox %{buildroot}%{_bindir}/vboxballoonctrl
ln -s VBox %{buildroot}%{_bindir}/VBoxAutostart
ln -s VBox %{buildroot}%{_bindir}/vboxautostart
ln -s VBox %{buildroot}%{_bindir}/VirtualBoxVM
ln -s VBox %{buildroot}%{_bindir}/virtualboxvm
%if %{with webservice}
ln -s VBox %{buildroot}%{_bindir}/vboxwebsrv
%endif
ln -s ../..%{_libdir}/virtualbox/vbox-img %{buildroot}%{_bindir}
ln -s ../..%{_libdir}/virtualbox/vboximg-mount %{buildroot}%{_bindir}

#ln -s /usr/share/virtualbox/src/vboxhost $RPM_BUILD_ROOT/usr/src/vboxhost-%VER%

# Components, preserve symlinks
cp -a out/linux.*/release/bin/components/* %{buildroot}%{_libdir}/virtualbox/components/
cp out/linux.*/release/bin/UnattendedTemplates/* %{buildroot}%{_libdir}/virtualbox/UnattendedTemplates

# Language files
install -p -m 0755 -t %{buildroot}%{_libdir}/virtualbox/nls \
    out/linux.*/release/bin/nls/*

# Python
%if %{with python3}
pushd out/linux.*/release/bin/sdk/installer/python
export VBOX_INSTALL_PATH=%{_libdir}/virtualbox
%{__python3} vboxapisetup.py install --prefix %{_prefix} --root %{buildroot}
%py3_shebang_fix -pni "%{__python3} %{py3_shbang_opts}" %{buildroot}${VBOX_INSTALL_PATH}/vboxshell.py
popd
%endif

# SDK
cp -rp out/linux.*/release/bin/sdk/. %{buildroot}%{_libdir}/virtualbox/sdk
rm -rf %{buildroot}%{_libdir}/virtualbox/sdk/installer

%if %{with python3}
pushd out/linux.*/release/bin/sdk/installer/python
%py_byte_compile %{__python3} %{buildroot}%{_libdir}/virtualbox/sdk/bindings/xpcom/python
popd
%endif

# Icons
install -p -m 0644 -t %{buildroot}%{_datadir}/pixmaps \
    out/linux.*/release/bin/VBox.png
for S in out/linux.*/release/bin/icons/*
do
    SIZE=$(basename $S)
    install -d %{buildroot}%{_datadir}/icons/hicolor/$SIZE/{mimetypes,apps}
    install -p -m 0644 $S/* %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes
    [ -f %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png ] && mv \
        %{buildroot}%{_datadir}/icons/hicolor/$SIZE/mimetypes/virtualbox.png \
        %{buildroot}%{_datadir}/icons/hicolor/$SIZE/apps/virtualbox.png
done
install -p -m 0644 out/linux.*/release/bin/virtualbox.xml %{buildroot}%{_datadir}/mime/packages

%if %{with guest_additions}
# Guest X.Org drivers
mkdir -p %{buildroot}%{_libdir}/security

# Guest-additions tools
install -m 0755 -t %{buildroot}%{_sbindir}   \
    out/linux.*/release/bin/additions/VBoxService            \
    out/linux.*/release/bin/additions/mount.vboxsf
install -m 0755 -t %{buildroot}%{_bindir}    \
    out/linux.*/release/bin/additions/VBoxDRMClient          \
    out/linux.*/release/bin/additions/VBoxClient             \
    out/linux.*/release/bin/additions/VBoxControl

# Guest libraries
install -m 0755 -t %{buildroot}%{_libdir}/security \
    out/linux.*/release/bin/additions/pam_vbox.so

# init/vboxadd-x11 code near call the function install_x11_startup_app
install -p -m 0755 -D src/VBox/Additions/x11/Installer/98vboxadd-xclient \
    %{buildroot}%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
ln -s ../..%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh \
    %{buildroot}%{_bindir}/VBoxClient-all
desktop-file-install --dir=%{buildroot}%{_sysconfdir}/xdg/autostart/ \
    --remove-key=Encoding src/VBox/Additions/x11/Installer/vboxclient.desktop
desktop-file-validate \
    %{buildroot}%{_sysconfdir}/xdg/autostart/vboxclient.desktop

install -p -m 0644 -D %{SOURCE7} %{buildroot}%{_unitdir}/vboxservice.service
install -p -m 0644 -D %{SOURCE8} %{buildroot}%{_presetdir}/96-vboxguest.preset
install -p -m 0644 -D %{SOURCE5} %{buildroot}%{_udevrulesdir}/60-vboxguest.rules
install -p -m 0644 -D %{SOURCE6} %{buildroot}%{_unitdir}/vboxclient.service

# Create a sysusers.d config file
cat >virtualbox-guest-additions.sysusers.conf <<EOF
# Group "vboxsf" for Shared Folders access.
# All users which want to access the auto-mounted Shared Folders
# have to be added to this group.
g vboxsf -
u vboxadd -:1 - /var/run/vboxadd -
EOF
install -m0644 -D virtualbox-guest-additions.sysusers.conf %{buildroot}%{_sysusersdir}/virtualbox-guest-additions.conf

%endif

cat >virtualbox.sysusers.conf << EOF
g vboxusers - - - -
EOF
install -m0644 -D virtualbox.sysusers.conf %{buildroot}%{_sysusersdir}/virtualbox.conf

%if %{with webservice}
install -m 0644 -D %{SOURCE10} \
    %{buildroot}%{_unitdir}/vboxweb.service
%endif

# Install udev rules
install -p -m 0755 -D out/linux.*/release/bin/VBoxCreateUSBNode.sh %{buildroot}%{_prefix}/lib/udev/VBoxCreateUSBNode.sh
install -p -m 0644 -D %{SOURCE3} %{buildroot}%{_udevrulesdir}/60-vboxusb.rules

# Menu entry
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    out/linux.*/release/bin/virtualbox.desktop
desktop-file-install --dir=%{buildroot}%{_datadir}/applications \
    out/linux.*/release/bin/virtualboxvm.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/virtualbox.desktop
desktop-file-validate %{buildroot}%{_datadir}/applications/virtualboxvm.desktop

install -p -m 0644 -D %{SOURCE2} %{buildroot}%{_metainfodir}/VirtualBox.appdata.xml

%if %{with vnc}
echo "entering VNC extension install section"
pushd out/linux.*/release/packages/
mkdir -p %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/VNC
install -D -m 644 VNC-*.vbox-extpack %{buildroot}%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack
popd
%endif

# to review:
#set_selinux_permissions /usr/lib/virtualbox /usr/share/virtualbox
# vboxautostart-service

%if %{with vnc}
%post vnc
EXTPACK="%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack"
ACCEPT="$(tar --to-stdout -xf "${EXTPACK}" ./ExtPack-license.txt | sha256sum | head --bytes=64)"
VBoxManage extpack install --replace "${EXTPACK}" --accept-license="${ACCEPT}" > /dev/null

%files vnc
%license COPYING
%dir %{_libdir}/virtualbox/ExtensionPacks/VNC/
%{_libdir}/virtualbox/ExtensionPacks/VNC/VNC-%{version}.vbox-extpack
%endif

%post server
# Assign USB devices
if /sbin/udevadm control --reload-rules >/dev/null 2>&1
then
   /sbin/udevadm trigger --subsystem-match=usb --action=add >/dev/null 2>&1 || :
   /sbin/udevadm settle >/dev/null 2>&1 || :
fi

%post webservice
%systemd_post vboxweb.service

%preun webservice
%systemd_preun vboxweb.service

%postun webservice
%systemd_postun_with_restart vboxweb.service

# Guest additions install
%post guest-additions
/sbin/ldconfig
%systemd_post vboxclient.service
%systemd_post vboxservice.service

#chcon -u system_u -t mount_exec_t "$lib_path/$PACKAGE/mount.vboxsf" > /dev/null 2>&1
# for i in "$lib_path"/*.so
# do
#     restorecon "$i" >/dev/null
# done
# ;;
#chcon -u system_u -t lib_t "$lib_dir"/*.so

# Our logging code generates some glue code on 32-bit systems.  At least F10
# needs a rule to allow this.  Send all output to /dev/null in case this is
# completely irrelevant on the target system.
#chcon -t unconfined_execmem_exec_t '/usr/bin/VBoxClient' > /dev/null 2>&1
#semanage fcontext -a -t unconfined_execmem_exec_t '/usr/bin/VBoxClient' > /dev/null 2>&1

%preun guest-additions
%systemd_preun vboxclient.service
%systemd_preun vboxservice.service

%postun guest-additions
/sbin/ldconfig
%systemd_postun_with_restart vboxclient.service
%systemd_postun_with_restart vboxservice.service

%files server
%doc doc/*cpp doc/VMM
%if %{with docs}
%doc out/linux.*/release/bin/UserManual*.pdf
%else
%doc UserManual.pdf
%endif
%license COPYING*
%{_bindir}/VBox
%{_bindir}/VBoxAutostart
%{_bindir}/vboxautostart
%{_bindir}/VBoxBalloonCtrl
%{_bindir}/vboxballoonctrl
%{_bindir}/VBoxBugReport
%{_bindir}/vboxbugreport
%{_bindir}/VBoxDTrace
%{_bindir}/vboxdtrace
%{_bindir}/vboxheadless
%{_bindir}/VBoxHeadless
%{_bindir}/VBoxManage
%{_bindir}/vboxmanage
#{_bindir}/VBoxSDL
#{_bindir}/vboxsdl
%{_bindir}/VBoxVRDP
%{_bindir}/VirtualBoxVM
%{_bindir}/virtualboxvm
%{_bindir}/vbox-img
%{_bindir}/vboximg-mount
%dir %{_libdir}/virtualbox
%{_libdir}/virtualbox/*.[^p]*
%exclude %{_libdir}/virtualbox/VBoxDbg.so
%exclude %{_libdir}/virtualbox/UICommon.so
%exclude %{_libdir}/virtualbox/VirtualBoxVM.so
%{_libdir}/virtualbox/components/
%{_libdir}/virtualbox/VBoxExtPackHelperApp
%{_libdir}/virtualbox/VBoxManage
%{_libdir}/virtualbox/VBoxSVC
%{_libdir}/virtualbox/VBoxBalloonCtrl
%{_libdir}/virtualbox/SUPInstall
%{_libdir}/virtualbox/SUPLoggerCtl
%{_libdir}/virtualbox/SUPUninstall
%{_libdir}/virtualbox/UnattendedTemplates
%{_libdir}/virtualbox/VBoxAutostart
%{_libdir}/virtualbox/VBoxVMMPreload
%{_libdir}/virtualbox/VBoxBugReport
%{_libdir}/virtualbox/VBoxDTrace
%{_libdir}/virtualbox/vbox-img
%{_libdir}/virtualbox/vboximg-mount
%{_libdir}/virtualbox/iPxeBaseBin
%{_libdir}/virtualbox/bldRTLdrCheckImports
%{_libdir}/virtualbox/VBoxCpuReport
%{_libdir}/virtualbox/VBoxAudioTest
# This permissions have to be here, before generator of debuginfo need
# permissions to read this files
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetNAT
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxVolInfo
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxHeadless
#%%attr(4511,root,root) %%{_libdir}/virtualbox/VBoxSDL
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetDHCP
%attr(4511,root,root) %{_libdir}/virtualbox/VBoxNetAdpCtl
%attr(4511,root,root) %{_libdir}/virtualbox/VirtualBoxVM
# Group for USB devices
%{_sysusersdir}/virtualbox.conf
%{_prefix}/lib/udev/VBoxCreateUSBNode.sh
%{_udevrulesdir}/60-vboxusb.rules
%{_datadir}/applications/virtualboxvm.desktop

%files
%{_bindir}/VirtualBox
%{_bindir}/virtualbox
%{_libdir}/virtualbox/VBoxDbg.so
%{_libdir}/virtualbox/UICommon.so
%{_libdir}/virtualbox/VirtualBox
%{_libdir}/virtualbox/VirtualBoxVM.so
%{_libdir}/virtualbox/nls
%{_datadir}/pixmaps/*.png
%{_datadir}/applications/virtualbox.desktop
%{_datadir}/icons/hicolor/*/apps/*.png
%{_datadir}/icons/hicolor/*/mimetypes/*.png
%{_datadir}/icons/hicolor/scalable/mimetypes/virtualbox.svg
%{_datadir}/mime/packages/virtualbox.xml
%{_metainfodir}/VirtualBox.appdata.xml

%if %{with webservice}
%files webservice
%{_bindir}/vboxwebsrv
%{_unitdir}/vboxweb.service
%{_libdir}/virtualbox/vboxwebsrv
%{_libdir}/virtualbox/webtest
%endif

%files devel
%{_libdir}/virtualbox/sdk

%if %{with python3}
%files -n python%{python3_pkgversion}-%{name}
%{_libdir}/virtualbox/*.py*
%{_libdir}/virtualbox/VBoxPython3*.so
%{python3_sitelib}/vboxapi-1*.egg-info
%{python3_sitelib}/vboxapi
%endif

%if %{with guest_additions}
%files guest-additions
%license COPYING*
%{_bindir}/VBoxClient
%{_bindir}/VBoxControl
%{_bindir}/VBoxClient-all
%{_bindir}/VBoxDRMClient
%{_sbindir}/VBoxService
%{_sbindir}/mount.vboxsf
%{_libdir}/security/pam_vbox.so
%{_sysconfdir}/X11/xinit/xinitrc.d/98vboxadd-xclient.sh
%{_sysconfdir}/xdg/autostart/vboxclient.desktop
%{_unitdir}/vboxclient.service
%{_unitdir}/vboxservice.service
%{_presetdir}/96-vboxguest.preset
%{_udevrulesdir}/60-vboxguest.rules
%{_sysusersdir}/virtualbox-guest-additions.conf
%endif

%changelog
* Fri May 16 2025 Jack Greiner <jack@emoss.org> - 7.1.8-1
- Initial VirtualBox-kvm package 
