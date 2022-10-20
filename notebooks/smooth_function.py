def smooth_array(array, width):
    """Smooth a 1D array of data using a boxcar filter.
    Parameters
    ----------
    array: np.array[float]
        The array to be smoothed.
    width: int
        The size of the boxcar filter.
    Returns
    -------
    smoothed: np.ndarray
        The smoothed array
    """
    if width is None or width == 0:
        return array

    array = np.reshape(array, (len(array), ))  # todo: why do I have to do this? safety probably
    return convolve(array, boxcar(width) / float(width), mode="same")
