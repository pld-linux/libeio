#
# Conditional build:
%bcond_without	static_libs	# don't build static library
#
Summary:	libeio - an asynchronous I/O library
Name:		libeio
Version:	1.0
Release:	1
License:	BSD or GPL v2+
Group:		Libraries
Source0:	%{name}-20100311.tar.bz2
# Source0-md5:	a3b50842b683b3dfd17af57db767e484
# cvs -z3 -d :pserver:anonymous@cvs.schmorp.de/schmorpforge co libeio
URL:		http://software.schmorp.de/pkg/libeio
BuildRequires:	autoconf >= 2.50
BuildRequires:	automake
# inotify interface
BuildRequires:	glibc-devel >= 6:2.4
BuildRequires:	libtool
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Libeio is a full-featured asynchronous I/O library for C, modelled in
similar style and spirit as libev. Features include: asynchronous read,
write, open, close, stat, unlink, fdatasync, mknod, readdir etc. (basically
the full POSIX API). sendfile (native on solaris, linux, hp-ux, freebsd,
emulated everywehere else), readahead (emulated where not available).

%package devel
Summary:	Header files for libeio library
Summary(pl.UTF-8):	Pliki nagłówkowe biblioteki libeio
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for libeio library.

%description devel -l pl.UTF-8
Pliki nagłówkowe biblioteki libeio.

%package static
Summary:	Static libeio library
Summary(pl.UTF-8):	Statyczna biblioteka libeio
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static libeio library.

%description static -l pl.UTF-8
Statyczna biblioteka libeio.

%prep
%setup -q -n %{name}

%build
%{__libtoolize}
%{__aclocal}
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	%{!?with_static_libs:--disable-static}

# override -O3 which overrides our optflags in configure
%{__make} \
	CFLAGS="%{rpmcflags} -D_GNU_SOURCE"

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc Changes LICENSE
%attr(755,root,root) %{_libdir}/libeio.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libeio.so.1

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libeio.so
%{_libdir}/libeio.la
%{_includedir}/eio.h

%if %{with static_libs}
%files static
%defattr(644,root,root,755)
%{_libdir}/libeio.a
%endif
