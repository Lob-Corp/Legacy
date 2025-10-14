"""Test data for GeneWeb .gw file parser tests."""

# Sample minimal .gw content for each block type
FAM_BLOCK = """fam 0 John + 0 Jane
wit m: 0 John
src test_source
fevt
#marr 2020 #p Paris #c Ceremony #s Source
end fevt
beg
- Paul
end
"""

FAM_BLOCK_NO_MARRIAGE = """fam 0 John + #noment 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_NOT_MARRIED = """fam 0 John + #nm 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_ENGAGED = """fam 0 John + #eng 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_WITH_DIVORCE = """fam 0 John +2020 0 Jane
-2022
beg
- Paul
end
"""

FAM_BLOCK_SEPARATED = """fam 0 John +2020 #sep 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_WITH_MULTIPLE_CHILDREN = """fam 0 John + 0 Jane
beg
- Paul
- m: Peter
- f: Patricia
end
"""

FAM_BLOCK_WITH_COMMENT = """fam 0 John + 0 Jane
comm This is a family comment
beg
- Paul
end
"""

# TODO: Future implementation - marriage contracts, licenses, PACS, residence
FAM_BLOCK_MARRIAGE_CONTRACT = """fam 0 John + #contract 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_MARRIAGE_LICENSE = """fam 0 John + #license 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_PACS = """fam 0 John + #pacs 0 Jane
beg
- Paul
end
"""

FAM_BLOCK_RESIDENCE = """fam 0 John + #residence 0 Jane
beg
- Paul
end
"""

NOTES_BLOCK = """notes 0 John
This is a note about John.
Another line of note.
"""

REL_BLOCK = """rel 0 John
beg
- adop fath: 0 Mike
- adop moth: 0 Mary
end
"""

REL_BLOCK_DUAL_PARENT = """rel 0 John
beg
- adop: 0 Mike + 0 Mary
end
"""

REL_BLOCK_RECOGNITION = """rel 0 John
beg
- reco fath: 0 Mike
end
"""

REL_BLOCK_CANDIDATE_PARENT = """rel 0 John
beg
- cand fath: 0 Mike
end
"""

REL_BLOCK_GODPARENT = """rel 0 John
beg
- godp fath: 0 Mike
end
"""

REL_BLOCK_FOSTER_PARENT = """rel 0 John
beg
- fost fath: 0 Mike
end
"""

PEVT_BLOCK = """pevt 0 John
#birt 1990 #p Paris #c Born #s Source
end pevt
"""

PEVT_BLOCK_MULTIPLE_EVENTS = """pevt 0 John
#birt 1990 #p Paris
#bapt 15/02/1990 #p Paris
#deat 2050 #p London
end pevt
"""

PEVT_BLOCK_CUSTOM_EVENT = """pevt 0 John
#gradschool 2010 #p Boston #c Graduated_from_university
end pevt
"""

# TODO: Future implementation - special personal event types
PEVT_BLOCK_BAPTISM_LDS = """pevt 0 John
#brtm 1990 #p Salt_Lake_City
end pevt
"""

PEVT_BLOCK_BAR_MITZVAH = """pevt 0 John
#barm 2005 #p Jerusalem
end pevt
"""

NOTES_DB_BLOCK = """notes-db
This is a base note.
end notes-db
"""

WIZARD_NOTE_BLOCK = """wizard-note wiz123
This is a wizard note.
end wizard-note
"""

ENCODING_DIRECTIVE = """encoding: iso-8859-1
fam 0 John + 0 Jane
beg
- Paul
end
"""

GWPLUS_DIRECTIVE = """gwplus
fam 0 John + 0 Jane
beg
- Paul
end
"""

PAGE_EXT_BLOCK = """page-ext custom_page
This is extended page content.
Multiple lines allowed.
end page-ext
"""

INVALID_CONTENT_WITH_VALID_FAMILIES = """fam 0 John + 0 Jane
beg
- Paul
end

