%define name fib
%define version 1.0.0
%define release 1.0

Summary: fib service pkg
Name: %{name}
Version: %{version}
Release: %{release}
Source0: %{name}-%{version}.tar.gz
Group: Services
BuildArch: x86_64
Vendor: na

License: UNKNOWN
BuildRequires:  git
BuildRequires:  python2-devel
BuildRequires:  python-pbr
BuildRequires:  python-setuptools



%description
fib service pkg

%pre

%prep
%setup -n %{name}-%{version} -n %{name}-%{version}

%build
python setup.py build
cd fib_c && make all

%install
python setup.py install --single-version-externally-managed -O1 --root=$RPM_BUILD_ROOT

install -m 755 -d $RPM_BUILD_ROOT/usr/bin
cp -a fib_c/fib_c %{buildroot}%{_bindir}
cp -a bin/* %{buildroot}%{_bindir}
chmod 755 %{buildroot}%{_bindir}/*

install -m 755 -d $RPM_BUILD_ROOT/etc/fib/
cp -a fibsvc.conf $RPM_BUILD_ROOT/etc/fib/

install -m 755 -d $RPM_BUILD_ROOT/usr/lib/systemd/system/
cp -a systemd/*.service $RPM_BUILD_ROOT/usr/lib/systemd/system/

%post
systemctl enable fib-api
systemctl restart fib-api
systemctl enable fib-svc
systemctl restart fib-svc

%preun
systemctl stop fib-api
systemctl disable fib-api
systemctl stop fib-svc
systemctl disable fib-svc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root, root)
%{python_sitelib}/fib
%{python_sitelib}/fib-*.egg-info
/usr/lib/systemd/system/*
/usr/bin/*
/etc/fib/*

%changelog
