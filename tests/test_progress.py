from ipars import ProgressBarManager


def test_full_cycle_does_not_raise():
    bar = ProgressBarManager(max=3)
    bar.next()
    bar.next()
    bar.next()
    bar.finish()


def test_single_iteration():
    bar = ProgressBarManager(max=1)
    bar.next()
    bar.finish()


def test_custom_message():
    bar = ProgressBarManager(max=2, message='Загрузка')
    bar.next()
    bar.next()
    bar.finish()


def test_custom_fill_and_width():
    bar = ProgressBarManager(max=2, fill='=', width=20)
    bar.next()
    bar.next()
    bar.finish()
