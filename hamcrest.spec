# Copyright (c) 2000-2008, JPackage Project
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the
#    distribution.
# 3. Neither the name of the JPackage Project nor the names of its
#    contributors may be used to endorse or promote products derived
#    from this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

%define with()          %{expand:%%{?with_%{1}:1}%%{!?with_%{1}:0}}
%define without()       %{expand:%%{?with_%{1}:0}%%{!?with_%{1}:1}}
%define bcond_with()    %{expand:%%{?_with_%{1}:%%global with_%{1} 1}}
%define bcond_without() %{expand:%%{!?_without_%{1}:%%global with_%{1} 1}}

# This option controls integration which requires easymock2 and jmock
%bcond_with integration

# This option controls jarjar on qdox
# Since bundling the qdox classes prevents upgrades, we disable it by default
%bcond_with jarjar

# This option controls tests which requires ant-junit and testng
%bcond_with tests

# If integration is disabled, then tests are disabled
%if %without integration
%bcond_with tests
%endif

%define _with_gcj_support 1
%define gcj_support %{?_with_gcj_support:1}%{!?_with_gcj_support:%{?_without_gcj_support:0}%{!?_without_gcj_support:%{?_gcj_support:%{_gcj_support}}%{!?_gcj_support:0}}}

%global with_maven 0

Name:           hamcrest
Version:        1.1
Release:        9.4%{?dist}
Epoch:          0
Summary:        Library of matchers for building test expressions
License:        BSD
URL:            http://code.google.com/p/hamcrest/
Group:          Development/Tools
Source0:        http://hamcrest.googlecode.com/files/hamcrest-1.1.tgz
Source1:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-parent/1.1/hamcrest-parent-1.1.pom
Source2:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-library/1.1/hamcrest-library-1.1.pom
Source3:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-integration/1.1/hamcrest-integration-1.1.pom
Source4:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-generator/1.1/hamcrest-generator-1.1.pom
Source5:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-core/1.1/hamcrest-core-1.1.pom
Source6:        http://repo1.maven.org/maven2/org/hamcrest/hamcrest-all/1.1/hamcrest-all-1.1.pom
Source7:        hamcrest-text-1.1.pom
Source8:        hamcrest-core-MANIFEST.MF
Patch0:         hamcrest-1.1-build.patch
Patch1:         hamcrest-1.1-no-jarjar.patch
Patch2:         hamcrest-1.1-no-integration.patch
Requires:       java-1.6.0
%if %with integration
Requires:       easymock2
Requires:       jmock
%endif
Requires:       qdox
BuildRequires:  jpackage-utils >= 0:1.7.4
BuildRequires:  java-1.6.0-devel
BuildRequires:  ant >= 0:1.6.5
BuildRequires:  ant-junit
%if %with integration
BuildRequires:  easymock2
%endif
%if %with jarjar
BuildRequires:  jarjar
%endif
%if %with integration
BuildRequires:  jmock
%endif
BuildRequires:  junit
BuildRequires:  junit4
BuildRequires:  qdox
%if %with tests
BuildRequires:  testng
%endif

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
%if %{gcj_support}
BuildRequires:  java-gcj-compat-devel
%else
Buildarch:      noarch
%endif

Requires(post): jpackage-utils >= 0:1.7.4
Requires(postun): jpackage-utils >= 0:1.7.4

%description
Provides a library of matcher objects (also known as constraints or predicates)
allowing 'match' rules to be defined declaratively, to be used in other
frameworks. Typical scenarios include testing frameworks, mocking libraries and
UI validation rules.

%package javadoc
Group:          Documentation
Summary:        Javadoc for %{name}
BuildArch:      noarch

%description javadoc
Javadoc for %{name}.

%package demo
Group:          Development/Libraries
Summary:        Demos for %{name}
Requires:       %{name} = %{epoch}:%{version}-%{release}
Requires:       junit
Requires:       junit4
%if %with tests
Requires:       testng
%endif

