
-- Projects are high-level activities made up of tasks
create table project (
    id           integer primary key autoincrement not null,
    name        text,
    description text,
    master  text,
    deadline    date
);

-- Base info
create table chatdb (
    id           integer primary key autoincrement not null,
    name         text,
    usrid        text,
    date         date,
    time         time,
    contents     text
);