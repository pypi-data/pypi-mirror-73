from dataclasses import dataclass, field
from typing import Dict, List, Optional

import requests
from dataclasses_json import LetterCase, config, dataclass_json

from .uniprot import UniProt


def name(n):
    return field(default=None, metadata=config(field_name=n))


@dataclass_json()
@dataclass
class Residue:
    chain: str
    structPosition: int
    position: int
    name1: str
    mean_bfactor: float
    norm_mean_bfactor: float
    dssp: str


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ResPos:
    residue_number: int


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class ChainMapping:
    start: ResPos
    end: ResPos
    chain_id: str
    struct_asym_id: str
    unp_start: int
    unp_end: int


@dataclass_json(letter_case=LetterCase.SNAKE)
@dataclass
class SIFTSUniProt:
    identifier: str
    name: str
    mappings: List[ChainMapping]


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SIFTS:
    uniprot: Optional[Dict[str, SIFTSUniProt]] = name("UniProt")


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class PDB:
    id: str
    url: str
    pdb_url: str
    title: str
    date: str
    method: str
    resolution: float
    het_groups: List[str]
    chains: Dict[str, Dict[str, Residue]]
    sifts: SIFTS = field(metadata=config(field_name="SIFTS"))


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class SAS:
    position: int
    from_aa: str
    to_aa: str


@dataclass_json()
@dataclass
class FoldXSAS:
    sas: SAS
    ddG: float
    sasa: float
    sasa_apolar: float
    sasa_polar: float


@dataclass_json()
@dataclass
class RepairedStructure:
    sasa: float
    sasa_apolar: float
    sasa_polar: float


@dataclass_json()
@dataclass
class Stability:
    duration: int
    repaired_structure: Optional[RepairedStructure] = None
    error: Optional[str] = None
    foldx: Optional[List[FoldXSAS]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Exposure:
    duration: int
    error: Optional[str] = None
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Pocket:
    name: str
    drug_score: float
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Binding:
    duration: int
    error: Optional[str] = None
    residues: Optional[List[Residue]] = None
    pockets: Optional[List[Pocket]] = None
    ligands: Optional[Dict[str, List[Residue]]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Interaction:
    duration: int
    error: Optional[str] = None
    residues: Optional[List[Residue]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class FamilyMapping:
    position: int
    position_model: int
    bitscore: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Family:
    id: str
    mappings: Optional[List[FamilyMapping]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Conservation:
    duration: int
    error: Optional[str] = None
    families: Optional[List[Family]] = None


@dataclass_json(letter_case=LetterCase.PASCAL)
@dataclass
class TangoResults:
    beta: float
    beta_turn: float
    helix: float
    aggregation: float
    helix_aggregation: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class TangoPos:
    position: int
    results: TangoResults


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AbSwitchResults:
    gor: str
    pah: float
    pae: float
    pac: float
    amb: float
    ins: float
    swi: float
    s5s: float


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class AbSwitchPos:
    position: int
    results: AbSwitchResults


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Secondary:
    duration: int
    error: Optional[str] = None
    tango: Optional[List[TangoPos]] = None
    abswitch: Optional[List[AbSwitchPos]] = None


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class StructureResults:
    uniprot: UniProt
    pdb: PDB
    stability: Optional[Stability] = None
    exposure: Optional[Exposure] = None
    binding: Optional[Binding] = None
    interaction: Optional[Interaction] = None
    conservation: Optional[Conservation] = None
    secondary: Optional[Secondary] = None
