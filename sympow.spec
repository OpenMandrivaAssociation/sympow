%global         sympowdir                %{_libdir}/%{name}

Name:           sympow
Version:        1.019
Release:        4%{?dist}
Summary:        Special Values of Symmetric Power Elliptic Curve L-Functions
License:        BSD
URL:            http://www.maths.bris.ac.uk/~mamjw/
Source0:        http://www.maths.bris.ac.uk/~mamjw/sympow.tar.bz2
Source1:        sympow-README.Fedora
Patch0:         sympow-1.019-datafiles.patch
BuildRequires:  pari


%description
SYMPOW is a program for computing special values of symmetric power
elliptic curve L-functions.


%prep
%setup -q -n SYMPOW-%{version}
cp -p %{SOURCE1} README.Fedora
%patch0 -p1

sed \
    -e 's|"new_data"|"%{sympowdir}/new_data"|' \
    -e 's|\(standard.\.gp\)|%{sympowdir}/\1|g' \
    -i generate.c

%build
export CFLAGS="%{optflags}"
sh Configure
make %{?_smp_mflags}


%install
mkdir -p $RPM_BUILD_ROOT%{sympowdir}/datafiles
# executables
install -m 755 %{name} $RPM_BUILD_ROOT%{sympowdir}/
install -m 755 new_data $RPM_BUILD_ROOT%{sympowdir}/
# datafiles
install -m 644 datafiles/* $RPM_BUILD_ROOT%{sympowdir}/datafiles/
# more datafiles
install -m 644 *.gp $RPM_BUILD_ROOT%{sympowdir}/

# launcher script
mkdir -p $RPM_BUILD_ROOT%{_bindir}
cat > $RPM_BUILD_ROOT%{_bindir}/%{name} << EOF
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

exec %{sympowdir}/%{name} "\$@"
EOF
chmod +x $RPM_BUILD_ROOT%{_bindir}/%{name}

%files
%doc README COPYING README.Fedora
%{_bindir}/%{name}
%{_libdir}/%{name}
