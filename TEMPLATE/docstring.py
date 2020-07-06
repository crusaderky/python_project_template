class Vehicles(object):
    """The Vehicle object contains a lot of vehicles

    Parameters
    ----------
    arg : str
        The arg is used for...
    *args :
        The variable arguments are used for...
    **kwargs :
        The keyword arguments are used for...

    Returns
    -------

    """
    def __init__(self, arg, *args, **kwargs):
        self.arg = arg

    def cars(self, distance,destination):
        """We can't travel distance in vehicles without fuels, so here is the fuels

        Parameters
        ----------
        distance : int
            The amount of distance traveled
        destination : bool
            Should the fuels refilled to cover the distance?

        Returns
        -------
        cars
            A car mileage

        Raises
        ------
        RuntimeError
            Out of fuel

        """
        pass