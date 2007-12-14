#! /bin/sh -x

# blacksheep 2007

#
# Crea il database mysql $DB_TO_CREATE
#


. ../Environment.sh

echo "ATTENTION:"
echo "ASKs 2 times the pass..."
echo ""

#
# Viene chiesta la password di amministratore di mysql
#

mysqladmin -u root create $DB_INSTANCE -p


#mysql $DB_TO_CREATE


echo "use $DB_INSTANCE ; GRANT ALL PRIVILEGES ON *.* TO '$DB_USER'@'localhost' IDENTIFIED BY '$DB_PASS' WITH GRANT OPTION; "| mysql -u root  $DB_INSTANCE -p

