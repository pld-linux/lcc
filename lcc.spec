Summary:	A simple non-optimizing ANSI C compiler
Summary(pl.UTF-8):	Prosty nie-optymalizujący kompilator ANSI C
Name:		lcc
Version:	4.2
Release:	1
License:	distributable
Vendor:		C. W. Fraser & H. R. Hanson <lcc-bugs@cs.princeton.edu>
Group:		Development/Tools
# Source0-md5:	f4b11e93b023350c0a8b7619b09cb782
Source0:	ftp://ftp.cs.princeton.edu/pub/packages/lcc/%{name}-%{version}.tar.gz
Patch0:		%{name}-ftol.patch
URL:		http://www.cs.princeton.edu/software/lcc/
# sed and grep are required only for installation
Requires(post):	grep
Requires(post):	sed
Requires(post,preun):	fileutils
Requires:	gcc
ExclusiveArch:	%{ix86}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
lcc is the ANSI C compiler described in Christopher W. Fraser's and
David R. Hanson's book A Retargetable C Compiler: Design and
Implementation (Addison-Wesley, 1995, ISBN 0-8053-1670-1).

It doesn't have all the abilites of gcc. It's mainly mean as tool for
testing your program's compilance with ANSI C standards (or with
anything else then gcc ;).

%description -l pl.UTF-8
lcc jest kompilatorem ANSI C opisanym w książce Christopher'a W.
Fraser'a and David'a R. Hanson'a pod tytułem A Retargetable C
Compiler: Design and Implementation (Addison-Wesley, 1995, ISBN
0-8053-1670-1).

lcc nie posiada wszystkich możliwości gcc. Jest głównie użyteczne jako
narzędzie testowania zgodności z ANSI C (lub czymkolwiek innym niż gcc
;).

%prep
%setup -q
#%patch -p1

%build
mkdir build
mkdir build/include
cp include/x86/linux/* build/include
ln -s `gcc -v 2>&1 | grep from | sed -e 's/.*from //' -e 's|/specs||'` build/gcc
export BUILDDIR=`pwd`/build
%{__make} lcc \
	HOSTFILE=etc/linux.c \
	CFLAGS="%{rpmcflags} -DLCCDIR='\"%{_libdir}/lcc/\"'"

%{__make} all \
	CFLAGS="%{rpmcflags}"

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{_bindir},%{_libdir}/lcc,%{_mandir}/man1}

install build/lcc $RPM_BUILD_ROOT%{_bindir}
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
%dir %{_libdir}/lcc
%attr(755,root,root) %{_libdir}/lcc/bprint
%attr(755,root,root) %{_libdir}/lcc/cpp
%attr(755,root,root) %{_libdir}/lcc/lburg
%attr(755,root,root) %{_libdir}/lcc/rcc
%{_libdir}/lcc/include
%{_libdir}/lcc/liblcc.a
%{_mandir}/man?/*
