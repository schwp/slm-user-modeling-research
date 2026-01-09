# SLM User Modeling Research
SLM User Modeling Research - Understand how can we get user information (gender, age, nationality, ...) based on its prompt

## Setup
Make sure to create/have a python environment with the requirements inside `requirements.txt`:
```bash
pip install -r requirements.txt
```

And also dont forget to download the data. A CSV file will be created in the `data/` folder:
```bash
./download_data.sh
```

## Env variable
At the root of the project, make sure you have a `.env` that follows the `.env.example` 
file format. This file only contain an Hugging Face Toekn to allow us to see the
model weights. 

To setup this token, go [Hugging Face](https://huggingface.co/). Then go to your
Profile `Settings > Access Tokens`. From there create a `Read` access token and
store the value of your token inside the `.env` file.
