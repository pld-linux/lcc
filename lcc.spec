Summary:	a simple non-optimizing ANSI C compiler
Summary(pl):	prosty nie-optymalizuj±cy kompilator ANSI C
Name:		lcc
Version:	4.1
Release:	3
License:	distributable
Group:		Development/Tools
URL:		http://www.cs.princeton.edu/software/lcc/
Source0:	ftp://ftp.cs.princeton.edu/pub/packages/lcc/%{name}-%{version}.tar.gz
Patch0:		%{name}-ftol.patch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)
Requires:	gcc
# sed and grep are required only for installation
Prereq:		sed
Prereq:		grep
ExclusiveArch:	%{ix86}
Vendor:		C. W. Fraser & H. R. Hanson <lcc-bugs@cs.princeton.edu>

%description
lcc is the ANSI C compiler described in Christopher W. Fraser's and
David R. Hanson's book A Retargetable C Compiler: Design and
Implementation (Addison-Wesley, 1995, ISBN 0-8053-1670-1).

It doesn't have all the abilites of gcc. It's mainly mean as tool for
testing your program's compilance with ANSI C standards (or with
anything else then gcc ;).

%description -l pl
lcc jest kompilatorem ANSI C opisanym w ksi±¿ce Christopher'a W.
Fraser'a and David'a R. Hanson'a pod tytu³em A Retargetable C
Compiler: Design and Implementation (Addison-Wesley, 1995, ISBN
0-8053-1670-1).

lcc nie posiada wszystkich mo¿liwo¶ci gcc. Jest g³ównie u¿yteczne jako
narzêdzie testowania zgodno¶ci z ANSI C (lub czymkolwiek innym ni¿ gcc
;).

%prep
%setup -q
%patch -p1

%build
mkdir build
mkdir build/include
cp include/x86/linux/* build/include
ln -s `gcc -v 2>&1 | grep from | sed -e 's/.*from //' -e 's|/specs||'` build/gcc
export BUILDDIR=`pwd`/build
%{__make} HOSTFILE=etc/linux.c lcc \
	CFLAGS="%{rpmcflags} \
		-DLCCDIR='\"%{_libdir}/lcc/\"'"
%{__make} all CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/lcc,%{_mandir}/man1}
cp build/lcc $RPM_BUILD_ROOT%{_bindir}
cp -r build/{bprint,cpp,lburg,rcc,liblcc.a,include} \
	$RPM_BUILD_ROOT%{_libdir}/lcc
install doc/*.1 lburg/*.1 $RPM_BUILD_ROOT%{_mandir}/man1

%post
# lcc is not really gcc version dependent, possibly most version will do
ln -sf `gcc -v 2>&1 | grep from | sed -e 's/.*from //' -e 's|/specs||'` \
	%{_libdir}/lcc/gcc

%preun
rm -f %{_libdir}/lcc/gcc

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc README LOG CPYRIGHT doc/*html
%attr(755,root,root) %{_bindir}/lcc
%attr(755,root,root) %{_libdir}/lcc/bprint
%attr(755,root,root) %{_libdir}/lcc/cpp
%attr(755,root,root) %{_libdir}/lcc/lburg
%attr(755,root,root) %{_libdir}/lcc/rcc
%dir %{_libdir}/lcc
%{_libdir}/lcc/include
%{_libdir}/lcc/liblcc.a
%{_mandir}/man?/*
