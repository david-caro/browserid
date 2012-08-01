%define _rootdir /opt/browserid

Name:          browserid-server
Version:       %{ver}
Release:       %{rel}
Summary:       BrowserID server
Packager:      Pete Fritchman <petef@mozilla.com>
Group:         Development/Libraries
License:       MPL 2.0
URL:           https://github.com/mozilla/browserid
Source0:       %{name}.tar.gz
BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root
AutoReqProv:   no
Requires:      openssl nodejs
BuildRequires: gcc-c++ git jre make npm openssl-devel expat-devel

%description
Persona server & web home for persona.org

%prep
%setup -q -c -n browserid

%build
npm install
export PATH=$PWD/node_modules/.bin:$PATH
## Locales are optional
[[ -d locale ]] \
&& {
    ./locale/compile-mo.sh locale/
    ./locale/compile-json.sh locale/ resources/static/i18n/
    echo "locale svn r%{localerev}" >> resources/static/ver.txt
}
env CONFIG_FILES=$PWD/config/l10n-all.json scripts/compress
rm -r resources/static/build resources/static/test
echo "$GIT_REVISION" > resources/static/ver.txt
exit 0

%install
rm -rf %{buildroot}
mkdir -p %{buildroot}%{_rootdir}
for folder in bin lib locale node_modules resources scripts *.json; do
    [[ -d $folder ]] && cp -rp $folder %{buildroot}%{_rootdir}/
done
for folder in /etc/init.d %{_rootdir}/config; do
    mkdir -p %{buildroot}$folder
done
cp -p config/l10n-all.json %{buildroot}%{_rootdir}/config
cp -p config/l10n-prod.json %{buildroot}%{_rootdir}/config
cp -p config/browserid %{buildroot}/etc/init.d/
exit 0

%clean
rm -rf %{buildroot}
exit 0

%files
%defattr(-,root,root,-)
%{_rootdir}
%attr(775,root,root,-) /etc/init.d/browserid

%changelog
* Thu Aug 1  2012 David Caro <david.caro.estevez@gmail.com>
- Added init script
* Thu Jun 20 2012 David Caro <david.caro.estevez@gmail.com>
- locales are optional
- using a full version string
* Tue Oct 18 2011 Pete Fritchman <petef@mozilla.com>
- Initial version
