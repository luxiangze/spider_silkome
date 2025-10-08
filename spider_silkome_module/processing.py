"""
数据处理函数模块
用于处理 spidroin GFF 数据并提取位置信息
"""
from collections import defaultdict
from typing import List

from spider_silkome_module.models import GFFData, Position


def extract_positions_from_gff(
    gff_data: List[GFFData],
    positive_threshold: float = 0.85
) -> List[Position]:
    """
    从 GFF 数据中提取 spidroin 的位置信息
    
    根据 C 端和 N 端的比对结果，提取每个染色体-链组合的起始和终止位置。
    
    核心逻辑说明：
    - 正向链 (+)：基因从5'到3'，N端在前（start），C端在后（end）
    - 反向链 (-)：基因在反向互补链上，基因组坐标中start < end，但生物学意义上C端对应较小的坐标
    
    位置记录规则：
    | 类型 | 链方向 | 记录位置 | 原因                           |
    |------|--------|----------|--------------------------------|
    | CTD  | +      | end      | C端在基因末尾，向后延伸        |
    | CTD  | -      | start    | C端在基因起始（基因组坐标小），向前延伸 |
    | NTD  | +      | start    | N端在基因起始，向前延伸        |
    | NTD  | -      | end      | N端在基因末尾（基因组坐标大），向后延伸 |
    
    Parameters
    ----------
    gff_data : List[GFFData]
        miniprot 输出的 GFF 格式数据列表
    positive_threshold : float, optional
        质量阈值，过滤低于此阈值的比对结果，默认为 0.85
    
    Returns
    -------
    List[Position]
        按染色体和链排序的位置信息列表
    
    Examples
    --------
    >>> positions = extract_positions_from_gff(spidroin_gff_data, positive_threshold=0.85)
    >>> print(f"找到 {len(positions)} 个染色体-链组合")
    """
    # 用于存储每个染色体+链的位置信息
    positions_dict = defaultdict(lambda: {'start': defaultdict(int), 'end': defaultdict(int)})
    
    for aln in gff_data:
        # 过滤低质量比对
        if aln.attributes.Positive < positive_threshold:
            continue
        
        chr_id = aln.seqid
        strand = aln.strand
        key = (chr_id, strand)
        
        # 判断是C端还是N端
        domain_type = aln.attributes.Target[-1].split(" ")[0]
        
        if domain_type == 'CTD':  # C-terminal domain
            if strand == '+':  # 正向：C端在后面，记录end位置
                pos_value = aln.end
                positions_dict[key]['end'][pos_value] += 1
            else:  # 反向：C端在前面（基因组坐标），记录start位置
                pos_value = aln.start
                positions_dict[key]['start'][pos_value] += 1
        
        elif domain_type == 'NTD':  # N-terminal domain
            if strand == '+':  # 正向：N端在前面，记录start位置
                pos_value = aln.start
                positions_dict[key]['start'][pos_value] += 1
            else:  # 反向：N端在后面（基因组坐标），记录end位置
                pos_value = aln.end
                positions_dict[key]['end'][pos_value] += 1
    
    # 转换为 Position 对象列表
    positions = []
    for (chr_id, strand), pos_data in positions_dict.items():
        positions.append(Position(
            chr=chr_id,
            strand=strand,
            start=dict(pos_data['start']),
            end=dict(pos_data['end'])
        ))
    
    # 按染色体和链排序
    positions.sort(key=lambda x: (int(x.chr.replace('Chr', '')), x.strand))
    
    return positions
