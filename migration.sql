ALTER TABLE `vendor` ENGINE = INNODB;
ALTER TABLE `album` ENGINE = INNODB;
ALTER TABLE `actualites_disques` ENGINE = INNODB;
ALTER TABLE `artist` ENGINE = INNODB;
ALTER TABLE `image_file` ENGINE = INNODB;
ALTER TABLE `country` ENGINE = INNODB;
ALTER TABLE `artist_country` ENGINE = INNODB;
ALTER TABLE `coups_de_coeur` ENGINE = INNODB;
ALTER TABLE `carrousels` ENGINE = INNODB;

ALTER TABLE `album` CHANGE `alb_vendor_id` `vendor_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `album` CHANGE `alb_artist_id` `artist_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `actualites_disque` CHANGE `ad_album1` `album1_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `actualites_disque` CHANGE `ad_album2` `album2_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `actualites_disque` CHANGE `ad_album3` `album3_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `image_file` CHANGE `ima_album_id` `album_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `image_file` CHANGE `ima_artist_id` `artist_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `artist_country` CHANGE `ac_artist_id` `artist_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `artist_country` CHANGE `ac_country_id` `country_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `coups_de_coeur` CHANGE `cdc_album1` `album1_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `coups_de_coeur` CHANGE `cdc_album2` `album2_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `coups_de_coeur` CHANGE `cdc_album3` `album3_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album1` `album1_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album2` `album2_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album3` `album3_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album4` `album4_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album5` `album5_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album6` `album6_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album7` `album7_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album8` `album8_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album9` `album9_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album10` `album10_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album11` `album11_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album12` `album12_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album13` `album13_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album14` `album14_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album15` `album15_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album16` `album16_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album17` `album17_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album18` `album18_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album19` `album19_id` INT( 11 ) NULL DEFAULT NULL;
ALTER TABLE `carrousels` CHANGE `car_album20` `album20_id` INT( 11 ) NULL DEFAULT NULL;


UPDATE `artist_country`
SET artist_id=NULL
WHERE artist_id NOT 
IN (
SELECT 
artist 
FROM 
artist
);

UPDATE `artist_country` 
SET country_id
=NULL
WHERE 
country_id 
NOT 
IN (
SELECT 
country 
FROM 
country
);



ALTER TABLE `album` ADD CONSTRAINT album_vendor_fk FOREIGN KEY (vendor_id) REFERENCES vendor(vendor);
ALTER TABLE `album` ADD CONSTRAINT album_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(artist);
ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk1 FOREIGN KEY (album1_id) REFERENCES album(album);
ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk2 FOREIGN KEY (album2_id) REFERENCES album(album);
ALTER TABLE `actualites_disque` ADD CONSTRAINT actu_disqu_fk3 FOREIGN KEY (album3_id) REFERENCES album(album);
ALTER TABLE `image_file` ADD CONSTRAINT image_album_fk FOREIGN KEY (album_id) REFERENCES album(album);
ALTER TABLE `image_file` ADD CONSTRAINT image_a_fk FOREIGN KEY (artist_id) REFERENCES artist(artist);
ALTER TABLE `artist_country` ADD CONSTRAINT ac_artist_fk FOREIGN KEY (artist_id) REFERENCES artist(artist);
ALTER TABLE `artist_country` ADD CONSTRAINT ac_country_fk FOREIGN KEY (country_id) REFERENCES country(country);
ALTER TABLE `
coups_de_coeur` ADD CONSTRAINT tu_cdc_album_fk1 FOREIGN KEY (album1_id) REFERENCES album(album);
ALTER TABLE `
coups_de_coeur` ADD CONSTRAINT actu_disqu_fk2 FOREIGN KEY (album2_id) REFERENCES album(album);
ALTER TABLE `
coups_de_coeur` ADD CONSTRAINT actu_disqu_fk3 FOREIGN KEY (album3_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk1 FOREIGN KEY (album1_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk2 FOREIGN KEY (album2_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk3 FOREIGN KEY (album3_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk4 FOREIGN KEY (album4_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk5 FOREIGN KEY (album5_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk6 FOREIGN KEY (album6_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk7 FOREIGN KEY (album7_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk8 FOREIGN KEY (album8_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk9 FOREIGN KEY (album9_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk10 FOREIGN KEY (album10_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk11 FOREIGN KEY (album11_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk12 FOREIGN KEY (album12_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk13 FOREIGN KEY (album13_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk14 FOREIGN KEY (album14_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk15 FOREIGN KEY (album15_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk16 FOREIGN KEY (album16_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk17 FOREIGN KEY (album17_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk18 FOREIGN KEY (album18_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk19 FOREIGN KEY (album19_id) REFERENCES album(album);
ALTER TABLE `carrousels` ADD CONSTRAINT carousel_album_fk20 FOREIGN KEY (album20_id) REFERENCES album(album);












