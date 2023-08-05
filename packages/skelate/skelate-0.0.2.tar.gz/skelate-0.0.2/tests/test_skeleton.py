import os.path
import pytest

from skelate.skeleton import Skeleton
from uuid import uuid4


def test_render_source(skeleton_dir):
    """ Feature: Render a template from a skeleton

    Given I have a skeleton directory
    And this skeleton directory contains templates
    When I render a template to a target
    Then the target should contain the templated content,
    And all variables should be expanded.
    """
    skel = Skeleton(skeleton_dir)
    result = skel.render_source(
        "test/template.txt.j2",
        os.path.join(skeleton_dir, "rendered.txt"),
        variables=dict(data_type="TEST"),
    )

    assert result == os.path.join(skeleton_dir, "rendered.txt")
    assert os.path.getsize(result) > 0
    with open(result, 'rb') as rendered_file:
        assert b"TEST" in rendered_file.read()

    # Second 'render' should do nothing since path exists.
    exists_result = skel.render_source(
        "test/template.txt.j2",
        os.path.join(skeleton_dir, "rendered.txt"),
        variables=dict(data_type="TEST")
    )

    assert exists_result is None

    # Force should cause the file to be written even if it does exist
    force_result = skel.render_source(
        "test/template.txt.j2",
        os.path.join(skeleton_dir, "rendered.txt"),
        variables=dict(data_type="TEST"),
        force=True
    )

    assert force_result == os.path.join(skeleton_dir, "rendered.txt")

    # An error should be raised if the target directory doesn't exist.
    with pytest.raises(IOError):
        skel.render_source(
            "test/template.txt.j2",
            os.path.join(skeleton_dir, f"{uuid4().hex}/rendered.txt"),
            variables=dict(data_type="TEST"),
            force=True
        )

    # Second 'render' should do nothing since path exists.
    exists_result = skel.render_source(
        "test/template.txt.j2",
        os.path.join(skeleton_dir, "rendered.txt")
    )


def test_copy_source(skeleton_dir):
    """ Feature: Copy raw files from skeleton.

    Given I have a skeleton directory
    And this skeleton directory contains raw files
    When I copy a raw file to a target
    Then that file's contents should be copied as-is to the target.
    """
    skel = Skeleton(skeleton_dir)
    target = os.path.join(skeleton_dir, f"{uuid4().hex}.txt")
    source = os.path.join(skeleton_dir, "test/static.txt")
    result = skel.copy_source("test/static.txt", target)

    assert result == target
    assert os.path.getsize(result) == os.path.getsize(source)
    assert open(result, 'rb').read() == open(source, 'rb').read()

    # Second 'copy' should do nothing since path exists.
    exists_result = skel.copy_source("test/static.txt", target)
    assert exists_result is None

    # Force should cause the file to be written even if it does exist
    force_result = skel.copy_source("test/static.txt", target, force=True)

    assert force_result == target
    assert os.path.getsize(result) == os.path.getsize(source)
    assert open(result, 'rb').read() == open(source, 'rb').read()

    # An error should be raised if the target directory doesn't exist.
    with pytest.raises(IOError):
        skel.copy_source(
            "test/static.txt",
            os.path.join(skeleton_dir, f"{uuid4().hex}/copy.txt"),
            force=True
        )


def test_process_source_file(skeleton_dir):
    """ Feature: Process a skeleton file into a target directory

    Given I have a skeleton directory
    And this skeleton directory contains raw files and templates
    When I process a file to a target directory
    Then if that file is a template, its content should be rendered to a file
    whose name is the template name without its extension,
    And if that file is a raw file, it should be copied as is to a file of the
    same name under the target directory.
    """
    skel = Skeleton(skeleton_dir)
    target_root = os.path.join(skeleton_dir, "processed")
    rendered_result = skel.process_source_file(
        "test/template.txt.j2",
        target_root,
        variables=dict(data_type="TEST"),
    )

    assert rendered_result == os.path.join(target_root, "test/template.txt")
    assert os.path.getsize(rendered_result) > 0
    with open(rendered_result, 'rb') as rendered_file:
        assert b"TEST" in rendered_file.read()

    copied_result = skel.process_source_file(
        "test/static.txt",
        target_root,
        variables=dict(data_type="TEST"),
    )
    assert copied_result == os.path.join(target_root, "test/static.txt")
    assert os.path.getsize(os.path.join(skeleton_dir, "test/static.txt")) \
        == os.path.getsize(os.path.join(target_root, "test/static.txt"))
    assert open(os.path.join(skeleton_dir, "test/static.txt"), 'rb').read() \
        == open(os.path.join(target_root, "test/static.txt"), 'rb').read()

    os.remove(os.path.join(target_root, "test/static.txt"))
    os.remove(os.path.join(target_root, "test/template.txt"))

    # Check that raw_paths entries are treated like regular files, and that
    # excluded files are not processed
    skel = Skeleton(
        skeleton_dir,
        raw_paths=["test/template.txt.j2"],
        excluded_paths=["test/static.txt"]
    )

    raw_result = skel.process_source_file(
        "test/template.txt.j2",
        target_root,
        variables=dict(data_type="TEST"),
    )

    assert raw_result == os.path.join(target_root, "test/template.txt.j2")
    with open(raw_result, 'rb') as raw_file:
        assert b"{{data_type}}" in raw_file.read()
    assert skel.process_source_file("test/static.txt", target_root) is None


def test_create(skeleton_dir):
    """ Feature: Create a directory from a skeleton directory

    Given I have a skeleton directory
    And this skeleton directory contains raw files and templates
    When I create a target directory
    Then raw files should be copied as is to the target directory
    And templates should be rendered
    """

    skel = Skeleton(skeleton_dir, variables=dict(data_type="TEST"))
    target_root = os.path.join(skeleton_dir, "processed")

    result = skel.create(target_root)
    assert result == target_root

    rendered_result = os.path.join(target_root, "test/template.txt")
    assert os.path.exists(rendered_result)
    assert os.path.getsize(rendered_result) > 0
    with open(rendered_result, 'rb') as rendered_file:
        assert b"TEST" in rendered_file.read()

    static_result = os.path.join(target_root, "test/static.txt")
    assert os.path.exists(static_result)
    assert os.path.getsize(static_result) == \
        os.path.getsize(os.path.join(skeleton_dir, "test/static.txt"))

    os.remove(os.path.join(target_root, "test/static.txt"))
    os.remove(os.path.join(target_root, "test/template.txt"))

    skel = Skeleton(
        skeleton_dir,
        raw_paths=["test/template.txt.j2"],
        excluded_paths=["test/static.txt"]
    )

    target_root = os.path.join(skeleton_dir, "processed")

    result = skel.create(target_root, variables=dict(data_type="TEST"))
    assert result == target_root

    assert not os.path.exists(os.path.join(target_root, "test/template.txt"))
    assert os.path.exists(os.path.join(target_root, "test/template.txt.j2"))
    raw_template = os.path.join(target_root, "test/template.txt.j2")
    with open(raw_template, 'rb') as raw_file:
        assert b"TEST" not in raw_file.read()

    static_result = os.path.join(target_root, "test/static.txt")
    assert not os.path.exists(static_result)

    # Create should fail if a silly number of workers is given.
    with pytest.raises(ValueError):
        skel.create(target_root, workers=0)

    with pytest.raises(ValueError):
        skel.create(target_root, workers=-1)
