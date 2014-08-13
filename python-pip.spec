%global with_python2 0
%global with_python3 1
%global build_wheel 1

%global srcname pip

%{?scl:%scl_package python-%{srcname}}
%{!?scl:%global pkg_name %{name}}
%{?scl:%global py3dir %{_builddir}/python3-%{name}-%{version}-%{release}}

%if 0%{?build_wheel}
%global python2_wheelname %{srcname}-*-py2.py3-none-any.whl
%if 0%{?with_python3}
%global python3_wheelname %python2_wheelname
%endif
%endif

Name:           %{?scl_prefix}python-%{srcname}
Version:        1.6
Release:        0.20.20140814gitb3aa026d%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        python3-nightly-pip-b3aa026d.tar
Patch0:         pip-1.6-allow-stripping-prefix-from-wheel-RECORD-files.patch
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
%if 0%{?with_python2}
BuildRequires:  python-devel
BuildRequires:  python-setuptools
%if 0%{?build_wheel}
BuildRequires:  python-pip
BuildRequires:  python-wheel
%endif
Requires:       python-setuptools
%endif # with_python2

%description
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.


%if 0%{?with_python3}
%package -n %{?scl_prefix}python3-%{srcname}
Summary:        A tool for installing and managing Python3 packages
Group:          Development/Libraries

BuildRequires:  %{?scl_prefix}python3-devel
BuildRequires:  %{?scl_prefix}python3-setuptools
%if 0%{?build_wheel}
BuildRequires:  %{?scl_prefix}python3-pip
BuildRequires:  %{?scl_prefix}python3-wheel
%endif
Requires:  %{?scl_prefix}python3-setuptools

%description -n %{?scl_prefix}python3-%{srcname}
Pip is a replacement for `easy_install
<http://peak.telecommunity.com/DevCenter/EasyInstall>`_.  It uses mostly the
same techniques for finding packages, so packages that were made
easy_installable should be pip-installable as well.
%endif # with_python3

%prep
%setup -q -n python3-nightly-%{srcname}

%patch0 -p1

%{__sed} -i '1d' pip/__init__.py

%if 0%{?with_python3}
cp -a . %{py3dir}
%endif # with_python3


%build
%{?scl:scl enable %scl - << \EOF}
%if 0%{?with_python2}
%if 0%{?build_wheel}
%{__python2} setup.py bdist_wheel
%else
%{__python2} setup.py build
%endif
%endif # with_python2

%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
%{__python3} setup.py bdist_wheel
%else
%{__python3} setup.py build
%endif
popd
%endif # with_python3
%{?scl:EOF}

%install
%{__rm} -rf %{buildroot}

%{?scl:scl enable %scl - << \EOF}
%if 0%{?with_python3}
pushd %{py3dir}
%if 0%{?build_wheel}
pip3 install -I dist/%{python3_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}

%if 0%{?with_python2}
# TODO: we have to remove this by hand now, but it'd be nice if we wouldn't have to
# (pip install wheel doesn't overwrite)
rm %{buildroot}%{_bindir}/pip
%endif # with_python2

%else
%{__python3} setup.py install --skip-build --root %{buildroot}
%endif
%endif # with_python3

%if 0%{?with_python2}
%if 0%{?build_wheel}
pip2 install -I dist/%{python2_wheelname} --root %{buildroot} --strip-file-prefix %{buildroot}
%else
%{__python} setup.py install -O1 --skip-build --root %{buildroot}
%endif
%endif # with_python2
%{?scl:EOF}

%clean
%{__rm} -rf %{buildroot}

# unfortunately, pip's test suite requires virtualenv >= 1.6 which isn't in
# fedora yet. Once it is, check can be implemented

%if 0%{?with_python2}
%files
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst docs
%attr(755,root,root) %{_bindir}/pip
%attr(755,root,root) %{_bindir}/pip2*
%{python_sitelib}/pip*
%endif # with_python2

%if 0%{?with_python3}
%files -n %{?scl_prefix}python3-%{srcname}
%defattr(-,root,root,-)
%doc LICENSE.txt README.rst docs
%attr(755,root,root) %{_bindir}/pip3*
%{python3_sitelib}/pip*

%if ! 0%{?with_python2}
%attr(755,root,root) %{_bindir}/pip
%endif # ! with_python2

%endif # with_python3

%changelog
* Thu Aug 14 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.20.20140814gitb3aa026d
- Update to git: b3aa026d

* Wed Aug 13 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.19.20140813git2eb6ed3c
- Update to git: 2eb6ed3c

* Tue Aug 12 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.18.20140812git739d0c16
- Update to git: 739d0c16

