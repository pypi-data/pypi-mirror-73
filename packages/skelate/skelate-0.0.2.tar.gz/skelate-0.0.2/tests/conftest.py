import pytest


@pytest.fixture
def skeleton_dir(tmpdir):
    (tmpdir / "test").mkdir()
    (tmpdir / "empty_test").mkdir()

    with (tmpdir / "test" / "static.txt").open("wb") as regular_file:
        regular_file.write(b"regular data")

    with (tmpdir / "test" / "template.txt.j2").open("wb") as template_file:
        template_file.write(b"{{data_type}} data")

    return tmpdir
