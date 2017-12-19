Summary: Mellanox userland tools and scripts
Name: mlnx-tools
Version: 1.5.0
Release: 0%{?_dist}
License: GPLv2
Url: https://github.com/aron-silverton/mlnx-tools
Group: Applications/System
Source: https://github.com/aron-silverton/mlnx-tools/releases/download/v%{version}/%{name}-%{version}.tgz
BuildRoot: %{?build_root:%{build_root}}%{!?build_root:/var/tmp/%{name}}
Vendor: Mellanox Technologies
Requires: perl
Requires: python
%description
Mellanox userland tools and scripts

%prep
%setup -n %{name}-%{version}

%install

add_env()
{
	efile=$1
	evar=$2
	epath=$3

cat >> $efile << EOF
if ! echo \$${evar} | grep -q $epath ; then
	export $evar=$epath:\$$evar
fi

EOF
}

touch mlnx-tools-files
cd ofed_scripts/utils
mlnx_python_sitelib=%{python_sitelib}
if [ "$(echo %{_prefix} | sed -e 's@/@@g')" != "usr" ]; then
	mlnx_python_sitelib=$(echo %{python_sitelib} | sed -e 's@/usr@%{_prefix}@')
fi
python setup.py install -O1 --prefix=%{buildroot}%{_prefix} --install-lib=%{buildroot}${mlnx_python_sitelib}
cd -

install -D -m 0755 ofed_scripts/cma_roce_mode %{buildroot}%{_sbindir}/cma_roce_mode
install -D -m 0755 ofed_scripts/ibdev2netdev %{buildroot}%{_bindir}/ibdev2netdev
install -D -m 0755 ofed_scripts/show_gids %{buildroot}%{_sbindir}/show_gids
install -D -m 0755 roce_config.sh %{buildroot}%{_bindir}/roce_config

if [ "$(echo %{_prefix} | sed -e 's@/@@g')" != "usr" ]; then
	conf_env=/etc/profile.d/mlnx-tools.sh
	install -d %{buildroot}/etc/profile.d
	add_env %{buildroot}$conf_env PYTHONPATH $mlnx_python_sitelib
	add_env %{buildroot}$conf_env PATH %{_bindir}
	add_env %{buildroot}$conf_env PATH %{_sbindir}
	echo $conf_env >> mlnx-tools-files
fi
find %{buildroot}${mlnx_python_sitelib} -type f -print | sed -e 's@%{buildroot}@@' >> mlnx-tools-files

%clean
rm -rf %{buildroot}

%files -f mlnx-tools-files
%defattr(-,root,root,-)
%{_sbindir}/*
%{_bindir}/*

%changelog
* Tue Dec 19 2017 Aron Silverton <aron.silverton@mellanox.com> - 1.5.0-0
- [Orabug: 27284449] Add Oracle copyright and remove Mellanox copyright
  from spec file

* Wed Nov 1 2017 Vladimir Sokolovsky <vlad@mellanox.com>
- Initial packaging

