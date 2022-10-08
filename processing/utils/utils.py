def group_bool_columns(df, cols_name, new_col_name, index) -> None:
    new_category_data = []

    for i in range(df.shape[0]):
        new_category_data.append([j[index:] for j, k in df.iloc[i][cols_name].items() if k == True])

    df.drop(columns=cols_name, inplace=True)
    df[new_col_name] = new_category_data
