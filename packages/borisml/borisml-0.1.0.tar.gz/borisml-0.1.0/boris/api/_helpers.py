import os

import pandas as pd

from itertools import islice

from boris.api._communication import get_presigned_upload_url
from boris.api._communication import upload_file_with_signed_url
from boris.api._communication import upload_embedding
from boris.data import BorisDataset
from boris.utils import pandas_to_dict

import tqdm
from concurrent.futures import ThreadPoolExecutor

MAXIUM_DATASET_SIZE = 100_000


def upload_embeddings_from_csv(path_to_embeddings: str,
                               dataset_id: str,
                               token: str,
                               max_upload: int = 512):
    """Uploads embeddings from a csv file to the cloud solution

    Args:
        path_to_embeddings: Path to csv file containing embeddings
        dataset_id: The unique identifier for the dataset
        token: Token for authentication
    """
    df = pd.read_csv(path_to_embeddings)
    data = pandas_to_dict(df)

    for embedding in data['embeddings']:
        embedding['fileName'] = os.path.basename(embedding['fileName'])

    data['token'] = token
    data['datasetId'] = dataset_id

    def _upload_single_batch(batch, append=False):
        batch['append'] = int(append)
        success = upload_embedding(batch)
        return success

    n_embeddings = len(data['embeddings'])
    n_batches = n_embeddings // max_upload
    n_batches = n_batches + 1 if n_embeddings % max_upload else n_batches

    embedding_batches = [None] * n_batches
    for i in range(n_batches):
        left = i*max_upload
        right = min((i + 1) * max_upload, n_embeddings)
        batch = data.copy()
        batch['embeddings'] = data['embeddings'][left:right]
        embedding_batches[i] = batch

    pbar = tqdm.tqdm(unit='embs', total=n_embeddings)
    for i, batch in enumerate(embedding_batches):
        success = _upload_single_batch(batch, append=i > 0)
        if not success:
            raise RuntimeError('Error during upload of embedding')
        pbar.update(len(batch['embeddings']))

    return success


def upload_images_from_folder(path_to_folder: str,
                              dataset_id: str,
                              token: str,
                              max_workers: int = 16,
                              max_requests: int = 16):

    bds = BorisDataset(from_folder=path_to_folder)
    fnames = bds.get_filenames()

    if len(fnames) > MAXIUM_DATASET_SIZE:
        raise ValueError(f'Your dataset has {len(fnames)} samples which' +
                         f'is more than the maximum of {MAXIUM_DATASET_SIZE}')

    def _upload_single_image(fname):
        basename = os.path.basename(fname)
        signed_url, success = get_presigned_upload_url(
            basename, dataset_id, token)
        if success:
            full_fname = os.path.join(path_to_folder, fname)
            success = upload_file_with_signed_url(full_fname, signed_url)
        return success

    n_batches = len(fnames) // max_requests
    n_batches = n_batches + 1 if len(fnames) % max_requests else n_batches
    fname_batches = [
        list(islice(fnames, i * max_requests, (i + 1) * max_requests))
        for i in range(n_batches)
    ]

    chunksize = max(max_requests // max_workers, 1)
    executor = ThreadPoolExecutor(max_workers=max_workers)

    pbar = tqdm.tqdm(unit='imgs', total=len(fnames))
    for i, batch in enumerate(fname_batches):
        mapped = executor.map(_upload_single_image, batch, chunksize=chunksize)
        mapped = list(mapped)
        if not all(mapped):
            msg = 'Warning: Unsuccessful upload(s) in batch {}! '.format(i)
            msg += 'This could cause problems when uploading embeddings.'
            msg += 'Failed at file: {}'.format(batch[batch.find(False)])
            print(msg)
        pbar.update(len(batch))


def upload_metadata_from_json(path_to_embeddings: str,
                              dataset_id: str,
                              token: str):
    pass
