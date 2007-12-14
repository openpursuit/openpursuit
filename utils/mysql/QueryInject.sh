#! /bin/sh -x

# blacksheep 2007

#
#  Launch <sql-file> SQL commands
#

. ../Environment.sh

if [ $# != 1 ]; then
	echo "Use: $0 <sql-file>"
else
	cat $1 | mysql -u root  $DB_INSTANCE -p
fi
