%if 0%{?fedora} || 0%{?rhel} == 6
%global with_devel 1
%global with_bundled 1
%global with_debug 1
%global with_check 1
%global with_unit_test 1
%else
%global with_devel 0
%global with_bundled 0
%global with_debug 0
%global with_check 0
%global with_unit_test 0
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
# https://bugzilla.redhat.com/show_bug.cgi?id=995136#c12
%if 0%{?with_debug}
%global _dwz_low_mem_die_limit 0
%else
%global debug_package   %{nil}
%endif

# https://fedoraproject.org/wiki/PackagingDrafts/Go#Debuginfo
%if ! 0%{?gobuild:1}
%define gobuild(o:) go build -ldflags "${LDFLAGS:-} -B 0x$(head -c20 /dev/urandom|od -An -tx1|tr -d ' \\n')" -a -v -x %{?**};
%endif

%global provider        github
%global provider_tld    com
%global project         skippbox
%global repo            kompose
# https://github.com/skippbox/kompose
%global provider_prefix %{provider}.%{provider_tld}/%{project}/%{repo}
%global import_path     %{provider_prefix}
%global commit          822768446621d71ffd02eafd138db0d8ab4a7d0e
%global shortcommit     %(c=%{commit}; echo ${c:0:7})

Name:           kompose
Version:        0.1.0
Release:        0.1.git%{shortcommit}%{?dist}
Summary:        Tool to move from `docker-compose` to Kubernetes
License:        Apache 2.0
URL:            https://%{provider_prefix}
Source0:        https://%{provider_prefix}/archive/%{commit}/%{repo}-%{shortcommit}.tar.gz

# e.g. el6 has ppc64 arch without gcc-go, so EA tag is required
ExclusiveArch:  %{?go_arches:%{go_arches}}%{!?go_arches:%{ix86} x86_64 %{arm}}
# If go_compiler is not set to 1, there is no virtual provide. Use golang instead.
BuildRequires:  %{?go_compiler:compiler(go-compiler)}%{!?go_compiler:golang}

%if ! 0%{?with_bundled}
# cli/main/main.go
BuildRequires: golang(github.com/urfave/cli)

# Remaining dependencies not included in main packages
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(github.com/docker/docker/api/client/bundlefile)
BuildRequires: golang(github.com/Sirupsen/logrus)
%endif

%description
%{summary}

%if 0%{?with_devel}
%package devel
Summary:       %{summary}
BuildArch:     noarch

%if 0%{?with_check} && ! 0%{?with_bundled}
# These buildrequires are only for our tests (check)
BuildRequires: golang(github.com/Sirupsen/logrus)
BuildRequires: golang(github.com/docker/docker/api/client/bundlefile)
BuildRequires: golang(github.com/docker/libcompose/config)
BuildRequires: golang(github.com/docker/libcompose/lookup)
BuildRequires: golang(github.com/docker/libcompose/project)
BuildRequires: golang(github.com/fatih/structs)
BuildRequires: golang(github.com/ghodss/yaml)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api)
BuildRequires: golang(github.com/openshift/origin/pkg/deploy/api/install)
BuildRequires: golang(github.com/urfave/cli)
BuildRequires: golang(k8s.io/kubernetes/pkg/api)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/api/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions)
BuildRequires: golang(k8s.io/kubernetes/pkg/apis/extensions/install)
BuildRequires: golang(k8s.io/kubernetes/pkg/client/unversioned)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl)
BuildRequires: golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
BuildRequires: golang(k8s.io/kubernetes/pkg/runtime)
BuildRequires: golang(k8s.io/kubernetes/pkg/util/intstr)
%endif

# devel subpackage requires. This is basically the source code from 
# all of the libraries that kompose imports during build.
Requires:      golang(github.com/Sirupsen/logrus)
Requires:      golang(github.com/docker/docker/api/client/bundlefile)
Requires:      golang(github.com/docker/libcompose/config)
Requires:      golang(github.com/docker/libcompose/lookup)
Requires:      golang(github.com/docker/libcompose/project)
Requires:      golang(github.com/fatih/structs)
Requires:      golang(github.com/ghodss/yaml)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api)
Requires:      golang(github.com/openshift/origin/pkg/deploy/api/install)
Requires:      golang(github.com/urfave/cli)
Requires:      golang(k8s.io/kubernetes/pkg/api)
Requires:      golang(k8s.io/kubernetes/pkg/api/install)
Requires:      golang(k8s.io/kubernetes/pkg/api/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions)
Requires:      golang(k8s.io/kubernetes/pkg/apis/extensions/install)
Requires:      golang(k8s.io/kubernetes/pkg/client/unversioned)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl)
Requires:      golang(k8s.io/kubernetes/pkg/kubectl/cmd/util)
Requires:      golang(k8s.io/kubernetes/pkg/runtime)
Requires:      golang(k8s.io/kubernetes/pkg/util/intstr)

