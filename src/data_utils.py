import pandas as pd
import pyarrow.parquet as pq
import os
# Read the Parquet file into a DataFrame
def estimate_compression_factor(df, engine='pyarrow', compression='snappy'):
    temp_file = 'temp.parquet'
    df.to_parquet(temp_file, engine=engine, compression=compression)
    uncompressed_size = df.memory_usage(index=True, deep=True).sum()
    compressed_size = os.path.getsize(temp_file)
    os.remove(temp_file)
    return uncompressed_size / compressed_size


def split_parquet_file_into_chunks(input_file_path, desired_chunk_size, output_folder):
    df = pd.read_parquet(input_file_path, engine='pyarrow')
    compression_factor = estimate_compression_factor(df)
    # Calculate the number of rows per chunk to keep the size below 25 MB
    bytes_per_row = df.memory_usage(index=True, deep=True).sum() / len(df)
    max_chunk_size_bytes = desired_chunk_size * 1024 * 1024  
    rows_per_chunk = int((max_chunk_size_bytes * compression_factor) / bytes_per_row) # 25 MB in bytes

    # Split the DataFrame into smaller DataFrames
    dfs = [df[i:i + rows_per_chunk] for i in range(0, len(df), rows_per_chunk)]

    for idx, chunk in enumerate(dfs):
        output_file = f"{output_folder}/tmWordsSingles_chunk_{idx}.parquet"
        chunk.to_parquet(output_file, engine='pyarrow')

def load_and_merge_chunks(input_folder, engine='pyarrow'):
    file_list = [f for f in os.listdir(input_folder) if f.endswith('.parquet')]

    # Sort the file list to preserve the original order of the chunks
    #file_list.sort(key=lambda x: int(x.split('_')[1].split('.')[0]))

    # Load and merge the chunks into a single DataFrame
    merged_df = pd.DataFrame()
    for file in file_list:
        file_path = os.path.join(input_folder, file)
        df_chunk = pd.read_parquet(file_path, engine=engine)
        merged_df = pd.concat([merged_df, df_chunk], ignore_index=True)

    return merged_df
if __name__ =='__main__':

    # input_file = 'data/tmWordsSingles.parquet'

    # split_parquet_file_into_chunks(input_file, 24, "data/")
    input_folder = 'data/'
    merged_df = load_and_merge_chunks(input_folder)
    print(merged_df.shape)
