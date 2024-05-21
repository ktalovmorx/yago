import game2048

def test_move_row_right():
    game = {
        'board' : [[0, 2, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 3, -1, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 2],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 0
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 2, 2, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 1, 3, -1, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 4],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 4
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 64, 64, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 2, 3, -1, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 2, 128],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 128
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 2, 64, 64]]
    }
    moved, score = game2048.move_row(game, 3, 3, -1, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 4, 128]]
    assert moved
    assert score == 132
    print('OK')

    game = {
        'board' : [[2, 64, 128, 256],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 3, -1, False)
    print(game['board'])
    assert game['board'] == [[2, 64, 128, 256],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert not moved
    assert score == 0
    print('OK')


def test_move_row_left():
    game = {
        'board' : [[0, 2, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 0, 4, False)
    print(game['board'])
    assert game['board'] == [[2, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 0
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 2, 2, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 1, 0, 4, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [4, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 4
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 64, 64, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 2, 0, 4, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [2, 128, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 128
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 2, 64, 64]]
    }
    moved, score = game2048.move_row(game, 3, 0, 4, False)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [4, 128, 0, 0]]
    assert moved
    assert score == 132
    print('OK')

    game = {
        'board' : [[2, 64, 128, 256],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 0, 4, False)
    print(game['board'])
    assert game['board'] == [[2, 64, 128, 256],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert not moved
    assert score == 0
    print('OK')

def test_move_row_down():
    game = {
        'board' : [[2, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [2, 0, 0, 0]]
    assert moved
    assert score == 0
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 2, 0, 0],
                   [0, 2, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 1, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 4, 0, 0]]
    assert moved
    assert score == 4
    print('OK')

    game = {
        'board' : [[0, 0, 2, 0],
                   [0, 0, 64, 0],
                   [0, 0, 64, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 2, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 2, 0],
                             [0, 0, 128, 0]]
    assert moved
    assert score == 128
    print('OK')

    game = {
        'board' : [[0, 0, 0, 2],
                   [0, 0, 0, 2],
                   [0, 0, 0, 64],
                   [0, 0, 0, 64]]
    }
    moved, score = game2048.move_row(game, 3, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 4],
                             [0, 0, 0, 128]]
    assert moved
    assert score == 132
    print('OK')

    game = {
        'board' : [[0, 0, 0, 256],
                   [0, 0, 0, 128],
                   [0, 0, 0, 64],
                   [0, 0, 0, 32]]
    }
    moved, score = game2048.move_row(game, 0, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 256],
                             [0, 0, 0, 128],
                             [0, 0, 0, 64],
                             [0, 0, 0, 32]]
    assert not moved
    assert score == 0
    print('OK')

def test_move_row_up():
    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [0, 0, 0, 0],
                   [2, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 0, 0, 4, True)
    print(game['board'])
    assert game['board'] == [[2, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 0
    print('OK')

    game = {
        'board' : [[0, 0, 0, 0],
                   [0, 2, 0, 0],
                   [0, 2, 0, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 1, 0, 4, True)
    print(game['board'])
    assert game['board'] == [[0, 4, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 4
    print('OK')

    game = {
        'board' : [[0, 0, 2, 0],
                   [0, 0, 64, 0],
                   [0, 0, 64, 0],
                   [0, 0, 0, 0]]
    }
    moved, score = game2048.move_row(game, 2, 0, 4, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 2, 0],
                             [0, 0, 128, 0],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 128
    print('OK')

    game = {
        'board' : [[0, 0, 0, 2],
                   [0, 0, 0, 2],
                   [0, 0, 0, 64],
                   [0, 0, 0, 64]]
    }
    moved, score = game2048.move_row(game, 3, 0, 4, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 4],
                             [0, 0, 0, 128],
                             [0, 0, 0, 0],
                             [0, 0, 0, 0]]
    assert moved
    assert score == 132
    print('OK')

    game = {
        'board' : [[0, 0, 0, 256],
                   [0, 0, 0, 128],
                   [0, 0, 0, 64],
                   [0, 0, 0, 32]]
    }
    moved, score = game2048.move_row(game, 0, 0, 4, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 256],
                             [0, 0, 0, 128],
                             [0, 0, 0, 64],
                             [0, 0, 0, 32]]
    assert not moved
    assert score == 0
    print('OK')


def test_1():
    game = {
        'board': [[0, 0, 0, 2],
                  [0, 0, 2, 0],
                  [0, 0, 0, 8],
                  [32,4, 4, 4]]
    }
    moved, score = game2048.move_row(game, 3, 3, -1, True)
    print(game['board'])
    assert game['board'] == [[0, 0, 0, 0],
                             [0, 0, 2, 2],
                             [0, 0, 0, 8],
                             [32,4, 4, 4]]
    assert moved
    assert score == 0
    print('OK')
