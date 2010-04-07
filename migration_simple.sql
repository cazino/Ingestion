ALTER TABLE `vendor` ENGINE = INNODB;
ALTER TABLE `album` ENGINE = INNODB;
ALTER TABLE `actualites_disque` ENGINE = INNODB;
ALTER TABLE `artist` ENGINE = INNODB;
ALTER TABLE `image_file` ENGINE = INNODB;
ALTER TABLE `country` ENGINE = INNODB;
ALTER TABLE `artist_country` ENGINE = INNODB;
ALTER TABLE `coups_de_coeur` ENGINE = INNODB;
ALTER TABLE `carrousels` ENGINE = INNODB;
ALTER TABLE `orders` ENGINE = INNODB;
ALTER TABLE `label` ENGINE = INNODB;
ALTER TABLE `track` ENGINE = INNODB;
ALTER TABLE `audio_file` ENGINE = INNODB;
ALTER TABLE `disk` ENGINE = INNODB;
ALTER TABLE `prix` ENGINE = INNODB;



CREATE TABLE `artist_vendor` (
    `artist_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `artist_id` integer NOT NULL,
    `vendor_id` integer NOT NULL,
    `external_artist_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_artist_id`)
) ENGINE InnoDB;

CREATE TABLE `label_vendor` (
    `label_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `label_id` integer NOT NULL,
    `vendor_id` integer NOT NULL,
    `external_label_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_label_id`)
) ENGINE InnoDB;

CREATE TABLE `album_vendor` (
    `album_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `album_id` integer NOT NULL UNIQUE,
    `vendor_id` integer NOT NULL,
    `external_album_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_album_id`)
) ENGINE InnoDB;
    
CREATE TABLE `track_vendor` (
    `track_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `track_id` integer NOT NULL UNIQUE,
    `external_track_id` integer NOT NULL
) ENGINE InnoDB;

ALTER TABLE `track` ADD `tra_author` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '';
ALTER TABLE `track` ADD `tra_composer` varchar(255) CHARACTER SET latin1 COLLATE latin1_swedish_ci NOT NULL DEFAULT '';


UPDATE `artist_country`
SET ac_artist_id=NULL
WHERE ac_artist_id NOT 
IN (
SELECT 
artist 
FROM 
artist
);


UPDATE `album` 
SET alb_artist_id=NULL
WHERE alb_artist_id 
NOT IN ( SELECT artist FROM artist);

UPDATE `album` 
SET alb_vendor_id=NULL
WHERE alb_vendor_id 
NOT IN ( SELECT vendor FROM vendor);

UPDATE `album` 
SET alb_label_id=NULL
WHERE alb_label_id 
NOT IN ( SELECT label FROM label);


UPDATE `image_file` 
SET ima_artist_id=NULL
WHERE ima_artist_id
NOT IN ( SELECT artist FROM artist);

UPDATE `image_file` 
SET ima_album_id=NULL
WHERE ima_album_id 
NOT IN ( SELECT album FROM album);

UPDATE `artist_country` 
SET ac_artist_id=NULL
WHERE ac_artist_id 
NOT IN ( SELECT artist FROM artist);

UPDATE `artist_country` 
SET ac_country_id=NULL
WHERE ac_country_id 
NOT IN ( SELECT country FROM country);

ALTER TABLE  `track` CHANGE  `tra_album_id`  `tra_album_id` INT( 11 ) NULL DEFAULT NULL;
UPDATE `track` 
SET tra_album_id=NULL
WHERE tra_album_id 
NOT IN (SELECT album FROM album);

UPDATE `audio_file` 
SET aud_track_id=NULL
WHERE aud_track_id 
NOT IN (SELECT track FROM track);

