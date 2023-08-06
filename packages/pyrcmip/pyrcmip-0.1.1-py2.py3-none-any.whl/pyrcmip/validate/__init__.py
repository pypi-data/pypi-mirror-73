from logging import getLogger

from scmdata.run import ScmRun, df_append

from pyrcmip.readers import (
    read_protocol_scenarios,
    read_protocol_variables,
    read_results_csvs,
)

from .checks import all_checks

logger = getLogger(__name__)


def run_validation(files):
    try:
        results_df = read_results_csvs(files)
    except ValueError:
        logger.exception("Could not load data")
        raise ValueError("Data failed validation. See log for more details")

    protocol_variables = read_protocol_variables()
    protocol_scenarios = read_protocol_scenarios()

    clean_db = []
    any_failures = False

    for climatemodel, cdf in results_df.timeseries().groupby("climatemodel"):
        logger.info("checking results for climate model {}".format(climatemodel))

        any_failures_climatemodel = False

        cdf = ScmRun(cdf)

        try:
            for func_name, check in all_checks:
                logger.info(func_name)
                res = check(
                    cdf,
                    protocol_variables=protocol_variables,
                    protocol_scenarios=protocol_scenarios,
                )
                if res is not None:
                    cdf = res
        except AssertionError as e:
            logger.error(e)
            any_failures_climatemodel = True
        #     # currently not possible as groups weren't told to obey variable hierarchy,
        #     # add this in phase 2
        #     for v_top in cdf_converted_units.filter(level=0)["variable"].unique():
        #         print(v_top)
        #         cdf_pyam = cdf_converted_units.filter(variable="{}*".format(v_top)).timeseries()
        #         cdf_pyam.columns = cdf_pyam.columns.map(lambda x: x.year)

        #         cdf_consistency_checker = pyam.IamDataFrame(cdf_pyam)
        #         if cdf_consistency_checker.check_internal_consistency() is not None:
        #             print("Failed for {}".format(v_top))
        #             any_failures_climatemodel = True
        #             failing_set = cdf_consistency_checker.copy()

        if not any_failures_climatemodel:
            clean_db.append(cdf)
            logger.info("All clear for {}".format(climatemodel))
        else:
            logger.error("Failed {}".format(climatemodel))
            any_failures = True
    if any_failures:
        logger.error("database isn't ready yet")
        raise ValueError("Data failed validation. See log for more details")
    else:
        return df_append(clean_db)