# devel subpackage provides
Provides:      golang(%{import_path}/cli/app) = %{version}-%{release}
Provides:      golang(%{import_path}/cli/command) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/kobject) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/bundle) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/loader/compose) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/kubernetes) = %{version}-%{release}
Provides:      golang(%{import_path}/pkg/transformer/openshift) = %{version}-%{release}
Provides:      golang(%{import_path}/version) = %{version}-%{release}

%description devel
%{summary}

This package contains library source intended for
building other packages which use import path with
%{import_path} prefix.
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%package unit-test-devel
Summary:         Unit tests for %{name} package
%if 0%{?with_check}
#Here comes all BuildRequires: PACKAGE the unit tests
#in %%check section need for running
%endif

# test subpackage tests code from devel subpackage
Requires:        %{name}-devel = %{version}-%{release}

%if 0%{?with_check} && ! 0%{?with_bundled}
%endif


%description unit-test-devel
%{summary}

This package contains unit tests for project
providing packages with %{import_path} prefix.
%endif

%prep
%setup -q -n %{repo}-%{commit}

%build
# set up temporary build gopath
mkdir -p src/%{provider}.%{provider_tld}/%{project}
ln -s ../../../ src/%{import_path}

%if ! 0%{?with_bundled}
export GOPATH=$(pwd):%{gopath}
%else
export GOPATH=$(pwd):$(pwd)/vendor:%{gopath}
%endif

# define buildflags here. these were taken from script/.build
# we will need to periodically check these for consistentcy
%define buildflags -tags experimental -ldflags="-w -X github.com/skippbox/kompose/version.GITCOMMIT=%{shortcommit}"
%gobuild %{buildflags} -o bin/kompose %{import_path}/cli/main


%install
install -d -p %{buildroot}%{_bindir}
install -p -m 0755 bin/kompose %{buildroot}%{_bindir}

# source codes for building projects
%if 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
echo "%%dir %%{gopath}/src/%%{import_path}/." >> devel.file-list
# find all *.go but no *_test.go files and generate devel.file-list
for file in $(find . \( -iname "*.go" -or -iname "*.s" \) \! -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

# testing files for this project
%if 0%{?with_unit_test} && 0%{?with_devel}
install -d -p %{buildroot}/%{gopath}/src/%{import_path}/
# find all *_test.go files and generate unit-test-devel.file-list
for file in $(find . -iname "*_test.go" | grep -v "vendor") ; do
    dirprefix=$(dirname $file)
    install -d -p %{buildroot}/%{gopath}/src/%{import_path}/$dirprefix
    cp -pav $file %{buildroot}/%{gopath}/src/%{import_path}/$file
    echo "%%{gopath}/src/%%{import_path}/$file" >> unit-test-devel.file-list

    while [ "$dirprefix" != "." ]; do
        echo "%%dir %%{gopath}/src/%%{import_path}/$dirprefix" >> devel.file-list
        dirprefix=$(dirname $dirprefix)
    done
done
%endif

%if 0%{?with_devel}
sort -u -o devel.file-list devel.file-list
%endif

# Why does check need to use buildroot at all? 
%check
%if 0%{?with_check} && 0%{?with_unit_test} && 0%{?with_devel}
%if ! 0%{?with_bundled}
export GOPATH=%{buildroot}/%{gopath}:%{gopath}
%else
#export GOPATH=%{buildroot}/%{gopath}:$(pwd)/vendor:%{gopath}
#export GOPATH=%{buildroot}/%{gopath}:$(pwd):%{gopath}
export GOPATH=$(pwd):%{gopath}
%endif

# Not using %gotest as it doesn't allow us to define our own ldflags
# Since you can only define ldflags once and %gotest and %buildflags
# both try to define -ldflags
%if ! 0%{?gotest:1}
%global gotest go test
%endif

# define testflags here. these were taken from script/test-unit
# we will need to periodically check these for consistency
%define testflags -cover -coverprofile=cover.out
go test -compiler gc %{buildflags} %{testflags} %{import_path}/cli/app
go test -compiler gc %{buildflags} %{testflags} %{import_path}/pkg/transformer/kubernetes
%endif

#define license tag if not already defined
%{!?_licensedir:%global license %doc}

%files
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%{_bindir}/kompose

%if 0%{?with_devel}
%files devel -f devel.file-list
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%dir %{gopath}/src/%{provider}.%{provider_tld}/%{project}
%endif

%if 0%{?with_unit_test} && 0%{?with_devel}
%files unit-test-devel -f unit-test-devel.file-list
%license LICENSE
%doc CONTRIBUTING.md CHANGELOG.md RELEASE.md README.md code-of-conduct.md
%endif

%changelog
* Thu Sep 22 2016 dustymabe - 0.1.0-0.1.git8227684
- First package for Fedora
