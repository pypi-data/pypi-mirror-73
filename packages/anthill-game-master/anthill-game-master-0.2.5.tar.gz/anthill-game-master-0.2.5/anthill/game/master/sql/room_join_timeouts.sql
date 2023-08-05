CREATE TABLE `room_join_timeouts` (
  `gamespace_id` int(11) unsigned NOT NULL,
  `host_id` int(11) unsigned NOT NULL,
  `room_id` int(11) unsigned NOT NULL,
  `account_id` int(11) unsigned NOT NULL,
  `date` datetime NOT NULL,
  PRIMARY KEY (`account_id`,`room_id`,`gamespace_id`),
  KEY `host_id` (`host_id`,`gamespace_id`,`room_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;