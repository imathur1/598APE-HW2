import numpy as np
import matplotlib.pyplot as plt
from collections import OrderedDict

optimizations = OrderedDict([
    ("Baseline", {
        "Diabetes": [9.832242233, 9.898433960, 9.930509535],
        "Cancer":   [108.299985386, 109.120835589, 107.841465908],
        "Housing":  [289.125258301, 291.045838926, 295.082400119]
    }),
    ("Clang++ -O3", {
        "Diabetes": [0.961290797, 0.954295434, 0.953475269],
        "Cancer":   [19.079862055, 19.058465229, 19.057118075],
        "Housing":  [30.505952716, 30.396710262, 30.456433594]
    }),
    ("Compiler warnings", {
        "Diabetes": [0.913525763, 0.912697225, 0.912179028],
        "Cancer":   [18.565376548, 18.414447790, 18.499392435],
        "Housing":  [29.038928183, 28.916525375, 28.945862936]
    }),
    ("Log Loss", {
        "Diabetes": [0.913525763, 0.912697225, 0.912179028],
        "Cancer":   [18.005562139, 18.009735141, 17.997030449],
        "Housing":  [29.038928183, 28.916525375, 28.945862936]
    }),
    ("Evaluate_node", {
        "Diabetes": [0.797680795, 0.798880122, 0.798274934],
        "Cancer":   [16.913134362, 16.879334632, 16.868307628],
        "Housing":  [25.710224412, 25.667361269, 25.699842317]
    }),
    ("-march=native & -O2", {
        "Diabetes": [1.880102764, 1.883749315, 1.868602983],
        "Cancer":   [17.741056411, 17.746970849, 17.735036280],
        "Housing":  [23.251008684, 23.331704536, 23.319383258]
    }),
    ("InsertionSort -> Top2", {
        "Diabetes": [1.847607730, 1.856844333, 1.847098288],
        "Cancer":   [12.940348670, 12.899241596, 12.962559413],
        "Housing":  [23.290001576, 23.281467508, 23.260473828]
    }),
    ("Parallelize", {
        "Diabetes": [0.509411440, 0.498193645, 0.495425934],
        "Cancer":   [6.809391055, 6.810639581, 6.789860196],
        "Housing":  [6.644735262, 6.639169622, 6.636613757]
    }),
    ("Misc changes", {
        "Diabetes": [0.338699212, 0.340929644, 0.339713612],
        "Cancer":   [6.050434546, 6.032045493, 6.098246422],
        "Housing":  [4.872712479, 4.763448837, 4.744498946]
    }),
    ("Metric parallelization", {
        "Diabetes": [0.354050964, 0.337726345, 0.337262932],
        "Cancer":   [3.154059077, 3.168250414, 3.177484467],
        "Housing":  [4.221863957, 4.224897459, 4.211829262]
    }),
    ("Redundant RNG modulus", {
        "Diabetes": [0.328508336, 0.331481922, 0.330373539],
        "Cancer":   [3.098728243, 3.139407175, 3.124798793],
        "Housing":  [4.365922074, 4.152621574, 4.177905029]
    })
])

datasets = ["Diabetes", "Cancer", "Housing"]

ordered_labels = list(optimizations.keys())
n_steps = len(ordered_labels)
transition_labels = [ordered_labels[i] for i in range(1, n_steps)]

# Create a dictionary to store relative speedup values for each dataset.
speedups = {ds: [] for ds in datasets}

for i in range(1, n_steps):
    prev_opt = optimizations[ordered_labels[i-1]]
    curr_opt = optimizations[ordered_labels[i]]
    for ds in datasets:
        prev_vals = prev_opt.get(ds)
        curr_vals = curr_opt.get(ds)
        prev_min = np.min(prev_vals)
        curr_min = np.min(curr_vals)
        # Relative speedup from previous step.
        speedups[ds].append(prev_min / curr_min)

for ds in datasets:
    speedups[ds] = np.array(speedups[ds])

x = np.arange(len(transition_labels))
width = 0.25

fig, ax = plt.subplots(figsize=(14, 6))

# Define offsets and colors for each dataset.
offsets = {
    "Diabetes": -width,
    "Cancer": 0,
    "Housing": width
}

colors = {
    "Diabetes": 'skyblue',
    "Cancer": 'lightgreen',
    "Housing": 'salmon'
}

for ds in datasets:
    ax.bar(x + offsets[ds], speedups[ds], width, label=ds, color=colors[ds])

ax.set_xlabel("Optimization")
ax.set_ylabel("Relative Speedup (x)")
ax.set_xticks(x)
ax.set_xticklabels(transition_labels, rotation=45, ha="right")
ax.legend()

for ds in datasets:
    for i, val in enumerate(speedups[ds]):
        ax.text(x[i] + offsets[ds], val + 0.02, f"{val:.2f}x", 
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
plt.savefig('optimization_results.png', dpi=600, bbox_inches='tight')