fam INVALID SYNTAX HERE
beg
end

fam 0 Mike + 0 Mary
beg
- Peter
end
"""

# Complex scenarios for advanced testing

COMPLEX_FAMILY_WITH_EVERYTHING = """fam Smith John[2] +1950 Jones Mary[1]
wit m: 0 Thomas
wit f: 0 Elizabeth
src Marriage_Certificate_1950
csrc Birth_Registry
cbp New_York
comm John and Mary were married in a small ceremony
fevt
#marr 15/06/1950 #p New_York #c Small_ceremony #s Certificate_NYC
wit m: Williams James
wit f: Davis Sarah
note Marriage witnessed by close friends
#resi 1955 #p Boston #c Moved_for_work
end fevt
beg
- m: Robert 10/03/1951 #bp New_York #bs Birth_Cert_1951
- f: Susan 22/08/1953 #bp Boston #bs Birth_Cert_1953
- m: Michael 05/11/1955 #bp Boston
end
"""

PERSON_WITH_COMPLEX_DATES = """fam 0 Pierre + 0 Marie
beg
- Jean ~1890 #bp Paris
- Luc ?1892/05 #bp Lyon
- Paul <1895 #bp Marseille
- Marc >1897 #bp Nice
- Henri 1900|1901 #bp Toulouse
- Louis 1902..1903 #bp Bordeaux
end
"""

PERSON_WITH_ALL_FIELDS = """fam 0 John + 0 Jane
beg
- Robert {Bob} {Robbie} #salias Roberts #salias Robertson (Robert_the_Great) #image photo.jpg #nick Bobby #nick Rob #alias Bob_Smith [Duke:duke_id:London:1980:1990:1] [Baron:baron_id:Oxford:1990:2000:2] #apubl #occu Engineer #src Person_Registry 15/03/1950 #bp London #bn Born_at_hospital #bs Birth_Cert 01/04/1950 #pp London #pn Baptized_at_church #ps Baptism_Cert k2010 #dp Paris #dn Died_in_accident #ds Death_Cert #buri 15/05/2010 #rp Pere_Lachaise #rn Funeral_note #rs Burial_Cert
end
"""

MULTIPLE_RELATIONS_SAME_PERSON = """rel 0 John #h
beg
- adop fath: Smith Thomas
- adop moth: Smith Elizabeth
- godp fath: Williams Robert
- godp moth: Williams Mary
- fost fath: Johnson David
end
"""

MULTIPLE_EVENTS_WITH_WITNESSES = """pevt Smith 0 John
#birt 15/03/1950 #p London #c Hospital_birth #s Birth_Certificate
wit m: #godp 0 Doctor Smith
wit f: #atte 0 Nurse Johnson
note Complicated birth, required medical attention
#bapt 01/04/1950 #p St_Pauls_Church #c Catholic_baptism
wit m: #godp 0 Thomas Williams
wit f: #godp 0 Mary Williams
note Traditional ceremony
#marr 20/06/1975 #p London_Cathedral
wit m: #offi 0 Reverend Brown
wit f: #atte 0 Robert Davis
wit f: #atte 0 Sarah Brown
#deat 10/05/2010 #p Paris_Hospital #c Heart_attack
wit m: #info 0 Doctor Dupont
note Sudden death
end pevt
"""

FAMILY_WITH_COMPLEX_MARRIAGE_HISTORY = """fam Martin Jean +15/05/1970 Dupont Marie
#mp Paris #mn First_marriage #ms Marriage_Cert_1
-10/12/1975
beg
- Pierre 01/03/1971
end

fam Martin Jean +20/08/1977 Bernard Sophie
#mp Lyon #mn Second_marriage #ms Marriage_Cert_2
beg
- Luc 15/10/1978
- Claire 22/05/1980
end
"""

NESTED_SURNAMES_AND_OCCURRENCES = """fam Smith John[1] + Jones Mary[1]
beg
- Robert[1]
end

