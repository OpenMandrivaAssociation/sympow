%define name		sympow
%define	sympowdir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Mathematics
License:	BSDish
Summary:	Compute special values of symmetric power elliptic curve L-functions
Version:	1.019
Release:	%mkrel 1
Source:		http://www.maths.bris.ac.uk/~mamjw/sympow.src.tar.bz2
URL:		http://www.maths.bris.ac.uk/~mamjw/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

Requires:	pari

Patch0:		sympow-1.019-datafiles.patch
Patch1:		sympow-1.019-new_data.patch

%description
SYMPOW is a package to compute special values of symmetric power elliptic
curve L-functions. It can compute up to about 64 digits of precision.

%prep
%setup -q -n SYMPOW-%{version}

%patch0	-p1
%patch1	-p1

perl -pi							\
	-e 's|"new_data"|"%{_datadir}/%{name}/bin/new_data"|;'	\
	-e 's|(standard.\.gp)|%{sympowdir}/$1|g;'		\
	generate.c

perl -pi							\
	-e 's|datafiles|sympowdat|;'				\
	standard?.gp

%build
sh Configure
make

%install
mkdir -p %{buildroot}%{_bindir}
cp -fa %{name} %{buildroot}%{_bindir}

mkdir -p %{buildroot}%{sympowdir}/bin
cp -fa new_data %{buildroot}%{sympowdir}/bin
cp -fa standard?.gp %{buildroot}%{sympowdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{sympowdir}
%{_datadir}/%{name}/*
