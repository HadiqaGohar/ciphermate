Creating service 
Creating service
Completed
Creating Cloud Build trigger
Completed
Building and deploying from repository (see logs)
Failed. Details: Build failed; check build logs for details
Creating revision
Failed. Details: The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout. This can happen when the container port is misconfigured or if the timeout is too short. The health check timeout can be extended. Logs for this revision might contain more information. Logs URL: Open Cloud Logging  For more troubleshooting guidance, see https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start 
Routing traffic
Cancelled 
 Failed: 7ae5d9f0-73e3-4d8d-9d4b-754b67307612
Started on Apr 6, 2026, 8:20:06 PM

Trigger
cloudrun-cipheremate-europe-west1-HadiqaGohar-ciphermate-muzh
Source
HadiqaGohar/ciphermate 
Branch
main
Commit
763836d 
Steps
Duration
Build Summary
4 Steps
00:08:22
0: Pull
/bin/bash -c docker pull europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:latest || exit 0
00:00:02
1: Build
build --cache-from europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:latest -t europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:763836dd0e0a6849bacc726feb63cb84b20078c0 -t europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:latest backend -f backend/Dockerfile
00:03:10
2: Push
push --all-tags europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate
00:02:22
3: Deploy
gcloud run services update cipheremate --image=europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:763836dd0e0a6849bacc726feb63cb84b20078c0 --update-labels=managed-by=gcp-cloud-build-deploy-cloud-run,gcb-trigger-id=f01eb568-1a4e-4f32-ba13-93862a957f9a,gcb-trigger-region=europe-west1,commit-sha=763836dd0e0a6849bacc726feb63cb84b20078c0,gcb-build-id=7ae5d9f0-73e3-4d8d-9d4b-754b67307612 --region=europe-west1 --quiet
00:02:32
Build Summary
Build log
Execution details
Build artifacts
Log viewer toolbar
When enabled, log entries which do not fit on one line wrap to the next line.
When enabled, log entries appear in reverse chronological order.
When enabled, log entries are shown with timestamps.
starting build "7ae5d9f0-73e3-4d8d-9d4b-754b67307612"
FETCHSOURCE
From https://github.com/HadiqaGohar/ciphermate
 * branch            763836dd0e0a6849bacc726feb63cb84b20078c0 -> FETCH_HEAD
HEAD is now at 763836d first commit.
GitCommit:
763836dd0e0a6849bacc726feb63cb84b20078c0
BUILD
Starting Step #0 - "Pull"
Already have image (with digest): gcr.io/cloud-builders/docker
Error response from daemon: manifest for europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:latest not found: manifest unknown: Failed to fetch "latest"
Finished Step #0 - "Pull"
Starting Step #1 - "Build"
Already have image (with digest): gcr.io/cloud-builders/docker
Sending build context to Docker daemon   1.42MB
Step 1/14 : FROM python:3.11-slim
3.11-slim: Pulling from library/python
ec781dee3f47: Already exists
6944007a5b45: Pulling fs layer
e35b92e2619d: Pulling fs layer
7524aba74b8c: Pulling fs layer
7524aba74b8c: Verifying Checksum
7524aba74b8c: Download complete
6944007a5b45: Download complete
e35b92e2619d: Verifying Checksum
e35b92e2619d: Download complete
6944007a5b45: Pull complete
e35b92e2619d: Pull complete
7524aba74b8c: Pull complete
Digest: sha256:9358444059ed78e2975ada2c189f1c1a3144a5dab6f35bff8c981afb38946634
Status: Downloaded newer image for python:3.11-slim
 ---> e67db9b14d09
Step 2/14 : ENV PYTHONUNBUFFERED=1
 ---> Running in 75bd64952f18
Removing intermediate container 75bd64952f18
 ---> 320d67997c50
Step 3/14 : ENV PYTHONDONTWRITEBYTECODE=1
 ---> Running in f62d0a4c9579
Removing intermediate container f62d0a4c9579
 ---> 90794bf28fc9
Step 4/14 : ENV PORT=8080
 ---> Running in 88b56afceaac
Removing intermediate container 88b56afceaac
 ---> 94c5f155f226
Step 5/14 : WORKDIR /app
 ---> Running in fb258a46617d
Removing intermediate container fb258a46617d
 ---> 3425240569f0
