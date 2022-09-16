CREATE TABLE site (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
url VARCHAR(100) NOT NULL,
status INT(1) NOT NULL, 
update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
max_pages INT(3) NOT NULL, 
max_depth INT(3) NOT NULL,
max_non_ad_imgs INT(3) NOT NULL DEFAULT 3,
);

CREATE TABLE site_annoying_elements (
site_id INT(6),
element VARCHAR(1000) NOT NULL
)

CREATE TABLE site_report (
id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY,
update_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
pages_visited INT(6) NOT NULL DEFAULT 0, 
ads_no INT(6) NOT NULL  DEFAULT 0,
non_ads_no INT(6) NOT NULL  DEFAULT 0,
);


INSERT INTO site (ID,URL,STATUS,MAX_PAGES,MAX_DEPTH) VALUES (1,'https://www.sport.ro/', 0, 100,10, 3);


INSERT INTO site_annoying_elements (SITE_ID,ELEMENT) VALUES (1,'//*[@id="onetrust-accept-btn-handler"]');
INSERT INTO site_annoying_elements (SITE_ID,ELEMENT) VALUES (1,'//*[@id="byebyevideo"]');
INSERT INTO site_annoying_elements (SITE_ID,ELEMENT) VALUES (1,'//*[@id="onesignal-slidedown-cancel-button"]');

INSERT INTO site (ID,URL,STATUS,MAX_PAGES,MAX_DEPTH) VALUES (2,'https://www.gandul.ro/', 0, 100,10, 3);

INSERT INTO site_annoying_elements (SITE_ID,ELEMENT) VALUES (2,'//*[@id="qc-cmp2-ui"]/div[2]/div/button[2]/span');
INSERT INTO site_annoying_elements (SITE_ID,ELEMENT) VALUES (2,'//*[@id="onesignal-slidedown-cancel-button"]');
