import pandas as pd
import pkg_resources
from scmdata.run import ScmRun, df_append

SUBMISSION_TEMPLATE = "data/rcmip-data-submission-template-v4-0-0.xlsx"


def read_results_csvs(results):
    """

    Parameters
    ----------
    results: str or list of str
        Files to read in. All files to be read should be formatted as CSV or XLSX files following the formatting
        defined in the template spreadsheet.

    Returns
    -------
        `scmdata.ScmDataFrame
    """
    if isinstance(results, str):
        results = [results]

    db = []
    for rf in results:
        if rf.endswith(".csv"):
            loaded = ScmRun(rf)
        else:
            loaded = ScmRun(rf, sheet_name="your_data")
        db.append(loaded)

    db = df_append(db).timeseries().reset_index()
    db = ScmRun(db)
    return db


def read_protocol_variables():
    stream = pkg_resources.resource_stream(__name__, SUBMISSION_TEMPLATE)
    protocol_variables = pd.read_excel(stream, sheet_name="variable_definitions")
    protocol_variables.columns = protocol_variables.columns.str.lower()

    return protocol_variables


def read_protocol_scenarios():
    stream = pkg_resources.resource_stream(__name__, SUBMISSION_TEMPLATE)
    protocol_scenarios = pd.read_excel(stream, sheet_name="scenario_info")
    protocol_scenarios.columns = protocol_scenarios.columns.str.lower()

    return protocol_scenarios
