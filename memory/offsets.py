from enum import Enum, unique


@unique
class Offset(int, Enum):
    dw_entity_list = 0x17B5200
    dw_local_player_pawn = 0x16BC5B8
    m_i_id_ent_index = 0x153C
    m_i_team_num = 0x3BF
    m_i_health = 0x32C
