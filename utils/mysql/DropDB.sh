#! /bin/sh -x

# blacksheep 2007

#
# Drops database $DB_INSTANCE
#

. ../Environment.sh

echo "Are you sure you want to delete db [$DB_TO_DROP] ?"
echo "type [yes] to proceed"
read check

if [ "$check" = "yes" ]; then
    echo "drop database $DB_INSTANCE;" | mysql -u $DB_USER $DB_INSTANCE  -p
else 
    echo "you did not type [yes], skipping..."
fi
