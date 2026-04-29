import pytest
from ipars import JsonManager


def test_dump_and_load(tmp_path):
    jm = JsonManager()
    filepath = str(tmp_path / 'data.json')
    data = {'name': 'ipars', 'version': 3, 'active': True}

    jm.dump(filepath, data)
    result = jm.load(filepath)

    assert result == data


def test_dump_and_load_list(tmp_path):
    jm = JsonManager()
    filepath = str(tmp_path / 'list.json')
    data = [1, 2, 3, 'hello']

    jm.dump(filepath, data)
    result = jm.load(filepath)

    assert result == data


def test_dump_and_load_with_cyrillic(tmp_path):
    jm = JsonManager()
    filepath = str(tmp_path / 'cyrillic.json')
    data = {'текст': 'привет'}

    jm.dump(filepath, data)
    result = jm.load(filepath)

    assert result == data


def test_load_nonexistent_file():
    jm = JsonManager()
    with pytest.raises(FileNotFoundError):
        jm.load('nonexistent_file_xyz.json')


def test_invalid_encoding_raises():
    with pytest.raises(ValueError):
        JsonManager(encoding=123)


def test_load_invalid_path_type():
    jm = JsonManager()
    with pytest.raises(ValueError):
        jm.load(123)


def test_dump_invalid_path_type(tmp_path):
    jm = JsonManager()
    with pytest.raises(ValueError):
        jm.dump(123, {'key': 'value'})


def test_pprint_does_not_raise(capsys):
    jm = JsonManager()
    jm.pprint({'key': 'value'})
    captured = capsys.readouterr()
    assert 'key' in captured.out
