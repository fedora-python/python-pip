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
Version:        6.1.0
Release:        0.65.20150701git0ba95ace%{?dist}
Summary:        A tool for installing and managing Python packages

Group:          Development/Libraries
License:        MIT
URL:            http://www.pip-installer.org
Source0:        python3-nightly-pip-0ba95ace.tar
Patch0:         pip-allow-stripping-prefix-from-wheel-RECORD-files.patch
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
* Wed Jul 01 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.65.20150701git0ba95ace
- Update to git: 0ba95ace

* Tue Jun 30 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.64.20150630git40242fe4
- Update to git: 40242fe4

* Thu Jun 25 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.63.20150625git8f828b49
- Update to git: 8f828b49

* Wed Jun 24 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.62.20150624git0b9beab5
- Update to git: 0b9beab5

* Sat Jun 20 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.61.20150620git759eba04
- Update to git: 759eba04

* Wed Jun 10 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.60.20150610git530464b1
- Update to git: 530464b1

* Tue Jun 09 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.59.20150609git8e3eaec5
- Update to git: 8e3eaec5

* Wed Jun 03 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.58.20150603git6ad6c597
- Update to git: 6ad6c597

* Tue Jun 02 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.57.20150602git19623d82
- Update to git: 19623d82

* Fri May 29 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.56.20150529git91172f57
- Update to git: 91172f57

* Wed May 27 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.55.20150527gitb3c6f611
- Update to git: b3c6f611

* Sun May 24 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.54.20150524gitc6310814
- Update to git: c6310814

* Sat May 23 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.53.20150523git91e59df2
- Update to git: 91e59df2

* Fri May 22 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.52.20150522git02331fb2
- Update to git: 02331fb2

* Thu May 21 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.51.20150521git83aae0f6
- Update to git: 83aae0f6

* Wed May 20 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.50.20150520gitfa571061
- Update to git: fa571061

* Sat May 16 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.49.20150516git869ad9ad
- Update to git: 869ad9ad

* Fri May 15 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.48.20150515git416f9d0e
- Update to git: 416f9d0e

* Wed May 13 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.47.20150513git7d1a2361
- Update to git: 7d1a2361

* Mon May 11 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.46.20150511git99d2d1ce
- Update to git: 99d2d1ce

* Sun May 10 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.45.20150510git1f16235f
- Update to git: 1f16235f

* Sat May 09 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.44.20150509git43ac83fb
- Update to git: 43ac83fb

* Tue May 05 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.43.20150505git0f0a4f0f
- Update to git: 0f0a4f0f

* Sun May 03 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.42.20150503gitada5a6d5
- Update to git: ada5a6d5

* Wed Apr 29 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.41.20150429gite1e428bb
- Update to git: e1e428bb

* Mon Apr 27 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.40.20150427git8de0217e
- Update to git: 8de0217e

* Sat Apr 25 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.39.20150425gitd2ec9164
- Update to git: d2ec9164

* Fri Apr 24 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.38.20150424git31eb67d0
- Update to git: 31eb67d0

* Thu Apr 23 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.37.20150423git33764609
- Update to git: 33764609

* Wed Apr 22 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.36.20150422git6cc0e28f
- Update to git: 6cc0e28f

* Sat Apr 18 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.35.20150418git0e1704ac
- Update to git: 0e1704ac

* Thu Apr 16 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.34.20150416gita761f018
- Update to git: a761f018

* Tue Apr 14 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.33.20150414gitd043e4bc
- Update to git: d043e4bc

* Mon Apr 13 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.32.20150413gitb5762ca9
- Update to git: b5762ca9

* Fri Apr 10 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.31.20150410gitc6e149f6
- Update to git: c6e149f6

* Thu Apr 09 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.30.20150409git87ab2a00
- Update to git: 87ab2a00

* Wed Apr 08 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.29.20150408git0c9af4ca
- Update to git: 0c9af4ca

* Tue Apr 07 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.28.20150407gitf82d033b
- Update to git: f82d033b

