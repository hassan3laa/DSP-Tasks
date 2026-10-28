
def Shift_Fold_Signal(file_name, Your_indices, Your_samples):
    expected_indices = []
    expected_samples = []

    with open(file_name, "r") as f:
        f.readline()
        f.readline()
        f.readline()

        for line in f:
            data = line.split()

            if len(data) >= 2:
                expected_indices.append(int(data[0]))
                expected_samples.append(float(data[1]))

    print("Current Output Test file is:")
    print(file_name)

    if (
        len(expected_indices) != len(Your_indices)
        or len(expected_samples) != len(Your_samples)
    ):
        print(
            "Shift_Fold_Signal Test case failed: "
            "your signal has a different length from the expected one"
        )
        return

    for i in range(len(Your_indices)):
        if Your_indices[i] != expected_indices[i]:
            print(
                "Shift_Fold_Signal Test case failed: "
                "your signal has different indices from the expected one"
            )
            return

    for i in range(len(Your_samples)):
        if abs(Your_samples[i] - expected_samples[i]) >= 0.01:
            print(
                "Shift_Fold_Signal Test case failed: "
                "your signal has different values from the expected one"
            )
            return

    print("Shift_Fold_Signal Test case passed successfully")
