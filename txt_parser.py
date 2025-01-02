from datetime import datetime
import os

def file_parser(file_content):
    """
    Parse the input file content into batches based on the presence of `^PQ` and `^XZ`.
    Returns two lists:
    - `batches_with_pq`: List of batches containing the `^PQ` marker.
    - `batches_without_pq`: List of batches without the `^PQ` marker.
    """
    batches_reconstructed = []
    batches_with_pq = []
    batches_without_pq = []
    batch_files = []

    now = int(datetime.now().timestamp())

    # Strip and split the input content
    data = file_content.strip()  # Remove leading/trailing whitespace
    batches_list = data.split('^XZ')  # Split into batches using `^XZ`

    # Reconstruct batches by appending `^XZ` (if not empty)
    for item in batches_list:
        if item.strip():  # Ignore empty batches
            batches_reconstructed.append(item + '^XZ')

    # Separate batches with and without '^PQ'
    for batch in batches_reconstructed:
        if '^PQ' in batch:
            batches_with_pq.append(batch)
        else:
            batches_without_pq.append(batch)

    # Process batches with '^PQ' one by one
    for i, batch in enumerate(batches_with_pq, start=1):
        file_path = f'queue/{now}_batch_with_pq_{i}.txt'
        os.makedirs('queue', exist_ok=True)  # Ensure the directory exists
        with open(file_path, 'w') as f:
            f.write(batch)
        batch_files.append(file_path)

    # Process batches without '^PQ' in groups of 50
    for i in range(0, len(batches_without_pq), 50):
        combined_batch = ''.join(batches_without_pq[i:i+50])
        file_path = f'queue/{now}_batch_without_pq_{i//50 + 1}.txt'
        os.makedirs('queue', exist_ok=True)  # Ensure the directory exists
        with open(file_path, 'w') as f:
            f.write(combined_batch)
        batch_files.append(file_path)

    return batch_files, now