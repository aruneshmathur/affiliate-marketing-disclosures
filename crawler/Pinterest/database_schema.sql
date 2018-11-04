CREATE TABLE category( 
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, 
id CHARACTER(100) UNIQUE NOT NULL, 
name CHARACTER(100), 
type CHARACTER(100),
key CHARACTER(100));

BEGIN TRANSACTION;
INSERT INTO category(id, name, type, key) VALUES(1, "Popular", "non_board", "popular");
INSERT INTO category(id, name, type, key) VALUES(2, "Everything", "non_board", "everything");
INSERT INTO category(id, name, type, key) VALUES(3, "Gifts", "non_board", "gifts");
INSERT INTO category(id, name, type, key) VALUES(4, "Videos", "non_board", "videos");
INSERT INTO category(id, name, type, key) VALUES(5, "Animals and pets", "main", "animals");
INSERT INTO category(id, name, type, key) VALUES(6, "Architecture", "main", "architecture");
INSERT INTO category(id, name, type, key) VALUES(7, "Art", "main", "art");
INSERT INTO category(id, name, type, key) VALUES(8, "Cars and motorcycles", "main", "cars_motorcycles");
INSERT INTO category(id, name, type, key) VALUES(9, "Celebrities", "main", "celebrities");
INSERT INTO category(id, name, type, key) VALUES(10, "DIY and crafts", "main", "diy_crafts");
INSERT INTO category(id, name, type, key) VALUES(11, "Design", "main", "design");
INSERT INTO category(id, name, type, key) VALUES(12, "Education", "main", "education");
INSERT INTO category(id, name, type, key) VALUES(13, "Entertainment", "main", "film_music_books");
INSERT INTO category(id, name, type, key) VALUES(14, "Food and drink", "main", "food_drink");
INSERT INTO category(id, name, type, key) VALUES(15, "Gardening", "main", "gardening");
INSERT INTO category(id, name, type, key) VALUES(16, "Geek", "main", "geek");
INSERT INTO category(id, name, type, key) VALUES(17, "Hair and beauty", "main", "hair_beauty");
INSERT INTO category(id, name, type, key) VALUES(18, "Health and fitness", "main", "health_fitness");
INSERT INTO category(id, name, type, key) VALUES(19, "History", "main", "history");
INSERT INTO category(id, name, type, key) VALUES(20, "Holidays and events", "main", "holidays_events");
INSERT INTO category(id, name, type, key) VALUES(21, "Home decor", "main", "home_decor");
INSERT INTO category(id, name, type, key) VALUES(22, "Humor", "main", "humor");
INSERT INTO category(id, name, type, key) VALUES(23, "Illustrations and posters", "main", "illustrations_posters");
INSERT INTO category(id, name, type, key) VALUES(24, "Kids and parenting", "main", "kids");
INSERT INTO category(id, name, type, key) VALUES(25, "Men's fashion", "main", "mens_fashion");
INSERT INTO category(id, name, type, key) VALUES(26, "Outdoors", "main", "outdoors");
INSERT INTO category(id, name, type, key) VALUES(27, "Photography", "main", "photography");
INSERT INTO category(id, name, type, key) VALUES(28, "Products", "main", "products");
INSERT INTO category(id, name, type, key) VALUES(29, "Quotes", "main", "quotes");
INSERT INTO category(id, name, type, key) VALUES(30, "Science and nature", "main", "science_nature");
INSERT INTO category(id, name, type, key) VALUES(31, "Sports", "main", "sports");
INSERT INTO category(id, name, type, key) VALUES(32, "Tattoos", "main", "tattoos");
INSERT INTO category(id, name, type, key) VALUES(33, "Technology", "main", "technology");
INSERT INTO category(id, name, type, key) VALUES(34, "Travel", "main", "travel");
INSERT INTO category(id, name, type, key) VALUES(35, "Weddings", "main", "weddings");
INSERT INTO category(id, name, type, key) VALUES(36, "Women's fashion", "main", "womens_fashion");
INSERT INTO category(id, name, type, key) VALUES(37, "Other", "main", "other");
COMMIT;


CREATE TABLE user(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(1000) NOT NULL, 
userName CHARACTER(1000),
fullName CHARACTER(1000),
domainUrl CHARACTER(10000),
domainVerified CHARACTER(10),
location CHARACTER(1000),
type CHARACTER(100));

CREATE TABLE promoter(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(1000) NOT NULL, 
userName CHARACTER(1000),
fullName CHARACTER(1000),
type CHARACTER(100));

CREATE TABLE board(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(1000) NOT NULL, 
name CHARACTER(1000),
url CHARACTER(10000),
type CHARACTER(100),
privacy CHARACTER(100),
ownerId CHARACTER(1000),
description CHARACTER(20000),
category CHARACTER(100),
FOREIGN KEY (category) REFERENCES category(key) ON UPDATE CASCADE);

CREATE TABLE pin(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
id CHARACTER(1000) NOT NULL, 
link CHARACTER(10000),
trackedLink CHARACTER(10000),
title CHARACTER(10000),
description CHARACTER(20000),
descriptionHTML CHARACTER(20000),
closeupDescription CHARACTER(20000),
closeupUserNote CHARACTER(20000),
type CHARACTER(100),
ownerId CHARACTER(1000),
promoterId CHARACTER(1000),
boardId CHARACTER(1000),
originOwnerId CHARACTER(1000),
likeCount CHARACTER(1000),
commentCount CHARACTER(1000),
repinCount CHARACTER(1000),
isPromoted CHARACTER(100),
method CHARACTER(100),
isRepin CHARACTER(100),
priceValue CHARACTER(1000),
priceCurrency CHARACTER(100),
richMetadataSiteName CHARACTER(10000),
richMetadataDescription CHARACTER(20000),
richMetadataTitle CHARACTER(1000),
richMetadataLocale CHARACTER(10),
richMetadataUrl CHARACTER(10000),
richMetadataType CHARACTER(100),
richMetadataId CHARACTER(1000),
createdAt CHARACTER(100),
category CHARACTER(100),
FOREIGN KEY (ownerId) REFERENCES user(id) ON UPDATE CASCADE,
FOREIGN KEY (promoterId) REFERENCES promoter(id) ON UPDATE CASCADE,
FOREIGN KEY (boardId) REFERENCES board(id) ON UPDATE CASCADE);

CREATE TABLE url(
autoId INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL,
pinId CHARACTER(1000) NOT NULL,
url CHARACTER(10000),
origin CHARACTER(100) NOT NULL,
FOREIGN KEY (pinId) REFERENCES pin(id) ON UPDATE CASCADE);

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

CREATE INDEX id_index1 ON user(id);
CREATE INDEX id_index2 ON promoter(id);
CREATE INDEX id_index3 ON board(id);
CREATE INDEX id_index4 ON pin(id);
CREATE INDEX id_index5 ON url(autoId);
CREATE INDEX id_index6 ON urlResolve(autoId);
