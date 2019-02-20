SET NAMES utf8mb4;

--
-- Table structure for table `comments`
--
SET character_set_client = utf8mb4 ;
CREATE TABLE `comments` (
  `id` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `auto_id` int(11) NOT NULL AUTO_INCREMENT,
  `auto_link_id` int(11) NOT NULL,
  `link_id` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `body` mediumtext COLLATE utf8mb4_bin,
  `parent_id` varchar(20) COLLATE utf8mb4_bin DEFAULT NULL,
  `author` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_utc` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auto_id` (`auto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Table structure for table `links`
--
SET character_set_client = utf8mb4 ;
CREATE TABLE `links` (
  `auto_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `subreddit_id` varchar(20) COLLATE utf8mb4_bin NOT NULL DEFAULT '',
  `author` varchar(255) COLLATE utf8mb4_bin DEFAULT NULL,
  `title` text COLLATE utf8mb4_bin,
  `self_text` mediumtext COLLATE utf8mb4_bin,
  `url` varchar(700) COLLATE utf8mb4_bin DEFAULT NULL,
  `full_link` varchar(500) COLLATE utf8mb4_bin DEFAULT NULL,
  `created_utc` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auto_id` (`auto_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_bin;

--
-- Table structure for table `links_collection`
--
SET character_set_client = utf8mb4 ;
CREATE TABLE `links_collection` (
  `subredit` varchar(100) COLLATE utf8mb4_general_ci NOT NULL,
  `after` datetime DEFAULT NULL,
  UNIQUE KEY `links_collection_subredit_after_uindex` (`subredit`,`after`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;
