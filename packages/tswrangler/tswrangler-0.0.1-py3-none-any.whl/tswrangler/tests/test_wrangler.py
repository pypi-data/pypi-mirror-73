from tswrangler import wrangler


def test_wrangle_to_yearly(continuous_timeseries):
    wrangled_df = wrangler.wrangle_to_yearly(continuous_timeseries, columns="price")
    assert len(wrangled_df.columns) == 366