fam Smith John[2] + Williams Elizabeth[1]
beg
- Robert[2] Smith
- m: Thomas[1] Johnson
- f: Sarah[1]
end

fam Smith John[3] + Davis Anne[1]
beg
- Robert[3]
end
"""

MIXED_CONTENT_FILE = """encoding: utf-8
gwplus

fam 0 John + 0 Jane
beg
- Paul
end

notes Paul John
These are notes about Paul John.
He was a remarkable person.

rel 0 Paul #h
beg
- godp fath: Smith Thomas
end

pevt 0 Paul
#birt 1980 #p London
#grad 2002 #p Oxford #c BSc_Computer_Science
end pevt

notes-db
This is the family database.
It contains information about the Smith family.
end notes-db

wizard-note admin123
Last updated by administrator
Verified genealogy sources
end wizard-note

page-ext sources
Primary sources:
- Birth certificates
- Marriage records
- Census data
end page-ext

fam Smith Thomas + Williams Mary
beg
- m: Robert
- f: Elizabeth
end
"""

PERSON_WITH_DEATH_VARIATIONS = """fam 0 Test + 0 Test
beg
- Alice ? #dp Unknown
- Bob mj #dp Hospital
- Charlie od #dp Home
- David k1945 #dp Battlefield
- Eve m1950 #dp Crime_scene
- Frank e1960 #dp Prison
- Grace s1970 #dp Missing
end
"""

DATES_WITH_CALENDARS = """fam 0 Test + 0 Test
beg
- AliceG 15/03/1950G #bp Paris
- BobJ 15/03/1950J #bp Rome
- CharlieF 15/03/1950F #bp Paris
- DavidH 15/03/1950H #bp Jerusalem
end
"""

FAMILY_WITH_SEX_OVERRIDES = """fam 0 Alex + #nm ff 0 Jordan
beg
- Child1
end

fam 0 Morgan + #eng mm 0 Riley
beg
- Child2
end

fam 0 Casey + #noment mf 0 Jamie
beg
- Child3
end
"""

COMPLEX_TITLES_AND_ALIASES = """fam 0 John + 0 Jane
beg
- Robert {Bobby} {Rob} {Robby} #salias Roberts #salias Robertson #salias Robertsen #nick Bob #nick Bert #alias Bob_the_Builder [King:king_1:London:1990:2000:1] [Duke:duke_2:Oxford:2000:2010:2] [Baron:baron_3:Cambridge:2010:2020:3] [*:::2020::4]
end
"""

EVENTS_WITH_ALL_WITNESS_TYPES = """pevt 0 John
#marr 20/06/1975 #p London
wit m: #godp Godfather Smith
wit f: #godp Godmother Jones
wit m: #offi Officer Brown
wit f: #reli Priest Williams
wit m: #info Informant Davis
wit f: #atte Attendee Wilson
wit m: #ment Mentioned Taylor
wit f: #othe Other Anderson
end pevt
"""

EMPTY_AND_EDGE_CASES = """fam 0 John + 0 Jane
beg
end

fam Smith ? + ? Jane
beg
- ?
end