%description demo
Demonstrations and samples for %{name}.

%prep
%setup -q
find . -type f -name "*.jar" | xargs -t rm
# BUILD/hamcrest-%{version}/lib/generator/jarjar-1.0rc3.jar.no
%if %with jarjar
ln -sf $(build-classpath jarjar) lib/generator/
%endif
# BUILD/hamcrest-1.1/lib/generator/qdox-1.6.1.jar.no
ln -sf $(build-classpath qdox) lib/generator/
# BUILD/hamcrest-1.1/lib/integration/easymock-2.2.jar.no
%if %with integration
ln -sf $(build-classpath easymock2) lib/integration/
%endif
# BUILD/hamcrest-1.1/lib/integration/jmock-1.10RC1.jar.no
%if %with integration
ln -sf $(build-classpath jmock) lib/integration/
%endif
# BUILD/hamcrest-1.1/lib/integration/junit-3.8.1.jar.no
ln -sf $(build-classpath junit) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/junit-4.0.jar.no
ln -sf $(build-classpath junit4) lib/integration/
# BUILD/hamcrest-1.1/lib/integration/testng-4.6-jdk15.jar.no
%if %with tests
ln -sf $(build-classpath testng-jdk15) lib/integration/
%endif
%patch0 -p0
%if %without jarjar
%patch1 -p1
%endif
%if %without integration
%patch2 -p1
%endif

perl -pi -e 's/\r$//g' LICENSE.txt

%build
export CLASSPATH=$(build-classpath qdox)
export OPT_JAR_LIST="junit ant/ant-junit"
%if %with integration
ant -Dant.build.javac.source=1.5 -Dversion=%{version} -Dbuild.sysclasspath=first all javadoc
%else
ant -Dant.build.javac.source=1.5 -Dversion=%{version} -Dbuild.sysclasspath=first clean core generator library text bigjar javadoc
%endif

# inject OSGi manifests
mkdir -p META-INF
cp -p %{SOURCE8} META-INF/MANIFEST.MF
touch META-INF/MANIFEST.MF
zip -u build/%{name}-core-%{version}.jar META-INF/MANIFEST.MF

%install
rm -rf $RPM_BUILD_ROOT
# jars
install -d -m 755 $RPM_BUILD_ROOT%{_javadir}/%{name}
%if %{with_maven}
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/maven2/poms
install -m 644 %{SOURCE1} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-parent.pom
%add_to_maven_depmap org.hamcrest %{name}-parent %{version} JPP/%{name} parent
%endif

install -m 644 build/%{name}-all-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/all-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE6} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-all.pom
%add_to_maven_depmap org.hamcrest %{name}-all %{version} JPP/%{name} all
%endif

install -m 644 build/%{name}-core-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/core-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE5} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-core.pom
%add_to_maven_depmap org.hamcrest %{name}-core %{version} JPP/%{name} core
%endif

install -m 644 build/%{name}-generator-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/generator-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE4} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-generator.pom
%add_to_maven_depmap org.hamcrest %{name}-generator %{version} JPP/%{name} generator
%endif

install -m 644 build/%{name}-library-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/library-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE2} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-library.pom
%add_to_maven_depmap org.hamcrest %{name}-library %{version} JPP/%{name} library
%endif

%if %with integration
install -m 644 build/%{name}-integration-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/integration-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE3} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-integration.pom
%add_to_maven_depmap org.hamcrest %{name}-integration %{version} JPP/%{name} integration
%endif
%endif

install -m 644 build/%{name}-text-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/text-%{version}.jar
%if %{with_maven}
install -m 644 %{SOURCE7} $RPM_BUILD_ROOT%{_datadir}/maven2/poms/JPP.%{name}-text.pom
%add_to_maven_depmap org.hamcrest %{name}-text %{version} JPP/%{name} text
%endif

%if %with tests
install -m 644 build/%{name}-unit-test-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/%{name}/unit-test-%{version}.jar
%endif

