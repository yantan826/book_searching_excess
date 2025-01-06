import pandas as pd 

def get_to_read_titles(file_path):
    df = pd.read_csv(file_path)
    # df = df[df['Exclusive Shelf'] == 'to-read']
    titles_and_authors = list(zip(df['Title'].values, df['Author'].values))
    return titles_and_authors

# Example usage:
# titles_and_authors = get_to_read_titles('data/goodreads_library_export.csv')