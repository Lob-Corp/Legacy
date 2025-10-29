CREATE TABLE
	"Person" (
		id INTEGER NOT NULL,
		first_name TEXT NOT NULL,
		surname TEXT NOT NULL,
		occ INTEGER NOT NULL,
		image TEXT NOT NULL,
		public_name TEXT NOT NULL,
		qualifiers TEXT NOT NULL,
		aliases TEXT NOT NULL,
		first_names_aliases TEXT NOT NULL,
		surname_aliases TEXT NOT NULL,
		occupation TEXT NOT NULL,
		sex VARCHAR(6) NOT NULL,
		access_right VARCHAR(8) NOT NULL,
		birth_date INTEGER,
		birth_place TEXT NOT NULL,
		birth_note TEXT NOT NULL,
		birth_src TEXT NOT NULL,
		baptism_date INTEGER,
		baptism_place TEXT NOT NULL,
		baptism_note TEXT NOT NULL,
		baptism_src TEXT NOT NULL,
		death_status VARCHAR(19) NOT NULL,
		death_reason VARCHAR(11),
		death_date INTEGER,
		death_place TEXT NOT NULL,
		death_note TEXT NOT NULL,
		death_src TEXT NOT NULL,
		burial_status VARCHAR(14) NOT NULL,
		burial_date INTEGER,
		burial_place TEXT NOT NULL,
		burial_note TEXT NOT NULL,
		burial_src TEXT NOT NULL,
		notes TEXT NOT NULL,
		src TEXT NOT NULL,
		ascend_id INTEGER,
		families_id INTEGER,
		PRIMARY KEY (id),
		FOREIGN KEY (birth_date) REFERENCES "Date" (id),
		FOREIGN KEY (baptism_date) REFERENCES "Date" (id),
		FOREIGN KEY (death_date) REFERENCES "Date" (id),
		FOREIGN KEY (burial_date) REFERENCES "Date" (id),
		FOREIGN KEY (ascend_id) REFERENCES "Ascends" (id),
		FOREIGN KEY (families_id) REFERENCES "Unions" (id),
		CONSTRAINT "chk_Person_sex" CHECK (sex IN ('MALE', 'FEMALE', 'NEUTER')),
		CONSTRAINT "chk_Person_access_right" CHECK (access_right IN ('IFTITLES', 'PUBLIC', 'PRIVATE')),
		CONSTRAINT "chk_Person_death_status" CHECK (
			death_status IN (
				'NOT_DEAD',
				'DEAD',
				'DEAD_YOUNG',
				'DEAD_DONT_KNOW_WHEN',
				'DONT_KNOW_IF_DEAD',
				'OF_COURSE_DEAD'
			)
		),
		CONSTRAINT "chk_Person_death_reason" CHECK (
			death_reason IN (
				'KILLED',
				'MURDERED',
				'EXECUTED',
				'DISAPPEARED',
				'UNSPECIFIED'
			)
		),
		CONSTRAINT "chk_Person_burial_status" CHECK (
			burial_status IN ('UNKNOWN_BURIAL', 'BURIAL', 'CREMATED')
		)
	);

