import mysql.connector
"""
mydb = mysql.connector.connect(
            host="127.0.0.1",
            user="comexys",
            password="comexys4$",
            auth_plugin='mysql_native_password'
      )

print(mydb)
"""
mydb = mysql.connector.connect(
          host="fdb5.biz.nf",
          user="2277874_aaa",
          password="Bumerang3#",
         # auth_plugin='mysql_native_password'
      )

print(mydb)
# INSERT INTO `comexys_schema`.`instalation` (`name`, `date`, `location_time`, `location.lat`, `location.long`, `qr_scaned_time`, `company`, `mac_address`, `sereal_id`) VALUES ('Perry Shoham', '2022-03-27', '11:40', '30.2345678', '40.9876543', '11:41', 'Comexys', 'aa.bb.cc.ee.ff.ee', '13A4332');

"""
CREATE TABLE `comexys_schema`.`instalation` (
  `index` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(50) NULL,
  `date` DATE NULL,
  `location_time` TIME NULL,
  `location.lat` DOUBLE NULL,
  `location.long` DOUBLE NULL,
  `qr_scaned_time` TIME NULL,
  `company` VARCHAR(20) NULL,
  `mac_address` VARCHAR(20) NULL,
  `sereal_id` VARCHAR(20) NULL,
  PRIMARY KEY (`index`),
  UNIQUE INDEX `index_UNIQUE` (`index` ASC) VISIBLE)
ENGINE = InnoDB;
"""