fam 0 Test1 + 0 Test2
beg
- Child1
- m: Child2
- f: Child3
- Child4 ?
- Child5 ? Surname
end
"""

# Family event tests

FAMILY_EVENTS_ALL_TYPES = """fam Smith 0 John + Jones 0 Mary
fevt
#marr 15/06/1950 #p London_Church #c Religious_ceremony #s Marriage_Cert
wit m: #offi 0 Reverend Brown
wit f: #atte 0 Sarah Johnson
note Beautiful ceremony
#marb 01/05/1950 #p Town_Hall #c Banns_posted #s Banns_Record
#marc 10/05/1950 #p Lawyer_Office #c Contract_signed #s Contract_Doc
#marl 12/05/1950 #p Registry #c License_issued #s License_Doc
#resi 1951 #p 123_Main_Street #c First_home #s Census_1951
#resi 1960 #p 456_Oak_Avenue #c Moved_house #s Census_1960
#sep 1965 #p Court #c Legal_separation #s Court_Doc
note Marriage difficulties
#div 1970 #p Court #c Final_divorce #s Divorce_Cert
note Irreconcilable differences
end fevt
beg
- Robert 1952
end
"""

FAMILY_EVENTS_WITH_WITNESSES = """fam 0 John + 0 Jane
fevt
#marr 20/06/1975 #p Cathedral #c Catholic_wedding
wit m: #offi 0 Father Smith
wit m: #offi 0 Father Brown
wit f: #atte 0 Bridesmaid Alice
wit f: #atte 0 Bridesmaid Mary
wit m: #atte 0 Best_Man Robert
note Five witnesses present
#resi 1976 #p First_Home
wit m: #info 0 Neighbor John
wit f: #info 0 Neighbor Jane
note Neighbors confirmed residence
end fevt
beg
- Child1 1977
end
"""

FAMILY_EVENTS_NO_MARRIAGE = """fam 0 John + #nm 0 Jane
fevt
#resi 1990 #p Common_Address #c Living_together
#nmar 1990 #c Not_married_but_together
note Chose not to marry
end fevt
beg
- Child1 1991
end
"""

FAMILY_EVENTS_ENGAGEMENT_ONLY = """fam 0 John + #eng 0 Jane
fevt
#enga 01/01/2000 #p Restaurant #c Proposal
note He proposed on New Year's Day
end fevt
beg
end
"""

FAMILY_EVENTS_PACS = """fam Dupont 0 Pierre + Martin 0 Jacques
fevt
#pacs 15/11/1999 #p Paris_Mairie #c PACS_ceremony #s PACS_Certificate
note French civil union
#resi 2000 #p Paris_Apartment
end fevt
beg
end
"""

FAMILY_EVENTS_ANNULMENT = """fam 0 John + 0 Mary
fevt
#marr 01/06/1980 #p Church #c Wedding
#anul 01/12/1980 #p Vatican #c Marriage_annulled #s Annulment_Doc
note Marriage annulled after 6 months
end fevt
beg
end
"""

FAMILY_EVENTS_MULTIPLE_RESIDENCES = """fam 0 John + 0 Jane
fevt
#marr 1950 #p London
#resi 1950 #p 10_Downing_Street #c First_residence
#resi 1955 #p 20_Baker_Street #c Second_residence
#resi 1960 #p 30_Abbey_Road #c Third_residence
#resi 1965 #p 40_Oxford_Street #c Fourth_residence
#resi 1970 #p 50_Regent_Street #c Fifth_residence
note Moved frequently
end fevt
beg
- Child1 1952
end
"""

FAMILY_EVENTS_COMPLEX_DATES = """fam 0 Test + 0 Test
fevt
#marr ~1950 #p London #c Approximate_date
#resi <1955 #p Address1 #c Before_1955
#resi >1960 #p Address2 #c After_1960
#resi ?1965 #p Address3 #c Maybe_1965
#sep 1970 #p Court #c Separation_year
end fevt
beg
end
"""

FAMILY_EVENTS_WITH_NOTES_AND_SOURCES = """fam 0 John + 0 Mary
fevt
#marr 15/06/1950 #p Church #c Religious #s Parish_Register_p123
note The bride wore white. Weather was sunny. 100 guests attended.
#resi 1951 #p Home #s Census_1951_Page_45
note First home together
#div 1960 #p Court #s Court_Records_Case_456
note Cited adultery as grounds
note Both parties agreed to divorce
end fevt
beg
end
"""

FAMILY_EVENTS_NAMED_CUSTOM = """fam 0 John + 0 Jane
fevt
#marr 2000 #p Church
#CustomEvent1 2001 #p Location1 #c Context1 #s Source1
note First custom event
#AnotherEvent 2002 #p Location2 #c Context2 #s Source2
wit m: #info 0 Witness One
note Second custom event
end fevt
beg
end
"""
