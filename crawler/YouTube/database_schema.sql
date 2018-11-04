CREATE TABLE category( 
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
id CHARACTER(100) UNIQUE NOT NULL, 
key CHARACTER(100));

BEGIN TRANSACTION;
INSERT INTO category(id, key) VALUES(1, 'Film & Animation');
INSERT INTO category(id, key) VALUES(2, 'Autos & Vehicles');
INSERT INTO category(id, key) VALUES(10,  'Music');
INSERT INTO category(id, key) VALUES(15, 'Pets & Animals');
INSERT INTO category(id, key) VALUES(17, 'Sports');
INSERT INTO category(id, key) VALUES(18, 'Short Movies');
INSERT INTO category(id, key) VALUES(19, 'Travel & Events');
INSERT INTO category(id, key) VALUES(20, 'Gaming');
INSERT INTO category(id, key) VALUES(21, 'Videoblogging');
INSERT INTO category(id, key) VALUES(22, 'People & Blogs');
INSERT INTO category(id, key) VALUES(23, 'Comedy');
INSERT INTO category(id, key) VALUES(24, 'Entertainment');
INSERT INTO category(id, key) VALUES(25, 'News & Politics');
INSERT INTO category(id, key) VALUES(26, 'Howto & Style');
INSERT INTO category(id, key) VALUES(27, 'Education');
INSERT INTO category(id, key) VALUES(28, 'Science & Technology');
INSERT INTO category(id, key) VALUES(29, 'Nonprofits & Activism');
INSERT INTO category(id, key) VALUES(30, 'Movies');
INSERT INTO category(id, key) VALUES(31, 'Anime/Animation');
INSERT INTO category(id, key) VALUES(32, 'Action/Adventure');
INSERT INTO category(id, key) VALUES(33, 'Classics');
INSERT INTO category(id, key) VALUES(34, 'Comedy');
INSERT INTO category(id, key) VALUES(35, 'Documentary');
INSERT INTO category(id, key) VALUES(36, 'Drama');
INSERT INTO category(id, key) VALUES(37, 'Family');
INSERT INTO category(id, key) VALUES(38, 'Foreign');
INSERT INTO category(id, key) VALUES(39, 'Horror');
INSERT INTO category(id, key) VALUES(40, 'Sci-Fi/Fantasy');
INSERT INTO category(id, key) VALUES(41, 'Thriller');
INSERT INTO category(id, key) VALUES(42, 'Shorts');
INSERT INTO category(id, key) VALUES(43, 'Shows');
INSERT INTO category(id, key) VALUES(44, 'Trailers');
COMMIT;

CREATE TABLE sample(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
seed CHARACTER(10),
resultsCount INTEGER,
completedStatus INTEGER);

CREATE TABLE sampleVideos(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(20),
sampleId INTEGER,
FOREIGN KEY (sampleId) REFERENCES sample(autoId) ON UPDATE CASCADE);

CREATE TABLE channel(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(100) UNIQUE NOT NULL,
title CHARACTER(100),
description CHARACTER(10000),
playlistId CHARACTER(1000),
publishedAt CHARACTER(25),
viewCount BIGINT,
commentCount BIGINT,
subscriberCount BIGINT,
videoCount BIGINT, country CHARACTER(1000));

CREATE TABLE video(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(200) UNIQUE NOT NULL,
categoryId INTEGER NOT NULL,
channelId CHARACTER(100) NOT NULL,
publishedAt CHARACTER(25),
title CHARACTER(200),
description CHARACTER(20000),
viewCount BIGINT,
likeCount BIGINT,
dislikeCount BIGINT,
favoriteCount BIGINT,
commentCount BIGINT,
duration CHARACTER(25),
defaultLanguage CHARACTER(10));

CREATE TABLE sampleVideosStatus(
sampleVideoId CHARACTER(20) NOT NULL,
completedStatus INTEGER,
FOREIGN KEY (sampleVideoId) REFERENCES sampleVideos(Id) ON UPDATE CASCADE);

CREATE TABLE url(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
videoId CHARACTER(200) NOT NULL,
url CHARACTER(10000),
FOREIGN KEY (videoId) REFERENCES video(id) ON UPDATE CASCADE);

CREATE TABLE urlResolve(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
urlId INTEGER NOT NULL,
url CHARACTER(10000),
urlOrder INTEGER NOT NULL,
code INTEGER,
FOREIGN KEY (urlId) REFERENCES url(autoId) ON UPDATE CASCADE);

CREATE TABLE urlStatus(
urlId INTEGER NOT NULL,
completedStatus INTEGER,
FOREIGN KEY (urlId) REFERENCES url(autoId) ON UPDATE CASCADE);

CREATE TABLE channelStatus(
channelId CHARACTER(100) NOT NULL,
completedStatus INTEGER,
FOREIGN KEY (channelId) REFERENCES video(channelId) ON UPDATE CASCADE);

CREATE TABLE channelSamples(
channelId CHARACTER(100) NOT NULL);

CREATE TABLE captions (
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
num INTEGER NOT NULL,
startMinutes INTEGER NOT NULL,
endMinutes INTEGER NOT NULL,
startSeconds INTEGER NOT NULL,
endSeconds INTEGER NOT NULL,
videoId CHARACTER(200) NOT NULL, text TEXT,
FOREIGN KEY (videoId) REFERENCES video(id) ON UPDATE CASCADE);

CREATE TABLE urlNumber(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
videoId CHARACTER(200) NOT NULL,
url CHARACTER(10000),
lineNumber INTEGER NOT NULL,
FOREIGN KEY (videoId) REFERENCES video(id) ON UPDATE CASCADE);
