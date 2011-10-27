%define debug_package %{nil}

%ifarch	%{ix86}
%define	basearch i386
%else
%define	basearch %{_target_cpu}
%endif

Summary:    RPM Fusion (nonfree) configuration files for the Smart package manager
Name:       rpmfusion-nonfree-package-config-smart
Version:    16
Release:    2
License:    GPLv2+
Group:      System Environment/Base
URL:        http://rpmfusion.org/
Source0:    COPYING
Source1:    rpmfusion-nonfree.channel
Source2:    rpmfusion-nonfree-rawhide.channel
Source3:    rpmfusion-nonfree-updates.channel
Source4:    rpmfusion-nonfree-updates-testing.channel
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   smart
Requires:   rpmfusion-free-package-config-smart >= %{version}-%{release}
Provides:   smart-config-rpmfusion-nonfree = %{version}-%{release}

%description
This package provides the configuration files required by the Smart package
manager to use RPM Fusion's "nonfree" software repository.

%prep
%setup -cT
cp %{SOURCE0} .
sleep 3m

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels
for channel in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4};do
  name=$(basename $channel)
  %{__install} -p -m0644 $channel $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
  sed -i 's/\$basearch/%{basearch}/' $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
  sed -i 's/\$releasever/%{fedora}/' $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/smart/channels/*.channel

%changelog
* Wed Oct 26 2011 Nicolas Chauvet <kwizart@gmail.com> - 16-2
- Fix basearch on i386 - rfbz#2000

* Mon Oct 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 16-1
- Update for F-16

* Mon Oct 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 15-1
- Update for F-15

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 11-0.4
- rebuild for new F11 features

* Fri Dec 26 2008 Stewart Adam <s.adam at diffingo.com> 11-0.3
- Add "sleep 3m" to workaround buildsys bug
- Update .channel files for devel

* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> 10-2
- Make summary and description fields clearer

* Sat Dec 6 2008 Stewart Adam <s.adam at diffingo.com> 10-1
- Split rpmfusion-package-config-smart into free and nonfree
- Don't use %%{__commandname} in some places but not others
- Add rpmfusion-free-package-config-smart requires