-- Table: Family
CREATE TABLE
	"Family" (
		id INTEGER NOT NULL,
		marriage_date INTEGER NOT NULL,
		marriage_place TEXT NOT NULL,
		marriage_note TEXT NOT NULL,
		marriage_src TEXT NOT NULL,
		relation_kind VARCHAR(26) NOT NULL,
		divorce_status VARCHAR(12) NOT NULL,
		divorce_date INTEGER,
		parents_id INTEGER,
		children_id INTEGER,
		comment TEXT NOT NULL,
		origin_file TEXT NOT NULL,
		src TEXT NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (marriage_date) REFERENCES "Date" (id),
		FOREIGN KEY (divorce_date) REFERENCES "Date" (id),
		FOREIGN KEY (parents_id) REFERENCES "Couple" (id),
		FOREIGN KEY (children_id) REFERENCES "Descends" (id),
		CONSTRAINT "chk_Family_relation_kind" CHECK (
			relation_kind IN (
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
		CONSTRAINT "chk_Family_divorce_status" CHECK (
			divorce_status IN ('NOT_DIVORCED', 'DIVORCED', 'SEPARATED')
		)
	);

-- Table: Couple
CREATE TABLE
	"Couple" (
		id INTEGER NOT NULL,
		father_id INTEGER NOT NULL,
		mother_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (father_id) REFERENCES "Person" (id),
		FOREIGN KEY (mother_id) REFERENCES "Person" (id)
	);

-- Table: Ascends
CREATE TABLE
	"Ascends" (
		id INTEGER NOT NULL,
		parents INTEGER,
		consang INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (parents) REFERENCES "Family" (id)
	);

-- Table: Descends
CREATE TABLE
	"Descends" (id INTEGER NOT NULL, PRIMARY KEY (id));

-- Table: Unions
CREATE TABLE
	"Unions" (id INTEGER NOT NULL, PRIMARY KEY (id));

-- Table: UnionFamilies
CREATE TABLE
	"UnionFamilies" (
		id INTEGER NOT NULL,
		union_id INTEGER NOT NULL,
		family_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (union_id) REFERENCES "Unions" (id),
		FOREIGN KEY (family_id) REFERENCES "Family" (id)
	);

-- Table: Precision
CREATE TABLE
	"Precision" (
		id INTEGER NOT NULL,
		precision_level VARCHAR(7) NOT NULL,
		iso_date TEXT,
		calendar VARCHAR(9),
		delta INTEGER,
		PRIMARY KEY (id),
		CONSTRAINT "chk_Precision_precision_level" CHECK (
			precision_level IN (
				'SURE',
				'ABOUT',
				'MAYBE',
				'BEFORE',
				'AFTER',
				'ORYEAR',
				'YEARINT'
			)
		),
		CONSTRAINT "chk_Precision_calendar" CHECK (
			calendar IN ('GREGORIAN', 'JULIAN', 'FRENCH', 'HEBREW')
		)
	);

-- Table: Date
CREATE TABLE
	"Date" (
		id INTEGER NOT NULL,
		iso_date TEXT NOT NULL,
		calendar VARCHAR(9) NOT NULL,
		precision_id INTEGER NOT NULL,
		delta INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (precision_id) REFERENCES "Precision" (id),
		CONSTRAINT "chk_Date_calendar" CHECK (
			calendar IN ('GREGORIAN', 'JULIAN', 'FRENCH', 'HEBREW')
		)
	);

-- Table: Place
CREATE TABLE
	"Place" (
		id INTEGER NOT NULL,
		town TEXT NOT NULL,
		township TEXT NOT NULL,
		canton TEXT NOT NULL,
		district TEXT NOT NULL,
		county TEXT NOT NULL,
		region TEXT NOT NULL,
		country TEXT NOT NULL,
		other TEXT NOT NULL,
		PRIMARY KEY (id)
	);

-- Table: Relation
CREATE TABLE
	"Relation" (
		id INTEGER NOT NULL,
		type VARCHAR(15) NOT NULL,
		father_id INTEGER NOT NULL,
		mother_id INTEGER NOT NULL,
		sources TEXT NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (father_id) REFERENCES "Person" (id),
		FOREIGN KEY (mother_id) REFERENCES "Person" (id),
		CONSTRAINT "chk_Relation_type" CHECK (
			type IN (
				'Adoption',
				'Recognition',
				'CandidateParent',
				'GodParent',
				'FosterParent'
			)
		)
	);

-- Table: Titles
CREATE TABLE
	"Titles" (
		id INTEGER NOT NULL,
		name TEXT NOT NULL,
		ident TEXT NOT NULL,
		place TEXT NOT NULL,
		date_start INTEGER NOT NULL,
		date_end INTEGER NOT NULL,
		nth INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (date_start) REFERENCES "Date" (id),
		FOREIGN KEY (date_end) REFERENCES "Date" (id)
	);

-- Table: PersonalEvent
CREATE TABLE
	"PersonalEvent" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		name VARCHAR(24) NOT NULL,
		date INTEGER NOT NULL,
		place TEXT NOT NULL,
		reason TEXT NOT NULL,
		note TEXT NOT NULL,
		src TEXT NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (date) REFERENCES "Date" (id),
		CONSTRAINT "chk_PersonalEvent_name" CHECK (
			name IN (
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
		)
	);

-- Table: FamilyEvent
CREATE TABLE
	"FamilyEvent" (
		id INTEGER NOT NULL,
		family_id INTEGER NOT NULL,
		name VARCHAR(17) NOT NULL,
		date INTEGER NOT NULL,
		place TEXT NOT NULL,
		reason TEXT NOT NULL,
		note TEXT NOT NULL,
		src TEXT NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (family_id) REFERENCES "Family" (id),
		FOREIGN KEY (date) REFERENCES "Date" (id),
		CONSTRAINT "chk_FamilyEvent_name" CHECK (
			name IN (
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
		)
	);

-- Table: PersonEvents
CREATE TABLE
	"PersonEvents" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		event_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (event_id) REFERENCES "PersonalEvent" (id)
	);

-- Table: FamilyEvents
CREATE TABLE
	"FamilyEvents" (
		id INTEGER NOT NULL,
		family_id INTEGER NOT NULL,
		event_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (family_id) REFERENCES "Family" (id),
		FOREIGN KEY (event_id) REFERENCES "FamilyEvent" (id)
	);

-- Table: PersonRelations
CREATE TABLE
	"PersonRelations" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		related_person_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (related_person_id) REFERENCES "Person" (id)
	);

-- Table: PersonNonNativeRelations
CREATE TABLE
	"PersonNonNativeRelations" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		relation_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (relation_id) REFERENCES "Relation" (id)
	);

