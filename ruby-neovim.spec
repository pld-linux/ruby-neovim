#
# Conditional build:
%bcond_with	tests		# build without tests

%define	pkgname	neovim
Summary:	A Ruby client for Neovim
Name:		ruby-%{pkgname}
Version:	0.3.0
Release:	1
License:	MIT
Group:		Development/Languages
Source0:	http://rubygems.org/downloads/%{pkgname}-%{version}.gem
# Source0-md5:	fc4441ed1758ffb76008f29e9cfbe774
Patch0:		rubygems.patch
URL:		https://github.com/alexgenco/neovim-ruby
BuildRequires:	rpm-rubyprov
BuildRequires:	rpmbuild(macros) >= 1.656
BuildRequires:	sed >= 4.0
%if %{with tests}
BuildRequires:	ruby-bundler
BuildRequires:	ruby-pry
BuildRequires:	ruby-rake
BuildRequires:	ruby-rspec < 4
BuildRequires:	ruby-rspec >= 3.0
%endif
Requires:	ruby-msgpack < 2
Requires:	ruby-msgpack >= 1.0
Requires:	ruby-rubygems
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
A Ruby client for Neovim.

%prep
%setup -q -n %{pkgname}-%{version}
%{__sed} -i -e '1 s,#!.*ruby,#!%{__ruby},' bin/*
%patch0 -p1

%build
# write .gemspec
%__gem_helper spec

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{ruby_vendorlibdir},%{ruby_specdir},%{_bindir}}
cp -a lib/* $RPM_BUILD_ROOT%{ruby_vendorlibdir}
cp -a bin/* $RPM_BUILD_ROOT%{_bindir}
cp -p %{pkgname}-%{version}.gemspec $RPM_BUILD_ROOT%{ruby_specdir}

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/j2mp
%attr(755,root,root) %{_bindir}/mp2j
%attr(755,root,root) %{_bindir}/neovim-ruby-host
%{ruby_vendorlibdir}/%{pkgname}.rb
%{ruby_vendorlibdir}/%{pkgname}
%{ruby_specdir}/%{pkgname}-%{version}.gemspec
