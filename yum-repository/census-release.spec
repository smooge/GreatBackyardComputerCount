Name:		census-release
Version:	1.00
Release:	1%{?dist}
Summary:	A simple yum/dnf census tool

License:	MIT
URL:		http://www.smoogespace.com/greatbackyardcounter
Source0:	%{name}-%{version}.tar.gz


%description
The Great Backyard Computer Counter is a project to better count
systems using DNF/Yum based applications with a dummy repository which
parses the OS, release, architecture, and uuid of the system. 

%prep
%setup -q 

%build
echo "Nothing to see here folks"

%install
rm -rf %{buildroot}

mkdir -p -m 755 %{buildroot}/etc/yum.repos.d/
mkdir -p %{buildroot}/%{_libexecdir}/census-release
install -m 700 census_setup.sh %{buildroot}/%{_libexecdir}/census-release
install -m 644 census.repo %{buildroot}/etc/yum.repos.d/

%post
%{buildroot}/%{_libexecdir}/census-release/census_setup.sh

%files
%doc README.rst LICENSE.MIT
/etc/yum.repos.d/census.repo
%{_libexecdir}/census-release/*
%ghost /etc/yum/vars/census_os
%ghost /etc/yum/vars/census_variant
%ghost /etc/yum/vars/census_uuid
%ghost /etc/dnf/vars/census_os
%ghost /etc/dnf/vars/census_variant
%ghost /etc/dnf/vars/census_uuid

%changelog
* Sun Jun 24 2018 Stephen Smoogen <smooge@smoogespace.com> - 1.00-1
- Fix obvious bugs with spec file to make it actually work

* Sun Jun 10 2018 Stephen Smoogen <smooge@smoogespace.com> - 1.00-1
- Setup the initial files