* Sun Apr 05 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.27.20150405gitfeb5cae3
- Update to git: feb5cae3

* Sat Apr 04 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.26.20150404git34e27fe8
- Update to git: 34e27fe8

* Fri Apr 03 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.25.20150403git72735a1f
- Update to git: 72735a1f

* Thu Apr 02 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.24.20150402gitbe1ffedf
- Update to git: be1ffedf

* Wed Apr 01 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.23.20150401gitc85f1d6f
- Update to git: c85f1d6f

* Tue Mar 24 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.22.20150324git47963aec
- Update to git: 47963aec

* Mon Mar 23 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.21.20150323git707e889f
- Update to git: 707e889f

* Sat Mar 21 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.20.20150321gitb7f0472e
- Update to git: b7f0472e

* Fri Mar 20 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.19.20150320git3bacab35
- Update to git: 3bacab35

* Thu Mar 19 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.18.20150319gitc06f84a9
- Update to git: c06f84a9

* Wed Mar 18 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.17.20150318git18b1fc84
- Update to git: 18b1fc84

* Tue Mar 17 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.16.20150317git6023179e
- Update to git: 6023179e

* Mon Mar 16 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.15.20150316gitdfb27d14
- Update to git: dfb27d14

* Fri Mar 13 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.14.20150313git5a32a4d3
- Update to git: 5a32a4d3

* Thu Mar 12 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.13.20150312git554303b2
- Update to git: 554303b2

* Tue Mar 10 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.12.20150310gite5b1d4fd
- Update to git: e5b1d4fd

* Sun Mar 08 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.11.20150308git98df8386
- Update to git: 98df8386

* Sat Mar 07 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.10.20150307git8f69e31e
- Update to git: 8f69e31e

* Fri Mar 06 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.9.20150306git7fbde56a
- Update to git: 7fbde56a

* Tue Mar 03 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.8.20150303gitad0a129a
- Update to git: ad0a129a

* Fri Feb 27 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.7.20150227gitb2619544
- Update to git: b2619544

* Wed Feb 25 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.6.20150225git435d7b46
- Update to git: 435d7b46

* Thu Feb 12 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.5.20150212gitc1c638bd
- Update to git: c1c638bd

* Fri Feb 06 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.4.20150206git04c8dd36
- Update to git: 04c8dd36

* Mon Feb 02 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.3.20150202gita0b151cb
- Update to git: a0b151cb

* Fri Jan 30 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.2.20150130git311622bc
- Update to git: 311622bc

* Fri Jan 30 2015 Miro Hrončok <mhroncok@redhat.com> - 6.1.0-0.1.20150129git311622bc
- Synced the version with upstream
- Rebased pacthes

* Thu Jan 29 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.74.20150129git311622bc
- Update to git: 311622bc

* Fri Jan 23 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.73.20150123gite228bc05
- Update to git: e228bc05

* Sat Jan 17 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.72.20150117git01eb41cf
- Update to git: 01eb41cf

* Fri Jan 16 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.71.20150116git7bfeb3a5
- Update to git: 7bfeb3a5

* Wed Jan 07 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.70.20150107git52287cae
- Update to git: 52287cae

* Sun Jan 04 2015 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.69.20150104git28d7dce0
- Update to git: 28d7dce0

* Wed Dec 31 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.68.20141231git1503a218
- Update to git: 1503a218

* Tue Dec 30 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.67.20141230gite70c01f6
- Update to git: e70c01f6

* Mon Dec 29 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.66.20141229gitb88970fb
- Update to git: b88970fb

* Thu Dec 25 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.65.20141225git1927dfce
- Update to git: 1927dfce

* Wed Dec 24 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.64.20141224git4fbd8468
- Update to git: 4fbd8468

* Tue Dec 23 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.63.20141223git0fad8773
- Update to git: 0fad8773

* Sun Dec 21 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.62.20141221git89b8bb2a
- Update to git: 89b8bb2a

