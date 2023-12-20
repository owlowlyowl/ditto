from __future__ import annotations

import pytest

from ditto.snapshot import Snapshot
from ditto.io.protocol import SnapshotIO
from ditto.io._pickle import PickleIO
from ditto.io._json import JsonIO
from ditto.io._yaml import YamlIO


IO_MAP: dict[str, SnapshotIO] = {
    "pkl": PickleIO(),
    "json": JsonIO(),
    "yaml": YamlIO(),
}


def register_io(name: str, io: SnapshotIO) -> None:
    IO_MAP[name] = io


@pytest.fixture(scope="function")
def snapshot(request) -> Snapshot:

    # TODO: ability 
    io_name = None
    for mark in request.node.iter_markers(name="record"):
        if mark.args:
            if io_name is not None:
                pytest.fail("Only one 'record' mark is allowed.")
            io_name = mark.args[0]
    
    io_name = io_name if io_name is not None else "pkl"
        
    # TODO: do i like this?
    # if io_name is None:
    #     pytest.fail("'record' is a required mark when using the 'snapshot' fixture.")

    path = request.path.parent / ".ditto"
    path.mkdir(exist_ok=True)

    return Snapshot(
        path=path,
        name=request.node.name,
        record=True,
        io=IO_MAP.get(io_name, PickleIO()),
    )


def pytest_configure(config):
    # register an additional marker
    config.addinivalue_line(
        "markers", "record(io): snapshot values"
    )

# @pytest.hookimpl(tryfirst=True)
# def pytest_fixture_setup(fixturedef, request):
#     # print('Fixture setup: ', fixturedef.argname)
#     # print(fixturedef)
#     pass


# def pytest_addoption(parser):
#     parser.addoption(
#         "-E",
#         action="store",
#         metavar="NAME",
#         help="only run tests matching the environment NAME.",
#     )
#     parser.addoption(
#         "-R",
#         action="store",
#         metavar="RECORD",
#         help="only run tests matching the environment NAME.",
#     )

# def pytest_runtest_setup(item):
#     envnames = [mark.args[0] for mark in item.iter_markers(name="env")]
#     if envnames:
#         if item.config.getoption("-E") not in envnames:
#             pytest.skip("test requires env in {!r}".format(envnames))

#     for mark in item.iter_markers(name="record"):
#         msg =f"recording: args={mark.args}; kwargs={mark.kwargs}" 
#         pytest.skip(msg)
#         # print(msg)