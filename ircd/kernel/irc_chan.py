import re
from command import command

chan_re = re.compile(r'^#\w+$')


@command
def cmd_join(server, user, chan_name):
    if not chan_re.match(chan_name):
        server.send_reply(user, 'ERR_BADCHANNAME', chan_name)
        return

    if 'auth' not in user:
        server.send_reply(user, 'ERR_NOTREGISTERED')
        return

    chan, created = server.find_or_create_chan(chan_name)
    if server.nick_in_chan(user, chan):
        server.send_reply(user, 'ERR_ALREADYONCHANNEL', chan_name)
        return

    server.join_chan(user, chan, 'o' if created else '')
    server.send_chan(user, 'JOIN', chan)

    if chan['topic']:
        server.send_reply(user, 'RPL_TOPIC', chan['name'], chan['topic'])
    else:
        server.send_reply(user, 'RPL_NOTOPIC', chan['name'])

    send_names(server, user, chan)


def map_mode(mode):
    if 'o' in mode:
        return '@'
    return ''


def send_names(server, user, chan):
    nicks = []
    for nick, mode in server.chan_nicks(chan).iteritems():
        nicks.append('%s%s' % (map_mode(mode), nick))
    nick_list = ' '.join(nicks)

    server.send_reply(user, 'RPL_NAMREPLY', chan['name'], nick_list)
    server.send_reply(user, 'RPL_ENDOFNAMES', chan['name'])


@command
def irc_names(server, user, chan_name):
    if 'auth' not in user:
        server.send_reply(user, 'ERR_NOTREGISTERED')
        return

    if not chan_name:
        server.send_reply(user, 'ERR_NEEDMOREPARAMS', 'NAMES')
        return

    chan = server.find_chan(chan_name)
    if not chan:
        server.send_reply(user, 'ERR_NOSUCHCHANNEL', chan_name)
        return

    if not server.user_in_chan(user, chan):
        server.send_reply(user, 'ERR_NOTONCHANNEL', chan_name)
        return

    send_names(server, user, chan)


@command
def cmd_part(server, user, chan_name):
    chan = server.find_chan(chan_name)
    if not chan:
        server.send_reply(user, 'ERR_NOSUCHCHANNEL', chan_name)
        return

    if not server.user_in_chan(user, chan):
        server.send_reply(user, 'ERR_NOTONCHANNEL', chan_name)
        return

    server.send_chan(user, 'PART', chan)
    server.part_chan(user, chan)
    if not server.chan_count(chan):
        server.destroy_chan(chan)
