import sys
import imaplib
from timeit import default_timer as timer
import time
import datetime
import click


def process_mailbox(M, login_time):
    rv, data = M.search(None, "ALL")
    if rv != 'OK':
        print "No messages found!"
        return
    fetch_loop_start = timer()
    for num in data[0].split():
        if int(num) < 21:
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print "ERROR getting message", num
                return
    fetch_loop_end = timer()
    fetch_loop_time = fetch_loop_end - fetch_loop_start
    now = datetime.datetime.now()
    total_time = login_time + fetch_loop_time
    print str(now) + "," + "%.3f" % login_time + "," + "%.3f" % fetch_loop_time + "," + "%.3f" % total_time

def print_usage_and_die():
    print "Usage: imap-test.py --help"
    exit(1)

@click.command()
@click.option('--host', default="imap.gmail.com", help='IMAP Host FQDN.')
@click.option('--username', default="", help='IMAP Username.')
@click.option('--password', default="", help='IMAP Password.')
@click.option('--folder', default="Inbox", help='IMAP Folder ie Inbox.')


def main(host, username, password, folder):

    #Check Args
    if username == "":
        print_usage_and_die()
    if password == "":
        print_usage_and_die()

    M = imaplib.IMAP4_SSL(host)
    try:
        login_start = timer()
        rv, data = M.login(username, password)
        time.sleep(5)
        login_end = timer()
        login_time = login_end - login_start
        #print "Login Time: " + "%.9f" % login_time
    except imaplib.IMAP4.error:
        print "LOGIN FAILED!!! "
        sys.exit(1)
    rv, data = M.select(folder)
    if rv == 'OK':
        process_mailbox(M, login_time)
        M.close()
    else:
        print "ERROR: Unable to open mailbox ", rv
    M.logout()

if __name__ == '__main__':
    main()
