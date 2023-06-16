from neet.ml_logic.data import clean_data


def test_clean_data(train, train_cleaned):
    df_cleaned = clean_data(train)
    assert df_cleaned.shape == train_cleaned.shape
    diff_means = df_cleaned['XXX'].mean() - train_cleaned['XXX'].mean()
    assert round(diff_means, 3) == 0
