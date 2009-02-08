Summary:	High rate file compressor
Name:		paq8p
Version:	1.0
Release:	%mkrel 1
License:	GPLv3
Group:		Archiving/Compression
URL:		http://www2.cs.fit.edu/~mmahoney/compression/
Source0:	http://www2.cs.fit.edu/~mmahoney/compression/paq8p.zip
Patch0:		paq8p-asm-labels.patch
Patch1:		paq8p-asm-noexec.patch
%ifarch %{ix86}
BuildRequires:	nasm
%endif
%ifarch x86_64
BuildRequires:	yasm
%endif
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
PAQ8p is a file compressor that achieve very high compression rates at
the expense of speed and memory.

%prep 
%setup -q -c -n %{name}
%patch0 -p1 -b .label
#how to fix exec stack in yasm?
#%patch1 -p1 -b .noexec

%build
%ifarch %{ix86}
nasm -f elf paq7asm.asm
nasm -f elf paq7asmsse.asm
nasm -f elf paq7asmsse2.asm
g++ paq8p.cpp %{optflags} -DNOASM -DUNIX -s -o paq8p_i386
g++ paq8p.cpp %{optflags} -DUNIX -s -o paq8p_mmx paq7asm.o
g++ paq8p.cpp %{optflags} -DUNIX -s -o paq8p_sse paq7asmsse.o
g++ paq8p.cpp %{optflags} -DUNIX -s -o paq8p_sse2 paq7asmsse2.o
%endif

%ifarch x86_64
yasm paq7asm-x86_64.asm -f elf -m amd64
g++ paq8p.cpp %{optflags} -DUNIX -s -o paq8p paq7asm-x86_64.o
g++ paq8p.cpp %{optflags} -DNOASM -DUNIX -s -o paq8p_noasm
%endif

%install
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

install -d %{buildroot}%{_bindir}
%ifarch x86_64
install -m 0755 paq8p %{buildroot}%{_bindir}/
install -m 0755 paq8p_noasm %{buildroot}%{_bindir}/
%endif
%ifarch %{ix86}
install -m 0755 paq8p_i386 %{buildroot}%{_bindir}/
install -m 0755 paq8p_mmx %{buildroot}%{_bindir}/
install -m 0755 paq8p_sse %{buildroot}%{_bindir}/
install -m 0755 paq8p_sse2 %{buildroot}%{_bindir}/
ln -sf %{_bindir}/paq8p_sse2 %{buildroot}%{_bindir}/paq8p
%endif

%clean
[ -n "%{buildroot}" -a "%{buildroot}" != / ] && rm -rf %{buildroot}

%files
%defattr(-,root,root)
%doc readme.txt
%attr(0755,root,root) %{_bindir}/paq8p*

