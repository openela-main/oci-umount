%global provider        github
%global provider_tld    com
%global project         projectatomic
%global repo            oci-umount
# https://github.com/projectatomic/oci-umount
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          87f9237e1de6e0bb6aedec9165db0ffe214df004
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           oci-umount
Epoch:          2
Version:        2.3.4
Release:        2.git%{shortcommit}%{?dist}
Summary:        OCI umount hook for docker
Group:          Applications/Text
License:        GPLv3+
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz
ExclusiveArch: x86_64 aarch64 ppc64le s390x
Obsoletes: docker-oci-umount < 2:1.13.1-13
BuildRequires:  gcc
BuildRequires:  autoconf
BuildRequires:  automake
BuildRequires:  pkgconfig(yajl)
BuildRequires:  pkgconfig(libselinux)
BuildRequires:  pkgconfig(mount)
BuildRequires:  golang-github-cpuguy83-go-md2man
BuildRequires:  pcre-devel

%description
OCI umount hooks umount potential leaked mount points in a containers
mount name-spaces

%prep
%setup -q -n %{name}-%{commit}

%build
autoreconf -i
%configure --libexecdir=%{_libexecdir}/oci/hooks.d/
%make_build

%install
%make_install
install -d %{buildroot}%{_datadir}/%{name}/%{name}.d

%files
%{_libexecdir}/oci/hooks.d/%{name}
%{_mandir}/man1/%{name}.1*
%doc README.md
%license LICENSE
%config(noreplace) %{_sysconfdir}/%{name}.conf
%dir %{_libexecdir}/oci
%dir %{_libexecdir}/oci/hooks.d
%dir %{_datadir}/containers/oci/hooks.d
%dir %{_datadir}/%{name}
%dir %{_datadir}/%{name}/%{name}.d
%{_datadir}/%{name}/oci-umount-options.conf
%{_datadir}/containers/oci/hooks.d/%{name}.json
%ghost %{_sysconfdir}/%{name}/%{name}.d
%ghost /etc/oci-umount/oci-umount-options.conf

%changelog
* Wed Aug 08 2018 Lokesh Mandvekar <lsm5@redhat.com> - 2:2.3.4-2.git87f9237
- Resolves: #1614019 - disable i686 (and also ppc64)

* Wed Feb 28 2018 Dan Walsh <dwalsh@redhat.com> - 2:2.3.4-1.git
- Add new paths for CRI-O

* Thu Feb 08 2018 Fedora Release Engineering <releng@fedoraproject.org> - 2:2.3.3-2.gite3c9055
- Rebuilt for https://fedoraproject.org/wiki/Fedora_28_Mass_Rebuild

* Mon Jan 22 2018 Dan Walsh <dwalsh@redhat.com> - 2:2.3.3-1.git
- Support passing of stage via stage environment variable.

* Thu Dec 21 2017 Dan Walsh <dwalsh@redhat.com> - 2:2.3.2-1.git
- Fix oci-umount.json to run in stages to support CRI-O

* Tue Nov 7 2017 Dan Walsh <dwalsh@redhat.com> - 2:2.3.1-1.git51e7c505
-  Provide a knob log_level to control verbosity of messages

* Thu Sep 21 2017 Dan Walsh <dwalsh@redhat.com> - 2:2.2.0-2.git0a4dcd6
* Thu Sep 21 2017 Dan Walsh <dwalsh@redhat.com> - 2:2.2.0-2.git0a4dcd6
- Add support for multiple configuration files.
  oci-umount will still read config file /etc/oci-umount.conf if it
  exists, but will also read config files in /usr/share/oci-umount/oci-umount.d
  and config files in /etc/oci-umount/oci-umount.d.  If the same file name exists
  in both directories, then oci-umount will only use the content in /ect/oci-umount/oci-umount.d.
- Make Logs less noisy
- Improve logs output, adding containier id, and needed file information
- Add support for specifying submounts PATH/* will unmount all mountpoints 
  under PATH in a container
- Support for oci configuration files to specify when to run the plugin

* Thu Sep 21 2017 Lokesh Mandvekar <lsm5@fedoraproject.org> - 2:2.2.0-1.git0a4dcd6
- bump to v2.2.0

* Thu Aug 17 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:2.0.0-2.gitf90b64c
- rebased to f90b64c144ff1a126f7c57b32396e8990ca696fd

* Thu Jul 27 2017 Frantisek Kluknavsky <fkluknav@redhat.com> - 2:1.13-103.git7623f6a
- obsolete with epoch

* Thu Jul 20 2017 fkluknav <fkluknav@redhat.com> - 2:1.13-102.git7623f6a
- fixes according to package review

* Mon Jul 17 2017 fkluknav <fkluknav@redhat.com> - 2:1.13-101.git7623f6a
- adapted for Fedora, versioning continues from the current docker version

* Wed May 17 2017 Dan Walsh <dwalsh@redhat.com> - 0.1.1
- Initial RPM release
