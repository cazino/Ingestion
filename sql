BEGIN;
CREATE TABLE `vendor` (
    `vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ven_name` varchar(255) NOT NULL UNIQUE,
    `ven_website` varchar(255) NOT NULL,
    `ven_business` varchar(255) NOT NULL,
    `ven_address` longtext NOT NULL,
    `ven_country_id` integer,
    `ven_email` varchar(255) NOT NULL,
    `ven_telephone` varchar(255) NOT NULL,
    `ven_fax` varchar(255) NOT NULL,
    `ven_mondomixContact` varchar(255) NOT NULL,
    `ven_followUp` longtext NOT NULL,
    `ven_DMDsigned` integer,
    `ven_calabashID` varchar(255) NOT NULL,
    `ven_calabashPassword` varchar(255) NOT NULL,
    `ven_notes` longtext NOT NULL,
    `ven_created` date,
    `ven_modified` date,
    `MDB` integer NOT NULL,
    `MDB2` integer NOT NULL,
    `ven_language` varchar(6) NOT NULL,
    `ven_territoires` varchar(255) NOT NULL,
    `ven_cp` varchar(150) NOT NULL,
    `ven_ville` varchar(255) NOT NULL,
    `ven_isdistrib_on_mdx` integer,
    `ven_isdistrib_on_mediatheque` integer,
    `ven_isdistrib_on_ioda` integer,
    `ven_reporting_periodicite` integer,
    `ven_magasin_mdx_rate` integer,
    `ven_distrib_mdx_rate` integer,
    `ven_distrib_mediatheque_rate` integer,
    `ven_distrib_ioda_rate` integer,
    `ven_deduction_sacem` integer,
    `ven_contrat_date_signature` date,
    `ven_contrat_length` varchar(255) NOT NULL,
    `ven_password` varchar(255) NOT NULL
)
;
CREATE TABLE `prix` (
    `prix` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pri_condition` varchar(255) NOT NULL,
    `pri_code` varchar(255) NOT NULL,
    `pri_libelle` varchar(255) NOT NULL,
    `pri_note` longtext NOT NULL,
    `pri_object_type` integer,
    `pri_prix_eur` integer,
    `pri_prix_usd` integer,
    `pri_prix_gbp` integer
)
;
CREATE TABLE `country` (
    `country` integer NOT NULL PRIMARY KEY,
    `cou_name` varchar(255) NOT NULL,
    `cou_code` varchar(12),
    `cou_iso_code` varchar(6),
    `cou_continent` varchar(150),
    `cou_currency_zone` integer,
    `cou_name_en` varchar(255) NOT NULL,
    `cou_continent_en` varchar(150),
    `cou_taxe_zone` double precision
)
;
CREATE TABLE `artist` (
    `artist` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `art_name` varchar(255) NOT NULL UNIQUE,
    `art_biography` longtext,
    `art_header` longtext,
    `art_url_rewriting` varchar(255) UNIQUE,
    `art_mondomixcom_fr` varchar(255),
    `art_mondomixcom_en` varchar(255),
    `art_mondomix_id` integer,
    `art_image` varchar(255),
    `art_thumbnail` varchar(255),
    `art_keywords` longtext,
    `art_website` varchar(255),
    `art_links_fr` longtext,
    `art_links_en` longtext,
    `art_notes` longtext,
    `art_created` date,
    `art_modified` date,
    `MDB` integer NOT NULL,
    `MDB2` integer NOT NULL,
    `EXCEL` integer NOT NULL,
    `art_type` varchar(33),
    `art_birth_date` date,
    `art_death_date` date,
    `art_header_fr` longtext,
    `art_biography_fr` longtext,
    `art_header_en` longtext,
    `art_biography_en` longtext,
    `art_calabash_url` varchar(255),
    `art_calabash_genre` integer,
    `art_calabashGenres` varchar(255),
    `art_calabashSituation` longtext,
    `art_calabashGenre` longtext,
    `art_alias` longtext,
    `art_url_rewriting2` varchar(255),
    `art_ioda_id` integer,
    `art_calimp_url_calabash` varchar(255) NOT NULL,
    `art_calimp_id_calabash` integer,
    `art_calimp_noteimport` longtext NOT NULL,
    `art_calimp_artcal_id` integer
)
;
CREATE TABLE `artist_vendor` (
    `artist_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `artist_id` integer NOT NULL,
    `vendor_id` integer NOT NULL,
    `external_artist_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_artist_id`)
)
;
ALTER TABLE `artist_vendor` ADD CONSTRAINT `artist_id_refs_artist_e55a3e3f` FOREIGN KEY (`artist_id`) REFERENCES `artist` (`artist`);
ALTER TABLE `artist_vendor` ADD CONSTRAINT `vendor_id_refs_vendor_ac20bb84` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
CREATE TABLE `artist_country` (
    `artist_country` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ac_artist_id` integer,
    `ac_country_id` integer
)
;
ALTER TABLE `artist_country` ADD CONSTRAINT `ac_artist_id_refs_artist_8abecfc6` FOREIGN KEY (`ac_artist_id`) REFERENCES `artist` (`artist`);
ALTER TABLE `artist_country` ADD CONSTRAINT `ac_country_id_refs_country_f2c5e0c` FOREIGN KEY (`ac_country_id`) REFERENCES `country` (`country`);
CREATE TABLE `label` (
    `label` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `lab_name` varchar(255) NOT NULL UNIQUE,
    `lab_created` date,
    `lab_modified` date,
    `lab_website` varchar(255),
    `MDB` integer NOT NULL,
    `EXCEL` integer NOT NULL,
    `lab_notes` longtext,
    `lab_ioda_id` varchar(150)
)
;
CREATE TABLE `label_vendor` (
    `label_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `label_id` integer NOT NULL,
    `vendor_id` integer NOT NULL,
    `external_label_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_label_id`)
)
;
ALTER TABLE `label_vendor` ADD CONSTRAINT `label_id_refs_label_e3708415` FOREIGN KEY (`label_id`) REFERENCES `label` (`label`);
ALTER TABLE `label_vendor` ADD CONSTRAINT `vendor_id_refs_vendor_cac09a00` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
CREATE TABLE `album` (
    `album` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `alb_title` varchar(255) NOT NULL,
    `alb_other_artists` longtext,
    `alb_label_id` integer,
    `alb_reference` varchar(255),
    `alb_record_year` varchar(255),
    `alb_notes` longtext,
    `alb_created` date,
    `alb_modified` date,
    `MDB` integer NOT NULL,
    `MDB2` integer NOT NULL,
    `EXCEL` integer UNSIGNED NOT NULL,
    `alb_location_media` varchar(255),
    `alb_location_shop` varchar(255),
    `alb_barcode` varchar(255),
    `alb_paperarticle` integer,
    `alb_webarticle` varchar(255),
    `alb_calabash_url` varchar(255),
    `alb_calabash_online` date,
    `alb_status_indexation` varchar(9),
    `alb_status_files` varchar(9),
    `alb_status_shop` varchar(24),
    `alb_status_media` varchar(24),
    `alb_collection_id` integer,
    `alb_domain` varchar(24),
    `alb_vendor_id` integer,
    `alb_distributor_id` integer,
    `alb_nbitems_shop` integer,
    `alb_nbitems_media` integer,
    `alb_publish_date` varchar(30),
    `alb_country_id` integer,
    `alb_text_en` longtext,
    `alb_text_fr` longtext,
    `alb_press` integer,
    `alb_keywords` longtext,
    `alb_volume` integer,
    `alb_oldstyle` varchar(255),
    `alb_status_indexation_en` varchar(9),
    `alb_status_indexation_fr` varchar(9),
    `alb_calabash_status` varchar(21),
    `alb_artist_id` integer,
    `multiartist` integer NOT NULL,
    `alb_arrival_date_media` date,
    `alb_arrival_date_shop` date,
    `alb_infos_media` varchar(255),
    `alb_infos_shop` varchar(255),
    `alb_type_media` varchar(330),
    `alb_type_shop` varchar(330),
    `alb_support_type_media` varchar(27),
    `alb_support_type_shop` varchar(27),
    `alb_nb_supports_media` integer,
    `alb_nb_supports_shop` integer,
    `alb_prix` integer,
    `alb_territoires` longtext,
    `alb_publish_date_digital` date,
    `alb_publish_date2` date,
    `alb_ioda_id` integer
)
;
ALTER TABLE `album` ADD CONSTRAINT `alb_label_id_refs_label_ee1280e6` FOREIGN KEY (`alb_label_id`) REFERENCES `label` (`label`);
ALTER TABLE `album` ADD CONSTRAINT `alb_vendor_id_refs_vendor_9d5b13e9` FOREIGN KEY (`alb_vendor_id`) REFERENCES `vendor` (`vendor`);
ALTER TABLE `album` ADD CONSTRAINT `alb_artist_id_refs_artist_6ee2db8e` FOREIGN KEY (`alb_artist_id`) REFERENCES `artist` (`artist`);
ALTER TABLE `album` ADD CONSTRAINT `alb_prix_refs_prix_30fac930` FOREIGN KEY (`alb_prix`) REFERENCES `prix` (`prix`);
CREATE TABLE `album_vendor` (
    `album_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `album_id` integer NOT NULL,
    `vendor_id` integer NOT NULL,
    `external_album_id` integer NOT NULL,
    UNIQUE (`vendor_id`, `external_album_id`)
)
;
ALTER TABLE `album_vendor` ADD CONSTRAINT `album_id_refs_album_81881025` FOREIGN KEY (`album_id`) REFERENCES `album` (`album`);
ALTER TABLE `album_vendor` ADD CONSTRAINT `vendor_id_refs_vendor_a023cbb9` FOREIGN KEY (`vendor_id`) REFERENCES `vendor` (`vendor`);
CREATE TABLE `disk` (
    `disk` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `dik_name` varchar(255),
    `dik_status` varchar(21),
    `dik_path` varchar(255),
    `dik_mountpoint` varchar(255),
    `dik_description` longtext
)
;
CREATE TABLE `image_file` (
    `image_file` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ima_album_id` integer,
    `ima_artist_id` integer,
    `ima_filepath` varchar(255),
    `ima_disk_id` integer NOT NULL,
    `ima_format` varchar(9) NOT NULL,
    `ima_filesize` integer,
    `ima_width` integer,
    `ima_height` integer,
    `ima_quality` integer,
    `ima_usage` varchar(60) NOT NULL
)
;
ALTER TABLE `image_file` ADD CONSTRAINT `ima_album_id_refs_album_1e780577` FOREIGN KEY (`ima_album_id`) REFERENCES `album` (`album`);
ALTER TABLE `image_file` ADD CONSTRAINT `ima_artist_id_refs_artist_97a1e4b8` FOREIGN KEY (`ima_artist_id`) REFERENCES `artist` (`artist`);
ALTER TABLE `image_file` ADD CONSTRAINT `ima_disk_id_refs_disk_79dcbd84` FOREIGN KEY (`ima_disk_id`) REFERENCES `disk` (`disk`);
CREATE TABLE `track` (
    `track` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `tra_album_id` integer NOT NULL,
    `tra_support_number` integer,
    `tra_track_number` integer,
    `tra_title` varchar(255) NOT NULL,
    `tra_price` integer,
    `tra_ISRC` varchar(36),
    `tra_status` varchar(27) NOT NULL,
    `tra_created` date,
    `tra_modified` date,
    `MDB` integer NOT NULL,
    `MDB2` integer NOT NULL,
    `tra_artist_id` integer,
    `tr_prix` integer,
    `tra_mdxteam_rating` integer,
    `tra_vente_albumbundle_only` integer,
    `tra_vente_track_only` integer,
    `tr_notes` longtext NOT NULL,
    `tra_ioda_id` integer,
    `tra_author` varchar(255) NOT NULL,
    `tra_composer` varchar(255) NOT NULL
)
;
ALTER TABLE `track` ADD CONSTRAINT `tra_album_id_refs_album_69a5beb` FOREIGN KEY (`tra_album_id`) REFERENCES `album` (`album`);
ALTER TABLE `track` ADD CONSTRAINT `tr_prix_refs_prix_2e363e98` FOREIGN KEY (`tr_prix`) REFERENCES `prix` (`prix`);
CREATE TABLE `track_vendor` (
    `track_vendor` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `track_id` integer NOT NULL UNIQUE,
    `external_track_id` integer NOT NULL
)
;
ALTER TABLE `track_vendor` ADD CONSTRAINT `track_id_refs_track_f84cfbcb` FOREIGN KEY (`track_id`) REFERENCES `track` (`track`);
CREATE TABLE `audio_file` (
    `audio_file` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `aud_filepath` varchar(255) NOT NULL,
    `aud_disk_id` integer,
    `aud_content` varchar(21),
    `aud_format` varchar(12),
    `aud_filesize` integer,
    `aud_duration` integer,
    `aud_bitrate` integer,
    `aud_frequency` integer,
    `aud_mode` varchar(36),
    `aud_track_id` integer,
    `aud_tags` integer,
    `aud_iodaimp_id` integer
)
;
ALTER TABLE `audio_file` ADD CONSTRAINT `aud_disk_id_refs_disk_744dedd5` FOREIGN KEY (`aud_disk_id`) REFERENCES `disk` (`disk`);
ALTER TABLE `audio_file` ADD CONSTRAINT `aud_track_id_refs_track_c5bc0b72` FOREIGN KEY (`aud_track_id`) REFERENCES `track` (`track`);
CREATE TABLE `actualites_disque` (
    `actualites_disque` integer NOT NULL PRIMARY KEY,
    `ad_semaine` varchar(255) NOT NULL,
    `ad_date_creation` datetime,
    `ad_album1` integer NOT NULL,
    `ad_album2` integer NOT NULL,
    `ad_album3` integer NOT NULL,
    `ad_localisation` integer
)
;
ALTER TABLE `actualites_disque` ADD CONSTRAINT `ad_album1_refs_album_a3a0f79d` FOREIGN KEY (`ad_album1`) REFERENCES `album` (`album`);
ALTER TABLE `actualites_disque` ADD CONSTRAINT `ad_album2_refs_album_a3a0f79d` FOREIGN KEY (`ad_album2`) REFERENCES `album` (`album`);
ALTER TABLE `actualites_disque` ADD CONSTRAINT `ad_album3_refs_album_a3a0f79d` FOREIGN KEY (`ad_album3`) REFERENCES `album` (`album`);
CREATE TABLE `coups_de_coeur` (
    `coups_de_coeur` integer NOT NULL PRIMARY KEY,
    `cdc_label` varchar(255) NOT NULL,
    `cdc_album1` integer NOT NULL,
    `cdc_album2` integer NOT NULL,
    `cdc_album3` integer NOT NULL,
    `cdc_date_creation` date,
    `cdc_localisation` integer
)
;
ALTER TABLE `coups_de_coeur` ADD CONSTRAINT `cdc_album1_refs_album_4b2578a0` FOREIGN KEY (`cdc_album1`) REFERENCES `album` (`album`);
ALTER TABLE `coups_de_coeur` ADD CONSTRAINT `cdc_album2_refs_album_4b2578a0` FOREIGN KEY (`cdc_album2`) REFERENCES `album` (`album`);
ALTER TABLE `coups_de_coeur` ADD CONSTRAINT `cdc_album3_refs_album_4b2578a0` FOREIGN KEY (`cdc_album3`) REFERENCES `album` (`album`);
CREATE TABLE `carrousels` (
    `carrousels` integer NOT NULL PRIMARY KEY,
    `car_titre` varchar(255) NOT NULL,
    `car_langue` integer,
    `car_pagegenre` integer,
    `car_pagecontinent` integer,
    `car_album1` integer NOT NULL,
    `car_album2` integer NOT NULL,
    `car_album3` integer NOT NULL,
    `car_album4` integer NOT NULL,
    `car_album5` integer NOT NULL,
    `car_album6` integer NOT NULL,
    `car_album7` integer NOT NULL,
    `car_album8` integer NOT NULL,
    `car_album9` integer NOT NULL,
    `car_album10` integer NOT NULL,
    `car_album11` integer NOT NULL,
    `car_album12` integer NOT NULL,
    `car_album13` integer NOT NULL,
    `car_album14` integer NOT NULL,
    `car_album15` integer NOT NULL,
    `car_album16` integer NOT NULL,
    `car_album17` integer NOT NULL,
    `car_album18` integer NOT NULL,
    `car_album19` integer NOT NULL,
    `car_album20` integer NOT NULL,
    `car_date_creation` date,
    `car_date_maj` date
)
;
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album1_refs_album_25d98c4a` FOREIGN KEY (`car_album1`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album2_refs_album_25d98c4a` FOREIGN KEY (`car_album2`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album3_refs_album_25d98c4a` FOREIGN KEY (`car_album3`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album4_refs_album_25d98c4a` FOREIGN KEY (`car_album4`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album5_refs_album_25d98c4a` FOREIGN KEY (`car_album5`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album6_refs_album_25d98c4a` FOREIGN KEY (`car_album6`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album7_refs_album_25d98c4a` FOREIGN KEY (`car_album7`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album8_refs_album_25d98c4a` FOREIGN KEY (`car_album8`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album9_refs_album_25d98c4a` FOREIGN KEY (`car_album9`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album10_refs_album_25d98c4a` FOREIGN KEY (`car_album10`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album11_refs_album_25d98c4a` FOREIGN KEY (`car_album11`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album12_refs_album_25d98c4a` FOREIGN KEY (`car_album12`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album13_refs_album_25d98c4a` FOREIGN KEY (`car_album13`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album14_refs_album_25d98c4a` FOREIGN KEY (`car_album14`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album15_refs_album_25d98c4a` FOREIGN KEY (`car_album15`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album16_refs_album_25d98c4a` FOREIGN KEY (`car_album16`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album17_refs_album_25d98c4a` FOREIGN KEY (`car_album17`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album18_refs_album_25d98c4a` FOREIGN KEY (`car_album18`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album19_refs_album_25d98c4a` FOREIGN KEY (`car_album19`) REFERENCES `album` (`album`);
ALTER TABLE `carrousels` ADD CONSTRAINT `car_album20_refs_album_25d98c4a` FOREIGN KEY (`car_album20`) REFERENCES `album` (`album`);
CREATE TABLE `affiliate` (
    `affiliate` integer NOT NULL PRIMARY KEY,
    `aff_nom` varchar(255) NOT NULL,
    `aff_url` varchar(255) NOT NULL
)
;
CREATE TABLE `aidefaq` (
    `aidefaq` integer NOT NULL PRIMARY KEY,
    `aid_categorieaide` integer,
    `aid_order` integer,
    `aid_texte` longtext NOT NULL,
    `aid_titre` varchar(255) NOT NULL
)
;
CREATE TABLE `album_artist` (
    `album_artist` integer NOT NULL PRIMARY KEY,
    `aa_album_id` integer,
    `aa_artist_id` integer,
    `EXCEL` integer NOT NULL
)
;
CREATE TABLE `album_country` (
    `album_country` integer NOT NULL PRIMARY KEY,
    `alco_album_id` integer,
    `alco_country_id` integer
)
;
CREATE TABLE `album_instrument` (
    `album_instrument` integer NOT NULL PRIMARY KEY,
    `alin_album_id` integer,
    `alin_instrument_id` integer
)
;
CREATE TABLE `album_style` (
    `album_style` integer NOT NULL PRIMARY KEY,
    `as_style_id` integer,
    `as_album_id` integer
)
;
CREATE TABLE `article` (
    `article` integer NOT NULL PRIMARY KEY,
    `atc_type` varchar(27) NOT NULL,
    `atc_language_id` varchar(255) NOT NULL,
    `atc_title` varchar(255) NOT NULL,
    `atc_header` longtext NOT NULL,
    `atc_text` longtext NOT NULL,
    `atc_author` varchar(255) NOT NULL,
    `atc_origin` varchar(255) NOT NULL,
    `atc_publishing_date` date,
    `atc_created` date,
    `atc_modified` date
)
;
CREATE TABLE `artist_noimportcalabash` (
    `artist` integer NOT NULL PRIMARY KEY,
    `art_name` varchar(255) NOT NULL UNIQUE,
    `art_biography` longtext NOT NULL,
    `art_header` longtext NOT NULL,
    `art_url_rewriting` varchar(255) NOT NULL,
    `art_mondomixcom_fr` varchar(255) NOT NULL,
    `art_mondomixcom_en` varchar(255) NOT NULL,
    `art_mondomix_id` integer,
    `art_image` varchar(255) NOT NULL,
    `art_thumbnail` varchar(255) NOT NULL,
    `art_keywords` longtext NOT NULL,
    `art_website` varchar(255) NOT NULL,
    `art_links_fr` longtext NOT NULL,
    `art_links_en` longtext NOT NULL,
    `art_notes` longtext NOT NULL,
    `art_created` date,
    `art_modified` date,
    `MDB` integer NOT NULL,
    `MDB2` integer NOT NULL,
    `EXCEL` integer NOT NULL,
    `art_type` varchar(33) NOT NULL,
    `art_birth_date` date,
    `art_death_date` date,
    `art_header_fr` longtext NOT NULL,
    `art_biography_fr` longtext NOT NULL,
    `art_header_en` longtext NOT NULL,
    `art_biography_en` longtext NOT NULL,
    `art_calabash_url` varchar(255) NOT NULL,
    `art_calabash_genre` integer,
    `art_calabashGenres` varchar(255) NOT NULL,
    `art_calabashSituation` longtext NOT NULL,
    `art_calabashGenre` longtext NOT NULL,
    `art_alias` longtext NOT NULL,
    `art_url_rewriting2` varchar(255) NOT NULL,
    `art_ioda_id` integer
)
;
CREATE TABLE `auteur` (
    `auteur` integer NOT NULL PRIMARY KEY,
    `aut_login` varchar(60) NOT NULL UNIQUE,
    `aut_lastname` varchar(75) NOT NULL,
    `aut_firstname` varchar(75) NOT NULL,
    `aut_pwd` varchar(150) NOT NULL,
    `aut_privilege` integer,
    `aut_email` varchar(240) NOT NULL,
    `aut_active` varchar(3) NOT NULL,
    `aut_type` varchar(21) NOT NULL,
    `aut_reportto` varchar(60) NOT NULL
)
;
CREATE TABLE `bug_tracking` (
    `bug_tracking` integer NOT NULL PRIMARY KEY,
    `bt_raw_datas` longtext NOT NULL,
    `bt_timestamp` datetime NOT NULL
)
;
CREATE TABLE `cadi_007` (
    `cadi_007` integer NOT NULL PRIMARY KEY,
    `cadi_jstag` varchar(255) NOT NULL,
    `cadi_ip` varchar(255) NOT NULL,
    `cadi_session` varchar(255) NOT NULL,
    `cadi_cookie` varchar(255) NOT NULL,
    `cadi_url` varchar(255) NOT NULL,
    `cadi_datetime` datetime NOT NULL
)
;
CREATE TABLE `calabash_genre` (
    `calabash_genre` integer NOT NULL PRIMARY KEY,
    `cag_name` varchar(255) NOT NULL,
    `cag_number` integer
)
;
CREATE TABLE `calabashdownloads` (
    `calabashdownloads` integer NOT NULL PRIMARY KEY,
    `cdw_track_item_id` integer NOT NULL,
    `cdw_album_item_id` integer NOT NULL,
    `cdw_artist_item_id` integer NOT NULL,
    `cdw_tracktitle` longtext NOT NULL,
    `cdw_albumname` longtext NOT NULL,
    `cdw_artistname` longtext NOT NULL,
    `cdw_artist_url_calabash` varchar(255) NOT NULL,
    `cdw_artist_url_mondomix` varchar(255) NOT NULL,
    `cdw_pathmp3` longtext NOT NULL,
    `cdw_filesize` varchar(255) NOT NULL,
    `cdw_mimetype` varchar(255) NOT NULL
)
;
CREATE TABLE `calabashdownloads_account` (
    `account_calabashdownloads` integer NOT NULL PRIMARY KEY,
    `adl_account` integer NOT NULL,
    `adl_calabashdownloads` integer NOT NULL,
    `adl_orderdate` datetime NOT NULL
)
;
CREATE TABLE `categorieaide` (
    `categorieaide` integer NOT NULL PRIMARY KEY,
    `cat_version` integer,
    `cat_order` integer,
    `cat_titremenu` varchar(255) NOT NULL,
    `cat_titrelong` longtext NOT NULL
)
;
CREATE TABLE `category` (
    `category` integer NOT NULL PRIMARY KEY,
    `cat_name` varchar(255) NOT NULL UNIQUE,
    `cat_order` integer UNIQUE,
    `cat_created` date,
    `cat_modified` date,
    `cat_name_en` varchar(255) NOT NULL
)
;
CREATE TABLE `category_style` (
    `category_style` integer NOT NULL PRIMARY KEY,
    `cs_style_id` integer,
    `cs_category_id` integer
)
;
CREATE TABLE `collection` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `collection` integer NOT NULL,
    `col_name` varchar(255) NOT NULL,
    `EXCEL` integer NOT NULL,
    `col_notes` longtext NOT NULL,
    `col_created` date,
    `col_modified` date
)
;
CREATE TABLE `commentaires` (
    `commentaires` integer NOT NULL PRIMARY KEY,
    `com_user_id` varchar(255) NOT NULL,
    `com_titre` varchar(255) NOT NULL,
    `com_texte` longtext NOT NULL,
    `com_date_creation` datetime,
    `com_isPublished` integer,
    `com_album_id` integer
)
;
CREATE TABLE `contact` (
    `contact` integer NOT NULL PRIMARY KEY,
    `con_name` varchar(255) NOT NULL,
    `con_position` varchar(255) NOT NULL,
    `con_address` longtext NOT NULL,
    `con_country_id` integer,
    `con_phone` varchar(255) NOT NULL,
    `con_mobile` varchar(255) NOT NULL,
    `con_fax` varchar(255) NOT NULL,
    `con_email` varchar(255) NOT NULL,
    `con_vendor_id` integer,
    `con_distributor_id` integer,
    `con_label_id` integer,
    `con_artist_id` integer,
    `con_notes` longtext NOT NULL,
    `con_created` date,
    `con_modified` date
)
;
CREATE TABLE `country_backup` (
    `country` integer NOT NULL PRIMARY KEY,
    `cou_name` varchar(255) NOT NULL,
    `cou_code` varchar(12) NOT NULL,
    `cou_iso_code` varchar(6) NOT NULL,
    `cou_created` date,
    `cou_modified` date,
    `image` longtext NOT NULL
)
;
CREATE TABLE `profil_sessions` (
    `profil_sessions` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ps_session_id` varchar(255) NOT NULL UNIQUE,
    `ps_user_ip` varchar(90) NOT NULL,
    `ps_useraccount_id` integer,
    `ps_date_start` datetime,
    `ps_store_id` integer,
    `ps_localtime` varchar(15) NOT NULL,
    `ps_session_dotCom` varchar(255) NOT NULL,
    `ps_date_end` datetime,
    `ps_cadi_cookie` varchar(255) NOT NULL,
    `ps_country` varchar(3) NOT NULL
)
;
CREATE TABLE `country_ip` (
    `country_ip` integer NOT NULL PRIMARY KEY,
    `ci_ip_from` double precision NOT NULL,
    `ci_ip_to` double precision NOT NULL,
    `ci_country_code2` varchar(6) NOT NULL,
    `ci_country_code3` varchar(9) NOT NULL,
    `ci_country_name` varchar(300) NOT NULL
)
;
CREATE TABLE `country_iso_en` (
    `id` integer NOT NULL PRIMARY KEY,
    `name` varchar(255) NOT NULL,
    `code` varchar(6) NOT NULL
)
;
CREATE TABLE `credits` (
    `credits` integer NOT NULL PRIMARY KEY,
    `cre_libelle_fr` varchar(255) NOT NULL,
    `cre_nb_credit` integer,
    `cre_prix` integer,
    `cre_validite` integer,
    `cre_libelle_en` varchar(255) NOT NULL
)
;
ALTER TABLE `credits` ADD CONSTRAINT `cre_prix_refs_prix_b31818bd` FOREIGN KEY (`cre_prix`) REFERENCES `prix` (`prix`);
CREATE TABLE `portefeuille_credit` (
    `portefeuille_credit` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pc_user_id` integer NOT NULL,
    `pc_nb_credit` integer NOT NULL,
    `pc_currency` varchar(9) NOT NULL,
    `pc_unit_amount` double precision,
    `pc_exchange_rate` double precision,
    `pc_created` datetime,
    `pc_modified` datetime
)
;
CREATE TABLE `currency` (
    `currency` integer NOT NULL PRIMARY KEY,
    `cur_name` varchar(9) NOT NULL
)
;
CREATE TABLE `distributor` (
    `distributor` integer NOT NULL PRIMARY KEY,
    `dis_name` varchar(255) NOT NULL UNIQUE,
    `dis_website` varchar(255) NOT NULL,
    `dis_notes` longtext NOT NULL,
    `EXCEL` integer NOT NULL,
    `dis_created` date,
    `dis_modified` date
)
;
CREATE TABLE `eticket` (
    `eticket` integer NOT NULL PRIMARY KEY,
    `eti_profile` integer NOT NULL,
    `eti_mail` varchar(255) NOT NULL,
    `eti_nom` varchar(255) NOT NULL,
    `eti_prenom` varchar(255) NOT NULL,
    `eti_subject` varchar(255) NOT NULL,
    `eti_message` longtext NOT NULL,
    `eti_reply` longtext NOT NULL,
    `eti_priority` integer NOT NULL,
    `eti_datetime` datetime NOT NULL,
    `eti_os` varchar(255) NOT NULL,
    `eti_browser` varchar(255) NOT NULL,
    `eti_language` varchar(255) NOT NULL,
    `eti_status` varchar(60) NOT NULL
)
;
CREATE TABLE `genres_focus` (
    `genres_focus` integer NOT NULL PRIMARY KEY,
    `gf_label` varchar(255) NOT NULL,
    `gf_album1` integer,
    `gf_album2` integer,
    `gf_album3` integer,
    `gf_localisation` integer,
    `gf_album4` integer,
    `gf_album5` integer,
    `gf_album6` integer,
    `gf_date_creation` date,
    `gf_album_master` integer
)
;
CREATE TABLE `highlight_types` (
    `highlight_types` integer NOT NULL PRIMARY KEY,
    `ht_label` varchar(255) NOT NULL
)
;
CREATE TABLE `image_file_noimportcalabash` (
    `image_file` integer NOT NULL PRIMARY KEY,
    `ima_album_id` integer,
    `ima_artist_id` integer,
    `ima_filepath` varchar(255) NOT NULL,
    `ima_disk_id` integer,
    `ima_format` varchar(9) NOT NULL,
    `ima_filesize` integer,
    `ima_width` integer,
    `ima_height` integer,
    `ima_quality` integer,
    `ima_usage` varchar(60) NOT NULL
)
;
CREATE TABLE `instrument` (
    `instrument` integer NOT NULL PRIMARY KEY,
    `ins_name` varchar(255) NOT NULL,
    `ins_name_en` varchar(255) NOT NULL
)
;
CREATE TABLE `languages` (
    `languages` integer NOT NULL PRIMARY KEY,
    `lan_name` varchar(255) NOT NULL,
    `lan_code` varchar(30) NOT NULL,
    `lan_created` date,
    `lan_currency_symbol` varchar(30) NOT NULL,
    `lan_currency_code` varchar(30) NOT NULL,
    `lan_currency_converTaux` varchar(30) NOT NULL,
    `lan_format_date` varchar(60) NOT NULL,
    `lan_currency_label_zone` varchar(450) NOT NULL
)
;
CREATE TABLE `log_recherche` (
    `recherche_id` integer NOT NULL PRIMARY KEY,
    `session_id` varchar(300) NOT NULL,
    `visit_at` datetime NOT NULL,
    `keywords` longtext NOT NULL
)
;
CREATE TABLE `mdb_country` (
    `id` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pays` longtext NOT NULL,
    `code_pays` longtext NOT NULL,
    `italien` longtext NOT NULL,
    `espagnol` longtext NOT NULL,
    `anglais` longtext NOT NULL,
    `allemand` longtext NOT NULL,
    `indicatif` longtext NOT NULL
)
;
CREATE TABLE `multiartist` (
    `album` integer NOT NULL PRIMARY KEY,
    `nb` integer NOT NULL
)
;
CREATE TABLE `newsletter` (
    `newsletter` integer NOT NULL PRIMARY KEY,
    `nl_email` varchar(255) NOT NULL,
    `nl_langue` varchar(30) NOT NULL,
    `nl_date_creation` date NOT NULL,
    `nl_session_id` varchar(255) NOT NULL,
    `nl_imported` varchar(3) NOT NULL
)
;
CREATE TABLE `paniers` (
    `paniers` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pa_user_session` varchar(255) NOT NULL,
    `pa_date_start` datetime,
    `pa_date_end` datetime
)
;
ALTER TABLE `paniers` ADD CONSTRAINT `pa_user_session_refs_ps_session_id_d248d91f` FOREIGN KEY (`pa_user_session`) REFERENCES `profil_sessions` (`ps_session_id`);
CREATE TABLE `panier_items` (
    `panier_items` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pi_object_id` integer,
    `pi_object_type` integer,
    `pi_panier_id` integer,
    `pi_date_update` datetime,
    `pi_date_suppr` datetime,
    `pi_date_DL` datetime NOT NULL,
    `pi_object_official_current_price` double precision NOT NULL,
    `pi_objet_real_current_price` double precision NOT NULL
)
;
ALTER TABLE `panier_items` ADD CONSTRAINT `pi_panier_id_refs_paniers_6c3b5bfe` FOREIGN KEY (`pi_panier_id`) REFERENCES `paniers` (`paniers`);
CREATE TABLE `orders` (
    `orders` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `ord_user_id` integer,
    `ord_cart_id` integer,
    `ord_price` double precision,
    `ord_status` varchar(75),
    `pp_txn_id` varchar(75),
    `pp_payment_status` varchar(75),
    `pp_payer_id` varchar(75),
    `pp_payer_status` varchar(75),
    `pp_mc_gross` double precision,
    `pp_mc_fee` double precision,
    `pp_mc_currency` varchar(9),
    `pp_residence_country` varchar(9),
    `pp_settle_amount` double precision,
    `pp_exchange_rate` double precision,
    `pp_reason_code` varchar(255),
    `pp_pending_reason` varchar(255),
    `pp_raw_datas` longtext,
    `ord_created` datetime,
    `ord_modified` datetime,
    `ord_validated` datetime
)
;
ALTER TABLE `orders` ADD CONSTRAINT `ord_cart_id_refs_paniers_83ac4327` FOREIGN KEY (`ord_cart_id`) REFERENCES `paniers` (`paniers`);
CREATE TABLE `panier_items_finance` (
    `panier_items_finance` integer NOT NULL PRIMARY KEY,
    `pif_panier_item` integer NOT NULL,
    `pif_object_parent_id` integer NOT NULL,
    `pif_object_parent_type` integer NOT NULL,
    `pif_object_type` integer NOT NULL,
    `pif_object_id` integer NOT NULL,
    `pif_object_price_l10n` double precision NOT NULL,
    `pif_object_parent_price_l10n` double precision NOT NULL,
    `pif_currency` varchar(15) NOT NULL,
    `pif_exchange_rate` double precision NOT NULL,
    `pif_residence_country` varchar(15) NOT NULL,
    `pif_txn_type` varchar(255) NOT NULL,
    `pif_ord_validated` datetime NOT NULL,
    `pif_datetime` datetime NOT NULL
)
;
CREATE TABLE `pays` (
    `pays` integer NOT NULL PRIMARY KEY,
    `pay_nom` varchar(192) NOT NULL,
    `eng_pay_nom` varchar(255) NOT NULL,
    `pay_isocode2` varchar(6) NOT NULL,
    `pay_continent` varchar(150) NOT NULL
)
;
CREATE TABLE `platform` (
    `platform` integer NOT NULL PRIMARY KEY,
    `pla_name` varchar(255) NOT NULL,
    `pla_code` varchar(255) NOT NULL
)
;
CREATE TABLE `prix_historique` (
    `prix_historique` integer NOT NULL PRIMARY KEY,
    `ph_modification_date` datetime,
    `ph_objet_id` integer,
    `ph_objet_type` integer,
    `ph_objet_prix_eur` integer,
    `ph_objet_prix_usd` integer,
    `ph_objet_prix_gbp` integer
)
;
CREATE TABLE `profil` (
    `profil` integer AUTO_INCREMENT NOT NULL PRIMARY KEY,
    `pro_wallet_mdx_solde` integer,
    `pro_wallet_clb_solde` integer,
    `pro_mondomix_id` integer
)
;
CREATE TABLE `profil_backupmigration` (
    `profil` integer NOT NULL PRIMARY KEY,
    `pro_email` varchar(255) NOT NULL,
    `pro_password` varchar(255) NOT NULL,
    `pro_genre` integer,
    `pro_datebirth` varchar(255) NOT NULL,
    `pro_language` integer,
    `pro_createdatetime` date,
    `pro_firstname` varchar(255) NOT NULL,
    `pro_name` varchar(255) NOT NULL,
    `pro_wallet_solde` integer,
    `pro_isActived` integer,
    `pro_date_activation` date,
    `pro_typeUser` integer,
    `pro_photo` longtext NOT NULL,
    `pro_mondomix_id` integer
)
;
CREATE TABLE `profil_oldbeforeimportcalabash` (
    `profil` integer NOT NULL PRIMARY KEY,
    `pro_wallet_mdx_solde` integer,
    `pro_wallet_clb_solde` integer,
    `pro_mondomix_id` integer
)
;
CREATE TABLE `project_artist` (
    `project_artist` integer NOT NULL PRIMARY KEY,
    `prar_project_id` integer,
    `prar_artist_id` integer
)
;
CREATE TABLE `promotions` (
    `promotions` integer NOT NULL PRIMARY KEY,
    `pr_libelle` varchar(255) NOT NULL,
    `pr_img_homepage` longtext NOT NULL,
    `pr_texte` longtext NOT NULL,
    `pr_image` longtext NOT NULL,
    `pr_prix_id` integer,
    `pr_date_start` date,
    `pr_date_stop` date,
    `pr_promo_pageid` integer,
    `pr_image_alt` varchar(255) NOT NULL
)
;
CREATE TABLE `radioplaylist` (
    `radioplaylist` integer NOT NULL PRIMARY KEY,
    `rad_statut` varchar(150) NOT NULL,
    `rad_name` varchar(255) NOT NULL
)
;
CREATE TABLE `radiotracks` (
    `radiotracks` integer NOT NULL PRIMARY KEY,
    `rad_radioplaylist` integer NOT NULL,
    `rad_trackid` integer
)
;
CREATE TABLE `rating` (
    `rating` integer NOT NULL PRIMARY KEY,
    `rat_user_id` varchar(255) NOT NULL,
    `rat_album_id` integer,
    `rat_score` integer,
    `rat_date_creation` datetime
)
;
CREATE TABLE `send_to_friend` (
    `send_to_friend` integer NOT NULL PRIMARY KEY,
    `s2f_user_id` varchar(255) NOT NULL,
    `s2f_texte` varchar(255) NOT NULL,
    `s2f_album_id` integer,
    `s2f_email_to` varchar(255) NOT NULL,
    `s2f_date_creation` datetime,
    `s2f_nom_from` varchar(255) NOT NULL
)
;
CREATE TABLE `statement` (
    `id` integer NOT NULL PRIMARY KEY,
    `sta_year` integer NOT NULL,
    `sta_quarter` integer NOT NULL,
    `sta_platform_name` varchar(255) NOT NULL,
    `sta_provider_name` varchar(255) NOT NULL,
    `sta_track_title` varchar(255) NOT NULL,
    `sta_artist_name` varchar(255) NOT NULL,
    `sta_album_title` varchar(255) NOT NULL,
    `sta_quantity` integer NOT NULL,
    `sta_net_price` double precision,
    `sta_provider_rate` double precision NOT NULL,
    `sta_track_isrc` varchar(36) NOT NULL,
    `sta_track_id` integer,
    `sta_track_nb` integer,
    `sta_track_cd_nb` integer,
    `sta_artist_id` integer,
    `sta_album_id` integer,
    `sta_provider_id` integer,
    `sta_platform_id` integer NOT NULL
)
;
CREATE TABLE `statistiques` (
    `statistiques` integer NOT NULL PRIMARY KEY
)
;
CREATE TABLE `style` (
    `style` integer NOT NULL PRIMARY KEY,
    `sty_name` varchar(255) NOT NULL UNIQUE,
    `sty_created` date,
    `sty_modified` date,
    `sty_name_en` varchar(255) NOT NULL
)
;
CREATE TABLE `xport_mp3_img` (
    `termine` integer NOT NULL PRIMARY KEY,
    `objet_id` integer NOT NULL,
    `objet_type` varchar(255) NOT NULL,
    `date_validation` datetime NOT NULL,
    `is_uploaded` integer NOT NULL,
    `date_upload` datetime NOT NULL,
    `objet_disk` integer NOT NULL
)
;
CREATE INDEX `artist_vendor_artist_id` ON `artist_vendor` (`artist_id`);
CREATE INDEX `artist_vendor_vendor_id` ON `artist_vendor` (`vendor_id`);
CREATE INDEX `artist_country_ac_artist_id` ON `artist_country` (`ac_artist_id`);
CREATE INDEX `artist_country_ac_country_id` ON `artist_country` (`ac_country_id`);
CREATE INDEX `label_vendor_label_id` ON `label_vendor` (`label_id`);
CREATE INDEX `label_vendor_vendor_id` ON `label_vendor` (`vendor_id`);
CREATE INDEX `album_alb_label_id` ON `album` (`alb_label_id`);
CREATE INDEX `album_alb_vendor_id` ON `album` (`alb_vendor_id`);
CREATE INDEX `album_alb_artist_id` ON `album` (`alb_artist_id`);
CREATE INDEX `album_alb_prix` ON `album` (`alb_prix`);
CREATE INDEX `album_vendor_album_id` ON `album_vendor` (`album_id`);
CREATE INDEX `album_vendor_vendor_id` ON `album_vendor` (`vendor_id`);
CREATE INDEX `image_file_ima_album_id` ON `image_file` (`ima_album_id`);
CREATE INDEX `image_file_ima_artist_id` ON `image_file` (`ima_artist_id`);
CREATE INDEX `image_file_ima_disk_id` ON `image_file` (`ima_disk_id`);
CREATE INDEX `track_tra_album_id` ON `track` (`tra_album_id`);
CREATE INDEX `track_tr_prix` ON `track` (`tr_prix`);
CREATE INDEX `audio_file_aud_disk_id` ON `audio_file` (`aud_disk_id`);
CREATE INDEX `audio_file_aud_track_id` ON `audio_file` (`aud_track_id`);
CREATE INDEX `actualites_disque_ad_album1` ON `actualites_disque` (`ad_album1`);
CREATE INDEX `actualites_disque_ad_album2` ON `actualites_disque` (`ad_album2`);
CREATE INDEX `actualites_disque_ad_album3` ON `actualites_disque` (`ad_album3`);
CREATE INDEX `coups_de_coeur_cdc_album1` ON `coups_de_coeur` (`cdc_album1`);
CREATE INDEX `coups_de_coeur_cdc_album2` ON `coups_de_coeur` (`cdc_album2`);
CREATE INDEX `coups_de_coeur_cdc_album3` ON `coups_de_coeur` (`cdc_album3`);
CREATE INDEX `carrousels_car_album1` ON `carrousels` (`car_album1`);
CREATE INDEX `carrousels_car_album2` ON `carrousels` (`car_album2`);
CREATE INDEX `carrousels_car_album3` ON `carrousels` (`car_album3`);
CREATE INDEX `carrousels_car_album4` ON `carrousels` (`car_album4`);
CREATE INDEX `carrousels_car_album5` ON `carrousels` (`car_album5`);
CREATE INDEX `carrousels_car_album6` ON `carrousels` (`car_album6`);
CREATE INDEX `carrousels_car_album7` ON `carrousels` (`car_album7`);
CREATE INDEX `carrousels_car_album8` ON `carrousels` (`car_album8`);
CREATE INDEX `carrousels_car_album9` ON `carrousels` (`car_album9`);
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
CREATE INDEX `carrousels_car_album20` ON `carrousels` (`car_album20`);
CREATE INDEX `credits_cre_prix` ON `credits` (`cre_prix`);
CREATE INDEX `paniers_pa_user_session` ON `paniers` (`pa_user_session`);
CREATE INDEX `panier_items_pi_panier_id` ON `panier_items` (`pi_panier_id`);
CREATE INDEX `orders_ord_cart_id` ON `orders` (`ord_cart_id`);
COMMIT;