* Sat Dec 20 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.61.20141220git5addd1b7
- Update to git: 5addd1b7

* Fri Dec 19 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.60.20141219gitb1c3afe1
- Update to git: b1c3afe1

* Thu Dec 18 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.59.20141218gitf5a5eb27
- Update to git: f5a5eb27

* Wed Dec 17 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.58.20141217git7f4fa85c
- Update to git: 7f4fa85c

* Tue Dec 16 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.57.20141216git00ec8e63
- Update to git: 00ec8e63

* Mon Dec 15 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.56.20141215git8e11f761
- Update to git: 8e11f761

* Sun Dec 14 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.55.20141214gitbff1145f
- Update to git: bff1145f

* Sat Dec 13 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.54.20141213gitb73269e2
- Update to git: b73269e2

* Fri Dec 12 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.53.20141212git63884359
- Update to git: 63884359

* Thu Dec 11 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.52.20141211git09d8897b
- Update to git: 09d8897b

* Wed Dec 10 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.51.20141210gitd251fe55
- Update to git: d251fe55

* Tue Dec 09 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.50.20141209git73a18d09
- Update to git: 73a18d09

* Wed Dec 03 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.49.20141203git33ad03c6
- Update to git: 33ad03c6

* Tue Nov 25 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.48.20141125git0c2bf1ae
- Update to git: 0c2bf1ae

* Fri Nov 21 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.47.20141121git293c3131
- Update to git: 293c3131

* Wed Nov 12 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.46.20141112git043fe9f5
- Update to git: 043fe9f5

* Wed Nov 05 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.45.20141105git043af838
- Update to git: 043af838

* Mon Nov 03 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.44.20141103gitbc9efbd2
- Update to git: bc9efbd2

* Sat Oct 18 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.43.20141018gita2ab21d0
- Update to git: a2ab21d0

* Fri Oct 17 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.42.20141017gitf69851e1
- Update to git: f69851e1

* Fri Oct 10 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.41.20141010gitc72668f1
- Update to git: c72668f1

* Thu Oct 09 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.40.20141009gitf720d3d7
- Update to git: f720d3d7

* Tue Oct 07 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.39.20141007git0e390f1f
- Update to git: 0e390f1f

* Wed Oct 01 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.38.20141001git8be83cff
- Update to git: 8be83cff

* Tue Sep 30 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.37.20140930git38282342
- Update to git: 38282342

* Sat Sep 27 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.36.20140927git4411d86f
- Update to git: 4411d86f

* Fri Sep 26 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.35.20140926git3bb4cbdd
- Update to git: 3bb4cbdd

* Wed Sep 24 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.34.20140924gita684d9da
- Update to git: a684d9da

* Sat Sep 20 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.33.20140920git4c124273
- Update to git: 4c124273

* Fri Sep 19 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.32.20140919git7eff500a
- Update to git: 7eff500a

* Thu Sep 18 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.31.20140918git37f8a2f1
- Update to git: 37f8a2f1

* Sat Sep 13 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.30.20140913gitea3252e6
- Update to git: ea3252e6

* Fri Sep 12 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.29.20140912gitd62b10a3
- Update to git: d62b10a3

* Thu Sep 11 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.28.20140911git796320ab
- Update to git: 796320ab

* Mon Sep 01 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.27.20140901gite90b86fa
- Update to git: e90b86fa

* Sun Aug 31 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.26.20140831git0783bc17
- Update to git: 0783bc17

* Sun Aug 31 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.25.20140831git8f1cddb7
- Update to git: 8f1cddb7

* Fri Aug 29 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.24.20140829git673b7c31
- Update to git: 673b7c31

* Thu Aug 28 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.23.20140828git09a74c60
- Update to git: 09a74c60

* Tue Aug 26 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.22.20140826git3fa6f04e
- Update to git: 3fa6f04e

* Sat Aug 23 2014 Miro Hrončok <mhroncok@redhat.com> - 1.6-0.21.20140823git8b505a36
- Update to git: 8b505a36

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

