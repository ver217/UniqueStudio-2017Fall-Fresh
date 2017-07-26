# UniqueStudio-2017-fall-h5-backend

``` shell
pip install -U sanic-gunicorn
gunicorn --bind 0.0.0.0:8000 --worker-class sanic.worker.GunicornWorker run:app

```

``` MySQL

CREATE SCHEMA `submit_info` DEFAULT CHARACTER SET utf8 ;
USE submit_info;
CREATE TABLE `info` (
  `name` varchar(50) NOT NULL,
  `sex` varchar(10) NOT NULL,
  `college` varchar(100) NOT NULL,
  `major` varchar(100) NOT NULL,
  `grade` int(11) NOT NULL,
  `area` varchar(100) NOT NULL,
  `phone` varchar(20) NOT NULL,
  `email` varchar(50) NOT NULL,
  `team` varchar(10) NOT NULL,
  `intro` varchar(1000) NOT NULL,
  `resume` int(11) NOT NULL,
  `lasttime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8;


```