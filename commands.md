<!-- Библиотека для загрузки файлов на Pypi -->
pip install twine
<!-- Сборка библиотеки -->
python setup.py sdist bdist_wheel
<!-- Загрузка библиотеки -->
twine upload dist/*
