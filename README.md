# SurfDispMap
A workflow for computing 3D surface-wave phase/group velocity maps from a 3D Vs model based on the surfdisp96 package from CPS.

This program combines Python preprocessing scripts with the CPS surface-wave forward modeling tool to automatically generate synthetic surface-wave dispersion maps (use them directly) and export them into MATLAB-readable formats compatible with [**EGFAnalysisTimeFreq_version_2024**](https://github.com/Ycpan-seis/EGFAnalysisTimeFreq_version_2024).

---

# 🔧 Dependencies

- Linux/Mac (gfortran)
- Python 3 (numpy,scipy)

---
# 📂 Project Structure

```text
SurfDispMap/
│
├── bin/                # surfdisp executable
├── src/                # Source scripts
├── OUTPUT/             # Output files
├── SurfMap.sh          # Main file 
├── SurfMap.in          # Input parameter file
├── Vs.txt              # reference Vs model
└── README.md
```

---

# ⚙️ Compile

Compile the CPS forward modeling code:

```bash
make
```

After compilation, the executable file will be generated 

```text
./bin/surfdisp
```

---

# 📥 Prepare the Reference Vs Model

Prepare a reference 3D shear-wave velocity model  
(example: `USTClithoTB.txt`).

## Format

```text
longitude(°) latitude(°) depth(km) Vs(km/s)
```

## Example

```text
90.0000 23.0000 0.00 2.6650
90.5000 23.0000 0.00 2.6680
```

---

# 📝 Prepare the Input File

Edit:

```text
SurfMap.in
```

## Parameters

| Parameter | Description |
|---|---|
| `model_in` | Reference Vs model |
| `nx, ny, nz` | Grid number in longitude, latitude, and depth directions |
| `depth` | Maximum depth of the model |
| `thick` | Thickness of each interpolated layer |
| `ifunc` | Wave type (`1`: Love wave, `2`: Rayleigh wave) |
| `mode` | Surface-wave mode (`1`: fundamental mode) |
| `kmax` | Number of periods |
| `dT` | Period interval |
| `periods` | Periods used in forward modeling |
| `Tstart` | Starting period |
| `xstart, ystart` | Starting longitude and latitude |
| `dx, dy` | Grid spacing in longitude and latitude |
| `ref` | Reference range (percentage) |

---

# ▶️ Run the Workflow

After preparing all input files, simply run:

```bash
sh SurfMap.sh
```

The workflow will automatically execute:

```text
3D Vs Model
    ↓
process.py
    ↓
surfdisp96
    ↓
process2.py
    ↓
convert_to_mat.py
    ↓
SurfDisp.mat
```

---

# 📤 Output Files

All output files are generated in:

```text
OUTPUT/
```

---

## 1. Dispersion Data

### Files

```text
disp_all_phase.txt
disp_all_group.txt
```

These files contain the forward-modeled:

- phase velocity dispersion
- group velocity dispersion

ordered according to the grid sequence of the reference Vs model.

---

## Format

```text
period(s) velocity(km/s)
```

## Example

```text
5.000000000000000000e+00 3.050875190000000181e+00
6.000000000000000000e+00 3.094695329999999966e+00
7.000000000000000000e+00 3.128513569999999966e+00
```

---

## 2. MATLAB Output

### File

```text
SurfDisp.mat
```

This file packages the forward-modeled surface-wave dispersion maps into MATLAB `.mat` format.

The output format is compatible with:

https://github.com/Ycpan-seis/EGFAnalysisTimeFreq_version_2024

---


# Reference


