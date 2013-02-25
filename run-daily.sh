#!/bin/bash
(
    flock --exclusive 200
    sql-backup.py --daily -c sql.mit.edu-daily.json
) 200> /var/lock/backup-ng.lock
