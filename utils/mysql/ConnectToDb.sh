#! /bin/sh -x

# blacksheep 2007

#
# Connects to DataBase
#

. ../Environment.sh

mysql -u $DB_USER  $DB_INSTANCE -p

