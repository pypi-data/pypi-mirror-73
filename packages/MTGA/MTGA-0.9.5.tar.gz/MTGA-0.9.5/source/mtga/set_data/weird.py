""" WARNING! These cards are no longer in MTGA! This file is likely incorrect, and is left only for reference.

"""
from mtga.models.card import Card
from mtga.models.card_set import Set

CinderBarrens = Card("cinder_barrens", "Cinder Barrens", [], ["B", "R"], "Land", "", "OGW", "Common", -1, 62499)
TranquilExpanse = Card("tranquil_expanse", "Tranquil Expanse", [], ["G", "W"], "Land", "", "OGW", "Common", -1, 62523)
MeanderingRiver = Card("meandering_river", "Meandering River", [], ["U", "W"], "Land", "", "OGW", "Common", -1, 62509)
SubmergedBoneyard = Card("submerged_boneyard", "Submerged Boneyard", [], ["B", "U"], "Land", "", "OGW", "Common", -1, 62519)
TimberGorge = Card("timber_gorge", "Timber Gorge", [], ["G", "R"], "Land", "", "OGW", "Common", -1, 62521)

# TODO: why are these offset more than the others?

FullArtPlainsAKH = Card("plains", "Plains", [], ['W'], "Basic Land", "Plains", "AKH", "Common", 251, 65433)
FullArtIslandAKH = Card("island", "Island", [], ['U'], "Basic Land", "Island", "AKH", "Common", 250, 65435)
FullArtSwampAKH = Card("swamp", "Swamp", [], ['B'], "Basic Land", "Swamp", "AKH", "Common", 252, 65437)
FullArtMountainAKH = Card("mountain", "Mountain", [], ['R'], "Basic Land", "Mountain", "Common", "AKH", 253, 65439)
FullArtForestAKH = Card("forest", "Forest", [], ['G'], "Basic Land", "Forest", "AKH", "Common", 254, 65441)


WeirdLands = Set("weird_lands", cards=[CinderBarrens, TranquilExpanse, MeanderingRiver, TimberGorge, SubmergedBoneyard,
                                       FullArtPlainsAKH, FullArtIslandAKH, FullArtSwampAKH, FullArtMountainAKH, FullArtForestAKH])
