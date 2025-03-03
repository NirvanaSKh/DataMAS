def analyze_data(dataframe):
    if dataframe.empty:
        return None

    column_count = len(dataframe.columns)
    
    if column_count == 2:
        return "comparison"
    elif column_count > 2:
        return "trends"
    return "distribution"
