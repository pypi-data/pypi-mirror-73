import pandas as pd


def wrangle_to_yearly(df, columns=None):
    """
    Wrangles a continuous dataframe (1x row per day) to a dataframe with
    one row per year.

    Parameters
    ----------
    df : pd.DataFrame
        with index as a DateTime Index
    columns : str or list of str
        Columns to use, by default all columns are used

    Returns
    -------
    df : pd.DataFrame

    """

    df = df.copy()

    df.loc[:, "date"] = df.index
    df.loc[:, "date"] = df.loc[:, "date"].apply(lambda x: x.strftime('2000-%m-%d'))
    # Format index for pivoting
    df.index = df.index.year.astype(str)
    df["date"] = pd.to_datetime(df.date, format="%Y-%m-%d")

    if not columns:
        columns = df.columns.tolist()
        columns.remove("date")

    df = df.pivot(columns='date', values=columns)

    return df
