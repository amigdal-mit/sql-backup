#!/bin/bash

# We can't do an AFS backup unless
#  a) we're under the lock
#  b) we have tokens
#
# unfortunately, we can't guarantee both of these at the same time,
# but we can guarantee a valid token once we get one, using k5start.
# As a result, we're going to use a clever scheme, in which we
# premptively lock, run k5start, and if that succeeds, we can then do
# the backup.  If not, we release the lock and try again.
#
# For this to work, we need to run k5start in "kinit daemon" mode,
# which means we need a pid fie.

kstartpid=$(mktemp /tmp/backup-ng-k5start.XXXXXXXXXX)
kstartret=1

while [ $kstartret -ne 0 ]; do
    (
	flock --exclusive 200
	k5start -f /etc/daemon.keytab -u daemon/sql.mit.edu -t -K 15m -l6h -b -p "$kstartpid" || exit 1
	# If we get here, we're under both the lock and the k5start
	
	# Get a list of all the mysql databases
	for db in $(mysqlshow.py); do
	    echo "$db" | grep -q '+'
	    [ $? -ne 0 ] && continue
	    user="${db%%+*}"
	    sql-backup.py --local -c sql.mit.edu-afs.json --user="$user" --database="$db"
	done

	# Okay, we're all done. Kill k5start
	kill -TERM $(cat "$kstartpid")
	exit 0
    ) 200> /var/lock/backup-ng.lock
    kstartret=$?
done

rm -f "$kstartpid"
