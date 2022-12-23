# HarvestApp IP Box Report

This simple script will help you create a yearly report for your `IP Box` tax relief from the HarvestApp entries.

## Usage

1. Create `.env` file from the `.env.dist` file.
2. Fill the `.env` file with the authentication credentials - https://id.getharvest.com/developers
3. Install python dependencies via `pipenv`: `pipenv install`
4. Run the script: `pipenv run python runner.py 2022` or simply `make run YEAR=2022`

> The `HARVEST_IPBOXABLE_TASK_PHRASES` environmental variables takes comma separated values. 
> Any of the provided phrases needs to be found in the Harvest task name in order to mark it as "ipboxable".
