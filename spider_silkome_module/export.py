"""
导出 positions 数据到不同格式的工具函数
"""
from typing import List

import pandas as pd
from loguru import logger

from spider_silkome_module.models import GenePrediction, Position


def positions_export(
    positions: List[Position],
    output_file: str,
    format: str = 'csv',
    spidroin: str = None,
    min_length: int = 1000,
    max_length: int = 100000
):
    """
    Export the positions list to CSV or GFF format.

    Parameters:
    - positions: List of Position objects
    - output_file: Output file path
    - format: Output format, 'csv' or 'gff' (default 'csv')
    - spidroin: Spidroin name (required for GFF format ID generation)
    - min_length: Minimum gene length threshold (default 1000bp)
    - max_length: Maximum gene length threshold (default 100000bp)

    Returns:
    - If CSV format, returns DataFrame
    - If GFF format, returns list of gff_records
    """
    if format.lower() == 'csv':
        return _export_to_csv(positions, output_file, min_length, max_length)
    elif format.lower() == 'gff':
        if spidroin is None:
            raise ValueError("GFF 格式需要提供 spidroin 参数")
        return _export_to_gff(spidroin, positions, output_file, min_length, max_length)
    else:
        raise ValueError(f"不支持的格式: {format}，请使用 'csv' 或 'gff'")


def _export_to_csv(
    positions: List[Position],
    output_file: str,
    min_length: int,
    max_length: int
) -> pd.DataFrame:
    """Convert positions list to CSV format with all possible start-end pairs"""
    predictions: List[GenePrediction] = []

    for pos in positions:
        # Get all start and end positions
        start_positions = sorted(pos.start.keys()) if pos.start else []
        end_positions = sorted(pos.end.keys()) if pos.end else []

        # Handle cases with missing start or end
        if not start_positions and not end_positions:
            continue
        elif not start_positions:
            # Only end positions available
            for end_pos, end_count in pos.end.items():
                pred = GenePrediction(
                    chr=pos.chr,
                    strand=pos.strand,
                    start_position=0,
                    start_count=0,
                    end_position=end_pos,
                    end_count=end_count,
                    length=0,
                    score=0,
                    valid=False,
                    reason='no_start'
                )
                predictions.append(pred)
        elif not end_positions:
            # Only start positions available
            for start_pos, start_count in pos.start.items():
                pred = GenePrediction(
                    chr=pos.chr,
                    strand=pos.strand,
                    start_position=start_pos,
                    start_count=start_count,
                    end_position=0,
                    end_count=0,
                    length=0,
                    score=0,
                    valid=False,
                    reason='no_end'
                )
                predictions.append(pred)
        else:
            # Generate all possible start-end pairs
            for start_pos in start_positions:
                for end_pos in end_positions:
                    start_count = pos.start[start_pos]
                    end_count = pos.end[end_pos]

                    # Use GenePrediction model to create prediction
                    pred = GenePrediction.from_positions(
                        chr=pos.chr,
                        strand=pos.strand,
                        start_pos=start_pos,
                        start_count=start_count,
                        end_pos=end_pos,
                        end_count=end_count,
                        min_length=min_length,
                        max_length=max_length
                    )
                    predictions.append(pred)

    # Convert to DataFrame
    rows = [
        {
            'chr': pred.chr,
            'strand': pred.strand,
            'start_position': pred.start_position if pred.start_position > 0 else '',
            'start_count': pred.start_count if pred.start_count > 0 else '',
            'end_position': pred.end_position if pred.end_position > 0 else '',
            'end_count': pred.end_count if pred.end_count > 0 else '',
            'length': pred.length if pred.length > 0 else '',
            'score': pred.score if pred.score > 0 else '',
            'valid': pred.valid,
            'reason': pred.reason
        }
        for pred in predictions
    ]

    df = pd.DataFrame(rows)
    df = df.sort_values(['chr', 'strand', 'start_position', 'end_position'])
    df.to_csv(output_file, index=False)

    logger.info(f"CSV saved to {output_file}")
    logger.info(f"Total combinations: {len(df)}")
    logger.info(f"Valid combinations: {df['valid'].sum()}")
    logger.info(f"Invalid combinations: {(~df['valid']).sum()}")

    return df


def _export_to_gff(
    spidroin: str,
    positions: List[Position],
    output_file: str,
    min_length: int,
    max_length: int
) -> List[dict]:
    """
    Convert positions to GFF format gene predictions

    Parameters:
    - spidroin: Spidroin name
    - positions: List of Position objects
    - output_file: Output GFF file path
    - min_length: Minimum gene length threshold
    - max_length: Maximum gene length threshold
    """
    gff_records = []
    gene_id = 1

    for pos in positions:
        # Skip records without both start and end
        if not pos.has_valid_pair():
            continue

        # Get all start and end positions
        start_positions = sorted(pos.start.keys())
        end_positions = sorted(pos.end.keys())

        # Iterate through all possible start-end combinations
        for start_pos in start_positions:
            for end_pos in end_positions:
                # Create prediction using the model
                pred = GenePrediction.from_positions(
                    chr=pos.chr,
                    strand=pos.strand,
                    start_pos=start_pos,
                    start_count=pos.start[start_pos],
                    end_pos=end_pos,
                    end_count=pos.end[end_pos],
                    min_length=min_length,
                    max_length=max_length
                )

                # Only include valid predictions
                if pred.valid:
                    gff_records.append({
                        'seqid': pred.chr,
                        'source': 'miniprot',
                        'type': 'gene',
                        'start': pred.start_position,
                        'end': pred.end_position,
                        'score': pred.score,
                        'strand': pred.strand,
                        'phase': '.',
                        'attributes': f'ID={spidroin}_{gene_id:04d};length={pred.length};start_count={pred.start_count};end_count={pred.end_count}'
                    })
                    gene_id += 1

    # 写入 GFF 文件
    with open(output_file, 'w') as f:
        f.write("##gff-version 3\n")
        for record in gff_records:
            line = '\t'.join([
                str(record['seqid']),
                str(record['source']),
                str(record['type']),
                str(record['start']),
                str(record['end']),
                str(record['score']),
                str(record['strand']),
                str(record['phase']),
                str(record['attributes'])
            ])
            f.write(line + '\n')

    logger.info(f"GFF saved to {output_file}")
    logger.info(f"Total genes predicted: {len(gff_records)}")

    return gff_records
