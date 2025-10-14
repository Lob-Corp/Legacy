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
