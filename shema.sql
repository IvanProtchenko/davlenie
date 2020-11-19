CREATE DATABASE sdpl_free_bot ENGINE = Ordinary
CREATE TABLE sdpl_free_bot.history (`day` Date, `userid` UInt64, `clock` DateTime, `sistola` Int32, `diastola` Int32, `pulse` Int32, `notes` String) ENGINE = MergeTree() PARTITION BY toDate(clock) ORDER BY (userid, clock) TTL toDate(clock) + toIntervalDay(365) SETTINGS index_granularity = 8192, merge_with_ttl_timeout = 86400
