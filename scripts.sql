CREATE TABLE user
(
    user_id  INTEGER PRIMARY KEY,
    username text,
    email    text,
    password text,
    UNIQUE (email)
);
CREATE INDEX user_id_index ON user (user_id);

CREATE TABLE blogs
(
    blog_id          INTEGER PRIMARY KEY,
    user_id          INTEGER not null,
    username         text    not null,
    title            text    not null,
    description      text    not null,
    image_path_one   text default '',
    last_modified_at TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
    created_at       TEXT DEFAULT (strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')),
    UNIQUE (title)
);

CREATE INDEX blog_id_index ON blogs (blog_id);


CREATE TRIGGER update_last_modified_at
    BEFORE UPDATE
    ON blogs
BEGIN
    UPDATE blogs
    SET last_modified_at = strftime('%Y-%m-%d %H:%M:%S', 'now', 'localtime')
    WHERE blog_id = old.blog_id;
END;