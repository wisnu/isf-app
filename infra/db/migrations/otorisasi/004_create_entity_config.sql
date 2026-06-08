CREATE TABLE otorisasi.entity_config (
    entity_type    VARCHAR(50)  PRIMARY KEY,
    module         VARCHAR(50)  NOT NULL,
    level_required INTEGER      NOT NULL DEFAULT 1,
    label          VARCHAR(100) NOT NULL,
    menu_key       VARCHAR(100) NOT NULL
);
