# Copyright (c) 2014-2019, iocage
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted providing that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY
# DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS
# OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION)
# HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT,
# STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING
# IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

import pytest


require_root = pytest.mark.require_root
require_zpool = pytest.mark.require_zpool


@require_root
@require_zpool
def test_01_destroy_jail(invoke_cli, resource_selector, skip_test):
    jails = resource_selector.all_jails
    skip_test(not jails)

    jail = jails[0]
    invoke_cli(
        ['destroy', '-f', jail.name]
    )

    assert jail.exists is False


@require_root
@require_zpool
def test_02_destroy_jails(invoke_cli, resource_selector, skip_test):
    jails = resource_selector.not_cloned_jails
    skip_test(not jails)

    # Let's destroy 50% of jails - in case of only one jail, let's skip
    up = int(len(jails) / 2)
    skip_test(up == 0)

    destroy_jails = jails[:up]
    invoke_cli(
        ['destroy', '-f', *[j.name for j in destroy_jails]]
    )

    for jail in destroy_jails:
        assert jail.exists is False


@require_root
@require_zpool
def test_03_destroy_release(invoke_cli, skip_test, resource_selector):
    releases = resource_selector.releases
    skip_test(not releases)

    release = releases[0]
    assert release.exists is True

    invoke_cli(
        ['destroy', '-fr', release]
    )

    assert release.exists is False

# TODO: Add tests for release and download later - fetching is time consuming :P
