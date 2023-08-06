import statistics

from dataclasses import dataclass, field, astuple
from typing import List, Optional

import requests
from dataclasses_json import LetterCase, config, dataclass_json

from .structure import Residue, StructureResults, Family
from .uniprot import Variant

STATUS = {
    0: "in queue",
    1: "processing",
    2: "done",
}


class PositionError(Exception):
    pass


class NotFoundInResults(Exception):
    pass


class SIFTSError(Exception):
    pass


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Request:
    name: str
    uniprot_id: str
    pdb_ids: List[str]
    sas: List[str]
    ip: str
    email: str
    time: str


@dataclass_json(letter_case=LetterCase.CAMEL)
@dataclass
class Results:
    id: str
    request: Request
    status: str
    started: str
    ended: str


class Job():
    def __init__(self, protocol: str, host: str, job_id: str):
        self.host = host
        self.protocol = protocol
        self.api_url = f"{protocol}://{host}/api"
        self.id = job_id

        self._update()

    def _update(self):
        url = f"{self.api_url}/job/{self.id}"
        self.overview = Results.from_json(requests.get(url).text)
        if self.overview.status == 2:
            struct_res_url = f"{url}/{self.overview.request.pdb_ids[0]}"
            self.results = StructureResults.from_json(requests.get(struct_res_url).text)
            self._create_mappings()

    @property
    def _unp_mappings(self):
        sifts = self.results.pdb.sifts.uniprot
        unp_id = self.overview.request.uniprot_id
        if unp_id not in sifts.keys():
            raise SIFTSError("UniProt protein not in PDB structure.")

        return self.results.pdb.sifts.uniprot[self.overview.request.uniprot_id].mappings

    @property
    def status(self):
        self._update()
        status_code = self.overview.status
        return status_code, STATUS[status_code]

    def _create_mappings(self):
        self.mappings = {}
        for chain in self._unp_mappings:
            self.mappings[chain.struct_asym_id] = -chain.unp_start + chain.start.residue_number

    def _check_bounds(self, unp_pos: int):
        if not self.in_structure(unp_pos):
            raise PositionError("UniProt position not included in PDB structure.")

    def in_structure(self, unp_pos: int) -> bool:
        for chain in self._unp_mappings:
            if chain.unp_start <= unp_pos <= chain.unp_end:
                return True
        return False

    def _has_residue(self, res_list: List[Residue], unp_pos: int) -> bool:
        if not res_list:
            return False
        self._check_bounds(unp_pos)
        for res in res_list:
            if res.chain in self.mappings.keys() and res.position == self.unp_to_pdb(res.chain, unp_pos):
                return True
        return False

    def struct_res(self, unp_pos: int) -> List[Residue]:
        self._check_bounds(unp_pos)
        r = []
        for chain, residues in self.results.pdb.chains.items():
            for _, chain_res in residues.items():
                if chain in self.mappings.keys() and chain_res.position == self.unp_to_pdb(chain_res.chain, unp_pos):
                    r.append(chain_res)
        return r

    def _sas(self, sas: str):
        for mut in self.results.stability.foldx:
            s = mut.sas
            if s.from_aa + str(s.position) + s.to_aa == sas:
                return mut
        raise NotFoundInResults("SAS not found in FoldX results.")

    def unp_to_pdb(self, chain: str, unp_pos: int) -> int:
        return self.mappings[chain] + unp_pos

    def variant(self, change: str) -> Optional[Variant]:
        for var in self.results.uniprot.variants:
            if var.change == change:
                return var
        return None

    def repaired_sasa(self) -> float:
        r = self.results.stability.repaired_structure
        return r.sasa, r.sasa_apolar, r.sasa_polar

    def sas_sasa(self, sas: str) -> float:
        s = self._sas(sas)
        return s.sasa, s.sasa_apolar, s.sasa_polar

    def sas_ddg(self, sas: str) -> float:
        return self._sas(sas).ddG

    def buried(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.exposure.residues, unp_pos)

    def catalytic(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.binding.catalytic.residues, unp_pos)

    def binding(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.binding.residues, unp_pos)

    def near_ligands(self, unp_pos: int) -> bool:
        near = []
        for lig, residues in self.results.binding.ligands.items():
            if self._has_residue(residues, unp_pos):
                near.append(lig)
        return near

    def interface(self, unp_pos: int) -> bool:
        return self._has_residue(self.results.interaction.residues, unp_pos)

    def pocket(self, unp_pos: int) -> bool:
        for pocket in self.results.binding.pockets:
            if self._has_residue(pocket.residues, unp_pos):
                return True
        return False

    def bfactor(self, unp_pos: int) -> float:
        residues = self.struct_res(unp_pos)
        if len(residues) == 0:
            return 0
        return statistics.mean(r.mean_bfactor for r in residues)

    def bfactor_norm(self, unp_pos: int) -> float:
        residues = self.struct_res(unp_pos)
        if len(residues) == 0:
            return 0
        return statistics.mean(r.norm_mean_bfactor for r in residues)

    def dssp(self, unp_pos: int) -> float:
        residues = self.struct_res(unp_pos)
        if len(residues) == 0:
            return " "
        return residues[0].dssp

    def disulfide(self, unp_pos: int) -> bool:
        if not self.results.uniprot.ptms.disulfide_bonds:
            return False
        for bond in self.results.uniprot.ptms.disulfide_bonds:
            if bond.positions[0] == unp_pos or bond.positions[1] == unp_pos:
                return True
        return False

    def glycosilation(self, unp_pos: int) -> bool:
        if not self.results.uniprot.ptms.glycosilation_sites:
            return False
        for glyco in self.results.uniprot.ptms.glycosilation_sites:
            if glyco.position == unp_pos:
                return True
        return False

    def families(self) -> List[Family]:
        return [fam.id for fam in self.results.conservation.families]

    def conservation(self, unp_pos: int) -> float:
        for fam in self.results.conservation.families:
            for res in fam.mappings:
                if res.position == unp_pos:
                    return res.bitscore

        return 0

    def aggregation(self, unp_pos: int) -> float:
        for res in self.results.secondary.tango:
            if res.position == unp_pos:
                return res.results.aggregation
        return 0

    def tango_fields(self, unp_pos: int) -> tuple:
        for res in self.results.secondary.tango:
            if res.position == unp_pos:
                return astuple(res.results)
        return ()

    def switchability(self, unp_pos: int) -> float:
        for res in self.results.secondary.abswitch:
            if res.position == unp_pos:
                return res.results.s5s
        return 0

    def abswitch_fields(self, unp_pos: int) -> tuple:
        for res in self.results.secondary.abswitch:
            if res.position == unp_pos:
                return astuple(res.results)
        return ()
