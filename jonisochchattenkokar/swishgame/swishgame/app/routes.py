from flask import Blueprint, request, jsonify
from .db import get_db
from .utils import triangelfordelning
from datetime import datetime
import uuid

game_bp = Blueprint('game', __name__)

roll_index = {}

@game_bp.route('/roll', methods=['POST'])
def roll():
    data = request.get_json()

    spelare = data['spelare']
    mottagare = data['mottagare']
    pengar = int(data['pengar'])
    std = int(data['avvikelse'])
    dricks = int(data['dricks'])
    grupp_id = data['grupp_id']

    medelvärde = pengar
    slumptal, minv, maxv = triangelfordelning(medelvärde, std, dricks)

    game_id = data.get('game_id') or str(uuid.uuid4())

    index = roll_index.get(game_id, 1)
    roll_index[game_id] = index + 1

    datum_tid = datetime.now().isoformat()
    db = get_db()
    db.execute('''
        INSERT INTO games (game_id, roll, pengar_i_spel, dricks, avvikelse, grupp_id,
                           spelare, mottagare, slumptal, datum_tid)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ''', (game_id, index, pengar, dricks, std, grupp_id,
          spelare, mottagare, slumptal, datum_tid))
    db.commit()

    return jsonify({
        'game_id': game_id,
        'roll': index,
        'slumptal': slumptal,
        'min': minv,
        'max': maxv,
        'tid': datum_tid
    })