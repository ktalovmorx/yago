import json

def init(dim:int=None) -> dict:
    '''
    Carga el archivo de configuracion 2048.ini
    parameters
    ----------
        :param dim : int
                description ->

    returns
    -------
        bool
    '''

    if not dim:
        with open('2048.ini', 'r') as archivo:
            # Carga el contenido del archivo JSON en un diccionario
            data = json.load(archivo)
    else:
        data = {'dim': 4, 'max_score': 2048}
    return data

def play(game:dict) -> None:
    '''
    Carga el archivo de configuracion 2048.ini
    parameters
    ----------
        :param game : dict
                description ->

    returns
    -------
        bool
    '''
    return None

def finalize(game:dict) -> None:
    '''
    Finaliza el juego
    parameters
    ----------
        :param game : dict
                description ->

    returns
    -------
        None
    '''
    return None

def main(dim):
    game = init(dim)
    play(game)
    finalize(game)

main()