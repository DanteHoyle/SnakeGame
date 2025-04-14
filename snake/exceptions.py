class InvalidGameStateError(Exception):
    """
    SnakeGame will throw this exception if it encounters a game state when it should not
    """

class ImpossibleConfigError(Exception):
    """
    main.py will throw this error if there are any invalid configs thrown. This should be impossible
    but may occur if there's a mistake in the argparse calls
    """