Step 6/14 : RUN apt-get update && apt-get install -y     gcc     libpq-dev     && rm -rf /var/lib/apt/lists/*     && apt-get clean
 ---> Running in ee0d39d4d917
Hit:1 http://deb.debian.org/debian trixie InRelease
Get:2 http://deb.debian.org/debian trixie-updates InRelease [47.3 kB]
Get:3 http://deb.debian.org/debian-security trixie-security InRelease [43.4 kB]
Get:4 http://deb.debian.org/debian trixie/main amd64 Packages [9671 kB]
Get:5 http://deb.debian.org/debian trixie-updates/main amd64 Packages [5412 B]
Get:6 http://deb.debian.org/debian-security trixie-security/main amd64 Packages [119 kB]
Fetched 9886 kB in 1s (6851 kB/s)
Reading package lists...
Reading package lists...
Building dependency tree...
Reading state information...
The following additional packages will be installed:
  binutils binutils-common binutils-x86-64-linux-gnu cpp cpp-14
  cpp-14-x86-64-linux-gnu cpp-x86-64-linux-gnu gcc-14 gcc-14-x86-64-linux-gnu
  gcc-x86-64-linux-gnu krb5-locales libasan8 libatomic1 libbinutils
  libc-dev-bin libc6-dev libcc1-0 libcom-err2 libcrypt-dev libctf-nobfd0
  libctf0 libgcc-14-dev libgomp1 libgprofng0 libgssapi-krb5-2 libhwasan0
  libisl23 libitm1 libjansson4 libk5crypto3 libkeyutils1 libkrb5-3
  libkrb5support0 libldap-common libldap2 liblsan0 libmpc3 libmpfr6 libpq5
  libquadmath0 libsasl2-2 libsasl2-modules libsasl2-modules-db libsframe1
  libssl-dev libtsan2 libubsan1 linux-libc-dev manpages manpages-dev
  rpcsvc-proto
Suggested packages:
  binutils-doc gprofng-gui binutils-gold cpp-doc gcc-14-locales cpp-14-doc
  gcc-multilib make autoconf automake libtool flex bison gdb gcc-doc
  gcc-14-multilib gcc-14-doc gdb-x86-64-linux-gnu libc-devtools glibc-doc
  krb5-doc krb5-user postgresql-doc-17 libsasl2-modules-gssapi-mit
  | libsasl2-modules-gssapi-heimdal libsasl2-modules-ldap libsasl2-modules-otp
  libsasl2-modules-sql libssl-doc man-browser
The following NEW packages will be installed:
  binutils binutils-common binutils-x86-64-linux-gnu cpp cpp-14
  cpp-14-x86-64-linux-gnu cpp-x86-64-linux-gnu gcc gcc-14
  gcc-14-x86-64-linux-gnu gcc-x86-64-linux-gnu krb5-locales libasan8
  libatomic1 libbinutils libc-dev-bin libc6-dev libcc1-0 libcom-err2
  libcrypt-dev libctf-nobfd0 libctf0 libgcc-14-dev libgomp1 libgprofng0
  libgssapi-krb5-2 libhwasan0 libisl23 libitm1 libjansson4 libk5crypto3
  libkeyutils1 libkrb5-3 libkrb5support0 libldap-common libldap2 liblsan0
  libmpc3 libmpfr6 libpq-dev libpq5 libquadmath0 libsasl2-2 libsasl2-modules
  libsasl2-modules-db libsframe1 libssl-dev libtsan2 libubsan1 linux-libc-dev
  manpages manpages-dev rpcsvc-proto
0 upgraded, 53 newly installed, 0 to remove and 0 not upgraded.
Need to get 64.8 MB of archives.
After this operation, 244 MB of additional disk space will be used.
Get:1 http://deb.debian.org/debian trixie/main amd64 krb5-locales all 1.21.3-5 [101 kB]
Get:2 http://deb.debian.org/debian trixie/main amd64 manpages all 6.9.1-1 [1393 kB]
Get:3 http://deb.debian.org/debian trixie/main amd64 libsframe1 amd64 2.44-3 [78.4 kB]
Get:4 http://deb.debian.org/debian trixie/main amd64 binutils-common amd64 2.44-3 [2509 kB]
Get:5 http://deb.debian.org/debian trixie/main amd64 libbinutils amd64 2.44-3 [534 kB]
Get:6 http://deb.debian.org/debian trixie/main amd64 libgprofng0 amd64 2.44-3 [808 kB]
Get:7 http://deb.debian.org/debian trixie/main amd64 libctf-nobfd0 amd64 2.44-3 [156 kB]
Get:8 http://deb.debian.org/debian trixie/main amd64 libctf0 amd64 2.44-3 [88.6 kB]
Get:9 http://deb.debian.org/debian trixie/main amd64 libjansson4 amd64 2.14-2+b3 [39.8 kB]
Get:10 http://deb.debian.org/debian trixie/main amd64 binutils-x86-64-linux-gnu amd64 2.44-3 [1014 kB]
Get:11 http://deb.debian.org/debian trixie/main amd64 binutils amd64 2.44-3 [265 kB]
Get:12 http://deb.debian.org/debian trixie/main amd64 libisl23 amd64 0.27-1 [659 kB]
Get:13 http://deb.debian.org/debian trixie/main amd64 libmpfr6 amd64 4.2.2-1 [729 kB]
Get:14 http://deb.debian.org/debian trixie/main amd64 libmpc3 amd64 1.3.1-1+b3 [52.2 kB]
Get:15 http://deb.debian.org/debian trixie/main amd64 cpp-14-x86-64-linux-gnu amd64 14.2.0-19 [11.0 MB]
Get:16 http://deb.debian.org/debian trixie/main amd64 cpp-14 amd64 14.2.0-19 [1280 B]
Get:17 http://deb.debian.org/debian trixie/main amd64 cpp-x86-64-linux-gnu amd64 4:14.2.0-1 [4840 B]
Get:18 http://deb.debian.org/debian trixie/main amd64 cpp amd64 4:14.2.0-1 [1568 B]
Get:19 http://deb.debian.org/debian trixie/main amd64 libcc1-0 amd64 14.2.0-19 [42.8 kB]
Get:20 http://deb.debian.org/debian trixie/main amd64 libgomp1 amd64 14.2.0-19 [137 kB]
Get:21 http://deb.debian.org/debian trixie/main amd64 libitm1 amd64 14.2.0-19 [26.0 kB]
Get:22 http://deb.debian.org/debian trixie/main amd64 libatomic1 amd64 14.2.0-19 [9308 B]
Get:23 http://deb.debian.org/debian trixie/main amd64 libasan8 amd64 14.2.0-19 [2725 kB]
Get:24 http://deb.debian.org/debian trixie/main amd64 liblsan0 amd64 14.2.0-19 [1204 kB]
Get:25 http://deb.debian.org/debian trixie/main amd64 libtsan2 amd64 14.2.0-19 [2460 kB]
Get:26 http://deb.debian.org/debian trixie/main amd64 libubsan1 amd64 14.2.0-19 [1074 kB]
Get:27 http://deb.debian.org/debian trixie/main amd64 libhwasan0 amd64 14.2.0-19 [1488 kB]
Get:28 http://deb.debian.org/debian trixie/main amd64 libquadmath0 amd64 14.2.0-19 [145 kB]
Get:29 http://deb.debian.org/debian trixie/main amd64 libgcc-14-dev amd64 14.2.0-19 [2672 kB]
Get:30 http://deb.debian.org/debian trixie/main amd64 gcc-14-x86-64-linux-gnu amd64 14.2.0-19 [21.4 MB]
Get:31 http://deb.debian.org/debian trixie/main amd64 gcc-14 amd64 14.2.0-19 [540 kB]
Get:32 http://deb.debian.org/debian trixie/main amd64 gcc-x86-64-linux-gnu amd64 4:14.2.0-1 [1436 B]
Get:33 http://deb.debian.org/debian trixie/main amd64 gcc amd64 4:14.2.0-1 [5136 B]
Get:34 http://deb.debian.org/debian trixie/main amd64 libc-dev-bin amd64 2.41-12+deb13u2 [59.4 kB]
Get:35 http://deb.debian.org/debian-security trixie-security/main amd64 linux-libc-dev all 6.12.74-2 [2746 kB]
Get:36 http://deb.debian.org/debian trixie/main amd64 libcrypt-dev amd64 1:4.4.38-1 [119 kB]
Get:37 http://deb.debian.org/debian trixie/main amd64 rpcsvc-proto amd64 1.4.3-1 [63.3 kB]
Get:38 http://deb.debian.org/debian trixie/main amd64 libc6-dev amd64 2.41-12+deb13u2 [1996 kB]
Get:39 http://deb.debian.org/debian trixie/main amd64 libcom-err2 amd64 1.47.2-3+b10 [25.0 kB]
Get:40 http://deb.debian.org/debian trixie/main amd64 libkrb5support0 amd64 1.21.3-5 [33.0 kB]
Get:41 http://deb.debian.org/debian trixie/main amd64 libk5crypto3 amd64 1.21.3-5 [81.5 kB]
Get:42 http://deb.debian.org/debian trixie/main amd64 libkeyutils1 amd64 1.6.3-6 [9456 B]
Get:43 http://deb.debian.org/debian trixie/main amd64 libkrb5-3 amd64 1.21.3-5 [326 kB]
Get:44 http://deb.debian.org/debian trixie/main amd64 libgssapi-krb5-2 amd64 1.21.3-5 [138 kB]
Get:45 http://deb.debian.org/debian trixie/main amd64 libldap-common all 2.6.10+dfsg-1 [35.1 kB]
Get:46 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules-db amd64 2.1.28+dfsg1-9 [19.8 kB]
Get:47 http://deb.debian.org/debian trixie/main amd64 libsasl2-2 amd64 2.1.28+dfsg1-9 [57.5 kB]
Get:48 http://deb.debian.org/debian trixie/main amd64 libldap2 amd64 2.6.10+dfsg-1 [194 kB]
Get:49 http://deb.debian.org/debian trixie/main amd64 libpq5 amd64 17.9-0+deb13u1 [228 kB]
Get:50 http://deb.debian.org/debian trixie/main amd64 libssl-dev amd64 3.5.5-1~deb13u1 [2953 kB]
Get:51 http://deb.debian.org/debian trixie/main amd64 libpq-dev amd64 17.9-0+deb13u1 [152 kB]
Get:52 http://deb.debian.org/debian trixie/main amd64 libsasl2-modules amd64 2.1.28+dfsg1-9 [66.7 kB]
Get:53 http://deb.debian.org/debian trixie/main amd64 manpages-dev all 6.9.1-1 [2122 kB]
debconf: unable to initialize frontend: Dialog
debconf: (TERM is not set, so the dialog frontend is not usable.)
debconf: falling back to frontend: Readline
debconf: unable to initialize frontend: Readline
debconf: (Can't locate Term/ReadLine.pm in @INC (you may need to install the Term::ReadLine module) (@INC entries checked: /etc/perl /usr/local/lib/x86_64-linux-gnu/perl/5.40.1 /usr/local/share/perl/5.40.1 /usr/lib/x86_64-linux-gnu/perl5/5.40 /usr/share/perl5 /usr/lib/x86_64-linux-gnu/perl-base /usr/lib/x86_64-linux-gnu/perl/5.40 /usr/share/perl/5.40 /usr/local/lib/site_perl) at /usr/share/perl5/Debconf/FrontEnd/Readline.pm line 8, <STDIN> line 53.)
debconf: falling back to frontend: Teletype
debconf: unable to initialize frontend: Teletype
debconf: (This frontend requires a controlling tty.)
debconf: falling back to frontend: Noninteractive
Fetched 64.8 MB in 1s (108 MB/s)
Selecting previously unselected package krb5-locales.
(Reading database ... (Reading database ... 5%(Reading database ... 10%(Reading database ... 15%(Reading database ... 20%(Reading database ... 25%(Reading database ... 30%(Reading database ... 35%(Reading database ... 40%(Reading database ... 45%(Reading database ... 50%(Reading database ... 55%(Reading database ... 60%(Reading database ... 65%(Reading database ... 70%(Reading database ... 75%(Reading database ... 80%(Reading database ... 85%(Reading database ... 90%(Reading database ... 95%(Reading database ... 100%(Reading database ... 5645 files and directories currently installed.)
Preparing to unpack .../00-krb5-locales_1.21.3-5_all.deb ...
Unpacking krb5-locales (1.21.3-5) ...
Selecting previously unselected package manpages.
Preparing to unpack .../01-manpages_6.9.1-1_all.deb ...
Unpacking manpages (6.9.1-1) ...
Selecting previously unselected package libsframe1:amd64.
Preparing to unpack .../02-libsframe1_2.44-3_amd64.deb ...
Unpacking libsframe1:amd64 (2.44-3) ...
Selecting previously unselected package binutils-common:amd64.
Preparing to unpack .../03-binutils-common_2.44-3_amd64.deb ...
Unpacking binutils-common:amd64 (2.44-3) ...
Selecting previously unselected package libbinutils:amd64.
Preparing to unpack .../04-libbinutils_2.44-3_amd64.deb ...
Unpacking libbinutils:amd64 (2.44-3) ...
Selecting previously unselected package libgprofng0:amd64.
Preparing to unpack .../05-libgprofng0_2.44-3_amd64.deb ...
Unpacking libgprofng0:amd64 (2.44-3) ...
Selecting previously unselected package libctf-nobfd0:amd64.
Preparing to unpack .../06-libctf-nobfd0_2.44-3_amd64.deb ...
Unpacking libctf-nobfd0:amd64 (2.44-3) ...
Selecting previously unselected package libctf0:amd64.
Preparing to unpack .../07-libctf0_2.44-3_amd64.deb ...
Unpacking libctf0:amd64 (2.44-3) ...
Selecting previously unselected package libjansson4:amd64.
Preparing to unpack .../08-libjansson4_2.14-2+b3_amd64.deb ...
Unpacking libjansson4:amd64 (2.14-2+b3) ...
Selecting previously unselected package binutils-x86-64-linux-gnu.
Preparing to unpack .../09-binutils-x86-64-linux-gnu_2.44-3_amd64.deb ...
Unpacking binutils-x86-64-linux-gnu (2.44-3) ...
Selecting previously unselected package binutils.
Preparing to unpack .../10-binutils_2.44-3_amd64.deb ...
Unpacking binutils (2.44-3) ...
Selecting previously unselected package libisl23:amd64.
Preparing to unpack .../11-libisl23_0.27-1_amd64.deb ...
Unpacking libisl23:amd64 (0.27-1) ...
Selecting previously unselected package libmpfr6:amd64.
Preparing to unpack .../12-libmpfr6_4.2.2-1_amd64.deb ...
Unpacking libmpfr6:amd64 (4.2.2-1) ...
Selecting previously unselected package libmpc3:amd64.
Preparing to unpack .../13-libmpc3_1.3.1-1+b3_amd64.deb ...
Unpacking libmpc3:amd64 (1.3.1-1+b3) ...
Selecting previously unselected package cpp-14-x86-64-linux-gnu.
Preparing to unpack .../14-cpp-14-x86-64-linux-gnu_14.2.0-19_amd64.deb ...
Unpacking cpp-14-x86-64-linux-gnu (14.2.0-19) ...
Selecting previously unselected package cpp-14.
Preparing to unpack .../15-cpp-14_14.2.0-19_amd64.deb ...
Unpacking cpp-14 (14.2.0-19) ...
Selecting previously unselected package cpp-x86-64-linux-gnu.
Preparing to unpack .../16-cpp-x86-64-linux-gnu_4%3a14.2.0-1_amd64.deb ...
Unpacking cpp-x86-64-linux-gnu (4:14.2.0-1) ...
Selecting previously unselected package cpp.
Preparing to unpack .../17-cpp_4%3a14.2.0-1_amd64.deb ...
Unpacking cpp (4:14.2.0-1) ...
Selecting previously unselected package libcc1-0:amd64.
Preparing to unpack .../18-libcc1-0_14.2.0-19_amd64.deb ...
Unpacking libcc1-0:amd64 (14.2.0-19) ...
Selecting previously unselected package libgomp1:amd64.
Preparing to unpack .../19-libgomp1_14.2.0-19_amd64.deb ...
Unpacking libgomp1:amd64 (14.2.0-19) ...
Selecting previously unselected package libitm1:amd64.
Preparing to unpack .../20-libitm1_14.2.0-19_amd64.deb ...
Unpacking libitm1:amd64 (14.2.0-19) ...
Selecting previously unselected package libatomic1:amd64.
Preparing to unpack .../21-libatomic1_14.2.0-19_amd64.deb ...
Unpacking libatomic1:amd64 (14.2.0-19) ...
Selecting previously unselected package libasan8:amd64.
Preparing to unpack .../22-libasan8_14.2.0-19_amd64.deb ...
Unpacking libasan8:amd64 (14.2.0-19) ...
Selecting previously unselected package liblsan0:amd64.
Preparing to unpack .../23-liblsan0_14.2.0-19_amd64.deb ...
Unpacking liblsan0:amd64 (14.2.0-19) ...
Selecting previously unselected package libtsan2:amd64.
Preparing to unpack .../24-libtsan2_14.2.0-19_amd64.deb ...
Unpacking libtsan2:amd64 (14.2.0-19) ...
Selecting previously unselected package libubsan1:amd64.
Preparing to unpack .../25-libubsan1_14.2.0-19_amd64.deb ...
Unpacking libubsan1:amd64 (14.2.0-19) ...
Selecting previously unselected package libhwasan0:amd64.
Preparing to unpack .../26-libhwasan0_14.2.0-19_amd64.deb ...
Unpacking libhwasan0:amd64 (14.2.0-19) ...
Selecting previously unselected package libquadmath0:amd64.
Preparing to unpack .../27-libquadmath0_14.2.0-19_amd64.deb ...
Unpacking libquadmath0:amd64 (14.2.0-19) ...
Selecting previously unselected package libgcc-14-dev:amd64.
Preparing to unpack .../28-libgcc-14-dev_14.2.0-19_amd64.deb ...
Unpacking libgcc-14-dev:amd64 (14.2.0-19) ...
Selecting previously unselected package gcc-14-x86-64-linux-gnu.
Preparing to unpack .../29-gcc-14-x86-64-linux-gnu_14.2.0-19_amd64.deb ...
Unpacking gcc-14-x86-64-linux-gnu (14.2.0-19) ...
Selecting previously unselected package gcc-14.
Preparing to unpack .../30-gcc-14_14.2.0-19_amd64.deb ...
Unpacking gcc-14 (14.2.0-19) ...
Selecting previously unselected package gcc-x86-64-linux-gnu.
Preparing to unpack .../31-gcc-x86-64-linux-gnu_4%3a14.2.0-1_amd64.deb ...
Unpacking gcc-x86-64-linux-gnu (4:14.2.0-1) ...
Selecting previously unselected package gcc.
Preparing to unpack .../32-gcc_4%3a14.2.0-1_amd64.deb ...
Unpacking gcc (4:14.2.0-1) ...
Selecting previously unselected package libc-dev-bin.
Preparing to unpack .../33-libc-dev-bin_2.41-12+deb13u2_amd64.deb ...
Unpacking libc-dev-bin (2.41-12+deb13u2) ...
Selecting previously unselected package linux-libc-dev.
Preparing to unpack .../34-linux-libc-dev_6.12.74-2_all.deb ...
Unpacking linux-libc-dev (6.12.74-2) ...
Selecting previously unselected package libcrypt-dev:amd64.
Preparing to unpack .../35-libcrypt-dev_1%3a4.4.38-1_amd64.deb ...
Unpacking libcrypt-dev:amd64 (1:4.4.38-1) ...
Selecting previously unselected package rpcsvc-proto.
Preparing to unpack .../36-rpcsvc-proto_1.4.3-1_amd64.deb ...
Unpacking rpcsvc-proto (1.4.3-1) ...
Selecting previously unselected package libc6-dev:amd64.
Preparing to unpack .../37-libc6-dev_2.41-12+deb13u2_amd64.deb ...
Unpacking libc6-dev:amd64 (2.41-12+deb13u2) ...
Selecting previously unselected package libcom-err2:amd64.
Preparing to unpack .../38-libcom-err2_1.47.2-3+b10_amd64.deb ...
Unpacking libcom-err2:amd64 (1.47.2-3+b10) ...
Selecting previously unselected package libkrb5support0:amd64.
Preparing to unpack .../39-libkrb5support0_1.21.3-5_amd64.deb ...
Unpacking libkrb5support0:amd64 (1.21.3-5) ...
Selecting previously unselected package libk5crypto3:amd64.
Preparing to unpack .../40-libk5crypto3_1.21.3-5_amd64.deb ...
Unpacking libk5crypto3:amd64 (1.21.3-5) ...
Selecting previously unselected package libkeyutils1:amd64.
Preparing to unpack .../41-libkeyutils1_1.6.3-6_amd64.deb ...
Unpacking libkeyutils1:amd64 (1.6.3-6) ...
Selecting previously unselected package libkrb5-3:amd64.
Preparing to unpack .../42-libkrb5-3_1.21.3-5_amd64.deb ...
Unpacking libkrb5-3:amd64 (1.21.3-5) ...
Selecting previously unselected package libgssapi-krb5-2:amd64.
Preparing to unpack .../43-libgssapi-krb5-2_1.21.3-5_amd64.deb ...
Unpacking libgssapi-krb5-2:amd64 (1.21.3-5) ...
Selecting previously unselected package libldap-common.
Preparing to unpack .../44-libldap-common_2.6.10+dfsg-1_all.deb ...
Unpacking libldap-common (2.6.10+dfsg-1) ...
Selecting previously unselected package libsasl2-modules-db:amd64.
Preparing to unpack .../45-libsasl2-modules-db_2.1.28+dfsg1-9_amd64.deb ...
Unpacking libsasl2-modules-db:amd64 (2.1.28+dfsg1-9) ...
Selecting previously unselected package libsasl2-2:amd64.
Preparing to unpack .../46-libsasl2-2_2.1.28+dfsg1-9_amd64.deb ...
Unpacking libsasl2-2:amd64 (2.1.28+dfsg1-9) ...
Selecting previously unselected package libldap2:amd64.
Preparing to unpack .../47-libldap2_2.6.10+dfsg-1_amd64.deb ...
Unpacking libldap2:amd64 (2.6.10+dfsg-1) ...
Selecting previously unselected package libpq5:amd64.
Preparing to unpack .../48-libpq5_17.9-0+deb13u1_amd64.deb ...
Unpacking libpq5:amd64 (17.9-0+deb13u1) ...
Selecting previously unselected package libssl-dev:amd64.
Preparing to unpack .../49-libssl-dev_3.5.5-1~deb13u1_amd64.deb ...
Unpacking libssl-dev:amd64 (3.5.5-1~deb13u1) ...
Selecting previously unselected package libpq-dev.
Preparing to unpack .../50-libpq-dev_17.9-0+deb13u1_amd64.deb ...
Unpacking libpq-dev (17.9-0+deb13u1) ...
Selecting previously unselected package libsasl2-modules:amd64.
Preparing to unpack .../51-libsasl2-modules_2.1.28+dfsg1-9_amd64.deb ...
Unpacking libsasl2-modules:amd64 (2.1.28+dfsg1-9) ...
Selecting previously unselected package manpages-dev.
Preparing to unpack .../52-manpages-dev_6.9.1-1_all.deb ...
Unpacking manpages-dev (6.9.1-1) ...
Setting up libkeyutils1:amd64 (1.6.3-6) ...
Setting up manpages (6.9.1-1) ...
Setting up libsasl2-modules:amd64 (2.1.28+dfsg1-9) ...
Setting up binutils-common:amd64 (2.44-3) ...
Setting up linux-libc-dev (6.12.74-2) ...
Setting up libctf-nobfd0:amd64 (2.44-3) ...
Setting up krb5-locales (1.21.3-5) ...
Setting up libcom-err2:amd64 (1.47.2-3+b10) ...
Setting up libgomp1:amd64 (14.2.0-19) ...
Setting up libldap-common (2.6.10+dfsg-1) ...
Setting up libsframe1:amd64 (2.44-3) ...
Setting up libjansson4:amd64 (2.14-2+b3) ...
Setting up libkrb5support0:amd64 (1.21.3-5) ...
Setting up libsasl2-modules-db:amd64 (2.1.28+dfsg1-9) ...
Setting up rpcsvc-proto (1.4.3-1) ...
Setting up libmpfr6:amd64 (4.2.2-1) ...
Setting up libquadmath0:amd64 (14.2.0-19) ...
Setting up libssl-dev:amd64 (3.5.5-1~deb13u1) ...
Setting up libmpc3:amd64 (1.3.1-1+b3) ...
Setting up libatomic1:amd64 (14.2.0-19) ...
Setting up libk5crypto3:amd64 (1.21.3-5) ...
Setting up libsasl2-2:amd64 (2.1.28+dfsg1-9) ...
Setting up libubsan1:amd64 (14.2.0-19) ...
Setting up libhwasan0:amd64 (14.2.0-19) ...
Setting up libcrypt-dev:amd64 (1:4.4.38-1) ...
Setting up libasan8:amd64 (14.2.0-19) ...
Setting up libkrb5-3:amd64 (1.21.3-5) ...
Setting up libtsan2:amd64 (14.2.0-19) ...
Setting up libbinutils:amd64 (2.44-3) ...
Setting up libisl23:amd64 (0.27-1) ...
Setting up libc-dev-bin (2.41-12+deb13u2) ...
Setting up libcc1-0:amd64 (14.2.0-19) ...
Setting up libldap2:amd64 (2.6.10+dfsg-1) ...
Setting up liblsan0:amd64 (14.2.0-19) ...
Setting up libitm1:amd64 (14.2.0-19) ...
Setting up libctf0:amd64 (2.44-3) ...
Setting up manpages-dev (6.9.1-1) ...
Setting up libgprofng0:amd64 (2.44-3) ...
Setting up libgssapi-krb5-2:amd64 (1.21.3-5) ...
Setting up cpp-14-x86-64-linux-gnu (14.2.0-19) ...
Setting up cpp-14 (14.2.0-19) ...
Setting up libc6-dev:amd64 (2.41-12+deb13u2) ...
Setting up libgcc-14-dev:amd64 (14.2.0-19) ...
Setting up binutils-x86-64-linux-gnu (2.44-3) ...
Setting up cpp-x86-64-linux-gnu (4:14.2.0-1) ...
Setting up libpq5:amd64 (17.9-0+deb13u1) ...
Setting up libpq-dev (17.9-0+deb13u1) ...
Setting up binutils (2.44-3) ...
Setting up cpp (4:14.2.0-1) ...
Setting up gcc-14-x86-64-linux-gnu (14.2.0-19) ...
Setting up gcc-x86-64-linux-gnu (4:14.2.0-1) ...
Setting up gcc-14 (14.2.0-19) ...
Setting up gcc (4:14.2.0-1) ...
Processing triggers for libc-bin (2.41-12+deb13u2) ...
Removing intermediate container ee0d39d4d917
 ---> d9638098d266
Step 7/14 : COPY requirements.txt ./
 ---> 49a0375bb2a5
Step 8/14 : RUN pip install --no-cache-dir --upgrade pip     && pip install --no-cache-dir -r requirements.txt
 ---> Running in 068ad31a25a5
Requirement already satisfied: pip in /usr/local/lib/python3.11/site-packages (24.0)
Collecting pip
  Downloading pip-26.0.1-py3-none-any.whl.metadata (4.7 kB)
Downloading pip-26.0.1-py3-none-any.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 89.6 MB/s eta 0:00:00
Installing collected packages: pip
  Attempting uninstall: pip
    Found existing installation: pip 24.0
    Uninstalling pip-24.0:
      Successfully uninstalled pip-24.0
Successfully installed pip-26.0.1
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv
Collecting fastapi>=0.104.0 (from -r requirements.txt (line 2))
  Downloading fastapi-0.135.3-py3-none-any.whl.metadata (28 kB)
Collecting uvicorn>=0.24.0 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading uvicorn-0.44.0-py3-none-any.whl.metadata (6.7 kB)
Collecting pydantic>=2.5.0 (from -r requirements.txt (line 4))
  Downloading pydantic-2.12.5-py3-none-any.whl.metadata (90 kB)
Collecting python-dotenv>=1.0.0 (from -r requirements.txt (line 5))
  Downloading python_dotenv-1.2.2-py3-none-any.whl.metadata (27 kB)
Collecting httpx>=0.25.0 (from -r requirements.txt (line 6))
  Downloading httpx-0.28.1-py3-none-any.whl.metadata (7.1 kB)
Collecting openai>=1.0.0 (from -r requirements.txt (line 7))
  Downloading openai-2.30.0-py3-none-any.whl.metadata (29 kB)
Collecting agents>=0.1.0 (from -r requirements.txt (line 8))
  Downloading agents-1.4.0.tar.gz (37 kB)
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting google-generativeai>=0.3.0 (from -r requirements.txt (line 9))
  Downloading google_generativeai-0.8.6-py3-none-any.whl.metadata (3.9 kB)
Collecting sqlalchemy>=2.0.0 (from -r requirements.txt (line 10))
  Downloading sqlalchemy-2.0.49-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (9.5 kB)
Collecting aiosqlite>=0.19.0 (from -r requirements.txt (line 11))
  Downloading aiosqlite-0.22.1-py3-none-any.whl.metadata (4.3 kB)
Collecting asyncpg>=0.29.0 (from -r requirements.txt (line 12))
  Downloading asyncpg-0.31.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.4 kB)
Collecting psycopg2-binary>=2.9.9 (from -r requirements.txt (line 13))
  Downloading psycopg2_binary-2.9.11-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (4.9 kB)
Collecting python-jose>=3.3.0 (from python-jose[cryptography]>=3.3.0->-r requirements.txt (line 14))
  Downloading python_jose-3.5.0-py2.py3-none-any.whl.metadata (5.5 kB)
Collecting cryptography>=42.0.0 (from -r requirements.txt (line 15))
  Downloading cryptography-46.0.6-cp311-abi3-manylinux_2_34_x86_64.whl.metadata (5.7 kB)
Collecting redis>=5.0.0 (from -r requirements.txt (line 16))
  Downloading redis-7.4.0-py3-none-any.whl.metadata (12 kB)
Collecting structlog>=24.0.0 (from -r requirements.txt (line 17))
  Downloading structlog-25.5.0-py3-none-any.whl.metadata (9.5 kB)
Collecting auth0-python>=4.0.0 (from -r requirements.txt (line 18))
  Downloading auth0_python-5.2.0-py3-none-any.whl.metadata (11 kB)
Collecting fastapi-limiter>=0.1.0 (from -r requirements.txt (line 19))
  Downloading fastapi_limiter-0.2.0-py3-none-any.whl.metadata (5.4 kB)
Collecting google-api-python-client>=2.0.0 (from -r requirements.txt (line 22))
  Downloading google_api_python_client-2.193.0-py3-none-any.whl.metadata (7.0 kB)
Collecting google-auth-httplib2>=0.2.0 (from -r requirements.txt (line 23))
  Downloading google_auth_httplib2-0.3.1-py3-none-any.whl.metadata (3.0 kB)
Collecting google-auth-oauthlib>=1.0.0 (from -r requirements.txt (line 24))
  Downloading google_auth_oauthlib-1.3.1-py3-none-any.whl.metadata (2.6 kB)
Collecting authlib>=1.3.0 (from -r requirements.txt (line 25))
  Downloading authlib-1.6.9-py2.py3-none-any.whl.metadata (9.8 kB)
Collecting itsdangerous>=2.1.0 (from -r requirements.txt (line 26))
  Downloading itsdangerous-2.2.0-py3-none-any.whl.metadata (1.9 kB)
Collecting starlette>=0.46.0 (from fastapi>=0.104.0->-r requirements.txt (line 2))
  Downloading starlette-1.0.0-py3-none-any.whl.metadata (6.3 kB)
Collecting typing-extensions>=4.8.0 (from fastapi>=0.104.0->-r requirements.txt (line 2))
  Downloading typing_extensions-4.15.0-py3-none-any.whl.metadata (3.3 kB)
Collecting typing-inspection>=0.4.2 (from fastapi>=0.104.0->-r requirements.txt (line 2))
  Downloading typing_inspection-0.4.2-py3-none-any.whl.metadata (2.6 kB)
Collecting annotated-doc>=0.0.2 (from fastapi>=0.104.0->-r requirements.txt (line 2))
  Downloading annotated_doc-0.0.4-py3-none-any.whl.metadata (6.6 kB)
Collecting click>=7.0 (from uvicorn>=0.24.0->uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading click-8.3.2-py3-none-any.whl.metadata (2.6 kB)
Collecting h11>=0.8 (from uvicorn>=0.24.0->uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading h11-0.16.0-py3-none-any.whl.metadata (8.3 kB)
Collecting annotated-types>=0.6.0 (from pydantic>=2.5.0->-r requirements.txt (line 4))
  Downloading annotated_types-0.7.0-py3-none-any.whl.metadata (15 kB)
Collecting pydantic-core==2.41.5 (from pydantic>=2.5.0->-r requirements.txt (line 4))
  Downloading pydantic_core-2.41.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (7.3 kB)
Collecting anyio (from httpx>=0.25.0->-r requirements.txt (line 6))
  Downloading anyio-4.13.0-py3-none-any.whl.metadata (4.5 kB)
Collecting certifi (from httpx>=0.25.0->-r requirements.txt (line 6))
  Downloading certifi-2026.2.25-py3-none-any.whl.metadata (2.5 kB)
Collecting httpcore==1.* (from httpx>=0.25.0->-r requirements.txt (line 6))
  Downloading httpcore-1.0.9-py3-none-any.whl.metadata (21 kB)
Collecting idna (from httpx>=0.25.0->-r requirements.txt (line 6))
  Downloading idna-3.11-py3-none-any.whl.metadata (8.4 kB)
Collecting distro<2,>=1.7.0 (from openai>=1.0.0->-r requirements.txt (line 7))
  Downloading distro-1.9.0-py3-none-any.whl.metadata (6.8 kB)
Collecting jiter<1,>=0.10.0 (from openai>=1.0.0->-r requirements.txt (line 7))
  Downloading jiter-0.13.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (5.2 kB)
Collecting sniffio (from openai>=1.0.0->-r requirements.txt (line 7))
  Downloading sniffio-1.3.1-py3-none-any.whl.metadata (3.9 kB)
Collecting tqdm>4 (from openai>=1.0.0->-r requirements.txt (line 7))
  Downloading tqdm-4.67.3-py3-none-any.whl.metadata (57 kB)
Collecting tensorflow (from agents>=0.1.0->-r requirements.txt (line 8))
  Downloading tensorflow-2.21.0-cp311-cp311-manylinux_2_27_x86_64.whl.metadata (4.4 kB)
Collecting gym (from agents>=0.1.0->-r requirements.txt (line 8))
  Downloading gym-0.26.2.tar.gz (721 kB)
     ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 721.7/721.7 kB 69.2 MB/s  0:00:00
  Installing build dependencies: started
  Installing build dependencies: finished with status 'done'
  Getting requirements to build wheel: started
  Getting requirements to build wheel: finished with status 'done'
  Preparing metadata (pyproject.toml): started
  Preparing metadata (pyproject.toml): finished with status 'done'
Collecting ruamel.yaml (from agents>=0.1.0->-r requirements.txt (line 8))
  Downloading ruamel_yaml-0.19.1-py3-none-any.whl.metadata (16 kB)
Collecting google-ai-generativelanguage==0.6.15 (from google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading google_ai_generativelanguage-0.6.15-py3-none-any.whl.metadata (5.7 kB)
Collecting google-api-core (from google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading google_api_core-2.30.2-py3-none-any.whl.metadata (3.1 kB)
Collecting google-auth>=2.15.0 (from google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading google_auth-2.49.1-py3-none-any.whl.metadata (6.2 kB)
Collecting protobuf (from google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading protobuf-7.34.1-cp310-abi3-manylinux2014_x86_64.whl.metadata (595 bytes)
Collecting proto-plus<2.0.0dev,>=1.22.3 (from google-ai-generativelanguage==0.6.15->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading proto_plus-1.27.2-py3-none-any.whl.metadata (2.2 kB)
Collecting protobuf (from google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl.metadata (592 bytes)
Collecting googleapis-common-protos<2.0.0,>=1.63.2 (from google-api-core->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading googleapis_common_protos-1.74.0-py3-none-any.whl.metadata (9.2 kB)
Collecting requests<3.0.0,>=2.20.0 (from google-api-core->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading requests-2.33.1-py3-none-any.whl.metadata (4.8 kB)
Collecting grpcio<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-ai-generativelanguage==0.6.15->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading grpcio-1.80.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (3.8 kB)
Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-ai-generativelanguage==0.6.15->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading grpcio_status-1.80.0-py3-none-any.whl.metadata (1.3 kB)
Collecting pyasn1-modules>=0.2.1 (from google-auth>=2.15.0->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading pyasn1_modules-0.4.2-py3-none-any.whl.metadata (3.5 kB)
INFO: pip is looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
Collecting grpcio-status<2.0.0,>=1.33.2 (from google-api-core[grpc]!=2.0.*,!=2.1.*,!=2.10.*,!=2.2.*,!=2.3.*,!=2.4.*,!=2.5.*,!=2.6.*,!=2.7.*,!=2.8.*,!=2.9.*,<3.0.0dev,>=1.34.1->google-ai-generativelanguage==0.6.15->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading grpcio_status-1.78.0-py3-none-any.whl.metadata (1.3 kB)
  Downloading grpcio_status-1.76.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.75.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.74.0-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.73.0-py3-none-any.whl.metadata (1.1 kB)
INFO: pip is still looking at multiple versions of grpcio-status to determine which version is compatible with other requirements. This could take a while.
  Downloading grpcio_status-1.72.2-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.72.1-py3-none-any.whl.metadata (1.1 kB)
  Downloading grpcio_status-1.71.2-py3-none-any.whl.metadata (1.1 kB)
Collecting charset_normalizer<4,>=2 (from requests<3.0.0,>=2.20.0->google-api-core->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (40 kB)
Collecting urllib3<3,>=1.26 (from requests<3.0.0,>=2.20.0->google-api-core->google-generativeai>=0.3.0->-r requirements.txt (line 9))
  Downloading urllib3-2.6.3-py3-none-any.whl.metadata (6.9 kB)
Collecting greenlet>=1 (from sqlalchemy>=2.0.0->-r requirements.txt (line 10))
  Downloading greenlet-3.3.2-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl.metadata (3.7 kB)
Collecting ecdsa!=0.15 (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r requirements.txt (line 14))
  Downloading ecdsa-0.19.2-py2.py3-none-any.whl.metadata (29 kB)
Collecting rsa!=4.1.1,!=4.4,<5.0,>=4.0 (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r requirements.txt (line 14))
  Downloading rsa-4.9.1-py3-none-any.whl.metadata (5.6 kB)
Collecting pyasn1>=0.5.0 (from python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r requirements.txt (line 14))
  Downloading pyasn1-0.6.3-py3-none-any.whl.metadata (8.4 kB)
Collecting cffi>=2.0.0 (from cryptography>=42.0.0->-r requirements.txt (line 15))
  Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl.metadata (2.6 kB)
Collecting aiohttp>=3.11.18 (from auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading aiohttp-3.13.5-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (8.1 kB)
Collecting pyjwt>=2.8.0 (from auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading pyjwt-2.12.1-py3-none-any.whl.metadata (4.1 kB)
Collecting pyrate-limiter>=3.9.0 (from fastapi-limiter>=0.1.0->-r requirements.txt (line 19))
  Downloading pyrate_limiter-4.1.0-py3-none-any.whl.metadata (28 kB)
Collecting httplib2<1.0.0,>=0.19.0 (from google-api-python-client>=2.0.0->-r requirements.txt (line 22))
  Downloading httplib2-0.31.2-py3-none-any.whl.metadata (2.2 kB)
Collecting uritemplate<5,>=3.0.1 (from google-api-python-client>=2.0.0->-r requirements.txt (line 22))
  Downloading uritemplate-4.2.0-py3-none-any.whl.metadata (2.6 kB)
Collecting pyparsing<4,>=3.1 (from httplib2<1.0.0,>=0.19.0->google-api-python-client>=2.0.0->-r requirements.txt (line 22))
  Downloading pyparsing-3.3.2-py3-none-any.whl.metadata (5.8 kB)
Collecting requests-oauthlib>=0.7.0 (from google-auth-oauthlib>=1.0.0->-r requirements.txt (line 24))
  Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl.metadata (11 kB)
Collecting aiohappyeyeballs>=2.5.0 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl.metadata (5.9 kB)
Collecting aiosignal>=1.4.0 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading aiosignal-1.4.0-py3-none-any.whl.metadata (3.7 kB)
Collecting attrs>=17.3.0 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading attrs-26.1.0-py3-none-any.whl.metadata (8.8 kB)
Collecting frozenlist>=1.1.1 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading frozenlist-1.8.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (20 kB)
Collecting multidict<7.0,>=4.5 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading multidict-6.7.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (5.3 kB)
Collecting propcache>=0.2.0 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading propcache-0.4.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (13 kB)
Collecting yarl<2.0,>=1.17.0 (from aiohttp>=3.11.18->auth0-python>=4.0.0->-r requirements.txt (line 18))
  Downloading yarl-1.23.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (79 kB)
Collecting pycparser (from cffi>=2.0.0->cryptography>=42.0.0->-r requirements.txt (line 15))
  Downloading pycparser-3.0-py3-none-any.whl.metadata (8.2 kB)
Collecting six>=1.9.0 (from ecdsa!=0.15->python-jose>=3.3.0->python-jose[cryptography]>=3.3.0->-r requirements.txt (line 14))
  Downloading six-1.17.0-py2.py3-none-any.whl.metadata (1.7 kB)
Collecting oauthlib>=3.0.0 (from requests-oauthlib>=0.7.0->google-auth-oauthlib>=1.0.0->-r requirements.txt (line 24))
  Downloading oauthlib-3.3.1-py3-none-any.whl.metadata (7.9 kB)
Collecting httptools>=0.6.3 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading httptools-0.7.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (3.5 kB)
Collecting pyyaml>=5.1 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.4 kB)
Collecting uvloop>=0.15.1 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading uvloop-0.22.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (4.9 kB)
Collecting watchfiles>=0.20 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading watchfiles-1.1.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.9 kB)
Collecting websockets>=10.4 (from uvicorn[standard]>=0.24.0->-r requirements.txt (line 3))
  Downloading websockets-16.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (6.8 kB)
Collecting numpy>=1.18.0 (from gym->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading numpy-2.4.4-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (6.6 kB)
Collecting cloudpickle>=1.2.0 (from gym->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading cloudpickle-3.1.2-py3-none-any.whl.metadata (7.1 kB)
Collecting gym_notices>=0.0.4 (from gym->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading gym_notices-0.1.0-py3-none-any.whl.metadata (1.2 kB)
Collecting absl-py>=1.0.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading absl_py-2.4.0-py3-none-any.whl.metadata (3.3 kB)
Collecting astunparse>=1.6.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading astunparse-1.6.3-py2.py3-none-any.whl.metadata (4.4 kB)
Collecting flatbuffers>=25.9.23 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading flatbuffers-25.12.19-py2.py3-none-any.whl.metadata (1.0 kB)
Collecting gast!=0.5.0,!=0.5.1,!=0.5.2,>=0.2.1 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading gast-0.7.0-py3-none-any.whl.metadata (1.5 kB)
Collecting google_pasta>=0.1.1 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading google_pasta-0.2.0-py3-none-any.whl.metadata (814 bytes)
Collecting libclang>=13.0.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading libclang-18.1.1-py2.py3-none-manylinux2010_x86_64.whl.metadata (5.2 kB)
Collecting opt_einsum>=2.3.2 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading opt_einsum-3.4.0-py3-none-any.whl.metadata (6.3 kB)
Collecting packaging (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading packaging-26.0-py3-none-any.whl.metadata (3.3 kB)
INFO: pip is looking at multiple versions of tensorflow to determine which version is compatible with other requirements. This could take a while.
Collecting tensorflow (from agents>=0.1.0->-r requirements.txt (line 8))
  Downloading tensorflow-2.20.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl.metadata (4.5 kB)
Requirement already satisfied: setuptools in /usr/local/lib/python3.11/site-packages (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8)) (79.0.1)
Collecting termcolor>=1.1.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading termcolor-3.3.0-py3-none-any.whl.metadata (6.5 kB)
Collecting wrapt>=1.11.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading wrapt-2.1.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl.metadata (7.4 kB)
Collecting tensorboard~=2.20.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading tensorboard-2.20.0-py3-none-any.whl.metadata (1.8 kB)
Collecting keras>=3.10.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading keras-3.14.0-py3-none-any.whl.metadata (6.3 kB)
Collecting h5py>=3.11.0 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading h5py-3.16.0-cp311-cp311-manylinux_2_28_x86_64.whl.metadata (3.0 kB)
Collecting ml_dtypes<1.0.0,>=0.5.1 (from tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading ml_dtypes-0.5.4-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.9 kB)
Collecting markdown>=2.6.8 (from tensorboard~=2.20.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading markdown-3.10.2-py3-none-any.whl.metadata (5.1 kB)
Collecting pillow (from tensorboard~=2.20.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading pillow-12.2.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (8.8 kB)
Collecting tensorboard-data-server<0.8.0,>=0.7.0 (from tensorboard~=2.20.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading tensorboard_data_server-0.7.2-py3-none-manylinux_2_31_x86_64.whl.metadata (1.1 kB)
Collecting werkzeug>=1.0.1 (from tensorboard~=2.20.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading werkzeug-3.1.8-py3-none-any.whl.metadata (4.0 kB)
Requirement already satisfied: wheel<1.0,>=0.23.0 in /usr/local/lib/python3.11/site-packages (from astunparse>=1.6.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8)) (0.45.1)
Collecting rich (from keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading rich-14.3.3-py3-none-any.whl.metadata (18 kB)
Collecting namex (from keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading namex-0.1.0-py3-none-any.whl.metadata (322 bytes)
Collecting optree (from keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading optree-0.19.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl.metadata (34 kB)
Collecting markupsafe>=2.1.1 (from werkzeug>=1.0.1->tensorboard~=2.20.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl.metadata (2.7 kB)
Collecting markdown-it-py>=2.2.0 (from rich->keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading markdown_it_py-4.0.0-py3-none-any.whl.metadata (7.3 kB)
Collecting pygments<3.0.0,>=2.13.0 (from rich->keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading pygments-2.20.0-py3-none-any.whl.metadata (2.5 kB)
Collecting mdurl~=0.1 (from markdown-it-py>=2.2.0->rich->keras>=3.10.0->tensorflow->agents>=0.1.0->-r requirements.txt (line 8))
  Downloading mdurl-0.1.2-py3-none-any.whl.metadata (1.6 kB)
Downloading fastapi-0.135.3-py3-none-any.whl (117 kB)
Downloading uvicorn-0.44.0-py3-none-any.whl (69 kB)
Downloading pydantic-2.12.5-py3-none-any.whl (463 kB)
Downloading pydantic_core-2.41.5-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (2.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.1/2.1 MB 98.7 MB/s  0:00:00
Downloading python_dotenv-1.2.2-py3-none-any.whl (22 kB)
Downloading httpx-0.28.1-py3-none-any.whl (73 kB)
Downloading httpcore-1.0.9-py3-none-any.whl (78 kB)
Downloading openai-2.30.0-py3-none-any.whl (1.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.1/1.1 MB 134.1 MB/s  0:00:00
Downloading anyio-4.13.0-py3-none-any.whl (114 kB)
Downloading distro-1.9.0-py3-none-any.whl (20 kB)
Downloading jiter-0.13.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (362 kB)
Downloading typing_extensions-4.15.0-py3-none-any.whl (44 kB)
Downloading google_generativeai-0.8.6-py3-none-any.whl (155 kB)
Downloading google_ai_generativelanguage-0.6.15-py3-none-any.whl (1.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.3/1.3 MB 129.7 MB/s  0:00:00
Downloading google_api_core-2.30.2-py3-none-any.whl (173 kB)
Downloading google_auth-2.49.1-py3-none-any.whl (240 kB)
Downloading googleapis_common_protos-1.74.0-py3-none-any.whl (300 kB)
Downloading grpcio-1.80.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (6.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.8/6.8 MB 233.1 MB/s  0:00:00
Downloading grpcio_status-1.71.2-py3-none-any.whl (14 kB)
Downloading proto_plus-1.27.2-py3-none-any.whl (50 kB)
Downloading protobuf-5.29.6-cp38-abi3-manylinux2014_x86_64.whl (320 kB)
Downloading requests-2.33.1-py3-none-any.whl (64 kB)
Downloading charset_normalizer-3.4.7-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (214 kB)
Downloading idna-3.11-py3-none-any.whl (71 kB)
Downloading urllib3-2.6.3-py3-none-any.whl (131 kB)
Downloading sqlalchemy-2.0.49-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.3 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.3/3.3 MB 201.8 MB/s  0:00:00
Downloading aiosqlite-0.22.1-py3-none-any.whl (17 kB)
Downloading asyncpg-0.31.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.0/3.0 MB 229.1 MB/s  0:00:00
Downloading psycopg2_binary-2.9.11-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (4.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.2/4.2 MB 356.8 MB/s  0:00:00
Downloading python_jose-3.5.0-py2.py3-none-any.whl (34 kB)
Downloading rsa-4.9.1-py3-none-any.whl (34 kB)
Downloading cryptography-46.0.6-cp311-abi3-manylinux_2_34_x86_64.whl (4.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 4.5/4.5 MB 350.4 MB/s  0:00:00
Downloading redis-7.4.0-py3-none-any.whl (409 kB)
Downloading structlog-25.5.0-py3-none-any.whl (72 kB)
Downloading auth0_python-5.2.0-py3-none-any.whl (2.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 2.0/2.0 MB 111.6 MB/s  0:00:00
Downloading fastapi_limiter-0.2.0-py3-none-any.whl (5.2 kB)
Downloading google_api_python_client-2.193.0-py3-none-any.whl (14.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 14.9/14.9 MB 244.4 MB/s  0:00:00
Downloading google_auth_httplib2-0.3.1-py3-none-any.whl (9.5 kB)
Downloading httplib2-0.31.2-py3-none-any.whl (91 kB)
Downloading pyparsing-3.3.2-py3-none-any.whl (122 kB)
Downloading uritemplate-4.2.0-py3-none-any.whl (11 kB)
Downloading google_auth_oauthlib-1.3.1-py3-none-any.whl (19 kB)
Downloading authlib-1.6.9-py2.py3-none-any.whl (244 kB)
Downloading itsdangerous-2.2.0-py3-none-any.whl (16 kB)
Downloading aiohttp-3.13.5-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (1.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.8/1.8 MB 344.8 MB/s  0:00:00
Downloading multidict-6.7.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (246 kB)
Downloading yarl-1.23.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (102 kB)
Downloading aiohappyeyeballs-2.6.1-py3-none-any.whl (15 kB)
Downloading aiosignal-1.4.0-py3-none-any.whl (7.5 kB)
Downloading annotated_doc-0.0.4-py3-none-any.whl (5.3 kB)
Downloading annotated_types-0.7.0-py3-none-any.whl (13 kB)
Downloading attrs-26.1.0-py3-none-any.whl (67 kB)
Downloading certifi-2026.2.25-py3-none-any.whl (153 kB)
Downloading cffi-2.0.0-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.whl (215 kB)
Downloading click-8.3.2-py3-none-any.whl (108 kB)
Downloading ecdsa-0.19.2-py2.py3-none-any.whl (150 kB)
Downloading frozenlist-1.8.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (231 kB)
Downloading greenlet-3.3.2-cp311-cp311-manylinux_2_24_x86_64.manylinux_2_28_x86_64.whl (594 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 594.2/594.2 kB 202.7 MB/s  0:00:00
Downloading h11-0.16.0-py3-none-any.whl (37 kB)
Downloading propcache-0.4.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (210 kB)
Downloading pyasn1-0.6.3-py3-none-any.whl (83 kB)
Downloading pyasn1_modules-0.4.2-py3-none-any.whl (181 kB)
Downloading pyjwt-2.12.1-py3-none-any.whl (29 kB)
Downloading pyrate_limiter-4.1.0-py3-none-any.whl (38 kB)
Downloading requests_oauthlib-2.0.0-py2.py3-none-any.whl (24 kB)
Downloading oauthlib-3.3.1-py3-none-any.whl (160 kB)
Downloading six-1.17.0-py2.py3-none-any.whl (11 kB)
Downloading starlette-1.0.0-py3-none-any.whl (72 kB)
Downloading tqdm-4.67.3-py3-none-any.whl (78 kB)
Downloading typing_inspection-0.4.2-py3-none-any.whl (14 kB)
Downloading httptools-0.7.1-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (456 kB)
Downloading pyyaml-6.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (806 kB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 806.6/806.6 kB 473.3 MB/s  0:00:00
Downloading uvloop-0.22.1-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (3.8 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 3.8/3.8 MB 392.7 MB/s  0:00:00
Downloading watchfiles-1.1.1-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (456 kB)
Downloading websockets-16.0-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (184 kB)
Downloading cloudpickle-3.1.2-py3-none-any.whl (22 kB)
Downloading gym_notices-0.1.0-py3-none-any.whl (3.3 kB)
Downloading numpy-2.4.4-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (16.9 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 16.9/16.9 MB 225.6 MB/s  0:00:00
Downloading pycparser-3.0-py3-none-any.whl (48 kB)
Downloading ruamel_yaml-0.19.1-py3-none-any.whl (118 kB)
Downloading sniffio-1.3.1-py3-none-any.whl (10 kB)
Downloading tensorflow-2.20.0-cp311-cp311-manylinux_2_17_x86_64.manylinux2014_x86_64.whl (620.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 620.6/620.6 MB 169.8 MB/s  0:00:04
Downloading ml_dtypes-0.5.4-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (5.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.0/5.0 MB 295.7 MB/s  0:00:00
Downloading tensorboard-2.20.0-py3-none-any.whl (5.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.5/5.5 MB 363.8 MB/s  0:00:00
Downloading tensorboard_data_server-0.7.2-py3-none-manylinux_2_31_x86_64.whl (6.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 6.6/6.6 MB 158.8 MB/s  0:00:00
Downloading absl_py-2.4.0-py3-none-any.whl (135 kB)
Downloading astunparse-1.6.3-py2.py3-none-any.whl (12 kB)
Downloading flatbuffers-25.12.19-py2.py3-none-any.whl (26 kB)
Downloading gast-0.7.0-py3-none-any.whl (22 kB)
Downloading google_pasta-0.2.0-py3-none-any.whl (57 kB)
Downloading h5py-3.16.0-cp311-cp311-manylinux_2_28_x86_64.whl (5.0 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 5.0/5.0 MB 240.9 MB/s  0:00:00
Downloading keras-3.14.0-py3-none-any.whl (1.6 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.6/1.6 MB 352.3 MB/s  0:00:00
Downloading libclang-18.1.1-py2.py3-none-manylinux2010_x86_64.whl (24.5 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 24.5/24.5 MB 254.6 MB/s  0:00:00
Downloading markdown-3.10.2-py3-none-any.whl (108 kB)
Downloading opt_einsum-3.4.0-py3-none-any.whl (71 kB)
Downloading termcolor-3.3.0-py3-none-any.whl (7.7 kB)
Downloading werkzeug-3.1.8-py3-none-any.whl (226 kB)
Downloading markupsafe-3.0.3-cp311-cp311-manylinux2014_x86_64.manylinux_2_17_x86_64.manylinux_2_28_x86_64.whl (22 kB)
Downloading wrapt-2.1.2-cp311-cp311-manylinux1_x86_64.manylinux_2_28_x86_64.manylinux_2_5_x86_64.whl (114 kB)
Downloading namex-0.1.0-py3-none-any.whl (5.9 kB)
Downloading optree-0.19.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (441 kB)
Downloading packaging-26.0-py3-none-any.whl (74 kB)
Downloading pillow-12.2.0-cp311-cp311-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl (7.1 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 7.1/7.1 MB 225.0 MB/s  0:00:00
Downloading rich-14.3.3-py3-none-any.whl (310 kB)
Downloading pygments-2.20.0-py3-none-any.whl (1.2 MB)
   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ 1.2/1.2 MB 317.1 MB/s  0:00:00
Downloading markdown_it_py-4.0.0-py3-none-any.whl (87 kB)
Downloading mdurl-0.1.2-py3-none-any.whl (10.0 kB)
Building wheels for collected packages: agents, gym
  Building wheel for agents (pyproject.toml): started
  Building wheel for agents (pyproject.toml): finished with status 'done'
  Created wheel for agents: filename=agents-1.4.0-py3-none-any.whl size=62745 sha256=80811409c46410e88d839dadc27f79a9719b78cf5ba9984db80af5f2a37d10e4
  Stored in directory: /tmp/pip-ephem-wheel-cache-ar42xi3z/wheels/6a/41/e1/4d212ede7c9752d8f7050d78fa3295304bc22b8fb530d9ebe4
  Building wheel for gym (pyproject.toml): started
  Building wheel for gym (pyproject.toml): finished with status 'done'
  Created wheel for gym: filename=gym-0.26.2-py3-none-any.whl size=827727 sha256=09b5bc177f671b203f63c4aa9d68a94a3abb3ec77ed33190ee7ec8aab32b3303
  Stored in directory: /tmp/pip-ephem-wheel-cache-ar42xi3z/wheels/1c/77/9e/9af5470201a0b0543937933ee99ba884cd237d2faefe8f4d37
Successfully built agents gym
Installing collected packages: namex, libclang, gym_notices, flatbuffers, wrapt, websockets, uvloop, urllib3, uritemplate, typing-extensions, tqdm, termcolor, tensorboard-data-server, structlog, sniffio, six, ruamel.yaml, redis, pyyaml, python-dotenv, pyrate-limiter, pyparsing, pyjwt, pygments, pycparser, pyasn1, psycopg2-binary, protobuf, propcache, pillow, packaging, opt_einsum, oauthlib, numpy, multidict, mdurl, markupsafe, markdown, jiter, itsdangerous, idna, httptools, h11, greenlet, gast, frozenlist, distro, cloudpickle, click, charset_normalizer, certifi, attrs, asyncpg, annotated-types, annotated-doc, aiosqlite, aiohappyeyeballs, absl-py, yarl, werkzeug, uvicorn, typing-inspection, sqlalchemy, rsa, requests, pydantic-core, pyasn1-modules, proto-plus, optree, ml_dtypes, markdown-it-py, httplib2, httpcore, h5py, gym, grpcio, googleapis-common-protos, google_pasta, ecdsa, cffi, astunparse, anyio, aiosignal, watchfiles, tensorboard, starlette, rich, requests-oauthlib, python-jose, pydantic, httpx, grpcio-status, cryptography, aiohttp, openai, keras, google-auth, fastapi, authlib, auth0-python, tensorflow, google-auth-oauthlib, google-auth-httplib2, google-api-core, fastapi-limiter, google-api-python-client, agents, google-ai-generativelanguage, google-generativeai
Successfully installed absl-py-2.4.0 agents-1.4.0 aiohappyeyeballs-2.6.1 aiohttp-3.13.5 aiosignal-1.4.0 aiosqlite-0.22.1 annotated-doc-0.0.4 annotated-types-0.7.0 anyio-4.13.0 astunparse-1.6.3 asyncpg-0.31.0 attrs-26.1.0 auth0-python-5.2.0 authlib-1.6.9 certifi-2026.2.25 cffi-2.0.0 charset_normalizer-3.4.7 click-8.3.2 cloudpickle-3.1.2 cryptography-46.0.6 distro-1.9.0 ecdsa-0.19.2 fastapi-0.135.3 fastapi-limiter-0.2.0 flatbuffers-25.12.19 frozenlist-1.8.0 gast-0.7.0 google-ai-generativelanguage-0.6.15 google-api-core-2.30.2 google-api-python-client-2.193.0 google-auth-2.49.1 google-auth-httplib2-0.3.1 google-auth-oauthlib-1.3.1 google-generativeai-0.8.6 google_pasta-0.2.0 googleapis-common-protos-1.74.0 greenlet-3.3.2 grpcio-1.80.0 grpcio-status-1.71.2 gym-0.26.2 gym_notices-0.1.0 h11-0.16.0 h5py-3.16.0 httpcore-1.0.9 httplib2-0.31.2 httptools-0.7.1 httpx-0.28.1 idna-3.11 itsdangerous-2.2.0 jiter-0.13.0 keras-3.14.0 libclang-18.1.1 markdown-3.10.2 markdown-it-py-4.0.0 markupsafe-3.0.3 mdurl-0.1.2 ml_dtypes-0.5.4 multidict-6.7.1 namex-0.1.0 numpy-2.4.4 oauthlib-3.3.1 openai-2.30.0 opt_einsum-3.4.0 optree-0.19.0 packaging-26.0 pillow-12.2.0 propcache-0.4.1 proto-plus-1.27.2 protobuf-5.29.6 psycopg2-binary-2.9.11 pyasn1-0.6.3 pyasn1-modules-0.4.2 pycparser-3.0 pydantic-2.12.5 pydantic-core-2.41.5 pygments-2.20.0 pyjwt-2.12.1 pyparsing-3.3.2 pyrate-limiter-4.1.0 python-dotenv-1.2.2 python-jose-3.5.0 pyyaml-6.0.3 redis-7.4.0 requests-2.33.1 requests-oauthlib-2.0.0 rich-14.3.3 rsa-4.9.1 ruamel.yaml-0.19.1 six-1.17.0 sniffio-1.3.1 sqlalchemy-2.0.49 starlette-1.0.0 structlog-25.5.0 tensorboard-2.20.0 tensorboard-data-server-0.7.2 tensorflow-2.20.0 termcolor-3.3.0 tqdm-4.67.3 typing-extensions-4.15.0 typing-inspection-0.4.2 uritemplate-4.2.0 urllib3-2.6.3 uvicorn-0.44.0 uvloop-0.22.1 watchfiles-1.1.1 websockets-16.0 werkzeug-3.1.8 wrapt-2.1.2 yarl-1.23.0
WARNING: Running pip as the 'root' user can result in broken permissions and conflicting behaviour with the system package manager, possibly rendering your system unusable. It is recommended to use a virtual environment instead: https://pip.pypa.io/warnings/venv. Use the --root-user-action option if you know what you are doing and want to suppress this warning.
Removing intermediate container 068ad31a25a5
 ---> 2d466e3a74f9
Step 9/14 : COPY . .
 ---> 97600223864a
Step 10/14 : RUN useradd --create-home --shell /bin/bash app     && chown -R app:app /app
 ---> Running in 9906d4339311
Removing intermediate container 9906d4339311
 ---> 84f38323a7a9
Step 11/14 : USER app
 ---> Running in 28780df78072
Removing intermediate container 28780df78072
 ---> 6f5472c04df4
Step 12/14 : HEALTHCHECK --interval=30s --timeout=30s --start-period=5s --retries=3     CMD python -c "import requests; requests.get('http://localhost:8080/health')" || exit 1
 ---> Running in cbf40129ab77
Removing intermediate container cbf40129ab77
 ---> 9cd30e3a1948
Step 13/14 : EXPOSE 8080
 ---> Running in a5b5445e0684
Removing intermediate container a5b5445e0684
 ---> 42357c274d05
Step 14/14 : CMD exec uvicorn app.main:app --host 0.0.0.0 --port $PORT --workers 1
 ---> Running in e1f2ab87a5e4
Removing intermediate container e1f2ab87a5e4
 ---> 7bdd91f7f18d
Successfully built 7bdd91f7f18d
Successfully tagged europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:763836dd0e0a6849bacc726feb63cb84b20078c0
Successfully tagged europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate:latest
Finished Step #1 - "Build"
Starting Step #2 - "Push"
Already have image (with digest): gcr.io/cloud-builders/docker
The push refers to repository [europe-west1-docker.pkg.dev/gemini-cli-478208/cloud-run-source-deploy/hadiqagohar-ciphermate/cipheremate]
eb4c1703f111: Preparing
5a268342df1b: Preparing
78936f928288: Preparing
c789cc85613a: Preparing
97b7041c26b6: Preparing
10d07cb235b4: Preparing
8347a0657a00: Preparing
34b037810a00: Preparing
188695d9eb1d: Preparing
188c9b34dfbe: Preparing
c789cc85613a: Pushed
10d07cb235b4: Pushed
8347a0657a00: Pushed
eb4c1703f111: Pushed
5a268342df1b: Pushed
188695d9eb1d: Pushed
188c9b34dfbe: Pushed
34b037810a00: Pushed
97b7041c26b6: Pushed
78936f928288: Pushed
763836dd0e0a6849bacc726feb63cb84b20078c0: digest: sha256:e163badb5aecbee9dd7c58888021b2bd7c753321876b0af2b05d16e0b661e3f5 size: 2418
eb4c1703f111: Preparing
5a268342df1b: Preparing
78936f928288: Preparing
c789cc85613a: Preparing
97b7041c26b6: Preparing
10d07cb235b4: Preparing
8347a0657a00: Preparing
34b037810a00: Preparing
188695d9eb1d: Preparing
188c9b34dfbe: Preparing
c789cc85613a: Layer already exists
97b7041c26b6: Layer already exists
10d07cb235b4: Layer already exists
eb4c1703f111: Layer already exists
5a268342df1b: Layer already exists
78936f928288: Layer already exists
8347a0657a00: Layer already exists
34b037810a00: Layer already exists
188695d9eb1d: Layer already exists
188c9b34dfbe: Layer already exists
latest: digest: sha256:e163badb5aecbee9dd7c58888021b2bd7c753321876b0af2b05d16e0b661e3f5 size: 2418
Finished Step #2 - "Push"
Starting Step #3 - "Deploy"
Pulling image: gcr.io/google.com/cloudsdktool/cloud-sdk:slim
slim: Pulling from google.com/cloudsdktool/cloud-sdk
9d2f29087bcd: Already exists
9a3989f83f88: Pulling fs layer
efa6e181a280: Pulling fs layer
29987e94ac22: Pulling fs layer
9a3989f83f88: Verifying Checksum
9a3989f83f88: Download complete
29987e94ac22: Verifying Checksum
29987e94ac22: Download complete
9a3989f83f88: Pull complete
efa6e181a280: Verifying Checksum
efa6e181a280: Download complete
efa6e181a280: Pull complete
29987e94ac22: Pull complete
Digest: sha256:bc12b41388a0dc1bdc7ed0e051d50a2f15c7e8479914bc1c21f913aa3f6d7cf7
Status: Downloaded newer image for gcr.io/google.com/cloudsdktool/cloud-sdk:slim
gcr.io/google.com/cloudsdktool/cloud-sdk:slim
Deploying...
Creating Revision...................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................................failed
Deployment failed
ERROR: (gcloud.run.services.update) The user-provided container failed to start and listen on the port defined provided by the PORT=8080 environment variable within the allocated timeout. This can happen when the container port is misconfigured or if the timeout is too short. The health check timeout can be extended. Logs for this revision might contain more information.
Logs URL: https://console.cloud.google.com/logs/viewer?project=gemini-cli-478208&resource=cloud_run_revision/service_name/cipheremate/revision_name/cipheremate-00003-7vv&advancedFilter=resource.type%3D%22cloud_run_revision%22%0Aresource.labels.service_name%3D%22cipheremate%22%0Aresource.labels.revision_name%3D%22cipheremate-00003-7vv%22 
For more troubleshooting guidance, see https://cloud.google.com/run/docs/troubleshooting#container-failed-to-start
Finished Step #3 - "Deploy"
ERROR
ERROR: build step 3 "gcr.io/google.com/cloudsdktool/cloud-sdk:slim" failed: step exited with non-zero status: 1

 