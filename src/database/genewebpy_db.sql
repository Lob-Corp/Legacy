BEGIN TRANSACTION;

CREATE TABLE
    IF NOT EXISTS "Ascends" (
        "id" INTEGER NOT NULL,
        "parents" INTEGER,
        "consang" INTEGER NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("parents") REFERENCES "Family" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Couple" ("id" INTEGER NOT NULL, PRIMARY KEY ("id"));

CREATE TABLE
    IF NOT EXISTS "CoupleParents" (
        "couple_id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        PRIMARY KEY ("couple_id", "person_id"),
        FOREIGN KEY ("couple_id") REFERENCES "Couple" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "DateValue" (
        "id" INTEGER NOT NULL,
        "greg_date" TEXT NOT NULL,
        "precision" TEXT NOT NULL CHECK (
            "precision" IN (
                'sure',
                'about',
                'maybe',
                'before',
                'after',
                'orYear',
                'yearInt'
            )
        ),
        "precision_date_value" INTEGER NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("precision_date_value") REFERENCES "DateValue" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "DescendChildren" (
        "descend_id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        PRIMARY KEY ("descend_id", "person_id"),
        FOREIGN KEY ("descend_id") REFERENCES "Descends" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Descends" ("id" INTEGER NOT NULL, PRIMARY KEY ("id"));

CREATE TABLE
    IF NOT EXISTS "Family" (
        "id" INTEGER NOT NULL,
        "marriage_date" INTEGER NOT NULL,
        "marriage_place" TEXT NOT NULL,
        "marriage_note" TEXT NOT NULL,
        "marriage_src" TEXT NOT NULL,
        "relation_kind" TEXT NOT NULL CHECK (
            "relation_kind" IN (
                'MARRIED',
                'NOT_MARRIED',
                'ENGAGED',
                'NO_SEXES_CHECK_NOT_MARRIED',
                'NO_MENTION',
                'NO_SEXES_CHECK_MARRIED',
                'MARRIAGE_BANN',
                'MARRIAGE_CONTRACT',
                'MARRIAGE_LICENSE',
                'PACS',
                'RESIDENCE'
            )
        ),
        "divorce_status" TEXT NOT NULL CHECK (
            "divorce_status" IN ('NOT_DIVORCED', 'DIVORCED', 'SEPARATED')
        ),
        "divorce_date" INTEGER,
        "comment" TEXT NOT NULL,
        "origin_file" TEXT NOT NULL,
        "src" TEXT NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("marriage_date") REFERENCES "DateValue" ("id"),
        FOREIGN KEY ("divorce_date") REFERENCES "DateValue" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "FamilyEvent" (
        "id" INTEGER NOT NULL,
        "family_id" INTEGER NOT NULL,
        "name" TEXT NOT NULL CHECK (
            "name" IN (
                'MARRIAGE',
                'NO_MARRIAGE',
                'NO_MENTION',
                'ENGAGE',
                'DIVORCE',
                'SEPARATED',
                'ANNULATION',
                'MARRIAGE_BANN',
                'MARRIAGE_CONTRACT',
                'MARRIAGE_LICENSE',
                'PACS',
                'RESIDENCE',
                'NAMED_EVENT'
            )
        ),
        "date" INTEGER NOT NULL,
        "place" TEXT NOT NULL,
        "reason" TEXT NOT NULL,
        "note" TEXT NOT NULL,
        "src" TEXT NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("family_id") REFERENCES "Family" ("id"),
        FOREIGN KEY ("date") REFERENCES "DateValue" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "FamilyEventWitness" (
        "id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        "event_id" INTEGER NOT NULL,
        "kind" TEXT NOT NULL CHECK (
            "kind" IN (
                'WITNESS',
                'WITNESS_GODPARENT',
                'WITNESS_CIVILOFFICER',
                'WITNESS_RELIGIOUSOFFICER',
                'WITNESS_INFORMANT',
                'WITNESS_ATTENDING',
                'WITNESS_MENTIONED',
                'WITNESS_OTHER'
            )
        ),
        PRIMARY KEY ("id"),
        FOREIGN KEY ("event_id") REFERENCES "FamilyEvent" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "FamilyEvents" (
        "family_id" INTEGER NOT NULL,
        "event_id" INTEGER NOT NULL,
        PRIMARY KEY ("family_id", "event_id"),
        FOREIGN KEY ("event_id") REFERENCES "FamilyEvent" ("id"),
        FOREIGN KEY ("family_id") REFERENCES "Family" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "FamilyWitness" (
        "family_id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        PRIMARY KEY ("family_id", "person_id"),
        FOREIGN KEY ("family_id") REFERENCES "Family" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Person" (
        "id" INTEGER NOT NULL,
        "first_name" TEXT NOT NULL,
        "surname" TEXT NOT NULL,
        "occ" INTEGER NOT NULL,
        "image" TEXT NOT NULL,
        "public_name" TEXT NOT NULL,
        "qualifiers" TEXT NOT NULL,
        "aliases" TEXT NOT NULL,
        "first_names_aliases" TEXT NOT NULL,
        "surname_aliases" TEXT NOT NULL,
        "occupation" TEXT NOT NULL,
        "sex" TEXT NOT NULL CHECK ("sex" IN ('MALE', 'FEMALE', 'NEUTER')),
        "access_right" TEXT NOT NULL CHECK (
            "access_right" IN ('PUBLIC', 'PRIVATE', 'IF_TITLES')
        ),
        "birth_date" INTEGER NOT NULL,
        "birth_place" TEXT NOT NULL,
        "birth_note" TEXT NOT NULL,
        "birth_src" TEXT NOT NULL,
        "baptism_date" INTEGER NOT NULL,
        "baptism_place" TEXT NOT NULL,
        "baptism_note" TEXT NOT NULL,
        "baptism_src" TEXT NOT NULL,
        "death_status" TEXT NOT NULL CHECK (
            "death" IN (
                'NOT_DEAD',
                'DEAD',
                'DEAD_YOUNG',
                'DEAD_DONT_KNOW_WHEN',
                'DONT_KNOW_IF_DEAD',
                'OF_COURSE_DEAD'
            )
        ),
        "death_reason" TEXT CHECK (
            "death_reason" IN (
                'KILLED',
                'MURDERED',
                'EXECUTED',
                'DISAPPEARED',
                'UNSPECIFIED'
            )
        ),
        "death_date" INTEGER,
        "death_place" TEXT NOT NULL,
        "death_note" TEXT NOT NULL,
        "death_src" TEXT NOT NULL,
        "burial_status" TEXT NOT NULL CHECK (
            "burial_status" IN ('UNKNOWN_BURIAL', 'BURIAL', 'CREMATED')
        ),
        "burial_date" INTEGER,
        "burial_place" TEXT NOT NULL,
        "burial_note" TEXT NOT NULL,
        "burial_src" TEXT NOT NULL,
        "notes" TEXT NOT NULL,
        "src" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonEventWitness" (
        "id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        "event_id" INTEGER NOT NULL,
        "kind" TEXT NOT NULL CHECK (
            "kind" IN (
                'WITNESS',
                'WITNESS_GODPARENT',
                'WITNESS_CIVILOFFICER',
                'WITNESS_RELIGIOUSOFFICER',
                'WITNESS_INFORMANT',
                'WITNESS_ATTENDING',
                'WITNESS_MENTIONED',
                'WITNESS_OTHER'
            )
        ),
        PRIMARY KEY ("id"),
        FOREIGN KEY ("event_id") REFERENCES "PersonalEvent" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonEvents" (
        "person_id" INTEGER NOT NULL,
        "event_id" INTEGER NOT NULL,
        PRIMARY KEY ("person_id", "event_id"),
        FOREIGN KEY ("event_id") REFERENCES "PersonalEvent" ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonNonNativeRelations" (
        "person_id" INTEGER NOT NULL,
        "relation_id" INTEGER NOT NULL,
        PRIMARY KEY ("person_id", "relation_id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id"),
        FOREIGN KEY ("relation_id") REFERENCES "Relation" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonRelations" (
        "person_id" INTEGER NOT NULL,
        "related_person_id" INTEGER NOT NULL,
        PRIMARY KEY ("person_id", "related_person_id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id"),
        FOREIGN KEY ("related_person_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonTitles" (
        "person_id" INTEGER NOT NULL,
        "title_id" INTEGER NOT NULL,
        PRIMARY KEY ("person_id", "title_id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id"),
        FOREIGN KEY ("title_id") REFERENCES "Titles" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "PersonalEvent" (
        "id" INTEGER NOT NULL,
        "person_id" INTEGER NOT NULL,
        "name" TEXT NOT NULL CHECK (
            "name" IN (
                'BIRTH',
                'BAPTISM',
                'DEATH',
                'BURIAL',
                'CREMATION',
                'ACCOMPLISHMENT',
                'ACQUISITION',
                'ADHESION',
                'BAPTISM_LDS',
                'BAR_MITZVAH',
                'BAT_MITZVAH',
                'BENEDICTION',
                'CHANGE_NAME',
                'CIRCUMCISION',
                'CONFIRMATION',
                'CONFIRMATION_LDS',
                'DECORATION',
                'DEMOBILISATION_MILITAIRE',
                'DIPLOMA',
                'DISTINCTION',
                'DOTATION',
                'DOTATION_LDS',
                'EDUCATION',
                'ELECTION',
                'EMIGRATION',
                'EXCOMMUNICATION',
                'FAMILY_LINK_LDS',
                'FIRST_COMMUNION',
                'FUNERAL',
                'GRADUATE',
                'HOSPITALISATION',
                'ILLNESS',
                'IMMIGRATION',
                'LISTE_PASSENGER',
                'MILITARY_DISTINCTION',
                'MILITARY_PROMOTION',
                'MILITARY_SERVICE',
                'MOBILISATION_MILITAIRE',
                'NATURALISATION',
                'OCCUPATION',
                'ORDINATION',
                'PROPERTY',
                'RECENSEMENT',
                'RESIDENCE',
                'RETIRED',
                'SCELLENT_CHILD_LDS',
                'SCELLENT_PARENT_LDS',
                'SCELLENT_SPOUSE_LDS',
                'VENTE_BIEN',
                'WILL',
                'NAMED_EVENT'
            )
        ),
        "date" INTEGER NOT NULL,
        "place" TEXT NOT NULL,
        "reason" TEXT NOT NULL,
        "note" TEXT NOT NULL,
        "src" TEXT NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("person_id") REFERENCES "Person" ("id"),
        FOREIGN KEY ("date") REFERENCES "DateValue" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Place" (
        "id" INTEGER NOT NULL,
        "town" TEXT NOT NULL,
        "township" TEXT NOT NULL,
        "canton" TEXT NOT NULL,
        "district" TEXT NOT NULL,
        "county" TEXT NOT NULL,
        "region" TEXT NOT NULL,
        "country" TEXT NOT NULL,
        "other" TEXT NOT NULL,
        PRIMARY KEY ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Relation" (
        "id" INTEGER NOT NULL,
        "type" TEXT NOT NULL CHECK (
            "type" IN (
                'ADOPTION',
                'RECOGNITION',
                'CANDIDATEPARENT',
                'GODPARENT',
                'FOSTERPARENT'
            )
        ),
        "father_id" INTEGER NOT NULL,
        "mother_id" INTEGER NOT NULL,
        "sources" TEXT NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("father_id") REFERENCES "Person" ("id"),
        FOREIGN KEY ("mother_id") REFERENCES "Person" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Titles" (
        "id" INTEGER NOT NULL,
        "name" TEXT NOT NULL,
        "ident" TEXT NOT NULL,
        "place" TEXT NOT NULL,
        "date_start" INTEGER NOT NULL,
        "date_end" INTEGER NOT NULL,
        "nth" INTEGER NOT NULL,
        PRIMARY KEY ("id"),
        FOREIGN KEY ("date_end") REFERENCES "DateValue" ("id"),
        FOREIGN KEY ("date_start") REFERENCES "DateValue" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "UnionFamilies" (
        "union_id" INTEGER NOT NULL,
        "family_id" INTEGER NOT NULL,
        PRIMARY KEY ("union_id", "family_id"),
        FOREIGN KEY ("family_id") REFERENCES "Family" ("id"),
        FOREIGN KEY ("union_id") REFERENCES "Unions" ("id")
    );

CREATE TABLE
    IF NOT EXISTS "Unions" ("id" INTEGER NOT NULL, PRIMARY KEY ("id"));

COMMIT;
