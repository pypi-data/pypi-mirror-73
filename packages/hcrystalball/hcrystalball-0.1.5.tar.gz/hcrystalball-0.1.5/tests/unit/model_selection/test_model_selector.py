from hcrystalball.model_selection import ModelSelector
from hcrystalball.utils import generate_multiple_tsdata
from hcrystalball.wrappers import get_sklearn_wrapper
from sklearn.linear_model import LinearRegression
from hcrystalball.model_selection import load_model_selector
import os
import pytest


def test_model_selector(tmp_path):

    n_regions = 1
    n_plants = 1
    n_products = 2
    target_col_name = "Quantity"
    persist_path = os.path.join(tmp_path, "results")

    df = generate_multiple_tsdata(n_dates=200, n_regions=n_regions, n_plants=n_plants, n_products=n_products)
    ms = ModelSelector(frequency="D", horizon=1, country_code_column="Country")

    with pytest.raises(ValueError):
        ms.results
    with pytest.raises(ValueError):
        ms.partitions
    with pytest.raises(ValueError):
        ms.stored_path
    with pytest.raises(ValueError):
        ms.get_result_for_partition(partition="non existing partition")
    assert ms.horizon == 1

    ms.create_gridsearch(
        n_splits=1,
        prophet_models=True,
        sklearn_models=False,
        sklearn_models_optimize_for_horizon=False,
        autosarimax_models=False,
        tbats_models=False,
        exp_smooth_models=False,
        average_ensembles=False,
        stacking_ensembles=False,
        exog_cols=["Raining"],
    )
    assert hasattr(ms, "grid_search")
    ms.add_model_to_gridsearch(get_sklearn_wrapper(LinearRegression))
    ms.select_model(
        df=df, target_col_name=target_col_name, partition_columns=["Region", "Plant", "Product"],
    )

    assert len(ms.results) == n_regions * n_plants * n_products
    assert len(ms.partitions) == n_regions * n_plants * n_products

    ms.persist_results(persist_path)

    print(ms.partitions)

    ms_load = load_model_selector(folder_path=persist_path)

    # we do not ensure the same order of results and partitions after loading,
    # thus checking they are all there
    assert all([partition in ms_load.partitions for partition in ms.partitions])
    # TODO redefine __eq__ for ModelSelectorResult to str(MSR).__dict__?
    assert all(
        [
            str(ms_load.get_result_for_partition(partition).__dict__)
            == str(ms.get_result_for_partition(partition).__dict__)
            for partition in ms.partitions
        ]
    )
    assert ms.horizon == ms_load.horizon
    assert ms.frequency == ms_load.frequency

    ms.plot_best_wrapper_classes()
    ms.plot_results()
    assert "ModelSelector" in repr(ms)
    assert "ModelSelectorResults" in repr(ms)
    assert "ModelSelectorResult" in repr(ms.results[0])

    with pytest.raises(ValueError):
        ms.results[0].persist(attribute_name="non_existing_attribute")

    assert ms.results[0].cv_splits_overlap is False

    ms.results[0].plot_error()
