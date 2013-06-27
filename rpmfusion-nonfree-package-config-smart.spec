%global debug_package %{nil}

%global	basearch %{_target_cpu}

%ifarch	%{ix86}
%global	basearch i386
%endif

%ifarch %{arm}
%ifarch armv7hl armv7hnl
%global	basearch armhfp
%else
%global	basearch arm
%endif
%endif

%global repo nonfree

Summary:    RPM Fusion (%{repo}) configuration files for the Smart package manager
Name:       rpmfusion-free-package-config-smart
Version:    19
Release:    1
License:    GPLv2+
Group:      System Environment/Base
URL:        http://rpmfusion.org/
Source0:    COPYING
Source1:    rpmfusion-%{repo}.channel
Source2:    rpmfusion-%{repo}-rawhide.channel
Source3:    rpmfusion-%{repo}-updates.channel
Source4:    rpmfusion-%{repo}-updates-testing.channel
BuildRoot:  %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
Requires:   smart
Provides:   smart-config-rpmfusion-%{repo} = %{version}-%{release}
%if %repo == "nonfree"
Requires:   rpmfusion-free-package-config-smart >= %{version}
%endif

%description
This package provides the configuration files required by the Smart package
manager to use RPM Fusion's "%{repo}" software repository.


%prep
%setup -cT
cp %{SOURCE0} .

%build

%install
rm -rf $RPM_BUILD_ROOT

mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels
for channel in %{SOURCE1} %{SOURCE2} %{SOURCE3} %{SOURCE4};do
  name=$(basename $channel)
  install -p -m0644 $channel $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
  sed -i 's/\$basearch/%{basearch}/' $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
  sed -i 's/\$releasever/%{fedora}/' $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
%ifnarch %{ix86} x86_64
  #Fedora secondary
  sed -i 's/free\/fedora\//free\/fedora-secondary\//' $RPM_BUILD_ROOT%{_sysconfdir}/smart/channels/$name
%endif
done

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root,-)
%doc COPYING
%config(noreplace) %{_sysconfdir}/smart/channels/*.channel

%changelog
* Thu Jun 27 2013 Nicolas Chauvet <kwizart@gmail.com> - 19-1
- Update to F-19

* Fri Sep 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 18-1
- Update for F-18

* Fri Sep 07 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-2
- Add support for secondary-arches

* Tue May 01 2012 Nicolas Chauvet <kwizart@gmail.com> - 17-1
- Update for F-17

* Mon Oct 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 16-1
- Update for F-16

* Mon Oct 17 2011 Nicolas Chauvet <kwizart@gmail.com> - 15-1
- Update for F-15

* Sat Apr 9 2011 Stewart Adam <s.adam at diffingo.com> - 14-1
- Update for F-14
- Use hardcoded %%{basearch} instead of %%{_target_cpu} (fixes #1268)

* Sun Mar 29 2009 Thorsten Leemhuis <fedora [AT] leemhuis [DOT] info> - 11-0.4
- rebuild for new F11 features

* Thu Dec 25 2008 Stewart Adam <s.adam at diffingo.com> 11-0.3
- Add "sleep 3m" to workaround buildsys bug

* Mon Dec 22 2008 Stewart Adam <s.adam at diffingo.com> 11-0.2
- Another workaround since buildsys doesn't seem to like ||:

* Sun Dec 21 2008 Stewart Adam <s.adam at diffingo.com> 11-0.1
- Update .channel files for devel
- Append ||: to cp so build doesn't fail on "make local"

* Thu Dec 11 2008 Stewart Adam <s.adam at diffingo.com> 10-2
- Make summary and description fields clearer

* Sat Dec 6 2008 Stewart Adam <s.adam at diffingo.com> 10-1
- Split rpmfusion-package-config-smart into free and nonfree
- Don't use %%{__commandname} in some places but not others

