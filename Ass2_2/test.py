import numpy as np
import json
with open("./outputs/part_3_output.json", "r") as f:
    arjun = json.load(f)
    arjun = arjun["r"]
with open("part_3_output2.json", "r") as f1:
    harsha = json.load(f1)
    harsha = harsha["r"]
for j in range(0, 1936):
    if abs(arjun[j] - harsha[j]) >= 0.0001:
        print(arjun[j], harsha[j], j)
# for i in range(0, 600):
#     arjun[i] = np.array(arjun[i])
#     harsha[i] = np.array(harsha[i])
#     if not np.allclose(arjun[i], harsha[i]):
#         print(i)
#         for j in range(0, 1936):
#             if abs(arjun[i][j] - harsha[i][j]) >= 0.0001:
#                 print(arjun[i][j], harsha[i][j], j)

        quit()
