from comptests import (comptests_for_all, comptests_for_all_dynamic,
    comptests_for_all_pairs, comptests_for_all_pairs_dynamic, comptests_for_some,
    comptests_for_some_pairs)
from example_package import (get_conftools_example_class1,
    get_conftools_example_class2)

library_class1 = get_conftools_example_class1()
library_class2 = get_conftools_example_class2()

for_all_class1 = comptests_for_all(library_class1)
for_some_class1 = comptests_for_some(library_class1)
for_some_class1_class2 = comptests_for_some_pairs(library_class1, library_class2)

for_all_class1_class2 = comptests_for_all_pairs(library_class1, library_class2)
for_all_class1_dynamic = comptests_for_all_dynamic(library_class1)
for_all_class1_class2_dynamic = comptests_for_all_pairs_dynamic(library_class1, library_class2)

