from src.psb_modules.classification import PSDClassification


c = PSDClassification('./psb_v1/benchmark/classification')
print(c.base_test[2].models_in_class)