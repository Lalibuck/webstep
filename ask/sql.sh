sudo python3 -m pip install mysqlclient
sudo /etc/init.d/mysql start
mysql -uroot -e "CREATE DATABASE stepic_web;"
mysql -uroot -e "create user 'box'@'localhost' identified by '1234';"
mysql -uroot -e "grant all privileges on stepic_web.* to 'box'@'localhost' with grant option;"