import os
from tqdm import tqdm
import urllib.request
import ssl
from loguru import logger
import progressbar
import multiprocessing as mp
from multiprocessing import Process, Manager
from multiprocessing import Pool
import shutil

num_processes = mp.cpu_count()


pbar = None


def download_and_process(files):

    url_string = "http://commoncrawl.s3.amazonaws.com/"

    for f in tqdm(files, desc="individual"):
        head, filename = os.path.split(f)
        download_url = f"{url_string}{f}"
        folder_location = filename.replace(".warc.gz", "")
        save_location = f"{folder_location}/{filename}"

        logger.info(f"File location: {save_location}")
        logger.info(f"Filename: {filename}")
        logger.info(f"Download url: {download_url}")
        os.mkdir(folder_location)
        urllib.request.urlretrieve(download_url, save_location, show_progress)
        logger.success(f"Filename {filename} done")

        os.system(
            f'python crawl_instructions.py --input_warc_dir="./{folder_location}" --output_instruction_json="./prep/crawled_instruction_{filename}.json"'
        )

        logger.info(f"Saving file to: ./prep/crawled_instruction_{filename}.json")

        shutil.rmtree(folder_location)
        logger.info(f"Deleting location: {folder_location}")


def show_progress(block_num, block_size, total_size):
    global pbar
    if pbar is None:
        pbar = progressbar.ProgressBar(maxval=total_size)
        pbar.start()

    downloaded = block_num * block_size
    if downloaded < total_size:
        pbar.update(downloaded)
    else:
        pbar.finish()
        pbar = None


manager = Manager()

d = manager.dict()


with open("used_warc.paths") as f:
    files = [line.rstrip() for line in f]

logger.info(f"Number of processes: {num_processes}")

files_split = [
    files[x : x + num_processes] for x in range(0, len(files), num_processes)
]

pool = Pool(num_processes)
for _ in tqdm(
    pool.map(download_and_process, files_split),
    total=num_processes,
    desc="All processes",
):
    pass
pool.close()
pool.join()

