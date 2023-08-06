from pprint import pprint

from scmdata import ScmRun


def check_all_scenarios_as_in_protocol(df_to_check, protocol_scenarios, **kwargs):
    checker_df = df_to_check["scenario"].to_frame()
    merged_df = checker_df.merge(protocol_scenarios[["scenario"]])
    assert len(merged_df) == len(checker_df), set(checker_df["scenario"]) - set(
        merged_df["scenario"]
    )
    return df_to_check


def check_all_variables_and_units_as_in_protocol(
    df_to_check, protocol_variables, **kwargs
):
    checker_df = df_to_check.filter(variable="*Other*", keep=False).meta[
        ["variable", "unit"]
    ]
    checker_df["unit"] = checker_df["unit"].apply(
        lambda x: x.replace("dimensionless", "Dimensionless")
        if isinstance(x, str)
        else x
    )

    def strip_quantile(inv):
        if any([inv.endswith(suf) for suf in ["quantile", "mean", "stddev"]]):
            return "|".join(inv.split("|")[:-1])

        return inv

    checker_df["variable"] = checker_df["variable"].apply(strip_quantile)
    merged_df = checker_df.merge(protocol_variables[["variable", "unit"]])
    try:
        assert len(merged_df) == len(checker_df)
    except AssertionError:  # pragma: no cover
        pprint(set(checker_df["variable"]) - set(protocol_variables["variable"]))
        pprint(set(checker_df["unit"]) - set(protocol_variables["unit"]))
        raise


def unify_units(in_df, protocol_variables, **kwargs):
    out_df = in_df.copy()

    def get_units(v):
        try:
            return protocol_variables[protocol_variables["variable"] == v]["unit"].iloc[
                0
            ]
        except Exception:
            raise AssertionError(f"Failed to find unit for {variable}")

    for variable in out_df["variable"].unique():
        if variable.startswith("Radiative Forcing|Anthropogenic|Albedo Change"):
            target_unit = get_units("Radiative Forcing|Anthropogenic|Albedo Change")

        elif variable.startswith(
            "Effective Radiative Forcing|Anthropogenic|Albedo Change"
        ):
            target_unit = get_units(
                "Effective Radiative Forcing|Anthropogenic|Albedo Change"
            )

        elif variable.startswith("Carbon Pool"):
            target_unit = get_units("Carbon Pool|Atmosphere")

        elif "Other" in variable:
            target_unit = get_units("{}".format(variable.split("|Other")[0]))

        elif any([variable.endswith(suf) for suf in ["quantile", "mean", "stddev"]]):
            target_unit = get_units("|".join(variable.split("|")[:-1]))
        else:
            target_unit = get_units(variable)

        try:
            if "CH4" in target_unit:
                out_df = out_df.convert_unit(
                    target_unit, variable=variable, context="CH4_conversions"
                )
            elif "NOx" in target_unit:
                out_df = out_df.convert_unit(
                    target_unit, variable=variable, context="NOx_conversions"
                )
            else:
                if target_unit == "Dimensionless":
                    target_unit = "dimensionless"

                out_df = out_df.convert_unit(target_unit, variable=variable)
        except Exception:  # pragma: no cover
            current_unit = out_df.filter(variable=variable)["unit"].unique()
            raise AssertionError(
                f"Failed for {variable} with target unit: {target_unit} and current_unit: {current_unit}"
            )

    out_df = out_df.timeseries().reset_index()
    out_df["unit_context"] = out_df["unit_context"].fillna("not_required")
    return ScmRun(out_df)


all_checks = [
    ("fix_units", unify_units),
    ("check_scenarios", check_all_scenarios_as_in_protocol),
    ("check_variables", check_all_variables_and_units_as_in_protocol),
]
