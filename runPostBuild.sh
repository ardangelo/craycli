#!/bin/bash
#
# MIT License
# 
# (C) Copyright [2020] Hewlett Packard Enterprise Development LP
# 
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.

: ${DIST:="dist"}
RPM_PATH="${DIST}/rpmbuild/RPMS/x86_64"
RPM=$(ls -l $RPM_PATH | grep rpm | grep -v src | awk '{print $NF}')

if command -v yum > /dev/null; then
    yum install -y $RPM_PATH/$RPM
elif command -v zypper > /dev/null; then
    zypper --no-gpg-checks install -y -f -l $RPM_PATH/$RPM
else
    echo "Unsupported package manager or package manager not found -- installing nothing"
    exit 1
fi
