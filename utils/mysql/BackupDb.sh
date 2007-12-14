#! /bin/sh -x

# blacksheep 2007

#
# Connects to DataBase
#

. ../Environment.sh

mysqldump -u $DB_USER  $DB_INSTANCE -p > backup_openpursuit.sql

