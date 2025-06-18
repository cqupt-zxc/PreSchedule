create table user_info
(
    id       int auto_increment
        primary key,
    account  varchar(50)                not null,
    password varchar(200)               not null,
    role     varchar(20) default 'user' not null,
    constraint account
        unique (account)
);

ALTER TABLE user_info ADD COLUMN login_attempts INT DEFAULT 0;
ALTER TABLE user_info ADD COLUMN lock_until DATETIME DEFAULT NULL;

