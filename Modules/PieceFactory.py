import Pawn as p
import Knight as k
import Bishop as b
import Rook as r
import Queen as q
import King as kg

def createPiece(name, white):
    pieces = {
        "Pawn": p.Pawn,
        "Knight": k.Knight,
        "Bishop": b.Bishop,
        "Rook": r.Rook,
        "Queen": q.Queen,
        "King": kg.King,
    }
    return pieces.get(name)(white) if name in pieces else None