pushd $RPM_BUILD_ROOT%{_javadir}/%{name}
for jar in *-%{version}*; do ln -sf ${jar} `echo $jar| sed  "s|-%{version}||g"`; done
popd

# javadoc
install -d -m 755 $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadoc/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name}

# demo
install -d -m 755 $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%if %with integration
install -m 644 build/%{name}-examples-%{version}.jar $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}
%endif
cp -pr %{name}-examples $RPM_BUILD_ROOT%{_datadir}/%{name}-%{version}/
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_datadir}/%{name}

%if %{gcj_support}
%{_bindir}/aot-compile-rpm
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%if %{with_maven}
%update_maven_depmap
%endif
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%postun
%if %{with_maven}
%update_maven_depmap
%endif
%if %{gcj_support}
if [ -x %{_bindir}/rebuild-gcj-db ]
then
  %{_bindir}/rebuild-gcj-db
fi
%endif

%files
%defattr(0644,root,root,0755)
%doc LICENSE.txt
%dir %{_javadir}/%{name}
%{_javadir}/%{name}/all-%{version}.jar
%{_javadir}/%{name}/all.jar
%{_javadir}/%{name}/core-%{version}.jar
%{_javadir}/%{name}/core.jar
%{_javadir}/%{name}/generator-%{version}.jar
%{_javadir}/%{name}/generator.jar
%if %with integration
%{_javadir}/%{name}/integration-%{version}.jar
%{_javadir}/%{name}/integration.jar
%endif
%{_javadir}/%{name}/library-%{version}.jar
%{_javadir}/%{name}/library.jar
%{_javadir}/%{name}/text-%{version}.jar
%{_javadir}/%{name}/text.jar
%if %with tests
%{_javadir}/%{name}/unit-test-%{version}.jar
%{_javadir}/%{name}/unit-test.jar
%endif
%if %{with_maven}
%{_datadir}/maven2/*
%{_mavendepmapfragdir}/*
%endif
%if %{gcj_support}
%dir %{_libdir}/gcj/%{name}
%attr(-,root,root) %{_libdir}/gcj/%{name}/all-%{version}.jar.db
%attr(-,root,root) %{_libdir}/gcj/%{name}/all-%{version}.jar.so
%endif

%files javadoc
%defattr(0644,root,root,0755)
%{_javadocdir}/%{name}-%{version}
%{_javadocdir}/%{name}

%files demo
%defattr(0644,root,root,0755)
%{_datadir}/%{name}-%{version}
%{_datadir}/%{name}

%changelog
* Mon Jan 11 2010 Andrew Overholt <overholt@redhat.com> 0:1.1-9.4
- Add variable for shipping maven files.  Default to no.

* Mon Nov 30 2009 Dennis Gregorovic <dgregor@redhat.com> - 0:1.1-9.3
- Rebuilt for RHEL 6

* Tue Aug 18 2009 Alexander Kurtakov <akurtako@redhat.com> 0:1.1-9.2
- Add OSGi manifest for hamcrest-core.
- Make javadoc package noarch.

* Fri Jul 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-9.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Tue Feb 24 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0:1.1-8.1
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7.1
- Fedora-specific: enable GCJ support
- Fedora-specific: build with java 1.6.0
- Fedora-specific: disable integration and tests

* Mon Nov 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-7
- update summary and description

* Tue Oct 28 2008 David Walluck <dwalluck@redhat.com> 0:1.1-6
- make demo dependency on testng conditional

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-5
- fix GCJ file list
- simplify build by always setting OPT_JAR_LIST

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-4
- add epoch to demo Requires

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-3
- set -Dant.build.javac.source=1.5

* Fri Oct 24 2008 David Walluck <dwalluck@redhat.com> 0:1.1-2
- add options to build without integration, jarjar, and tests
- allow build with java-devel >= 1.5.0
- remove javadoc scriptlets
- use more strict file list
- fix maven directory ownership
- add non-versioned symlink for demo
- fix GCJ requires
- fix eol in LICENSE.txt
- remove Vendor and Distribution

* Tue Feb 19 2008 Ralph Apel <r.apel@r-apel.de> - 0:1.1-1jpp
- 1.1

* Mon Feb 11 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-4jpp
- Fix versioned jar name, was junit-4.3.1
- Restore Epoch

* Fri Jan 25 2008 Ralph Apel <r.apel@r-apel.de> - 0:4.3.1-3jpp
- build and upload noarch packages
- Add pom and depmap frag
- BR java-devel = 1.5.0
- Restore Vendor, Distribution from macros

* Tue Aug 07 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-2jpp
- Set gcj_support to 0 to work around problems with GCJ.
- Fix buglet with the gcj post/postun if statement.
- Fix tab / space problems.
- Fix buildroot.
- Update Summary.
- Convert html files to Unix file endings.
- Disable aot-compile-rpm because it's not working ATM.

* Mon Jul 09 2007 Ben Konrath <bkonrath@redhat.com> - 4.3.1-1jpp
- 4.3.1.

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1.fc7
- Add dist tag

* Mon Feb 12 2007 Thomas Fitzsimmons <fitzsim@redhat.com> - 3.8.2-3jpp.1
- Committed on behalf of Tania Bento <tbento@redhat.com>
- Update per Fedora review process
- Resolves rhbz#225954

* Thu Aug 10 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-3jpp.1
- Added missing requirements.

* Thu Aug 10 2006 Karsten Hopp <karsten@redhat.de> 0:3.8.2-2jpp_3fc
- Require(post/postun): coreutils

* Sun Jun 23 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_2fc
- Rebuilt.

* Sat Jun 22 2006 Deepak Bhole <dbhole@redhat.com> -  0:3.8.2-2jpp_1fc
- Upgrade to 3.8.2
- Added conditional native compilation.
- Fix path where demo is located.

* Mon Mar 03 2006 Ralph Apel <r.apel at r-apel.de> - 0:3.8.2-1jpp
- First JPP-1.7 release

* Sun Aug 23 2004 Randy Watler <rwatler at finali.com> - 0:3.8.1-4jpp
- Rebuild with ant-1.6.2
* Fri May 09 2003 David Walluck <david@anti-microsoft.org> 0:3.8.1-3jpp
- update for JPackage 1.5

* Fri Mar 21 2003 Nicolas Mailhot <Nicolas.Mailhot (at) JPackage.org> 3.8.1-2jpp
- For jpackage-utils 1.5

* Fri Sep 06 2002 Henri Gomez <hgomez@users.sourceforge.net> 3.8.1-1jpp
- 3.8.1

* Sun Sep 01 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-2jpp
- used original zip file

* Thu Aug 29 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.8-1jpp
- 3.8
- group, vendor and distribution tags

* Sat Jan 19 2002 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-6jpp
- versioned dir for javadoc
- no dependencies for manual and javadoc packages
- stricter dependency for demo package
- additional sources in individual archives
- section macro

* Sat Dec 1 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-5jpp
- javadoc in javadoc package

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-4jpp
- fixed previous releases ...grrr

* Wed Nov 21 2001 Christian Zoffoli <czoffoli@littlepenguin.org> 3.7-3jpp
- added jpp extension
- removed packager tag

* Sun Sep 30 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-2jpp
- first unified release
- s/jPackage/JPackage

* Mon Sep 17 2001 Guillaume Rousse <guillomovitch@users.sourceforge.net> 3.7-1mdk
- 3.7
- vendor tag
- packager tag
- s/Copyright/License/
- truncated description to 72 columns in spec
- spec cleanup
- used versioned jar
- moved demo files to %%{_datadir}/%%{name}

* Sat Feb 17 2001 Guillaume Rousse <g.rousse@linux-mandrake.com> 3.5-1mdk
- first Mandrake release
