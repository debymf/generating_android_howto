# AndroidHowTo dataset

:rotating_light: **Attention** :rotating_light: The code in this repo was designed to facilitate the download and generation of the AndroidHowTo dataset. All credit goes to the authors of the Seq2Act paper, I am only reproducing their results. If you use the dataset, please cite their work:

```
@inproceedings{seq2act,
  title = {Mapping Natural Language Instructions to Mobile UI Action Sequences},
  author = {Yang Li and Jiacong He and Xin Zhou and Yuan Zhang and Jason Baldridge},
  booktitle = {Annual Conference of the Association for Computational Linguistics (ACL 2020)},
  year = {2020},
  url = {https://www.aclweb.org/anthology/2020.acl-main.729.pdf},
}
```

## Dataset files

The generated AndroidHowTo dataset is available in the ```androidhowto_dataset``` folder. The downloaded files needed for generating this dataset in folder ```prep```. If you want to generate the dataset yourself, follow the steps below.

### Running the code to generate AndroidHowTo dataset:

Download all the files in used_warc.paths

```
python download_and_extract.py
```

This will take a LONG time, come back after two days :hourglass_flowing_sand:


For each file in ```used_warc.paths``` a output file will be generated inside prep. You can find two examples there, make sure to delete those files before running the code, or else you might have problems :bug: 


After you download and parsed all the files (3,414 in total), you can merge all the files into one, by running:

```
python merge_files.py
```

The output file is ```crawled_output.json```.

Then, generate the TFrecords by running:

```

python -m seq2act.data_generation.create_commoncrawl_dataset \
--input_instruction_json_file="crawled_output.json" \
--input_csv_file="common_crawl_annotation.csv" \
--vocab_file="commoncrawl_rico_vocab_subtoken_44462" \
--output_dir="androidhowto_dataset/"

```