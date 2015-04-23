DROP TABLE IF EXISTS "main"."url";
create table url (
    id           integer primary key autoincrement not null,
    host        text,
    page text,
    url text
);
DROP TABLE IF EXISTS "main"."link";
create table link (
    id           integer primary key autoincrement not null,
    source        integer,
    target integer
);