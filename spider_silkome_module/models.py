"""
Data Model Definition for Data Structures Used in Spidroin Gene Annotation and Prediction
"""
from dataclasses import dataclass
from typing import Dict, List, Optional


@dataclass
class Attributes:
    """Data structure of the attributes field in the GFF file output by miniprot"""
    ID: str
    Rank: int
    Identity: float
    Positive: float
    Target: List[str]


@dataclass
class GFFData:
    """GFF format data output by miniprot"""
    seqid: str              # Sequence ID (Chromosome Name)
    source: str             # Source Text: Source (e.g., 'miniprot')
    type: str               # Feature types (such as 'gene', 'mRNA', 'CDS')
    start: int              # Starting position (1-based)
    end: int                # End position (1-based, inclusive)
    score: float            # Score
    strand: str             # Strand ('+' or '-')
    frame: str              # Reading frame ('0', '1', '2' or '.')
    attributes: Attributes  # Attribute Information


@dataclass
class Position:
    """
    Store the start and end position information on a specific chromosome-strand combination.
    For gene boundary prediction
    """
    chr: str                        # Chromosome name
    strand: str                     # Strand ('+' or '-')
    start: Optional[Dict[int, int]] # Start position and count {position: count}
    end: Optional[Dict[int, int]]   # End position and count {position: count}

    def __post_init__(self):
        """Post initialization processing, ensure start and end are dictionaries"""
        if self.start is None:
            self.start = {}
        if self.end is None:
            self.end = {}

    def has_valid_pair(self) -> bool:
        """Check if there is a valid start-end pair"""
        return bool(self.start and self.end)

    def get_combinations_count(self) -> int:
        """Get the number of possible start-end combinations"""
        return len(self.start) * len(self.end)


@dataclass
class GenePrediction:
    """Gene prediction result"""
    chr: str
    strand: str
    start_position: int
    start_count: int
    end_position: int
    end_count: int
    length: int
    score: int
    valid: bool
    reason: str

    @classmethod
    def from_positions(
        cls,
        chr: str,
        strand: str,
        start_pos: int,
        start_count: int,
        end_pos: int,
        end_count: int,
        min_length: int = 1000,
        max_length: int = 100000
    ) -> 'GenePrediction':
        """
        Create gene prediction from position information

        Parameters:
        - chr: Chromosome name
        - strand: Strand ('+' or '-')
        - start_pos: Start position
        - start_count: Start position count
        - end_pos: End position
        - end_count: End position count
        - min_length: Minimum gene length threshold
        - max_length: Maximum gene length threshold
        """
        if start_pos < end_pos:
            length = end_pos - start_pos
            score = start_count + end_count

            if length < min_length:
                valid = False
                reason = f'too_short_{length}'
            elif length > max_length:
                valid = False
                reason = f'too_long_{length}'
            else:
                valid = True
                reason = 'valid'
        else:
            length = 0
            score = 0
            valid = False
            reason = 'invalid_order'

        return cls(
            chr=chr,
            strand=strand,
            start_position=start_pos,
            start_count=start_count,
            end_position=end_pos,
            end_count=end_count,
            length=length,
            score=score,
            valid=valid,
            reason=reason
        )
