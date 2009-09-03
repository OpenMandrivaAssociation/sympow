%define name		sympow
%define	sympowdir	%{_datadir}/%{name}

Name:		%{name}
Group:		Sciences/Mathematics
License:	BSDish
Summary:	Compute special values of symmetric power elliptic curve L-functions
Version:	1.019
Release:	%mkrel 3
Source:		http://www.maths.bris.ac.uk/~mamjw/sympow.src.tar.bz2
# sagemath sympow datafiles
Source1:	datafiles.tar.bz2
URL:		http://www.maths.bris.ac.uk/~mamjw/
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

BuildRequires:	pari
Requires:	pari

Patch0:		sympow-1.019-datafiles.patch

%description
SYMPOW is a package to compute special values of symmetric power elliptic
curve L-functions. It can compute up to about 64 digits of precision.

%prep
%setup -q -n SYMPOW-%{version}

%patch0	-p1

perl -pi							\
	-e 's|"new_data"|"%{_datadir}/%{name}/bin/new_data"|;'	\
	-e 's|(standard.\.gp)|%{sympowdir}/$1|g;'		\
	generate.c

%build
sh Configure
make

%install
mkdir -p %{buildroot}%{_bindir}

cat > %{buildroot}%{_bindir}/%{name} << EOF
#!/bin/sh

SYMPOW_DATA=%{sympowdir}/datafiles
if test -n "\$SYMPOW_DIR"; then
    if [ ! -d \$SYMPOW_DIR/datafiles ]; then
	mkdir -p \$SYMPOW_DIR/datafiles
	cp -far \$SYMPOW_DATA/*.txt \$SYMPOW_DATA/param_data \$SYMPOW_DIR/datafiles
    fi
    cd \$SYMPOW_DIR
else
    cd %{sympowdir}
fi

exec %{sympowdir}/bin/%{name} "\$@"
EOF
chmod +x %{buildroot}%{_bindir}/%{name}

mkdir -p %{buildroot}%{sympowdir}/bin
cp -fa %{name} %{buildroot}%{sympowdir}/bin
cp -fa new_data %{buildroot}%{sympowdir}/bin
cp -fa standard?.gp %{buildroot}%{sympowdir}
tar jxf %{SOURCE1} -C %{buildroot}%{sympowdir}

%clean
rm -rf %{buildroot}

%files
%defattr(-,root,root)
%{_bindir}/%{name}
%dir %{sympowdir}
%{sympowdir}/*