* Thu Aug 07 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.17.20140807git1605b761
- Update to git: 1605b761

* Tue Aug 05 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.16.20140805gitaaa4bfcd
- Update to git: aaa4bfcd

* Sat Aug 02 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.15.20140802gitfcdde73e
- Update to git: fcdde73e

* Fri Jul 25 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.14.20140725git530f5f87
- Update to git: 530f5f87

* Wed Jul 23 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.13.20140723git80fb4fd8
- Update to git: 80fb4fd8

* Fri Jul 18 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.12.20140718git19e29fc2
- Update to git: 19e29fc2

* Wed Jul 16 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.11.20140716git25bd97d7
- Update to git: 25bd97d7

* Fri Jul 11 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.10.20140711git7c652cb0
- Update to git: 7c652cb0

* Sat Jul 05 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.9.20140705gitd359d1a0
- Update to git: d359d1a0

* Fri Jul 04 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.8.20140704git2432fe67
- Rebased the stripping patch

* Fri Jul 04 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.7.20140704git2432fe67
- Update to git: 2432fe67

* Wed Jul 02 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.6.20140702gitc720ca67
- Update to git: c720ca67

* Tue Jul 01 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.5.20140701git6410ba43
- Update to git: 6410ba43

* Fri Jun 27 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.4.20140626gitbb6c11ed
- Bootstrap

* Thu Jun 26 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.3.20140626gitbb6c11ed
- Update to git: bb6c11ed
- SCL

* Sun May 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.6-1
- Update to 1.5.6

* Fri Apr 25 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-4
- Rebuild as wheel for Python 3.4

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-3
- Disable build_wheel

* Thu Apr 24 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-2
- Rebuild as wheel for Python 3.4

* Mon Apr 07 2014 Matej Stuchlik <mstuchli@redhat.com> - 1.5.4-1
- Updated to 1.5.4

* Mon Oct 14 2013 Tim Flink <tflink@fedoraproject.org> - 1.4.1-1
- Removed patch for CVE 2013-2099 as it has been included in the upstream 1.4.1 release
- Updated version to 1.4.1

* Sun Aug 04 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3.1-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_20_Mass_Rebuild

* Tue Jul 16 2013 Toshio Kuratomi <toshio@fedoraproject.org> - 1.3.1-4
- Fix for CVE 2013-2099

* Thu May 23 2013 Tim Flink <tflink@fedoraproject.org> - 1.3.1-3
- undo python2 executable rename to python-pip. fixes #958377
- fix summary to match upstream

* Mon May 06 2013 Kevin Kofler <Kevin@tigcc.ticalc.org> - 1.3.1-2
- Fix main package Summary, it's for Python 2, not 3 (#877401)

* Fri Apr 26 2013 Jon Ciesla <limburgher@gmail.com> - 1.3.1-1
- Update to 1.3.1, fix for CVE-2013-1888.

* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.2.1-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Tue Oct 09 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-2
- Fixing files for python3-pip

* Thu Oct 04 2012 Tim Flink <tflink@fedoraproject.org> - 1.2.1-1
- Update to upstream 1.2.1
- Change binary from pip-python to python-pip (RHBZ#855495)
- Add alias from python-pip to pip-python, to be removed at a later date

* Tue May 15 2012 Tim Flink <tflink@fedoraproject.org> - 1.1.0-1
- Update to upstream 1.1.0

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Sat Oct 22 2011 Tim Flink <tflink@fedoraproject.org> - 1.0.2-1
- update to 1.0.2 and added python3 subpackage

* Wed Jun 22 2011 Tim Flink <tflink@fedoraproject.org> - 0.8.3-1
- update to 0.8.3 and project home page

* Tue Feb 08 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 0.8.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Dec 20 2010 Luke Macken <lmacken@redhat.com> - 0.8.2-1
- update to 0.8.2 of pip
* Mon Aug 30 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.8-1
- update to 0.8 of pip
* Thu Jul 22 2010 David Malcolm <dmalcolm@redhat.com> - 0.7.2-5
- Rebuilt for https://fedoraproject.org/wiki/Features/Python_2.7/MassRebuild

* Wed Jul 7 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.2-1
- update to 0.7.2 of pip
* Sun May 23 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.7.1-1
- update to 0.7.1 of pip
* Fri Jan 1 2010 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1.4
- fix dependency issue
* Fri Dec 18 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-2
- fix spec file
* Thu Dec 17 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.6.1-1
- upgrade to 0.6.1 of pip
* Mon Aug 31 2009 Peter Halliday <phalliday@excelsiorsystems.net> - 0.4-1
- Initial package

