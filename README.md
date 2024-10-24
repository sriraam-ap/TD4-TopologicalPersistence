# TD4-TopologicalPersistence
Emails for project submission:

— steve.oudot@inria.fr  
— ringyi.li@polytechnique.edu  
— julie.mordacq@inria.fr  

# Environment
- python 3.11.2 or later
- dependencies 
    - pandas
    - pytest # No need to install if you do not run test code.

# Tests
This test code is optional for running code of Q1-Q4.
Run following code on the project root directory after installing pytest.

```
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ pwd
/home/kazetof/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ ls
LICENSE  README.md  __pycache__  examples  filtrations  persistence  requirements.txt  tests
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ PYTHONPATH=./ pytest ./tests -s
```

# Directory structure

```
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ tree
.
├── LICENSE
├── README.md
├── execution
│   └── main.py # code for timing from reading data to computing barcode
├── filtrations # directoru for data
│   ├── filtration_A.txt
│   ├── filtration_B.txt
│   ├── filtration_C.txt
│   └── filtration_D.txt
├── outputs
│   ├── barcodes
│   │   ├── barcode_filtration_A.txt
│   │   ├── barcode_filtration_B.txt
│   │   └── barcode_filtration_C.txt
│   └── results_of_timing.txt
├── persistence
│   ├── __init__.py
│   ├── boundary_matrix.py
│   ├── compute_barcode.py
│   ├── persistence.py
│   └── reduce_boundary_matrix.py
├── requirements.txt
└── tests # test code is optional for TD, you can run the code without this directory.
    ├── test_boundary_matrix.py
    ├── test_reduce_boundary_matrix.py
    └── testcases
        ├── filtration_1.txt
        └── filtration_2.txt
```

# How to execute
1. Put filtrations data in filtrations directories with the names of `filtration_A.txt`, `filtration_B.txt`, `filtration_C.txt`, and `filtration_D.txt`.
2. to run timing code, execute `main.py` like below on the project root directory.
3. You have generated barcodes in `outputs/barcode` and timing result in `outputs/results_of_timing.txt`

```
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ pwd
/home/kazetof/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ ls
LICENSE  README.md  drafts  execution  filtrations  outputs  persistence  requirements.txt  tests
kazetof@inspiron:~/Works/IPParis/TDA/TD4/TD4-TopologicalPersistence$ PYTHONPATH=./ python ./execution/main.py
```