-- Table: PersonTitles
CREATE TABLE
	"PersonTitles" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		title_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (title_id) REFERENCES "Titles" (id)
	);

-- Table: PersonEventWitness
CREATE TABLE
	"PersonEventWitness" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		event_id INTEGER NOT NULL,
		kind VARCHAR(24) NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (event_id) REFERENCES "PersonalEvent" (id),
		CONSTRAINT "chk_PersonEventWitness_kind" CHECK (
			kind IN (
				'WITNESS',
				'WITNESS_GODPARENT',
				'WITNESS_CIVILOFFICER',
				'WITNESS_RELIGIOUSOFFICER',
				'WITNESS_INFORMANT',
				'WITNESS_ATTENDING',
				'WITNESS_MENTIONED',
				'WITNESS_OTHER'
			)
		)
	);

-- Table: FamilyEventWitness
CREATE TABLE
	"FamilyEventWitness" (
		id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		event_id INTEGER NOT NULL,
		kind VARCHAR(24) NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id),
		FOREIGN KEY (event_id) REFERENCES "FamilyEvent" (id),
		CONSTRAINT "chk_FamilyEventWitness_kind" CHECK (
			kind IN (
				'WITNESS',
				'WITNESS_GODPARENT',
				'WITNESS_CIVILOFFICER',
				'WITNESS_RELIGIOUSOFFICER',
				'WITNESS_INFORMANT',
				'WITNESS_ATTENDING',
				'WITNESS_MENTIONED',
				'WITNESS_OTHER'
			)
		)
	);

-- Table: FamilyWitness
CREATE TABLE
	"FamilyWitness" (
		id INTEGER NOT NULL,
		family_id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (family_id) REFERENCES "Family" (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id)
	);

-- Table: DescendChildren
CREATE TABLE
	"DescendChildren" (
		id INTEGER NOT NULL,
		descend_id INTEGER NOT NULL,
		person_id INTEGER NOT NULL,
		PRIMARY KEY (id),
		FOREIGN KEY (descend_id) REFERENCES "Descends" (id),
		FOREIGN KEY (person_id) REFERENCES "Person" (id)
	);