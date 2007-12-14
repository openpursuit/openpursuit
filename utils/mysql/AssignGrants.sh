#! /bin/sh -x

# blacksheep 2007

#
# Assegna a $DB_USER le GRANT per il database mysql $DB_INSTANCE
#


. ../Environment.sh

echo "ATTENTION:"
echo "ASKs 2 times the pass..."
echo ""


echo "use $DB_INSTANCE ; GRANT ALL PRIVILEGES ON *.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS' WITH GRANT OPTION; "| mysql -u root  $DB_INSTANCE -p

