#!/bin/bash

# FLAG is in the environment variable

rootdir="$(mktemp -d)"
trap "{ rm -rf '$rootdir'; }" EXIT
mkdir "$rootdir/bin"
cp -a /chroot/bin "$rootdir"
mkdir "$rootdir/root"
mkdir "$rootdir/work"
mkdir "$rootdir/dev"
mknod "$rootdir/dev/null" c 1 3
chmod 666 "$rootdir/dev/null"

exec /chroot/bin/busybox sh -c "exec chroot '$rootdir' /bin/jail"
