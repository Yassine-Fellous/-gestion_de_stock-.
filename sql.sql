create table categorie
(
    id  int auto_increment
        primary key,
    nom varchar(255) null
);

create table produit
(
    id           int auto_increment
        primary key,
    nom          varchar(255) null,
    description  text         null,
    prix         int          null,
    quantite     int          null,
    id_categorie int          null,
    constraint produit_ibfk_1
        foreign key (id_categorie) references categorie (id)
);

create index id_categorie
    on produit (id_categorie);