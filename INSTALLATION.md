# Setup the database
Install mysql (database)
```console
sudo apt install mysql-server
sudo mysql
```

In mysql :
```console
CREATE DATABASE sailboat;
USE sailboat;
CREATE TABLE boat (lat double, lon double, heading float, speed float, true_wind_direction float);
CREATE TABLE waypoints (id int NOT NULL AUTO_INCREMENT, lat double, lon double,PRIMARY KEY (id));
CREATE USER 'username'@'localhost' IDENTIFIED BY '';
GRANT ALL PRIVILEGES ON sailboat.* TO 'username'@'localhost';
```

# Install PHP

*ubuntu 22.04 -> php8.1*

```console
sudo apt install php?.?
sudo apt install php-mysqli
```

# Setup the webserver

Install apache2 (HTTP server)
```console
sudo apt install apache2
sudo systemctl start apache2
```

Copy the content of 'website' into /var/www/html
```console
git clone https://github.com/vivipal/Birmingham-Sailboat-monitoring-website
rm -rf /var/www/html/*
cp -r Birmingham-Sailboat-monitoring-website/* /var/www/html/

sudo a2enmod php?.?
sudo systemctl restart apache2
```

**WARNING**: Don't forget to change your credential in the connect.php file


# Use downloaded tiles

You can use https://github.com/AliFlux/MapTilesDownloader to download offline tiles.

Make sure that your downloaded tiles are following this format "{z}/{x}/{y}.png".

In the folder containing those files run:

```python3 -m http.server 5432```
*(5432 is the server port, if you want to use another port dont forget to change it in map.html l.62)*

It will create a basic http server to serve the downloaded tiles.
