from testutil import *


def test_reset(k1):
    msg('JOIN #a')
    popall()

    raw('reset test ')
    assert pop() == 'test:__1 :test1!test1@::1 PART #a\r\n'


def test_utf8(k1):
    msg('PING \xAA\xAA\xAA\xAA\xAA\xAA\xAA\xAA')
    assert code() == '998'  # invalid utf8


def test_nouser(k0):
    msg('PING oi')
    assert code() is None

    raw('disconnect test:__1 ')
    assert code() is None


def test_main():
    from ircd.kernel.main import main

    r = redis.StrictRedis(db=1)
    r.rpush('mq:kernel', 'shutdown test test')

    main(Config())

    # control should reach here
    assert True
