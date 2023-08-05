from unittest import mock

import pytest

from mopidy.models import Ref
from mopidy_dleyna.util import Future


@pytest.fixture
def servers():
    return [
        {
            "FriendlyName": "Media Server #1",
            "DisplayName": "Media1",
            "URI": "dleyna://media1",
        },
        {
            "FriendlyName": "Media Server #2",
            "DisplayName": "Media2",
            "URI": "dleyna://media2",
        },
    ]


@pytest.fixture
def container():
    return {"DisplayName": "Root", "Type": "container", "URI": "dleyna://media"}


@pytest.fixture
def items():
    return [
        {"DisplayName": "Track #1", "Type": "music", "URI": "dleyna://media/1"},
        {"DisplayName": "Track #2", "Type": "audio", "URI": "dleyna://media/2"},
        {"DisplayName": "Track #3", "Type": "audio", "URI": "dleyna://media/3"},
    ]


def test_browse_root(backend, servers):
    with mock.patch.object(backend, "client") as m:
        m.servers.return_value = Future.fromvalue(servers)
        assert backend.library.browse(backend.library.root_directory.uri) == [
            Ref.directory(name="Media Server #1", uri="dleyna://media1"),
            Ref.directory(name="Media Server #2", uri="dleyna://media2"),
        ]


def test_browse_items(backend, container, items):
    # FIXME: how to patch multiple object methods...
    with mock.patch.object(backend, "client") as m:
        m.properties.return_value = Future.fromvalue(container)
        m.browse.side_effect = [
            Future.fromvalue([items[0:2], True]),
            Future.fromvalue([items[2:3], True]),
            Future.fromvalue([[], False]),
        ]
        assert backend.library.browse(container["URI"]) == [
            Ref.track(name="Track #1", uri="dleyna://media/1"),
            Ref.track(name="Track #2", uri="dleyna://media/2"),
            Ref.track(name="Track #3", uri="dleyna://media/3"),
        ]
