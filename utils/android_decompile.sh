#! /bin/sh

# PL Last Day of 2007
# REQUIRE JAD !!!


mkdir /tmp/wk
cp /tmp/android.jar /tmp/wk/android.jar 
cd /tmp/wk
jar xvf android.jar

for i in `find . -name *.class`; do
jad -r $i  
done