UPDATE `album` 
SET alb_prix=NULL
WHERE alb_prix 
NOT IN (SELECT prix FROM prix);


ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk1 FOREIGN KEY (ad_album1) REFERENCES album(album);
ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk2 FOREIGN KEY (ad_album2) REFERENCES album(album);
ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk3 FOREIGN KEY (ad_album3) REFERENCES album(album);
ALTER TABLE `album_vendor` ADD CONSTRAINT `albumvendor_album` FOREIGN KEY (`album_id`) REFERENCES `album` (`album`);
ALTER TABLE `album_vendor` ADD CONSTRAINT `albumvendor_vendor` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
ALTER TABLE `album` ADD CONSTRAINT `album_artist_fk` FOREIGN KEY (alb_artist_id) REFERENCES artist(artist);
ALTER TABLE `album` ADD CONSTRAINT `album_label_fk` FOREIGN KEY (`alb_label_id`) REFERENCES `label` (`label`);
ALTER TABLE `album` ADD CONSTRAINT `album_vendor_fk` FOREIGN KEY (`alb_vendor_id`) REFERENCES `vendor`(`vendor`);
ALTER TABLE `album` ADD CONSTRAINT `album_prix_fk` FOREIGN KEY (`alb_prix`) REFERENCES `prix` (`prix`);
ALTER TABLE `artist_country` ADD CONSTRAINT ac_artist_fk FOREIGN KEY (ac_artist_id) REFERENCES artist(artist);
ALTER TABLE `artist_country` ADD CONSTRAINT ac_country_fk FOREIGN KEY (ac_country_id) REFERENCES country(country);
ALTER TABLE `artist_vendor` ADD CONSTRAINT `av_artist_fk` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`artist`);
ALTER TABLE `artist_vendor` ADD CONSTRAINT `av_vendor_fk` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
ALTER TABLE `audio_file` ADD CONSTRAINT `audiofile_track_fk` FOREIGN KEY (`aud_track_id`) REFERENCES `track` (`track`);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk1 FOREIGN KEY (car_album1) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk10 FOREIGN KEY (car_album10) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk11 FOREIGN KEY (car_album11) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk12 FOREIGN KEY (car_album12) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk13 FOREIGN KEY (car_album13) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk14 FOREIGN KEY (car_album14) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk15 FOREIGN KEY (car_album15) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk16 FOREIGN KEY (car_album16) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk17 FOREIGN KEY (car_album17) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk18 FOREIGN KEY (car_album18) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk19 FOREIGN KEY (car_album19) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk2 FOREIGN KEY (car_album2) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk20 FOREIGN KEY (car_album20) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk3 FOREIGN KEY (car_album3) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk4 FOREIGN KEY (car_album4) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk5 FOREIGN KEY (car_album5) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk6 FOREIGN KEY (car_album6) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk7 FOREIGN KEY (car_album7) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk8 FOREIGN KEY (car_album8) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk9 FOREIGN KEY (car_album9) REFERENCES album(album);
/*ALTER TABLE `coups_de_coeur` ADD CONSTRAINT actu_disqu_fk1 FOREIGN KEY (cdc_album1) REFERENCES album(album);
ALTER TABLE `coups_de_coeur` ADD CONSTRAINT actu_disqu_fk2 FOREIGN KEY (cdc_album2) REFERENCES album(album);
ALTER TABLE `coups_de_coeur` ADD CONSTRAINT actu_disqu_fk3 FOREIGN KEY (cdc_album3) REFERENCES album(album);*/
ALTER TABLE `label_vendor` ADD CONSTRAINT `lv_label_fk` FOREIGN KEY (`label_id`) REFERENCES `label` (`label`);
ALTER TABLE `label_vendor` ADD CONSTRAINT `lv_vendor_fk` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
ALTER TABLE `image_file` ADD CONSTRAINT `image_disk_fk` FOREIGN KEY (`ima_disk_id`) REFERENCES `disk` (`disk`);
ALTER TABLE `image_file` ADD CONSTRAINT image_album_fk FOREIGN KEY (ima_album_id) REFERENCES album(album);
ALTER TABLE `image_file` ADD CONSTRAINT image_artist_fk FOREIGN KEY (ima_artist_id) REFERENCES artist(artist);
ALTER TABLE `track_vendor` ADD CONSTRAINT `track_vendor_track_fk` FOREIGN KEY (`track_id`) REFERENCES `track` (`track`);
ALTER TABLE `track` ADD CONSTRAINT `track_album_fk` FOREIGN KEY (`tra_album_id`) REFERENCES `album` (`album`);
ALTER TABLE `track` ADD CONSTRAINT `track_prix_fk` FOREIGN KEY (`tr_prix`) REFERENCES `prix` (`prix`);
CREATE INDEX `actualites_disque_ad_album1` ON `actualites_disque` (`ad_album1`);
CREATE INDEX `actualites_disque_ad_album2` ON `actualites_disque` (`ad_album2`);
CREATE INDEX `actualites_disque_ad_album3` ON `actualites_disque` (`ad_album3`);
CREATE INDEX `album_alb_artist_id` ON `album` (`alb_artist_id`);
CREATE INDEX `album_alb_label_id` ON `album` (`alb_label_id`);
CREATE INDEX `album_alb_vendor_id` ON `album` (`alb_vendor_id`);
CREATE INDEX `album_alb_prix` ON `album` (`alb_prix`);
CREATE INDEX `album_vendor_album_id` ON `album_vendor` (`album_id`);
CREATE INDEX `album_vendor_vendor_id` ON `album_vendor` (`vendor_id`);
CREATE INDEX `artist_country_ac_artist_id` ON `artist_country` (`ac_artist_id`);
CREATE INDEX `artist_country_ac_country_id` ON `artist_country` (`ac_country_id`);
CREATE INDEX `artist_vendor_artist` ON `artist_vendor` (`artist_id`);
CREATE INDEX `artist_vendor_vendor` ON `artist_vendor` (`vendor_id`);
CREATE INDEX `carrousels_car_album10` ON `carrousels` (`car_album10`);
CREATE INDEX `carrousels_car_album11` ON `carrousels` (`car_album11`);
CREATE INDEX `carrousels_car_album12` ON `carrousels` (`car_album12`);
CREATE INDEX `carrousels_car_album13` ON `carrousels` (`car_album13`);
CREATE INDEX `carrousels_car_album14` ON `carrousels` (`car_album14`);
CREATE INDEX `carrousels_car_album15` ON `carrousels` (`car_album15`);
CREATE INDEX `carrousels_car_album16` ON `carrousels` (`car_album16`);
CREATE INDEX `carrousels_car_album17` ON `carrousels` (`car_album17`);
CREATE INDEX `carrousels_car_album18` ON `carrousels` (`car_album18`);
CREATE INDEX `carrousels_car_album19` ON `carrousels` (`car_album19`);
CREATE INDEX `carrousels_car_album1` ON `carrousels` (`car_album1`);
CREATE INDEX `carrousels_car_album20` ON `carrousels` (`car_album20`);
CREATE INDEX `carrousels_car_album2` ON `carrousels` (`car_album2`);
CREATE INDEX `carrousels_car_album3` ON `carrousels` (`car_album3`);
CREATE INDEX `carrousels_car_album4` ON `carrousels` (`car_album4`);
CREATE INDEX `carrousels_car_album5` ON `carrousels` (`car_album5`);
CREATE INDEX `carrousels_car_album6` ON `carrousels` (`car_album6`);
CREATE INDEX `carrousels_car_album7` ON `carrousels` (`car_album7`);
CREATE INDEX `carrousels_car_album8` ON `carrousels` (`car_album8`);
CREATE INDEX `carrousels_car_album9` ON `carrousels` (`car_album9`);
CREATE INDEX `coups_de_coeur_cdc_album1` ON `coups_de_coeur` (`cdc_album1`);
CREATE INDEX `coups_de_coeur_cdc_album2` ON `coups_de_coeur` (`cdc_album2`);
CREATE INDEX `coups_de_coeur_cdc_album3` ON `coups_de_coeur` (`cdc_album3`);
CREATE INDEX `label_vendor_label` ON `label_vendor` (`label_id`);
CREATE INDEX `label_vendor_vendor` ON `label_vendor` (`vendor_id`);
CREATE INDEX `image_file_ima_album_id` ON `image_file` (`ima_album_id`);
CREATE INDEX `image_file_ima_artist_id` ON `image_file` (`ima_artist_id`);
CREATE INDEX `track_tr_prix` ON `track` (`tr_prix`);
CREATE INDEX `track_tra_album_id` ON `track` (`tra_album_id`);
