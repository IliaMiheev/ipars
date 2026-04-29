import pytest
from ipars import CsvManager


def test_writerow_and_getrows(tmp_path):
    cm = CsvManager()
    filepath = str(tmp_path / 'data.csv')
    row = ['Alice', '30', 'Engineer']

    cm.writerow(filepath, 'w', row)
    result = cm.getRows(filepath)

    assert result == [row]


def test_writerows_and_getrows(tmp_path):
    cm = CsvManager()
    filepath = str(tmp_path / 'data.csv')
    rows = [['Alice', '30'], ['Bob', '25'], ['Carol', '28']]

    cm.writerows(filepath, 'w', rows)
    result = cm.getRows(filepath)

    assert result == rows


def test_append_mode(tmp_path):
    cm = CsvManager()
    filepath = str(tmp_path / 'data.csv')

    cm.writerow(filepath, 'w', ['first'])
    cm.writerow(filepath, 'a', ['second'])
    result = cm.getRows(filepath)

    assert result == [['first'], ['second']]


def test_custom_delimiter(tmp_path):
    cm = CsvManager(delimiter=',')
    filepath = str(tmp_path / 'data.csv')
    row = ['one', 'two', 'three']

    cm.writerow(filepath, 'w', row)
    result = cm.getRows(filepath)

    assert result == [row]


def test_invalid_mode_raises(tmp_path):
    cm = CsvManager()
    filepath = str(tmp_path / 'data.csv')
    with pytest.raises(ValueError):
        cm.writerow(filepath, 'x', ['data'])


def test_invalid_row_type_raises(tmp_path):
    cm = CsvManager()
    filepath = str(tmp_path / 'data.csv')
    with pytest.raises(ValueError):
        cm.writerow(filepath, 'w', 'not a list')


def test_invalid_constructor_args():
    with pytest.raises(ValueError):
        CsvManager(delimiter=123)


def test_pprint_does_not_raise(capsys):
    cm = CsvManager()
    cm.pprint([['a', 'b'], ['c', 'd']])
    captured = capsys.readouterr()
    assert 'a' in captured.out
