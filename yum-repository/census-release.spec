Name:		census-release
Version:	1.00
Release:	1%{?dist}
Summary:	A simple yum/dnf census tool

License:	MIT
URL:		http://www.smoogespace.com/greatbackyardcounter
Source0:	census_setup.sh
Source1:        census.repo


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
mkdir -p %{buildroot}/%{_libexec}/census-release
instlal -m 700 %{SOURCE0} %{buildroot}/%{_libexec}/census-release
install -m 644 %{SOURCE1} %{buildroot}/etc/yum.repos.d/

%post
%{buildroot}/%{_libexec}/census-release/census_setup.sh

%files
%doc README.rst LICENSE.MIT
%{_libexec}/census-release/*


%changelog
* Sun Jun 10 2018 Stephen Smoogen <smooge@smoogespace.com> - 1.00-1
- Setup the initial files

